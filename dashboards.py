import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from styles import render_metric_card

# Фирменная изумрудная палитра
ECO_PALETTE = ["#10b981", "#059669", "#34d399", "#6ee7b7", "#047857", "#a7f3d0", "#064e3b"]

def render_overview_kpis(df):
    """Отрисовка верхних карточек KPI."""
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        avg_b_carbon = df["B_Carbon"].mean() if "B_Carbon" in df.columns else 0.0
        render_metric_card("🌿 Выгода CO2 (Bcarbon)", f"{avg_b_carbon:.2f} т", "т CO2-экв/га за год")
    with c2:
        avg_cost = df["C_Total_Costs"].mean() if "C_Total_Costs" in df.columns else 0.0
        render_metric_card("💰 Общие затраты (C)", f"{avg_cost:,.0f} ₽", "тыс. руб./га")
    with c3:
        avg_eff = df["F6_1_Efficiency"].mean() if "F6_1_Efficiency" in df.columns else 0.0
        render_metric_card("⚡ Эффективность (F6.1)", f"{avg_eff:.2f}", "индекс нейтральности")
    with c4:
        avg_risk = df["Risk_1_R"].mean() if "Risk_1_R" in df.columns else 0.0
        render_metric_card("🛡️ Риск (1-R)", f"{avg_risk:.2f}", "средневзвешенный")

def render_donut_charts(df):
    """Два интерактивных бублика (Donut Charts)."""
    st.markdown('<h3 class="eco-header">🍩 Структура рисков и составляющих углеродного следа</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Бублик 1: Распределение категорий риска (1-R)
        if "Risk_1_R" in df.columns:
            risk_counts = df["Risk_1_R"].value_counts().reset_index()
            risk_counts.columns = ["Категория риска", "Количество полей"]
            risk_counts["Категория риска"] = risk_counts["Категория риска"].astype(str)
            
            fig_donut1 = go.Figure(data=[go.Pie(
                labels=risk_counts["Категория риска"],
                values=risk_counts["Количество полей"],
                hole=0.62,
                marker=dict(colors=ECO_PALETTE),
                textinfo="label+percent",
                hoverinfo="label+value+percent"
            )])
            fig_donut1.update_layout(
                title_text="<b>Распределение полей по рискам (1-R)</b>",
                title_font=dict(color="#a7f3d0", size=15),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
                annotations=[dict(text='РИСКИ<br>(1-R)', x=0.5, y=0.5, font_size=15, font_color="#34d399", showarrow=False)],
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_donut1, use_container_width=True)
            
    with col2:
        # Бублик 2: Доли операций в совокупном следе
        harvest_sum = df["CF_Harvest"].abs().sum() if "CF_Harvest" in df.columns else 100
        leaf_sum = df["CF_Leaf_Operations"].abs().sum() if "CF_Leaf_Operations" in df.columns else 100
        fert_sum = df["Fertilizer_Costs_Neutral"].abs().sum() if "Fertilizer_Costs_Neutral" in df.columns else 50
        
        balance_df = pd.DataFrame({
            "Источник эмиссии": ["CF уборки (C_Fуб)", "CF листовых операций", "Удобрения с нейтральностью"],
            "Объем": [harvest_sum, leaf_sum, fert_sum]
        })
        
        fig_donut2 = go.Figure(data=[go.Pie(
            labels=balance_df["Источник эмиссии"],
            values=balance_df["Объем"],
            hole=0.62,
            marker=dict(colors=["#059669", "#10b981", "#34d399"]),
            textinfo="label+percent",
            hoverinfo="label+value+percent"
        )])
        fig_donut2.update_layout(
            title_text="<b>Доля операций в углеродном балансе</b>",
            title_font=dict(color="#a7f3d0", size=15),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            annotations=[dict(text='БАЛАНС<br>CO2', x=0.5, y=0.5, font_size=15, font_color="#34d399", showarrow=False)],
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_donut2, use_container_width=True)

def render_carbon_vs_economy(df):
    """Интерактивный Bubble Chart: Затраты vs Выгода CO2."""
    st.markdown('<h3 class="eco-header">📈 Затраты vs Углеродная выгода</h3>', unsafe_allow_html=True)
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
                "F6_1_Efficiency": "Эффективность F6.1"
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

def render_climate_and_yield(df):
    """Анализ климата и урожайности."""
    st.markdown('<h3 class="eco-header">⛅ Климатический профиль и прогноз урожайности (F5)</h3>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if "Temp_Avg_Apr_Jun" in df.columns and "F5_Yield_Forecast" in df.columns:
            fig1 = px.box(
                df,
                x="Temp_Avg_Apr_Jun",
                y="F5_Yield_Forecast",
                color="Temp_Avg_Apr_Jun",
                color_discrete_sequence=ECO_PALETTE,
                title="Урожайность по температурам апреля–июня (°C)",
                labels={"Temp_Avg_Apr_Jun": "Температура (°C)", "F5_Yield_Forecast": "Урожайность (кг/га)"}
            )
            fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(6,78,59,0.1)", font=dict(color="#ffffff"))
            st.plotly_chart(fig1, use_container_width=True)
    with c2:
        if "Precipitation_P" in df.columns and "F5_Yield_Forecast" in df.columns:
            fig2 = px.scatter(
                df,
                x="Precipitation_P",
                y="F5_Yield_Forecast",
                trendline="ols",
                color_discrete_sequence=["#34d399"],
                title="Урожайность vs Уровень осадков (мм)",
                labels={"Precipitation_P": "Осадки (мм)", "F5_Yield_Forecast": "Урожайность (кг/га)"}
            )
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(6,78,59,0.1)", font=dict(color="#ffffff"))
            st.plotly_chart(fig2, use_container_width=True)

def render_top_fields(df):
    """ТОП-10 полей по выгоде поглощения CO2."""
    st.markdown('<h3 class="eco-header">🏆 ТОП-10 полей по снижению выбросов (Bcarbon)</h3>', unsafe_allow_html=True)
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
            height=380
        )
        st.plotly_chart(fig, use_container_width=True)

def render_correlation_matrix(df):
    """Матрица корреляций."""
    st.markdown('<h3 class="eco-header">🔬 Корреляционная матрица ключевых агро-параметров</h3>', unsafe_allow_html=True)
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
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#ffffff"))
        st.plotly_chart(fig, use_container_width=True)
