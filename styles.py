import streamlit as st

def apply_custom_styles(theme="dark"):
    is_dark = theme == "dark"

    if is_dark:
        theme_vars = """
        --browser-scheme: dark;
        --bg-main: #0E1A14;
        --sidebar-bg: #14241C;
        --card-bg: #1A2E24;
        --card-border: #244233;
        --card-accent: #52B788;
        --text-main: #EEF6F1;
        --text-muted: #9BB3A6;
        --text-metric-val: #74C69D;
        --table-border: #244233;
        --btn-bg: #1A2E24;
        --btn-text: #EEF6F1;
        --btn-active-bg: #2D6A4F;
        --input-bg: #1A2E24;
        --input-border: #2B4D3C;
        """
    else:
        theme_vars = """
        --browser-scheme: light;
        --bg-main: #F4F7F4;
        --sidebar-bg: #F4F9F4;
        --card-bg: #FFFFFF;
        --card-border: #E0E7E1;
        --card-accent: #2E7D32;
        --text-main: #1B3826;
        --text-muted: #616161;
        --text-metric-val: #1B5E20;
        --table-border: #E0E0E0;
        --btn-bg: #FFFFFF;
        --btn-text: #1B3826;
        --btn-active-bg: #2E7D32;
        --input-bg: #FFFFFF;
        --input-border: #D0DCD4;
        """

    css_template = """
    <style>
    :root {
        __THEME_VARS__
    }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        color-scheme: var(--browser-scheme) !important;
        background-color: var(--bg-main) !important;
        color: var(--text-main) !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: var(--text-metric-val) !important;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: var(--text-muted) !important;
        margin-bottom: 1.5rem;
    }

    .metric-card {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-left: 5px solid var(--card-accent) !important;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.04);
    }
    .metric-title {
        font-size: 0.85rem;
        color: var(--text-muted) !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-metric-val) !important;
        margin-top: 4px;
    }

    [data-testid="stSidebar"], 
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"],
    [data-testid="stSidebar"] > div:first-child {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--card-border) !important;
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--text-main) !important;
    }

    .stButton > button {
        background-color: var(--btn-bg) !important;
        color: var(--btn-text) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 6px !important;
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: var(--btn-active-bg) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--btn-active-bg) !important;
    }

    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] > div {
        background-color: var(--input-bg) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 6px !important;
    }

    .stDataFrame {
        border: 1px solid var(--table-border) !important;
        border-radius: 6px;
    }
    .stPlotlyChart {
        border-radius: 8px;
    }

    footer {visibility: hidden;}
    </style>
    """
    custom_css = css_template.replace("__THEME_VARS__", theme_vars)
    st.markdown(custom_css, unsafe_allow_html=True)