import streamlit as st

def render_top_navigation():
    """Переключатель режимов в верхней плашке Streamlit"""
    c1, c2, _ = st.columns([1.5, 2, 4])
    with c1:
        st.markdown("<b style='font-size:15px; color:#143c2d;'>🌱 Агро-Модуль:</b>", unsafe_allow_html=True)
    with c2:
        mode = st.radio(
            "Режим",
            ["Углеродно-нейтральное (F1–F6)", "Органическое земледелие (ФЗ-280)"],
            horizontal=True,
            label_visibility="collapsed"
        )
    return "carbon" if "Углеродно" in mode else "organic"