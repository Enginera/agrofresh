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

# Переключатель темы
with st.sidebar:
    st.image("https://img.icons8.com/color/96/plant-under-sun.png", width=55)
    st.markdown("### **AgroFresh Control**")
    st.caption("Система анализа углеродного следа")
    
    theme_choice = st.radio("🎨 Тема оформления", ["🌙 Тёмная", "☀️ Светлая"], horizontal=True)
    active_theme = "dark" if "🌙" in theme_choice else "light"
    st.markdown("---")

# Применяем стили (быстро, без перегрузки браузера)
apply_custom_styles(theme=active_theme)

with st.sidebar:
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