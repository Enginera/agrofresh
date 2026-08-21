import streamlit as st

def apply_custom_styles():
    """Подключение кастомных стилей интерфейса."""
    custom_css = """
    <style>
        .main-header {
            font-size: 2.1rem;
            font-weight: 700;
            color: #1B5E20;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #4E6E58;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            background-color: #FFFFFF;
            border: 1px solid #E0E7E1;
            border-left: 5px solid #2E7D32;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.04);
        }
        .metric-title {
            font-size: 0.85rem;
            color: #616161;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .metric-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: #1B5E20;
            margin-top: 4px;
        }
        [data-testid="stSidebar"] {
            background-color: #F4F9F4;
            border-right: 1px solid #E3ECE3;
        }
        .stDataFrame {
            border: 1px solid #E0E0E0;
            border-radius: 6px;
        }
        footer {visibility: hidden;}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)