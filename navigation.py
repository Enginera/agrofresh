import streamlit as st
import pandas as pd

def render_sidebar(df: pd.DataFrame = None):
    """Боковая панель по структуре макетов."""
    st.sidebar.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; padding: 6px 0 14px 0;">
            <div style="background:#0f4432; border:2px solid #34d399; border-radius:50%; width:38px; height:38px; display:flex; align-items:center; justify-content:center; font-size:18px; color:#34d399; font-weight:bold;">C</div>
            <div>
                <div style="color: #ffffff; font-weight: 700; font-size: 0.85rem; line-height: 1.2;">Модуль углеродно-нейтрального земледелия</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    # Синхронизация активной страницы
    if "current_page" not in st.session_state:
        st.session_state.current_page = "🔷 Дашборд"
        
    pages = [
        "🔷 Дашборд",
        "⏹ Параметры",
        "🔀 Функции F1–F6",
        "⚪ Сводный анализ"
    ]
    
    # Радиокнопки сайдбара
    curr_idx = pages.index(st.session_state.current_page) if st.session_state.current_page in pages else 0
    selected_page = st.sidebar.radio("Разделы:", pages, index=curr_idx)
    st.session_state.current_page = selected_page

    # Подменю для выбора функции напрямую
    if selected_page == "🔀 Функции F1–F6":
        st.sidebar.markdown("---")
        fn_options = [
            "📋 Общий экран функций",
            "F1 - Планирования севооборота",
            "F2 - Управления удобрениями и обработкой почвы",
            "F3 - Мониторинга и управления защитой растений",
            "F4 - Управления урожайностью и качеством продукции",
            "F5 - Оценки углеродного следа, прогнозирования...",
            "F6 - Принятия стратегических решений"
        ]
        
        if "active_fn" not in st.session_state:
            st.session_state.active_fn = "📋 Общий экран функций"
            
        fn_idx = fn_options.index(st.session_state.active_fn) if st.session_state.active_fn in fn_options else 0
        selected_sub_fn = st.sidebar.selectbox("Экран функции:", fn_options, index=fn_idx)
        st.session_state.active_fn = selected_sub_fn
    else:
        selected_sub_fn = None

    st.sidebar.markdown("---")
    
    # Фильтр по выборке
    filtered_df = df
    if df is not None and not df.empty and "ID" in df.columns:
        min_id = int(df["ID"].min())
        max_id = int(df["ID"].max())
        
        st.sidebar.markdown("<div style='color:#a7f3d0; font-weight:600; font-size:0.85rem; margin-bottom:5px;'>🔍 Выборка полей</div>", unsafe_allow_html=True)
        if min_id < max_id:
            id_range = st.sidebar.slider("Диапазон полей:", min_value=min_id, max_value=max_id, value=(min_id, max_id))
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