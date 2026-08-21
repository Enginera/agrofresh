import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

AGRO_PALETTE = ["#2D6A4F", "#52B788", "#E07A5F", "#3D5A80", "#F4A261", "#81B29A"]
TECH_COLORS = {"No-Till": "#2D6A4F", "Классическая": "#E07A5F"}

def get_plot_theme():
    return {
        "layout": go.Layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(family="Plus Jakarta Sans, sans-serif", color="#121F17", size=12),
            margin=dict(l=30, r=20, t=50, b=30),
            xaxis=dict(
                gridcolor="#EEF2EF",
                showline=True,
                linecolor="#DDE5DF",
                tickfont=dict(size=11, color="#586B60")
            ),
            yaxis=dict(
                gridcolor="#EEF2EF",
                showline=True,
                linecolor="#DDE5DF",
                tickfont=dict(size=11, color="#586B60")
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=11)
            )
        )
    }

def render_carbon_dashboard(df: pd.DataFrame):
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">🌱 Carbon Telemetry & Yield Intelligence</div>
        <div class="hero-title">Углеродный след в растениеводстве</div>
        <div class="hero-subtitle">Мониторинг удельных и валовых эмиссий CO₂-эквивалента по агротехнологиям, полевым операциям и расходу энергоносителей.</div>
    </div>
    """, unsafe_allow_html=True)

    # 1. KPI Cards
    total_co2_ton = (df["co2_emission_kg"].sum() / 1000) if "co2_emission_kg" in df.columns else 0.0
    avg_per_ton = df["co2_per_ton"].mean() if "co2_per_ton" in df.columns else 0.0
    avg_f_razl = df["f_razl"].mean() if "f_razl" in df.columns else 0.0
    avg_yield = df["yield_t_ha"].mean() if "yield_t_ha" in df.columns else 0.0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-grid-card">
            <div class="metric-label-row">
                <span class="metric-label">Суммарный выброс</span>
                <span class="metric-icon-badge">☁️</span>
            </div>
            <div>
                <span class="metric-value-num">{total_co2_ton:,.1f}</span>
                <span class="metric-unit">т CO₂</span>
            </div>
            <div class="metric-pill pill-orange">Валовая эмиссия</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-grid-card">
            <div class="metric-label-row">
                <span class="metric-label">Удельный след</span>
                <span class="metric-icon-badge">🎯</span>
            </div>
            <div>
                <span class="metric-value-num">{avg_per_ton:.1f}</span>
                <span class="metric-unit">кг/т</span>
            </div>
            <div class="metric-pill pill-green">Среднее по выборке</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-grid-card">
            <div class="metric-label-row">
                <span class="metric-label">Фактор разложения Fразл</span>
                <span class="metric-icon-badge">🍂</span>
            </div>
            <div>
                <span class="metric-value-num">{avg_f_razl:.2f}</span>
                <span class="metric-unit">гумус</span>
            </div>
            <div class="metric-pill pill-green">Индекс минерализации</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-grid-card">
            <div class="metric-label-row">
                <span class="metric-label">Ср. Урожайность</span>
                <span class="metric-icon-badge">🌾</span>
            </div>
            <div>
                <span class="metric-value-num">{avg_yield:.2f}</span>
                <span class="metric-unit">т/га</span>
            </div>
            <div class="metric-pill pill-green">Продуктивность угодий</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # 2. Charts Row 1
    g1, g2 = st.columns(2)
    with g1:
        if "technology" in df.columns and "co2_per_ton" in df.columns:
            fig_tech = px.box(
                df, x="crop", y="co2_per_ton", color="technology",
                title="<b>Сравнение следа (кг CO₂/т):</b> No-Till vs Классическая",
                labels={"co2_per_ton": "кг CO₂/т", "crop": "Культура", "technology": "Технология"},
                color_discrete_map=TECH_COLORS
            )
            fig_tech.update_layout(get_plot_theme()["layout"])
            st.plotly_chart(fig_tech, use_container_width=True)

    with g2:
        if "emission_type" in df.columns and "co2_emission_kg" in df.columns:
            df_src = df.groupby("emission_type")["co2_emission_kg"].sum().reset_index()
            fig_donut = px.pie(
                df_src, names="emission_type", values="co2_emission_kg", hole=0.55,
                title="<b>Структура выбросов по ресурсам и энергоносителям</b>",
                color_discrete_sequence=AGRO_PALETTE
            )
            fig_donut.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
            fig_donut.update_layout(get_plot_theme()["layout"])
            st.plotly_chart(fig_donut, use_container_width=True)

    # 3. Charts Row 2
    g3, g4 = st.columns(2)
    with g3:
        if "operation" in df.columns and "co2_emission_kg" in df.columns:
            df_ops = df.groupby(["operation", "technology"])["co2_emission_kg"].sum().reset_index()
            fig_ops = px.bar(
                df_ops, x="operation", y="co2_emission_kg", color="technology", barmode="group",
                title="<b>Эмиссия CO₂ по полевым операциям (кг)</b>",
                labels={"co2_emission_kg": "Выбросы CO₂ (кг)", "operation": "Операция", "technology": "Технология"},
                color_discrete_map=TECH_COLORS
            )
            fig_ops.update_layout(get_plot_theme()["layout"])
            st.plotly_chart(fig_ops, use_container_width=True)

    with g4:
        if "yield_t_ha" in df.columns and "co2_emission_kg" in df.columns:
            fig_scatter = px.scatter(
                df, x="yield_t_ha", y="co2_emission_kg", color="crop",
                size="emission_coeff_e", hover_data=["technology", "operation"],
                title="<b>Корреляция:</b> Урожайность vs Выбросы CO₂",
                labels={"yield_t_ha": "Урожайность (т/га)", "co2_emission_kg": "Эмиссия CO₂ (кг/га)", "crop": "Культура"},
                color_discrete_sequence=AGRO_PALETTE
            )
            fig_scatter.update_layout(get_plot_theme()["layout"])
            st.plotly_chart(fig_scatter, use_container_width=True)

    # 4. Interactive No-Till Calculator
    st.markdown("""
    <div class="calc-container">
        <div class="calc-header">⚡ Интерактивный калькулятор эффекта No-Till</div>
        <div class="calc-desc">Рассчитайте потенциал сокращения карбонового следа за счет исключения пахоты и экономии дизельного топлива.</div>
    """, unsafe_allow_html=True)

    c_calc1, c_calc2, c_calc3 = st.columns(3)
    with c_calc1:
        area_ha = st.number_input("Площадь угодий (га)", min_value=10.0, value=1000.0, step=50.0)
    with c_calc2:
        crops_list = sorted(list(df["crop"].unique())) if "crop" in df.columns else ["Все"]
        calc_crop = st.selectbox("Целевая культура", crops_list)
    with c_calc3:
        diesel_saved_per_ha = st.number_input("Экономия ДТ при No-Till (л/га)", min_value=0.0, value=32.0, step=2.0)

    co2_saved_fuel = (area_ha * diesel_saved_per_ha * 2.68) / 1000
    humus_carbon_saved = (area_ha * 210) / 1000

    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f"""
        <div class="calc-result-card accent-emerald">
            <div class="calc-res-title">Сокращение прямых выбросов топлива</div>
            <div class="calc-res-val">-{co2_saved_fuel:,.2f} <span style="font-size: 0.9rem; font-weight: 500;">т CO₂-экв/год</span></div>
            <div style="font-size: 0.8rem; color: #2D6A4F; margin-top: 6px;">Фактор эмиссии ДТ: 2.68 кг CO₂/литр</div>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        st.markdown(f"""
        <div class="calc-result-card accent-blue">
            <div class="calc-res-title">Депонирование углерода в почве</div>
            <div class="calc-res-val">+{humus_carbon_saved:,.2f} <span style="font-size: 0.9rem; font-weight: 500;">т C/год</span></div>
            <div style="font-size: 0.8rem; color: #0E7490; margin-top: 6px;">Сохранение органического вещества почвы</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)