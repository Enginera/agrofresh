import streamlit as st
import pandas as pd
from styles import apply_custom_styles
from parser import advanced_multi_field_parser
from navigation import render_button_navigation
from dashboards import render_carbon_dashboard

st.set_page_config(
    page_title="AgroFresh — Precision Carbon & Yield",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Сайдбар: тема, загрузка и фильтры
with st.sidebar:
    st.image("https://img.icons8.com/color/96/plant-under-sun.png", width=55)
    st.markdown("### **AgroFresh Control**")
    st.caption("Система анализа углеродного следа")
    
    theme_choice = st.radio("🎨 Тема оформления", ["🌙 Тёмная", "☀️ Светлая"], horizontal=True)
    active_theme = "dark" if "🌙" in theme_choice else "light"
    st.markdown("---")

    st.markdown("##### 📁 **Источник данных**")
    uploaded_file = st.file_uploader(
        "Загрузить отчет",
        type=["xlsx", "xls", "csv"],
        help="Поддерживаются сырые отчеты полевых замеров"
    )
    df_carbon = advanced_multi_field_parser(uploaded_file)

    st.markdown("---")
    st.markdown("##### 🔍 **Фильтры выборки**")

    if "crop" in df_carbon.columns:
        all_crops = sorted(list(df_carbon["crop"].unique()))
        selected_crops = st.multiselect("Культуры", options=all_crops, default=all_crops)
        if selected_crops:
            df_carbon = df_carbon[df_carbon["crop"].isin(selected_crops)]

    if "technology" in df_carbon.columns:
        all_techs = sorted(list(df_carbon["technology"].unique()))
        selected_tech = st.multiselect("Агротехнология", options=all_techs, default=all_techs)
        if selected_tech:
            df_carbon = df_carbon[df_carbon["technology"].isin(selected_tech)]

    st.markdown("---")
    st.caption(f"Строк в выборке: **{len(df_carbon):,}**")

# Применяем кастомные стили после выбора темы
apply_custom_styles(theme=active_theme)

# Верхняя навигация
page = render_button_navigation()

if page == "Углеродный след (Эмиссия CO₂)":
    render_carbon_dashboard(df_carbon, theme=active_theme)

elif page == "Таблица данных и Экспорт":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">📊 Data Warehouse</div>
        <div class="hero-title">Нормализованные данные</div>
        <div class="hero-subtitle">Выборка после автоматического парсинга, валидации числовых полей и маппинга справочников.</div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df_carbon, use_container_width=True, height=520)

    csv_data = df_carbon.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 Скачать выборку (CSV)",
        data=csv_data,
        file_name="agrofresh_carbon_export.csv",
        mime="text/csv",
        type="primary"
    )

elif page == "Справочник агротехнологий":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">📖 Reference & Methodology</div>
        <div class="hero-title">Методические коэффициенты и формулы</div>
        <div class="hero-subtitle">Параметры минерализации, секвестрации и удельных выбросов для оценки климатического баланса.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="formula-card">
            <h3>1. Фактор разложения гумуса ($F_{разл}$)</h3>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">Характеризует устойчивость органического вещества почвы к деградации при различных технологиях обработки:</p>
            <ul>
                <li><b>Лён:</b> Классическая — <span class="data-table-badge">0.48</span>, No-Till — <span class="data-table-badge">0.70</span></li>
                <li><b>Озимая пшеница:</b> Классическая — <span class="data-table-badge">0.65</span>, No-Till — <span class="data-table-badge">0.82</span></li>
                <li><b>Горох:</b> Классическая — <span class="data-table-badge">0.55</span>, No-Till — <span class="data-table-badge">0.80</span></li>
                <li><b>Многолетние травы:</b> Классическая — <span class="data-table-badge">0.55</span>, No-Till — <span class="data-table-badge">0.70</span></li>
                <li><b>Кукуруза:</b> Классическая — <span class="data-table-badge">0.65</span>, No-Till — <span class="data-table-badge">0.85</span></li>
                <li><b>Подсолнечник:</b> Классическая — <span class="data-table-badge">0.68</span>, No-Till — <span class="data-table-badge">0.75</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="formula-card">
            <h3>2. Базовый потенциал орудий ($\Delta C_{баз}$)</h3>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">Прямые механические потери углерода почвы за проход орудия:</p>
            <ul>
                <li><b>Плуг:</b> <span class="data-table-badge">525 кг CO₂/га</span></li>
                <li><b>Борона:</b> <span class="data-table-badge">400 кг CO₂/га</span></li>
                <li><b>Чизель:</b> <span class="data-table-badge">350 кг CO₂/га</span></li>
            </ul>
            <h3 style="margin-top: 22px;">3. Нормы и коэффициенты эмиссий СЗР</h3>
            <ul>
                <li><b>Гербициды:</b> Норма 1.5 кг/га, $EF = 25$ кг CO₂-экв/кг д.в.</li>
                <li><b>Фунгициды:</b> Норма 0.5 кг/га, $EF = 20$ кг CO₂-экв/кг д.в.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)