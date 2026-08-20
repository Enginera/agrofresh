import streamlit as st
from styles import apply_custom_styles
from navigation import render_sidebar
from dashboards import render_carbon_dashboard

st.set_page_config(
    page_title="AgroFresh — Carbon & Yield Analytics",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()

page, df = render_sidebar()

if page == "Углеродный след (Эмиссия CO₂)":
    render_carbon_dashboard(df)

elif page == "Таблица данных и Экспорт":
    st.markdown('<div class="main-header">📋 Обработанные агроэкологические данные</div>', unsafe_allow_html=True)
    st.markdown(f"Всего строк в текущей выборке: **{len(df)}**")
    st.dataframe(df)

    csv_data = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 Скачать обработанную таблицу (CSV)",
        data=csv_data,
        file_name="agrofresh_carbon_data_processed.csv",
        mime="text/csv"
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