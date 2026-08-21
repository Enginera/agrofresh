import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Цветовой маппинг под маркеры сайдбара
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

# Компактный режим панели инструментов (виден, стилизован, не мешает)
CHART_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'responsive': True
}

def get_plot_theme(theme="dark"):
    is_dark = theme == "dark"
    bg_color = "#182C22" if is_dark else "#FFFFFF"
    text_color = "#EEF6F1" if is_dark else "#122B1E"
    sub_color = "#9BB3A6" if is_dark else "#5A7565"
    grid_color = "#244233" if is_dark else "#EAF1EC"
    line_color = "#2F5441" if is_dark else "#CFDDD3"

    # Аккуратный полупрозрачный pill-виджет панели инструментов
    modebar_bg = "rgba(24, 44, 34, 0.85)" if is_dark else "rgba(240, 246, 242, 0.9)"
    modebar_color = "#9EC7B0" if is_dark else "#2E5E42"
    modebar_active = "#52B788" if is_dark else "#1B4332"

    return {
        "layout": go.Layout(
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font=dict(family="Plus Jakarta Sans, sans-serif", color=text_color, size=11),
            title=dict(
                font=dict(color=text_color, size=12.5),
                y=0.96,
                x=0.01,
                xanchor="left"
            ),
            modebar=dict(
                bgcolor=modebar_bg,
                color=modebar_color,
                activecolor=modebar_active,
                orientation="h"
            ),
            # Эргономичные отступы под 100% ширины
            margin=dict(l=25, r=20, t=48, b=45),
            xaxis=dict(
                gridcolor=grid_color,
                linecolor=line_color,
                tickfont=dict(color=sub_color, size=10),
                automargin=True
            ),
            yaxis=dict(
                gridcolor=grid_color,
                linecolor=line_color,
                tickfont=dict(color=sub_color, size=10),
                automargin=True
            ),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.22,
                xanchor="center",
                x=0.5,
                font=dict(color=text_color, size=10.5)
            )
        )
    }

def render_carbon_dashboard(df: pd.DataFrame, theme="dark"):
    st.markdown('<div class="main-header">🌍 Углеродный след в растениеводстве</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Оценка эмиссий CO₂-эквивалента по культурам, агротехнологиям и операциям</div>', unsafe_allow_html=True)

    # 1. Адаптивные карточки KPI
    c1, c2, c3, c4 = st.columns(4)
    total_co2_ton = (df["co2_emission_kg"].sum() / 1000) if "co2_emission_kg" in df.columns else 0
    avg_per_ton = df["co2_per_ton"].mean() if "co2_per_ton" in df.columns else 0
    avg_f_razl = df["f_razl"].mean() if "f_razl" in df.columns else 0
    avg_yield = df["yield_t_ha"].mean() if "yield_t_ha" in df.columns else 0

    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Суммарные выбросы</div><div class="metric-value">{total_co2_ton:,.1f} <span style="font-size:0.9rem;font-weight:500;">т CO₂</span></div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Удельный след (ср.)</div><div class="metric-value">{avg_per_ton:.1f} <span style="font-size:0.9rem;font-weight:500;">кг/т</span></div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Фактор разложения Fразл</div><div class="metric-value">{avg_f_razl:.2f}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Ср. Урожайность</div><div class="metric-value">{avg_yield:.2f} <span style="font-size:0.9rem;font-weight:500;">т/га</span></div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    agro_palette = ["#52B788", "#74C69D", "#E07A5F", "#81B29A", "#F4A261", "#4EA8DE"] if theme == "dark" else px.colors.qualitative.Safe
    text_color = "#EEF6F1" if theme == "dark" else "#122B1E"
    pie_border = "#182C22" if theme == "dark" else "#FFFFFF"

    # 2. Графики Ряд 1
    g1, g2 = st.columns(2)
    with g1:
        if "technology" in df.columns and "co2_per_ton" in df.columns:
            fig_tech = px.box(
                df, x="crop", y="co2_per_ton", color="technology",
                title="<b>Удельный след (кг CO₂/т):</b> No-Till vs Классическая",
                labels={"co2_per_ton": "кг CO₂/т", "crop": "Культура", "technology": "Технология"},
                color_discrete_map=TECH_COLOR_MAP
            )
            fig_tech.update_layout(get_plot_theme(theme)["layout"])
            fig_tech.update_xaxes(tickangle=-15, automargin=True)
            st.plotly_chart(fig_tech, use_container_width=True, config=CHART_CONFIG)

    with g2:
        if "emission_type" in df.columns and "co2_emission_kg" in df.columns:
            df_src = df.groupby("emission_type")["co2_emission_kg"].sum().reset_index()
            fig_donut = px.pie(
                df_src, names="emission_type", values="co2_emission_kg", hole=0.52,
                title="<b>Структура выбросов по ресурсам</b>",
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
                title="<b>Выбросы CO₂ по операциям (кг)</b>",
                labels={"co2_emission_kg": "Выбросы CO₂ (кг)", "operation": "Операция", "technology": "Технология"},
                color_discrete_map=TECH_COLOR_MAP
            )
            fig_ops.update_layout(get_plot_theme(theme)["layout"])
            fig_ops.update_xaxes(tickangle=-15, automargin=True)
            st.plotly_chart(fig_ops, use_container_width=True, config=CHART_CONFIG)

    with g4:
        if "yield_t_ha" in df.columns and "co2_emission_kg" in df.columns:
            fig_scatter = px.scatter(
                df, x="yield_t_ha", y="co2_emission_kg", color="crop",
                size="emission_coeff_e",
                size_max=15,
                hover_data=["technology", "operation"],
                title="<b>Корреляция:</b> Урожайность vs Выбросы CO₂",
                labels={"yield_t_ha": "Урожайность (т/га)", "co2_emission_kg": "Эмиссия CO₂ (кг/га)", "crop": "Культура"},
                color_discrete_map=CROP_COLOR_MAP
            )
            border_color = "rgba(255, 255, 255, 0.85)" if theme == "dark" else "rgba(0, 0, 0, 0.35)"
            fig_scatter.update_traces(marker=dict(opacity=0.75, line=dict(width=1.2, color=border_color)))
            
            scatter_layout = get_plot_theme(theme)["layout"]
            fig_scatter.update_layout(scatter_layout)
            fig_scatter.update_layout(
                margin=dict(l=25, r=20, t=48, b=60),
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.26,
                    xanchor="center",
                    x=0.5,
                    font=dict(color=text_color, size=10)
                )
            )
            st.plotly_chart(fig_scatter, use_container_width=True, config=CHART_CONFIG)

    # 4. Калькулятор No-Till
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown("### 🧮 Калькулятор эффекта No-Till")
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

        r1, r2 = st.columns(2)
        with r1:
            st.markdown(f"""
            <div class="calc-card">
                <div class="calc-title">Сокращение прямых выбросов топлива</div>
                <div class="calc-val">-{co2_saved_fuel:,.2f} <span style="font-size:0.85rem;font-weight:500;">т CO₂-экв/год</span></div>
                <div style="font-size:0.78rem;color:var(--text-muted);margin-top:4px;">Фактор эмиссии ДТ: 2.68 кг CO₂/л</div>
            </div>
            """, unsafe_allow_html=True)

        with r2:
            st.markdown(f"""
            <div class="calc-card">
                <div class="calc-title">Депонирование углерода в почве</div>
                <div class="calc-val">+{humus_carbon_saved:,.2f} <span style="font-size:0.85rem;font-weight:500;">т C/год</span></div>
                <div style="font-size:0.78rem;color:var(--text-muted);margin-top:4px;">Сохранение органического вещества почвы</div>
            </div>
            """, unsafe_allow_html=True)

def render_kpi_metrics(df):
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Температура", "4.2 °C")
    with c2:
        st.metric("Влажность", "91.5 %")

def render_storage_climate(df):
    render_kpi_metrics(df)