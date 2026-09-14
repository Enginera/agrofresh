import streamlit as st

def apply_custom_styles():
    """Применяет стилизацию из HTML-прототипа."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700;800;900&display=swap');
        
        html, body, [class*="css"] {
            font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
            color: #24342b;
        }

        .stApp {
            background-color: #f3f6f3;
        }

        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
            max-width: 1550px;
        }

        /* Сайдбар */
        section[data-testid="stSidebar"] {
            background-color: #173b2a !important;
            color: #ffffff !important;
            border-right: none;
        }
        section[data-testid="stSidebar"] * {
            color: #cfe0d6 !important;
        }
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #cfe0d6 !important;
        }

        /* Верхняя шапка */
        .header-box {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        .eyebrow {
            color: #2e6c50;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: .12em;
            font-weight: 800;
        }
        .main-title {
            font-size: 28px;
            font-weight: 850;
            color: #24342b;
            margin: 4px 0;
            line-height: 1.15;
        }
        .sub-title {
            color: #748178;
            font-size: 13px;
        }

        /* Блок функций F1-F6 СВЕРХУ */
        .fn-top-container {
            background: #ffffff;
            border: 1px solid #e0e7e1;
            border-radius: 13px;
            padding: 14px 16px;
            margin-bottom: 14px;
            box-shadow: 0 8px 25px rgba(32,55,43,.06);
        }
        .fn-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 10px;
            margin-top: 8px;
        }
        .fn-card {
            background: #f8faf8;
            border: 1px solid #dbe5dd;
            border-radius: 9px;
            padding: 10px 12px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .fn-card:hover {
            border-color: #2e6c50;
            background: #ffffff;
            box-shadow: 0 4px 12px rgba(46,108,80,0.12);
        }
        .fn-badge {
            font-size: 11px;
            font-weight: 900;
            color: #2e6c50;
            margin-bottom: 3px;
        }
        .fn-title {
            font-size: 11px;
            font-weight: 700;
            color: #24342b;
            line-height: 1.25;
            margin-bottom: 6px;
        }
        .fn-val {
            font-size: 14px;
            font-weight: 850;
            color: #173b2a;
        }

        /* Карточки KPI */
        .kpi-card {
            background: #ffffff;
            border: 1px solid #e0e7e1;
            border-radius: 13px;
            padding: 14px 16px;
            box-shadow: 0 8px 25px rgba(32,55,43,.06);
            margin-bottom: 14px;
        }
        .kpi-card small {
            color: #748178;
            font-weight: 700;
            font-size: 11px;
            text-transform: uppercase;
        }
        .kpi-card .value {
            font-size: 24px;
            font-weight: 850;
            color: #24342b;
            margin-top: 4px;
        }

        /* Блоки графиков */
        .chart-card {
            background: #ffffff;
            border: 1px solid #e0e7e1;
            border-radius: 13px;
            padding: 15px;
            box-shadow: 0 8px 25px rgba(32,55,43,.06);
            margin-bottom: 14px;
            height: 100%;
        }
        .chart-title {
            font-weight: 850;
            font-size: 15px;
            color: #24342b;
            margin: 0;
        }
        .chart-meta {
            color: #748178;
            font-size: 12px;
            margin-bottom: 8px;
        }

        /* Футер сайдбара */
        .sidebar-note {
            background: #24513c;
            padding: 12px;
            border-radius: 10px;
            color: #cfe0d6 !important;
            font-size: 11px;
            line-height: 1.4;
            margin-top: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

def render_top_header(title="Углеродный след агросезона", eyebrow="Аналитическая панель", subtitle="Аналитика данных Excel и визуализация ключевых показателей"):
    """Шапка по макету с кнопками Печать и Экспорт."""
    c_left, c_right = st.columns([3.5, 1.2])
    with c_left:
        st.markdown(f"""
            <div class="header-box">
                <div>
                    <div class="eyebrow">{eyebrow}</div>
                    <div class="main-title">{title}</div>
                    <div class="sub-title">{subtitle}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with c_right:
        st.write("")
        b1, b2 = st.columns(2)
        with b1:
            st.button("🖨️ Печать", use_container_width=True)
        with b2:
            st.button("📥 Экспорт", use_container_width=True, type="primary")