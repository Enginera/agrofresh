"""Streamlit entrypoint: fullscreen iframe with the unified agro panel."""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from dashboards import get_unified_html
from styles import apply_fullscreen_container_styles

st.set_page_config(
    page_title="Агрономическая Аналитическая Панель",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_fullscreen_container_styles()
# scrolling=True: скролл внутри iframe (сайдбар модуля остаётся на месте)
components.html(get_unified_html(), height=920, scrolling=True)
