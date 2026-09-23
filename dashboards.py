"""
dashboards.py - Интерактивный дашборд углеродно-нейтрального земледелия (8 Графиков + Расчеты F1-F6)
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from styles import apply_carbon_styles
from parser import get_default_dataframe, parse_carbon_excel, CULTURES_LIST, TECHS_LIST

def render_carbon_neutral_dashboard():
    apply_carbon_styles()

    # Сессионное хранилище датасета
    if "agro_data" not in st.session_state:
        st.session_state.agro_data = get_default_dataframe()

    # Верхний заголовок и панель действий
    st.markdown("""
    <div class="hero-header">
        <div class="eyebrow">Аналитическая панель</div>
        <div class="main-title">🌱 Модуль углеродно-нейтрального земледелия</div>
        <div class="subtitle">Интерактивная аналитика данных Excel и визуализация ключевых показателей агросезона</div>
    </div>
    """, unsafe_allow_html=True)

    # Панель действий: Загрузка Excel / Сброс
    top_col1, top_col2, top_col3 = st.columns([2, 1, 1])
    with top_col1:
        uploaded_file = st.file_uploader("Загрузить файл Excel (.xlsx, .xls)", type=["xlsx", "xls"], label_visibility="collapsed")
        if uploaded_file is not None:
            new_df, err = parse_carbon_excel(uploaded_file)
            if err:
                st.error(err)
            elif new_df is not None and not new_df.empty:
                st.session_state.agro_data = new_df
                st.success(f"Успешно загружено {len(new_df)} строк из Excel.")
    with top_col2:
        if st.button("🔄 Сбросить фильтры", use_container_width=True):
            st.session_state.selected_cultures = CULTURES_LIST.copy()
            st.session_state.selected_techs = TECHS_LIST.copy()
            st.rerun()

    df = st.session_state.agro_data

    # Секция фильтров
    st.markdown("### 🔍 Параметры выборки")
    f_col1, f_col2, f_col3 = st.columns([2, 1.5, 1])
    with f_col1:
        selected_cultures = st.multiselect("Культура", CULTURES_LIST, default=CULTURES_LIST, key="selected_cultures")
    with f_col2:
        selected_techs = st.multiselect("Технология", TECHS_LIST, default=TECHS_LIST, key="selected_techs")
    with f_col3:
        season = st.selectbox("Агросезон", ["Текущий расчёт", "Все агросезоны"])

    # Фильтрация данных
    filt_df = df[df["culture"].isin(selected_cultures) & df["technology"].isin(selected_techs)]
    if filt_df.empty:
        filt_df = df.copy()

    # Блок KPI
    avg_footprint = filt_df["footprint"].mean() if not filt_df.empty else 0
    avg_eff = filt_df["efficiency"].mean() if not filt_df.empty else 0
    avg_area = filt_df["area"].mean() if not filt_df.empty else 0
    avg_cost = filt_df["cost"].mean() if not filt_df.empty else 0

    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Средний чистый след</div>
            <div class="kpi-value">{avg_footprint:.1f}</div>
            <div class="kpi-hint">кг CO₂-экв./т</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Средняя эффективность</div>
            <div class="kpi-value">{avg_eff:.2f}</div>
            <div class="kpi-hint">показатель F6</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Площадь колебания</div>
            <div class="kpi-value">{avg_area:.1f}</div>
            <div class="kpi-hint">га, по выбранным строкам</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Средняя себестоимость</div>
            <div class="kpi-value">{avg_cost:.1f}</div>
            <div class="kpi-hint">тыс. руб./га</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Верхний блок расчётных функций F1-F6
    with st.expander("⚡ Верхний блок расчетных функций F1–F6 (Сценарный ввод)", expanded=False):
        c_f1, c_f2 = st.columns(2)
        with c_f1:
            st.markdown("**F1: Планирование севооборота**")
            f1_cult = st.selectbox("F1 Культура", CULTURES_LIST, key="f1_c")
            f1_area = st.number_input("Площадь, га", value=100.0, step=10.0, key="f1_a")
            f1_cseq = st.number_input("Секвестрация Cseq, т CO₂/га", value=2.8, key="f1_seq")
            f1_cnet = st.number_input("Углеродный след Cnet, т CO₂/га", value=1.6, key="f1_net")
            st.info(f"F1 Прогноз: {f1_cult}, {f1_area:.1f} га · Cseq: {f1_cseq} · Cnet: {f1_cnet} т CO₂-экв./га")

        with c_f2:
            st.markdown("**F2: Управление удобрениями и почвой**")
            f2_fert = st.number_input("Норма удобрений, кг/га", value=180.0, step=5.0, key="f2_f")
            f2_soil = st.slider("Интенсивность обработки почвы, %", 0, 100, 70, key="f2_s")
            st.info(f"F2 Параметры: Удобрения {f2_fert} кг/га | Интенсивность {f2_soil}%")

    # Сетка графиков (8 штук из прототипа)
    st.markdown("### 📊 Аналитические панели")
    
    # 1. Удельный след: No-Till vs Классическая (Широкая)
    st.markdown("""<div class="chart-card"><div class="chart-head"><h3>Удельный след: No-Till vs Классическая</h3><p>кг CO₂-экв./т · среднее по выбранным культурам</p></div></div>""", unsafe_allow_html=True)
    c1_df = filt_df.groupby(["culture", "technology"])["footprint"].mean().reset_index()
    fig1 = px.bar(
        c1_df, x="culture", y="footprint", color="technology", barmode="group",
        color_discrete_map={"Классическая": "#4e91ad", "No-Till": "#a93d72"},
        labels={"culture": "Культура", "footprint": "След (кг CO₂-экв./т)", "technology": "Технология"}
    )
    fig1.update_layout(template="plotly_white", margin=dict(t=10, b=10, l=10, r=10), height=320)
    st.plotly_chart(fig1, use_container_width=True)

    # 2 и 3 в две колонки
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.markdown("""<div class="chart-card"><div class="chart-head"><h3>Структура выбросов по ресурсам</h3><p>технологические операции · техника · севооборот</p></div></div>""", unsafe_allow_html=True)
        r_ops = filt_df["operation_cf"].mean() if not filt_df.empty else 0
        r_tech = filt_df["tech_cf"].mean() if not filt_df.empty else 0
        r_rot = filt_df["rotation_cf"].mean() if not filt_df.empty else 0
        fig2 = go.Figure(data=[go.Pie(
            labels=["Технологические операции", "Техника", "Севооборот"],
            values=[r_ops, r_tech, r_rot],
            hole=0.6,
            marker=dict(colors=["#4e91ad", "#a93d72", "#e49a27"])
        )])
        fig2.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)
        st.plotly_chart(fig2, use_container_width=True)

    with g_col2:
        st.markdown("""<div class="chart-card"><div class="chart-head"><h3>Эффективность по культуре</h3><p>среднее значение F6 · столбчатая диаграмма</p></div></div>""", unsafe_allow_html=True)
        c3_df = filt_df.groupby("culture")["efficiency"].mean().reset_index()
        fig3 = px.bar(c3_df, x="culture", y="efficiency", color_discrete_sequence=["#2d8b68"])
        fig3.update_layout(template="plotly_white", margin=dict(t=10, b=10, l=10, r=10), height=300)
        st.plotly_chart(fig3, use_container_width=True)

    # 4. Выбросы CO₂ по технологическим операциям (Широкая горизонтальная)
    st.markdown("""<div class="chart-card"><div class="chart-head"><h3>Выбросы CO₂ по технологическим операциям</h3><p>кг CO₂-экв./га · данные F5</p></div></div>""", unsafe_allow_html=True)
    c4_df = filt_df.groupby("operation")["gross"].mean().reset_index()
    fig4 = px.bar(c4_df, y="operation", x="gross", orientation="h", color_discrete_sequence=["#2d7655"])
    fig4.update_layout(template="plotly_white", margin=dict(t=10, b=10, l=10, r=10), height=280)
    st.plotly_chart(fig4, use_container_width=True)

    # 5 и 6 в две колонки
    g_col3, g_col4 = st.columns(2)
    with g_col3:
        st.markdown("""<div class="chart-card"><div class="chart-head"><h3>Зависимость углеродного следа от урожайности</h3><p>урожайность, т/га · след, кг CO₂-экв./т</p></div></div>""", unsafe_allow_html=True)
        fig5 = px.scatter(filt_df, x="yield", y="footprint", color="technology",
                          color_discrete_map={"Классическая": "#4e91ad", "No-Till": "#a93d72"})
        fig5.update_layout(template="plotly_white", margin=dict(t=10, b=10, l=10, r=10), height=300)
        st.plotly_chart(fig5, use_container_width=True)

    with g_col4:
        st.markdown("""<div class="chart-card"><div class="chart-head"><h3>Вид углеродных выбросов</h3><p>минеральные удобрения · пестициды · топливо</p></div></div>""", unsafe_allow_html=True)
        c6_df = filt_df.groupby("culture")[["fert", "pest", "fuel"]].mean().reset_index()
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(name="Удобрения", x=c6_df["culture"], y=c6_df["fert"], marker_color="#e49a27"))
        fig6.add_trace(go.Bar(name="Пестициды", x=c6_df["culture"], y=c6_df["pest"], marker_color="#a93d72"))
        fig6.add_trace(go.Bar(name="Топливо", x=c6_df["culture"], y=c6_df["fuel"], marker_color="#4e91ad"))
        fig6.update_layout(barmode="group", template="plotly_white", margin=dict(t=10, b=10, l=10, r=10), height=300)
        st.plotly_chart(fig6, use_container_width=True)

    # 7 и 8 в две колонки
    g_col5, g_col6 = st.columns(2)
    with g_col5:
        st.markdown("""<div class="chart-card"><div class="chart-head"><h3>Изменение углеродного следа</h3><p>сводный показатель по технологическим операциям</p></div></div>""", unsafe_allow_html=True)
        c7_df = filt_df.groupby("operation")["change_cf"].mean().reset_index()
        fig7 = px.line(c7_df, x="operation", y="change_cf", markers=True, color_discrete_sequence=["#2f7657"])
        fig7.update_layout(template="plotly_white", margin=dict(t=10, b=10, l=10, r=10), height=300)
        st.plotly_chart(fig7, use_container_width=True)

    with g_col6:
        st.markdown("""<div class="chart-card"><div class="chart-head"><h3>Себестоимость по заданным полям в агросезон</h3><p>тыс. руб./га · F6</p></div></div>""", unsafe_allow_html=True)
        c8_df = filt_df.groupby("culture")["cost"].mean().reset_index()
        fig8 = px.bar(c8_df, x="culture", y="cost", color_discrete_sequence=["#7a6fb1"])
        fig8.update_layout(template="plotly_white", margin=dict(t=10, b=10, l=10, r=10), height=300)
        st.plotly_chart(fig8, use_container_width=True)

    # Секция детальных расчетных подмодулей F1-F6
    st.markdown("### 🧮 Расчётные подмодули F1–F6")
    
    fns = [
        ("F.1", "Планирование севооборота", [
            ("Csequestered", "Секвестрация углерода при выборе с/х культур", "2.80", "т CO₂-экв./га"),
            ("Cnet", "Расчет показателя углеродного следа за период агросрока", "1.60", "т CO₂-экв./га"),
            ("E", "Интегральный коэффициент эффективности севооборота", "7.89", "коэффициент")
        ]),
        ("F.2", "Управление удобрениями и обработкой почвы", [
            ("Ktemp", "Коэффициент температуры почвы", "1.05", "коэффициент"),
            ("Wфакт", "Влажность почвы фактическая", "24", "%"),
            ("Iат", "Индекс агротехнического воздействия", "0.82", "индекс"),
            ("ΔCобработка", "Секвестрация углерода от технологической операции", "-42", "кг CO₂-экв./га")
        ]),
        ("F.3", "Мониторинг и управление защитой растений", [
            ("УЗ", "Уровень заражения растения", "18", "%"),
            ("ИПВ", "Индекс повреждения (интегральная оценка)", "0.34", "индекс"),
            ("D", "Усредненная дозировка препаратов", "2.50", "л/га"),
            ("Cсезон", "Углеродный след мероприятий защиты растений", "86", "кг CO₂-экв./га")
        ]),
        ("F.4", "Управление урожайностью и качеством", [
            ("ОП", "Общие потери", "0.42", "т/га"),
            ("Уфин", "Финальная урожайность", "4.80", "т/га"),
            ("CFитог", "Показатель углеродного следа на тонну зерна", "24.6", "кг CO₂-экв./т"),
            ("SCO₂", "Секвестрация за счёт пожнивных остатков", "-96", "кг CO₂-экв./га")
        ]),
        ("F.5", "Оценка углеродного следа, отчетность", [
            ("У CO₂", "Углеродоемкость", "1.84", "т CO₂/га"),
            ("OCO₂", "Общие валовые выбросы углерода", "3180", "кг CO₂-экв./га"),
            ("Ctotal", "Углеродный след i-го агросрока", "3015", "кг CO₂-экв./га")
        ]),
        ("F.6", "Принятие стратегических решений", [
            ("Kэф", "Коэффициент эффективности нейтральности", "0.86", "коэффициент"),
            ("PI", "Индекс приоритета поглощения на 1 рубль затрат", "0.42", "кг CO₂/руб"),
            ("Себестоимость", "Себестоимость по заданным полям", "52.5", "тыс. руб/га")
        ])
    ]

    fn_cols = st.columns(2)
    for i, (code, title, subs) in enumerate(fns):
        with fn_cols[i % 2]:
            with st.expander(f"{code} — {title}"):
                for var, desc, def_val, unit in subs:
                    st.text_input(f"{desc} ({var}) [{unit}]", value=def_val, key=f"sub_{code}_{var}")

    st.caption(f"Источник данных: активный датасет ({len(filt_df)} строк)")