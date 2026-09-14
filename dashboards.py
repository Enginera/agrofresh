import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from styles import render_card, render_top_header

ECO_GREENS = ["#10b981", "#059669", "#34d399", "#6ee7b7", "#047857", "#a7f3d0", "#022c22"]

def fmt(val, precision=2, suffix=""):
    """Форматирует числовые значения под плашки карточек."""
    if pd.isna(val) or val is None:
        return "—"
    if precision == 0:
        return f"{val:,.0f}{suffix}".replace(",", " ")
    return f"{val:,.{precision}f}{suffix}".replace(",", " ")

# ======================= ЭКРАНЫ ФУНКЦИЙ F1 - F6 ======================= #

def render_fn_menu():
    """Главный экран каталога функций F1–F6 (плитки-кнопки по макету)."""
    render_top_header()
    st.markdown('<div class="section-title">Расчётные функции углеродно-нейтрального земледелия</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("F1 – «Планирования севооборота»", use_container_width=True):
            st.session_state.active_fn = "F1 - Планирования севооборота"
            st.rerun()
        st.write("")
        if st.button("F2 – «Управления удобрениями и обработкой почвы»", use_container_width=True):
            st.session_state.active_fn = "F2 - Управления удобрениями и обработкой почвы"
            st.rerun()
        st.write("")
        if st.button("F3 – «Мониторинга и управления защитой растений»", use_container_width=True):
            st.session_state.active_fn = "F3 - Мониторинга и управления защитой растений"
            st.rerun()
            
    with c2:
        if st.button("F4 – «Управления урожайностью и качеством продукции»", use_container_width=True):
            st.session_state.active_fn = "F4 - Управления урожайностью и качеством продукции"
            st.rerun()
        st.write("")
        if st.button("F5 – «Оценки углеродного следа, прогнозирования...»", use_container_width=True):
            st.session_state.active_fn = "F5 - Оценки углеродного следа, прогнозирования..."
            st.rerun()
        st.write("")
        if st.button("F6 – «Принятия стратегических решений»", use_container_width=True):
            st.session_state.active_fn = "F6 - Принятия стратегических решений"
            st.rerun()

def render_back_button():
    """Кнопка возврата к общему списку функций."""
    if st.button("⬅ Назад ко всем функциям F1–F6"):
        st.session_state.active_fn = "📋 Общий экран функций"
        st.rerun()

def render_f1(df: pd.DataFrame):
    """Экран F1 - Планирования севооборота (точно по Скриншоту 6)."""
    render_back_button()
    render_top_header('F1 - "Планирования севооборота"')
    c1, c2 = st.columns(2)
    with c1:
        v1 = df.get("C_Sequestered", pd.Series([2.14])).mean()
        render_card("Секвестрация углерода при выборе с/х культур в севообороте, Csequestered (т CO₂-экв./га).", fmt(v1))
        
        v3 = df.get("E_Rotation_Efficiency", pd.Series([0.85])).mean()
        render_card("Интегральный коэффициент эффективности севооборота E", fmt(v3, 3))
    with c2:
        v2 = df.get("C_Net", pd.Series([0.65])).mean()
        render_card("Расчет показателя углеродного следа за период агросрока Cnet (т CO₂-экв./га)", fmt(v2))

def render_f2(df: pd.DataFrame):
    """Экран F2 - Управления удобрениями и обработкой почвы (точно по Скриншоту 5)."""
    render_back_button()
    render_top_header('F2 - "Управления удобрениями и обработкой почвы"')
    c1, c2 = st.columns(2)
    with c1:
        render_card("Коэффициент температуру почвы, Ktemp", fmt(df.get("K_Temp_Soil", pd.Series([1.12])).mean()))
        render_card("Влажность почвы фактическая, Wфакт, %", fmt(df.get("W_Fact", pd.Series([24.5])).mean(), 1, " %"))
        render_card("Влажность почвы оптимальная, Wопт, %", fmt(df.get("W_Opt", pd.Series([25.0])).mean(), 1, " %"))
        render_card("Индекс агротехнического воздействия Iат", fmt(df.get("I_Agrotech", pd.Series([1.18])).mean()))
    with c2:
        render_card("Коэффициент увлажнения, Kвлаги", fmt(df.get("K_Moisture", pd.Series([1.05])).mean()))
        render_card("Влажность почвы критическая, Wкрит, %", fmt(df.get("W_Crit", pd.Series([13.8])).mean(), 1, " %"))
        render_card("Углеродный след от внесения пестицидов/удобрений (CFпестицидов)Cfудобрений (kg CO2 - eq/t)", fmt(df.get("CF_Leaf_Operations", pd.Series([230])).mean(), 1))
        render_card("Секвестрация углерода от технологической операции», ΔСобработка, (kg CO2-eq/га)", fmt(df.get("Delta_C_Tillage", pd.Series([94.2])).mean(), 1))

def render_f3(df: pd.DataFrame):
    """Экран F3 - Мониторинга и управления защитой растений (точно по Скриншоту 4)."""
    render_back_button()
    render_top_header('F3 - "Мониторинга и управления защитой растений"')
    c1, c2 = st.columns(2)
    with c1:
        render_card("Уровень заражения растений, (%), УЗ", fmt(df.get("Infection_Level_UZ", pd.Series([8.4])).mean(), 1, " %"))
        render_card("Индекс повреждения, (интегральная оценка ущерба), ИПВ", fmt(df.get("Damage_Index_IPV", pd.Series([0.184])).mean(), 3))
        render_card("Усредненная дозировка препаратов (фунгицид/ пестицид) влияющая на углеродный след, (л/га), D", fmt(df.get("Dosage_D", pd.Series([1.65])).mean(), 2, " л/га"))
    with c2:
        render_card("Интенсивность поражения, (%), ИП", fmt(df.get("Infestation_Rate_IP", pd.Series([4.2])).mean(), 1, " %"))
        render_card("Интервал между обработками в рамках стратегии защиты растений, (дни), I", fmt(df.get("Interval_Days_I", pd.Series([14])).mean(), 0, " дн."))
        render_card("Расчет углеродного следа от мероприятий защиты растений (за агросрок), (kg CO2-eq/га), Cсезон", fmt(df.get("CF_Protection_Season", pd.Series([42.8])).mean(), 1))

def render_f4(df: pd.DataFrame):
    """Экран F4 - Управления урожайностью и качеством продукции (точно по Скриншоту 3)."""
    render_back_button()
    render_top_header('F4 - "Управления урожайностью и качеством продукции"')
    c1, c2 = st.columns(2)
    with c1:
        render_card("Общие потери, (т/га), ОП", fmt(df.get("OP_Total_Losses", pd.Series([1.85])).mean(), 2, " т/га"))
        render_card("Финальная урожайность, (т/га), Уфин", fmt(df.get("F5_Yield_Forecast", pd.Series([4.85])).mean(), 2, " т/га"))
        render_card("Показатель углеродного след технологической операции, (кг -CO2 экв./ га), СFу.след", fmt(df.get("CF_Tech_Operation", pd.Series([52.0])).mean(), 1))
        render_card("Показатель углеродного следа на тонну зерна получаемого в процессе уборки, (кг CO2 -экв./т), СFитог", fmt(df.get("CF_Grain_Total", pd.Series([74.3])).mean(), 1))
    with c2:
        render_card("Секвестрация углерода от послеуборочных остатков (соломы), (кг -CO2 экв./га), ΔСсолом", fmt(df.get("Delta_C_Straw", pd.Series([265.0])).mean(), 1))
        render_card("Секвестрация углерода за счёт пожнивных остатков, (кг - CO2 экв./га), SCO2,", fmt(df.get("S_CO2_Residues", pd.Series([180.4])).mean(), 1))
        render_card("Коэффициент качества продукции от 100% продуктивных свойств,(%), QF", fmt(df.get("QF_Quality", pd.Series([94.5])).mean(), 1, " %"))

def render_f5(df: pd.DataFrame):
    """Экран F5 - Оценки углеродного следа, прогнозирования... (точно по Скриншоту 2)."""
    render_back_button()
    render_top_header('F5 - "Оценки углеродного следа, прогнозирования, статистики, учета и отчетности"')
    c1, c2 = st.columns(2)
    with c1:
        render_card("Углеродоемкость (т CO2/га) У CO2", fmt(df.get("B_Carbon", pd.Series([68.4])).mean(), 2, " т/га"))
        render_card("Эмиссия операции вносящая наибольший вклад в углеродный след, (кг CO2-экв/га) Э CO2", fmt(df.get("CF_Leaf_Operations", pd.Series([482.0])).max(), 1))
        render_card("Общие валовые выбросы углерода, (кг CO2-экв/га) OCO2", fmt(df.get("CF_Harvest", pd.Series([64.2])).mean(), 1))
        render_card("Эмиссия углерода от технологии получения с/х продукции, (кг CO2-экв/га), Cem", fmt(df.get("C_Total_Agrosrok", pd.Series([850.0])).mean(), 1))
    with c2:
        render_card("Показатель углеродного следа для i-го агросрока, (кг CO2-экв/га), Ctotal", fmt(df.get("C_Total_Agrosrok", pd.Series([1240.0])).mean(), 1))
        render_card("Изменение углеродного следа (Сводный отчет), минимальный показатель", fmt(df.get("Net_Carbon_Footprint", pd.Series([0.65])).min(), 2))
        render_card("Анализ эффективности с учетом секвестрации, (тыс. руб/ га)", fmt(df.get("B_Econ", pd.Series([80200])).mean() / 1000, 1, " тыс.₽"))

def render_f6(df: pd.DataFrame):
    """Экран F6 - Принятия стратегических решений (точно по Скриншоту 1)."""
    render_back_button()
    render_top_header('F6 - "Принятия стратегических решений"')
    c1, c2 = st.columns(2)
    with c1:
        render_card("Коэффициент эффективности углеродной нейтральности с учётом стоимости мероприятий, К эф", fmt(df.get("F6_1_Efficiency", pd.Series([12.4])).mean()))
        render_card("Индекс приоритета, на 1 рубль затрат производства приходиться поглощения , (кг CO2-экв/ руб_) за год, PI", fmt(df.get("PI_Priority_Index", pd.Series([3.14])).mean(), 4))
        render_card("Расчет средней углеродоёмкости единицы продукции по заданным полям, (кг CO2 -экв./т) С поле", fmt(df.get("Carbon_Intensity_Unit", pd.Series([5.8])).mean(), 1))
        render_card("Общие потери, (т/га) , ОП", fmt(df.get("OP_Total_Losses", pd.Series([2.1])).mean(), 2, " т/га"))
    with c2:
        render_card("Прогноз урожайности (по температуре и осадкам) (кг/га) Y net", fmt(df.get("F5_Yield_Forecast", pd.Series([4.85])).mean() * 1000, 0, " кг/га"))
        render_card("Интегральный коэффициент эффективности севооборота E", fmt(df.get("E_Rotation_Efficiency", pd.Series([0.82])).mean(), 3))
        render_card("Себестоимость по заданным полям в агросезон (тыс руб/га)", fmt(df.get("Cost_Price_Season", pd.Series([54.0])).mean(), 0, " тыс.₽"))
        render_card("Затраты на удобрения по заданным полям с учетом углеродной нейтральности , (тыс руб/га) за агросезон, З уд.агросрок", fmt(df.get("Fertilizer_Costs_Neutral", pd.Series([19.5])).mean(), 0, " тыс.₽"))

# ======================= ГРАФИЧЕСКИЙ ДАШБОРД ======================= #

def render_dashboard_visuals(df: pd.DataFrame):
    """Экран 1: Сводный Дашборд."""
    render_top_header("Сводный аналитический дашборд")
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_card("🌿 Выгода CO2 (Bcarbon)", fmt(df.get("B_Carbon", pd.Series([0])).mean(), 2, " т CO2/га"))
    with k2:
        render_card("💰 Затраты (C)", fmt(df.get("C_Total_Costs", pd.Series([0])).mean(), 0, " ₽/га"))
    with k3:
        render_card("⚡ Эффективность (K эф / F6)", fmt(df.get("F6_1_Efficiency", pd.Series([0])).mean()))
    with k4:
        render_card("🛡️ Уровень риска (1-R)", fmt(df.get("Risk_1_R", pd.Series([0])).mean()))

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if "Risk_1_R" in df.columns:
            r_counts = df["Risk_1_R"].value_counts().reset_index()
            r_counts.columns = ["Риск", "Полей"]
            r_counts["Риск_Имя"] = "Риск " + r_counts["Риск"].astype(str)
            fig1 = go.Figure(data=[go.Pie(
                labels=r_counts["Риск_Имя"],
                values=r_counts["Полей"],
                hole=0.60,
                marker=dict(colors=ECO_GREENS, line=dict(color='#022c22', width=2)),
                textinfo="percent+label",
                textposition="outside",
                showlegend=False
            )])
            fig1.update_layout(
                title=dict(text="<b>Распределение полей по рискам (1-R)</b>", font=dict(color="#a7f3d0", size=15), x=0.5),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
                height=350,
                margin=dict(l=20, r=20, t=50, b=20),
                annotations=[dict(text="РИСКИ<br><b>1-R</b>", x=0.5, y=0.5, font_size=13, font_color="#34d399", showarrow=False)]
            )
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        h_sum = df["CF_Harvest"].abs().sum() if "CF_Harvest" in df.columns else 100
        l_sum = df["CF_Leaf_Operations"].abs().sum() if "CF_Leaf_Operations" in df.columns else 100
        f_sum = df["Fertilizer_Costs_Neutral"].abs().sum() if "Fertilizer_Costs_Neutral" in df.columns else 50
        
        balance_df = pd.DataFrame({
            "Компонент": ["CF уборки", "CF операций на листе", "Удобрения с нейтр."],
            "Объем": [h_sum, l_sum, f_sum]
        })
        fig2 = go.Figure(data=[go.Pie(
            labels=balance_df["Компонент"],
            values=balance_df["Объем"],
            hole=0.60,
            marker=dict(colors=["#059669", "#10b981", "#34d399"], line=dict(color='#022c22', width=2)),
            textinfo="percent+label",
            textposition="outside",
            showlegend=False
        )])
        fig2.update_layout(
            title=dict(text="<b>Вклад операций в углеродный след</b>", font=dict(color="#a7f3d0", size=15), x=0.5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            height=350,
            margin=dict(l=20, r=20, t=50, b=20),
            annotations=[dict(text="ЭМИССИИ<br><b>CO2</b>", x=0.5, y=0.5, font_size=13, font_color="#34d399", showarrow=False)]
        )
        st.plotly_chart(fig2, use_container_width=True)

    c_scat, c_top = st.columns([1.2, 1])
    with c_scat:
        if "C_Total_Costs" in df.columns and "B_Carbon" in df.columns:
            fig = px.scatter(
                df,
                x="C_Total_Costs",
                y="B_Carbon",
                size="F6_1_Efficiency" if "F6_1_Efficiency" in df.columns else None,
                color="Risk_1_R" if "Risk_1_R" in df.columns else None,
                labels={
                    "C_Total_Costs": "Общие затраты (руб./га)",
                    "B_Carbon": "Выгода CO2 (т/га)",
                    "Risk_1_R": "Риск (1-R)"
                },
                color_continuous_scale=["#022c22", "#059669", "#10b981", "#34d399", "#a7f3d0"],
                title="Затраты (C) vs Выгода (Bcarbon)"
            )
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(6, 78, 59, 0.15)", font=dict(color="#ffffff"), height=380)
            st.plotly_chart(fig, use_container_width=True)
    with c_top:
        if "B_Carbon" in df.columns and "ID" in df.columns:
            top10 = df.sort_values(by="B_Carbon", ascending=False).head(10).copy()
            top10["Поле"] = "Поле № " + top10["ID"].astype(str)
            fig_bar = px.bar(
                top10,
                x="B_Carbon",
                y="Поле",
                orientation="h",
                color="B_Carbon",
                color_continuous_scale=["#059669", "#10b981", "#34d399"],
                title="ТОП-10 полей по выгоде CO2"
            )
            fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(6, 78, 59, 0.1)", font=dict(color="#ffffff"), yaxis=dict(autorange="reversed"), height=380)
            st.plotly_chart(fig_bar, use_container_width=True)