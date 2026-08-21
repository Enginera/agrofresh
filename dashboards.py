import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def get_plot_theme(theme="dark"):
    is_dark = theme == "dark"
    bg_color = "#15261E" if is_dark else "#FFFFFF"
    text_color = "#EEF6F1" if is_dark else "#122B1E"
    sub_color = "#97B2A3" if is_dark else "#4D6B5A"
    grid_color = "#1F382C" if is_dark else "#EEF4F0"
    line_color = "#244031" if is_dark else "#DFE8E2"

    return {
        "layout": go.Layout(
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font=dict(family="Plus Jakarta Sans, sans-serif", color=text_color, size=12),
            title=dict(font=dict(color=text_color, size=14)),
            margin=dict(l=30, r=20, t=50, b=30),
            xaxis=dict(
                gridcolor=grid_color,
                showline=True,
                linecolor=line_color,
                title=dict(font=dict(color=sub_color)),
                tickfont=dict(size=11, color=sub_color)
            ),
            yaxis=dict(
                gridcolor=grid_color,
                showline=True,
                linecolor=line_color,
                title=dict(font=dict(color=sub_color)),
                tickfont=dict(size=11, color=sub_color)
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=11, color=text_color)
            )
        )
    }

def render_carbon_dashboard(df: pd.DataFrame, theme="dark"):
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">🌱 Carbon Telemetry & AgTech Intelligence</div>
        <div class="hero-title">Углеродный след в растениеводстве</div>
        <div class="hero-subtitle">Мониторинг удельных и валовых эмиссий CO₂-эквивалента по агротехнологиям, полевым операциям и расходу энергоносителей.</div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Метрические карточки (KPI)
    total_co2_ton = (df["co2_emission_kg"].sum() / 1000) if "co2_emission_kg" in df.columns else 0.0
    avg_per_ton = df["co2_per_ton"].mean() if "co2_per_ton" in df.columns else 0.0
    avg_f_razl = df["f_razl"].mean() if "f_razl" in df.columns else 0.0
    avg_yield = df["yield_t_ha"].mean() if "yield_t_ha" in df.columns else 0.0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-card-header">
                <span class="kpi-title">Суммарные выбросы</span>
                <span style="font-size: 1.1rem;">☁️</span>
            </div>
            <div class="kpi-card-body">
                <span class="kpi-value">{total_co2_ton:,.1f}</span>
                <span class="kpi-unit">т CO₂</span>
                <br>
                <span class="kpi-sub-badge">Валовая эмиссия</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-card-header">
                <span class="kpi-title">Удельный след (ср.)</span>
                <span style="font-size: 1.1rem;">🎯</span>
            </div>
            <div class="kpi-card-body">
                <span class="kpi-value">{avg_per_ton:.1f}</span>
                <span class="kpi-unit">кг/т</span>
                <br>
                <span class="kpi-sub-badge">Эмиссия на тонну</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-card-header">
                <span class="kpi-title">Фактор разложения Fразл</span>
                <span style="font-size: 1.1rem;">🍂</span>
            </div>
            <div class="kpi-card-body">
                <span class="kpi-value">{avg_f_razl:.2f}</span>
                <span class="kpi-unit">гумус</span>
                <br>
                <span class="kpi-sub-badge">Индекс минерализации</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-card-header">
                <span class="kpi-title">Ср. Урожайность</span>
                <span style="font-size: 1.1rem;">🌾</span>
            </div>
            <div class="kpi-card-body">
                <span class="kpi-value">{avg_yield:.2f}</span>
                <span class="kpi-unit">т/га</span>
                <br>
                <span class="kpi-sub-badge">Продуктивность угодий</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Гармоничная палитра графиков
    if theme == "dark":
        tech_colors = {"No-Till": "#52B788", "Классическая": "#E07A5F"}
        agro_palette = ["#52B788", "#74C69D", "#E07A5F", "#81B29A", "#F4A261", "#4EA8DE"]
        pie_border = "#15261E"
    else:
        tech_colors = {"No-Till": "#2D6A4F", "Классическая": "#D95D39"}
        agro_palette = ["#2D6A4F", "#52B788", "#74C69D", "#3D5A80", "#E07A5F", "#E9C46A"]
        pie_border = "#FFFFFF"

    # 2. Графики Ряд 1
    g1, g2 = st.columns(2)
    with g1:
        if "technology" in df.columns and "co2_per_ton" in df.columns:
            fig_tech = px.box(
                df, x="crop", y="co2_per_ton", color="technology",
                title="<b>Сравнение следа (кг CO₂/т):</b> No-Till vs Классическая",
                labels={"co2_per_ton": "кг CO₂/т", "crop": "Культура", "technology": "Технология"},
                color_discrete_map=tech_colors
            )
            fig_tech.update_layout(get_plot_theme(theme)["layout"])
            st.plotly_chart(fig_tech, use_container_width=True)

    with g2:
        if "emission_type" in df.columns and "co2_emission_kg" in df.columns:
            df_src = df.groupby("emission_type")["co2_emission_kg"].sum().reset_index()
            fig_donut = px.pie(
                df_src, names="emission_type", values="co2_emission_kg", hole=0.55,
                title="<b>Структура выбросов по энергоносителям и ресурсам</b>",
                color_discrete_sequence=agro_palette
            )
            fig_donut.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color=pie_border, width=2))
            )
            fig_donut.update_layout(get_plot_theme(theme)["layout"])
            st.plotly_chart(fig_donut, use_container_width=True)

    # 3. Графики Ряд 2
    g3, g4 = st.columns(2)
    with g3:
        if "operation" in df.columns and "co2_emission_kg" in df.columns:
            df_ops = df.groupby(["operation", "technology"])["co2_emission_kg"].sum().reset_index()
            fig_ops = px.bar(
                df_ops, x="operation", y="co2_emission_kg", color="technology", barmode="group",
                title="<b>Эмиссия CO₂ по полевым операциям (кг)</b>",
                labels={"co2_emission_kg": "Выбросы CO₂ (кг)", "operation": "Операция", "technology": "Технология"},
                color_discrete_map=tech_colors
            )
            fig_ops.update_layout(get_plot_theme(theme)["layout"])
            st.plotly_chart(fig_ops, use_container_width=True)

    with g4:
        if "yield_t_ha" in df.columns and "co2_emission_kg" in df.columns:
            fig_scatter = px.scatter(
                df, x="yield_t_ha", y="co2_emission_kg", color="crop",
                size="emission_coeff_e", hover_data=["technology", "operation"],
                title="<b>Корреляция:</b> Урожайность vs Выбросы CO₂",
                labels={"yield_t_ha": "Урожайность (т/га)", "co2_emission_kg": "Эмиссия CO₂ (кг/га)", "crop": "Культура"},
                color_discrete_sequence=agro_palette
            )
            fig_scatter.update_layout(get_plot_theme(theme)["layout"])
            st.plotly_chart(fig_scatter, use_container_width=True)

    # 4. Калькулятор No-Till
    st.markdown("""
    <div class="calc-container">
        <div style="font-weight: 700; font-size: 1.25rem; margin-bottom: 4px;">⚡ Интерактивный калькулятор эффекта No-Till</div>
        <div style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 20px;">Расчет потенциала сокращения карбонового следа за счет исключения вспашки и экономии топлива.</div>
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
        <div class="calc-result-card">
            <div class="calc-res-title">Сокращение прямых выбросов топлива</div>
            <div class="calc-res-val">-{co2_saved_fuel:,.2f} <span style="font-size: 0.9rem; font-weight: 500;">т CO₂-экв/год</span></div>
            <div style="font-size: 0.8rem; color: var(--border-accent); margin-top: 8px;">Фактор эмиссии ДТ: 2.68 кг CO₂/л</div>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        st.markdown(f"""
        <div class="calc-result-card">
            <div class="calc-res-title">Депонирование углерода в почве</div>
            <div class="calc-res-val">+{humus_carbon_saved:,.2f} <span style="font-size: 0.9rem; font-weight: 500;">т C/год</span></div>
            <div style="font-size: 0.8rem; color: var(--border-accent); margin-top: 8px;">Сохранение гумуса почвы</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)