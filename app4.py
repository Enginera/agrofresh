import streamlit as st
import pandas as pd
import io
from parser import parse_agro_excel, generate_sample_dataset
from dashboards import (
    render_overview_kpis,
    render_donut_charts,
    render_carbon_vs_economy,
    render_climate_and_yield,
    render_top_fields,
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

st.title("🌾 AgroFresh: Углеродная нейтральность & Эффективность севооборота")

with st.expander("📂 Загрузка Excel-таблицы (или генерация демо-выборки на 1000 полей)", expanded=(st.session_state.agro_data is None)):
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
                st.success(f"✅ Файл успешно обработан! Загружено {res['total_rows']} полей.")
            except Exception as e:
                st.error(f"❌ Ошибка при чтении файла: {e}")
                
    with col_demo:
        st.write("Быстрый старт:")
        if st.button("Сгенерировать 1000 полей"):
            df_demo = generate_sample_dataset(1000)
            st.session_state.agro_data = df_demo
            st.success("✅ Демо-данные (1000 полей) загружены!")

df = st.session_state.agro_data

if df is not None:
    if current_page == "📊 Главный Дашборд & Бублики":
        render_overview_kpis(df)
        st.markdown("---")
        render_donut_charts(df)
        st.markdown("---")
        render_carbon_vs_economy(df)
        render_top_fields(df)
        render_correlation_matrix(df)

    elif current_page == "🌱 Углеродный след & Выгода":
        render_donut_charts(df)
        render_carbon_vs_economy(df)
        render_top_fields(df)

    elif current_page == "⛅ Климат и Урожайность":
        render_climate_and_yield(df)

    elif current_page == "📑 Данные и Статистика":
        st.markdown('<h3 class="eco-header">📑 Очищенный массив данных и доверительные интервалы</h3>', unsafe_allow_html=True)
        tab_data, tab_stats = st.tabs(["📋 База 1000 полей", "📐 Мат. статистика & Погрешности (95% CI)"])
        
        with tab_data:
            st.dataframe(df, use_container_width=True, height=520)
            st.caption(f"Всего обработанных записей: {len(df)}")
            
        with tab_stats:
            if st.session_state.agro_stats is not None:
                st.dataframe(st.session_state.agro_stats.T, use_container_width=True)
            else:
                st.info("Статистика рассчитывается автоматически при парсинге Excel.")

    elif current_page == "📥 Экспорт отчетов":
        st.markdown('<h3 class="eco-header">📥 Экспорт готового отчета в Excel</h3>', unsafe_allow_html=True)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Data_1000_Fields', index=False)
            if st.session_state.agro_stats is not None:
                st.session_state.agro_stats.to_excel(writer, sheet_name='Statistics_95CI')
                
        st.download_button(
            label="💾 Скачать обработанный Excel (Данные + Статистика)",
            data=buffer.getvalue(),
            file_name="agrofresh_full_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("👆 Загрузите файл Excel или нажмите «Сгенерировать 1000 полей» для отображения дашбордов.")
