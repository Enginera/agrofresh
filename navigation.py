import streamlit as st

def render_sidebar():
    """Боковая панель в эко-стиле."""
    st.sidebar.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <h2 style="color: #34d399; margin: 0;">🌾 AgroFresh</h2>
            <p style="color: #a7f3d0; font-size: 0.8rem; margin: 0;">Carbon & Yield Intelligence</p>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    selected_page = st.sidebar.radio(
        "Навигация по разделам:",
        [
            "📊 Главный Дашборд & Бублики",
            "🌱 Углеродный след & Выгода",
            "⛅ Климат и Урожайность",
            "📑 Данные и Статистика",
            "📥 Экспорт отчетов"
        ]
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("🟢 Статус: Система активна")
    st.sidebar.caption("Модель: 1000 полей • 2026")
    return selected_page
