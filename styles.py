import streamlit as st

def apply_custom_styles():
    """Применяет CSS-стили с сочными прозрачно-зелеными кнопками и всеми карточками в один ряд."""
    st.markdown("""
    <style>
    /* ОБЩИЙ ФОН ПРИЛОЖЕНИЯ: Делаем более зеленым, но очень светлым и мягким */
    .stApp { background-color: #F4F9F4 !important; }
    h1, h2, h3 { color: #1B5E20 !important; font-family: 'Inter', sans-serif !important; font-weight: 600 !important; }
    
    /* СТИЛИЗАЦИЯ И ПРИНУДИТЕЛЬНОЕ ВЫРАВНИВАНИЕ ПЛОСКИХ КАРТОЧЕК */
    [data-testid="stMetric"], .metric-card { 
        background: white !important; 
        padding: 10px 10px !important;     
        border-radius: 8px !important; 
        border: 1px solid #C8E6C9 !important; 
        box-shadow: none !important;        
        box-sizing: border-box !important;
    }
    
    [data-testid="stMetric"] > div {
        box-shadow: none !important;
        border: none !important;
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
    
    /* Прямоугольная вертикальная закладочка для мобильного меню */
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
        transition: all 0.3s ease;
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
        transition: all 0.2s ease;
        box-shadow: none !important;
    }
    div.stButton > button:first-child:hover { 
        background-color: rgba(46, 125, 50, 0.25) !important; 
        border-color: #1B5E20;
        color: #1B5E20 !important;
    }

    /* --- МОБИЛЬНАЯ АДАПТАЦИЯ (ЭКРАНЫ МЕНЕЕ 768px) --- */
    @media (max-width: 768px) {
        /* Принудительно сохраняем 3 колонки кнопок в один горизонтальный ряд на телефоне */
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

        /* 1. ЖЕСТКО НОРМАЛИЗУЕМ ВЕРХНИЙ РЯД КАРТОЧЕК (ПОД ДОБРО ПОЖАЛОВАТЬ) В ОДИН РЯД */
        .main div.welcome-card + [data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            display: flex !important;
            gap: 4px !important;
        }
        .main div.welcome-card + [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 32% !important;
            min-width: 0 !important;
            width: 32% !important;
        }
        
        /* Ультра-компактный шрифт для верхних метрик, чтобы всё влезло в строку дисплея */
        .top-kpi-card {
            padding: 8px 4px !important;
            font-size: 8px !important;
            line-height: 1.1 !important;
        }
        .top-kpi-card b { font-size: 8px !important; }
        .top-kpi-card h3 { font-size: 11px !important; margin: 2px 0 0 0 !important; }

        /* 2. ЖЕСТКО УДЕРЖИВАЕМ НИЖНИЙ БЛОК «СОСТОЯНИЕ МОДУЛЕЙ» В ОДИН РЯД */
        .main [data-testid="stVerticalBlock"] > div:last-child [data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            display: flex !important;
            gap: 4px !important;
        }
        .main [data-testid="stVerticalBlock"] > div:last-child [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 32% !important;
            min-width: 0 !important;
            width: 32% !important;
        }
        
        /* Шрифт для нижних модулей */
        .module-card {
            padding: 8px 4px !important;
            font-size: 8px !important;
            line-height: 1.1 !important;
        }
        .module-card b { font-size: 8px !important; }
        .module-card small { font-size: 7px !important; }
        .module-card .status-badge { font-size: 7px !important; padding: 2px 4px !important; }

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
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
        }
        
        /* Адаптация приветственного блока */
        .welcome-card { padding: 12px !important; margin-bottom: 15px !important; border-left-width: 3px !important; }
        .welcome-card h2 { font-size: 14px !important; font-weight: 700 !important; line-height: 1.2 !important; }
        .welcome-card p { font-size: 11px !important; line-height: 1.2 !important; }
    }
    </style>
    """, unsafe_allow_html=True)
