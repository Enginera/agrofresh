import streamlit as st


def apply_fullscreen_container_styles():
    st.markdown(
        """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container {
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        height: 100vh !important;
        max-width: 100% !important;
        background-color: #0a0e0c !important;
        overflow: hidden !important;
    }
    header[data-testid="stHeader"],
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"],
    footer,
    #MainMenu {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        visibility: hidden !important;
    }
    /* один внешний iframe на весь экран, без зелёной полосы сверху */
    [data-testid="stAppViewContainer"] iframe {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        z-index: 1000 !important;
        background: #0a0e0c !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
