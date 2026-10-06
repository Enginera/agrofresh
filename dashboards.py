import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

PALETTE = {
    "blue": "#4e91ad",
    "green": "#2d8b68",
    "pink": "#a93d72",
    "amber": "#e49a27",
    "purple": "#7a6fb1",
    "dark_green": "#1e7655"
}

def render_carbon_dashboard(carbon_data):
    df = carbon_data["records"]
    
    st.markdown("""
    <div class="dashboard-header">
        <div class="eyebrow">Аналитическая панель</div>
        <div class="dashboard-title">Модуль углеродно-нейтрального земледелия по 5 полям</div>
        <div class="dashboard-subtitle">Интерактивная аналитика данных Excel и визуализация ключевых показателей агросезона</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1.5, 1])
    all_cultures = sorted(df["culture"].unique()) if not df.empty else ["Озимая пшеница", "Горох", "Кукуруза", "Многолетние травы", "Подсолнечник", "Лён"]
    all_techs = ["No-Till", "Классическая"]
    
    with col1:
        sel_cultures = st.multiselect("Культура", all_cultures, default=all_cultures)
    with col2:
        sel_techs = st.multiselect("Технология", all_techs, default=all_techs)
    with col3:
        season = st.selectbox("Агросезон", ["Текущий расчёт", "Все агросезоны"])
        
    f_df = df[(df["culture"].isin(sel_cultures)) & (df["technology"].isin(sel_techs))] if not df.empty else df

    st.markdown("### 🌾 Статистика выбранного поля")
    field_col1, field_col2 = st.columns([1, 4])
    with field_col1:
        sel_field = st.selectbox("Выберите поле", ["1", "2", "3", "4", "5"], index=0)
    
    f_stat = carbon_data["fields_stat"].get(sel_field, carbon_data["fields_stat"]["1"])
    
    st.markdown(f"""
    <div class="field-banner">
        <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <b style="font-size: 20px;">Поле {sel_field}</b>
            <span>Ретроспективные данные за <b>5 лет</b></span>
        </div>
        <div style="font-size: 14px; margin-top: 4px; opacity: 0.9;">{' · '.join(f_stat['cultures'])} | Технологии: {' · '.join(f_stat['techs'])}</div>
        <div class="field-grid">
            <div class="field-stat"><span>Площадь</span><b>{f_stat['area_avg']} га</b></div>
            <div class="field-stat"><span>Урожайность</span><b>{f_stat['yield_avg']} т/га</b></div>
            <div class="field-stat"><span>Удельный след</span><b>{f_stat['cf_avg']} кг CO₂/т</b></div>
            <div class="field-stat"><span>Валовые выбросы</span><b>{f_stat['gross_avg']} кг CO₂/га</b></div>
            <div class="field-stat"><span>Эффективность (F1)</span><b>{f_stat['eff_avg']}</b></div>
            <div class="field-stat"><span>Себестоимость</span><b>{f_stat['cost_avg']} тыс.₽/га</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    avg_footprint = f_df["footprint"].mean() if not f_df.empty else 13.5
    avg_eff = f_df["efficiency"].mean() if not f_df.empty else 6.7
    avg_area = f_df["area"].mean() if not f_df.empty else 118.0
    avg_cost = f_df["cost"].mean() if not f_df.empty else 52.0

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
            <div class="kpi-hint">га, по выборке</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Средняя себестоимость</div>
            <div class="kpi-value">{avg_cost:.1f}</div>
            <div class="kpi-hint">тыс. руб./га</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("⚙️ Расчётные функции F1–F6 (Настройка сценарных параметров)", expanded=False):
        c_f1, c_f2 = st.columns(2)
        with c_f1:
            st.markdown("**F1. Планирование севооборота**")
            st.number_input("Секвестрация Cseq, т CO₂-экв./га", value=2.8, step=0.1, key="c_f1_seq")
            st.number_input("Углеродный след Cnet, т CO₂-экв./га", value=1.6, step=0.1, key="c_f1_net")
            
            st.markdown("**F2. Управление удобрениями и почвой**")
            st.number_input("Норма удобрений, кг/га", value=180.0, key="c_f2_fert")
            st.number_input("Интенсивность обработки, %", value=70.0, key="c_f2_soil")
            
            st.markdown("**F3. Мониторинг защиты растений**")
            st.number_input("Пестициды, кг/га", value=4.5, key="c_f3_pest")
        with c_f2:
            st.markdown("**F4. Управление урожайностью и качеством**")
            st.number_input("Урожайность Уфин, т/га", value=4.8, key="c_f4_y")
            st.number_input("QF Индекс качества, %", value=92.0, key="c_f4_q")
            
            st.markdown("**F5. Оценка выбросов и отчетность**")
            st.number_input("Валовые выбросы, кг CO₂-экв./га", value=2250.0, key="c_f5_em")
            
            st.markdown("**F6. Принятие стратегических решений**")
            st.selectbox("Сценарий оптимизации", ["Текущий расчет", "Снижение выбросов", "Максимальная маржинальность"], key="c_f6_sc")
        st.button("Сохранить параметры модели F1–F6")

    st.markdown("### 📊 Аналитические диаграммы")
    if not f_df.empty:
        fig1 = px.bar(
            f_df.groupby(["culture", "technology"])["footprint"].mean().reset_index(),
            x="culture", y="footprint", color="technology", barmode="group",
            color_discrete_map={"No-Till": PALETTE["blue"], "Классическая": PALETTE["pink"]},
            title="Удельный след: No-Till vs Классическая (кг CO₂-экв./т)",
            labels={"footprint": "кг CO₂-экв./т", "culture": "Культура", "technology": "Технология"}
        )
        fig1.update_layout(plot_bgcolor="white", height=320, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig1, use_container_width=True)

    g_col1, g_col2 = st.columns(2)
    with g_col1:
        fig2 = go.Figure(data=[go.Pie(
            labels=["Технологические операции", "Техника", "Севооборот"],
            values=[f_df["operation_cf"].mean(), f_df["tech_cf"].mean(), f_df["rotation_cf"].mean()] if not f_df.empty else [50, 100, 10],
            hole=.6,
            marker=dict(colors=[PALETTE["blue"], PALETTE["pink"], PALETTE["amber"]])
        )])
        fig2.update_layout(title="Структура выбросов по ресурсам", height=300, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    with g_col2:
        fig3 = px.bar(
            f_df.groupby("culture")["efficiency"].mean().reset_index(),
            x="culture", y="efficiency",
            color_discrete_sequence=[PALETTE["green"]],
            title="Эффективность по культуре (показатель F6)",
            labels={"efficiency": "F6 Интегральный показатель", "culture": "Культура"}
        )
        fig3.update_layout(plot_bgcolor="white", height=300, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig3, use_container_width=True)

    g_col3, g_col4 = st.columns(2)
    with g_col3:
        fig4 = px.bar(
            f_df.groupby("operation")["gross"].mean().reset_index(),
            y="operation", x="gross", orientation="h",
            color_discrete_sequence=[PALETTE["dark_green"]],
            title="Выбросы CO₂ по операциям (кг CO₂-экв./га)",
            labels={"gross": "кг CO₂/га", "operation": "Операция"}
        )
        fig4.update_layout(plot_bgcolor="white", height=300, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig4, use_container_width=True)

    with g_col4:
        fig5 = px.scatter(
            f_df, x="yield", y="footprint", color="culture",
            title="Углеродный след vs Урожайность",
            labels={"yield": "Урожайность, т/га", "footprint": "След, кг CO₂/т"}
        )
        fig5.update_layout(plot_bgcolor="white", height=300, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig5, use_container_width=True)

def render_organic_dashboard(organic_data):
    st.markdown("""
    <div class="dashboard-header">
        <div class="eyebrow">Модуль органического земледелия</div>
        <div class="dashboard-title">Аналитика соответствия ФЗ № 280-ФЗ и биологической эффективности</div>
        <div class="dashboard-subtitle">Контроль запрета синтетических удобрений, глубины обработки почвы и фиксации азота бобовыми</div>
    </div>
    """, unsafe_allow_html=True)
    
    df4 = organic_data["f4"] if not organic_data["f4"].empty else pd.DataFrame()
    df5 = organic_data["f5"] if not organic_data["f5"].empty else pd.DataFrame()
    df2 = organic_data["f2"] if not organic_data["f2"].empty else pd.DataFrame()
    df1 = organic_data["f1"] if not organic_data["f1"].empty else pd.DataFrame()

    col1, col2, col3 = st.columns(3)
    cultures = sorted(df4.iloc[:, 1].dropna().unique()) if len(df4.columns)>1 else ["Озимая пшеница", "Горох", "Лён", "Кукуруза", "Многолетние травы", "Подсолнечник"]
    techs = sorted(df4.iloc[:, 2].dropna().unique()) if len(df4.columns)>2 else ["No-Till", "Классическая"]
    
    with col1:
        sel_c = st.selectbox("Основная культура", ["Все культуры"] + list(cultures))
    with col2:
        sel_t = st.selectbox("Технология обработки", ["Все технологии"] + list(techs))
    with col3:
        sel_legume = st.selectbox("Бобовая культура (азотфиксатор)", ["Все бобовые", "Соя", "Люцерна", "Клевер", "Горох"])

    ufin_val = pd.to_numeric(df4.iloc[:, 7], errors="coerce").mean() if len(df4.columns)>7 else 4.8
    op_val = pd.to_numeric(df4.iloc[:, 6], errors="coerce").mean() if len(df4.columns)>6 else 0.42
    qindex_val = pd.to_numeric(df4.iloc[:, 9], errors="coerce").mean() if len(df4.columns)>9 else 85.0
    eff_e = pd.to_numeric(df1.iloc[:, 5], errors="coerce").mean() if len(df1.columns)>5 else 7.89

    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Финальная урожайность</div>
            <div class="kpi-value">{ufin_val:.2f}</div>
            <div class="kpi-hint">т/га (за вычетом потерь)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Общие потери при уборке</div>
            <div class="kpi-value">{op_val:.2f}</div>
            <div class="kpi-hint">т/га (жатва + сепарация)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Индекс качества Qindex</div>
            <div class="kpi-value">{qindex_val:.1f}%</div>
            <div class="kpi-hint">соответствие товарным нормам</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Эффективность севооборота</div>
            <div class="kpi-value">{eff_e:.2f}</div>
            <div class="kpi-hint">коэффициент E (лист F1)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📜 Контроль требований органического регламента (ФЗ-280)")
    c_ring1, c_ring2 = st.columns(2)
    with c_ring1:
        fig_comp = go.Figure(data=[go.Pie(
            labels=["Соответствует (глубина ≤ 5 см)", "Не соответствует"],
            values=[680, 320],
            hole=.6,
            marker=dict(colors=[PALETTE["green"], PALETTE["pink"]])
        )])
        fig_comp.update_layout(title="Соответствие технологии (глубина обработки почвы)", height=280, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_comp, use_container_width=True)
        
    with c_ring2:
        fig_fert = go.Figure(data=[go.Pie(
            labels=["Органическое сырье (разрешено)", "Запрещенные мин. удобрения"],
            values=[740, 260],
            hole=.6,
            marker=dict(colors=[PALETTE["green"], PALETTE["pink"]])
        )])
        fig_fert.update_layout(title="Соответствие удобрений положениям ФЗ-280", height=280, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_fert, use_container_width=True)

    st.markdown("### 🌾 Биологическая фиксация азота и ресурсосбережение (F2)")
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        n_df = pd.DataFrame({
            "Бобовая культура": ["Клевер", "Люцерна", "Соя", "Горох"],
            "Фиксированный N, кг/га": [148.5, 175.2, 112.4, 68.9]
        })
        fig_n = px.bar(n_df, x="Бобовая культура", y="Фиксированный N, кг/га", color_discrete_sequence=[PALETTE["green"]], title="Биологически фиксированный азот (кг N/га)")
        fig_n.update_layout(plot_bgcolor="white", height=300)
        st.plotly_chart(fig_n, use_container_width=True)
        
    with col_n2:
        fuel_df = pd.DataFrame({
            "Бобовая культура": ["Клевер", "Люцерна", "Соя", "Горох"],
            "Экономия дизтоплива, л/га": [245.0, 289.5, 185.0, 114.0]
        })
        fig_fuel = px.bar(fuel_df, x="Бобовая культура", y="Экономия дизтоплива, л/га", color_discrete_sequence=[PALETTE["amber"]], title="Экономия дизтоплива за счёт сидерации (л/га)")
        fig_fuel.update_layout(plot_bgcolor="white", height=300)
        st.plotly_chart(fig_fuel, use_container_width=True)

    st.markdown("### 📋 Сводные показатели качества и урожайности")
    summary_data = pd.DataFrame({
        "Культура": ["Озимая пшеница", "Горох", "Кукуруза", "Многолетние травы", "Подсолнечник", "Лён"],
        "Фактическая урожайность, т/га": [5.5, 2.1, 4.2, 4.5, 1.6, 1.1],
        "Финальная урожайность, т/га": [4.9, 1.8, 3.6, 4.0, 1.2, 0.8],
        "Общие потери, т/га": [0.60, 0.30, 0.60, 0.50, 0.40, 0.30],
        "Индекс качества Qindex, %": [91.5, 87.0, 89.2, 94.0, 85.5, 82.0]
    })
    st.dataframe(summary_data, use_container_width=True, hide_index=True)
