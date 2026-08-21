import streamlit as st

def render_button_navigation():
    pages = [
        ("🌍 Углеродный след (Эмиссия CO₂)", "Углеродный след (Эмиссия CO₂)"),
        ("📋 Таблица данных и Экспорт", "Таблица данных и Экспорт"),
        ("📖 Справочник агротехнологий", "Справочник агротехнологий")
    ]
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Углеродный след (Эмиссия CO₂)"

    c1, c2, c3 = st.columns(3)
    for col, (label, val) in zip([c1, c2, c3], pages):
        with col:
            is_active = st.session_state.current_page == val
            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"nav_{val}", use_container_width=True, type=btn_type):
                st.session_state.current_page = val
                st.rerun()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    return st.session_state.current_page