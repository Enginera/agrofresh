import streamlit as st

def apply_fullscreen_container_styles():
    """Убирает дефолтные отступы Streamlit для бесшовного отображения 1-в-1 с HTML"""
    st.markdown("""
    <style>
    .block-container {
        padding: 0rem !important;
        margin: 0rem !important;
        max-width: 100% !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    footer {
        display: none !important;
    }
    iframe {
        width: 100% !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)