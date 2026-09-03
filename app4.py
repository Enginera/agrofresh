import streamlit as st
import pandas as pd
import io
from parser import parse_agro_excel, generate_sample_dataset
from dashboards import (
    render_overview_kpis, 
    render_carbon_vs_economy, 
    render_climate_and_yield, 
    render_correlation_matrix
)
from navigation import render_sidebar
from styles import apply_custom_styles

st.set_page_config(
    page_title="AgroFresh — Агроэкологическая аналитика",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()
current_page = render_sidebar()

if "agro_data" not in st.session_state:
    st.session_state.agro_data = None
    st.session_state.agro_stats = None

st.title("🌾 AgroFresh: Анализ углеродной нейтральности и эффективности")

with st.expander("📂 Загрузка Excel-таблицы (или использование демо-данных)", expanded=(st.session_state.agro_data is None)):
    col_upload, col_demo = st.columns([3, 1])
    with col_upload:
        uploaded_file = st.file_uploader(
            "Выберите файл Excel (.xlsx, .xls)", 
            type=["xlsx", "xls"],
            help="Загрузите таблицу с расчетами агро-сроков и углеродных показателей"
        )
        if uploaded_file is not None:
            try:
                res = parse_agro_excel(uploaded_file)
                st.session_state.agro_data = res["data"]
                st.session_state.agro_stats = res["stats"]
                st.success(f"✅ Файл успешно обработан! Загружено строк: {res['total_rows']}")
            except Exception as e:
                st.error(f"❌ Ошибка при чтении файла: {e}")
                
    with col_demo:
        st.write("Или протестируйте на демо-выборке:")
        if st.button("Сгенерировать 1000 полей"):
            df_demo = generate_sample_dataset(1000)
            st.session_state.agro_data = df_demo
            st.success("✅ Демо-данные (1000 записей) сформированы!")

df = st.session_state.agro_data

if df is not None:
    if current_page == "📊 Общий Дашборд":
        render_overview_kpis(df)
        st.markdown("---")
        render_carbon_vs_economy(df)
        render_correlation_matrix(df)

    elif current_page == "🌱 Углеродный след & Выгода":
        st.header("Анализ углеродных показателей и нейтральности")
        render_carbon_vs_economy(df)
        
        c1, c2 = st.columns(2)
        with c1:
            if "PI_Priority_Index" in df.columns:
                st.subheader("Распределение индекса приоритета (PI)")
                st.bar_chart(df["PI_Priority_Index"].head(50))
        with c2:
            if "C_Total_Agrosrok" in df.columns:
                st.subheader("Углеродный след агросрока (Ctotal)")
                st.line_chart(df["C_Total_Agrosrok"].head(50))

    elif current_page == "⛅ Климат и Урожайность":
        st.header("Климатические факторы и прогноз урожайности (F5)")
        render_climate_and_yield(df)

    elif current_page == "📑 Данные и Статистика":
        st.header("Очищенные данные и блок статистических погрешностей")
        tab_data, tab_stats = st.tabs(["📋 Таблица данных", "📐 Статистика и Доверительные интервалы"])
        
        with tab_data:
            st.dataframe(df, use_container_width=True, height=500)
            st.caption(f"Всего записей: {len(df)}")
            
        with tab_stats:
            if st.session_state.agro_stats is not None:
                st.dataframe(st.session_state.agro_stats.T, use_container_width=True)
            else:
                st.info("Статистика рассчитывается автоматически при загрузке Excel.")

    elif current_page == "📥 Экспорт отчетов":
        st.header("Экспорт обработанных данных")
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
            if st.session_state.agro_stats is not None:
                st.session_state.agro_stats.to_excel(writer, sheet_name='Statistics')
                
        st.download_button(
            label="💾 Скачать очищенный Excel-файл со статистикой",
            data=buffer.getvalue(),
            file_name="agrofresh_processed_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("👆 Загрузите Excel-файл или нажмите «Сгенерировать 1000 полей» для начала работы.")
