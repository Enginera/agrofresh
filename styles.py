import streamlit as st

def apply_fullscreen_container_styles():
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container {
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        height: 100vh !important;
        max-width: 100% !important;
        background-color: #143c2d !important;
        overflow: hidden !important;
    }
    header[data-testid="stHeader"], div[data-testid="stToolbar"], div[data-testid="stDecoration"], footer {
        display: none !important;
    }
    iframe {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        z-index: 1000 !important;
    }
    </style>
    """, unsafe_allow_html=True)
