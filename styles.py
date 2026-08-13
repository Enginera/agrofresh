import streamlit as st

def apply_custom_styles():
    """Применяет CSS-стили с сочными прозрачно-зелеными кнопками и светлым зеленым фоном."""
    st.markdown("""
    <style>
    /* ОБЩИЙ ФОН ПРИЛОЖЕНИЯ: Делаем более зеленым, но очень светлым и мягким */
    .stApp { background-color: #F4F9F4 !important; }
    h1, h2, h3 { color: #1B5E20 !important; font-family: 'Inter', sans-serif !important; font-weight: 600 !important; }
    
    /* Красивые карточки метрик на новом фоне */
    .metric-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #C8E6C9; box-shadow: 0 4px 12px rgba(27,94,32,0.03); transition: all 0.3s ease; }
    .metric-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(27,94,32,0.06); }
    .status-badge { padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 500; display: inline-block; }
    .status-success { background-color: #E8F5E9; color: #2E7D32; }
    
    /* Стили для приветственной карточки */
    .welcome-card {
        background: #E8F5E9; 
        border-left: 5px solid #2E7D32; 
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 25px;
    }
    .welcome-card h2 { margin: 0 0 8px 0 !important; font-size: 24px !important; color: #1B5E20 !important; }
    .welcome-card p { margin: 0 !important; color: #3E2723; }
    
    /* --- СТИЛИЗАЦИЯ ВЫЕЗЖАЮЩЕГО МЕНЮ (SIDEBAR) --- */
    [data-testid="stSidebar"] {
        background-color: #EBF3E3 !important; /* Боковая панель в тон общему фону */
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
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }

    /* --- ЯРКИЕ ЗЕЛЕНЫЕ НО ПРОЗРАЧНЫЕ КНОПКИ НАВИГАЦИИ (ДЛЯ ПК) --- */
    div.stButton > button:first-child {
        height: 4.2em;
        border-radius: 10px;
        border: 2px solid #2E7D32;                 /* Яркая сочная зеленая рамка */
        background-color: rgba(76, 175, 80, 0.12) !important; /* Ярко-зеленый прозрачный фон */
        color: #1B5E20 !important;                 /* Насыщенный темно-зеленый текст */
        font-size: 15px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    /* Эффект при наведении — кнопка становится более плотной и заливается цветом */
    div.stButton > button:first-child:hover { 
        background-color: rgba(46, 125, 50, 0.25) !important; 
        border-color: #1B5E20;
        color: #1B5E20 !important;
        transform: scale(1.01);
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

        /* Адаптивные маленькие яркие прозрачные кнопки на мобильных */
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
        
        /* АДАПТАЦИЯ ПРИВЕТСТВЕННОГО БЛОКА НА ТЕЛЕФОНЕ */
        .welcome-card {
            padding: 12px !important;      
            margin-bottom: 15px !important;
            border-left-width: 3px !important;
        }
        .welcome-card h2 {
            font-size: 14px !important;    
            font-weight: 700 !important;   
            line-height: 1.2 !important;
        }
        .welcome-card p {
            font-size: 11px !important;    
            line-height: 1.2 !important;
        }

        /* НА СМАРТФОНЕ: Графы показателей выстраиваются строго вертикально друг под другом */
        .main div.welcome-card + [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            display: flex !important;
            gap: 12px !important;
        }
        .main div.welcome-card + [data-testid="stHorizontalBlock"] > div {
            width: 100% !important;
            max-width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
