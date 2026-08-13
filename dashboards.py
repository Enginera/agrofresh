import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render_page_content(page_name, df_active, selected_field, area_value, depth_value, avg_e_calculated):
    """Отрисовывает графики и метрики. Элементы идут строго друг под другим."""
    
    # --- Вкладка 1: ОБЗОР ---
    if page_name == "Обзор":
        st.markdown(f"""
            <div class='welcome-card'>
                <h2>Добро пожаловать! Объект анализа: {selected_field}</h2>
                <p>Обзор текущего состояния сельскохозяйственных подсистем комплекса.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Верхний блок метрик
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("<div class='metric-card'><b>Углеродная 🟢<br>нейтральность</b><br><h3>Прогресс на 85%</h3></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='metric-card'><b>Active Projects 🚜</b><br><h3>5 компаний</h3></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-card'><b>Средняя эффективность 📈<br>(E)</b><br><h3>{avg_e_calculated:.4f}</h3></div>", unsafe_allow_html=True)
        
        st.markdown("### Состояние модулей")
        
        # ВОЗВРАЩАЕМ КОЛОНКИ: Упаковываем модули в сетку из 3 столбцов
        m1, m2, m3 = st.columns(3)
        with m1: st.markdown(f"<div class='metric-card module-card'><b>Планирование 🌿<br>севооборота</b><br><small>{len(df_active)} агросроков</small><br><br><span class='status-badge status-success'>В норме</span></div>", unsafe_allow_html=True)
        with m2: st.markdown("<div class='metric-card module-card'><b>Удобрения и 🪱<br>почва</b><br><small>Стабильная секвестрация</small><br><br><span class='status-badge status-success'>В норме</span></div>", unsafe_allow_html=True)
        with m3: st.markdown("<div class='metric-card module-card'><b>Мониторинг защиты 🛡️<br>растений</b><br><small>Риски Rave рассчитаны</small><br><br><span class='status-badge status-success'>В норме</span></div>", unsafe_allow_html=True)

    # --- Вкладка 2: СЕВООБОРОТ ---
    elif page_name == "Севооборот":
        st.subheader(f"Планирование and анализ севооборота — 🔄 {selected_field}")
        
        st.markdown(f"<div class='metric-card' style='margin-bottom:10px;'><b>Общая 📐 площадь</b><h3>{area_value}</h3></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card' style='margin-bottom:10px;'><b>Количество записей</b><h3>{len(df_active)} активных</h3></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card' style='margin-bottom:20px;'><b>Средняя эффективность (E)</b><h3> 📈 {avg_e_calculated:.4f}</h3></div>", unsafe_allow_html=True)
        
        st.subheader("Распределение объемов по культурам 📊")
        df_pie = df_active.groupby("Культура")["Урожайность"].sum().reset_index()
        
        fig_sev_pie = px.pie(
            df_pie, 
            names="Культура", 
            values="Урожайность", 
            hole=0.4, 
            color_discrete_sequence=px.colors.qualitative.Dark2
        )
        
        fig_sev_pie.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5
            )
        )
        
        fig_sev_pie.update_traces(
            textinfo='percent+label', 
            textposition='inside',
            domain=dict(x=[0.035, 0.965], y=[0.035, 0.965])
        )
        st.plotly_chart(fig_sev_pie, use_container_width=True)
        
        st.subheader("Динамика индекса эффективности по годам 📉")
        fig_sev_trend = go.Figure(go.Scatter(x=df_active["Год"], y=df_active["Эффективность"], mode='lines+markers', line=dict(shape='spline', color='#2E7D32', width=4)))
        fig_sev_trend.update_layout(plot_bgcolor='white', height=300)
        fig_sev_trend.update_xaxes(type='category', showgrid=True, gridcolor='#F3F4F6')
        st.plotly_chart(fig_sev_trend, use_container_width=True)

    # --- Вкладка 3: УДОБРЕНИЯ И ПОЧВА ---
    elif page_name == "Удобрения и почва":
        st.subheader(f"Управление удобрениями и почвенным слоем — 🪱 {selected_field}")
        
        st.markdown("### Расписание внесения удобрений")
        data_ud = {"Дата": ["2026-07-20", "2026-07-15"], "Мероприятие": ["Органическое удобрение на Поле 1", "Компост на Поле 2"], "Статус": ["Предстоит", "Предстоит"]}
        st.dataframe(pd.DataFrame(data_ud), use_container_width=True)
        
        st.markdown(f"<div class='metric-card' style='margin-top:15px; margin-bottom:25px;'><b>Показатели почвы слоев 🧪</b><br> Глубина пласта: {depth_value} | pH: 6.5 | Азот: 0.12%</div>", unsafe_allow_html=True)
        
        st.markdown("**Внесение углерода (Cinputs)**")
        fig1 = px.bar(df_active, x="Год", y="Cinputs", color_discrete_sequence=['#2E7D32'])
        fig1.update_layout(height=250, plot_bgcolor='white')
        fig1.update_xaxes(type='category')
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown("**Карты точного внесения (NDVI)**")
        mat_ndvi = np.array([[0.2, 0.4, 0.6], [0.4, 0.8, 0.5], [0.3, 0.6, 0.7]])
        fig2 = px.imshow(mat_ndvi, color_continuous_scale="YlGn")
        fig2.update_layout(height=250)
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("**Прогноз углеродного баланса**")
        fig3 = go.Figure(go.Scatter(x=df_active["Год"], y=df_active["Cinputs"], mode='lines+markers', line=dict(shape='spline', color='#1565C0', width=3)))
        fig3.update_layout(height=250, plot_bgcolor='white')
        fig3.update_xaxes(type='category')
        st.plotly_chart(fig3, use_container_width=True)

    # --- Вкладка 4: ЗАЩИТА РАСТЕНИЙ ---
    elif page_name == "Защита растений":
        st.subheader(f"Мониторинг защиты растений — 🛡️ {selected_field}")
        st.metric("Active сессии контроля", len(df_active))
        st.metric("Процент здоровых культур", "92%")
        st.markdown("**Динамика коэффициента рисков Ravg по годам**")
        fig_prot = go.Figure(go.Scatter(x=df_active["Год"], y=df_active["Ravg"], mode='lines+markers', line=dict(shape='spline', color='#C62828', width=3)))
        fig_prot.update_layout(height=300, plot_bgcolor='white')
        fig_prot.update_xaxes(type='category')
        st.plotly_chart(fig_prot, use_container_width=True)

    # --- Вкладка 5: УРОЖАЙНОСТЬ И КАЧЕСТВО ---
    elif page_name == "Урожайность и качество":
        st.subheader(f"Управление урожайностью и качеством продукции — 🌾 {selected_field}")
        st.markdown(f"<div class='metric-card' style='margin-bottom:10px;'><b>Общая урожайность</b><h2>{df_active['Урожайность'].sum():.2f} т</h2></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card' style='margin-bottom:10px;'><b>Максимальный сбор</b><h2>{df_active['Урожайность'].max():.2f} т/га</h2></div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-card' style='margin-bottom:20px;'><b>Коэффициент качества</b><h2>92%</h2><span style='color:blue;'>Выше среднего</span></div>", unsafe_allow_html=True)
        
        st.subheader("Детализированные отчеты о качестве партий 📋")
        df_quality = pd.DataFrame({"Продукт": ["Пшеница", "Кукуруза", "Соя"], "Партия": ["2026-A", "2026-B", "2026-C"], "Влажность": ["14%", "15%", "11%"], "Статус": ["Отлично", "Хорошо", "Отлично"]})
        st.dataframe(df_quality, use_container_width=True)
        
        st.subheader("Распределение урожайности по годам 📊")
        fig_factors = px.bar(df_active, x="Год", y="Урожайность", text_auto='.2f', color_discrete_sequence=['#2E7D32'])
        fig_factors.update_layout(height=280, plot_bgcolor='white', xaxis_title="", yaxis_title="т/га")
        fig_factors.update_xaxes(type='category')
        st.plotly_chart(fig_factors, use_container_width=True)

    # --- Вкладка 6: УГЛЕРОДНЫЙ СЛЕД ---
    elif page_name == "Углеродный след":
        st.subheader(f"Моделирование баланса декарбонизации — ☁️ {selected_field}")
        st.metric("Чистый след Cnet (Средний)", f"{df_active['Cnet'].mean():.2f} т")
        st.metric("Внесение Cinputs (Среднее)", f"{df_active['Cinputs'].mean():.2f} кг")
        st.metric("Целевой прогноз секвестрации", "Выполнено 🌳")
        
        fig_cnet = px.area(df_active, x="Год", y="Cnet", title="Динамическая модель изменения чистого следа Cnet", color_discrete_sequence=['#78909C'])
        fig_cnet.update_layout(plot_bgcolor='white', height=400)
        fig_cnet.update_xaxes(type='category')
        st.plotly_chart(fig_cnet, use_container_width=True)

    # --- Вкладка 7: ПРИНЯТИЕ РЕШЕНИЙ ---
    elif page_name == "Принятие решений":
        st.subheader(f"Сводная расчетная матрица севооборота — 💡 {selected_field}")
        st.markdown("Все строки и столбцы выгружены на основе структуры ТЗ:")
        available_cols = [c for c in ["Год", "Культура", "Урожайность", "Cinputs", "Cnet", "Ravg", "Эффективность"] if c in df_active.columns]
        df_display = df_active[available_cols].copy()
        rename_display = {"Год": "Год агросрока", "Культура": "Культура", "Урожайность": "Урожайность (т/га)", "Cinputs": "Внесение Cinputs (кг)", "Cnet": "Чистый след Cnet", "Ravg": "Коэффициент Rave", "Эффективность": "Индекс эффективности (E)"}
        df_display = df_display.rename(columns=rename_display)
        if "Индекс эффективности (E)" in df_display.columns:
            st.dataframe(df_display.style.format({"Индекс эффективности (E)": "{:.4f}"}), use_container_width=True)
        else:
            st.dataframe(df_display, use_container_width=True)
