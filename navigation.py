import streamlit as st

def render_top_navigation():
    c_brand, c_nav, _ = st.columns([1.8, 4.2, 2])
    
    with c_brand:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; height:100%; padding: 4px 0;">
            <div style="background:#2f8c69; width:34px; height:34px; border-radius:10px; display:grid; place-items:center; font-size:18px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">🌱</div>
            <b style="color:#ffffff; font-size:16px; letter-spacing:0.02em; white-space:nowrap;">Агро-Модуль</b>
        </div>
        """, unsafe_allow_html=True)
        
    with c_nav:
        mode = st.radio(
            "Выбор модуля",
            ["Углеродно-нейтральное (F1–F6)", "Органическое земледелие (ФЗ-280)"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
    return "carbon" if "Углеродно" in mode else "organic"
