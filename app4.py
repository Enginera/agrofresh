import streamlit as st
import pandas as pd

from styles import apply_custom_styles
from parser import advanced_multi_field_parser, get_mock_data
from navigation import render_button_navigation
from dashboards import render_carbon_dashboard

st.set_page_config(
    page_title="AgroFresh — Carbon & Yield Analytics",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()

with st.sidebar:
    st.image("https://img.icons8.com/color/96/plant-under-sun.png", width=65)
    st.title("AgroFresh Control")
    st.caption("Анализ углеродного следа")
    st.markdown("---")

    st.subheader("📁 Источник данных")
    uploaded_file = st.file_uploader(
        "Загрузить Excel файл (.xlsx, .xls)",
        type=["xlsx", "xls", "csv"],
        help="Загрузите таблицу расчетов полевых эмиссий CO2"
    )

    df_carbon = advanced_multi_field_parser(uploaded_file)

    st.subheader("🔍 Фильтры выборки")
    if "crop" in df_carbon.columns:
        all_crops = sorted(list(df_carbon["crop"].unique()))
        selected_crops = st.multiselect("Культура", options=all_crops, default=all_crops)
        if selected_crops:
            df_carbon = df_carbon[df_carbon["crop"].isin(selected_crops)]

    if "technology" in df_carbon.columns:
        all_techs = sorted(list(df_carbon["technology"].unique()))
        selected_tech = st.multiselect("Технология", options=all_techs, default=all_techs)
        if selected_tech:
            df_carbon = df_carbon[df_carbon["technology"].isin(selected_tech)]

page = render_button_navigation()

if page == "Углеродный след (Эмиссия CO₂)":
    render_carbon_dashboard(df_carbon)

elif page == "Таблица данных и Экспорт":
    st.markdown('<div class="main-header">📋 Исходные данные (Excel / CSV)</div>', unsafe_allow_html=True)
    st.markdown(f"Всего строк в выборке: **{len(df_carbon)}**")
    st.dataframe(df_carbon, use_container_width=True)

    csv_data = df_carbon.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 Скачать обработанную выборку (CSV)",
        data=csv_data,
        file_name="agro_carbon_export.csv",
        mime="text/csv"
    )

elif page == "Справочник агротехнологий":
    st.markdown('<div class="main-header">📖 Справочник коэффициентов и формул</div>', unsafe_allow_html=True)
    st.markdown("""
    ### 1. Фактор разложения гумуса ($F_{разл}$)
    Коэффициент устойчивости органического вещества почвы к минерализации:
    - **Лён:** Классическая — `0.48`, No-Till — `0.70`
    - **Озимая пшеница:** Классическая — `0.65`, No-Till — `0.82`
    - **Горох:** Классическая — `0.55`, No-Till — `0.80`
    - **Многолетние травы:** Классическая — `0.55`, No-Till — `0.70`
    - **Кукуруза:** Классическая — `0.65`, No-Till — `0.85`
    - **Подсолнечник:** Классическая — `0.68`, No-Till — `0.75`

    ### 2. Базовый потенциал секвестрации орудий ($\Delta C_{баз}$):
    - **Плуг:** `525` кг CO₂/га
    - **Борона:** `400` кг CO₂/га
    - **Чизель:** `350` кг CO₂/га

    ### 3. Нормы и коэффициенты эмиссий СЗР:
    - **Гербициды:** Доза $1.5$ кг/га, $EF = 25$ кг CO₂-экв/кг д.в.
    - **Фунгициды:** Доза $0.5$ кг/га, $EF = 20$ кг CO₂-экв/кг д.в.
    """)