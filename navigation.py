import streamlit as st
import pandas as pd

def render_sidebar(df: pd.DataFrame = None):
    """Боковая панель с безопасной фильтрацией."""
    st.sidebar.markdown("""
        <div style="text-align: center; padding: 8px 0;">
            <h2 style="color: #34d399; margin: 0;">🌾 AgroFresh</h2>
            <p style="color: #a7f3d0; font-size: 0.8rem; margin: 0;">Carbon & Yield Intelligence</p>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    selected_page = st.sidebar.radio(
        "Навигация по разделам:",
        [
            "📊 Главный Дашборд & Бублики",
            "🌱 Углеродный след & Выгода",
            "⛅ Климат и Урожайность",
            "📑 Данные и Статистика (95% CI)",
            "📥 Экспорт отчетов"
        ]
    )
    st.sidebar.markdown("---")
    
    # Фильтрация по ID, если датасет передан
    filtered_df = df
    if df is not None and not df.empty and "ID" in df.columns:
        min_id = int(df["ID"].min())
        max_id = int(df["ID"].max())
        
        st.sidebar.subheader("🔍 Фильтр выборки")
        if min_id < max_id:
            id_range = st.sidebar.slider("Диапазон номеров полей:", min_value=min_id, max_value=max_id, value=(min_id, max_id))
            filtered_df = df[(df["ID"] >= id_range[0]) & (df["ID"] <= id_range[1])]
        
        if "Risk_1_R" in df.columns:
            risks = sorted(df["Risk_1_R"].dropna().unique().tolist())
            selected_risks = st.sidebar.multiselect("Уровень риска (1-R):", risks, default=risks)
            if selected_risks:
                filtered_df = filtered_df[filtered_df["Risk_1_R"].isin(selected_risks)]
                
        st.sidebar.caption(f"Отобрано полей: **{len(filtered_df)}** из **{len(df)}**")
        
    return selected_page, filtered_df
