import streamlit as st

def apply_custom_styles(theme="dark"):
    is_dark = theme == "dark"
    
    if is_dark:
        theme_vars = """
        --bg-main: #1C2620;
        --surface: #24332B;
        --surface-elevated: #2C3D34;
        --surface-header-band: #33443A;
        --kpi-title-color: #D3E4DA;
        --text-primary: #EEF4F0;
        --text-secondary: #A6BCB0;
        --border-subtle: #3D5246;
        --border-accent: #52B788;
        --brand-primary: #52B788;
        --hero-bg: linear-gradient(135deg, #24332B 0%, #33443A 50%, #3D5246 100%);
        --hero-text: #FFFFFF;
        --hero-sub: #D5E5DC;
        --calc-bg: #24332B;
        --calc-res-bg: #2C3D34;
        --table-badge-bg: #33443A;
        --table-badge-text: #BCE0CD;
        --input-bg: #33443A;
        --tag-bg: #44574C;
        --tag-text: #EEF4F0;
        --tag-border: #5C7365;
        --btn-inactive-bg: #33443A;
        --btn-inactive-text: #EEF4F0;
        --btn-active-bg: #3D5C4A;
        --btn-active-text: #FFFFFF;
        --shadow-card: 0 4px 14px rgba(0, 0, 0, 0.25);
        """
    else:
        theme_vars = """
        --bg-main: #F4F7F4;
        --surface: #FFFFFF;
        --surface-elevated: #F6FAF7;
        --surface-header-band: #33443A;
        --kpi-title-color: #FFFFFF;
        --text-primary: #12241A;
        --text-secondary: #4F6357;
        --border-subtle: #C8D6CD;
        --border-accent: #33443A;
        --brand-primary: #33443A;
        --hero-bg: linear-gradient(135deg, #24332B 0%, #33443A 60%, #44574C 100%);
        --hero-text: #FFFFFF;
        --hero-sub: #E2ECE5;
        --calc-bg: #FFFFFF;
        --calc-res-bg: #F2F7F4;
        --table-badge-bg: #E1EDE5;
        --table-badge-text: #223B2D;
        --input-bg: #33443A;
        --tag-bg: #44574C;
        --tag-text: #EEF4F0;
        --tag-border: #5C7365;
        --btn-inactive-bg: #FFFFFF;
        --btn-inactive-text: #223B2D;
        --btn-active-bg: #33443A;
        --btn-active-text: #FFFFFF;
        --shadow-card: 0 2px 10px rgba(45, 62, 52, 0.08);
        """

    custom_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {{
        {theme_vars}
    }}

    /* 1. Глобальный сброс фона и шрифтов */
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

    /* 4. ГРЯЗНО-СЕРО-ЗЕЛЕНЫЙ МУЛЬТИСЕЛЕКТ */
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    div[data-testid="stMultiSelect"] > div,
    div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {{
        background-color: var(--input-bg) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
    }}

    /* Плашки мультиселекта (Горох, Кукуруза, No-Till...) */
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

    div[data-baseweb="popover"],
    ul[role="listbox"] {{
        background-color: var(--surface-elevated) !important;
        border: 1px solid var(--border-subtle) !important;
    }}
    li[role="option"] {{
        background-color: var(--surface-elevated) !important;
        color: var(--text-primary) !important;
    }}

    /* 5. Загрузчик файлов */
    [data-testid="stFileUploader"] section {{
        background-color: var(--surface-elevated) !important;
        border: 1px dashed var(--border-subtle) !important;
        border-radius: 12px !important;
    }}
    [data-testid="stFileUploader"] section * {{
        color: var(--text-primary) !important;
    }}

    /* 6. Карточки метрик (Двухтоновые) */
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

    /* 7. Баннер, Графики и Калькулятор */
    .hero-banner {{
        background: var(--hero-bg);
        border-radius: 16px;
        padding: 28px 32px;
        color: var(--hero-text) !important;
        margin-bottom: 24px;
        box-shadow: var(--shadow-card);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }}
    .hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        color: #E8F8EE;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        padding: 4px 12px;
        border-radius: 30px;
        margin-bottom: 10px;
    }}
    .hero-title {{
        font-size: 2.0rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: var(--hero-text) !important;
        margin: 0 0 6px 0;
    }}
    .hero-subtitle {{
        font-size: 0.98rem;
        color: var(--hero-sub) !important;
        font-weight: 400;
        max-width: 800px;
        margin: 0;
        line-height: 1.5;
    }}

    .stPlotlyChart {{
        background: var(--surface);
        border-radius: 14px;
        border: 1px solid var(--border-subtle);
        padding: 10px;
        box-shadow: var(--shadow-card);
    }}
    .calc-container {{
        background: var(--calc-bg);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 24px;
        box-shadow: var(--shadow-card);
        margin-top: 24px;
    }}
    .calc-result-card {{
        background: var(--calc-res-bg);
        border-radius: 12px;
        padding: 18px;
        border: 1px solid var(--border-subtle);
    }}
    .calc-res-title {{
        font-size: 0.78rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.6px;
        color: var(--text-secondary) !important;
    }}
    .calc-res-val {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-primary) !important;
    }}

    /* 8. Справочник */
    .formula-card {{
        background: var(--surface);
        border-radius: 14px;
        border: 1px solid var(--border-subtle);
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: var(--shadow-card);
    }}
    .formula-card h3 {{
        color: var(--brand-primary);
        font-size: 1.1rem;
        font-weight: 700;
        margin-top: 0;
    }}
    .data-table-badge {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        background: var(--table-badge-bg);
        color: var(--table-badge-text);
        padding: 2px 7px;
        border-radius: 6px;
        border: 1px solid var(--border-subtle);
    }}

    footer {{visibility: hidden;}}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)