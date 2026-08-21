import streamlit as st

def apply_custom_styles(theme="dark"):
    is_dark = theme == "dark"
    
    if is_dark:
        # ТЁМНАЯ ТЕМА (Мягкий глубокий изумрудно-серый, БЕЗ резкого черного)
        theme_vars = """
        --bg-main: #0E1A15;
        --surface: #14241E;
        --surface-elevated: #1B2F27;
        --surface-header-band: #102019;
        --kpi-title-color: #A3CBB5;
        --text-primary: #EEF4F0;
        --text-secondary: #8FA699;
        --border-subtle: #243E33;
        --border-accent: #52B788;
        --brand-primary: #52B788;
        --hero-bg: linear-gradient(135deg, #10241B 0%, #173628 50%, #204B38 100%);
        --hero-text: #FFFFFF;
        --hero-sub: #D0EBE0;
        --calc-bg: #14241E;
        --calc-res-bg: #1B2F27;
        --table-badge-bg: #1E372D;
        --table-badge-text: #74C69D;
        --input-bg: #172C23;
        --tag-bg: #213D30;
        --tag-text: #A8D8BF;
        --tag-border: #2D5442;
        --btn-inactive-bg: #172C23;
        --btn-inactive-text: #D5E5DC;
        --btn-active-bg: #2D6A4F;
        --btn-active-text: #FFFFFF;
        --shadow-card: 0 4px 18px rgba(0, 0, 0, 0.25);
        """
    else:
        # СВЕТЛАЯ ТЕМА (Спокойная, естественная, нейтральная)
        theme_vars = """
        --bg-main: #F4F7F4;
        --surface: #FFFFFF;
        --surface-elevated: #F7F9F7;
        --surface-header-band: #E2ECE5;
        --kpi-title-color: #1E3C2B;
        --text-primary: #12241A;
        --text-secondary: #53685C;
        --border-subtle: #CFDCD3;
        --border-accent: #2D6A4F;
        --brand-primary: #2D6A4F;
        --hero-bg: linear-gradient(135deg, #1B4332 0%, #2D6A4F 60%, #40916C 100%);
        --hero-text: #FFFFFF;
        --hero-sub: #E8F5E9;
        --calc-bg: #FFFFFF;
        --calc-res-bg: #F2F7F4;
        --table-badge-bg: #E5EFE8;
        --table-badge-text: #1E3C2B;
        --input-bg: #FFFFFF;
        --tag-bg: #E3EDE6;
        --tag-text: #1E3C2B;
        --tag-border: #C4D7CB;
        --btn-inactive-bg: #FFFFFF;
        --btn-inactive-text: #1E3C2B;
        --btn-active-bg: #2D6A4F;
        --btn-active-text: #FFFFFF;
        --shadow-card: 0 2px 10px rgba(27, 67, 50, 0.05);
        """

    custom_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {{
        {theme_vars}
    }}

    /* 1. Глобальный фон приложения и шапка Streamlit */
    html, body, [class*="css"], .stApp, 
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"],
    section.main,
    .main .block-container {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
    }}

    [data-testid="stHeader"] {{
        background-color: var(--bg-main) !important;
        border-bottom: 1px solid var(--border-subtle) !important;
    }}
    [data-testid="stHeader"] * {{
        color: var(--text-primary) !important;
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
    [data-testid="stSidebar"] h5,
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
    .stButton > button[data-testid="baseButton-primary"] p,
    .stButton > button[data-testid="baseButton-primary"] span {{
        color: var(--btn-active-text) !important;
        font-weight: 700 !important;
    }}

    /* 4. СПОКОЙНЫЙ НЕЙТРАЛЬНЫЙ МУЛЬТИСЕЛЕКТ (БЕЗ ЧЕРНОГО И КРАСНОГО) */
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    div[data-testid="stMultiSelect"] > div,
    div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {{
        background-color: var(--input-bg) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
    }}

    /* Нейтральные шалфейные теги */
    div[data-baseweb="tag"],
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
        background-color: var(--tag-bg) !important;
        border: 1px solid var(--tag-border) !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
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

    /* Выпадающий список */
    div[data-baseweb="popover"],
    ul[role="listbox"] {{
        background-color: var(--surface) !important;
        border: 1px solid var(--border-subtle) !important;
    }}
    li[role="option"] {{
        background-color: var(--surface) !important;
        color: var(--text-primary) !important;
    }}
    li[role="option"]:hover {{
        background-color: var(--surface-elevated) !important;
    }}

    /* 5. Загрузчик файлов */
    [data-testid="stFileUploader"] section {{
        background-color: var(--input-bg) !important;
        border: 1px dashed var(--border-subtle) !important;
        border-radius: 12px !important;
    }}
    [data-testid="stFileUploader"] section * {{
        color: var(--text-primary) !important;
    }}

    /* 6. Карточки метрик */
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

    /* 7. Баннер, Графики и Таблица */
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
        box-shadow: var(--shadow-card);
    }}

    footer {{visibility: hidden;}}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)