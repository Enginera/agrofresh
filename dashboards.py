import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# ДАШБОРД УГЛЕРОДНОГО СЛЕДА (НОВЫЙ)
# ==========================================
def render_carbon_dashboard(df: pd.DataFrame):
    """Отрисовка интерактивной панели углеродного следа и эмиссий CO2."""
    st.markdown("## 🌍 Углеродный след в растениеводстве (CO₂-эмиссия)")
    st.caption("Анализ эмиссий на основе агротехнологий (No-Till vs Традиционная), операций и видов энергоресурсов")

    # --- KPI Карточки ---
    c1, c2, c3, c4 = st.columns(4)
    total_co2_ton = (df["co2_emission_kg"].sum() / 1000) if "co2_emission_kg" in df.columns else 0
    avg_per_ton = df["co2_per_ton"].mean() if "co2_per_ton" in df.columns else 0
    avg_f_razl = df["f_razl"].mean() if "f_razl" in df.columns else 0
    avg_yield = df["yield_t_ha"].mean() if "yield_t_ha" in df.columns else 0

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Всего выбросов CO₂-экв</div>
            <div class="metric-value">{total_co2_ton:,.1f} т</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Удельный след (ср.)</div>
            <div class="metric-value">{avg_per_ton:.1f} кг/т</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Ср. Фактор разложения Fразл</div>
            <div class="metric-value">{avg_f_razl:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Ср. Урожайность</div>
            <div class="metric-value">{avg_yield:.2f} т/га</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- Графики 1-го уровня ---
    g1, g2 = st.columns(2)

    with g1:
        if "technology" in df.columns and "co2_per_ton" in df.columns:
            fig_tech = px.box(
                df,
                x="crop",
                y="co2_per_ton",
                color="technology",
                title="🌱 Удельный углеродный след (кг CO₂/т): No-Till vs Классическая",
                labels={"co2_per_ton": "кг CO₂ на 1 т продукции", "crop": "Культура", "technology": "Технология"},
                color_discrete_map={"No-Till": "#2E7D32", "Классическая": "#D32F2F"},
                template="plotly_white"
            )
            st.plotly_chart(fig_tech, use_container_width=True)

    with g2:
        if "emission_type" in df.columns and "co2_emission_kg" in df.columns:
            df_src = df.groupby("emission_type")["co2_emission_kg"].sum().reset_index()
            fig_donut = px.pie(
                df_src,
                names="emission_type",
                values="co2_emission_kg",
                hole=0.45,
                title="⚡ Структура выбросов по видам ресурсов и энергоносителей",
                color_discrete_sequence=px.colors.qualitative.Safe,
                template="plotly_white"
            )
            st.plotly_chart(fig_donut, use_container_width=True)

    # --- Графики 2-го уровня ---
    g3, g4 = st.columns(2)

    with g3:
        if "operation" in df.columns and "co2_emission_kg" in df.columns:
            df_ops = df.groupby(["operation", "technology"])["co2_emission_kg"].sum().reset_index()
            fig_ops = px.bar(
                df_ops,
                x="operation",
                y="co2_emission_kg",
                color="technology",
                barmode="group",
                title="🚜 Выбросы CO₂ по этапам полевых операций (кг)",
                labels={"co2_emission_kg": "Выбросы CO₂ (кг)", "operation": "Операция"},
                template="plotly_white",
                color_discrete_map={"No-Till": "#388E3C", "Классическая": "#E57373"}
            )
            st.plotly_chart(fig_ops, use_container_width=True)

    with g4:
        if "yield_t_ha" in df.columns and "co2_emission_kg" in df.columns:
            fig_scatter = px.scatter(
                df,
                x="yield_t_ha",
                y="co2_emission_kg",
                color="crop",
                size="emission_coeff_e",
                hover_data=["technology", "operation"],
                title="🌾 Связь урожайности (т/га) и общего объема эмиссий (кг CO₂)",
                labels={"yield_t_ha": "Урожайность (т/га)", "co2_emission_kg": "Эмиссия CO₂ (кг/га)"},
                template="plotly_white"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    # --- Интерактивный калькулятор агроэкологического эффекта ---
    st.markdown("### 🧮 Интерактивный калькулятор снижения углеродного следа")
    with st.expander("Расчет перехода с Классической технологии на No-Till", expanded=False):
        c_calc1, c_calc2, c_calc3 = st.columns(3)
        with c_calc1:
            area_ha = st.number_input("Площадь угодий (га)", min_value=1.0, value=500.0, step=50.0)
        with c_calc2:
            calc_crop = st.selectbox("Культура", list(df["crop"].unique()))
        with c_calc3:
            diesel_economy_l = st.number_input("Экономия ДТ при No-Till (л/га)", min_value=0.0, value=35.0, step=5.0)

        # Коэффициент эмиссии дизеля ~ 2.68 кг CO2 / л
        co2_saved_diesel = area_ha * diesel_economy_l * 2.68
        f_diff = 0.20  # В среднем No-Till дает прирост гумификации Fразл на 15-25%
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.success(f"🌱 Сокращение прямых выбросов топлива: **{co2_saved_diesel / 1000:,.2f} т CO₂-экв** в сезон")
        with col_res2:
            st.info(f"📈 Дополнительное удержание углерода в почве за счет $F_{{разл}}$: **~{(area_ha * 180) / 1000:,.2f} т C**")

# ==========================================
# СТАНДАРТНЫЕ МИКРОКЛИМАТИЧЕСКИЕ ДАШБОРДЫ
# ==========================================
def render_kpi_metrics(df):
    c1, c2, c3 = st.columns(3)
    avg_temp = df["temperature"].mean() if "temperature" in df.columns else 0
    avg_hum = df["humidity"].mean() if "humidity" in df.columns else 0
    total_records = len(df)
    with c1:
        st.metric("Ср. Температура", f"{avg_temp:.1f} °C")
    with c2:
        st.metric("Ср. Влажность", f"{avg_hum:.1f} %")
    with c3:
        st.metric("Всего записей", total_records)