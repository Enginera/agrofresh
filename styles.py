import streamlit as st

def apply_custom_styles():
    """Применяет фирменный изумрудно-зеленый агро-дизайн AgroFresh."""
    st.markdown("""
        <style>
        /* Главный фон и отступы */
        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
            max-width: 96%;
        }
        
        /* Карточки KPI с зеленым неоновым свечением */
        .metric-card {
            background: linear-gradient(145deg, #064e3b 0%, #022c22 100%);
            border: 1px solid rgba(16, 185, 129, 0.35);
            border-radius: 14px;
            padding: 18px 22px;
            color: #ffffff;
            box-shadow: 0 8px 20px rgba(6, 78, 59, 0.3);
            transition: all 0.3s ease;
            margin-bottom: 12px;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            border-color: #34d399;
            box-shadow: 0 12px 28px rgba(16, 185, 129, 0.45);
        }
        .metric-card h4 {
            margin: 0;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #a7f3d0;
            font-weight: 600;
        }
        .metric-card .metric-value {
            font-size: 2.0rem;
            font-weight: 800;
            margin: 8px 0 4px 0;
            color: #34d399;
            text-shadow: 0 0 12px rgba(52, 211, 153, 0.4);
        }
        .metric-card .metric-sub {
            font-size: 0.8rem;
            color: #94a3b8;
        }
        
        /* Зеленые акценты заголовков */
        .eco-header {
            color: #ecfdf5;
            border-left: 4px solid #10b981;
            padding-left: 12px;
            margin-top: 18px;
            margin-bottom: 14px;
            font-weight: 700;
        }

        /* Бейджи */
        .badge-green {
            background-color: rgba(16, 185, 129, 0.2);
            color: #34d399;
            border: 1px solid #10b981;
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        
        /* Сайдбар */
        section[data-testid="stSidebar"] {
            background-color: #022c22 !important;
            border-right: 1px solid rgba(16, 185, 129, 0.25);
        }
        </style>
    """, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, subtitle: str = ""):
    """Отрисовка зеленой карточки KPI."""
    st.markdown(f"""
        <div class="metric-card">
            <h4>{title}</h4>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtitle}</div>
        </div>
    """, unsafe_allow_html=True)
