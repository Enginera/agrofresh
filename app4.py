import streamlit as st
import pandas as pd
import io
from parser import parse_agro_excel, generate_sample_dataset
from dashboards import (
    render_dashboard_visuals,
    render_fn_menu,
    render_f1,
    render_f2,
    render_f3,
    render_f4,
    render_f5,
    render_f6
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

with st.expander("📂 Загрузка таблицы F2.xlsx / Демо-генерация 1000 полей", expanded=(st.session_state.agro_data is None)):
    col_upload, col_demo = st.columns([3, 1])
    with col_upload:
        uploaded_file = st.file_uploader(
            "Выберите файл Excel (.xlsx, .xls)", 
            type=["xlsx", "xls"],
            help="Таблица с расчетами параметров 6 функций F1-F6"
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
        if st.button("Сгенерировать 1000 полей", use_container_width=True):
            data, stats_df, total = generate_sample_dataset(1000)
            st.session_state.agro_data = data
            st.session_state.agro_stats = stats_df
            st.success("✅ Сгенерировано 1000 полей со статистикой F1-F6!")

current_page, selected_sub_fn, filtered_df = render_sidebar(st.session_state.agro_data)

if filtered_df is not None and not filtered_df.empty:
    if current_page == "🔷 Дашборд":
        render_dashboard_visuals(filtered_df)

    elif current_page == "⏹ Параметры":
        render_top_header("Параметры и описательная статистика полей")
        st.markdown('<div class="section-title">Сводка параметров реестра (1000 полей)</div>', unsafe_allow_html=True)
        st.dataframe(filtered_df.describe().T, use_container_width=True)

    elif current_page == "🔀 Функции F1–F6":
        if selected_sub_fn == "📋 Общий экран функций" or selected_sub_fn is None:
            render_fn_menu()
        elif "F1" in selected_sub_fn:
            render_f1(filtered_df)
        elif "F2" in selected_sub_fn:
            render_f2(filtered_df)
        elif "F3" in selected_sub_fn:
            render_f3(filtered_df)
        elif "F4" in selected_sub_fn:
            render_f4(filtered_df)
        elif "F5" in selected_sub_fn:
            render_f5(filtered_df)
        elif "F6" in selected_sub_fn:
            render_f6(filtered_df)

    elif current_page == "⚪ Сводный анализ":
        render_top_header("Сводный анализ, доверительные интервалы (95% CI) и выгрузка")
        tab_reg, tab_ci, tab_exp = st.tabs(["📋 База полей (1000)", "📐 95% Доверительные интервалы", "💾 Экспорт отчета"])
        
        with tab_reg:
            st.dataframe(filtered_df, use_container_width=True, height=520)
            st.caption(f"Отображено записей: {len(filtered_df)}")
            
        with tab_ci:
            if st.session_state.agro_stats is not None:
                st.dataframe(st.session_state.agro_stats.T, use_container_width=True)
            else:
                st.info("Статистика рассчитывается автоматически при загрузке данных.")
                
        with tab_exp:
            st.markdown("#### Выгрузка итоговых аналитических таблиц")
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                filtered_df.to_excel(writer, sheet_name='F1_F6_Data', index=False)
                if st.session_state.agro_stats is not None:
                    st.session_state.agro_stats.to_excel(writer, sheet_name='Stats_95CI')
            
            st.download_button(
                label="📥 Скачать Excel (Данные F1-F6 + 95% CI)",
                data=buffer.getvalue(),
                file_name="agro_carbon_neutral_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
else:
    st.info("👆 Загрузите Excel-файл или нажмите кнопку «Сгенерировать 1000 полей» для открытия модулей.")