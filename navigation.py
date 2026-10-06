import streamlit as st

def render_top_navigation():
    st.markdown("""
    <div class="top-nav-bar">
        <div class="top-nav-brand">
            <span class="top-nav-icon">🌱</span>
            <span class="top-nav-title">Агро-Модуль:</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="top-radio-container">', unsafe_allow_html=True)
        mode = st.radio(
            "Выбор модуля",
            ["Углеродно-нейтральное (F1–F6)", "Органическое земледелие (ФЗ-280)"],
            horizontal=True,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    return "carbon" if "Углеродно" in mode else "organic"
