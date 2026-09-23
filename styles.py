"""
styles.py - Стили и UI-компоненты для AgroFresh
Цветовая палитра: Изумрудно-зеленая (#1e7655, #143c2d), Мятная (#dcefe6), Графика (#4e91ad, #a93d72, #e49a27)
"""

CARBON_DASHBOARD_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
  --bg: #eef4f1;
  --card: #ffffff;
  --ink: #20312b;
  --muted: #71817b;
  --green: #1e7655;
  --green2: #2d8b68;
  --mint: #dcefe6;
  --blue: #4e91ad;
  --violet: #a93d72;
  --amber: #e49a27;
  --line: #e2e9e5;
  --shadow: 0 8px 28px rgba(25, 55, 43, 0.08);
}

html, body, [class*="css"] {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: var(--ink);
}

.stApp {
  background: linear-gradient(180deg, #edf4f1 0%, #f6f9f7 100%);
}

/* Верхняя карточка-заголовок */
.hero-header {
  background: transparent;
  padding: 10px 0 20px;
}
.eyebrow {
  color: #5b8072;
  font-weight: 800;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.main-title {
  font-size: 28px;
  font-weight: 850;
  color: #143c2d;
  letter-spacing: -0.03em;
  margin: 4px 0;
}
.subtitle {
  color: var(--muted);
  font-size: 13px;
}

/* KPI Карточки */
.kpi-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin: 15px 0 22px;
}
.kpi-card {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 16px 18px;
  box-shadow: var(--shadow);
}
.kpi-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--muted);
}
.kpi-value {
  font-size: 26px;
  font-weight: 850;
  color: #143c2d;
  margin-top: 6px;
}
.kpi-hint {
  font-size: 11px;
  color: #8a9993;
  margin-top: 4px;
}

/* Карточки графиков */
.chart-card {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 18px;
  box-shadow: var(--shadow);
  margin-bottom: 16px;
}
.chart-head h3 {
  font-size: 15px;
  font-weight: 800;
  margin: 0 0 4px;
  color: #1f342d;
}
.chart-head p {
  font-size: 11px;
  color: var(--muted);
  margin: 0 0 10px;
}

/* Блоки формул и подмодулей F1–F6 */
.calc-module-card {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 16px;
  box-shadow: var(--shadow);
  margin-bottom: 12px;
}
.calc-module-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 800;
  color: #1e7655;
  margin-bottom: 8px;
}
.calc-desc {
  font-size: 12px;
  color: var(--muted);
  margin-bottom: 12px;
  line-height: 1.45;
}
.submod-chip {
  background: #fbfdfc;
  border: 1px solid #e3ebe7;
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 8px;
}
.submod-header {
  font-size: 12px;
  font-weight: 700;
  color: #284a3e;
}
.submod-formula {
  font-size: 10px;
  color: #81908a;
  margin-bottom: 6px;
}

/* Таблицы */
.custom-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}
.custom-table th {
  padding: 8px 10px;
  border-bottom: 1px solid #edf1ef;
  font-size: 10px;
  color: #7a8984;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  text-align: left;
}
.custom-table td {
  padding: 9px 10px;
  border-bottom: 1px solid #edf1ef;
}
.status-badge {
  color: #1e7655;
  font-weight: 800;
}
</style>
"""

def apply_carbon_styles():
    import streamlit as st
    st.markdown(CARBON_DASHBOARD_CSS, unsafe_allow_html=True)