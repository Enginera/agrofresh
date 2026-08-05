# ==============================================================================
# 1. СИСТЕМНЫЙ ФИКС БАГА GZIP STARLETTE НА PYTHON 3.14
# ==============================================================================
try:
    import starlette.middleware.gzip as st_gzip
    orig_init = st_gzip.GZipResponder.__init__
    def patched_init(self, *args, **kwargs):
        kwargs.setdefault('thread_minimum_size', 1024 * 1024)
        return orig_init(self, *args, **kwargs)
    st_gzip.GZipResponder.__init__ = patched_init
except Exception:
    pass

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="AgriCarbon Manager", page_icon="🌱")

st.markdown("""
<style>
.stApp { background-color: #F8F9FA; }
h1, h2, h3 { color: #1A1A1A !important; font-family: 'Inter', sans-serif !important; font-weight: 600 !important; }
.metric-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB; box-shadow: 0 4px 12px rgba(0,0,0,0.03); transition: all 0.3s ease; }
.metric-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.06); }
.status-badge { padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 500; display: inline-block; }
.status-success { background-color: #E8F5E9; color: #2E7D32; }
.stRadio div[role="radiogroup"] { flex-wrap: nowrap !important; overflow-x: auto !important; padding-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "Обзор"

def on_tab_change():
    st.session_state.page = st.session_state.nav_radio
# ==========================================
# 2. ИНТЕЛЛЕКТУАЛЬНЫЙ ПАРСЕР ПОД ФОРМАТ ТЗ
# ==========================================
st.sidebar.markdown("### Загрузка метаданных 📂")
uploaded_file = st.sidebar.file_uploader("Перетащите агрономическую таблицу Excel", type=["xlsx", "xls"])

@st.cache_data
def advanced_multi_field_parser(file_buffer):
    if file_buffer is None: return None
    try:
        df_sheet = pd.read_excel(file_buffer, header=None)
        parsed_fields = {}
        current_field_name = None
        accumulated_rows = []
        
        for idx, row in df_sheet.iterrows():
            cells = [str(c).strip() for c in row.values if pd.notna(c) and str(c).strip() != ""]
            if not cells: continue
            row_text_line = " ".join(cells).lower()
            
            if "поле" in row_text_line:
                if current_field_name and accumulated_rows:
                    parsed_fields[current_field_name] = pd.DataFrame(accumulated_rows)
                found_name = "Поле"
                for c in cells:
                    if "поле" in c.lower(): found_name = c.strip(); break
                current_field_name = found_name
                accumulated_rows = []
                continue
                
            if "год" in row_text_line or "культура" in row_text_line: continue
                
            if current_field_name and len(row) >= 10:
                first_cell = str(row.iloc[0]).strip().replace('.0', '')
                if first_cell.isdigit() and len(first_cell) == 4:
                    try:
                        year_val = int(first_cell)
                        def clean_float(val):
                            if pd.isna(val): return 0.0
                            try: return float(str(val).replace(',', '.').strip())
                            except: return 0.0
                                
                        accumulated_rows.append({
                            "Год": year_val,
                            "Культура": str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "Не указано",
                            "Урожайность": clean_float(row.iloc[2]),
                            "Cinputs": clean_float(row.iloc[3]),
                            "Cnet": clean_float(row.iloc[4]),
                            "Ravg": clean_float(row.iloc[5]),
                            "Площадь": clean_float(row.iloc[6]),
                            "Глубина": clean_float(row.iloc[7])
                        })
                    except Exception: continue
                        
        if current_field_name and accumulated_rows:
            parsed_fields[current_field_name] = pd.DataFrame(accumulated_rows)
            
        standardized_fields = {}
        for f_name, df_field in parsed_fields.items():
            if df_field.empty: continue
            df_field["Эффективность"] = df_field.apply(
                lambda r: round(((r["Урожайность"] * (1.0 - r["Ravg"])) / r["Cnet"]) * 10000) / 10000 if r["Cnet"] != 0 else 0.0, axis=1
            )
            standardized_fields[f_name] = df_field
        return standardized_fields
    except Exception as e:
        st.sidebar.error(f"Ошибка структуры: {e}")
        return None

def get_mock_data():
    mock_dict = {
        "Поле 1": pd.DataFrame([
            {"Год": 2021, "Культура": "Пшеница Озимая", "Урожайность": 4.2, "Cinputs": 850.0, "Cnet": 565.0, "Ravg": 0.12, "Площадь": 118.06, "Глубина": 0.3},
            {"Год": 2022, "Культура": "Многолетние травы", "Урожайность": 12.4, "Cinputs": 410.0, "Cnet": -215.0, "Ravg": 0.05, "Площадь": 118.06, "Глубина": 0.3},
            {"Год": 2023, "Культура": "Кукуруза на силос", "Урожайность": 35.0, "Cinputs": 920.0, "Cnet": 590.0, "Ravg": 0.08, "Площадь": 118.06, "Глубина": 0.3}
        ])
    }
    for f_name, df in mock_dict.items():
        df["Эффективность"] = df.apply(lambda r: round(((r["Урожайность"] * (1.0 - r["Ravg"])) / r["Cnet"]) * 10000) / 10000 if r["Cnet"] != 0 else 0.0, axis=1)
    return mock_dict

file_data = advanced_multi_field_parser(uploaded_file)
all_fields_dict = file_data if file_data is not None else get_mock_data()
# ==========================================
# 3. ИНТЕРФЕЙС И 7 ОРИГИНАЛЬНЫХ ВКЛАДОК ТЗ
# ==========================================
field_options = list(all_fields_dict.keys())
selected_field = st.sidebar.selectbox("Выберите Поле для анализа: 🎯", field_options)
df_active = all_fields_dict[selected_field]

area_value = f"{df_active['Площадь'].iloc[0]:.2f} га" if len(df_active) > 0 else "118.06 га"
depth_value = f"{df_active['Глубина'].iloc[0]:.2f} м" if len(df_active) > 0 else "0.30 м"
avg_e_calculated = df_active['Эффективность'].mean()

tabs = ["Обзор", "Севооборот", "Удобрения и почва", "Защита растений", "Урожайность и качество", "Углеродный след", "Принятие решений"]
st.radio("", tabs, index=tabs.index(st.session_state.page) if st.session_state.page in tabs else 0, horizontal=True, label_visibility="collapsed", key="nav_radio", on_change=on_tab_change)
st.markdown("---")

if st.session_state.page == "Обзор":
    st.markdown(f"<div class='metric-card' style='border-left: 5px solid #2E7D32;'><h2>Объект анализа: {selected_field}</h2><p>Состояние подсистем комплекса.</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='metric-card'><b>Средняя эффективность E</b><h3>{avg_e_calculated:.4f}</h3></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='metric-card'><b>Углеродный баланс</b><h3>Прогресс 85%</h3></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='metric-card'><b>Агросроки</b><h3>{len(df_active)} записей</h3></div>", unsafe_allow_html=True)

elif st.session_state.page == "Севооборот":
    st.subheader(f"Анализ севооборота — {selected_field}")
    fig_sev_trend = go.Figure(go.Scatter(x=df_active["Год"], y=df_active["Эффективность"], mode='lines+markers', line=dict(shape='spline', color='#2E7D32', width=4)))
    fig_sev_trend.update_layout(plot_bgcolor='white', height=300)
    fig_sev_trend.update_xaxes(type='category')
    st.plotly_chart(fig_sev_trend, use_container_width=True)

elif st.session_state.page == "Удобрения и почва":
    st.subheader(f"Управление почвенным слоем — {selected_field}")
    st.markdown(f"<div class='metric-card'>Глубина пласта: {depth_value} | Площадь: {area_value}</div>", unsafe_allow_html=True)
    fig1 = px.bar(df_active, x="Год", y="Cinputs", color_discrete_sequence=['#2E7D32'])
    fig1.update_layout(height=250, plot_bgcolor='white')
    fig1.update_xaxes(type='category')
    st.plotly_chart(fig1, use_container_width=True)

elif st.session_state.page == "Защита растений":
    st.subheader(f"Коэффициент рисков Ravg — {selected_field}")
    fig_prot = go.Figure(go.Scatter(x=df_active["Год"], y=df_active["Ravg"], mode='lines+markers', line=dict(shape='spline', color='#C62828', width=3)))
    fig_prot.update_layout(height=300, plot_bgcolor='white')
    fig_prot.update_xaxes(type='category')
    st.plotly_chart(fig_prot, use_container_width=True)

elif st.session_state.page == "Урожайность и качество":
    st.subheader(f"Распределение урожайности по годам (т/га) — {selected_field}")
    fig_factors = px.bar(df_active, x="Год", y="Урожайность", text_auto='.2f', color_discrete_sequence=['#2E7D32'])
    fig_factors.update_layout(height=280, plot_bgcolor='white')
    fig_factors.update_xaxes(type='category')
    st.plotly_chart(fig_factors, use_container_width=True)

elif st.session_state.page == "Углеродный след":
    st.subheader(f"Моделирование чистого следа Cnet — {selected_field}")
    fig_cnet = px.area(df_active, x="Год", y="Cnet", color_discrete_sequence=['#78909C'])
    fig_cnet.update_layout(plot_bgcolor='white', height=300)
    fig_cnet.update_xaxes(type='category')
    st.plotly_chart(fig_cnet, use_container_width=True)

elif st.session_state.page == "Принятие решений":
    st.subheader(f"Расчетная матрица севооборота — {selected_field}")
    df_display = df_active[["Год", "Культура", "Урожайность", "Cinputs", "Cnet", "Ravg", "Эффективность"]].copy()
    st.dataframe(df_display, use_container_width=True)
