import streamlit as st
import pandas as pd

def render_sidebar(df: pd.DataFrame = None):
    """Боковая панель по макетам системы."""
    st.sidebar.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; padding: 6px 0 16px 0;">
            <div style="background:#0f4432; border:2px solid #34d399; border-radius:50%; width:38px; height:38px; display:flex; align-items:center; justify-content:center; font-size:18px; color:#34d399; font-weight:bold;">C</div>
            <div>
                <div style="color: #ffffff; font-weight: 700; font-size: 0.85rem; line-height: 1.2;">Модуль углеродно-нейтрального земледелия</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    selected_page = st.sidebar.radio(
        "Навигация:",
        [
            "🔷 Дашборд",
            "⏹ Параметры",
            "🔀 Функции F1–F6",
            "⚪ Сводный анализ"
        ]
    )
    
    selected_sub_fn = None
    if selected_page == "🔀 Функции F1–F6":
        st.sidebar.markdown("---")
        selected_sub_fn = st.sidebar.selectbox(
            "Выберите функцию:",
            [
                "Обзор всех функций (Меню)",
                "F1 - Планирование севооборота",
                "F2 - Управление удобрениями и обработкой почвы",
                "F3 - Мониторинг и управление защитой растений",
                "F4 - Управление урожайностью и качеством продукции",
                "F5 - Оценка углеродного следа, отчетность",
                "F6 - Принятие стратегических решений"
            ]
        )

    st.sidebar.markdown("---")
    
    filtered_df = df
    if df is not None and not df.empty and "ID" in df.columns:
        min_id = int(df["ID"].min())
        max_id = int(df["ID"].max())
        
        st.sidebar.markdown("<div style='color:#a7f3d0; font-weight:600; font-size:0.85rem; margin-bottom:5px;'>🔍 Выборка полей</div>", unsafe_allow_html=True)
        if min_id < max_id:
            id_range = st.sidebar.slider("Номера полей:", min_value=min_id, max_value=max_id, value=(min_id, max_id))
            filtered_df = df[(df["ID"] >= id_range[0]) & (df["ID"] <= id_range[1])]
        
        if "Risk_1_R" in df.columns:
            risks = sorted(df["Risk_1_R"].dropna().unique().tolist())
            selected_risks = st.sidebar.multiselect("Уровень риска (1-R):", risks, default=risks)
            filtered_df = filtered_df[filtered_df["Risk_1_R"].isin(selected_risks)]
                
        st.sidebar.caption(f"Отобрано полей: **{len(filtered_df)}** из **{len(df)}**")

    st.sidebar.markdown("""
        <div class="sidebar-footer">
            <b>Источник</b><br>
            F2.xlsx · 6 расчётных функций<br>
            03.09.2026
        </div>
    """, unsafe_allow_html=True)
        
    return selected_page, selected_sub_fn, filtered_df