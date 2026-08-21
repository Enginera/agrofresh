import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Точные цвета для культур, соответствующие цветным маркерам в сайдбаре
CROP_COLOR_MAP = {
    "Кукуруза": "#4EA8DE",          # 🔵 Голубой
    "Горох": "#52B788",             # 🟢 Зеленый
    "Озимая пшеница": "#F4A261",    # 🟠 Янтарный
    "Лён": "#E07A5F",               # 🟤 Терракотовый
    "Многолетние травы": "#3D5A80",  # 🔷 Индиго
    "Подсолнечник": "#9D4EDD"       # 🟣 Фиолетовый
}

TECH_COLOR_MAP = {
    "No-Till": "#2E7D32",           # 🌱 Зеленый
    "Классическая": "#C62828"       # 🚜 Красный
}

CHART_CONFIG = {
    'displayModeBar': 'hover',
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'responsive': True
}

def get_plot_theme(theme="dark"):
    is_dark = theme == "dark"
    bg_color = "#1A2E24" if is_dark else "#FFFFFF"
    text_color = "#EEF6F1" if is_dark else "#1B3826"
    sub_color = "#9BB3A6" if is_dark else "#526B5C"
    grid_color = "#274435" if is_dark else "#EAEFEA"
    line_color = "#3A5C4A" if is_dark else "#D0DCD4"

    modebar_bg = "rgba(20, 36, 28, 0.9)" if is_dark else "rgba(235, 243, 238, 0.95)"
    modebar_color = "#A8CDB8" if is_dark else "#2D5A40"
    modebar_active = "#52B788" if is_dark else "#1B4332"

    return {
        "layout": go.Layout(
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font=dict(family="Plus Jakarta Sans, sans-serif", color=text_color, size=12),
            title=dict(font=dict(color=text_color, size=13), y=0.98, x=0.01, xanchor="left"),
            modebar=dict(bgcolor=modebar_bg, color=modebar_color, activecolor=modebar_active, orientation="h"),
            # Адаптивные отступы: графики занимают 100% ширины на телефонах и ПК
            margin=dict(l=25, r=20, t=45, b=45),
            xaxis=dict(gridcolor=grid_color, linecolor=line_color, tickfont=dict(color=sub_color, size=10), automargin=True),
            yaxis=dict(gridcolor=grid_color, linecolor=line_color, tickfont=dict(color=sub_color, size=10), automargin=True),
            # Нижняя горизонтальная легенда для мобильной адаптивности
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(color=text_color, size=11)
            )
        )
    }

def render_carbon_dashboard(df: pd.DataFrame, theme="dark"):
    st.markdown('<div class="main-header">🌍 Углеродный след в растениеводстве</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Оценка эмиссий CO₂-эквивалента по культурам, агротехнологиям и операциям</div>', unsafe_allow_html=True)

    # 1. Карточки KPI
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

    agro_palette = ["#52B788", "#74C69D", "#E07A5F", "#81B29A", "#F4A261", "#4EA8DE"] if theme == "dark" else px.colors.qualitative.Safe
    text_color = "#EEF6F1" if theme == "dark" else "#1B3826"
    pie_border = "#1A2E24" if theme == "dark" else "#FFFFFF"

    # 2. Графики Ряд 1
    g1, g2 = st.columns(2)
    with g1:
        if "technology" in df.columns and "co2_per_ton" in df.columns:
            fig_tech = px.box(
                df, x="crop", y="co2_per_ton", color="technology",
                title="🌱 Удельный след (кг CO₂/т): No-Till vs Классическая",
                labels={"co2_per_ton": "кг CO₂ на 1 т продукции", "crop": "Культура", "technology": "Технология"},
                color_discrete_map=TECH_COLOR_MAP
            )
            fig_tech.update_layout(get_plot_theme(theme)["layout"])
            fig_tech.update_xaxes(tickangle=-20, automargin=True)
            st.plotly_chart(fig_tech, use_container_width=True, config=CHART_CONFIG)

    with g2:
        if "emission_type" in df.columns and "co2_emission_kg" in df.columns:
            df_src = df.groupby("emission_type")["co2_emission_kg"].sum().reset_index()
            fig_donut = px.pie(
                df_src, names="emission_type", values="co2_emission_kg", hole=0.50,
                title="⚡ Структура выбросов по энергоносителям и ресурсам",
                color_discrete_sequence=agro_palette
            )
            fig_donut.update_traces(textposition='inside', textinfo='percent', marker=dict(line=dict(color=pie_border, width=2)))
            fig_donut.update_layout(get_plot_theme(theme)["layout"])
            st.plotly_chart(fig_donut, use_container_width=True, config=CHART_CONFIG)

    # 3. Графики Ряд 2
    g3, g4 = st.columns(2)
    with g3:
        if "operation" in df.columns and "co2_emission_kg" in df.columns:
            df_ops = df.groupby(["operation", "technology"])["co2_emission_kg"].sum().reset_index()
            fig_ops = px.bar(
                df_ops, x="operation", y="co2_emission_kg", color="technology", barmode="group",
                title="🚜 Выбросы CO₂ по полевым операциям (кг)",
                labels={"co2_emission_kg": "Выбросы CO₂ (кг)", "operation": "Операция", "technology": "Технология"},
                color_discrete_map=TECH_COLOR_MAP
            )
            fig_ops.update_layout(get_plot_theme(theme)["layout"])
            fig_ops.update_xaxes(tickangle=-20, automargin=True)
            st.plotly_chart(fig_ops, use_container_width=True, config=CHART_CONFIG)

    with g4:
        if "yield_t_ha" in df.columns and "co2_emission_kg" in df.columns:
            fig_scatter = px.scatter(
                df, x="yield_t_ha", y="co2_emission_kg", color="crop",
                size="emission_coeff_e",
                size_max=15,
                hover_data=["technology", "operation"],
                title="🌾 Зависимость объема выбросов от урожайности",
                labels={"yield_t_ha": "Урожайность (т/га)", "co2_emission_kg": "Эмиссия CO₂ (кг/га)", "crop": "Культура"},
                color_discrete_map=CROP_COLOR_MAP
            )
            
            border_color = "rgba(255, 255, 255, 0.8)" if theme == "dark" else "rgba(0, 0, 0, 0.4)"
            fig_scatter.update_traces(marker=dict(opacity=0.75, line=dict(width=1.2, color=border_color)))
            
            scatter_layout = get_plot_theme(theme)["layout"]
            fig_scatter.update_layout(scatter_layout)
            # Отдельный отступ снизу под горизонтальный перечень 6 культур
            fig_scatter.update_layout(
                margin=dict(l=25, r=20, t=45, b=65),
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.28,
                    xanchor="center",
                    x=0.5,
                    font=dict(color=text_color, size=10)
                )
            )
            st.plotly_chart(fig_scatter, use_container_width=True, config=CHART_CONFIG)

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