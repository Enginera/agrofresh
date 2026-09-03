import streamlit as st

def apply_custom_styles():
    """Применяет современную тему оформления для приложения AgroFresh."""
    st.markdown("""
        <style>
        .main .block-container {
            padding-top: 1.8rem;
            padding-bottom: 2.5rem;
            max-width: 95%;
        }
        .metric-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 18px 22px;
            color: #f8fafc;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            margin-bottom: 12px;
        }
        .metric-card h4 {
            margin: 0;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94a3b8;
        }
        .metric-card .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            margin: 8px 0 4px 0;
            color: #38bdf8;
        }
        .metric-card .metric-sub {
            font-size: 0.8rem;
            color: #64748b;
        }
        .dataframe {
            font-size: 0.85rem !important;
        }
        .section-header {
            border-bottom: 2px solid #22c55e;
            padding-bottom: 6px;
            margin-top: 20px;
            margin-bottom: 15px;
            font-weight: 600;
            color: #e2e8f0;
        }
        section[data-testid="stSidebar"] {
            background-color: #0f172a;
            border-right: 1px solid #1e293b;
        }
        </style>
    """, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, subtitle: str = ""):
    """Отрисовывает красивую HTML-карточку метрики."""
    st.markdown(f"""
        <div class="metric-card">
            <h4>{title}</h4>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtitle}</div>
        </div>
    """, unsafe_allow_html=True)
