import streamlit as st

def apply_custom_styles(theme="dark"):
    is_dark = theme == "dark"
    
    if is_dark:
        # === 🌙 ТЁМНАЯ ТЕМА ===
        theme_vars = """
        --bg-main: #142019;
        --sidebar-bg: #1B2921;
        --surface: #203027;
        --surface-elevated: #283C31;
        --surface-header-band: #2D4438;
        --kpi-title-color: #BEE3CD;
        --text-primary: #EEF6F1;
        --text-secondary: #9DB4A7;
        --border-subtle: #385042;
        --border-accent: #52B788;
        --brand-primary: #52B788;
        --hero-bg: linear-gradient(135deg, #1B2921 0%, #24382D 50%, #2F4A3B 100%);
        --hero-text: #FFFFFF;
        --hero-sub: #D5EBDD;
        --hero-badge-bg: rgba(255, 255, 255, 0.15);
        --hero-badge-text: #BEE3CD;
        --calc-bg: #203027;
        --calc-res-bg: #283C31;
        --table-badge-bg: #2D4438;
        --table-badge-text: #BEE3CD;
        --input-bg: #283C31;
        --tag-bg: #354E40;
        --tag-text: #EEF6F1;
        --tag-border: #4D6D5B;
        --btn-inactive-bg: #283C31;
        --btn-inactive-text: #EEF6F1;
        --btn-active-bg: #3B614B;
        --btn-active-text: #FFFFFF;
        --upload-bg: #283C31;
        --upload-btn-bg: #354E40;
        --shadow-card: 0 4px 14px rgba(0, 0, 0, 0.3);
        """
    else:
        # === ☀️ СВЕТЛАЯ ТЕМА (Мягкая, светлая, без черных пятен) ===
        theme_vars = """
        --bg-main: #F4F7F4;
        --sidebar-bg: #FFFFFF;
        --surface: #FFFFFF;
        --surface-elevated: #F6F9F7;
        --surface-header-band: #EBF2ED;      /* Светлая шалфейная плашка в шапках метрик */
        --kpi-title-color: #1B3F2B;          /* Четкий хвойный текст */
        --text-primary: #12281C;
        --text-secondary: #526B5C;
        --border-subtle: #D5E2D9;
        --border-accent: #2D6A4F;
        --brand-primary: #2D6A4F;
        --hero-bg: linear-gradient(135deg, #E2EFE7 0%, #D4E8DC 50%, #C7E0D1 100%); /* Светлый баннер */
        --hero-text: #0E291C;                /* Темный текст на светлом баннере */
        --hero-sub: #2B4E3A;
        --hero-badge-bg: #C7E2D0;
        --hero-badge-text: #0E291C;
        --calc-bg: #FFFFFF;
        --calc-res-bg: #F4F8F5;
        --table-badge-bg: #E3EDE6;
        --table-badge-text: #1B3F2B;
        --input-bg: #FFFFFF;                 /* Белый чистый фон селектов */
        --tag-bg: #E2EDE6;                   /* Светлые мягкие плашки культур */
        --tag-text: #1B3F2B;
        --tag-border: #BCD1C3;
        --btn-inactive-bg: #FFFFFF;
        --btn-inactive-text: #1E3B2C;
        --btn-active-bg: #2D6A4F;            /* Аккуратная акцентная кнопка */
        --btn-active-text: #FFFFFF;
        --upload-bg: #F8FAF8;
        --upload-btn-bg: #EAEFEA;
        --shadow-card: 0 2px 10px rgba(45, 62, 52, 0.05);
        """

    css_template = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        __THEME_VARS__
    }

    /* 1. Глобальный фон и шапка */
    html, body, [class*="css"], .stApp, 
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"],
    section.main,
    .main .block-container {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
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
    [data-testid="stSidebar"] > div:first-child,
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
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] div {
        color: var(--text-primary) !important;
    }
    [data-testid="stSidebar"] .stCaption, 
    [data-testid="stSidebar"] small {
        color: var(--text-secondary) !important;
    }

    /* 3. Кнопки верхней навигации */
    .stButton > button {
        background-color: var(--btn-inactive-bg) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        box-shadow: var(--shadow-card) !important;
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

    /* 4. Мультиселект (фильтры выборки) */
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    div[data-testid="stMultiSelect"] > div,
    div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
        background-color: var(--input-bg) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="tag"],
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
        background-color: var(--tag-bg) !important;
        border: 1px solid var(--tag-border) !important;
        border-radius: 6px !important;
        padding: 3px 8px !important;
    }
    div[data-baseweb="tag"] span,
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] span {
        color: var(--tag-text) !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    div[data-baseweb="tag"] svg,
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] svg {
        fill: var(--tag-text) !important;
        color: var(--tag-text) !important;
    }

    /* 5. Загрузчик файлов */
    [data-testid="stFileUploader"] section {
        background-color: var(--upload-bg) !important;
        border: 1px dashed var(--border-subtle) !important;
        border-radius: 12px !important;
    }
    [data-testid="stFileUploader"] section * {
        color: var(--text-primary) !important;
    }
    [data-testid="stFileUploader"] section button {
        background-color: var(--upload-btn-bg) !important;
        border: 1px solid var(--border-subtle) !important;
    }
    [data-testid="stFileUploader"] section button * {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }

    /* 6. Карточки метрик (KPI) */
    .kpi-card {
        background: var(--surface);
        border-radius: 14px;
        border: 1px solid var(--border-subtle);
        box-shadow: var(--shadow-card);
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    .kpi-card-header {
        background: var(--surface-header-band);
        padding: 12px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid var(--border-subtle);
    }
    .kpi-title {
        font-size: 0.78rem;
        font-weight: 700;
        color: var(--kpi-title-color) !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .kpi-card-body {
        padding: 16px;
        background: var(--surface);
    }
    .kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.85rem;
        font-weight: 700;
        color: var(--text-primary) !important;
    }
    .kpi-unit {
        font-size: 0.88rem;
        color: var(--text-secondary) !important;
    }
    .kpi-sub-badge {
        margin-top: 8px;
        display: inline-flex;
        padding: 3px 8px;
        border-radius: 6px;
        background: var(--surface-elevated);
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-subtle);
        font-size: 0.73rem;
        font-weight: 600;
    }

    /* 7. Главный баннер */
    .hero-banner {
        background: var(--hero-bg);
        border-radius: 16px;
        padding: 28px 32px;
        color: var(--hero-text) !important;
        margin-bottom: 24px;
        box-shadow: var(--shadow-card);
        border: 1px solid var(--border-subtle);
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
        padding: 4px 12px;
        border-radius: 30px;
        margin-bottom: 10px;
    }
    .hero-title {
        font-size: 2.0rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: var(--hero-text) !important;
        margin: 0 0 6px 0;
    }
    .hero-subtitle {
        font-size: 0.98rem;
        color: var(--hero-sub) !important;
        font-weight: 500;
        max-width: 800px;
        margin: 0;
        line-height: 1.5;
    }

    /* 8. Графики и Калькулятор */
    .stPlotlyChart {
        background: var(--surface);
        border-radius: 14px;
        border: 1px solid var(--border-subtle);
        padding: 10px;
        box-shadow: var(--shadow-card);
    }
    .calc-container {
        background: var(--calc-bg);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 24px;
        box-shadow: var(--shadow-card);
        margin-top: 24px;
    }
    .calc-result-card {
        background: var(--calc-res-bg);
        border-radius: 12px;
        padding: 18px;
        border: 1px solid var(--border-subtle);
    }
    .calc-res-title {
        font-size: 0.78rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.6px;
        color: var(--text-secondary) !important;
    }
    .calc-res-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-primary) !important;
    }

    /* 9. Справочник формул */
    .formula-card {
        background: var(--surface);
        border-radius: 14px;
        border: 1px solid var(--border-subtle);
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: var(--shadow-card);
    }
    .formula-card h3 {
        color: var(--brand-primary);
        font-size: 1.1rem;
        font-weight: 700;
        margin-top: 0;
    }
    .data-table-badge {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        background: var(--table-badge-bg);
        color: var(--table-badge-text);
        padding: 2px 7px;
        border-radius: 6px;
        border: 1px solid var(--border-subtle);
    }

    footer {visibility: hidden;}
    </style>
    """
    
    custom_css = css_template.replace("__THEME_VARS__", theme_vars)
    st.markdown(custom_css, unsafe_allow_html=True)