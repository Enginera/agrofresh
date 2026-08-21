import streamlit as st

def apply_custom_styles(theme="dark"):
    is_dark = theme == "dark"
    
    # Серо-зеленая палитра вместо черного
    theme_vars = """
    --bg-main: #1F2A24;
    --surface: #27362E;
    --surface-elevated: #314239;
    --surface-header-band: #3A4C41;
    --kpi-title-color: #D3E4DA;
    --text-primary: #EEF4F0;
    --text-secondary: #ADC1B5;
    --border-subtle: #41554A;
    --border-accent: #618A73;
    --brand-primary: #52B788;
    --hero-bg: linear-gradient(135deg, #27362E 0%, #33443A 50%, #405448 100%);
    --hero-text: #FFFFFF;
    --hero-sub: #D5E5DC;
    --calc-bg: #27362E;
    --calc-res-bg: #314239;
    --table-badge-bg: #3D4F44;
    --table-badge-text: #BCE0CD;
    --input-bg: #33443A;
    --tag-bg: #44574C;
    --tag-text: #E2ECE5;
    --tag-border: #586F62;
    --btn-inactive-bg: #33443A;
    --btn-inactive-text: #E2ECE5;
    --btn-active-bg: #436653;
    --btn-active-text: #FFFFFF;
    --shadow-card: 0 4px 14px rgba(0, 0, 0, 0.2);
    """ if is_dark else """
    --bg-main: #F4F7F4;
    --surface: #FFFFFF;
    --surface-elevated: #F6FAF7;
    --surface-header-band: #43554A; /* Грязно-серо-зеленая контрастная шапка */
    --kpi-title-color: #FFFFFF;
    --text-primary: #12241A;
    --text-secondary: #4F6357;
    --border-subtle: #C8D6CD;
    --border-accent: #3F5E4D;
    --brand-primary: #335341;
    --hero-bg: linear-gradient(135deg, #2D3E34 0%, #3D5246 60%, #4F6859 100%);
    --hero-text: #FFFFFF;
    --hero-sub: #E2ECE5;
    --calc-bg: #FFFFFF;
    --calc-res-bg: #F2F7F4;
    --table-badge-bg: #E1EDE5;
    --table-badge-text: #223B2D;
    --input-bg: #384A3F;          /* Грязно-серо-зеленый мультиселект */
    --tag-bg: #4D6355;            /* Грязно-серо-зеленые плашки */
    --tag-text: #F0F6F2;
    --tag-border: #627C6C;
    --btn-inactive-bg: #FFFFFF;
    --btn-inactive-text: #223B2D;
    --btn-active-bg: #384F41;
    --btn-active-text: #FFFFFF;
    --shadow-card: 0 2px 10px rgba(45, 62, 52, 0.08);
    """

    custom_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {{
        {theme_vars}
    }}

    /* 1. Глобальный фон и шапка */
    html, body, [class*="css"], .stApp, 
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"],
    section.main,
    .main .block-container {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
    }}

    [data-testid="stHeader"] {{
        background-color: var(--bg-main) !important;
        border-bottom: 1px solid var(--border-subtle) !important;
    }}

    /* 2. Сайдбар */
    [data-testid="stSidebar"], 
    [data-testid="stSidebarContent"] {{
        background-color: var(--surface) !important;
        border-right: 1px solid var(--border-subtle) !important;
    }}
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] div {{
        color: var(--text-primary) !important;
    }}
    [data-testid="stSidebar"] .stCaption, 
    [data-testid="stSidebar"] small {{
        color: var(--text-secondary) !important;
    }}

    /* 3. Кнопки навигации */
    .stButton > button {{
        background-color: var(--btn-inactive-bg) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        box-shadow: var(--shadow-card) !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {{
        color: var(--btn-inactive-text) !important;
        font-weight: 600 !important;
    }}
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {{
        background-color: var(--btn-active-bg) !important;
        border: 1px solid var(--btn-active-bg) !important;
    }}
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span,
    .stButton > button[data-testid="baseButton-primary"] p {{
        color: var(--btn-active-text) !important;
        font-weight: 700 !important;
    }}

    /* 4. ГРЯЗНО-СЕРО-ЗЕЛЕНЫЙ МУЛЬТИСЕЛЕКТ */
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    div[data-testid="stMultiSelect"] > div,
    div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {{
        background-color: var(--input-bg) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
    }}

    /* Плашки внутри мультиселекта */
    div[data-baseweb="tag"],
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
        background-color: var(--tag-bg) !important;
        border: 1px solid var(--tag-border) !important;
        border-radius: 6px !important;
        padding: 2px 8px !important;
    }}
    div[data-baseweb="tag"] span,
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] span {{
        color: var(--tag-text) !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
    }}
    div[data-baseweb="tag"] svg,
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] svg {{
        fill: var(--tag-text) !important;
        color: var(--tag-text) !important;
    }}

    div[data-baseweb="popover"],
    ul[role="listbox"] {{
        background-color: var(--surface-elevated) !important;
        border: 1px solid var(--border-subtle) !important;
    }}
    li[role="option"] {{
        background-color: var(--surface-elevated) !important;
        color: var(--text-primary) !important;
    }}

    /* 5. Карточки метрик */
    .kpi-card {{
        background: var(--surface);
        border-radius: 14px;
        border: 1px solid var(--border-subtle);
        box-shadow: var(--shadow-card);
        overflow: hidden;
    }}
    .kpi-card-header {{
        background: var(--surface-header-band);
        padding: 12px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid var(--border-subtle);
    }}
    .kpi-title {{
        font-size: 0.78rem;
        font-weight: 700;
        color: var(--kpi-title-color) !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}
    .kpi-card-body {{
        padding: 16px;
        background: var(--surface);
    }}
    .kpi-value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.85rem;
        font-weight: 700;
        color: var(--text-primary) !important;
    }}
    .kpi-unit {{
        font-size: 0.88rem;
        color: var(--text-secondary) !important;
    }}
    .kpi-sub-badge {{
        margin-top: 8px;
        display: inline-flex;
        padding: 3px 8px;
        border-radius: 6px;
        background: var(--surface-elevated);
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-subtle);
        font-size: 0.73rem;
        font-weight: 600;
    }}

    /* 6. Баннер, Графики и Таблица */
    .hero-banner {{
        background: var(--hero-bg);
        border-radius: 16px;
        padding: 28px 32px;
        color: var(--hero-text) !important;
        margin-bottom: 24px;
        box-shadow: var(--shadow-card);
    }}
    .stPlotlyChart {{
        background: var(--surface);
        border-radius: 14px;
        border: 1px solid var(--border-subtle);
        padding: 10px;
        box-shadow: var(--shadow-card);
    }}
    .stDataFrame {{
        background: var(--surface);
        border-radius: 12px;
        border: 1px solid var(--border-subtle);
        padding: 4px;
    }}
    footer {{visibility: hidden;}}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)