import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render_carbon_dashboard(df: pd.DataFrame, theme="dark"):
    st.markdown('<div class="main-header">🌍 Углеродный след в растениеводстве</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Оценка эмиссий CO₂-эквивалента по культурам, агротехнологиям и операциям</div>', unsafe_allow_html=True)

    # 1. Метрики KPI
    c1, c2, c3, c4 = st.columns(4)
    total_co2_ton = (df["co2_emission_kg"].sum() / 1000) if "co2_emission_kg" in df.columns else 0
    avg_per_ton = df["co2_per_ton"].mean() if "co2_per_ton" in df.columns else 0
    avg_f_razl = df["f_razl"].mean() if "f_razl" in df.columns else 0
    avg_yield = df["yield_t_ha"].mean() if "yield_t_ha" in df.columns else 0

    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Суммарные выбросы</div><div class="metric-value">{total_co2_ton:,.1f} т CO₂</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Удельный след (ср.)</div><div class="metric-value">{avg_per_ton:.1f} кг/т</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Фактор разложения Fразл</div><div class="metric-value">{avg_f_razl:.2f}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Ср. Урожайность</div><div class="metric-value">{avg_yield:.2f} т/га</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    plot_template = "plotly_dark" if theme == "dark" else "plotly_white"
    tech_colors = {"No-Till": "#52B788", "Классическая": "#E07A5F"} if theme == "dark" else {"No-Till": "#2E7D32", "Классическая": "#C62828"}

    # 2. Графики Ряд 1
    g1, g2 = st.columns(2)
    with g1:
        if "technology" in df.columns and "co2_per_ton" in df.columns:
            fig_tech = px.box(
                df, x="crop", y="co2_per_ton", color="technology",
                title="🌱 Удельный след (кг CO₂/т): No-Till vs Классическая",
                labels={"co2_per_ton": "кг CO₂ на 1 т продукции", "crop": "Культура", "technology": "Технология"},
                color_discrete_map=tech_colors,
                template=plot_template
            )
            fig_tech.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_tech, use_container_width=True)

    # === БЛОК С БУБЛИКОМ (7 КНОПОК PLOTLY + РОДНАЯ КНОПКА ФУЛСКРИНА STREAMLIT) ===
    with g2:
        if "emission_type" in df.columns and "co2_emission_kg" in df.columns:
            df_src = df.groupby("emission_type")["co2_emission_kg"].sum().reset_index()
            fig_donut = px.pie(
                df_src, names="emission_type", values="co2_emission_kg", hole=0.45,
                title="Структура выбросов по ресурсам",
                color_discrete_sequence=px.colors.qualitative.Safe,
                template=plot_template
            )
            fig_donut.update_layout(
                margin=dict(t=50, r=20, l=20, b=20)
            )
            donut_toolbar_config = {
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtons': [[
                    'toImage',
                    'zoom2d',
                    'pan2d',
                    'zoomIn2d',
                    'zoomOut2d',
                    'autoScale2d',
                    'resetScale2d'
                ]],
                'responsive': True
            }
            st.plotly_chart(fig_donut, use_container_width=True, config=donut_toolbar_config)

    # 3. Графики Ряд 2
    g3, g4 = st.columns(2)
    with g3:
        if "operation" in df.columns and "co2_emission_kg" in df.columns:
            df_ops = df.groupby(["operation", "technology"])["co2_emission_kg"].sum().reset_index()
            fig_ops = px.bar(
                df_ops, x="operation", y="co2_emission_kg", color="technology", barmode="group",
                title="🚜 Выбросы CO₂ по полевым операциям (кг)",
                labels={"co2_emission_kg": "Выбросы CO₂ (кг)", "operation": "Операция"},
                color_discrete_map=tech_colors,
                template=plot_template
            )
            st.plotly_chart(fig_ops, use_container_width=True)

    with g4:
        if "yield_t_ha" in df.columns and "co2_emission_kg" in df.columns:
            fig_scatter = px.scatter(
                df, x="yield_t_ha", y="co2_emission_kg", color="crop",
                size="emission_coeff_e",
                hover_data=["technology", "operation"],
                title="🌾 Зависимость объема выбросов от урожайности",
                labels={"yield_t_ha": "Урожайность (т/га)", "co2_emission_kg": "Эмиссия CO₂ (кг/га)"},
                template=plot_template
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    # 4. Калькулятор No-Till
    st.markdown("### 🧮 Калькулятор эффекта внедрения No-Till")
    with st.expander("Расчет сокращения углеродного следа и экономии топлива", expanded=True):
        c_calc1, c_calc2, c_calc3 = st.columns(3)
        with c_calc1:
            area_ha = st.number_input("Площадь угодий (га)", min_value=10.0, value=1000.0, step=50.0)
        with c_calc2:
            crops_list = sorted(list(df["crop"].unique())) if "crop" in df.columns else ["Все"]
            calc_crop = st.selectbox("Культура", crops_list)
        with c_calc3:
            diesel_saved_per_ha = st.number_input("Экономия ДТ при No-Till (л/га)", min_value=0.0, value=32.0, step=2.0)

        co2_saved_fuel = (area_ha * diesel_saved_per_ha * 2.68) / 1000
        humus_carbon_saved = (area_ha * 210) / 1000

        res1, res2 = st.columns(2)
        with res1:
            st.success(f"🌱 Сокращение прямых выбросов топлива: **{co2_saved_fuel:,.2f} т CO₂-экв/год**")
        with res2:
            st.info(f"📈 Дополнительное депонирование углерода в почве: **~{humus_carbon_saved:,.2f} т C/год**")

def render_kpi_metrics(df):
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Температура", "4.2 °C")
    with c2:
        st.metric("Влажность", "91.5 %")

def render_storage_climate(df):
    render_kpi_metrics(df)