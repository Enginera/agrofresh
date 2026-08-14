import streamlit as st

def render_button_navigation():
    """Строит сетку кнопок. Вместо устаревшего use_container_width=True используется width='stretch'."""
    
    # 1 кнопка — длинная прямоугольная сверху (Обзор)
    if st.button("Обзор 🌱", width='stretch', key="btn_tab_1"):
        st.session_state.page = "Обзор"

    # Ряд 1: кнопки 2, 3, 4 (по 1/3 ширины экрана)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Севооборот 🔄", width='stretch', key="btn_tab_2"):
            st.session_state.page = "Севооборот"
    with col2:
        if st.button("Удобнения и почва 🪱", width='stretch', key="btn_tab_3"):
            st.session_state.page = "Удобрения и почва"
    with col3:
        if st.button("Защита растений 🛡️", width='stretch', key="btn_tab_4"):
            st.session_state.page = "Защита растений"

    # Ряд 2: кнопки 5, 6, 7 (ровно под кнопками 2, 3, 4)
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("Урожайность и качество 🌾", width='stretch', key="btn_tab_5"):
            st.session_state.page = "Урожайность и качество"
    with col5:
        if st.button("Углеродный след ☁️", width='stretch', key="btn_tab_6"):
            st.session_state.page = "Углеродный след"
    with col6:
        if st.button("Принятие решений 💡", width='stretch', key="btn_tab_7"):
            st.session_state.page = "Принятие решений"

    st.markdown("---")
