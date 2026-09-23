import streamlit as st
from dashboards import render_carbon_neutral_dashboard

st.set_page_config(
    page_title="AgroFresh — Углеродно-нейтральное земледелие",
    page_icon="🌱",
    layout="wide"
)

# Сайдбар-навигация
menu_choice = st.sidebar.radio(
    "Разделы платформы",
    ["🌱 Углеродно-нейтральное земледелие", "📦 Каталог продукции", "🛒 Заказы", "👤 Личный кабинет"]
)

if menu_choice == "🌱 Углеродно-нейтральное земледелие":
    render_carbon_neutral_dashboard()