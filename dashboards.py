import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from styles import render_metric_card

def render_overview_kpis(df):
    """Отрисовка верхних карточек KPI."""
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        avg_b_carbon = df["B_Carbon"].mean() if "B_Carbon" in df.columns else 0.0
        render_metric_card("Средняя выгода CO2", f"{avg_b_carbon:.2f} т", "т CO2-экв/га за год")
    with c2:
        avg_cost = df["C_Total_Costs"].mean() if "C_Total_Costs" in df.columns else 0.0
        render_metric_card("Средние затраты", f"{avg_cost:,.0f} ₽", "тыс. руб./га")
    with c3:
        avg_eff = df["F6_1_Efficiency"].mean() if "F6_1_Efficiency" in df.columns else 0.0
        render_metric_card("Эффективность (F6.1)", f"{avg_eff:.2f}", "индекс")
    with c4:
        avg_risk = df["Risk_1_R"].mean() if "Risk_1_R" in df.columns else 0.0
        render_metric_card("Уровень риска (1-R)", f"{avg_risk:.2f}", "среднее значение")

def render_carbon_vs_economy(df):
    """График: углеродная выгода vs затраты."""
    st.subheader("Углеродная нейтральность vs Экономические затраты")
    if "C_Total_Costs" in df.columns and "B_Carbon" in df.columns and "Risk_1_R" in df.columns:
        fig = px.scatter(
            df,
            x="C_Total_Costs",
            y="B_Carbon",
            size="F6_1_Efficiency" if "F6_1_Efficiency" in df.columns else None,
            color="Risk_1_R",
            hover_data=["ID"] if "ID" in df.columns else None,
            title="Затраты (C) vs Выгода CO2 (Bcarbon)",
            labels={
                "C_Total_Costs": "Общие затраты (тыс. руб./га)",
                "B_Carbon": "Углеродная выгода (т CO2-экв/га)",
                "Risk_1_R": "Риск"
            },
            template="plotly_dark",
            color_continuous_scale="Viridis"
        )
        fig.update_layout(height=480, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

def render_climate_and_yield(df):
    """Анализ влияния погоды на урожайность (F5)."""
    st.subheader("Влияние температуры и осадков на урожайность")
    col1, col2 = st.columns(2)
    
    with col1:
        if "Temp_Avg_Apr_Jun" in df.columns and "F5_Yield_Forecast" in df.columns:
            fig1 = px.box(
                df,
                x="Temp_Avg_Apr_Jun",
                y="F5_Yield_Forecast",
                title="Урожайность (F5) по температурам (°C)",
                labels={"Temp_Avg_Apr_Jun": "Температура (°C)", "F5_Yield_Forecast": "Урожайность (кг/га)"},
                template="plotly_dark"
            )
            st.plotly_chart(fig1, use_container_width=True)
            
    with col2:
        if "Precipitation_P" in df.columns and "F5_Yield_Forecast" in df.columns:
            fig2 = px.scatter(
                df,
                x="Precipitation_P",
                y="F5_Yield_Forecast",
                trendline="ols",
                title="Урожайность vs Осадки (P, мм)",
                labels={"Precipitation_P": "Осадки (мм)", "F5_Yield_Forecast": "Урожайность (кг/га)"},
                template="plotly_dark"
            )
            st.plotly_chart(fig2, use_container_width=True)

def render_correlation_matrix(df):
    """Корреляционная матрица ключевых параметров."""
    st.subheader("Корреляционная матрица агро-экологических параметров")
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    key_cols = [c for c in [
        "F6_1_Efficiency", "B_Carbon", "C_Total_Costs", "PI_Priority_Index", 
        "F5_Yield_Forecast", "KPI_Field", "E_Rotation_Efficiency", 
        "Cost_Price_Season", "Fertilizer_Costs_Neutral"
    ] if c in numeric_df.columns]
    
    if len(key_cols) > 2:
        corr = numeric_df[key_cols].corr()
        fig = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale="RdBu_r",
            template="plotly_dark",
            title="Корреляции ключевых индексов"
        )
        st.plotly_chart(fig, use_container_width=True)
