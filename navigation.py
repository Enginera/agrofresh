import streamlit as st
import pandas as pd

def render_sidebar(df: pd.DataFrame = None):
    """Боковая панель по структуре HTML-шаблона."""
    st.sidebar.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 24px;">
            <div style="width:34px; height:34px; background:#9bc2a7; color:#173b2a; border-radius:9px; display:grid; place-items:center; font-weight:900; font-size:16px;">C</div>
            <div style="color: #ffffff; font-weight: 800; font-size: 0.95rem; line-height: 1.15;">Модуль<br>углеродно-нейтрального<br>земледелия</div>
        </div>
    """, unsafe_allow_html=True)
    
    selected_page = st.sidebar.radio(
        "Навигация:",
        [
            "◈ Дашборд",
            "▦ Параметры",
            "⌘ Функции F1–F6",
            "◌ Сводный анализ"
        ]
    )
    
    st.sidebar.markdown("---")
    
    # Фильтрация по выборке
    filtered_df = df
    if df is not None and not df.empty and "ID" in df.columns:
        min_id = int(df["ID"].min())
        max_id = int(df["ID"].max())
        
        st.sidebar.markdown("<div style='color:#cfe0d6; font-weight:700; font-size:0.8rem; text-transform:uppercase; margin-bottom:4px;'>Диапазон номеров полей</div>", unsafe_allow_html=True)
        if min_id < max_id:
            id_range = st.sidebar.slider("", min_value=min_id, max_value=max_id, value=(min_id, max_id))
            filtered_df = df[(df["ID"] >= id_range[0]) & (df["ID"] <= id_range[1])]
        
        if "Risk_1_R" in df.columns:
            risks = sorted(df["Risk_1_R"].dropna().unique().tolist())
            selected_risks = st.sidebar.multiselect("Уровень риска (1-R):", risks, default=risks)
            filtered_df = filtered_df[filtered_df["Risk_1_R"].isin(selected_risks)]
                
        st.sidebar.caption(f"Отобрано полей: **{len(filtered_df)}** из **{len(df)}**")

    st.sidebar.markdown("""
        <div class="sidebar-note">
            <b>Источник</b><br>
            F2.xlsx · 6 расчётных функций<br>
            03.09.2026
        </div>
    """, unsafe_allow_html=True)
        
    return selected_page, filtered_df