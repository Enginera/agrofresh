import streamlit as st
from parser import advanced_multi_field_parser

def render_button_navigation():
    """Кнопочная навигация в верхней части страницы (для app4.py)."""
    col1, col2, col3 = st.columns(3)
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Углеродный след (Эмиссия CO₂)"

    with col1:
        if st.button("🌍 Углеродный след", use_container_width=True):
            st.session_state.current_page = "Углеродный след (Эмиссия CO₂)"
    with col2:
        if st.button("📋 Данные и Экспорт", use_container_width=True):
            st.session_state.current_page = "Таблица данных и Экспорт"
    with col3:
        if st.button("📖 Справочник агротехнологий", use_container_width=True):
            st.session_state.current_page = "Справочник агротехнологий"

    st.markdown("---")
    return st.session_state.current_page

def render_sidebar():
    """Боковое меню навигации и загрузки файлов."""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/plant-under-sun.png", width=65)
        st.title("AgroFresh & Carbon")
        st.caption("Система расчета углеродного следа")
        st.markdown("---")

        page = st.radio(
            "Разделы приложения",
            options=[
                "Углеродный след (Эмиссия CO₂)",
                "Таблица данных и Экспорт",
                "Справочник агротехнологий"
            ],
            index=0
        )
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
            selected_crops = st.multiselect(
                "Культура",
                options=all_crops,
                default=all_crops
            )
            if selected_crops:
                df_carbon = df_carbon[df_carbon["crop"].isin(selected_crops)]

        if "technology" in df_carbon.columns:
            all_techs = sorted(list(df_carbon["technology"].unique()))
            selected_tech = st.multiselect(
                "Технология",
                options=all_techs,
                default=all_techs
            )
            if selected_tech:
                df_carbon = df_carbon[df_carbon["technology"].isin(selected_tech)]

        return page, df_carbon