import streamlit as st

# Импорт конфигурационных и математических блоков
from styles import apply_custom_styles
from parser import advanced_multi_field_parser, get_mock_data

# Импорт интерфейсных блоков навигации и дашбордов
from navigation import render_button_navigation
from dashboards import render_page_content

# 1. Применение общих настроек и темы мобильной адаптации
st.set_page_config(layout="wide", page_title="AgriCarbon Manager", page_icon="🌱")
apply_custom_styles()

# Фиксируем дефолтную страницу в сессии
if 'page' not in st.session_state:
    st.session_state.page = "Обзор"

# 2. Боковая панель в левой части (Светло-серая выезжающая плашка)
st.sidebar.markdown("### Загрузка метаданных 📂")
uploaded_file = st.sidebar.file_uploader("Перетащите агрономическую таблицу Excel", type=["xlsx", "xls"])

# Чтение загруженного Excel-файла или подгрузка демонстрационных данных
file_data = advanced_multi_field_parser(uploaded_file)
all_fields_dict = file_data if file_data is not None else get_mock_data()

# БЕЗОПАСНЫЙ ПРЕДОХРАНИТЕЛЬ: Проверяем, не пустой ли словарь данных
if not all_fields_dict:
    all_fields_dict = get_mock_data()

field_options = list(all_fields_dict.keys())
selected_field = st.sidebar.selectbox("Выберите Поле для анализа: 🎯", field_options)

# БЕЗОПАСНЫЙ ПЕРЕХВАТ КЛЮЧА: Если ключ пропал, берем первое доступное поле
if selected_field in all_fields_dict:
    df_active = all_fields_dict[selected_field]
else:
    df_active = all_fields_dict[list(all_fields_dict.keys())[0]]

# Математический расчет основных параметров выбранного поля
area_value = f"{df_active['Площадь'].iloc[0]:.2f} га" if (len(df_active) > 0 and 'Площадь' in df_active.columns) else "118.06 га"
depth_value = f"{df_active['Глубина'].iloc[0]:.2f} м" if (len(df_active) > 0 and 'Глубина' in df_active.columns) else "0.30 м"
avg_e_calculated = df_active['Эффективность'].mean() if 'Эффективность' in df_active.columns else 0.0

# 3. Запускаем навигацию
render_button_navigation()

# 4. Отображение контента в зависимости от нажатой кнопки
render_page_content(
    st.session_state.page, 
    df_active, 
    selected_field, 
    area_value, 
    depth_value, 
    avg_e_calculated
)
