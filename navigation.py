import streamlit as st
from parser import advanced_multi_field_parser

def render_button_navigation():
    """Кнопочная навигация по страницам приложения."""
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