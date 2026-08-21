import streamlit as st

def apply_custom_styles(theme="dark"):
    is_dark = theme == "dark"

    if is_dark:
        # === 🌙 ТЁМНАЯ ТЕМА ===
        theme_vars = """
        --browser-scheme: dark;
        --bg-main: #0F1D16;
        --sidebar-bg: #15261E;
        --card-bg: #1A2E24;
        --card-border: #274435;
        --card-accent: #52B788;
        --text-main: #EEF6F1;
        --text-muted: #9BB3A6;
        --text-metric-val: #74C69D;
        --table-border: #274435;
        --input-bg: #1A2E24;
        --input-border: #2B4D3C;
        --btn-bg: #1A2E24;
        --btn-text: #EEF6F1;
        --btn-active-bg: #2D6A4F;
        """
    else:
        # === ☀️ СВЕТЛАЯ ТЕМА ===
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
        --input-bg: #FFFFFF;
        --input-border: #D0DCD4;
        --btn-bg: #FFFFFF;
        --btn-text: #1B3826;
        --btn-active-bg: #2E7D32;
        """

    css_template = """
    <style>
    :root {
        __THEME_VARS__
    }

    /* 1. ПРИНУДИТЕЛЬНАЯ БЛОКИРОВКА СИСТЕМНОЙ ТЕМЫ ОС/БРАУЗЕРА */
    :root, html, body, .stApp, 
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"],
    section.main,
    .main .block-container {
        color-scheme: var(--browser-scheme) !important;
        background-color: var(--bg-main) !important;
        color: var(--text-main) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
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

    /* 2. Карточки метрик */
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

    /* 3. Сайдбар */
    [data-testid="stSidebar"], 
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"],
    [data-testid="stSidebar"] > div:first-child {
        background-color: var(--sidebar-bg) !important;
        background: var(--sidebar-bg) !important;
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

    /* 4. Кнопки верхней навигации */
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

    /* 5. Мультиселект (Контейнер и поле ввода) */
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] > div,
    [data-testid="stMultiSelect"] [data-baseweb="select"] > div {
        background-color: var(--input-bg) !important;
        background: var(--input-bg) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 6px !important;
    }

    /* Базовые стили для всех плашек тегов */
    div[data-baseweb="tag"],
    span[data-baseweb="tag"],
    [data-testid="stMultiSelect"] span[data-baseweb="tag"],
    [data-testid="stMultiSelect"] div[data-baseweb="tag"] {
        border-radius: 4px !important;
        padding: 3px 8px !important;
    }
    div[data-baseweb="tag"] span,
    div[data-baseweb="tag"] div,
    span[data-baseweb="tag"] span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="tag"] svg,
    span[data-baseweb="tag"] svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }

    /* 6. ТОЧНАЯ ПРИВЯЗКА ЦВЕТОВ КУЛЬТУР ПО ARIA-LABEL И TITLE */
    /* 🌽 Кукуруза -> Голубой (#4EA8DE) */
    [data-baseweb="tag"][aria-label*="Кукуруза"],
    [data-baseweb="tag"]:has(span[title*="Кукуруза"]),
    [data-testid="stMultiSelect"] [data-baseweb="tag"][aria-label*="Кукуруза"] {
        background-color: #4EA8DE !important;
        background: #4EA8DE !important;
        border: 1px solid #3A8EC0 !important;
    }

    /* 🟢 Горох -> Мятно-зеленый (#52B788) */
    [data-baseweb="tag"][aria-label*="Горох"],
    [data-baseweb="tag"]:has(span[title*="Горох"]),
    [data-testid="stMultiSelect"] [data-baseweb="tag"][aria-label*="Горох"] {
        background-color: #52B788 !important;
        background: #52B788 !important;
        border: 1px solid #3F9A70 !important;
    }

    /* 🌾 Озимая пшеница -> Янтарно-оранжевый (#F4A261) */
    [data-baseweb="tag"][aria-label*="Озимая"],
    [data-baseweb="tag"][aria-label*="пшеница"],
    [data-baseweb="tag"]:has(span[title*="Озимая"]),
    [data-testid="stMultiSelect"] [data-baseweb="tag"][aria-label*="Озимая"] {
        background-color: #F4A261 !important;
        background: #F4A261 !important;
        border: 1px solid #D98848 !important;
    }

    /* 🌺 Лён -> Кораллово-терракотовый (#E07A5F) */
    [data-baseweb="tag"][aria-label*="Лён"],
    [data-baseweb="tag"][aria-label*="лен"],
    [data-baseweb="tag"][aria-label*="Лен"],
    [data-baseweb="tag"]:has(span[title*="Лён"]),
    [data-testid="stMultiSelect"] [data-baseweb="tag"][aria-label*="Лён"] {
        background-color: #E07A5F !important;
        background: #E07A5F !important;
        border: 1px solid #C46247 !important;
    }

    /* 🌿 Многолетние травы -> Глубокий индиго (#3D5A80) */
    [data-baseweb="tag"][aria-label*="Многолет"],
    [data-baseweb="tag"][aria-label*="травы"],
    [data-baseweb="tag"]:has(span[title*="Многолет"]),
    [data-testid="stMultiSelect"] [data-baseweb="tag"][aria-label*="Многолет"] {
        background-color: #3D5A80 !important;
        background: #3D5A80 !important;
        border: 1px solid #2B4360 !important;
    }

    /* 🌻 Подсолнечник -> Фиолетовый (#9D4EDD) */
    [data-baseweb="tag"][aria-label*="Подсолне"],
    [data-baseweb="tag"]:has(span[title*="Подсолне"]),
    [data-testid="stMultiSelect"] [data-baseweb="tag"][aria-label*="Подсолне"] {
        background-color: #9D4EDD !important;
        background: #9D4EDD !important;
        border: 1px solid #7F35BF !important;
    }

    /* 🌱 No-Till -> Зеленый (#2E7D32) */
    [data-baseweb="tag"][aria-label*="No-Till"],
    [data-baseweb="tag"][aria-label*="notill"],
    [data-baseweb="tag"]:has(span[title*="No-Till"]),
    [data-testid="stMultiSelect"] [data-baseweb="tag"][aria-label*="No-Till"] {
        background-color: #2E7D32 !important;
        background: #2E7D32 !important;
        border: 1px solid #1B5E20 !important;
    }

    /* 🚜 Классическая -> Красный (#C62828) */
    [data-baseweb="tag"][aria-label*="Классиче"],
    [data-baseweb="tag"]:has(span[title*="Классиче"]),
    [data-testid="stMultiSelect"] [data-baseweb="tag"][aria-label*="Классиче"] {
        background-color: #C62828 !important;
        background: #C62828 !important;
        border: 1px solid #8E0000 !important;
    }

    /* 7. Выпадающий список мультиселекта */
    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    ul[role="listbox"] {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
    }
    li[role="option"] {
        background-color: var(--card-bg) !important;
        color: var(--text-main) !important;
    }

    /* 8. Таблица и Графики */
    .stDataFrame {
        border: 1px solid var(--table-border) !important;
        border-radius: 6px;
        background-color: var(--card-bg) !important;
    }
    .stPlotlyChart {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 8px;
        padding: 6px;
    }

    footer {visibility: hidden;}
    </style>
    """
    custom_css = css_template.replace("__THEME_VARS__", theme_vars)
    st.markdown(custom_css, unsafe_allow_html=True)