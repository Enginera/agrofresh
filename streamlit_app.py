import streamlit as st
from styles import apply_custom_styles
from navigation import render_sidebar
from dashboards import render_carbon_dashboard, render_kpi_metrics

st.set_page_config(
    page_title="AgroFresh — Carbon & Storage Monitor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Применение кастомных стилей CSS
apply_custom_styles()

# Получение страницы и отфильтрованных данных
page, df = render_sidebar()

# Роутинг страниц
if page == "Углеродный след (Эмиссия CO₂)":
    render_carbon_dashboard(df)

elif page == "Обзор микроклимата":
    st.markdown('<div class="main-header">🌡️ Мониторинг параметров хранения</div>', unsafe_allow_html=True)
    render_kpi_metrics(df)

elif page == "Таблица данных и Экспорт":
    st.markdown('<div class="main-header">📋 Таблица агроэкологических данных</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    # Кнопка скачивания нормализованной таблицы
    csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 Скачать обработанную таблицу (CSV)",
        data=csv_bytes,
        file_name="agro_carbon_emissions_processed.csv",
        mime="text/csv"
    )

elif page == "Справочник агротехнологий":
    st.markdown('<div class="main-header">📖 Справочник коэффициентов и формул</div>', unsafe_allow_html=True)
    st.markdown("""
    ### 1. Фактор разложения гумуса ($F_{разл}$)
    - **No-Till:** $0.70 - 0.85$ (сниженная минерализация, накопление органики).
    - **Классическая вспашка:** $0.48 - 0.68$ (ускоренная минерализация).

    ### 2. Базовый потенциал секвестрации орудий ($\Delta C_{баз}$):
    - **Плуг:** $525$ кг CO₂/га
    - **Борона:** $400$ кг CO₂/га
    - **Чизель:** $350$ кг CO₂/га

    ### 3. Коэффициенты пестицидов и удобрений:
    - **Гербициды:** $25$ кг CO₂-экв/кг д.в. (доза $1.5$ кг/га)
    - **Фунгициды:** $20$ кг CO₂-экв/кг д.в. (доза $0.5$ кг/га)
    """)