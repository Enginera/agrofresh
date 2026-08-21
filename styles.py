import streamlit as st

def apply_custom_styles(theme="dark"):
    is_dark = theme == "dark"

    if is_dark:
        theme_vars = """
        --browser-scheme: dark;
        --bg-main: #0D1913;
        --sidebar-bg: #13241B;
        --card-bg: #182C22;
        --card-border: #244233;
        --card-accent: #52B788;
        --text-main: #EEF6F1;
        --text-muted: #9BB3A6;
        --text-metric-val: #74C69D;
        --table-border: #244233;
        --input-bg: #182C22;
        --input-border: #2B4D3C;
        --btn-bg: #182C22;
        --btn-text: #EEF6F1;
        --btn-active-bg: #2D6A4F;
        --calc-res-bg: #1F382B;
        """
    else:
        theme_vars = """
        --browser-scheme: light;
        --bg-main: #F4F7F4;
        --sidebar-bg: #FFFFFF;
        --card-bg: #FFFFFF;
        --card-border: #DFE8E2;
        --card-accent: #2E7D32;
        --text-main: #122B1E;
        --text-muted: #5A7565;
        --text-metric-val: #1B5E20;
        --table-border: #DFE8E2;
        --input-bg: #FFFFFF;
        --input-border: #CFDDD3;
        --btn-bg: #FFFFFF;
        --btn-text: #122B1E;
        --btn-active-bg: #2E7D32;
        --calc-res-bg: #F2F7F4;
        """

    css_template = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        __THEME_VARS__
    }

    /* 1. Глобальный сброс и принудительная цветовая схема */
    :root, html, body, .stApp, [data-testid="stAppViewContainer"] {
        color-scheme: var(--browser-scheme) !important;
        background-color: var(--bg-main) !important;
        color: var(--text-main) !important;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    /* 2. Типографика */
    .main-header {
        font-size: clamp(1.35rem, 3.5vw, 2.1rem) !important;
        font-weight: 800;
        color: var(--text-metric-val) !important;
        margin-bottom: 0.2rem;
        line-height: 1.25;
        letter-spacing: -0.3px;
    }
    .sub-header {
        font-size: clamp(0.85rem, 2vw, 1.05rem) !important;
        color: var(--text-muted) !important;
        margin-bottom: 1.2rem;
        line-height: 1.4;
    }

    /* 3. Карточки метрик (KPI) */
    .metric-card {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-left: 4px solid var(--card-accent) !important;
        border-radius: 12px;
        padding: clamp(10px, 2vw, 16px);
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-title {
        font-size: clamp(0.72rem, 1.8vw, 0.82rem);
        color: var(--text-muted) !important;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        line-height: 1.2;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: clamp(1.35rem, 3.2vw, 1.85rem) !important;
        font-weight: 700;
        color: var(--text-metric-val) !important;
        margin-top: 4px;
        letter-spacing: -0.5px;
        line-height: 1.15;
    }

    /* 4. Сайдбар */
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

    /* 5. Кнопки навигации */
    .stButton > button {
        background-color: var(--btn-bg) !important;
        color: var(--btn-text) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 10px !important;
        padding: 8px 14px !important;
        font-size: clamp(0.8rem, 2vw, 0.95rem) !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: var(--btn-active-bg) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--btn-active-bg) !important;
        font-weight: 700 !important;
    }

    /* 6. Поля ввода и мультиселекты */
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] > div {
        background-color: var(--input-bg) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 8px !important;
    }

    /* 7. Графики Plotly (100% ширина, стильные скругления) */
    .stPlotlyChart {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 14px;
        padding: 6px;
        width: 100% !important;
        position: relative;
    }

    /* 🛠 8. КОМПАКТНАЯ И НЕБРОСКАЯ ПАНЕЛЬ МАСШТАБА (MODEBAR) НАД ТЕКСТОМ */
    .modebar-container {
        top: 4px !important;
        right: 8px !important;
        background: transparent !important;
    }
    .modebar-group {
        background: transparent !important;
        padding: 0 !important;
    }
    .modebar-btn {
        opacity: 0.60 !important;
        transform: scale(0.82) !important;
        padding: 2px !important;
        margin: 0 1px !important;
        transition: opacity 0.2s ease, transform 0.2s ease !important;
    }
    .modebar-btn:hover {
        opacity: 1.0 !important;
        transform: scale(0.95) !important;
    }
    .modebar-btn svg {
        width: 14px !important;
        height: 14px !important;
    }

    /* 9. Калькулятор No-Till */
    .calc-card {
        background-color: var(--calc-res-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 16px;
        margin-top: 10px;
    }
    .calc-title {
        font-size: 0.78rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.6px;
        color: var(--text-muted);
    }
    .calc-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: clamp(1.2rem, 3vw, 1.6rem);
        font-weight: 700;
        color: var(--text-main);
        margin-top: 4px;
    }

    /* 10. Таблица и Справочник */
    .stDataFrame {
        border: 1px solid var(--table-border) !important;
        border-radius: 8px;
        background-color: var(--card-bg) !important;
    }
    .formula-box {
        background-color: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 14px;
    }

    /* 📱 11. Мобильная адаптация экрана (до 768px) */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.7rem !important;
            padding-right: 0.7rem !important;
            padding-top: 1rem !important;
        }
        .stButton > button {
            padding: 6px 10px !important;
        }
        .modebar-btn {
            transform: scale(0.75) !important;
            margin: 0 !important;
        }
    }

    footer {visibility: hidden;}
    </style>
    """
    custom_css = css_template.replace("__THEME_VARS__", theme_vars)
    st.markdown(custom_css, unsafe_allow_html=True)