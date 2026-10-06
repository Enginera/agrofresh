import streamlit as st
import streamlit.components.v1 as components
from styles import apply_fullscreen_container_styles
from navigation import render_top_navigation
from dashboards import CARBON_HTML, ORGANIC_HTML

st.set_page_config(
    page_title="Агрономическая Аналитическая Панель",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Применяем полноэкранный бесшовный стиль
apply_fullscreen_container_styles()

# Переключатель модулей
mode = render_top_navigation()

# Отрисовываем 1-в-1 оригинальный HTML-референс
if mode == "carbon":
    components.html(CARBON_HTML, height=3600, scrolling=False)
else:
    components.html(ORGANIC_HTML, height=2800, scrolling=False)