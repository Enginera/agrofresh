import streamlit as st

def apply_custom_styles():
    """Применяет фирменную палитру и карточки по макетам модуля."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .main .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2.5rem;
            max-width: 96%;
        }

        /* Сайдбар */
        section[data-testid="stSidebar"] {
            background-color: #06281c !important;
            border-right: 1px solid rgba(52, 211, 153, 0.2);
        }

        /* Заголовок модуля */
        .module-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
            padding-bottom: 0.8rem;
            border-bottom: 1px solid rgba(52, 211, 153, 0.25);
        }
        .module-title-box {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .module-logo {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: #0f4432;
            border: 2px solid #34d399;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        .module-title {
            font-size: 1.35rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: 0.02em;
            margin: 0;
            text-transform: uppercase;
        }
        .module-subtitle {
            font-size: 1.05rem;
            font-weight: 600;
            color: #a7f3d0;
            margin: 2px 0 0 0;
        }

        /* Карточки метрик */
        .agro-card {
            background: #0e3d2d;
            border: 1px solid #165b43;
            border-radius: 6px;
            padding: 16px 14px 12px 14px;
            min-height: 125px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
            margin-bottom: 16px;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }
        .agro-card:hover {
            border-color: #34d399;
            transform: translateY(-2px);
        }
        .agro-card-title {
            color: #ffffff;
            font-size: 0.88rem;
            font-weight: 600;
            line-height: 1.3;
            margin-bottom: 10px;
        }
        .agro-card-valbox {
            background-color: #ffffff;
            color: #092e20;
            font-weight: 700;
            font-size: 1.05rem;
            text-align: center;
            padding: 7px 12px;
            border-radius: 4px;
            align-self: center;
            min-width: 140px;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);
        }

        /* Плитки каталога F1-F6 */
        .fn-tile {
            background: #0e3d2d;
            border: 2px solid #1a6b4f;
            border-radius: 8px;
            padding: 24px 16px;
            text-align: center;
            color: #ffffff;
            font-weight: 700;
            font-size: 1.05rem;
            min-height: 110px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 14px rgba(0,0,0,0.3);
            margin-bottom: 10px;
        }

        .sidebar-footer {
            background: rgba(14, 61, 45, 0.7);
            border: 1px solid rgba(52, 211, 153, 0.2);
            border-radius: 6px;
            padding: 10px 12px;
            margin-top: 25px;
            font-size: 0.75rem;
            color: #a7f3d0;
            line-height: 1.35;
        }

        .section-title {
            color: #ecfdf5;
            font-size: 1.15rem;
            font-weight: 700;
            border-left: 4px solid #10b981;
            padding-left: 10px;
            margin: 15px 0 15px 0;
        }
        </style>
    """, unsafe_allow_html=True)

def render_top_header(subtitle: str = ""):
    """Рендерит верхнюю плашку с логотипом, заголовком и кнопками."""
    col_left, col_right = st.columns([3.5, 1.2])
    with col_left:
        st.markdown(f"""
            <div class="module-title-box">
                <div class="module-logo">🌾</div>
                <div>
                    <div class="module-title">МОДУЛЬ УГЛЕРОД НЕЙТРАЛЬНОГО ЗЕМЛЕДЕЛИЯ</div>
                    {f'<div class="module-subtitle">{subtitle}</div>' if subtitle else ''}
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col_right:
        c_p, c_e = st.columns(2)
        with c_p:
            st.button("🖨️ Печать", use_container_width=True)
        with c_e:
            st.button("📥 Экспорт", use_container_width=True)

def render_card(title: str, value_text: str):
    """Отрисовывает карточку показателя с белым полем для значения."""
    st.markdown(f"""
        <div class="agro-card">
            <div class="agro-card-title">{title}</div>
            <div class="agro-card-valbox">{value_text}</div>
        </div>
    """, unsafe_allow_html=True)