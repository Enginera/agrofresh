import streamlit as st

def render_sidebar():
    """Боковая панель навигации."""
    st.sidebar.image("https://raw.githubusercontent.com/feathericons/feather/master/icons/activity.svg", width=40)
    st.sidebar.title("AgroFresh Analytics")
    st.sidebar.markdown("---")
    
    selected_page = st.sidebar.radio(
        "Разделы:",
        [
            "📊 Общий Дашборд",
            "🌱 Углеродный след & Выгода",
            "⛅ Климат и Урожайность",
            "📑 Данные и Статистика",
            "📥 Экспорт отчетов"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Платформа агро-экологической оценки • 2026")
    return selected_page
