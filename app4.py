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

if "agro_data" not in st.session_state:
    st.session_state.agro_data = None
    st.session_state.agro_stats = None

st.title("🌾 AgroFresh: Углеродная нейтральность & Эффективность полей")

# Блок загрузки
with st.expander("📂 Загрузка Excel-таблицы (или генерация 1000 полей)", expanded=(st.session_state.agro_data is None)):
    col_upload, col_demo = st.columns([3, 1])
    with col_upload:
        uploaded_file = st.file_uploader(
            "Выберите файл Excel (.xlsx, .xls)", 
            type=["xlsx", "xls"],
            help="Загрузите таблицу с расчетами агро-сроков и углеродных показателей"
        )
        if uploaded_file is not None:
            try:
                data, stats_df, total = parse_agro_excel(uploaded_file)
                st.session_state.agro_data = data
                st.session_state.agro_stats = stats_df
                st.success(f"✅ Файл успешно обработан! Загружено полей: {total}")
            except Exception as e:
                st.error(f"❌ Ошибка при парсинге Excel: {e}")
                
    with col_demo:
        st.write("Быстрый старт:")
        if st.button("Сгенерировать 1000 полей"):
            data, stats_df, total = generate_sample_dataset(1000)
            st.session_state.agro_data = data
            st.session_state.agro_stats = stats_df
            st.success("✅ Сгенерировано 1000 полей со статистикой!")

# Навигация и фильтрация
current_page, filtered_df = render_sidebar(st.session_state.agro_data)

if filtered_df is not None and not filtered_df.empty:
    if current_page == "📊 Главный Дашборд & Бублики":
        render_overview_kpis(filtered_df)
        st.markdown("---")
        render_donut_charts(filtered_df)
        st.markdown("---")
        render_carbon_vs_economy(filtered_df)
        render_top_fields(filtered_df)
        render_correlation_matrix(filtered_df)

    elif current_page == "🌱 Углеродный след & Выгода":
        render_overview_kpis(filtered_df)
        st.markdown("---")
        render_donut_charts(filtered_df)
        render_carbon_vs_economy(filtered_df)
        render_top_fields(filtered_df)

    elif current_page == "⛅ Климат и Урожайность":
        render_climate_and_yield(filtered_df)

    elif current_page == "📑 Данные и Статистика (95% CI)":
        st.markdown('<div class="section-title">📑 Реестр полей и статистическая оценка</div>', unsafe_allow_html=True)
        tab_data, tab_stats = st.tabs(["📋 База полей", "📐 Доверительные интервалы (95% CI) & Погрешности"])
        
        with tab_data:
            st.dataframe(filtered_df, use_container_width=True, height=520)
            st.caption(f"Отображено записей: {len(filtered_df)}")
            
        with tab_stats:
            if st.session_state.agro_stats is not None:
                st.dataframe(st.session_state.agro_stats.T, use_container_width=True)
            else:
                st.info("Статистика рассчитывается автоматически при загрузке данных.")

    elif current_page == "📥 Экспорт отчетов":
        st.markdown('<div class="section-title">📥 Экспорт результатов анализа в Excel</div>', unsafe_allow_html=True)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            filtered_df.to_excel(writer, sheet_name='Data_Fields', index=False)
            if st.session_state.agro_stats is not None:
                st.session_state.agro_stats.to_excel(writer, sheet_name='Stats_95CI')
                
        st.download_button(
            label="💾 Скачать итоговый Excel (Поля + Статистика)",
            data=buffer.getvalue(),
            file_name="agrofresh_report_1000_fields.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("👆 Загрузите Excel-файл или нажмите кнопку «Сгенерировать 1000 полей» для открытия дашборда.")
