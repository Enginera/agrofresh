import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from styles import render_top_header

# Цвета из оригинального JS: green, blue, pink, orange
C_GREEN = "#2e6c50"
C_BLUE = "#4d88a6"
C_PINK = "#a33e72"
C_ORANGE = "#e39a3d"
C_GRID = "#edf1ee"
C_MUTED = "#748178"

def fmt(val, precision=2, suffix=""):
    if pd.isna(val) or val is None:
        return "—"
    if precision == 0:
        return f"{val:,.0f}{suffix}".replace(",", " ")
    return f"{val:,.{precision}f}{suffix}".replace(",", " ")

def render_top_f1_f6_block(df: pd.DataFrame):
    """Блок F1-F6 СВЕРХУ со сводными метриками и раскрытием."""
    f1_val = df.get("C_Sequestered", pd.Series([2.14])).mean()
    f2_val = df.get("K_Temp_Soil", pd.Series([1.12])).mean()
    f3_val = df.get("CF_Protection_Season", pd.Series([42.8])).mean()
    f4_val = df.get("F5_Yield_Forecast", pd.Series([4.85])).mean()
    f5_val = df.get("B_Carbon", pd.Series([69.89])).mean()
    f6_val = df.get("F6_1_Efficiency", pd.Series([7.89])).mean()

    st.markdown(f"""
        <div class="fn-top-container">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="eyebrow">Расчётные функции F1–F6</span>
                <span style="font-size:11px; color:#748178; font-weight:700;">Сводка агрегатов по 1000 полей</span>
            </div>
            <div class="fn-grid">
                <div class="fn-card">
                    <div class="fn-badge">F1 · Севооборот</div>
                    <div class="fn-title">Секвестрация Cseq</div>
                    <div class="fn-val">{fmt(f1_val, 2, " т/га")}</div>
                </div>
                <div class="fn-card">
                    <div class="fn-badge">F2 · Удобрения</div>
                    <div class="fn-title">Коэфф. Ktemp</div>
                    <div class="fn-val">{fmt(f2_val, 2)}</div>
                </div>
                <div class="fn-card">
                    <div class="fn-badge">F3 · Защита</div>
                    <div class="fn-title">След Cсезон</div>
                    <div class="fn-val">{fmt(f3_val, 1, " кг/га")}</div>
                </div>
                <div class="fn-card">
                    <div class="fn-badge">F4 · Урожайность</div>
                    <div class="fn-title">Урожай Уфин</div>
                    <div class="fn-val">{fmt(f4_val, 2, " т/га")}</div>
                </div>
                <div class="fn-card">
                    <div class="fn-badge">F5 · Углерод</div>
                    <div class="fn-title">Выгода Bcarbon</div>
                    <div class="fn-val">{fmt(f5_val, 1, " т/га")}</div>
                </div>
                <div class="fn-card">
                    <div class="fn-badge">F6 · Стратегия</div>
                    <div class="fn-title">Эффективность Kэф</div>
                    <div class="fn-val">{fmt(f6_val, 2)}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔍 Развернуть детальные описания и таблицы функций F1–F6"):
        t1, t2, t3, t4, t5, t6 = st.tabs(["F1 Севооборот", "F2 Почва", "F3 Защита", "F4 Урожай", "F5 Углерод", "F6 Стратегия"])
        with t1:
            st.markdown("**F1 — Планирования севооборота**: секвестрация, $C_{net}$, прогнозируемая урожайность и интегральная эффективность.")
        with t2:
            st.markdown("**F2 — Управления удобрениями и обработкой почвы**: параметры почвы, изменение запасов углерода и след операций.")
        with t3:
            st.markdown("**F3 — Мониторинга и управления защитой растений**: уровень заражения растений, интенсивность поражения и сезонный след.")
        with t4:
            st.markdown("**F4 — Управления урожайностью и качеством**: общие потери, урожайность, пожнивные остатки и след на тонну зерна.")
        with t5:
            st.markdown("**F5 — Оценки углеродного следа и учета**: операции, валовые выбросы, материалы и экономический эффект.")
        with t6:
            st.markdown("**F6 — Принятия стратегических решений**: коэффициент нейтральности с учётом стоимости, индекс приоритета PI и риски.")

def render_kpis(df: pd.DataFrame):
    """4 верхние плашки KPI."""
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="kpi-card">
                <small>Средний чистый след</small>
                <div class="value">{fmt(df.get("Net_Carbon_Footprint", pd.Series([0.65])).mean(), 2, " кг")}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="kpi-card">
                <small>Средняя эффективность</small>
                <div class="value">{fmt(df.get("F6_1_Efficiency", pd.Series([7.89])).mean(), 2)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="kpi-card">
                <small>Средняя себестоимость</small>
                <div class="value">{fmt(df.get("C_Total_Costs", pd.Series([52513.5])).mean(), 1, " ₽/га")}</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="kpi-card">
                <small>Расчётных строк полей</small>
                <div class="value">{len(df):,}</div>
            </div>
        """, unsafe_allow_html=True)

def render_charts_grid(df: pd.DataFrame):
    """6 графиков из HTML-шаблона на Plotly."""
    
    # 1-й ряд (2 графика)
    r1_1, r1_2 = st.columns(2)
    with r1_1:
        st.markdown('<div class="chart-title">Удельный след: No-Till vs классическая</div><div class="chart-meta">кг CO₂-экв./т · среднее по культуре</div>', unsafe_allow_html=True)
        crops = ["Горох", "Кукуруза", "Лён", "Озимая пшеница", "Подсолнечник", "Многолетние травы"]
        no_till = [40.0, 17.7, 175.9, 9.4, 51.0, 12.9]
        classic = [37.0, 15.8, 358.0, 10.3, 111.0, 13.7]
        fig1 = go.Figure(data=[
            go.Bar(name='No-Till', x=crops, y=no_till, marker_color=C_BLUE),
            go.Bar(name='Классическая', x=crops, y=classic, marker_color=C_PINK)
        ])
        fig1.update_layout(
            barmode='group', height=270, margin=dict(l=10, r=10, t=15, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with r1_2:
        st.markdown('<div class="chart-title">Структура выбросов по ресурсам</div><div class="chart-meta">горох + кукуруза</div>', unsafe_allow_html=True)
        fig2 = go.Figure(data=[go.Pie(
            labels=["Технологические операции", "Техника", "Логистика"],
            values=[29.9, 64.0, 6.1],
            hole=0.6,
            marker=dict(colors=[C_BLUE, C_PINK, C_ORANGE])
        )])
        fig2.update_layout(
            height=270, margin=dict(l=10, r=10, t=15, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # 2-й ряд (2 графика)
    r2_1, r2_2 = st.columns(2)
    with r2_1:
        st.markdown('<div class="chart-title">Выбросы CO₂ по полевым операциям</div><div class="chart-meta">кг CO₂-экв./га</div>', unsafe_allow_html=True)
        ops = ["Внесение удобрений", "Предпосевная обработка", "Уборка"]
        vals_op = [2250.4, 2247.1, 2250.6]
        fig3 = go.Figure(data=[go.Bar(
            y=ops, x=vals_op, orientation='h', marker_color=C_GREEN
        )])
        fig3.update_layout(
            height=270, margin=dict(l=10, r=10, t=15, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with r2_2:
        st.markdown('<div class="chart-title">Технология и углеродный след</div><div class="chart-meta">сравнение сценариев</div>', unsafe_allow_html=True)
        fig4 = go.Figure(data=[go.Bar(
            x=["No-Till", "Классическая"], y=[29.6, 27.6], marker_color=[C_BLUE, C_PINK]
        )])
        fig4.update_layout(
            height=270, margin=dict(l=10, r=10, t=15, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig4, use_container_width=True)

    # 3-й ряд (Широкий scatter)
    st.markdown('<div class="chart-title">Зависимость углеродного следа от урожайности</div><div class="chart-meta">точки — расчётные поля выборки</div>', unsafe_allow_html=True)
    if "F5_Yield_Forecast" in df.columns and "B_Carbon" in df.columns:
        fig5 = px.scatter(
            df, x="F5_Yield_Forecast", y="B_Carbon",
            color="Risk_1_R" if "Risk_1_R" in df.columns else None,
            labels={"F5_Yield_Forecast": "Урожайность, т/га", "B_Carbon": "Углеродный след / выгода, кг CO₂-экв./т"},
            color_continuous_scale=[C_GREEN, C_BLUE, C_PINK, C_ORANGE]
        )
        fig5.update_layout(
            height=320, margin=dict(l=10, r=10, t=15, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig5, use_container_width=True)

    # 4-й ряд (Широкая интегральная эффективность)
    st.markdown('<div class="chart-title">Интегральная эффективность по культуре</div><div class="chart-meta">среднее значение F6</div>', unsafe_allow_html=True)
    eff_crops = ["Горох", "Кукуруза", "Лён", "Озимая пшеница", "Подсолнечник", "Многолетние травы"]
    eff_vals = [5.63, 10.73, 2.79, 14.66, 3.77, 11.68]
    fig6 = go.Figure(data=[go.Scatter(
        x=eff_crops, y=eff_vals, fill='tozeroy', mode='lines+markers',
        line=dict(color=C_GREEN, width=3), fillcolor='rgba(46,108,80,0.10)'
    )])
    fig6.update_layout(
        height=280, margin=dict(l=10, r=10, t=15, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig6, use_container_width=True)

def render_summary_tables():
    """Две таблицы статусов из HTML-шаблона."""
    st.markdown("### Параметры технологических сценариев")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Культура")
        st.dataframe(pd.DataFrame({
            "Культура": ["Горох", "Кукуруза", "Лён", "Озимая пшеница"],
            "Статус": ["Выбрано", "Выбрано", "Сравнение", "Сравнение"]
        }), use_container_width=True, hide_index=True)
    with c2:
        st.markdown("#### Технология")
        st.dataframe(pd.DataFrame({
            "Технология": ["Классическая", "No-Till"],
            "Статус": ["Выбрано", "Сравнение"]
        }), use_container_width=True, hide_index=True)