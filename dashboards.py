import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from styles import render_metric_card

ECO_GREENS = ["#10b981", "#059669", "#34d399", "#6ee7b7", "#047857", "#a7f3d0", "#022c22"]

def render_overview_kpis(df: pd.DataFrame):
    """Карточки ключевых показателей."""
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        avg_b = df["B_Carbon"].mean() if "B_Carbon" in df.columns else 0.0
        render_metric_card("🌿 Выгода CO2 (Bcarbon)", f"{avg_b:.2f} т", "т CO2-экв/га за год")
    with c2:
        avg_c = df["C_Total_Costs"].mean() if "C_Total_Costs" in df.columns else 0.0
        render_metric_card("💰 Затраты (C)", f"{avg_c:,.0f} ₽", "тыс. руб./га")
    with c3:
        avg_f = df["F6_1_Efficiency"].mean() if "F6_1_Efficiency" in df.columns else 0.0
        render_metric_card("⚡ Эффективность (F6.1)", f"{avg_f:.2f}", "индекс нейтральности")
    with c4:
        avg_r = df["Risk_1_R"].mean() if "Risk_1_R" in df.columns else 0.0
        render_metric_card("🛡️ Уровень риска (1-R)", f"{avg_r:.2f}", "среднее по выборке")

def render_donut_charts(df: pd.DataFrame):
    """Два раздельных и просторных бублика с четкими отступами."""
    st.markdown('<div class="section-title">🍩 Структура баланса эмиссий и распределение рисков</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        if "Risk_1_R" in df.columns:
            r_counts = df["Risk_1_R"].value_counts().reset_index()
            r_counts.columns = ["Риск", "Полей"]
            r_counts["Риск_Имя"] = "Риск " + r_counts["Риск"].astype(str)
            
            fig1 = go.Figure(data=[go.Pie(
                labels=r_counts["Риск_Имя"],
                values=r_counts["Полей"],
                hole=0.60,
                marker=dict(colors=ECO_GREENS, line=dict(color='#022c22', width=2)),
                textinfo="percent+label",
                textposition="outside",
                showlegend=False
            )])
            fig1.update_layout(
                title=dict(text="<b>Распределение полей по рискам (1-R)</b>", font=dict(color="#a7f3d0", size=15), x=0.5),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
                height=380,
                margin=dict(l=30, r=30, t=50, b=30),
                annotations=[dict(text="РИСКИ<br><b>1-R</b>", x=0.5, y=0.5, font_size=14, font_color="#34d399", showarrow=False)]
            )
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        h_sum = df["CF_Harvest"].abs().sum() if "CF_Harvest" in df.columns else 100
        l_sum = df["CF_Leaf_Operations"].abs().sum() if "CF_Leaf_Operations" in df.columns else 100
        f_sum = df["Fertilizer_Costs_Neutral"].abs().sum() if "Fertilizer_Costs_Neutral" in df.columns else 50
        
        balance_df = pd.DataFrame({
            "Компонент": ["CF уборки", "CF операций на листе", "Удобрения с нейтр."],
            "Объем": [h_sum, l_sum, f_sum]
        })
        
        fig2 = go.Figure(data=[go.Pie(
            labels=balance_df["Компонент"],
            values=balance_df["Объем"],
            hole=0.60,
            marker=dict(colors=["#059669", "#10b981", "#34d399"], line=dict(color='#022c22', width=2)),
            textinfo="percent+label",
            textposition="outside",
            showlegend=False
        )])
        fig2.update_layout(
            title=dict(text="<b>Вклад операций в углеродный след</b>", font=dict(color="#a7f3d0", size=15), x=0.5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            height=380,
            margin=dict(l=30, r=30, t=50, b=30),
            annotations=[dict(text="ЭМИССИИ<br><b>CO2</b>", x=0.5, y=0.5, font_size=14, font_color="#34d399", showarrow=False)]
        )
        st.plotly_chart(fig2, use_container_width=True)

def render_carbon_vs_economy(df: pd.DataFrame):
    """Точечный график взаимосвязи выгоды CO2 и затрат."""
    st.markdown('<div class="section-title">📈 Оценка эффективности: Затраты (C) vs Выгода (Bcarbon)</div>', unsafe_allow_html=True)
    if "C_Total_Costs" in df.columns and "B_Carbon" in df.columns:
        fig = px.scatter(
            df,
            x="C_Total_Costs",
            y="B_Carbon",
            size="F6_1_Efficiency" if "F6_1_Efficiency" in df.columns else None,
            color="Risk_1_R" if "Risk_1_R" in df.columns else None,
            hover_data=["ID", "E_Rotation_Efficiency"] if "ID" in df.columns and "E_Rotation_Efficiency" in df.columns else None,
            labels={
                "C_Total_Costs": "Общие затраты (тыс. руб./га)",
                "B_Carbon": "Углеродная выгода Bcarbon (т CO2-экв/га)",
                "Risk_1_R": "Риск (1-R)",
                "F6_1_Efficiency": "Индекс F6.1"
            },
            color_continuous_scale=["#022c22", "#059669", "#10b981", "#34d399", "#a7f3d0"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(6, 78, 59, 0.15)",
            font=dict(color="#ffffff"),
            height=460,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

def render_climate_and_yield(df: pd.DataFrame):
    """Климатический анализ."""
    st.markdown('<div class="section-title">⛅ Влияние климата на прогнозную урожайность (F5)</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if "Temp_Avg_Apr_Jun" in df.columns and "F5_Yield_Forecast" in df.columns:
            fig1 = px.box(
                df,
                x="Temp_Avg_Apr_Jun",
                y="F5_Yield_Forecast",
                color="Temp_Avg_Apr_Jun",
                color_discrete_sequence=ECO_GREENS,
                title="Урожайность по температурам (°C)",
                labels={"Temp_Avg_Apr_Jun": "Температура апр–июн (°C)", "F5_Yield_Forecast": "Урожайность (кг/га)"}
            )
            fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(6,78,59,0.1)", font=dict(color="#ffffff"), showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
    with c2:
        if "Precipitation_P" in df.columns and "F5_Yield_Forecast" in df.columns:
            fig2 = px.scatter(
                df,
                x="Precipitation_P",
                y="F5_Yield_Forecast",
                trendline="ols",
                color_discrete_sequence=["#34d399"],
                title="Урожайность vs Осадки (P, мм)",
                labels={"Precipitation_P": "Осадки (мм)", "F5_Yield_Forecast": "Урожайность (кг/га)"}
            )
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(6,78,59,0.1)", font=dict(color="#ffffff"))
            st.plotly_chart(fig2, use_container_width=True)

def render_top_fields(df: pd.DataFrame):
    """ТОП-10 полей лидеров по Bcarbon."""
    st.markdown('<div class="section-title">🏆 ТОП-10 полей по максимальной углеродной выгоде</div>', unsafe_allow_html=True)
    if "B_Carbon" in df.columns and "ID" in df.columns:
        top10 = df.sort_values(by="B_Carbon", ascending=False).head(10).copy()
        top10["Поле"] = "Поле № " + top10["ID"].astype(str)
        
        fig = px.bar(
            top10,
            x="B_Carbon",
            y="Поле",
            orientation="h",
            color="B_Carbon",
            color_continuous_scale=["#059669", "#10b981", "#34d399"],
            labels={"B_Carbon": "Выгода CO2 (т CO2-экв/га)", "Поле": "Поле"}
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(6, 78, 59, 0.1)",
            font=dict(color="#ffffff"),
            yaxis=dict(autorange="reversed"),
            height=360
        )
        st.plotly_chart(fig, use_container_width=True)

def render_correlation_matrix(df: pd.DataFrame):
    """Тепловая карта корреляций."""
    st.markdown('<div class="section-title">🔬 Корреляционная матрица параметров</div>', unsafe_allow_html=True)
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
            color_continuous_scale=["#047857", "#064e3b", "#0f172a", "#10b981", "#34d399"],
            title="Тепловая карта взаимосвязей"
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#ffffff"), height=420)
        st.plotly_chart(fig, use_container_width=True)
