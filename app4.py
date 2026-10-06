import streamlit as st
import streamlit.components.v1 as components
from styles import apply_fullscreen_container_styles
from dashboards import UNIFIED_AGRO_HTML

st.set_page_config(
    page_title="Агрономическая Аналитическая Панель",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_fullscreen_container_styles()
components.html(UNIFIED_AGRO_HTML, height=4000, scrolling=False)
