import streamlit as st
import pandas as pd
import io
from parser import parse_agro_excel, generate_sample_dataset
from dashboards import (
    render_top_f1_f6_block,
    render_kpis,
    render_charts_grid,
    render_summary_tables
)
from navigation import render_sidebar
from styles import apply_custom_styles, render_top_header

st.set_page_config(
    page_title="Модуль углеродно-нейтрального земледелия",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()

if "agro_data" not in st.session_state:
    st.session_state.agro_data = None
    st.session_state.agro_stats = None

# Верхний спойлер загрузки данных
with st.expander("📂 Загрузка Excel (F2.xlsx) / Быстрый старт (1000 полей)", expanded=(st.session_state.agro_data is None)):
    col_upload, col_demo = st.columns([3, 1])
    with col_upload:
        uploaded_file = st.file_uploader(
            "Выберите файл таблицы (.xlsx, .xls)", 
            type=["xlsx", "xls"],
            help="Таблица с расчетами параметров 6 функций углеродной нейтральности"
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
        st.write("Демо-режим:")
        if st.button("Сгенерировать 1000 полей", use_container_width=True, type="primary"):
            data, stats_df, total = generate_sample_dataset(1000)
            st.session_state.agro_data = data
            st.session_state.agro_stats = stats_df
            st.success("✅ Сгенерировано 1000 полей F1-F6!")

current_page, filtered_df = render_sidebar(st.session_state.agro_data)

if filtered_df is not None and not filtered_df.empty:
    # 1. Верхний заголовок и действия
    render_top_header()

    # 2. БЛОК F1-F6 СВЕРХУ (как требовалось)
    render_top_f1_f6_block(filtered_df)

    # 3. Фильтры-селекторы сценариев
    f_c1, f_c2, f_c3, f_c4 = st.columns([1.3, 1.3, 1, 0.8])
    with f_c1:
        st.selectbox("Культура", ["Горох + Кукуруза", "Все культуры", "Горох", "Кукуруза", "Лён", "Озимая пшеница", "Подсолнечник"])
    with f_c2:
        st.selectbox("Технология", ["Классическая", "Все технологии", "No-Till"])
    with f_c3:
        st.selectbox("Агросезон", ["Текущий расчёт", "Все периоды"])
    with f_c4:
        st.write("&nbsp;")
        if st.button("🔄 Сбросить", use_container_width=True):
            st.rerun()

    # 4. KPI Метрики
    render_kpis(filtered_df)

    # 5. Маршрутизация по вкладкам навигации
    if current_page == "◈ Дашборд":
        render_charts_grid(filtered_df)
        st.markdown("---")
        render_summary_tables()

    elif current_page == "▦ Параметры":
        st.markdown("### Описательная статистика и реестр параметров (1000 полей)")
        st.dataframe(filtered_df.describe().T, use_container_width=True)
        render_summary_tables()

    elif current_page == "⌘ Функции F1–F6":
        st.markdown("### Реестр расчётов по всем функциям F1–F6")
        st.dataframe(filtered_df, use_container_width=True, height=500)

    elif current_page == "◌ Сводный анализ":
        st.markdown("### Доверительные интервалы (95% CI) и экспорт")
        tab1, tab2 = st.tabs(["📐 95% Доверительные интервалы", "💾 Экспорт Excel"])
        with tab1:
            if st.session_state.agro_stats is not None:
                st.dataframe(st.session_state.agro_stats.T, use_container_width=True)
        with tab2:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                filtered_df.to_excel(writer, sheet_name='F1_F6_Data', index=False)
                if st.session_state.agro_stats is not None:
                    st.session_state.agro_stats.to_excel(writer, sheet_name='Stats_95CI')
            st.download_button(
                label="📥 Скачать итоговый отчёт Excel (F1-F6 + 95% CI)",
                data=buffer.getvalue(),
                file_name="agro_carbon_neutral_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
else:
    st.info("👆 Загрузите файл Excel или нажмите кнопку «Сгенерировать 1000 полей» для отображения аналитической панели.")