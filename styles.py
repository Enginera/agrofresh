import streamlit as st

def apply_custom_styles(theme="dark"):
    is_dark = theme == "dark"
    
    if is_dark:
        theme_vars = """
        --bg-main: #0E1A14;
        --sidebar-bg: #122019;
        --surface: #15261E;
        --surface-elevated: #1C3328;
        --surface-band: #1F382C;
        --text-primary: #EEF6F1;
        --text-secondary: #97B2A3;
        --text-muted: #6B8576;
        --border-subtle: #244031;
        --border-accent: #52B788;
        --brand-accent: #52B788;
        --brand-mint: #74C69D;
        --hero-bg: linear-gradient(135deg, #112219 0%, #1A3527 50%, #234734 100%);
        --hero-text: #FFFFFF;
        --hero-sub: #D0E8DC;
        --hero-badge-bg: rgba(82, 183, 136, 0.2);
        --hero-badge-text: #74C69D;
        --kpi-title: #A8CEBA;
        --kpi-value: #74C69D;
        --btn-active-bg: #2D6A4F;
        --btn-active-text: #FFFFFF;
        --btn-inactive-bg: #15261E;
        --btn-inactive-text: #EEF6F1;
        --input-bg: #1C3328;
        --input-border: #2B4C3A;
        --tag-bg: #234032;
        --tag-text: #CDE6D8;
        --tag-border: #355E49;
        --shadow-card: 0 4px 16px rgba(0, 0, 0, 0.35);
        """
    else:
        theme_vars = """
        --bg-main: #F5F8F6;
        --sidebar-bg: #FFFFFF;
        --surface: #FFFFFF;
        --surface-elevated: #F7FAF8;
        --surface-band: #EBF3EE;
        --text-primary: #122B1E;
        --text-secondary: #4D6B5A;
        --text-muted: #7E9789;
        --border-subtle: #DFE8E2;
        --border-accent: #2D6A4F;
        --brand-accent: #2D6A4F;
        --brand-mint: #1B4332;
        --hero-bg: linear-gradient(135deg, #1B4332 0%, #2D6A4F 60%, #40916C 100%);
        --hero-text: #FFFFFF;
        --hero-sub: #E2EFE7;
        --hero-badge-bg: rgba(255, 255, 255, 0.2);
        --hero-badge-text: #FFFFFF;
        --kpi-title: #1B4332;
        --kpi-value: #122B1E;
        --btn-active-bg: #2D6A4F;
        --btn-active-text: #FFFFFF;
        --btn-inactive-bg: #FFFFFF;
        --btn-inactive-text: #122B1E;
        --input-bg: #FFFFFF;
        --input-border: #D5E2DA;
        --tag-bg: #EAF2EC;
        --tag-text: #1B4332;
        --tag-border: #C4D9CC;
        --shadow-card: 0 2px 12px rgba(18, 43, 30, 0.05);
        """

    css_template = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        __THEME_VARS__
    }

    /* 1. Глобальный сброс */
    html, body, [class*="css"], .stApp, 
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"],
    section.main,
    .main .block-container {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
    }

    [data-testid="stHeader"] {
        background-color: var(--bg-main) !important;
        border-bottom: 1px solid var(--border-subtle) !important;
    }
    [data-testid="stHeader"] * {
        color: var(--text-primary) !important;
    }

    /* 2. Сайдбар */
    [data-testid="stSidebar"], 
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--border-subtle) !important;
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] div {
        color: var(--text-primary) !important;
    }
    [data-testid="stSidebar"] .stCaption {
        color: var(--text-secondary) !important;
    }

    /* 3. Верхние кнопки навигации */
    .stButton > button {
        background-color: var(--btn-inactive-bg) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        box-shadow: var(--shadow-card) !important;
        padding: 10px 16px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: var(--btn-inactive-text) !important;
        font-weight: 600 !important;
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: var(--btn-active-bg) !important;
        border: 1px solid var(--btn-active-bg) !important;
    }
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span,
    .stButton > button[data-testid="baseButton-primary"] p,
    .stButton > button[data-testid="baseButton-primary"] span {
        color: var(--btn-active-text) !important;
        font-weight: 700 !important;
    }
    .stButton > button:hover {
        border-color: var(--border-accent) !important;
        transform: translateY(-1px);
    }

    /* 4. Инпуты и мультиселекты */
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] > div {
        background-color: var(--input-bg) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="tag"],
    [data-testid="stMultiSelect"] span[data-baseweb="tag"] {
        background-color: var(--tag-bg) !important;
        border: 1px solid var(--tag-border) !important;
        border-radius: 6px !important;
        padding: 2px 8px !important;
    }
    div[data-baseweb="tag"] span,
    [data-testid="stMultiSelect"] span[data-baseweb="tag"] span {
        color: var(--tag-text) !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
    }
    div[data-baseweb="tag"] svg,
    [data-testid="stMultiSelect"] svg {
        fill: var(--text-secondary) !important;
        color: var(--text-secondary) !important;
    }

    /* 5. Карточки метрик (KPI) */
    .kpi-card {
        background: var(--surface);
        border-radius: 16px;
        border: 1px solid var(--border-subtle);
        box-shadow: var(--shadow-card);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: var(--border-accent);
    }
    .kpi-card-header {
        background: var(--surface-band);
        padding: 12px 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid var(--border-subtle);
    }
    .kpi-title {
        font-size: 0.76rem;
        font-weight: 700;
        color: var(--kpi-title) !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .kpi-card-body {
        padding: 18px;
        background: var(--surface);
    }
    .kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.95rem;
        font-weight: 700;
        color: var(--kpi-value) !important;
        letter-spacing: -0.5px;
    }
    .kpi-unit {
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--text-secondary) !important;
        margin-left: 4px;
    }
    .kpi-sub-badge {
        margin-top: 10px;
        display: inline-flex;
        padding: 4px 10px;
        border-radius: 20px;
        background: var(--surface-elevated);
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-subtle);
        font-size: 0.72rem;
        font-weight: 600;
    }

    /* 6. Главный баннер */
    .hero-banner {
        background: var(--hero-bg);
        border-radius: 18px;
        padding: 30px 36px;
        color: var(--hero-text) !important;
        margin-bottom: 24px;
        box-shadow: var(--shadow-card);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--hero-badge-bg);
        color: var(--hero-badge-text);
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        padding: 5px 12px;
        border-radius: 30px;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: var(--hero-text) !important;
        margin: 0 0 8px 0;
    }
    .hero-subtitle {
        font-size: 1.0rem;
        color: var(--hero-sub) !important;
        font-weight: 400;
        max-width: 820px;
        margin: 0;
        line-height: 1.5;
    }

    /* 7. Графики и Калькулятор */
    .stPlotlyChart {
        background: var(--surface);
        border-radius: 16px;
        border: 1px solid var(--border-subtle);
        padding: 10px;
        box-shadow: var(--shadow-card);
    }
    .calc-container {
        background: var(--surface);
        border: 1px solid var(--border-subtle);
        border-radius: 18px;
        padding: 26px;
        box-shadow: var(--shadow-card);
        margin-top: 24px;
    }
    .calc-result-card {
        background: var(--surface-elevated);
        border-radius: 14px;
        padding: 20px;
        border: 1px solid var(--border-subtle);
        height: 100%;
    }
    .calc-res-title {
        font-size: 0.76rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.7px;
        color: var(--text-secondary) !important;
    }
    .calc-res-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.7rem;
        font-weight: 700;
        color: var(--text-primary) !important;
        margin-top: 6px;
    }

    /* 8. Справочник */
    .formula-card {
        background: var(--surface);
        border-radius: 16px;
        border: 1px solid var(--border-subtle);
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: var(--shadow-card);
    }
    .formula-card h3 {
        color: var(--brand-mint);
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 12px;
    }
    .data-table-badge {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        background: var(--surface-band);
        color: var(--text-primary);
        padding: 2px 8px;
        border-radius: 6px;
        border: 1px solid var(--border-subtle);
    }

    /* Загрузчик файлов */
    [data-testid="stFileUploader"] section {
        background-color: var(--surface-elevated) !important;
        border: 1px dashed var(--border-subtle) !important;
        border-radius: 12px !important;
    }
    [data-testid="stFileUploader"] section * {
        color: var(--text-primary) !important;
    }

    footer {visibility: hidden;}
    </style>
    """
    
    custom_css = css_template.replace("__THEME_VARS__", theme_vars)
    st.markdown(custom_css, unsafe_allow_html=True)