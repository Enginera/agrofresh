import streamlit as st
import pandas as pd
from styles import apply_custom_styles
from parser import advanced_multi_field_parser
from navigation import render_button_navigation
from dashboards import render_carbon_dashboard

st.set_page_config(
    page_title="AgroFresh — Carbon & Yield Analytics",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Значки для культур и технологий
CROP_ICONS = {
    "Кукуруза": "🔵 Кукуруза",
    "Горох": "🟢 Горох",
    "Озимая пшеница": "🟠 Озимая пшеница",
    "Лён": "🟤 Лён",
    "Многолетние травы": "🔷 Многолетние травы",
    "Подсолнечник": "🟣 Подсолнечник"
}
ICON_TO_CROP = {v: k for k, v in CROP_ICONS.items()}

TECH_ICONS = {
    "No-Till": "🌱 No-Till",
    "Классическая": "🚜 Классическая"
}
ICON_TO_TECH = {v: k for k, v in TECH_ICONS.items()}

# Сайдбар: тема, загрузка и цветные фильтры
with st.sidebar:
    st.image("https://img.icons8.com/color/96/plant-under-sun.png", width=60)
    st.markdown("### **AgroFresh Control**")
    st.caption("Система расчета углеродного следа")
    
    theme_choice = st.radio("🎨 Тема оформления", ["🌙 Тёмная", "☀️ Светлая"], horizontal=True)
    active_theme = "dark" if "🌙" in theme_choice else "light"
    st.markdown("---")

    st.markdown("##### 📁 **Источник данных**")
    uploaded_file = st.file_uploader(
        "Загрузить файл замеров",
        type=["xlsx", "xls", "csv"],
        help="Загрузите таблицу расчетов полевых эмиссий CO2"
    )
    df_carbon = advanced_multi_field_parser(uploaded_file)

    st.markdown("---")
    st.markdown("##### 🔍 **Фильтры выборки**")

    # Фильтр по культурам с цветными маркерами графика
    if "crop" in df_carbon.columns:
        all_crops_raw = sorted(list(df_carbon["crop"].unique()))
        crop_options = [CROP_ICONS.get(c, c) for c in all_crops_raw]
        selected_crop_icons = st.multiselect(
            "Культуры (цвета графика):",
            options=crop_options,
            default=crop_options
        )
        selected_crops = [ICON_TO_CROP.get(icon, icon) for icon in selected_crop_icons]
        if selected_crops:
            df_carbon = df_carbon[df_carbon["crop"].isin(selected_crops)]

    # Фильтр по технологиям
    if "technology" in df_carbon.columns:
        all_techs_raw = sorted(list(df_carbon["technology"].unique()))
        tech_options = [TECH_ICONS.get(t, t) for t in all_techs_raw]
        selected_tech_icons = st.multiselect(
            "Агротехнология:",
            options=tech_options,
            default=tech_options
        )
        selected_techs = [ICON_TO_TECH.get(icon, icon) for icon in selected_tech_icons]
        if selected_techs:
            df_carbon = df_carbon[df_carbon["technology"].isin(selected_techs)]

    st.markdown("---")
    st.caption(f"Строк в выборке: **{len(df_carbon):,}**")

# Применяем стили
apply_custom_styles(theme=active_theme)

# Верхняя навигация
page = render_button_navigation()

if page == "Углеродный след (Эмиссия CO₂)":
    render_carbon_dashboard(df_carbon, theme=active_theme)

elif page == "Таблица данных и Экспорт":
    st.markdown('<div class="main-header">📋 Исходные данные (Excel / CSV)</div>', unsafe_allow_html=True)
    st.markdown(f"Всего строк в выборке: **{len(df_carbon)}**")
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
    st.markdown('<div class="main-header">📖 Справочник коэффициентов и формул</div>', unsafe_allow_html=True)
    st.markdown(r"""
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