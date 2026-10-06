import streamlit as st

def apply_global_styles(mode="carbon"):
    """
    Применяет глобальный CSS-дизайн в стиле HTML-прототипов.
    mode: 'carbon' | 'organic'
    """
    theme_accent = "#1e7655" if mode == "carbon" else "#2d8b68"
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    :root {{
        --bg: #edf4f1;
        --card-bg: #ffffff;
        --ink: #20312b;
        --muted: #71817b;
        --green-primary: {theme_accent};
        --green-dark: #143c2d;
        --green-light: #e8f2ed;
        --blue-accent: #4e91ad;
        --pink-accent: #a93d72;
        --amber-accent: #e49a27;
        --line: #e2e9e5;
        --shadow: 0 8px 24px rgba(25, 55, 43, 0.07);
    }}
    
    html, body, [class*="css"] {{
        font-family: 'Inter', 'Segoe UI', sans-serif;
        color: var(--ink);
    }}
    
    .stApp {{
        background: linear-gradient(180deg, #edf4f1 0%, #f6f9f7 100%);
    }}
    
    /* Стилизация Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: var(--green-dark) !important;
        color: #dcece5 !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: #dcece5 !important;
    }}
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label {{
        color: #a9c8b9 !important;
        font-weight: 600;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    /* Шапка дашборда */
    .dashboard-header {{
        margin-bottom: 20px;
    }}
    .eyebrow {{
        color: #5b8072;
        font-weight: 800;
        font-size: 11px;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }}
    .dashboard-title {{
        font-size: 28px;
        font-weight: 800;
        margin: 0 0 6px 0;
        letter-spacing: -0.02em;
        color: var(--ink);
    }}
    .dashboard-subtitle {{
        color: var(--muted);
        font-size: 13px;
        margin-bottom: 16px;
    }}
    
    /* Карточки KPI */
    .kpi-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 12px;
        margin-bottom: 20px;
    }}
    .kpi-card {{
        background: var(--card-bg);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: var(--shadow);
    }}
    .kpi-label {{
        font-size: 12px;
        color: var(--muted);
        font-weight: 500;
    }}
    .kpi-value {{
        font-size: 24px;
        font-weight: 800;
        color: var(--ink);
        margin: 6px 0 2px 0;
        font-variant-numeric: tabular-nums;
    }}
    .kpi-hint {{
        font-size: 11px;
        color: #8a9993;
    }}
    
    /* Баннер информации о поле / сводке */
    .field-banner {{
        background: linear-gradient(135deg, #174f3a, #236f51);
        color: #ffffff !important;
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 10px 24px rgba(23, 79, 58, 0.18);
        margin-bottom: 24px;
    }}
    .field-banner * {{
        color: #ffffff !important;
    }}
    .field-grid {{
        display: grid;
        grid-template-columns: 1.5fr repeat(5, 1fr);
        gap: 12px;
        margin-top: 14px;
    }}
    .field-stat {{
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 10px 12px;
    }}
    .field-stat span {{
        font-size: 11px;
        color: #cde4d9 !important;
        display: block;
    }}
    .field-stat b {{
        font-size: 16px;
        font-weight: 700;
        display: block;
        margin-top: 3px;
    }}
    
    /* Таблицы */
    .styled-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--line);
    }}
    .styled-table th {{
        background: #f8faf9;
        color: var(--muted);
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 10px 14px;
        border-bottom: 1px solid var(--line);
        text-align: left;
    }}
    .styled-table td {{
        padding: 10px 14px;
        border-bottom: 1px solid #f1f4f2;
    }}
    .status-ok {{
        color: #1e7655;
        font-weight: 700;
    }}
    .status-bad {{
        color: #a93d72;
        font-weight: 700;
    }}
    
    /* Чипы и теги */
    .chip {{
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        background: #e8f2ed;
        color: #1e7655;
        font-size: 12px;
        font-weight: 600;
        margin: 2px;
    }}
    </style>
    """, unsafe_allow_html=True)