import streamlit as st

def apply_custom_styles(theme="dark"):
    is_dark = theme == "dark"
    
    # CSS переменные под тему
    vars_css = """
    :root {
        --bg-main: #0B1612;
        --surface: #13251E;
        --surface-elevated: #182E25;
        --surface-header-band: #091510;
        --text-primary: #F0F6F2;
        --text-secondary: #95AA9E;
        --border-subtle: #234436;
        --border-accent: #52B788;
        --brand-primary: #52B788;
        --brand-forest: #2D6A4F;
        --calc-bg: #11231C;
        --table-badge-bg: #1B382B;
        --table-badge-text: #74C69D;
        --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.35);
    }
    """ if is_dark else """
    :root {
        --bg-main: #F2F6F3;
        --surface: #FFFFFF;
        --surface-elevated: #F8FAF8;
        --surface-header-band: #122B1E; /* Контрастная темная шапка в светлой теме */
        --text-primary: #0E1E16;
        --text-secondary: #52665B;
        --border-subtle: #D5E0D8;
        --border-accent: #2D6A4F;
        --brand-primary: #2D6A4F;
        --brand-forest: #1B4332;
        --calc-bg: #FFFFFF;
        --table-badge-bg: #EDF5F0;
        --table-badge-text: #1B4332;
        --shadow-card: 0 2px 10px rgba(10, 37, 24, 0.05);
    }
    """

    custom_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    {vars_css}

    /* Базовая типографика и фон приложения */
    html, body, [class*="css"], .stApp {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
    }}

    /* Баннер шапки */
    .hero-banner {{
        background: linear-gradient(135deg, #07170F 0%, #122E22 50%, #1E4D36 100%);
        border-radius: 18px;
        padding: 30px 34px;
        color: #FFFFFF !important;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(82, 183, 136, 0.25);
        box-shadow: var(--shadow-card);
    }}
    .hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(8px);
        color: #95D5B2;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        padding: 4px 12px;
        border-radius: 30px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }}
    .hero-title {{
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #FFFFFF;
        margin: 0 0 6px 0;
    }}
    .hero-subtitle {{
        font-size: 1.0rem;
        color: #D8F3DC;
        font-weight: 400;
        max-width: 800px;
        margin: 0;
        line-height: 1.5;
    }}

    /* ДВУХТОНОВЫЕ КАРТОЧКИ МЕТРИК (Контрастная темная шапка) */
    .kpi-card {{
        background: var(--surface);
        border-radius: 14px;
        border: 1px solid var(--border-subtle);
        box-shadow: var(--shadow-card);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .kpi-card:hover {{
        transform: translateY(-2px);
        border-color: var(--border-accent);
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
        font-size: 0.8rem;
        font-weight: 700;
        color: #E8F5E9; /* Всегда четкий светлый контрастный текст на темной плашке */
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}
    .kpi-icon {{
        font-size: 1.05rem;
        line-height: 1;
    }}
    .kpi-card-body {{
        padding: 16px;
        background: var(--surface);
    }}
    .kpi-value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.85rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.5px;
    }}
    .kpi-unit {{
        font-size: 0.88rem;
        font-weight: 500;
        color: var(--text-secondary);
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
        color: var(--text-secondary);
        border: 1px solid var(--border-subtle);
    }}

    /* Калькулятор No-Till */
    .calc-container {{
        background: var(--calc-bg);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 24px;
        box-shadow: var(--shadow-card);
        margin-top: 24px;
        margin-bottom: 24px;
    }}
    .calc-header {{
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 4px;
    }}
    .calc-desc {{
        color: var(--text-secondary);
        font-size: 0.88rem;
        margin-bottom: 18px;
    }}
    .calc-result-card {{
        background: var(--surface-elevated);
        border-radius: 12px;
        padding: 18px;
        border: 1px solid var(--border-subtle);
        height: 100%;
    }}
    .calc-res-title {{
        font-size: 0.78rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.6px;
        color: var(--text-secondary);
    }}
    .calc-res-val {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-top: 4px;
    }}

    /* Справочник и формулы */
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

    /* Сайдбар и графики */
    [data-testid="stSidebar"] {{
        background-color: var(--surface) !important;
        border-right: 1px solid var(--border-subtle) !important;
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