# HTML-референс 1: Углеродно-нейтральное земледелие
CARBON_HTML = r'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Модуль углеродно-нейтрального земледелия по 5 полям</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
<style>
:root{
  --bg:#eef4f1; --card:#fff; --ink:#20312b; --muted:#71817b;
  --green:#1e7655; --green2:#2d8b68; --mint:#dcefe6;
  --blue:#4e91ad; --violet:#a93d72; --amber:#e49a27;
  --line:#e2e9e5; --shadow:0 8px 28px rgba(25,55,43,.08);
}
*{box-sizing:border-box}
body{margin:0;background:linear-gradient(180deg,#edf4f1 0%,#f6f9f7 100%);color:var(--ink);font-family:Inter,Segoe UI,Arial,sans-serif}
.app{display:grid;grid-template-columns:260px 1fr;min-height:100vh}
.sidebar{background:#143c2d;color:#dcece5;padding:24px 18px;position:sticky;top:0;height:100vh}
.brand{display:flex;gap:12px;align-items:center;padding:6px 8px 26px}
.logo{width:42px;height:42px;border-radius:12px;background:#2f8c69;display:grid;place-items:center;font-size:21px}
.brand b{display:block;font-size:14px;letter-spacing:.02em}.brand span{font-size:11px;color:#9db9ad}
.nav{display:grid;gap:8px}.nav a{padding:12px 14px;border-radius:11px;color:#c8ddd5;text-decoration:none;font-size:13px}.nav a.active,.nav a:hover{background:#1d5942;color:#fff}
.side-note{margin-top:auto;padding:14px;color:#91ada2;font-size:11px;line-height:1.5;border-top:1px solid rgba(255,255,255,.1)}
main{padding:28px 32px 42px;max-width:1600px;width:100%;margin:auto}
.top{display:flex;justify-content:space-between;gap:20px;align-items:flex-start;margin-bottom:20px}
.eyebrow{color:#5b8072;font-weight:800;font-size:12px;letter-spacing:.12em;text-transform:uppercase}
h1{font-size:30px;margin:7px 0 5px;letter-spacing:-.03em}.subtitle{color:var(--muted);font-size:13px}
.actions{display:flex;gap:9px;align-items:center}.btn{border:1px solid var(--line);background:#fff;border-radius:10px;padding:10px 13px;color:var(--ink);font-weight:700;cursor:pointer}.btn.primary{background:var(--green);border-color:var(--green);color:#fff}.btn:hover{transform:translateY(-1px)}
.filters{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px;box-shadow:var(--shadow);display:grid;grid-template-columns:2fr 1.25fr 1fr auto;gap:12px;align-items:end}
.field label{display:block;font-size:10px;text-transform:uppercase;letter-spacing:.08em;font-weight:800;color:#7a8984;margin:0 0 7px}
.select{min-height:43px;border:1px solid #dce5e0;border-radius:10px;background:#fbfdfc;padding:7px 9px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.chip{display:inline-flex;gap:5px;align-items:center;padding:6px 8px;border-radius:8px;background:#e8f2ed;color:#255d48;font-size:12px;font-weight:700}
.chip input{accent-color:var(--green)}
select{width:100%;border:1px solid #dce5e0;background:#fbfdfc;border-radius:10px;padding:11px;font-size:13px;color:var(--ink)}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0}
.kpi{background:#fff;border:1px solid var(--line);border-radius:16px;padding:17px 18px;box-shadow:var(--shadow)}.kpi .label{font-size:12px;color:var(--muted)}.kpi .value{font-size:25px;font-weight:850;margin-top:7px}.kpi .hint{font-size:10px;color:#8a9993;margin-top:4px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px;box-shadow:var(--shadow);min-width:0}
.card.wide{grid-column:1/-1}.head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}.head h2{font-size:16px;margin:0 0 5px}.head p{margin:0;color:var(--muted);font-size:11px}
.chartbox{height:310px;margin-top:8px}.wide .chartbox{height:330px}
.tables{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}
table{width:100%;border-collapse:collapse;font-size:12px}th,td{padding:10px;border-bottom:1px solid #edf1ef;text-align:left}th{font-size:10px;color:#7a8984;text-transform:uppercase;letter-spacing:.06em}td.num{text-align:right;font-variant-numeric:tabular-nums}.status{font-weight:800;color:var(--green)}
.functions{margin-top:16px}.functions h2{font-size:17px;margin:0 0 10px}.fn-grid{display:grid;grid-template-columns:1fr 1fr;gap:9px}.fn{background:#fff;border:1px solid var(--line);border-radius:13px;overflow:hidden}.fn button{width:100%;border:0;background:#fff;padding:15px;display:flex;justify-content:space-between;align-items:center;text-align:left;cursor:pointer}.fn .code{font-weight:900;color:#244d3e;margin-right:8px}.fn .name{font-weight:750;font-size:12px}.plus{font-size:18px;color:#6c7c75}.fn-body{display:none;padding:0 15px 14px;color:var(--muted);font-size:11px;line-height:1.55}.fn.open .fn-body{display:block}.fn.open .plus{transform:rotate(45deg)}
.footer{display:flex;justify-content:space-between;margin-top:18px;color:#82908b;font-size:10px}
.submods{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.submod{background:#fff;border:1px solid #e3ebe7;border-radius:12px;padding:12px}.submod h4{margin:0 0 8px;font-size:12px;line-height:1.35;color:#284a3e}.submod .formula{font-size:10px;color:#81908a;margin-bottom:8px}.submod-row{display:grid;grid-template-columns:1fr 120px;gap:8px;align-items:end}.submod label{display:block;font-size:9px;color:#788881;font-weight:800;margin-bottom:4px}.submod input{width:100%;padding:8px 9px;border:1px solid #dce5e0;border-radius:8px;background:#fff;color:var(--ink);font-size:12px}.submod .unit{font-size:9px;color:#8a9892;margin-top:4px}.fn-save{margin-top:12px;border:0;background:#1e7655;color:#fff;border-radius:9px;padding:9px 12px;font-weight:800;cursor:pointer}.fn-status{display:inline-block;margin-left:8px;font-size:10px;color:#2d7658}
.calc-top{margin:18px 0 16px}.calc-top-title{display:flex;justify-content:space-between;align-items:end;gap:12px;margin-bottom:10px}.calc-top-title h2{font-size:18px;margin:0}.calc-top-title p{margin:0;color:var(--muted);font-size:11px}.calc-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.calc-card{background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);overflow:hidden}.calc-head{width:100%;border:0;background:#fff;padding:15px 16px;display:flex;justify-content:space-between;align-items:center;cursor:pointer;text-align:left;color:var(--ink)}.calc-head .code{font-weight:900;color:var(--green);margin-right:8px}.calc-head .name{font-weight:800;font-size:12px}.calc-head .chev{font-size:18px;color:#6b7b74;transition:.2s}.calc-card.open .calc-head .chev{transform:rotate(180deg)}.calc-body{display:none;padding:0 16px 16px;border-top:1px solid #eef2ef;background:#fbfdfc}.calc-card.open .calc-body{display:block}.calc-desc{font-size:11px;color:var(--muted);line-height:1.5;padding:12px 0 10px}.calc-fields{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.calc-field label{display:block;font-size:10px;color:#788881;font-weight:800;margin-bottom:5px}.calc-field input,.calc-field select{width:100%;padding:9px 10px;border:1px solid #dce5e0;border-radius:9px;background:#fff;color:var(--ink)}.calc-actions{display:flex;gap:8px;margin-top:11px}.calc-actions button{border:0;border-radius:9px;padding:9px 12px;cursor:pointer;font-weight:750}.calc-save{background:var(--green);color:#fff}.calc-clear{background:#e9f1ed;color:#255a47}.calc-result{margin-top:10px;padding:10px 12px;border-radius:9px;background:#eaf4ef;font-size:11px;color:#275b48;display:none}.calc-card.open .calc-result.visible{display:block}.calc-top-note{font-size:10px;color:#81918a;margin-top:8px}
.field-stat-card{margin:18px 0 24px;background:linear-gradient(135deg,#174f3a,#236f51);color:#fff;border-radius:18px;padding:22px 24px;box-shadow:0 12px 28px rgba(25,80,58,.16)}
.field-stat-head{display:flex;justify-content:space-between;align-items:flex-start;gap:24px}.field-stat-head h2{margin:3px 0 5px;font-size:20px;color:#fff}.field-stat-head p{margin:0;color:#d5e9df;font-size:13px;max-width:720px}.field-picker{min-width:210px}.field-picker label{display:block;font-size:11px;color:#c9e2d6;margin-bottom:6px}.field-picker select{width:100%;padding:11px 13px;border:1px solid rgba(255,255,255,.25);border-radius:10px;background:#fff;color:#17382b;font-weight:700}
.field-summary{display:grid;grid-template-columns:1.35fr repeat(6,1fr);gap:10px;margin-top:18px}.field-main,.stat{background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:13px}.field-main span{display:block;color:#bfe0d0;font-size:11px;margin-bottom:5px}.field-main b{display:block;font-size:15px;line-height:1.3}.field-main small{display:block;margin-top:5px;color:#d4e8df}.stat span{display:block;font-size:10px;color:#c8dfd5;margin-bottom:7px;line-height:1.25}.stat b{font-size:16px}.stat small{display:block;margin-top:4px;font-size:9px;color:#b9d7ca}.year-list{display:flex;flex-wrap:wrap;gap:5px}.year-list .year-chip{padding:4px 7px;border-radius:8px;background:rgba(255,255,255,.12);font-size:11px;color:#eef8f3;white-space:nowrap}
@media(max-width:1100px){.app{grid-template-columns:1fr}.sidebar{display:none}.filters{grid-template-columns:1fr 1fr}.kpis{grid-template-columns:1fr 1fr}.field-summary{grid-template-columns:repeat(3,1fr)}}
@media(max-width:760px){main{padding:18px}.grid,.tables,.fn-grid,.submods,.calc-grid,.calc-fields{grid-template-columns:1fr}.filters{grid-template-columns:1fr}.kpis{grid-template-columns:1fr 1fr}.top{display:block}.actions{margin-top:12px}.field-stat-head{display:block}.field-picker{margin-top:14px}.field-summary{grid-template-columns:1fr 1fr}}
</style>
</head>
<body>
<div class="app">
<aside class="sidebar">
  <div class="brand"><div class="logo">🌱</div><div><b>Углеродно-нейтральное<br>земледелие</b><span>аналитическая панель</span></div></div>
  <nav class="nav">
    <a class="active" href="#dashboard">Главная</a>
    <a href="#charts">Аналитика</a>
    <a href="#tables">Культура и технология</a>
    <a href="#functions">Расчётные функции</a>
  </nav>
  <div class="side-note">Данные загружены из Excel.<br>Фильтры пересчитывают KPI, таблицы и все диаграммы без перезагрузки страницы.</div>
</aside>
<main id="dashboard">
  <div class="top">
    <div><div class="eyebrow">Аналитическая панель</div><h1>Модуль углеродно-нейтрального земледелия по 5 полям</h1><div class="subtitle">Интерактивная аналитика данных Excel и визуализация ключевых показателей агросезона</div></div>
    <div class="actions"><label class="btn">Загрузить Excel<input id="fileInput" type="file" accept=".xlsx,.xls" hidden></label><button class="btn" id="resetBtn">Сбросить</button><button class="btn primary" onclick="window.print()">Печать</button></div>
  </div>

  <section class="filters">
    <div class="field"><label>Культура</label><div id="cultureFilter" class="select"></div></div>
    <div class="field"><label>Технология</label><div id="techFilter" class="select"></div></div>
    <div class="field"><label>Агросезон</label><select id="season"><option>Текущий расчёт</option><option>Все агросезоны</option></select></div>
    <button class="btn primary" id="applyBtn">Применить</button>
  </section>

<section class="field-stat-card" id="fieldStatsCard">
  <div class="field-stat-head">
    <div>
      <div class="eyebrow">Аналитика по полям</div>
      <h2>Статистика выбранного поля</h2>
      <p>Данные берутся из Excel. Выберите одно из пяти полей — показатели обновятся без перезагрузки страницы.</p>
    </div>
    <div class="field-picker">
      <label for="fieldSelector">Поле</label>
      <select id="fieldSelector">
        <option value="1">Поле 1</option><option value="2">Поле 2</option>
        <option value="3">Поле 3</option><option value="4">Поле 4</option>
        <option value="5">Поле 5</option>
      </select>
    </div>
  </div>
  <div class="field-summary">
    <div class="field-main">
      <span id="fieldName">Поле 1</span>
      <b id="fieldCultures">—</b>
      <small id="fieldTechs">—</small>
    </div>
    <div class="stat year-stat"><span>Ретроспективные данные за лет</span><div id="fsYears" class="year-list">5</div></div>
    <div class="stat"><span>Средняя площадь, га</span><b id="fsArea">—</b></div>
    <div class="stat"><span>Средняя урожайность, т/га</span><b id="fsYield">—</b></div>
    <div class="stat"><span>Удельный след, кг CO₂-экв./т</span><b id="fsCf">—</b></div>
    <div class="stat"><span>Валовые выбросы, кг CO₂-экв./га</span><b id="fsGross">—</b></div>
    <div class="stat"><span>Интегральная эффективность</span><b id="fsEff">—</b><small>F1 · лист F1</small></div>
    <div class="stat"><span>Себестоимость, тыс. руб./га</span><b id="fsCost">—</b></div>
  </div>
</section>

  <section class="calc-top" id="calcTop">
    <div class="calc-top-title"><div><h2>Расчётные функции F1–F6</h2><p>Функции раскрываются сверху; параметры можно вводить и сохранять без перезагрузки страницы.</p></div><div class="calc-top-note">Связано с аналитической панелью ниже</div></div>
    <div class="calc-grid" id="calcGrid"></div>
  </section>

  <section class="kpis">
    <div class="kpi"><div class="label">Средний чистый след</div><div class="value" id="kpiFoot">—</div><div class="hint">кг CO₂-экв./т</div></div>
    <div class="kpi"><div class="label">Средняя эффективность</div><div class="value" id="kpiEff">—</div><div class="hint">показатель F6</div></div>
    <div class="kpi"><div class="label">Площадь колебания</div><div class="value" id="kpiArea">—</div><div class="hint">га, по выбранным строкам</div></div>
    <div class="kpi"><div class="label">Средняя себестоимость</div><div class="value" id="kpiCost">—</div><div class="hint">тыс. руб./га</div></div>
  </section>

  <section id="charts" class="grid">
    <article class="card wide"><div class="head"><div><h2>Удельный след: No-Till vs Классическая</h2><p>кг CO₂-экв./т · среднее по выбранным культурам</p></div></div><div class="chartbox"><canvas id="c1"></canvas></div></article>
    <article class="card"><div class="head"><div><h2>Структура выбросов по ресурсам</h2><p>технологические операции · техника · севооборот</p></div></div><div class="chartbox"><canvas id="c2"></canvas></div></article>
    <article class="card"><div class="head"><div><h2>Эффективность по культуре</h2><p>среднее значение F6 · столбчатая диаграмма</p></div></div><div class="chartbox"><canvas id="c3"></canvas></div></article>
    <article class="card wide"><div class="head"><div><h2>Выбросы CO₂ по технологическим операциям</h2><p>кг CO₂-экв./га · данные F5</p></div></div><div class="chartbox"><canvas id="c4"></canvas></div></article>
    <article class="card"><div class="head"><div><h2>Зависимость углеродного следа от урожайности</h2><p>урожайность, т/га · след, кг CO₂-экв./т</p></div></div><div class="chartbox"><canvas id="c5"></canvas></div></article>
    <article class="card"><div class="head"><div><h2>Вид углеродных выбросов</h2><p>минеральные удобрения · пестициды · топливо</p></div></div><div class="chartbox"><canvas id="c6"></canvas></div></article>
    <article class="card"><div class="head"><div><h2>Изменение углеродного следа</h2><p>сводный показатель по технологическим операциям</p></div></div><div class="chartbox"><canvas id="c7"></canvas></div></article>
    <article class="card"><div class="head"><div><h2>Себестоимость по заданным полям в агросезон</h2><p>тыс. руб./га · F6</p></div></div><div class="chartbox"><canvas id="c8"></canvas></div></article>
  </section>

  <section id="tables" class="tables">
    <article class="card"><div class="head"><div><h2>Культура</h2><p>выбранные культуры из Excel</p></div></div><table><thead><tr><th>Культура</th><th>Статус</th></tr></thead><tbody id="cultureTable"></tbody></table></article>
    <article class="card"><div class="head"><div><h2>Технология</h2><p>сценарии сравнения</p></div></div><table><thead><tr><th>Технология</th><th>Статус</th></tr></thead><tbody id="techTable"></tbody></table></article>
  </section>

  <section id="functions" class="functions"><h2>Расчётные функции</h2><div class="fn-grid" id="fnGrid"></div></section>
  <div class="footer"><span>Прототип · источник данных: F2(3).xlsx</span><span id="rowCount"></span></div>
</main>
</div>

<script>
const FIELD_STATS = {"1": {"records": 5, "area_avg": 118.06, "yield_avg": 4.7, "cf_avg": 13.54, "gross_avg": 2184.8, "eff_avg": 6.70, "cost_avg": 52.0, "cultures": ["Лён", "многолетние травы", "озимая пшеница", "подсолнечник"], "techs": ["No-Till", "классическая технология"], "year_records": {"Год не указан": 5}}, "2": {"records": 5, "area_avg": 113.02, "yield_avg": 5.7, "cf_avg": 6.44, "gross_avg": 2147.6, "eff_avg": 7.48, "cost_avg": 52.0, "cultures": ["Горох", "многолетние травы", "озимая пшеница"], "techs": ["No-Till", "классическая технология"], "year_records": {"Год не указан": 5}}, "3": {"records": 5, "area_avg": 126.04, "yield_avg": 4.18, "cf_avg": 20.64, "gross_avg": 2257.8, "eff_avg": 5.68, "cost_avg": 50.6, "cultures": ["Горох", "озимая пшеница", "подсолнечник"], "techs": ["No-Till", "классическая технология"], "year_records": {"Год не указан": 5}}, "4": {"records": 5, "area_avg": 121.05, "yield_avg": 6.16, "cf_avg": 14.92, "gross_avg": 2200.8, "eff_avg": 6.33, "cost_avg": 52.6, "cultures": ["Горох", "многолетние травы", "озимая пшеница"], "techs": ["No-Till", "классическая технология"], "year_records": {"Год не указан": 5}}, "5": {"records": 5, "area_avg": 115.03, "yield_avg": 4.23, "cf_avg": 36.67, "gross_avg": 2279.2, "eff_avg": 5.86, "cost_avg": 51.2, "cultures": ["Горох", "Лён", "озимая пшеница", "подсолнечник"], "techs": ["No-Till"], "year_records": {"Год не указан": 5}}};
const DATA = [{"culture":"Лён","technology":"No-Till","area":243.0,"footprint":95.18,"yield":1.3,"operation_cf":64.0,"tech_cf":142.0,"rotation_cf":12.0,"operation":"Уборка","gross":2422.0,"fert":13.0,"pest":1.0,"fuel":9.0,"change_cf":77.25,"efficiency":4.16,"cost":65.0},{"culture":"Лён","technology":"Классическая","area":466.0,"footprint":440.0,"yield":1.1,"operation_cf":99.0,"tech_cf":140.0,"rotation_cf":5.0,"operation":"Внесение удобрений","gross":2380.0,"fert":14.0,"pest":1.0,"fuel":9.0,"change_cf":0,"efficiency":1.83,"cost":52.0},{"culture":"Озимая пшеница","technology":"No-Till","area":227.0,"footprint":7.46,"yield":5.7,"operation_cf":34.0,"tech_cf":82.0,"rotation_cf":8.0,"operation":"Предпосевная обработка","gross":2236.0,"fert":13.0,"pest":2.0,"fuel":7.0,"change_cf":0,"efficiency":9.83,"cost":44.0},{"culture":"Горох","technology":"Классическая","area":344.0,"footprint":5.17,"yield":1.9,"operation_cf":7.0,"tech_cf":63.0,"rotation_cf":5.0,"operation":"Внесение удобрений","gross":2024.0,"fert":11.0,"pest":2.0,"fuel":9.0,"change_cf":0,"efficiency":3.80,"cost":51.0},{"culture":"Кукуруза","technology":"Классическая","area":176.0,"footprint":16.96,"yield":3.9,"operation_cf":54.0,"tech_cf":104.0,"rotation_cf":10.0,"operation":"Предпосевная обработка","gross":2210.0,"fert":13.0,"pest":1.0,"fuel":8.0,"change_cf":0,"efficiency":6.50,"cost":58.0},{"culture":"Кукуруза","technology":"Классическая","area":204.0,"footprint":6.33,"yield":3.9,"operation_cf":16.0,"tech_cf":68.0,"rotation_cf":12.0,"operation":"Предпосевная обработка","gross":2338.0,"fert":11.0,"pest":1.0,"fuel":8.0,"change_cf":0,"efficiency":10.40,"cost":51.0},{"culture":"Многолетние травы","technology":"No-Till","area":168.0,"footprint":16.70,"yield":4.4,"operation_cf":50.0,"tech_cf":85.0,"rotation_cf":5.0,"operation":"Уборка","gross":2116.0,"fert":12.0,"pest":1.0,"fuel":9.0,"change_cf":0,"efficiency":9.10,"cost":56.0},{"culture":"Подсолнечник","technology":"Классическая","area":215.0,"footprint":54.35,"yield":1.6,"operation_cf":60.0,"tech_cf":136.0,"rotation_cf":10.0,"operation":"Предпосевная обработка","gross":2221.0,"fert":14.0,"pest":2.0,"fuel":9.0,"change_cf":0,"efficiency":4.80,"cost":53.0},{"culture":"Горох","technology":"Классическая","area":470.0,"footprint":66.50,"yield":2.4,"operation_cf":95.0,"tech_cf":132.0,"rotation_cf":6.0,"operation":"Уборка","gross":2282.0,"fert":13.0,"pest":1.0,"fuel":9.0,"change_cf":0,"efficiency":5.60,"cost":63.0},{"culture":"Горох","technology":"Классическая","area":406.0,"footprint":16.56,"yield":2.2,"operation_cf":23.0,"tech_cf":58.0,"rotation_cf":6.0,"operation":"Внесение удобрений","gross":2001.0,"fert":14.0,"pest":1.0,"fuel":7.0,"change_cf":0,"efficiency":6.07,"cost":46.0},{"culture":"Подсолнечник","technology":"Классическая","area":207.0,"footprint":93.08,"yield":1.0,"operation_cf":56.0,"tech_cf":117.0,"rotation_cf":11.0,"operation":"Предпосевная обработка","gross":2253.0,"fert":14.0,"pest":2.0,"fuel":8.0,"change_cf":0,"efficiency":2.50,"cost":51.0}];
const CULTURES = ["Озимая пшеница","Горох","Кукуруза","Многолетние травы","Подсолнечник","Лён"];
const TECHS = ["Классическая","No-Till"];
let active = {cultures:[...CULTURES], techs:[...TECHS]};
const charts = {};
const fnData = [
  ["F.1","Планирование севооборота","Три расчётных подмодуля: секвестрация, углеродный след за период агросрока и интегральная эффективность севооборота.",[
    {id:"f1_cseq",title:"Секвестрация углерода при выборах с/х культур в севообороте",code:"Csequestered",unit:"т CO₂-экв./га",value:"2.80"},
    {id:"f1_cnet",title:"Расчет показателя углеродного следа за период агросрока",code:"Cnet",unit:"т CO₂-экв./га",value:"1.60"},
    {id:"f1_e",title:"Интегральный коэффициент эффективности севооборота",code:"E",unit:"коэффициент",value:"7.89"}
  ]],
  ["F.2","Управления удобрениями и обработкой почвы","Восемь подмодулей для параметров температуры, влажности, агротехнического воздействия и углеродных потоков.",[
    {id:"f2_ktemp",title:"Коэффициент температуры почвы",code:"Ktemp",unit:"коэффициент",value:"1.05"},
    {id:"f2_wfact",title:"Влажность почвы фактическая",code:"Wфакт",unit:"%",value:"24"},
    {id:"f2_wopt",title:"Влажность почвы оптимальная",code:"Wопт",unit:"%",value:"27"},
    {id:"f2_iat",title:"Индекс агротехнического воздействия",code:"Iат",unit:"индекс",value:"0.82"},
    {id:"f2_kvl",title:"Коэффициент увлажнения",code:"Kвлаги",unit:"коэффициент",value:"0.89"},
    {id:"f2_wcrit",title:"Влажность почвы критическая",code:"Wкрит",unit:"%",value:"18"},
    {id:"f2_cf",title:"Углеродный след от внесения пестицидов/удобрений",code:"CFпестицидов / CFудобрений",unit:"кг CO₂-экв./т",value:"13.5"},
    {id:"f2_dc",title:"Секвестрация углерода от технологической операции",code:"ΔCобработка",unit:"кг CO₂-экв./га",value:"-42"}
  ]],
  ["F.3","Мониторинга и управления защитой растений","Шесть подмодулей для оценки заражения, повреждения, интенсивности поражения, интервалов обработок и углеродного следа защиты растений.",[
    {id:"f3_uz",title:"Уровень заражения растения",code:"УЗ",unit:"%",value:"18"},
    {id:"f3_ipv",title:"Индекс повреждения (интегральная оценка ущерба)",code:"ИПВ",unit:"индекс",value:"0.34"},
    {id:"f3_d",title:"Усредненная дозировка препаратов",code:"D",unit:"л/га",value:"2.50"},
    {id:"f3_ip",title:"Интенсивность поражения",code:"ИП",unit:"%",value:"12"},
    {id:"f3_i",title:"Интервал между обработками",code:"I",unit:"дни",value:"14"},
    {id:"f3_cseason",title:"Расчет углеродного следа",code:"Cсезон",unit:"кг CO₂-экв./га",value:"86"}
  ]],
  ["F.4","Управления урожайностью и качеством продукции","Семь подмодулей для оценки потерь, урожайности, технологического углеродного следа, секвестрации остатков и качества продукции.",[
    {id:"f4_op",title:"Общие потери",code:"ОП",unit:"т/га",value:"0.42"},
    {id:"f4_ufin",title:"Финальная урожайность",code:"Уфин",unit:"т/га",value:"4.80"},
    {id:"f4_cfuy",title:"Показатель углеродного следа операции",code:"CFу.след",unit:"кг CO₂-экв./га",value:"112"},
    {id:"f4_cfitog",title:"Показатель углеродного следа на тонну зерна",code:"CFитог",unit:"кг CO₂-экв./т",value:"24.6"},
    {id:"f4_dcs",title:"Секвестрация углерода от остатков",code:"ΔCсолом",unit:"кг CO₂-экв./га",value:"-185"},
    {id:"f4_sco2",title:"Секвестрация за счёт пожнивных остатков",code:"SCO₂",unit:"кг CO₂-экв./га",value:"-96"},
    {id:"f4_qf",title:"Коэффициент качества продукции",code:"QF",unit:"%",value:"92"}
  ]],
  ["F.5","Оценки углеродного следа, прогнозирования, статистики, учета и отчетности","Семь подмодулей для сводной оценки углеродной ёмкости, выбросов, изменения следа.",[
    {id:"f5_uco2",title:"Углеродоемкость",code:"У CO₂",unit:"т CO₂/га",value:"1.84"},
    {id:"f5_eco2",title:"Эмиссия операции",code:"Э CO₂",unit:"кг CO₂-экв./га",value:"2240"},
    {id:"f5_oco2",title:"Общие валовые выбросы",code:"OCO₂",unit:"кг CO₂-экв./га",value:"3180"},
    {id:"f5_cem",title:"Эмиссия углерода от технологии",code:"Cem",unit:"кг CO₂-экв./га",value:"2860"},
    {id:"f5_ctotal",title:"Показатель углеродного следа",code:"Ctotal",unit:"кг CO₂-экв./га",value:"3015"},
    {id:"f5_change",title:"Изменение углеродного следа",code:"ΔCF min",unit:"кг CO₂-экв./га",value:"-8.5"},
    {id:"f5_effsec",title:"Анализ эффективности с учетом секвестрации",code:"Эффективность",unit:"тыс. руб/га",value:"68.4"}
  ]],
  ["F.6","Принятия стратегических решений","Восемь подмодулей для стратегической оценки углеродной нейтральности, приоритета затрат.",[
    {id:"f6_keff",title:"Коэффициент эффективности нейтральности",code:"Kэф",unit:"коэффициент",value:"0.86"},
    {id:"f6_pi",title:"Индекс приоритета",code:"PI",unit:"кг CO₂-экв./руб",value:"0.42"},
    {id:"f6_cfield",title:"Расчёт средней углеродоёмкости",code:"C поле",unit:"кг CO₂-экв./т",value:"31.7"},
    {id:"f6_op",title:"Общие потери",code:"ОП",unit:"т/га",value:"0.38"},
    {id:"f6_ynet",title:"Прогноз урожайности",code:"Y net",unit:"кг/га",value:"4820"},
    {id:"f6_e",title:"Интегральный коэффициент эффективности",code:"E",unit:"коэффициент",value:"7.89"},
    {id:"f6_cost",title:"Себестоимость по заданным полям",code:"Себестоимость",unit:"тыс. руб/га",value:"52.5"},
    {id:"f6_fert",title:"Затраты на удобрения",code:"З уд.агросрок",unit:"тыс. руб/га",value:"18.6"}
  ]]
];

function n(v){return Number(v)||0}
function avg(a){return a.length?a.reduce((x,y)=>x+y,0)/a.length:0}
function fmt(v,d=1){return new Intl.NumberFormat("ru-RU",{maximumFractionDigits:d}).format(v)}
function filtered(){return DATA.filter(r=>active.cultures.includes(r.culture)&&active.techs.includes(r.technology))}
function baseOptions(){return {responsive:true,maintainAspectRatio:false,plugins:{legend:{position:"top",labels:{boxWidth:22,usePointStyle:true,font:{size:11}}}},scales:{x:{grid:{color:"#edf1ef"},ticks:{font:{size:10}}},y:{grid:{color:"#edf1ef"},ticks:{font:{size:10}}}}}}
function make(id,type,data,options={}){if(charts[id])charts[id].destroy(); charts[id]=new Chart(document.getElementById(id),{type,data,options:{...baseOptions(),...options}})}

function renderFilters(){
  const cf=document.getElementById("cultureFilter"), tf=document.getElementById("techFilter");
  cf.innerHTML=CULTURES.map(c=>`<label class="chip"><input type="checkbox" value="${c}" ${active.cultures.includes(c)?"checked":""}>${c}</label>`).join("");
  tf.innerHTML=TECHS.map(c=>`<label class="chip"><input type="checkbox" value="${c}" ${active.techs.includes(c)?"checked":""}>${c}</label>`).join("");
}
function readFilters(){
  active.cultures=[...document.querySelectorAll("#cultureFilter input:checked")].map(x=>x.value);
  active.techs=[...document.querySelectorAll("#techFilter input:checked")].map(x=>x.value);
  if(!active.cultures.length)active.cultures=[...CULTURES];
  if(!active.techs.length)active.techs=[...TECHS];
}
function updateKpis(rows){
  document.getElementById("kpiFoot").textContent=fmt(avg(rows.map(r=>n(r.footprint))),1);
  document.getElementById("kpiEff").textContent=fmt(avg(rows.map(r=>n(r.efficiency))),2);
  document.getElementById("kpiArea").textContent=fmt(avg(rows.map(r=>n(r.area))),1);
  document.getElementById("kpiCost").textContent=fmt(avg(rows.map(r=>n(r.cost))),1);
  document.getElementById("rowCount").textContent=`${rows.length} строк Excel участвует в расчёте`;
}
function updateTables(){
  document.getElementById("cultureTable").innerHTML=CULTURES.map(c=>`<tr><td>${c}</td><td class="${active.cultures.includes(c)?"status":""}">${active.cultures.includes(c)?"Выбрано":"Не выбрано"}</td></tr>`).join("");
  document.getElementById("techTable").innerHTML=TECHS.map(c=>`<tr><td>${c}</td><td class="${active.techs.includes(c)?"status":""}">${active.techs.includes(c)?"Выбрано":"Сравнение"}</td></tr>`).join("");
}
function renderCharts(){
 const rows=filtered(); updateKpis(rows); updateTables();
 const cultures=CULTURES.filter(c=>active.cultures.includes(c));
 const techs=TECHS.filter(t=>active.techs.includes(t));
 make("c1","bar",{labels:cultures,datasets:techs.map((t,i)=>({label:t,data:cultures.map(c=>avg(rows.filter(r=>r.culture===c&&r.technology===t).map(r=>n(r.footprint)))),backgroundColor:i?"#a93d72":"#4e91ad",borderRadius:4}))});
 const resource=[avg(rows.map(r=>n(r.operation_cf))),avg(rows.map(r=>n(r.tech_cf))),avg(rows.map(r=>n(r.rotation_cf)))];
 make("c2","doughnut",{labels:["Технологические операции","Техника","Севооборот"],datasets:[{data:resource,backgroundColor:["#4e91ad","#a93d72","#e49a27"],borderWidth:3,borderColor:"#fff"}]},{cutout:"62%",plugins:{legend:{position:"right"}}});
 const eff=cultures.map(c=>avg(rows.filter(r=>r.culture===c).map(r=>n(r.efficiency))));
 make("c3","bar",{labels:cultures,datasets:[{label:"Эффективность F6",data:eff,backgroundColor:"#2d8b68",borderRadius:5}]});
 const ops=["Внесение удобрений","Предпосевная обработка","Уборка"];
 const ov=ops.map(o=>avg(rows.filter(r=>r.operation===o).map(r=>n(r.gross))));
 make("c4","bar",{labels:ops,datasets:[{label:"кг CO₂-экв./га",data:ov,backgroundColor:"#2d7655",borderRadius:5}]},{indexAxis:"y"});
 make("c5","scatter",{datasets:[{label:"Выбранные поля",data:rows.filter(r=>n(r.yield)>0&&n(r.footprint)>0).slice(0,500).map(r=>({x:n(r.yield),y:n(r.footprint)})),backgroundColor:"#4e91ad",pointRadius:4} ]},{scales:{x:{title:{display:true,text:"Урожайность, т/га"},grid:{color:"#edf1ef"}},y:{title:{display:true,text:"След, кг CO₂-экв./т"},grid:{color:"#edf1ef"}}}});
 make("c6","bar",{labels:cultures,datasets:[{label:"Минеральные удобрения",data:cultures.map(c=>avg(rows.filter(r=>r.culture===c).map(r=>n(r.fert)))),backgroundColor:"#e49a27",borderRadius:4},{label:"Пестициды",data:cultures.map(c=>avg(rows.filter(r=>r.culture===c).map(r=>n(r.pest)))),backgroundColor:"#a93d72",borderRadius:4},{label:"Топливо",data:cultures.map(c=>avg(rows.filter(r=>r.culture===c).map(r=>n(r.fuel)))),backgroundColor:"#4e91ad",borderRadius:4}]});
 make("c7","line",{labels:ops,datasets:[{label:"Изменение углеродного следа",data:ops.map(o=>avg(rows.filter(r=>r.operation===o).map(r=>n(r.change_cf)))),borderColor:"#2f7657",backgroundColor:"rgba(47,118,87,.12)",fill:true,tension:.35,pointRadius:4}]});
 make("c8","bar",{labels:cultures,datasets:[{label:"тыс. руб./га",data:cultures.map(c=>avg(rows.filter(r=>r.culture===c).map(r=>n(r.cost)))),backgroundColor:"#7a6fb1",borderRadius:5}]});
}
function renderFunctions(){
 document.getElementById("fnGrid").innerHTML=fnData.map((f,i)=>{
   const subs=f[3]||[];
   const body=subs.length?`<p class="fn-intro">${f[2]}</p><div class="submods">${subs.map(x=>`<div class="submod"><h4>${x.title}</h4><div class="formula">${x.code}</div><div class="submod-row"><div><label>Изменяемое значение</label><input id="${x.id}" type="number" step="0.01" value="${x.value}"><div class="unit">${x.unit}</div></div><div></div></div></div>`).join('')}</div>`:`<div class="fn-placeholder"><b>${f[0]}</b> — ${f[2]}</div>`;
   return `<div class="fn ${i===0?'open':''}" id="fn${i}"><button onclick="this.parentElement.classList.toggle('open')"><span><span class="code">${f[0]}</span><span class="name">подмодуль «${f[1]}»</span></span><span class="plus">+</span></button><div class="fn-body">${body}</div></div>`;
 }).join("");
}
const CALC_FUNCS=[
 {code:'F1',name:'Планирование севооборота',desc:'Выбор культур, площади и сценария севооборота; расчёт секвестрации и чистого углеродного следа.',fields:[['f1culture','Культура','select',CULTURES],['f1area','Площадь, га','number','100'],['f1cseq','Секвестрация Cseq, т CO₂-экв./га','number','2.8'],['f1cnet','Углеродный след Cnet, т CO₂-экв./га','number','1.6']]},
 {code:'F2',name:'Управления удобрениями и обработкой почвы',desc:'Параметры внесения удобрений и интенсивности обработки почвы для сценарного анализа.',fields:[['f2fert','Норма удобрений, кг/га','number','180'],['f2soil','Интенсивность обработки почвы, %','number','70']]},
 {code:'F3',name:'Мониторинга и управления защитой растений',desc:'Параметры применения средств защиты и контроль связанного риска.',fields:[['f3pest','Пестициды, кг/га','number','4.5'],['f3risk','Индекс риска, %','number','25']]},
 {code:'F4',name:'Управления урожайностью и качеством продукции',desc:'Урожайность и показатель качества продукции по выбранному сценарию.',fields:[['f4yield','Урожайность, т/га','number','4.8'],['f4quality','Индекс качества, %','number','92']]},
 {code:'F5',name:'Оценки углеродного следа, прогнозирования, статистики, учета и отчетности',desc:'Сводные показатели выбросов, технологических операций и изменения углеродного следа.',fields:[['f5emission','Выбросы, кг CO₂-экв./га','number','2250'],['f5period','Период, лет','number','1']]},
 {code:'F6',name:'Принятия стратегических решений',desc:'Сценарий и целевой показатель для стратегической оценки.',fields:[['f6scenario','Сценарий','select',['Текущий расчёт','Оптимизация','Снижение углеродного следа']],['f6target','Целевой показатель, %','number','15']]}
];
function renderTopCalc(){
 const root=document.getElementById('calcGrid'); if(!root)return;
 root.innerHTML=CALC_FUNCS.map((f,i)=>{
   const fields=f.fields.map(x=> x[2]==='select' ? `<div class="calc-field"><label>${x[1]}</label><select id="${x[0]}">${x[3].map(v=>`<option>${v}</option>`).join('')}</select></div>` : `<div class="calc-field"><label>${x[1]}</label><input id="${x[0]}" type="number" value="${x[3]}" step="0.1"></div>`).join('');
   return `<article class="calc-card ${i===0?'open':''}" id="calc-${f.code}"><button class="calc-head" type="button" onclick="this.parentElement.classList.toggle('open')"><span><span class="code">${f.code}</span><span class="name">подмодуль «${f.name}»</span></span><span class="chev">⌄</span></button><div class="calc-body"><div class="calc-desc">${f.desc}</div><div class="calc-fields">${fields}</div></div></article>`;
 }).join('');
}
function renderFieldStats(){
 const f=String(document.getElementById("fieldSelector")?.value||"1");
 const st=FIELD_STATS[f]||FIELD_STATS["1"];
 document.getElementById("fieldName").textContent="Поле "+f;
 document.getElementById("fieldCultures").textContent=st.cultures.join(" · ");
 document.getElementById("fieldTechs").textContent="Технологии: "+st.techs.join(" · ");
 document.getElementById("fsArea").textContent=fmt(st.area_avg);
 document.getElementById("fsYield").textContent=fmt(st.yield_avg,2);
 document.getElementById("fsCf").textContent=fmt(st.cf_avg,2);
 document.getElementById("fsGross").textContent=fmt(st.gross_avg,1);
 document.getElementById("fsEff").textContent=fmt(st.eff_avg,2);
 document.getElementById("fsCost").textContent=fmt(st.cost_avg,1);
}
function loadExternalExcel(file){
 const reader=new FileReader();
 reader.onload=e=>{
  const wb=XLSX.read(new Uint8Array(e.target.result),{type:"array"});
  const s4=wb.Sheets["F4"], s5=wb.Sheets["F5"], s6=wb.Sheets["F6"];
  if(!s4||!s5){alert("Файл должен содержать листы F4 и F5.");return;}
  const a4=XLSX.utils.sheet_to_json(s4,{header:1,defval:null});
  const a5=XLSX.utils.sheet_to_json(s5,{header:1,defval:null});
  const a6=s6?XLSX.utils.sheet_to_json(s6,{header:1,defval:null}):[];
  DATA.length=0;
  for(let i=2;i<a4.length;i++){
   const r=a4[i]||[], r5=a5[i]||[], r6=a6[i]||[];
   const culture=String(r[1]||"").trim(), tech=String(r[2]||"").toLowerCase().startsWith("класс")?"Классическая":"No-Till";
   if(!culture)continue;
   DATA.push({culture,technology:tech,area:Number(r[10])||100,footprint:Number(r[14])||15,yield:Number(r[8])||4,operation_cf:Number(r[6])||50,tech_cf:Number(r[7])||100,rotation_cf:Number(r[8])||10,operation:String(r5[2]||"Уборка"),gross:Number(r5[6])||2200,fert:Number(r5[7])||12,pest:Number(r5[8])||2,fuel:Number(r5[9])||8,change_cf:Number(r5[10])||0,efficiency:Number(r6[2])||8,cost:Number(r6[25])||50});
  }
  renderFilters(); renderCharts();
 };
 reader.readAsArrayBuffer(file);
}
document.getElementById("fieldSelector").onchange=renderFieldStats;
document.getElementById("applyBtn").onclick=()=>{readFilters();renderCharts()};
document.getElementById("resetBtn").onclick=()=>{active={cultures:[...CULTURES],techs:[...TECHS]};renderFilters();renderCharts()};
document.getElementById("fileInput").onchange=e=>e.target.files[0]&&loadExternalExcel(e.target.files[0]);
renderFilters();renderFunctions();renderTopCalc();renderFieldStats();renderCharts();
</script>
</body></html>'''

# HTML-референс 2: Органическое земледелие (ФЗ-280)
ORGANIC_HTML = r'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Модуль органического земледелия</title><style>
:root{--green:#1e7655;--ink:#20312b;--muted:#657b70;--line:#e2e9e5}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:linear-gradient(180deg,#edf4f1,#f6f9f7);color:var(--ink);font:16px/1.5 'Segoe UI',Arial,sans-serif}.app{display:grid;grid-template-columns:250px minmax(0,1fr)}aside{background:#143c2d;color:#dcece5;padding:28px 20px;position:sticky;top:0;height:100vh}.brand{font-size:20px;font-weight:750;margin-bottom:30px}.brand small{display:block;font-size:14px;color:#a9c8b9;font-weight:400;margin-top:8px}.mark{display:inline-grid;place-items:center;background:#2f8c69;border-radius:12px;width:42px;height:42px;margin-bottom:16px}nav{display:grid;gap:8px}nav a{color:#c8ddd5;text-decoration:none;padding:12px;border-radius:10px;font-size:15px}nav a:hover,nav a.active{background:#1d5942;color:white}.source{font-size:14px;color:#a9c8b9;border-top:1px solid #38604e;margin-top:32px;padding-top:20px}main{padding:30px;max-width:1500px;width:100%;margin:auto}h1{font-size:30px;line-height:1.2;margin:6px 0 12px}h2{font-size:21px;margin:0 0 6px}h3{font-size:18px;margin:0}p{margin:0;color:var(--muted);font-size:14px}.eyebrow{font-size:13px;letter-spacing:.1em;text-transform:uppercase;font-weight:750;color:#527562}.filters,.card,.kpi{background:white;border:1px solid var(--line);box-shadow:0 8px 28px #19372b0c;border-radius:16px}.filters{display:flex;gap:16px;align-items:end;margin:22px 0 16px;padding:16px}.field{flex:1}label{display:block;font-size:14px;color:var(--muted);margin-bottom:5px}select,button{font:inherit;border:1px solid #dce5e0;border-radius:9px;padding:10px 12px;background:#fbfdfc;color:var(--ink)}select{width:100%}button{cursor:pointer;background:var(--green);color:white;border-color:var(--green)}.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:16px 0}.kpi{padding:18px}.kpi span{font-size:14px;color:var(--muted)}.kpi b{display:block;font-size:28px;margin:5px 0}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.card{padding:20px;min-width:0}.wide{grid-column:1/-1}.chart{margin-top:16px}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;padding:12px;border-bottom:1px solid #edf1ef}th{color:var(--muted);font-weight:600}.compact-upload{padding:14px 18px;margin-top:20px}.upload-row{display:flex;gap:12px;align-items:center}.file-symbol{font-size:12px;font-weight:800;color:#1e7655;background:#e3f1e9;border:1px solid #cce2d5;border-radius:9px;width:46px;height:44px;display:grid;place-items:center}.file-info{flex:1}.dropzone{padding:9px 15px;border:1px solid var(--green);background:var(--green);border-radius:9px;color:white;cursor:pointer;font-weight:650;position:relative}.dropzone input{position:absolute;inset:0;opacity:0;cursor:pointer}.parameter-shell{display:grid;grid-template-columns:230px minmax(0,1fr);background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden}.module-tabs{background:#f6faf7;padding:12px;display:flex;flex-direction:column;gap:8px;border-right:1px solid var(--line)}.module-tab{display:flex;gap:10px;padding:13px 10px;background:transparent;color:var(--ink);border:1px solid transparent;font-size:14px}.module-tab.active{background:#e3f0e8;border-color:#c5ddcf;color:#175d42}.module-content{padding:26px}.module-fields{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.input-wrap{border:1px solid #d3e0d8;border-radius:10px;padding:10px 12px;background:#fbfdfc;display:flex;gap:8px}.input-wrap input{border:0;width:100%;background:transparent;outline:none}.comparison{display:grid;gap:18px}.comparison-row{display:grid;grid-template-columns:160px minmax(0,1fr);gap:18px;align-items:center}.measure-row{display:flex;align-items:center;gap:12px}.measure-track{height:17px;flex:1;background:#edf3ef;border-radius:5px;overflow:hidden}.measure-fill{height:100%;border-radius:5px}.measure-number{font-size:16px;font-weight:750;min-width:105px;text-align:right}.ring-layout{display:flex;align-items:center;gap:24px}.ring{width:180px;height:180px;border-radius:50%;display:grid;place-items:center}.ring-center{width:130px;height:130px;border-radius:50%;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center}.ring-legend{flex:1;display:grid;gap:18px}.ring-item{display:flex;gap:10px;align-items:center}
.loss-summary{padding:8px 4px}.loss-stage{padding:0 8px 17px}.loss-track{position:relative;height:7px;background:#f0f1ed;border-radius:5px;margin:16px 0 12px}.loss-range{position:absolute;top:0;height:7px;background:#dba5c2;border-radius:5px}.loss-mean{position:absolute;top:-4px;width:15px;height:15px;border:3px solid white;background:#a93d72;border-radius:50%;transform:translateX(-50%)}.loss-values{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:9px}
@media(max-width:1050px){.app{grid-template-columns:1fr}aside{display:none}.grid,.parameter-shell,.module-fields{grid-template-columns:1fr}}
</style></head><body>
<div class="app"><aside><div class="brand"><div class="mark">F</div><br>Модуль органического<br>земледелия<small>Аналитическая панель</small></div><nav><a class="active" href="#overview">Обзор</a><a href="#parameters">Параметры F1–F5</a><a href="#harvest">Урожай и качество</a><a href="#compliance">Технологии и отчётность</a></nav><div class="source">Источник данных<br><b>Органика (ФЗ-280).xlsx</b></div></aside>
<main id="overview">
<div class="top"><div><div class="eyebrow">Аналитика агротехнологий</div><h1>Модуль органического земледелия</h1><p>Контроль соблюдения Федерального закона № 280-ФЗ и биологической фиксации азота</p></div><label class="dropzone">Загрузить XLSX<input type="file" id="fileIn" accept=".xlsx"></label></div>
<div class="filters"><div class="field"><label>Основная культура</label><select id="cFilter"><option value="">Все культуры</option><option>Озимая пшеница</option><option>Горох</option><option>Кукуруза</option><option>Многолетние травы</option><option>Подсолнечник</option><option>Лён</option></select></div><div class="field"><label>Технология</label><select id="tFilter"><option value="">Все технологии</option><option>No-Till</option><option>Классическая</option><option>Strip-till</option><option>Mini-till</option><option>Плоскорезная</option></select></div><button onclick="renderAll()">Применить</button></div>
<div class="kpis"><div class="kpi"><span>Финальная урожайность</span><b>4.85</b><small>т/га</small></div><div class="kpi"><span>Общие потери</span><b>0.41</b><small>т/га</small></div><div class="kpi"><span>Индекс качества Qindex</span><b>89.4%</b><small>соответствие норме</small></div><div class="kpi"><span>Эффективность севооборота</span><b>7.89</b><small>коэффициент E</small></div></div>

<section class="section" id="parameters"><h2>Параметры F1–F5</h2><div class="parameter-shell"><div class="module-tabs"><button class="module-tab active"><b>F1</b> Севооборот</button><button class="module-tab"><b>F2</b> Удобрения</button><button class="module-tab"><b>F3</b> Защита</button><button class="module-tab"><b>F4</b> Урожайность</button><button class="module-tab"><b>F5</b> Отчетность</button></div><div class="module-content"><h3>F1 · Планирование севооборота</h3><p>Коэффициенты урожайности и эффективности севооборота</p><div class="module-fields"><div class="field"><label>Ravg</label><div class="input-wrap"><input type="text" value="0.28"></div></div><div class="field"><label>Прогнозируемая урожайность Y net</label><div class="input-wrap"><input type="text" value="4.82"><span class="unit">т/га</span></div></div><div class="field"><label>Интегральный коэффициент E</label><div class="input-wrap"><input type="text" value="7.89"></div></div></div></div></div></section>

<section class="section" id="harvest"><h2>Урожай и качество продукции</h2><div class="grid"><article class="card wide"><h3>Фактическая и финальная урожайность</h3><div class="chart" id="yieldChart"></div></article><article class="card"><h3>Потери при уборке</h3><div class="chart" id="lossChart"></div></article><article class="card"><h3>Качество продукции</h3><div class="chart" id="qualityChart"></div></article></div></section>

<section class="section" id="compliance"><h2>Технологии и отчётность (ФЗ-280)</h2><div class="grid"><article class="card"><h3>Соответствие технологии</h3><div class="chart" id="compChart"></div></article><article class="card"><h3>Соответствие удобрений</h3><div class="chart" id="fertChart"></div></article><article class="card wide"><h3>Фиксированный азот бобовыми</h3><div class="chart" id="nitroChart"></div></article></div></section>
</main></div>
<script>
function renderBars(id, data, max, unit){
  const el = document.getElementById(id);
  el.innerHTML = `<div class="comparison">` + data.map(d => `<div class="comparison-row"><div>${d.label}</div><div class="measure-row"><div class="measure-track"><div class="measure-fill" style="width:${d.val/max*100}%;background:${d.color||'#2d8b68'}"></div></div><div class="measure-number">${d.val} ${unit}</div></div></div>`).join('') + `</div>`;
}
function renderLoss(){
  const stages = [{name:'Жатва', min:0.12, mean:0.29, max:0.61}, {name:'Обмолот', min:0.04, mean:0.08, max:0.15}, {name:'Сепарация', min:0.08, mean:0.26, max:0.61}];
  document.getElementById('lossChart').innerHTML = `<div class="loss-summary">` + stages.map(s => `<div class="loss-stage"><div style="display:flex;justify-content:space-between;"><b>${s.name}</b><small>т/га</small></div><div class="loss-track"><div class="loss-range" style="left:${s.min/0.7*100}%;width:${(s.max-s.min)/0.7*100}%"></div><div class="loss-mean" style="left:${s.mean/0.7*100}%"></div></div><div class="loss-values"><div><small>Мин</small><b>${s.min}</b></div><div style="text-align:center;"><small>Среднее</small><b style="color:#a93d72">${s.mean}</b></div><div style="text-align:right;"><small>Макс</small><b>${s.max}</b></div></div></div>`).join('') + `</div>`;
}
function renderRing(id, pct, label, color){
  document.getElementById(id).innerHTML = `<div class="ring-layout"><div class="ring" style="background:conic-gradient(${color} ${pct}%, #edf3ef ${pct}% 100%)"><div class="ring-center"><strong>${pct}%</strong><span>${label}</span></div></div><div class="ring-legend"><div class="ring-item"><b>${pct}%</b> Соответствует</div><div class="ring-item"><b>${100-pct}%</b> Не соответствует</div></div></div>`;
}
function renderAll(){
  renderBars('yieldChart', [{label:'Озимая пшеница',val:5.5,color:'#4e91ad'},{label:'Кукуруза',val:4.2,color:'#4e91ad'},{label:'Многолетние травы',val:4.5,color:'#4e91ad'},{label:'Горох',val:2.1,color:'#4e91ad'},{label:'Подсолнечник',val:1.6,color:'#4e91ad'},{label:'Лён',val:1.1,color:'#4e91ad'}], 6, 'т/га');
  renderBars('qualityChart', [{label:'Подсолнечник',val:94.0},{label:'Озимая пшеница',val:91.5},{label:'Кукуруза',val:89.2},{label:'Горох',val:87.0},{label:'Лён',val:85.5}], 100, '%');
  renderBars('nitroChart', [{label:'Люцерна',val:175.2,color:'#e49a27'},{label:'Клевер',val:148.5,color:'#e49a27'},{label:'Соя',val:112.4,color:'#e49a27'},{label:'Горох',val:68.9,color:'#e49a27'}], 200, 'кг N/га');
  renderLoss();
  renderRing('compChart', 68, 'ФЗ-280', '#2d8b68');
  renderRing('fertChart', 74, 'Органика', '#2d8b68');
}
renderAll();
</script>
</body></html>'''