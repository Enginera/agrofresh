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
        display: block !important;
    }

    div[data-testid="stHorizontalBlock"] {
        background-color: #143c2d !important;
        padding: 10px 24px !important;
        margin: 0 !important;
        border-bottom: 1px solid #1f5641 !important;
        align-items: center !important;
    }

    div[data-testid="stRadio"] {
        background: transparent !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        background-color: #0d281e !important;
        padding: 4px 6px !important;
        border-radius: 12px !important;
        border: 1px solid #1f543f !important;
        gap: 6px !important;
        display: flex !important;
        width: fit-content !important;
    }

    div[data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }

    div[data-testid="stRadio"] label {
        background: transparent !important;
        color: #a9c8b9 !important;
        padding: 6px 16px !important;
        border-radius: 8px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        border: none !important;
    }
    div[data-testid="stRadio"] label:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
    }
    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] label span {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: inherit !important;
    }

    div[data-testid="stRadio"] label:has(input:checked) {
        background: #2f8c69 !important;
        color: #ffffff !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)
