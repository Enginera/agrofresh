import streamlit as st

def apply_custom_styles():
    """Применяет CSS-стили с сочными прозрачно-зелеными кнопками и идеально выверенными размерами карточек."""
    st.markdown("""
    <style>
    /* ОБЩИЙ ФОН ПРИЛОЖЕНИЯ */
    .stApp { background-color: #F4F9F4 !important; }
    h1, h2, h3 { color: #1B5E20 !important; font-family: 'Inter', sans-serif !important; font-weight: 600 !important; }
    
    /* СТИЛИЗАЦИЯ И ВЫРАВНИВАНИЕ ВСЕХ КАРТОЧЕК */
    .metric-card { 
        background: white !important; 
        padding: 10px 4px !important;     
        border-radius: 8px !important; 
        border: 1px solid #C8E6C9 !important; 
        box-shadow: none !important;        
        box-sizing: border-box !important;
        
        height: 115px !important; 
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        align-items: center !important;
        text-align: center !important;
    }
    
    /* СТИЛИЗАЦИЯ НАШИХ НОВЫХ КЛАССОВ ТЕКСТА (ДЛЯ ПК) */
    .card-title-text {
        font-size: 14px;
        font-weight: 600;
        color: #1A1A1A;
        display: block;
    }
    .card-value-text {
        font-size: 18px;
        font-weight: 700;
        color: #1B5E20;
    }
    .card-sub-text {
        font-size: 12px;
        color: #4B5563;
    }
    
    /* Стили для приветственной карточки */
    .welcome-card {
        background: #E8F5E9; 
        border: 1px solid #C8E6C9 !important;
        border-left: 5px solid #2E7D32 !important; 
        padding: 12px 18px !important; 
        border-radius: 8px; 
        margin-bottom: 20px;
        box-shadow: none !important;        
    }
    .welcome-card h2 { margin: 0 0 6px 0 !important; font-size: 22px !important; color: #1B5E20 !important; }
    .welcome-card p { margin: 0 !important; color: #3E2723; }
    
    /* --- СТИЛИЗАЦИЯ ВЫЕЗЖАЮЩЕГО МЕНЮ (SIDEBAR) --- */
    [data-testid="stSidebar"] {
        background-color: #EBF3E3 !important; 
        border-right: 1px solid #C8E6C9;
    }
    
    [data-testid="stSidebarCollapsedControl"] {
        background-color: #EBF3E3 !important;
        border: 1px solid #A5D6A7;
        border-left: none;
        border-radius: 0 8px 8px 0 !important;
        width: 38px !important;
        height: 48px !important;
        top: 15px !important;
        left: 0px !important;
        box-shadow: none !important; 
    }

    /* --- ЯРКИЕ ЗЕЛЕНЫЕ НО ПРОЗРАЧНЫЕ КНОПКИ НАВИГАЦИИ (ДЛЯ ПК) --- */
    div.stButton > button:first-child {
        height: 4.2em;
        border-radius: 10px;
        border: 2px solid #2E7D32;                 
        background-color: rgba(76, 175, 80, 0.12) !important; 
        color: #1B5E20 !important;                 
        font-size: 15px;
        font-weight: 600;
        box-shadow: none !important;
    }

    /* --- МОБИЛЬНАЯ АДАПТАЦИЯ (ЭКРАНЫ МЕНЕЕ 768px) --- */
    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            display: flex !important;
            gap: 5px !important;
        }
        [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 32% !important;
            min-width: 0 !important;
            width: 32% !important;
        }

        /* УДЕРЖИВАЕМ ОБА БЛОКА КАРТОЧЕК В ОДИН РЯД */
        .main div.welcome-card + [data-testid="stHorizontalBlock"],
        .main [data-testid="stVerticalBlock"] > div:last-child [data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            display: flex !important;
            gap: 4px !important;
        }
        .main div.welcome-card + [data-testid="stHorizontalBlock"] > div,
        .main [data-testid="stVerticalBlock"] > div:last-child [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 32% !important;
            min-width: 0 !important;
            width: 32% !important;
        }
        
        /* СКОРРЕКТИРОВАННЫЕ НА СТРОГИЕ 2% МЕНЕЕ МОБИЛЬНЫЕ ШРИФТЫ */
        .card-title-text {
            font-size: 9.3px !important; 
            line-height: 1.1 !important;
            display: block !important;
            min-height: 24px;
        }
        .card-value-text {
            font-size: 13.2px !important; 
            margin: 0 !important;
            padding: 0 !important;
        }
        .card-sub-text {
            font-size: 7.8px !important;
            display: block !important;
        }
        .status-badge {
            font-size: 7.8px !important;
            padding: 2px 4px !important;
            margin-bottom: 2px !important;
        }

        /* Адаптивные маленькие кнопки на мобильных */
        div.stButton > button:first-child {
            height: 4.8em !important;      
            padding: 2px 4px !important;   
            font-size: 9px !important;     
            line-height: 1.1 !important;   
            white-space: normal !important;
            word-wrap: break-word !important;
            border-radius: 6px !important; 
            border-width: 1px !important;  
        }
        
        .welcome-card { padding: 12px !important; margin-bottom: 15px !important; border-left-width: 3px !important; }
        .welcome-card h2 { font-size: 14px !important; font-weight: 700 !important; line-height: 1.2 !important; }
        .welcome-card p { font-size: 11px !important; line-height: 1.2 !important; }
    }
    </style>
    """, unsafe_allow_html=True)
