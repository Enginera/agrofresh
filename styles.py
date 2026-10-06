import streamlit as st

def apply_fullscreen_container_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

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

    .top-nav-bar {
        background-color: #143c2d;
        padding: 12px 24px 4px 24px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .top-nav-brand {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .top-nav-icon {
        background: #2f8c69;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: inline-grid;
        place-items: center;
        font-size: 18px;
    }
    .top-nav-title {
        color: #ffffff !important;
        font-weight: 750;
        font-size: 16px;
        letter-spacing: 0.02em;
    }

    .top-radio-container {
        background-color: #143c2d;
        padding: 0px 24px 14px 24px;
        border-bottom: 2px solid #1d5942;
    }
    .top-radio-container div[data-testid="stRadio"] {
        background-color: transparent !important;
    }
    .top-radio-container div[data-testid="stRadio"] label {
        color: #dcece5 !important;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        padding: 4px 12px;
        border-radius: 8px;
        transition: 0.2s;
    }
    .top-radio-container div[data-testid="stRadio"] label:hover {
        background: rgba(255, 255, 255, 0.08);
    }
    .top-radio-container div[data-testid="stRadio"] label span {
        color: #dcece5 !important;
    }
    .top-radio-container div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 12px;
        align-items: center;
    }
    .top-radio-container div[data-testid="stRadio"] input:checked + div {
        background-color: #2f8c69 !important;
        border-color: #2f8c69 !important;
    }
    </style>
    """, unsafe_allow_html=True)
