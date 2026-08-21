import streamlit as st

def apply_custom_styles(theme="dark"):
    is_dark = theme == "dark"
    
    if is_dark:
        # ТЁМНАЯ ТЕМА (Deep Forest Obsidian)
        theme_vars = """
        --bg-main: #0B1612;
        --surface: #13251E;
        --surface-elevated: #182E25;
        --surface-header-band: #0A1913;
        --kpi-title-color: #A7D7BD;
        --text-primary: #F0F6F2;
        --text-secondary: #95AA9E;
        --border-subtle: #234436;
        --border-accent: #52B788;
        --brand-primary: #52B788;
        --hero-bg: linear-gradient(135deg, #07170F 0%, #122E22 50%, #1E4D36 100%);
        --hero-text: #FFFFFF;
        --hero-sub: #D8F3DC;
        --calc-bg: #11231C;
        --calc-res-bg: #182E25;
        --table-badge-bg: #1B382B;
        --table-badge-text: #74C69D;
        --input-bg: #182E25;
        --tag-bg: #1F3E30;
        --tag-text: #95D5B2;
        --btn-inactive-bg: #182E25;
        --btn-inactive-text: #C3D9CC;
        --btn-active-bg: #2D6A4F;
        --btn-active-text: #FFFFFF;
        --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.35);
        """
    else:
        # СВЕТЛАЯ ТЕМА (Precision Botanical Light)
        theme_vars = """
        --bg-main: #F4F7F4;
        --surface: #FFFFFF;
        --surface-elevated: #F8FAF8;
        --surface-header-band: #E3EDE6;
        --kpi-title-color: #1B4332;
        --text-primary: #0F2419;
        --text-secondary: #4A6355;
        --border-subtle: #D2DDD5;
        --border-accent: #2D6A4F;
        --brand-primary: #2D6A4F;
        --hero-bg: linear-gradient(135deg, #1B4332 0%, #2D6A4F 60%, #40916C 100%);
        --hero-text: #FFFFFF;
        --hero-sub: #E8F5E9;
        --calc-bg: #FFFFFF;
        --calc-res-bg: #F4F8F5;
        --table-badge-bg: #E8F2EC;
        --table-badge-text: #1B4332;
        --input-bg: #FFFFFF;
        --tag-bg: #E8F5E9;
        --tag-text: #1B4332;
        --btn-inactive-bg: #FFFFFF;
        --btn-inactive-text: #2D4A3A;
        --btn-active-bg: #2D6A4F;
        --btn-active-text: #FFFFFF;
        --shadow-card: 0 2px 12px rgba(27, 67, 50, 0.06);
        """

    custom_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {{
        {theme_vars}
    }}

    /* 1. Глобальный сброс цветов и фонов */
    html, body, [class*="css"], .stApp {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
    }}

    h1, h2, h3, h4, h5, h6, p, span, label, div {{
        color: var(--text-primary);
    }}

    /* 2. Сайдбар и все текстовые элементы внутри него */
    [data-testid="stSidebar"] {{
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
    [data-testid="stSidebar"] h5 {{
        color: var(--text-primary) !important;
    }}
    [data-testid="stSidebar"] .stCaption, 
    [data-testid="stSidebar"] small {{
        color: var(--text-secondary) !important;
    }}

    /* 3. Кнопки навигации (верхние вкладки) */
    .stButton > button {{
        background-color: var(--btn-inactive-bg) !important;
        color: var(--btn-inactive-text) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: var(--shadow-card) !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button[kind="primary"] {{
        background-color: var(--btn-active-bg) !important;
        color: var(--btn-active-text) !important;
        border: 1px solid var(--btn-active-bg) !important;
    }}
    .stButton > button:hover {{
        border-color: var(--border-accent) !important;
        transform: translateY(-1px);
    }}

    /* 4. Мультиселекты и выпадающие списки */
    div[data-baseweb="select"] > div {{
        background-color: var(--input-bg) !important;
        border: 1px solid var(--border-subtle) !important;
        color: var(--text-primary) !important;
    }}
    div[data-baseweb="select"] span {{
        color: var(--text-primary) !important;
    }}
    div[data-baseweb="tag"] {{
        background-color: var(--tag-bg) !important;
        border: 1px solid var(--border-subtle) !important;
    }}
    div[data-baseweb="tag"] span {{
        color: var(--tag-text) !important;
        font-weight: 600 !important;
    }}

    /* 5. Загрузчик файлов (File Uploader) */
    [data-testid="stFileUploader"] section {{
        background-color: var(--input-bg) !important;
        border: 1px dashed var(--border-subtle) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
    }}
    [data-testid="stFileUploader"] section * {{
        color: var(--text-primary) !important;
    }}
    [data-testid="stFileUploader"] section button {{
        background-color: var(--surface-elevated) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-subtle) !important;
    }}

    /* 6. Главный баннер */
    .hero-banner {{
        background: var(--hero-bg);
        border-radius: 16px;
        padding: 28px 32px;
        color: var(--hero-text) !important;
        margin-bottom: 24px;
        box-shadow: var(--shadow-card);
        border: 1px solid rgba(255, 255, 255, 0.15);
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

    /* 7. KPI-карточки */
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
        letter-spacing: -0.5px;
    }}
    .kpi-unit {{
        font-size: 0.88rem;
        font-weight: 500;
        color: var(--text-secondary) !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        margin-left: 4px;
    }}
    .kpi-sub-badge {{
        margin-top: 8px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 0.73rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
        background: var(--surface-elevated);
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-subtle);
    }}

    /* 8. Калькулятор и Plotly */
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
    .stPlotlyChart {{
        background: var(--surface);
        border-radius: 14px;
        border: 1px solid var(--border-subtle);
        padding: 10px;
        box-shadow: var(--shadow-card);
    }}
    footer {{visibility: hidden;}}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)