import streamlit as st

def apply_custom_styles():
    """Применяет чистый изумрудный дизайн с четким разделением блоков."""
    st.markdown("""
        <style>
        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 95%;
        }
        
        /* Карточки KPI */
        .metric-card {
            background: linear-gradient(135deg, #064e3b 0%, #022c22 100%);
            border: 1px solid rgba(52, 211, 153, 0.35);
            border-radius: 12px;
            padding: 16px 20px;
            color: #ffffff;
            box-shadow: 0 4px 14px rgba(6, 78, 59, 0.25);
            margin-bottom: 15px;
        }
        .metric-card h4 {
            margin: 0;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #a7f3d0;
            font-weight: 600;
        }
        .metric-card .metric-value {
            font-size: 1.85rem;
            font-weight: 800;
            margin: 6px 0 2px 0;
            color: #34d399;
            text-shadow: 0 0 10px rgba(52, 211, 153, 0.3);
        }
        .metric-card .metric-sub {
            font-size: 0.78rem;
            color: #94a3b8;
        }
        
        /* Контейнеры под графики (безопасные отступы) */
        .chart-box {
            background: rgba(6, 78, 59, 0.08);
            border: 1px solid rgba(52, 211, 153, 0.18);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 24px;
        }
        
        .section-title {
            color: #ecfdf5;
            font-size: 1.25rem;
            font-weight: 700;
            border-left: 4px solid #10b981;
            padding-left: 10px;
            margin: 20px 0 15px 0;
        }
        
        /* Сайдбар */
        section[data-testid="stSidebar"] {
            background-color: #022c22 !important;
            border-right: 1px solid rgba(16, 185, 129, 0.2);
        }
        </style>
    """, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, subtitle: str = ""):
    st.markdown(f"""
        <div class="metric-card">
            <h4>{title}</h4>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtitle}</div>
        </div>
    """, unsafe_allow_html=True)
