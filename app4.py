import streamlit as st
from parser import detect_workbook_type, parse_carbon_data, parse_organic_data
from styles import apply_global_styles
from navigation import render_sidebar
from dashboards import render_carbon_dashboard, render_organic_dashboard

st.set_page_config(
    page_title="Агрономическая Аналитическая Панель",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "mode" not in st.session_state:
    st.session_state.mode = "carbon"
if "data" not in st.session_state:
    st.session_state.data = None
if "source_name" not in st.session_state:
    st.session_state.source_name = "Демонстрационный датасет"

with st.sidebar:
    st.markdown("### 📂 Загрузка Excel")
    uploaded_file = st.file_uploader("Загрузите XLSX-файл", type=["xlsx", "xls"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        detected_mode = detect_workbook_type(file_bytes)
        st.session_state.mode = detected_mode
        st.session_state.source_name = uploaded_file.name
        
        if detected_mode == "carbon":
            st.session_state.data = parse_carbon_data(file_bytes)
        else:
            st.session_state.data = parse_organic_data(file_bytes)
        st.success(f"Определен модуль: {'Углеродный' if detected_mode=='carbon' else 'Органический'}")

if st.session_state.data is None:
    st.session_state.data = parse_carbon_data(None) if st.session_state.mode == "carbon" else parse_organic_data(None)

apply_global_styles(mode=st.session_state.mode)
active_nav = render_sidebar(mode=st.session_state.mode, source_name=st.session_state.source_name)

if st.session_state.mode == "carbon":
    render_carbon_dashboard(st.session_state.data)
else:
    render_organic_dashboard(st.session_state.data)
