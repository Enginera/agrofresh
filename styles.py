import streamlit as st

def apply_custom_styles(theme="dark"):
    is_dark = theme == "dark"
    
    if is_dark:
        theme_vars = """
        --bg-main: #18241E;
        --sidebar-bg: #1F2D26;
        --surface: #24332B;
        --surface-elevated: #2B3D34;
        --surface-header-band: #33443A;
        --kpi-title-color: #D3E4DA;
        --text-primary: #EEF4F0;
        --text-secondary: #A3B8AD;
        --border-subtle: #3A4E42;
        --border-accent: #52B788;
        --brand-primary: #52B788;
        --hero-bg: linear-gradient(135deg, #1F2D26 0%, #2A3B32 50%, #364A3F 100%);
        --hero-text: #FFFFFF;
        --hero-sub: #D5E5DC;
        --calc-bg: #24332B;
        --calc-res-bg: #2B3D34;
        --table-badge-bg: #33443A;
        --table-badge-text: #BCE0CD;
        --input-bg: #2B3D34;
        --tag-bg: #3B5245;
        --tag-text: #EEF4F0;
        --tag-border: #4D6959;
        --btn-inactive-bg: #2B3D34;
        --btn-inactive-text: #EEF4F0;
        --btn-active-bg: #385645;
        --btn-active-text: #FFFFFF;
        --shadow-card: 0 4px 14px rgba(0, 0, 0, 0.25);
        """
    else:
        theme_vars = """
        --bg-main: #F4F7F4;
        --sidebar-bg: #FFFFFF;       /* ЧИСТЫЙ СВЕТЛЫЙ САЙДБАР */
        --surface: #FFFFFF;
        --surface-elevated: #F6FAF7;
        --surface-header-band: #3A4D41;
        --kpi-title-color: #FFFFFF;
        --text-primary: #12241A;
        --text-secondary: #4F6357;
        --border-subtle: #CFDCD3;
        --border-accent: #3A4D41;
        --brand-primary: #3A4D41;
        --hero-bg: linear-gradient(135deg, #2A3C32 0%, #3A4F43 60%, #4D6456 100%);
        --hero-text: #FFFFFF;
        --hero-sub: #E2ECE5;
        --calc-bg: #FFFFFF;
        --calc-res-bg: #F2F7F4;
        --table-badge-bg: #E1EDE5;
        --table-badge-text: #223B2D;
        --input-bg: #F2F6F3;        /* Светлое поле выбора */
        --tag-bg: #44594C;          /* Аккуратный серо-зеленый тег */
        --tag-text: #FFFFFF;        /* Белый четкий текст */
        --tag-border: #566F60;
        --btn-inactive-bg: #FFFFFF;
        --btn-inactive-text: #223B2D;
        --btn-active-bg: #3A4D41;
        --btn-active-text: #FFFFFF;
        --shadow-card: 0 2px 10px rgba(45, 62, 52, 0.06);
        """

    custom_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {{
        {theme_vars}
    }}

    /* 1. Глобальный фон приложения и шапка */
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
    [data-testid="stHeader"] * {{
        color: var(--text-primary) !important;
    }}

    /* 2. САЙДБАР (БЕЗ ЧЕРНОГО ФОНА В СВЕТЛОЙ ТЕМЕ) */
    [data-testid="stSidebar"], 
    [data-testid="stSidebar"] > div:first-child,
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"] {{
        background-color: var(--sidebar-bg) !important;
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

    /* 3. Кнопки верхней навигации */
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

    /* 4. МУЛЬТИСЕЛЕКТ */
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    div[data-testid="stMultiSelect"] > div,
    div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {{
        background-color: var(--input-bg) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
    }}

    /* Плашки мультиселекта (Горох, Кукуруза...) */
    div[data-baseweb="tag"],
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
        background-color: var(--tag-bg) !important;
        border: 1px solid var(--tag-border) !important;
        border-radius: 6px !important;
        padding: 3px 8px !important;
    }}
    div[data-baseweb="tag"] span,
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] span {{
        color: var(--tag-text) !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }}
    div[data-baseweb="tag"] svg,
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] svg {{
        fill: var(--tag-text) !important;
        color: var(--tag-text) !important;
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

    /* 6. Двухтоновые KPI карточки */
    .kpi-card {{
        background: var(--surface);
        border-radius: 14px;
        border: 1px solid var(--border-subtle);
        box-shadow: var(--shadow-card);
        overflow: hidden;
        display: flex;
        flex-direction: column;
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
        padding: