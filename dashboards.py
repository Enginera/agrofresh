    # --- Вкладка 4: ЗАЩИТА РАСТЕНИЙ ---
    elif page_name == "Защита растений":
        st.subheader(f"Мониторинг защиты растений — 🛡️ {selected_field}")
        st.metric("Active сессии контроля", len(df_active))
        st.metric("Процент здоровых культур", "92%")
        st.markdown("**Динамика коэффициента рисков Ravg по годам**")
        fig_prot = go.Figure(go.Scatter(x=df_active["Год"], y=df_active["Ravg"], mode='lines+markers', line=dict(shape='spline', color='#C62828', width=3)))
        fig_prot.update_layout(height=300, plot_bgcolor='white')
        fig_prot.update_xaxes(type='category')
        st.plotly_chart(fig_prot, width='stretch')
    # --- Вкладка 5: УРОЖАЙНОСТЬ И КАЧЕСТВО ---
    elif page_name == "Урожайность и качество":
        st.subheader(f"Управление урожайностью и качеством продукции — 🌾 {selected_field}")
        st.markdown(f"<div class='metric-card' style='margin-bottom:10px; height:auto !important; display:block !important;'><b>Общая урожайность</b><h2>{df_active['Урожайность'].sum():.2f} т</h2></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card' style='margin-bottom:10px; height:auto !important; display:block !important;'><b>Максимальный сбор</b><h2>{df_active['Урожайность'].max():.2f} т/га</h2></div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-card' style='margin-bottom:20px; height:auto !important; display:block !important;'><b>Коэффициент качества</b><h2>92%</h2><span style='color:blue;'>Выше среднего</span></div>", unsafe_allow_html=True)
        
        st.subheader("Детализированные отчеты о качестве партий 📋")
        df_quality = pd.DataFrame({"Продукт": ["Пшеница", "Кукуруза", "Соя"], "Партия": ["2026-A", "2026-B", "2026-C"], "Влажность": ["14%", "15%", "11%"], "Статус": ["Отлично", "Хорошо", "Отлично"]})
        st.dataframe(df_quality, width='stretch')
        
        st.subheader("Распределение урожайности по годам 📊")
        fig_factors = px.bar(df_active, x="Год", y="Урожайность", text_auto='.2f', color_discrete_sequence=['#2E7D32'])
        fig_factors.update_layout(height=280, plot_bgcolor='white', xaxis_title="", yaxis_title="т/га")
        fig_factors.update_xaxes(type='category')
        st.plotly_chart(fig_factors, width='stretch')

    # --- Вкладка 6: УГЛЕРОДНЫЙ СЛЕД ---
    elif page_name == "Углеродный след":
        st.subheader(f"Моделирование баланса декарбонизации — ☁️ {selected_field}")
        st.metric("Чистый след Cnet (Средний)", f"{df_active['Cnet'].mean():.2f} т")
        st.metric("Внесение Cinputs (Среднее)", f"{df_active['Cinputs'].mean():.2f} кг")
        st.metric("Целевой прогноз секвестрации", "Выполнено 🌳")
        
        fig_cnet = px.area(df_active, x="Год", y="Cnet", title="Динамическая модель изменения чистого следа Cnet", color_discrete_sequence=['#78909C'])
        fig_cnet.update_layout(plot_bgcolor='white', height=400)
        fig_cnet.update_xaxes(type='category')
        st.plotly_chart(fig_cnet, width='stretch')
    # --- Вкладка 7: ПРИНЯТИЕ РЕШЕНИЙ ---
    elif page_name == "Принятие решений":
        st.subheader(f"Сводная расчетная матрица севооборота — 💡 {selected_field}")
        st.markdown("Все строки и столбцы выгружены на основе структуры ТЗ:")
        available_cols = [c for c in ["Год", "Культура", "Урожайность", "Cinputs", "Cnet", "Ravg", "Эффективность"] if c in df_active.columns]
        df_display = df_active[available_cols].copy()
        rename_display = {"Год": "Год агросрока", "Культура": "Культура", "Урожайность": "Урожайность (т/га)", "Cinputs": "Внесение Cinputs (кг)", "Cnet": "Чистый след Cnet", "Ravg": "Коэффициент Rave", "Эффективность": "Индекс эффективности (E)"}
        df_display = df_display.rename(columns=rename_display)
        if "Индекс эффективности (E)" in df_display.columns:
            st.dataframe(df_display.style.format({"Индекс эффективности (E)": "{:.4f}"}), width='stretch')
        else:
            st.dataframe(df_display, width='stretch')
