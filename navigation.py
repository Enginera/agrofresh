import streamlit as st

def render_sidebar(mode="carbon", source_name="Текущий файл"):
    with st.sidebar:
        st.markdown("""
        <div style="display: flex; gap: 12px; align-items: center; margin-bottom: 20px;">
            <div style="background: #2f8c69; width: 42px; height: 42px; border-radius: 12px; display: grid; place-items: center; font-size: 22px;">🌱</div>
            <div>
                <b style="font-size: 15px; letter-spacing: 0.02em; display: block; line-height: 1.2;">Агрономическая Аналитика</b>
                <span style="font-size: 12px; color: #a9c8b9;">интеллектуальный модуль</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12); padding: 12px 14px; border-radius: 10px; margin-bottom: 20px;">
            <small style="color: #9db9ad; display: block; font-size: 11px;">АКТИВНЫЙ РЕЖИМ</small>
            <b style="color: #ffffff; font-size: 14px;">{"Углеродно-нейтральное" if mode == "carbon" else "Органическое земледелие (ФЗ-280)"}</b>
        </div>
        """, unsafe_allow_html=True)
        
        if mode == "carbon":
            nav_items = ["Главная", "Статистика по полям", "Расчётные функции F1–F6", "Аналитика выбросов", "Культура и технологии"]
        else:
            nav_items = ["Обзор", "Параметры F1–F5", "Урожай и качество", "Севооборот", "Удобрения", "Соответствие ФЗ-280"]
            
        selected_nav = st.radio("Разделы панели", nav_items, label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown(f"""
        <div style="font-size: 12px; color: #91ada2; line-height: 1.5;">
            <b>Источник:</b> {source_name}<br>
            <i>Данные пересчитываются на лету без перезагрузки страницы.</i>
        </div>
        """, unsafe_allow_html=True)
        
        return selected_nav