# ХАК ДЛЯ ИСПРАВЛЕНИЯ БАГА STARLETTE GZIP НА PYTHON 3.14
try:
    import starlette.middleware.gzip as st_gzip
    orig_init = st_gzip.GZipResponder.__init__
    def patched_init(self, *args, **kwargs):
        kwargs.setdefault('thread_minimum_size', 1024 * 1024)
        orig_init(self, *args, **kwargs)
    st_gzip.GZipResponder.__init__ = patched_init
except:
    pass

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. КОНФИГУРАЦИЯ И КАСТОМНЫЕ СТИЛИ (ИЗ ТЗ)
# ==========================================
st.set_page_config(layout="wide", page_title="AgriCarbon Manager", page_icon="🌱")

st.markdown("""
<style>
.stApp { background-color: #F8F9FA; }
h1, h2, h3 { color: #1A1A1A !important; font-family: 'Inter', sans-serif !important; font-weight: 600 !important; }
.metric-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB; box-shadow: 0 4px 12px rgba(0,0,0,0.03); transition: all 0.3s ease; }
.metric-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.06); }
.status-badge { padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 500; display: inline-block; }
.status-success { background-color: #E8F5E9; color: #2E7D32; }
.status-process { background-color: #E3F2FD; color: #1565C0; }
.status-warning { background-color: #FFF3E0; color: #EF6C00; }
.status-danger { background-color: #FFEBEE; color: #C62828; }
.stRadio div[role="radiogroup"] { flex-wrap: nowrap !important; overflow-x: auto !important; padding-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "Обзор"

def on_tab_change():
    st.session_state.page = st.session_state.nav_radio

# ==========================================
# 2. АДАПТИВНЫЙ ИНТЕЛЛЕКТУАЛЬНЫЙ ПАРСЕР ПОД ФОРМАТ ТЗ
# ==========================================
st.sidebar.markdown("### 📂 Загрузка метаданных")
uploaded_file = st.sidebar.file_uploader("Перетащите агрономическую таблицу Excel", type=["xlsx", "xls"])

@st.cache_data
def advanced_multi_field_parser(file_buffer):
    if file_buffer is None:
        return None
    try:
        # Считываем сырой лист без автоматических заголовков
        df_sheet = pd.read_excel(file_buffer, header=None)
        
        parsed_fields = {}
        current_field_name = None
        accumulated_rows = []
        
        for idx, row in df_sheet.iterrows():
            # Превращаем строку ячеек в очищенный список строк
            cells = [str(c).strip() for c in row.values if pd.notna(c) and str(c).strip() != ""]
            if not cells:
                continue
                
            row_text_line = " ".join(cells).lower()
            
            # 1. Детекция заголовка начала нового Поля
            if "поле" in row_text_line:
                if current_field_name and accumulated_rows:
                    parsed_fields[current_field_name] = pd.DataFrame(accumulated_rows)
                
                # Извлекаем чистое имя, например "Поле 1"
                found_name = "Поле"
                for c in cells:
                    if "поле" in c.lower():
                        found_name = c.strip()
                        break
                current_field_name = found_name
                accumulated_rows = []
                continue
            
            # Пропускаем служебные строки с индексами колонок (например 1 2 3 .. 10) или шапки таблиц
            if "год" in row_text_line or "культура" in row_text_line or (len(cells) >= 5 and cells[0] == "1" and cells[1] == "2"):
                continue
            
            # 2. Сбор данных (строка должна начинаться с валидного четырехзначного года)
            if current_field_name and len(row) >= 10:
                first_cell = str(row.iloc[0]).strip().replace('.0', '')
                if first_cell.isdigit() and len(first_cell) == 4:
                    try:
                        year_val = int(first_cell)
                        if 2020 <= year_val <= 2035:
                            
                            # Безопасная функция кастинга строк в формат float
                            def clean_float(val):
                                if pd.isna(val): return 0.0
                                s = str(val).replace(',', '.').strip()
                                try: return float(s)
                                except: return 0.0

                            accumulated_rows.append({
                                "Год": year_val,
                                "Культура": str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "Не указано",
                                "Урожайность": clean_float(row.iloc[2]),
                                "Cinputs": clean_float(row.iloc[3]),
                                "Cnet": clean_float(row.iloc[6]),
                                "Ravg": clean_float(row.iloc[7]),
                                "Площадь": clean_float(row.iloc[8]),
                                "Глубина": clean_float(row.iloc[9])
                            })
                    except:
                        continue
                        
        # Запись последнего блока данных из цикла
        if current_field_name and accumulated_rows:
            parsed_fields[current_field_name] = pd.DataFrame(accumulated_rows)
            
        # Нормализация данных и расчет финального коэффициента E
        standardized_fields = {}
        for f_name, df_field in parsed_fields.items():
            if df_field.empty:
                continue
                
            # Математический расчет индекса эффективности E по формуле F1.1 из ТЗ
            df_field["Эффективность"] = df_field.apply(
                lambda r: round(((r["Урожайность"] * (1.0 - r["Ravg"])) / r["Cnet"]) * 10000) / 10000 if r["Cnet"] != 0 else 0.0,
                axis=1
            )
            standardized_fields[f_name] = df_field
            
        return standardized_fields
    except Exception as e:
        st.sidebar.error(f"Ошибка парсинга структуры: {e}")
        return None

all_fields_dict = advanced_multi_field_parser(uploaded_file)
# ==========================================
# 3. МАРШРУТИЗАЦИЯ СТРАНИЦ: ВКЛАДКИ 1 - 4
# ==========================================

# Блокируем весь интерфейс, если файл Excel еще не загружен пользователем вручную
if all_fields_dict is None or not all_fields_dict:
    st.info("💡 **Для начала работы перетащите Excel-файл со структурой ТЗ через боковую панель слева.**")
    st.markdown("""
    <br>
    <div class='metric-card' style='text-align: center; padding: 40px; color: #4B5563; border-top: 4px solid #2E7D32;'>
        <h2>🌱 Нативный аналитический комплекс AgriCarbon Core OS</h2>
        <p style='font-size: 15px; margin-top: 10px;'>Алгоритм адаптирован под многострочный сквозной формат таблиц ТЗ.<br>
        После загрузки система автоматически выделит блоки Полей (Поле 1, Поле 2 ...), преобразует типы данных, рассчитает коэффициенты декарбонизации и построит графики.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Динамический селектор полей на боковой панели
    field_options = list(all_fields_dict.keys())
    selected_field = st.sidebar.selectbox("🎯 Выберите Поле для анализа:", field_options)
    
    # Ссылка на активный датафрейм по выбранному полю
    df_active = all_fields_dict[selected_field]
    
    # Расчет глобальных переменных для KPI карт на основе Excel
    area_value = f"{df_active['Площадь'].iloc[0]:.2f} га" if len(df_active) > 0 else "Не указана"
    depth_value = f"{df_active['Глубина'].iloc[0]:.2f} м" if len(df_active) > 0 else "Не указана"
    avg_e_calculated = df_active['Эффективность'].mean()

    # Отрисовываем меню навигации (строго 7 оригинальных вкладок из ТЗ)
    tabs = ["Обзор", "Севооборот", "Удобрения и почва", "Защита растений", "Урожайность и качество", "Углеродный след", "Принятие решений"]
    
    st.radio(
        "", 
        tabs, 
        index=tabs.index(st.session_state.page) if st.session_state.page in tabs else 0, 
        horizontal=True, 
        label_visibility="collapsed",
        key="nav_radio",
        on_change=on_tab_change
    )
    st.markdown("---")

    # --- 1. ОБЗОР (ИЗ СТРАНИЦЫ 2 PDF) ---
    if st.session_state.page == "Обзор":
        st.markdown(f"<div class='metric-card' style='background: #F1F8E9; border-left: 5px solid #2E7D32; margin-bottom: 25px;'><h2>Добро пожаловать! Объект анализа: {selected_field}</h2><p>На этой панели управления представлен обзор текущего состояния всех ваших сельскохозяйственных модулей на основе загруженных данных Excel.</p></div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("<div class='metric-card'> <b>Углеродная 🟢 нейтральность</b><br><h3 style='margin:10px 0;'>Прогресс на 85%</h3></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='metric-card'> <b>Активные проекты</b><br><h3 style='margin:10px 0;'>🚜 5 кампаний</h3></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-card'> <b>Средняя эффективность 📈 (E)</b><br><h3 style='margin:10px 0;'>{avg_e_calculated:.4f}</h3></div>", unsafe_allow_html=True)
        
        st.markdown("### Состояние модулей")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"<div class='metric-card'> <b>Планирование 🌿 севооборота</b><br><small>Текущий план: {len(df_active)} агросроков</small><br><br><span class='status-badge status-success'>В норме</span></div>", unsafe_allow_html=True)
            if st.button("Подробнее", key="b1"): st.session_state.page = "Севооборот"; st.rerun()
        with m2:
            st.markdown("<div class='metric-card'> <b>Удобрения и 🪱 почва</b><br><small>Следующее внесение: 15 мая</small><br><br><span class='status-badge status-success'>В норме</span></div>", unsafe_allow_html=True)
            if st.button("Подробнее", key="b2"): st.session_state.page = "Удобрения и почва"; st.rerun()
        with m3:
            st.markdown("<div class='metric-card'> <b>Мониторинг защиты 🛡️ растений</b><br><small>Обработка рисков Rave завершена</small><br><br><span class='status-badge status-success'>В норме</span></div>", unsafe_allow_html=True)
            if st.button("Подробнее", key="b3"): st.session_state.page = "Защита растений"; st.rerun()

    # --- 2. СЕВООБОРОТ (ИЗ СТРАНИЦЫ 2-3 PDF) ---
    elif st.session_state.page == "Севооборот":
        st.subheader(f"🔄 Планирование и анализ севооборота — {selected_field}")
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        with kpi_col1: st.markdown(f"<div class='metric-card'> <b>Общая 📐 площадь</b><br><h2>{area_value}</h2></div>", unsafe_allow_html=True)
        with kpi_col2: st.markdown(f"<div class='metric-card'> <b>Количество записей</b><br><h2>{len(df_active)} активных</h2></div>", unsafe_allow_html=True)
        with kpi_col3: st.markdown(f"<div class='metric-card'> <b>Средняя эффективность 📈 (E)</b><br><h2>{avg_e_calculated:.4f}</h2></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        g_left, g_right = st.columns(2)
        with g_left:
            st.subheader("📊 Распределение объемов по культурам")
            df_pie = df_active.groupby("Культура")["Урожайность"].sum().reset_index()
            fig_sev_pie = px.pie(df_pie, names="Культура", values="Урожайность", hole=0.4, color_discrete_sequence=px.colors.qualitative.Dark2)
            fig_sev_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_sev_pie, use_container_width=True)
        with g_right:
            st.subheader("📉 Динамика индекса эффективности по годам")
            fig_sev_trend = go.Figure(go.Scatter(x=df_active["Год"], y=df_active["Эффективность"], mode='lines+markers', line=dict(shape='spline', color='#2E7D32', width=4)))
            fig_sev_trend.update_layout(plot_bgcolor='white', height=300, margin=dict(l=10, r=10, t=40, b=10))
            fig_sev_trend.update_xaxes(type='category', showgrid=True, gridcolor='#F3F4F6')
            fig_sev_trend.update_yaxes(showgrid=True, gridcolor='#F3F4F6')
            st.plotly_chart(fig_sev_trend, use_container_width=True)

    # --- 3. УДОБРЕНИЯ И ПОЧВА (ИЗ СТРАНИЦЫ 3-4 PDF) ---
    elif st.session_state.page == "Удобрения и почва":
        st.subheader(f"🪱 Управление удобрениями и почвенным слоем — {selected_field}")
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("### Расписание внесения удобрений")
            data_ud = {"Дата": ["2026-07-20", "2026-07-15"], "Мероприятие": ["Органическое удобрение на Поле 1", "Компост на Поле 2"], "Статус": ["Предстоит", "Предстоит"]}
            st.dataframe(pd.DataFrame(data_ud), use_container_width=True)
        with col_r:
            st.markdown("<div class='metric-card' style='height:125px;'><b>Показатели почвы слоев</b><br>🧪 pH: 6.5 | 🌾 Азот: 0.12% | 🌱 Фосфор: 45 мг/кг</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        g1, g2, g3 = st.columns(3)
        with g1:
            st.markdown("**Углеродный след и секвестрация**")
            fig1 = px.bar(df_active, x="Год", y="Cinputs", color_discrete_sequence=['#2E7D32'])
            fig1.update_layout(margin=dict(l=20,r=20,t=20,b=20), height=250, plot_bgcolor='white')
            fig1.update_xaxes(type='category')
            fig1.update_yaxes(showgrid=True, gridcolor='#F3F4F6')
            st.plotly_chart(fig1, use_container_width=True)
        with g2:
            st.markdown("**Карты точного внесения (NDVI)**")
            mat_ndvi = np.array([[1, 2, 3], [3, 2, 1], [2, 1, 3]])
            fig2 = px.imshow(mat_ndvi, color_continuous_scale="YlGn")
            fig2.update_layout(margin=dict(l=20,r=20,t=20,b=20), height=250)
            st.plotly_chart(fig2, use_container_width=True)
        with g3:
            st.markdown("**Прогноз углеродного баланса**")
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=df_active["Год"], y=df_active["Cinputs"], mode='lines+markers', line=dict(shape='spline', color='#1565C0', width=3)))
            fig3.update_layout(margin=dict(l=20,r=20,t=20,b=20), height=250, plot_bgcolor='white')
            fig3.update_xaxes(type='category', showgrid=True, gridcolor='#F3F4F6')
            fig3.update_yaxes(showgrid=True, gridcolor='#F3F4F6')
            st.plotly_chart(fig3, use_container_width=True)

    # --- 4. ЗАЩИТА РАСТЕНИЙ (ИЗ СТРАНИЦЫ 4 PDF) ---
    elif st.session_state.page == "Защита растений":
        st.subheader(f"🛡️ Мониторинг защиты растений — {selected_field}")
        k1, k2 = st.columns(2)
        with k1: st.metric("Активные сессии контроля", len(df_active))
        with k2: st.metric("Процент здоровых культур", "92%")
        
        st.markdown("**Динамика коэффициента рисков Rave по годам**")
        fig_prot = go.Figure(go.Scatter(x=df_active["Год"], y=df_active["Ravg"], mode='lines+markers', line=dict(shape='spline', color='#C62828', width=3)))
        fig_prot.update_layout(height=300, plot_bgcolor='white', margin=dict(l=10, r=10, t=10, b=10))
        fig_prot.update_xaxes(type='category', showgrid=True, gridcolor='#F3F4F6')
        fig_prot.update_yaxes(showgrid=True, gridcolor='#F3F4F6')
        st.plotly_chart(fig_prot, use_container_width=True)
    # --- 5. УРОЖАЙНОСТЬ И КАЧЕСТВО (ИЗ СТРАНИЦЫ 4-5 PDF) ---
    elif st.session_state.page == "Урожайность и качество":
        st.subheader(f"🌾 Управление урожайностью и качеством продукции — {selected_field}")
        uk1, uk2, uk3 = st.columns(3)
        with uk1: st.markdown(f"<div class='metric-card'> <b>Общая урожайность</b><br><h2>{df_active['Урожайность'].sum():.2f} т</h2></div>", unsafe_allow_html=True)
        with uk2: st.markdown(f"<div class='metric-card'> <b>Максимальный сбор</b><br><h2>{df_active['Урожайность'].max():.2f} т/га</h2></div>", unsafe_allow_html=True)
        with uk3: st.markdown("<div class='metric-card'> <b>Коэффициент качества</b><br><h2>92%</h2><span style='color:blue;'>Выше среднего по отрасли</span></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        u_left, u_right = st.columns(2)
        with u_left:
            st.subheader("📋 Детализированные отчеты о качестве партий")
            df_quality = pd.DataFrame({
                "Продукт": ["Пшеница", "Кукуруза", "Соя", "Ячмень"],
                "Партия": ["2026-A", "2026-B", "2026-C", "2026-D"],
                "Содержание белка": ["12.5%", "8.2%", "38.1%", "11.0%"],
                "Влажность": ["14%", "15%", "11%", "13%"],
                "Статус": ["Отлично", "Хорошо", "Отлично", "Хорошо"]
            })
            st.dataframe(df_quality, use_container_width=True)
        with u_right:
            st.subheader("📊 Распределение урожайности по годам")
            fig_factors = px.bar(df_active, x="Год", y="Урожайность", text_auto='.2f', color_discrete_sequence=['#2E7D32'])
            fig_factors.update_layout(margin=dict(l=20,r=20,t=20,b=20), height=280, plot_bgcolor='white', xaxis_title="", yaxis_title="т/га")
            fig_factors.update_xaxes(type='category')
            fig_factors.update_yaxes(showgrid=True, gridcolor='#F3F4F6')
            st.plotly_chart(fig_factors, use_container_width=True)

    # --- 6. УГЛЕРОДНЫЙ СЛЕД (ИЗ СТРАНИЦЫ 5 PDF) ---
    elif st.session_state.page == "Углеродный след":
        st.subheader(f"☁️ Моделирование баланса декарбонизации — {selected_field}")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Чистый след Cnet (Средний)", f"{df_active['Cnet'].mean():.2f} т")
        with c2: st.metric("Внесение Cinputs (Среднее)", f"{df_active['Cinputs'].mean():.2f} кг")
        with c3: st.metric("Целевой прогноз секвестрации", "🌳 Выполнено")
        
        fig_cnet = px.area(df_active, x="Год", y="Cnet", title="Динамическая модель изменения чистого следа Cnet из Excel", color_discrete_sequence=['#78909C'])
        fig_cnet.update_layout(plot_bgcolor='white', height=400, margin=dict(l=20, r=20, t=50, b=20))
        fig_cnet.update_xaxes(type='category', showgrid=True, gridcolor='#F3F4F6')
        fig_cnet.update_yaxes(showgrid=True, gridcolor='#F3F4F6')
        st.plotly_chart(fig_cnet, use_container_width=True)

    # --- 7. ПРИНЯТИЕ РЕШЕНИЙ (ИЗ СТРАНИЦЫ 5 PDF) ---
    elif st.session_state.page == "Принятие решений":
        st.subheader(f"💡 Сводная расчетная матрица севооборота — {selected_field}")
        st.markdown("Все строки и столбцы автоматически выгружены из предоставленного Excel-документа:")
        
        available_cols = [c for c in ["Год", "Культура", "Урожайность", "Cinputs", "Cnet", "Ravg", "Эффективность"] if c in df_active.columns]
        df_display = df_active[available_cols].copy()
        
        rename_display = {
            "Год": "Год агросрока", "Культура": "Культура", 
            "Урожайность": "Урожайность (т/га)", "Cinputs": "Внесение Cinputs (кг)",
            "Cnet": "Чистый след Cnet", "Ravg": "Коэффициент Rave", "Эффективность": "Индекс эффективности (E)"
        }
        df_display = df_display.rename(columns=rename_display)
        
        if "Индекс эффективности (E)" in df_display.columns:
            st.dataframe(df_display.style.format({"Индекс эффективности (E)": "{:.4f}"}), use_container_width=True)
        else:
            st.dataframe(df_display, use_container_width=True)
