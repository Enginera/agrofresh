"""
dashboards.py - Аналитический модуль углеродно-нейтрального земледелия
- Фильтры выборки и загрузка данных находятся в левом выезжающем сайдбаре.
- Все расчетные функции F1–F6 расположены сверху и рассчитываются на основе активного Excel датасета.
- Блоки F1–F6 по умолчанию свёрнуты.
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

    # 1. Инициализация датасета в сессии
    if "agro_data" not in st.session_state:
        st.session_state.agro_data = get_default_dataframe()

    # 2. ЛЕВАЯ ВЫЕЗЖАЮЩАЯ ПАНЕЛЬ (SIDEBAR)
    with st.sidebar:
        st.markdown("""
        <div style="padding: 6px 0 16px;">
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="background:#2f8c69; color:#fff; border-radius:10px; width:38px; height:38px; display:grid; place-items:center; font-size:20px;">🌱</div>
                <div>
                    <b style="font-size:14px; color:#143c2d; display:block; line-height:1.2;">Углеродно-нейтральное</b>
                    <span style="font-size:11px; color:#71817b;">аналитическая панель</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📥 Источник данных (Excel F4-F6)")
        uploaded_file = st.file_uploader("Загрузить файл Excel (.xlsx, .xls)", type=["xlsx", "xls"])
        if uploaded_file is not None:
            new_df, err = parse_carbon_excel(uploaded_file)
            if err:
                st.error(err)
            elif new_df is not None and not new_df.empty:
                st.session_state.agro_data = new_df
                st.success(f"Загружено {len(new_df)} строк из F4, F5, F6")

        st.markdown("---")
        st.markdown("### 🔍 Фильтры выборки")

        selected_cultures = st.multiselect(
            "Культуры",
            CULTURES_LIST,
            default=st.session_state.get("selected_cultures", CULTURES_LIST),
            key="selected_cultures"
        )

        selected_techs = st.multiselect(
            "Технологии",
            TECHS_LIST,
            default=st.session_state.get("selected_techs", TECHS_LIST),
            key="selected_techs"
        )

        season = st.selectbox(
            "Агросезон",
            ["Текущий расчёт", "Все агросезоны"],
            key="season_select"
        )

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Сбросить фильтры", use_container_width=True):
            st.session_state.selected_cultures = CULTURES_LIST.copy()
            st.session_state.selected_techs = TECHS_LIST.copy()
            st.rerun()

        st.markdown("""
        <div style="margin-top:24px; padding:12px; background:#f4f8f6; border-radius:10px; border:1px solid #e0eae5; font-size:11px; color:#5b8072; line-height:1.4;">
            ℹ️ Параметры функций F1–F6, KPI и графики автоматически рассчитываются по загруженной таблице Excel.
        </div>
        """, unsafe_allow_html=True)

    df = st.session_state.agro_data

    # Фильтрация данных
    filt_df = df[df["culture"].isin(selected_cultures) & df["technology"].isin(selected_techs)]
    if filt_df.empty:
        filt_df = df.copy()

    # 3. ОСНОВНАЯ ОБЛАСТЬ: ЗАГОЛОВОК
    st.markdown("""
    <div class="hero-header">
        <div class="eyebrow">Аналитическая панель</div>
        <div class="main-title">Модуль углеродно-нейтрального земледелия</div>
        <div class="subtitle">Интерактивная аналитика данных Excel (F4, F5, F6) и визуализация ключевых показателей агросезона</div>
    </div>
    """, unsafe_allow_html=True)

    # ДИНАМИЧЕСКИЕ СРЕДНИЕ ИЗ ТАБЛИЦЫ ДЛЯ F1-F6
    val_cseq = float(filt_df.get("cabs", pd.Series([14160.0])).mean() / 5000.0) if not filt_df.empty else 2.80
    val_cnet = float(filt_df["footprint"].mean() / 50.0) if not filt_df.empty else 1.60
    val_rote = float(filt_df.get("rot_e", pd.Series([7.89])).mean()) if not filt_df.empty else 7.89
    val_temp = float(filt_df.get("temp", pd.Series([18.0])).mean()) if not filt_df.empty else 18.0
    val_precip = float(filt_df.get("precip", pd.Series([180.0])).mean()) if not filt_df.empty else 180.0
    val_op = float(filt_df.get("op", pd.Series([0.42])).mean()) if not filt_df.empty else 0.42
    val_yield = float(filt_df["yield"].mean()) if not filt_df.empty else 4.80
    val_op_cf = float(filt_df["operation_cf"].mean()) if not filt_df.empty else 112.0
    val_footprint = float(filt_df["footprint"].mean()) if not filt_df.empty else 24.6
    val_gross = float(filt_df["gross"].mean()) if not filt_df.empty else 3180.0
    val_ctotal = float(filt_df.get("ctotal", pd.Series([3015.0])).mean()) if not filt_df.empty else 3015.0
    val_change = float(filt_df["change_cf"].mean()) if not filt_df.empty else -8.5
    val_eff = float(filt_df["efficiency"].mean()) if not filt_df.empty else 68.4
    val_keff = float(filt_df.get("keff", pd.Series([0.86])).mean()) if not filt_df.empty else 0.86
    val_pi = float(filt_df.get("pi", pd.Series([0.42])).mean()) if not filt_df.empty else 0.42
    val_cfield = float(filt_df.get("cfield", pd.Series([31.7])).mean()) if not filt_df.empty else 31.7
    val_ynet = float(filt_df.get("ynet", pd.Series([4820.0])).mean()) if not filt_df.empty else 4820.0
    val_cost = float(filt_df["cost"].mean()) if not filt_df.empty else 52.5
    val_fert_cost = float(filt_df.get("fert_cost", pd.Series([18.6])).mean()) if not filt_df.empty else 18.6

    # 4. РАСЧЁТНЫЕ ПОДМОДУЛИ F1–F6 (СВЕРХУ, СВЁРНУТЫ ПО УМОЛЧАНИЮ)
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:baseline; margin: 8px 0 12px;">
        <h3 style="margin:0; color:#143c2d; font-weight:800; font-size:18px;">⚡ Расчётные функции F1–F6 (Данные Excel)</h3>
        <span style="font-size:11px; color:#71817b;">Значения рассчитаны по текущей выборке таблицы · Доступно ручное моделирование</span>
    </div>
    """, unsafe_allow_html=True)

    calc_col1, calc_col2 = st.columns(2)

    with calc_col1:
        # F.1
        with st.expander("🟢 F.1 — Планирование севооборота", expanded=False):
            st.caption("Секвестрация, углеродный след за период агросрока и интегральная эффективность.")
            c1_1, c1_2 = st.columns(2)
            with c1_1:
                st.number_input("Csequestered (т CO₂-экв./га)", value=round(val_cseq, 2), step=0.1, key="top_f1_cseq")
                st.number_input("Cnet (т CO₂-экв./га)", value=round(val_cnet, 2), step=0.1, key="top_f1_cnet")
            with c1_2:
                st.number_input("E (Коэффициент севооборота)", value=round(val_rote, 2), step=0.1, key="top_f1_e")
                f1_cult = st.selectbox("Культура F1", selected_cultures if selected_cultures else CULTURES_LIST, key="top_f1_cult")
            st.info(f"F1 Расчёт: {f1_cult} · Cseq: {val_cseq:.2f} · Cnet: {val_cnet:.2f} · E: {val_rote:.2f}")

        # F.2
        with st.expander("🟢 F.2 — Управление удобрениями и обработкой почвы", expanded=False):
            st.caption("Параметры температуры, влажности, агротехнического воздействия и углеродных потоков.")
            c2_1, c2_2 = st.columns(2)
            with c2_1:
                st.number_input("Ktemp (Коэфф. температуры)", value=round(val_temp / 17.0, 2), step=0.01, key="top_f2_ktemp")
                st.number_input("Wфакт (Фактич. влажность, %)", value=24.0, step=0.5, key="top_f2_wf")
                st.number_input("Wопт (Оптимальн. влажность, %)", value=27.0, step=0.5, key="top_f2_wo")
                st.number_input("Iат (Индекс агротех. возд.)", value=0.82, step=0.01, key="top_f2_iat")
            with c2_2:
                st.number_input("Kвлаги (Коэффициент)", value=round(val_precip / 200.0, 2), step=0.01, key="top_f2_kvl")
                st.number_input("Wкрит (Критич. влажность, %)", value=18.0, step=0.5, key="top_f2_wc")
                st.number_input("CFпестицидов (кг CO₂-экв./т)", value=round(filt_df["pest"].mean() * 10, 1), step=0.5, key="top_f2_cf")
                st.number_input("ΔCобработка (кг CO₂-экв./га)", value=-42.0, step=1.0, key="top_f2_dc")

        # F.3
        with st.expander("🟢 F.3 — Мониторинг и управление защитой растений", expanded=False):
            st.caption("Оценка заражения, повреждения, интервалов обработок и углеродного следа СЗР.")
            c3_1, c3_2 = st.columns(2)
            with c3_1:
                st.number_input("УЗ (Уровень заражения, %)", value=18.0, step=1.0, key="top_f3_uz")
                st.number_input("ИПВ (Индекс повреждения)", value=round(val_op, 2), step=0.01, key="top_f3_ipv")
                st.number_input("D (Дозировка, л/га)", value=round(filt_df["pest"].mean(), 2), step=0.1, key="top_f3_d")
            with c3_2:
                st.number_input("ИП (Интенсивность поражения, %)", value=12.0, step=1.0, key="top_f3_ip")
                st.number_input("I (Интервал между обработками, дни)", value=14, step=1, key="top_f3_i")
                st.number_input("Cсезон (кг CO₂-экв./га)", value=round(filt_df["pest"].mean() * 45, 1), step=1.0, key="top_f3_cs")

    with calc_col2:
        # F.4
        with st.expander("🟢 F.4 — Управление урожайностью и качеством продукции", expanded=False):
            st.caption("Оценка потерь, урожайности, технологического следа и качества продукции.")
            c4_1, c4_2 = st.columns(2)
            with c4_1:
                st.number_input("ОП (Общие потери, т/га)", value=round(val_op, 2), step=0.01, key="top_f4_op")
                st.number_input("Уфин (Финальная урожайность, т/га)", value=round(val_yield, 2), step=0.1, key="top_f4_uf")
                st.number_input("CFу.след (кг CO₂-экв./га)", value=round(val_op_cf, 1), step=1.0, key="top_f4_cfuy")
                st.number_input("CFитог (кг CO₂-экв./т)", value=round(val_footprint, 1), step=0.1, key="top_f4_cfit")
            with c4_2:
                st.number_input("ΔCсолом (кг CO₂-экв./га)", value=-185.0, step=5.0, key="top_f4_dcs")
                st.number_input("SCO₂ (кг CO₂-экв./га)", value=-96.0, step=2.0, key="top_f4_sco")
                st.number_input("QF (Качество продукции, %)", value=92.0, step=1.0, key="top_f4_qf")

        # F.5
        with st.expander("🟢 F.5 — Оценка углеродного следа, учет и отчетность", expanded=False):
            st.caption("Сводная оценка углеродоемкости, валовых выбросов и эффективности.")
            c5_1, c5_2 = st.columns(2)
            with c5_1:
                st.number_input("У CO₂ (Углеродоемкость, т CO₂/га)", value=round(val_gross / 1000.0, 2), step=0.05, key="top_f5_uco")
                st.number_input("Э CO₂ (Эмиссия операции, кг CO₂/га)", value=round(val_gross * 0.7, 1), step=10.0, key="top_f5_eco")
                st.number_input("OCO₂ (Валовые выбросы, кг CO₂/га)", value=round(val_gross, 1), step=10.0, key="top_f5_oco")
                st.number_input("Cem (Эмиссия технологии, кг CO₂/га)", value=round(val_gross * 0.9, 1), step=10.0, key="top_f5_cem")
            with c5_2:
                st.number_input("Ctotal (След за агросрок, кг CO₂/га)", value=round(val_ctotal, 1), step=10.0, key="top_f5_ctot")
                st.number_input("ΔCF min (Изменение следа, кг CO₂/га)", value=round(val_change, 1), step=0.5, key="top_f5_dcf")
                st.number_input("Эффективность (тыс. руб/га)", value=round(val_eff, 1), step=0.5, key="top_f5_eff")

        # F.6
        with st.expander("🟢 F.6 — Принятие стратегических решений", expanded=False):
            st.caption("Оценка нейтральности, индекс приоритета затрат, прогноз урожайности и экономика.")
            c6_1, c6_2 = st.columns(2)
            with c6_1:
                st.number_input("Kэф (Коэффициент)", value=round(val_keff, 2), step=0.01, key="top_f6_keff")
                st.number_input("PI (Индекс приоритета, кг CO₂/руб)", value=round(val_pi, 3), step=0.01, key="top_f6_pi")
                st.number_input("C поле (Углеродоемкость, кг CO₂/т)", value=round(val_cfield, 1), step=0.5, key="top_f6_cpol")
                st.number_input("Y net (Прогноз урожайности, кг/га)", value=round(val_ynet, 1), step=50.0, key="top_f6_ynet")
            with c6_2:
                st.number_input("E (Эффективность севооборота)", value=round(val_rote, 2), step=0.05, key="top_f6_e")
                st.number_input("Себестоимость (тыс. руб/га)", value=round(val_cost, 1), step=0.5, key="top_f6_cost")
                st.number_input("З уд.агросрок (тыс. руб/га)", value=round(val_fert_cost, 1), step=0.2, key="top_f6_fert")

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # 5. БЛОК KPI
    avg_area = filt_df["area"].mean() if not filt_df.empty else 0

    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Средний чистый след</div>
            <div class="kpi-value">{val_footprint:.1f}</div>
            <div class="kpi-hint">кг CO₂-экв./т</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Средняя эффективность</div>
            <div class="kpi-value">{val_eff:.2f}</div>
            <div class="kpi-hint">показатель F6</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Площадь колебания</div>
            <div class="kpi-value">{avg_area:.1f}</div>
            <div class="kpi-hint">га, по выбранным строкам</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Средняя себестоимость</div>
            <div class="kpi-value">{val_cost:.1f}</div>
            <div class="kpi-hint">тыс. руб./га</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6. АНАЛИТИЧЕСКИЕ ДИАГРАММЫ (8 шт.)
    st.markdown("### 📊 Аналитические диаграммы")

    # 1. Удельный след: No-Till vs Классическая
    st.markdown("""<div class="chart-card"><div class="chart-head"><h3>Удельный след: No-Till vs Классическая</h3><p>кг CO₂-экв./т · среднее по выбранным культурам</p></div></div>""", unsafe_allow_html=True)
    c1_df = filt_df.groupby(["culture", "technology"])["footprint"].mean().reset_index()
    fig1 = px.bar(
        c1_df, x="culture", y="footprint", color="technology", barmode="group",
        color_discrete_map={"Классическая": "#4e91ad", "No-Till": "#a93d72"},
        labels={"culture": "Культура", "footprint": "След (кг CO₂-экв./т)", "technology": "Технология"}
    )
    fig1.update_layout(template="plotly_white", margin=dict(t=10, b=10, l=10, r=10), height=320)
    st.plotly_chart(fig1, use_container_width=True)

    # 2 и 3
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

    # 4. Выбросы CO₂ по технологическим операциям
    st.markdown("""<div class="chart-card"><div class="chart-head"><h3>Выбросы CO₂ по технологическим операциям</h3><p>кг CO₂-экв./га · данные F5</p></div></div>""", unsafe_allow_html=True)
    c4_df = filt_df.groupby("operation")["gross"].mean().reset_index()
    fig4 = px.bar(c4_df, y="operation", x="gross", orientation="h", color_discrete_sequence=["#2d7655"])
    fig4.update_layout(template="plotly_white", margin=dict(t=10, b=10, l=10, r=10), height=280)
    st.plotly_chart(fig4, use_container_width=True)

    # 5 и 6
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

    # 7 и 8
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

    # 7. Таблицы статуса культур и технологий
    st.markdown("### 📋 Статус культур и технологий")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        cult_status = pd.DataFrame({
            "Культура": CULTURES_LIST,
            "Статус": ["Выбрано" if c in selected_cultures else "Не выбрано" for c in CULTURES_LIST]
        })
        st.dataframe(cult_status, use_container_width=True, hide_index=True)
    with t_col2:
        tech_status = pd.DataFrame({
            "Технология": TECHS_LIST,
            "Статус": ["Выбрано" if t in selected_techs else "Сравнение" for t in TECHS_LIST]
        })
        st.dataframe(tech_status, use_container_width=True, hide_index=True)

    st.caption(f"Прототип · Источник данных: F2(3).xlsx · Листы: F4, F5, F6 · Строк в расчете: {len(filt_df)}")