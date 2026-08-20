import streamlit as st
from parser import parse_carbon_excel

def render_sidebar():
    """Отрисовка боковой панели с загрузчиком файлов и меню."""
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
        df_carbon = parse_carbon_excel(uploaded_file)

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