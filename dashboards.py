UNIFIED_AGRO_HTML = r"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Агрономическая Аналитическая Панель</title>
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
body{margin:0;padding:0;background:linear-gradient(180deg,#edf4f1 0%,#f6f9f7 100%);color:var(--ink);font-family:Inter,Segoe UI,Arial,sans-serif;height:100vh;overflow-x:hidden}
.app{display:grid;grid-template-columns:260px 1fr;min-height:100vh}
.sidebar{background:#143c2d;color:#dcece5;padding:24px 18px;position:sticky;top:0;height:100vh;display:flex;flex-direction:column;gap:12px;z-index:10}
.brand{display:flex;gap:12px;align-items:center;padding:0 4px 12px}
.logo{width:40px;height:40px;border-radius:12px;background:#2f8c69;display:grid;place-items:center;font-size:20px}
.brand b{display:block;font-size:14px;letter-spacing:.02em;color:#fff}.brand span{font-size:11px;color:#9db9ad}

.mode-switcher{background:#0d281e;border:1px solid #1f543f;border-radius:12px;padding:4px;display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-bottom:12px}
.mode-btn{background:transparent;border:0;color:#9db9ad;font-size:12px;font-weight:700;padding:8px 6px;border-radius:8px;cursor:pointer;transition:.2s;text-align:center}
.mode-btn:hover{color:#fff;background:rgba(255,255,255,0.06)}
.mode-btn.active{background:#2f8c69;color:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.3)}

.nav{display:grid;gap:6px}.nav a{padding:10px 14px;border-radius:10px;color:#c8ddd5;text-decoration:none;font-size:13px;font-weight:600}.nav a.active,.nav a:hover{background:#1d5942;color:#fff}
.side-note{margin-top:auto;padding:12px 4px;color:#91ada2;font-size:11px;line-height:1.4;border-top:1px solid rgba(255,255,255,.1)}

main{padding:28px 32px 42px;max-width:1600px;width:100%;margin:auto}
.top{display:flex;justify-content:space-between;gap:20px;align-items:flex-start;margin-bottom:20px}
.eyebrow{color:#5b8072;font-weight:800;font-size:11px;letter-spacing:.12em;text-transform:uppercase}
h1{font-size:28px;margin:5px 0;letter-spacing:-.02em;color:#20312b}.subtitle{color:var(--muted);font-size:13px}
.actions{display:flex;gap:8px;align-items:center}.btn{border:1px solid var(--line);background:#fff;border-radius:10px;padding:9px 13px;color:var(--ink);font-weight:700;font-size:13px;cursor:pointer}.btn.primary{background:var(--green);border-color:var(--green);color:#fff}.btn:hover{transform:translateY(-1px)}
.filters{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;box-shadow:var(--shadow);display:grid;grid-template-columns:2fr 1.25fr 1fr auto;gap:12px;align-items:end}
.field label{display:block;font-size:10px;text-transform:uppercase;letter-spacing:.08em;font-weight:800;color:#7a8984;margin:0 0 6px}
.select{min-height:40px;border:1px solid #dce5e0;border-radius:10px;background:#fbfdfc;padding:6px 8px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.chip{display:inline-flex;gap:5px;align-items:center;padding:5px 8px;border-radius:8px;background:#e8f2ed;color:#255d48;font-size:12px;font-weight:700}
.chip input{accent-color:var(--green)}
select{width:100%;border:1px solid #dce5e0;background:#fbfdfc;border-radius:10px;padding:9px;font-size:13px;color:var(--ink)}

.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0}
.kpi{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;box-shadow:var(--shadow)}.kpi .label{font-size:12px;color:var(--muted)}.kpi .value{font-size:24px;font-weight:850;margin-top:6px}.kpi .hint{font-size:11px;color:#8a9993;margin-top:2px}

.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px;box-shadow:var(--shadow);min-width:0}
.card.wide{grid-column:1/-1}.head h2{font-size:16px;margin:0 0 4px}.head p{margin:0;color:var(--muted);font-size:11px}
.chartbox{height:300px;margin-top:8px}

.field-stat-card{margin:16px 0 20px;background:linear-gradient(135deg,#174f3a,#236f51);color:#fff;border-radius:16px;padding:20px 22px;box-shadow:0 12px 28px rgba(25,80,58,.16)}
.field-stat-head{display:flex;justify-content:space-between;align-items:flex-start;gap:20px}
.field-stat-head h2{margin:2px 0 4px;font-size:19px;color:#fff}.field-stat-head p{margin:0;color:#d5e9df;font-size:12px}
.field-picker select{padding:8px 12px;border-radius:9px;background:#fff;color:#17382b;font-weight:700;border:0}
.field-summary{display:grid;grid-template-columns:1.35fr repeat(6,1fr);gap:10px;margin-top:16px}
.field-main,.stat{background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.12);border-radius:10px;padding:11px}
.field-main span{display:block;color:#bfe0d0;font-size:11px;margin-bottom:4px}.field-main b{display:block;font-size:14px}.field-main small{display:block;margin-top:4px;color:#d4e8df;font-size:11px}
.stat span{display:block;font-size:10px;color:#c8dfd5;margin-bottom:5px}.stat b{font-size:15px;color:#fff}

/* Верхний блок расчётных функций F1–F6 */
.calc-top{margin:18px 0 16px}
.calc-top-title{display:flex;justify-content:space-between;align-items:end;gap:12px;margin-bottom:10px}
.calc-top-title h2{font-size:18px;margin:0}.calc-top-title p{margin:0;color:var(--muted);font-size:11px}
.calc-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.calc-card{background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);overflow:hidden}
.calc-head{width:100%;border:0;background:#fff;padding:15px 16px;display:flex;justify-content:space-between;align-items:center;cursor:pointer;text-align:left;color:var(--ink)}
.calc-head:hover{background:#f8fbf9}
.calc-head .code{font-weight:900;color:var(--green);margin-right:8px}
.calc-head .name{font-weight:800;font-size:12px}
.calc-head .chev{font-size:18px;color:#6b7b74;transition:.2s}
.calc-card.open .calc-head .chev{transform:rotate(180deg)}
.calc-body{display:none;padding:0 16px 16px;border-top:1px solid #eef2ef;background:#fbfdfc}
.calc-card.open .calc-body{display:block}
.calc-desc{font-size:11px;color:var(--muted);line-height:1.5;padding:12px 0 10px}
.calc-fields{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.calc-field label{display:block;font-size:10px;color:#788881;font-weight:800;margin-bottom:5px}
.calc-field input,.calc-field select{width:100%;padding:9px 10px;border:1px solid #dce5e0;border-radius:9px;background:#fff;color:var(--ink);font-size:12px}
.calc-actions{display:flex;gap:8px;margin-top:11px}
.calc-actions button{border:0;border-radius:9px;padding:9px 12px;cursor:pointer;font-weight:750;font-size:12px}
.calc-save{background:var(--green);color:#fff}
.calc-clear{background:#e9f1ed;color:#255a47}
.calc-result{margin-top:10px;padding:10px 12px;border-radius:9px;background:#eaf4ef;font-size:11px;color:#275b48;display:none}
.calc-card.open .calc-result.visible{display:block}
.calc-top-note{font-size:10px;color:#81918a;margin-top:8px}

/* Нижний детальный блок подмодулей F1–F6 */
.functions{margin-top:20px}.functions h2{font-size:17px;margin:0 0 10px}
.fn-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.fn{background:#fff;border:1px solid var(--line);border-radius:13px;overflow:hidden;box-shadow:0 6px 20px rgba(25,55,43,.06)}
.fn button{width:100%;border:0;background:#fff;padding:15px;display:flex;justify-content:space-between;align-items:center;text-align:left;cursor:pointer}
.fn .code{font-weight:900;color:#244d3e;margin-right:8px}
.fn .name{font-weight:750;font-size:12px}
.plus{font-size:18px;color:#6c7c75;transition:.2s}
.fn-body{display:none;padding:14px 16px 16px;background:#fbfdfc;border-top:1px solid #eef2ef}
.fn.open .fn-body{display:block}
.fn.open .plus{transform:rotate(45deg)}
.fn-intro{margin:0 0 12px;color:#71817b;font-size:11px}
.submods{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.submod{background:#fff;border:1px solid #e3ebe7;border-radius:12px;padding:12px}
.submod h4{margin:0 0 8px;font-size:12px;line-height:1.35;color:#284a3e}
.submod .formula{font-size:10px;color:#81908a;margin-bottom:8px}
.submod-row{display:grid;grid-template-columns:1fr 100px;gap:8px;align-items:end}
.submod label{display:block;font-size:9px;color:#788881;font-weight:800;margin-bottom:4px}
.submod input{width:100%;padding:8px 9px;border:1px solid #dce5e0;border-radius:8px;background:#fff;color:var(--ink);font-size:12px}
.submod .unit{font-size:9px;color:#8a9892;margin-top:4px}
.fn-save{margin-top:12px;border:0;background:#1e7655;color:#fff;border-radius:9px;padding:9px 12px;font-weight:800;cursor:pointer;font-size:12px}
.fn-status{display:inline-block;margin-left:8px;font-size:10px;color:#2d7658}

.tables{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}
table{width:100%;border-collapse:collapse;font-size:12px}th,td{padding:10px;border-bottom:1px solid #edf1ef;text-align:left}th{font-size:10px;color:#7a8984;text-transform:uppercase;letter-spacing:.06em}td.num{text-align:right;font-variant-numeric:tabular-nums}.status{font-weight:800;color:var(--green)}
.footer{display:flex;justify-content:space-between;margin-top:18px;color:#82908b;font-size:10px}

/* Органика */
.comparison{display:grid;gap:14px;padding-top:6px}.comparison-row{display:grid;grid-template-columns:150px 1fr;gap:14px;align-items:center}.measure-row{display:flex;align-items:center;gap:10px}.measure-track{height:16px;flex:1;background:#edf3ef;border-radius:5px;overflow:hidden}.measure-fill{height:100%;border-radius:5px}.measure-number{font-size:14px;font-weight:750;min-width:90px;text-align:right}
.ring-layout{display:flex;align-items:center;gap:20px;padding:10px 0}.ring{width:160px;height:160px;border-radius:50%;display:grid;place-items:center;flex-shrink:0}.ring-center{width:115px;height:115px;border-radius:50%;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center}.ring-center strong{font-size:24px}.ring-legend{display:grid;gap:12px;flex:1}
.loss-summary{padding:6px 0}.loss-stage{padding:0 6px 14px}.loss-track{position:relative;height:6px;background:#f0f1ed;border-radius:4px;margin:14px 0 10px}.loss-range{position:absolute;top:0;height:6px;background:#dba5c2;border-radius:4px}.loss-mean{position:absolute;top:-4px;width:14px;height:14px;border:3px solid white;background:#a93d72;border-radius:50%;transform:translateX(-50%)}.loss-values{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}

.view-container{display:none}.view-container.active{display:block}
@media(max-width:1100px){.app{grid-template-columns:1fr}.sidebar{height:auto;position:relative}.field-summary{grid-template-columns:repeat(3,1fr)}}
@media(max-width:760px){main{padding:18px}.grid,.tables,.fn-grid,.submods,.calc-grid,.calc-fields{grid-template-columns:1fr}.kpis{grid-template-columns:1fr 1fr}.field-summary{grid-template-columns:1fr 1fr}}
</style>
</head>
<body>
<div class="app">
<aside class="sidebar">
  <div class="brand"><div class="logo">🌱</div><div><b>Агро-Аналитика</b><span>модульная панель</span></div></div>
  
  <div class="mode-switcher">
    <button class="mode-btn active" id="btnCarbon" onclick="switchDashboard('carbon')">Углеродное</button>
    <button class="mode-btn" id="btnOrganic" onclick="switchDashboard('organic')">Органика</button>
  </div>

  <nav class="nav" id="carbonNav">
    <a class="active" href="#carbonView">Главная</a>
    <a href="#calcTop">Функции F1–F6</a>
    <a href="#charts">Аналитика выбросов</a>
    <a href="#functions">Все подмодули</a>
  </nav>
  <nav class="nav" id="organicNav" style="display:none">
    <a class="active" href="#organicView">Обзор норм</a>
    <a href="#orgHarvest">Урожай и потери</a>
    <a href="#orgCompliance">ФЗ-280 регламент</a>
  </nav>
  <div class="side-note">Excel переключает модуль автоматически.<br>Значения сохраняются в браузере.</div>
</aside>

<!-- РЕЖИМ 1: УГЛЕРОДНО-НЕЙТРАЛЬНОЕ ЗЕМЛЕДЕЛИЕ (F1–F6) -->
<main id="carbonView" class="view-container active">
  <div class="top">
    <div><div class="eyebrow">Аналитическая панель</div><h1>Модуль углеродно-нейтрального земледелия по 5 полям</h1><div class="subtitle">Интерактивная аналитика данных Excel и визуализация ключевых показателей агросезона</div></div>
    <div class="actions"><label class="btn">Загрузить Excel<input type="file" onchange="loadXlsx(event)" accept=".xlsx,.xls" hidden></label><button class="btn" onclick="resetFilters()">Сбросить</button><button class="btn primary" onclick="window.print()">Печать</button></div>
  </div>

  <section class="filters">
    <div class="field"><label>Культура</label><div id="cultureFilter" class="select"></div></div>
    <div class="field"><label>Технология</label><div id="techFilter" class="select"></div></div>
    <div class="field"><label>Агросезон</label><select><option>Текущий расчёт</option><option>Все агросезоны</option></select></div>
    <button class="btn primary" onclick="renderCarbonCharts()">Применить</button>
  </section>

  <section class="field-stat-card">
    <div class="field-stat-head">
      <div><h2>Статистика выбранного поля</h2><p>Показатели по 5-летнему ретроспективному севообороту</p></div>
      <div class="field-picker"><select id="fieldSelector" onchange="renderFieldStats()"><option value="1">Поле 1</option><option value="2">Поле 2</option><option value="3">Поле 3</option><option value="4">Поле 4</option><option value="5">Поле 5</option></select></div>
    </div>
    <div class="field-summary">
      <div class="field-main"><span id="fieldName">Поле 1</span><b id="fieldCultures">—</b><small id="fieldTechs">—</small></div>
      <div class="stat"><span>Ретроспектива</span><b>5 лет</b></div>
      <div class="stat"><span>Средняя площадь</span><b id="fsArea">—</b></div>
      <div class="stat"><span>Урожайность</span><b id="fsYield">—</b></div>
      <div class="stat"><span>Удельный след</span><b id="fsCf">—</b></div>
      <div class="stat"><span>Выбросы</span><b id="fsGross">—</b></div>
      <div class="stat"><span>Эффективность F1</span><b id="fsEff">—</b></div>
    </div>
  </section>

  <!-- ВЕРХНИЙ БЛОК F1–F6 С СОХРАНЕНИЕМ -->
  <section class="calc-top" id="calcTop">
    <div class="calc-top-title">
      <div><h2>Расчётные функции F1–F6</h2><p>Функции раскрываются сверху; параметры можно вводить и сохранять без перезагрузки страницы.</p></div>
      <div class="calc-top-note">Связано с аналитической панелью ниже</div>
    </div>
    <div class="calc-grid" id="calcGrid"></div>
  </section>

  <section class="kpis">
    <div class="kpi"><div class="label">Средний чистый след</div><div class="value" id="kpiFoot">13.5</div><div class="hint">кг CO₂-экв./т</div></div>
    <div class="kpi"><div class="label">Средняя эффективность</div><div class="value" id="kpiEff">6.70</div><div class="hint">показатель F6</div></div>
    <div class="kpi"><div class="label">Площадь выборки</div><div class="value" id="kpiArea">118.1</div><div class="hint">га, в среднем</div></div>
    <div class="kpi"><div class="label">Себестоимость</div><div class="value" id="kpiCost">52.0</div><div class="hint">тыс. руб./га</div></div>
  </section>

  <section id="charts" class="grid">
    <article class="card wide"><div class="head"><h2>Удельный след: No-Till vs Классическая</h2><p>кг CO₂-экв./т · среднее по выбранным культурам</p></div><div class="chartbox"><canvas id="c1"></canvas></div></article>
    <article class="card"><div class="head"><h2>Структура выбросов по ресурсам</h2><p>технологические операции · техника · севооборот</p></div><div class="chartbox"><canvas id="c2"></canvas></div></article>
    <article class="card"><div class="head"><h2>Эффективность по культуре (F6)</h2><p>среднее значение F6</p></div><div class="chartbox"><canvas id="c3"></canvas></div></article>
    <article class="card wide"><div class="head"><h2>Выбросы CO₂ по технологическим операциям</h2><p>кг CO₂-экв./га · данные F5</p></div><div class="chartbox"><canvas id="c4"></canvas></div></article>
    <article class="card"><div class="head"><h2>Зависимость углеродного следа от урожайности</h2><p>урожайность, т/га · след, кг CO₂-экв./т</p></div><div class="chartbox"><canvas id="c5"></canvas></div></article>
    <article class="card"><div class="head"><h2>Вид углеродных выбросов</h2><p>минеральные удобрения · пестициды · топливо</p></div><div class="chartbox"><canvas id="c6"></canvas></div></article>
    <article class="card"><div class="head"><h2>Изменение углеродного следа</h2><p>сводный показатель по операциям</p></div><div class="chartbox"><canvas id="c7"></canvas></div></article>
    <article class="card"><div class="head"><h2>Себестоимость по заданным полям в агросезон</h2><p>тыс. руб./га · F6</p></div><div class="chartbox"><canvas id="c8"></canvas></div></article>
  </section>

  <section id="tables" class="tables">
    <article class="card"><div class="head"><h2>Культура</h2><p>выбранные культуры из Excel</p></div><table><thead><tr><th>Культура</th><th>Статус</th></tr></thead><tbody id="cultureTable"></tbody></table></article>
    <article class="card"><div class="head"><h2>Технология</h2><p>сценарии сравнения</p></div><table><thead><tr><th>Технология</th><th>Статус</th></tr></thead><tbody id="techTable"></tbody></table></article>
  </section>

  <!-- НИЖНИЙ ПОЛНЫЙ БЛОК ПОДМОДУЛЕЙ F1–F6 -->
  <section id="functions" class="functions">
    <h2>Расчётные функции</h2>
    <div class="fn-grid" id="fnGrid"></div>
  </section>
  <div class="footer"><span>Прототип · источник данных: F2(3).xlsx</span><span id="rowCount"></span></div>
</main>

<!-- РЕЖИМ 2: ОРГАНИЧЕСКОЕ ЗЕМЛЕДЕЛИЕ -->
<main id="organicView" class="view-container">
  <div class="top">
    <div><div class="eyebrow">Органический регламент</div><h1>Модуль органического земледелия (ФЗ-280)</h1><div class="subtitle">Контроль запрета минеральных удобрений, глубины обработки и азотфиксации</div></div>
    <div class="actions"><label class="btn">Загрузить Excel<input type="file" onchange="loadXlsx(event)" accept=".xlsx,.xls" hidden></label><button class="btn primary" onclick="window.print()">Печать</button></div>
  </div>

  <section class="kpis">
    <div class="kpi"><div class="label">Финальная урожайность</div><div class="value">4.85</div><div class="hint">т/га (за вычетом потерь)</div></div>
    <div class="kpi"><div class="label">Общие потери</div><div class="value">0.41</div><div class="hint">т/га (жатва + сепарация)</div></div>
    <div class="kpi"><div class="label">Индекс качества Qindex</div><div class="value">89.4%</div><div class="hint">товарные свойства</div></div>
    <div class="kpi"><div class="label">Эффективность севооборота</div><div class="value">7.89</div><div class="hint">коэффициент E (лист F1)</div></div>
  </section>

  <section class="grid" id="orgHarvest">
    <article class="card">
      <div class="head"><h2>Соответствие технологии ФЗ-280</h2><p>Глубина основной обработки почвы ≤ 5 см</p></div>
      <div id="orgCompRing"></div>
    </article>
    <article class="card">
      <div class="head"><h2>Соответствие удобрений</h2><p>Запрет синтетических форм азота</p></div>
      <div id="orgFertRing"></div>
    </article>
    <article class="card wide">
      <div class="head"><h2>Фактическая и финальная урожайность по культурам</h2><p>т/га</p></div>
      <div id="orgYieldBars" style="padding-top:10px"></div>
    </article>
    <article class="card" id="orgCompliance">
      <div class="head"><h2>Потери при уборке по этапам</h2><p>т/га (мин, среднее, макс)</p></div>
      <div id="orgLossSummary"></div>
    </article>
    <article class="card">
      <div class="head"><h2>Биологически фиксированный азот (F2)</h2><p>кг N/га бобовых сидератов</p></div>
      <div id="orgNitroBars" style="padding-top:10px"></div>
    </article>
  </section>
</main>
</div>

<script>
const FIELD_STATS = {
  "1": {cultures: ["Лён", "Многолетние травы", "Озимая пшеница", "Подсолнечник"], techs: ["No-Till", "Классическая"], area: "118.1 га", yield: "4.70 т/га", cf: "13.54", gross: "2 184.8", eff: "6.70", cost: "52.0"},
  "2": {cultures: ["Горох", "Многолетние травы", "Озимая пшеница"], techs: ["No-Till", "Классическая"], area: "113.0 га", yield: "5.70 т/га", cf: "6.44", gross: "2 147.6", eff: "7.48", cost: "52.0"},
  "3": {cultures: ["Горох", "Озимая пшеница", "Подсолнечник"], techs: ["No-Till", "Классическая"], area: "126.0 га", yield: "4.18 т/га", cf: "20.64", gross: "2 257.8", eff: "5.68", cost: "50.6"},
  "4": {cultures: ["Горох", "Многолетние травы", "Озимая пшеница"], techs: ["No-Till", "Классическая"], area: "121.1 га", yield: "6.16 т/га", cf: "14.92", gross: "2 200.8", eff: "6.33", cost: "52.6"},
  "5": {cultures: ["Горох", "Лён", "Озимая пшеница", "Подсолнечник"], techs: ["No-Till"], area: "115.0 га", yield: "4.23 т/га", cf: "36.67", gross: "2 279.2", eff: "5.86", cost: "51.2"}
};

let DATA = [
  {culture:"Озимая пшеница", technology:"No-Till", area:227.0, footprint:7.46, yield:5.7, gross:2236, operation_cf:34, tech_cf:82, rotation_cf:8, operation:"Предпосевная обработка", fert:13, pest:2, fuel:7, change_cf:0, efficiency:9.83, cost:44},
  {culture:"Озимая пшеница", technology:"Классическая", area:371.0, footprint:13.53, yield:4.0, gross:2455, operation_cf:44, tech_cf:100, rotation_cf:12, operation:"Уборка", fert:13, pest:1, fuel:8, change_cf:0, efficiency:10.37, cost:46},
  {culture:"Горох", technology:"No-Till", area:363.0, footprint:6.24, yield:2.1, gross:2300, operation_cf:8, tech_cf:50, rotation_cf:9, operation:"Предпосевная обработка", fert:11, pest:2, fuel:8, change_cf:0, efficiency:5.25, cost:50},
  {culture:"Горох", technology:"Классическая", area:344.0, footprint:5.17, yield:1.9, gross:2024, operation_cf:7, tech_cf:63, rotation_cf:5, operation:"Внесение удобрений", fert:11, pest:2, fuel:9, change_cf:0, efficiency:3.80, cost:51},
  {culture:"Кукуруза", technology:"Классическая", area:176.0, footprint:16.96, yield:3.9, gross:2210, operation_cf:54, tech_cf:104, rotation_cf:10, operation:"Предпосевная обработка", fert:13, pest:1, fuel:8, change_cf:0, efficiency:6.50, cost:58},
  {culture:"Кукуруза", technology:"No-Till", area:434.0, footprint:34.55, yield:3.7, gross:2049, operation_cf:98, tech_cf:135, rotation_cf:10, operation:"Внесение удобрений", fert:10, pest:2, fuel:9, change_cf:0, efficiency:7.66, cost:54},
  {culture:"Многолетние травы", technology:"No-Till", area:168.0, footprint:16.70, yield:4.4, gross:2116, operation_cf:50, tech_cf:85, rotation_cf:5, operation:"Уборка", fert:12, pest:1, fuel:9, change_cf:0, efficiency:9.10, cost:56},
  {culture:"Подсолнечник", technology:"Классическая", area:215.0, footprint:54.35, yield:1.6, gross:2221, operation_cf:60, tech_cf:136, rotation_cf:10, operation:"Предпосевная обработка", fert:14, pest:2, fuel:9, change_cf:0, efficiency:4.80, cost:53},
  {culture:"Лён", technology:"No-Till", area:243.0, footprint:95.18, yield:1.3, gross:2422, operation_cf:64, tech_cf:142, rotation_cf:12, operation:"Уборка", fert:13, pest:1, fuel:9, change_cf:77.25, efficiency:4.16, cost:65}
];

const CULTURES = ["Озимая пшеница","Горох","Кукуруза","Многолетние травы","Подсолнечник","Лён"];
const TECHS = ["Классическая","No-Till"];
let active = {cultures:[...CULTURES], techs:[...TECHS]};
const charts = {};

/* Структура данных верхнего блока F1–F6 */
const CALC_FUNCS=[
 {code:'F1',name:'Планирование севооборота',desc:'Выбор культур, площади и сценария севооборота; расчёт секвестрации и чистого углеродного следа.',fields:[['f1culture','Культура','select',CULTURES],['f1area','Площадь, га','number','100'],['f1cseq','Секвестрация Cseq, т CO₂-экв./га','number','2.8'],['f1cnet','Углеродный след Cnet, т CO₂-экв./га','number','1.6']]},
 {code:'F2',name:'Управления удобрениями и обработкой почвы',desc:'Параметры внесения удобрений и интенсивности обработки почвы для сценарного анализа.',fields:[['f2fert','Норма удобрений, кг/га','number','180'],['f2soil','Интенсивность обработки почвы, %','number','70']]},
 {code:'F3',name:'Мониторинга и управления защитой растений',desc:'Параметры применения средств защиты и контроль связанного риска.',fields:[['f3pest','Пестициды, кг/га','number','4.5'],['f3risk','Индекс риска, %','number','25']]},
 {code:'F4',name:'Управления урожайностью и качеством продукции',desc:'Урожайность и показатель качества продукции по выбранному сценарию.',fields:[['f4yield','Урожайность, т/га','number','4.8'],['f4quality','Индекс качества, %','number','92']]},
 {code:'F5',name:'Оценки углеродного следа, прогнозирования, статистики, учета и отчетности',desc:'Сводные показатели выбросов, технологических операций и изменения углеродного следа.',fields:[['f5emission','Выбросы, кг CO₂-экв./га','number','2250'],['f5period','Период, лет','number','1']]},
 {code:'F6',name:'Принятия стратегических решений',desc:'Сценарий и целевой показатель для стратегической оценки.',fields:[['f6scenario','Сценарий','select',['Текущий расчёт','Оптимизация','Снижение углеродного следа']],['f6target','Целевой показатель, %','number','15']]}
];

/* Структура данных нижнего блока F1–F6 со всеми формулами */
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

function switchDashboard(mode){
  document.getElementById('btnCarbon').classList.toggle('active', mode==='carbon');
  document.getElementById('btnOrganic').classList.toggle('active', mode==='organic');
  document.getElementById('carbonView').classList.toggle('active', mode==='carbon');
  document.getElementById('organicView').classList.toggle('active', mode==='organic');
  document.getElementById('carbonNav').style.display = mode==='carbon'?'grid':'none';
  document.getElementById('organicNav').style.display = mode==='organic'?'grid':'none';
  if(mode==='organic') renderOrganicViews(); else renderCarbonCharts();
}

function renderFieldStats(){
  const f = document.getElementById('fieldSelector')?.value || "1";
  const s = FIELD_STATS[f] || FIELD_STATS["1"];
  document.getElementById('fieldName').textContent = "Поле " + f;
  document.getElementById('fieldCultures').textContent = s.cultures.join(' · ');
  document.getElementById('fieldTechs').textContent = "Технологии: " + s.techs.join(' · ');
  document.getElementById('fsArea').textContent = s.area;
  document.getElementById('fsYield').textContent = s.yield;
  document.getElementById('fsCf').textContent = s.cf;
  document.getElementById('fsGross').textContent = s.gross;
  document.getElementById('fsEff').textContent = s.eff;
}

function renderFilters(){
  document.getElementById('cultureFilter').innerHTML = CULTURES.map(c => `<label class="chip"><input type="checkbox" value="${c}" checked>${c}</label>`).join('');
  document.getElementById('techFilter').innerHTML = TECHS.map(t => `<label class="chip"><input type="checkbox" value="${t}" checked>${t}</label>`).join('');
}
function readFilters(){
  active.cultures=[...document.querySelectorAll("#cultureFilter input:checked")].map(x=>x.value);
  active.techs=[...document.querySelectorAll("#techFilter input:checked")].map(x=>x.value);
  if(!active.cultures.length)active.cultures=[...CULTURES];
  if(!active.techs.length)active.techs=[...TECHS];
}
function resetFilters(){
  active={cultures:[...CULTURES],techs:[...TECHS]};
  renderFilters();
  renderCarbonCharts();
}

/* Отрисовка верхнего блока F1–F6 */
function renderTopCalc(){
 const root=document.getElementById('calcGrid'); if(!root)return;
 root.innerHTML=CALC_FUNCS.map((f,i)=>{
   const fields=f.fields.map(x=> x[2]==='select' ? `<div class="calc-field"><label>${x[1]}</label><select id="${x[0]}">${x[3].map(v=>`<option>${v}</option>`).join('')}</select></div>` : `<div class="calc-field"><label>${x[1]}</label><input id="${x[0]}" type="number" value="${x[3]}" step="0.1"></div>`).join('');
   return `<article class="calc-card ${i===0?'open':''}" id="calc-${f.code}"><button class="calc-head" type="button" onclick="toggleCalc('${f.code}')"><span><span class="code">${f.code}</span><span class="name">подмодуль «${f.name}»</span></span><span class="chev">⌄</span></button><div class="calc-body"><div class="calc-desc">${f.desc}</div><div class="calc-fields">${fields}</div><div class="calc-actions"><button class="calc-save" type="button" onclick="saveCalc('${f.code}')">Сохранить параметры</button><button class="calc-clear" type="button" onclick="clearCalc('${f.code}')">Очистить</button></div><div class="calc-result" id="result-${f.code}"></div></div></article>`;
 }).join('');
 restoreCalc();
}
function toggleCalc(code){document.getElementById('calc-'+code).classList.toggle('open')}
function saveCalc(code){
 const f=CALC_FUNCS.find(x=>x.code===code); const vals={}; f.fields.forEach(x=>{const el=document.getElementById(x[0]); vals[x[0]]=el?el.value:''});
 localStorage.setItem('agro-'+code,JSON.stringify(vals));
 const r=document.getElementById('result-'+code); r.classList.add('visible');
 r.textContent=`Параметры ${code} сохранены в браузере.`;
}
function clearCalc(code){
 const f=CALC_FUNCS.find(x=>x.code===code); f.fields.forEach(x=>{const el=document.getElementById(x[0]); if(!el)return; if(x[2]==='select')el.selectedIndex=0; else el.value='';});
 localStorage.removeItem('agro-'+code); const r=document.getElementById('result-'+code); r.textContent='Поля очищены.'; r.classList.add('visible');
}
function restoreCalc(){
 CALC_FUNCS.forEach(f=>{const raw=localStorage.getItem('agro-'+f.code); if(!raw)return; try{const vals=JSON.parse(raw); f.fields.forEach(x=>{const el=document.getElementById(x[0]); if(el && vals[x[0]]!==undefined)el.value=vals[x[0]];});}catch(e){}});
}

/* Отрисовка нижнего блока F1–F6 */
function renderFunctions(){
 document.getElementById("fnGrid").innerHTML=fnData.map((f,i)=>{
   const subs=f[3]||[];
   const body=subs.length?`<p class="fn-intro">${f[2]}</p><div class="submods">${subs.map(x=>`<div class="submod"><h4>${x.title}</h4><div class="formula">${x.code}</div><div class="submod-row"><div><label>Значение</label><input id="${x.id}" type="number" step="0.01" value="${x.value}"><div class="unit">${x.unit}</div></div><div></div></div></div>`).join('')}</div><button class="fn-save" onclick="saveBottomFn('${f[0]}')">Сохранить значения</button><span class="fn-status" id="fn-status-${i}"></span>`:`<div class="fn-placeholder"><b>${f[0]}</b> — ${f[2]}</div>`;
   return `<div class="fn ${i===0?'open':''}" id="fn${i}"><button onclick="this.parentElement.classList.toggle('open')"><span><span class="code">${f[0]}</span><span class="name">подмодуль «${f[1]}»</span></span><span class="plus">+</span></button><div class="fn-body">${body}</div></div>`;
 }).join("");
 restoreBottomFns();
}
function saveBottomFn(code){
 const f=fnData.find(x=>x[0]===code); if(!f||!f[3].length)return;
 const vals={}; f[3].forEach(x=>{const el=document.getElementById(x.id); vals[x.id]=el?el.value:""});
 localStorage.setItem('bottom-'+code,JSON.stringify(vals));
 const idx=fnData.indexOf(f), status=document.getElementById('fn-status-'+idx); if(status)status.textContent='Значения сохранены';
}
function restoreBottomFns(){
 fnData.forEach((f,i)=>{const raw=localStorage.getItem('bottom-'+f[0]); if(!raw)return; try{const vals=JSON.parse(raw); (f[3]||[]).forEach(x=>{const el=document.getElementById(x.id); if(el&&vals[x.id]!==undefined)el.value=vals[x.id]}); const st=document.getElementById('fn-status-'+i); if(st)st.textContent='Сохранено';}catch(e){}});
}

function makeChart(id, type, data, options={}){
  if(charts[id]) charts[id].destroy();
  charts[id] = new Chart(document.getElementById(id), {type, data, options:{responsive:true,maintainAspectRatio:false,...options}});
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

function renderCarbonCharts(){
  readFilters();
  const rows=filtered(); updateKpis(rows); updateTables(); renderFieldStats();
  const cultures=CULTURES.filter(c=>active.cultures.includes(c));
  const techs=TECHS.filter(t=>active.techs.includes(t));

  makeChart('c1', 'bar', {
    labels: cultures,
    datasets: techs.map((t,i)=>({label:t, data:cultures.map(c=>avg(rows.filter(r=>r.culture===c&&r.technology===t).map(r=>n(r.footprint)))), backgroundColor:i?"#a93d72":"#4e91ad", borderRadius:4}))
  });
  const resource=[avg(rows.map(r=>n(r.operation_cf))),avg(rows.map(r=>n(r.tech_cf))),avg(rows.map(r=>n(r.rotation_cf)))];
  makeChart('c2', 'doughnut', {
    labels: ['Операции', 'Техника', 'Севооборот'],
    datasets: [{data: resource, backgroundColor: ['#4e91ad', '#a93d72', '#e49a27'], borderWidth: 2}]
  }, {cutout: '65%'});
  makeChart('c3', 'bar', {
    labels: cultures,
    datasets: [{label: 'Эффективность F6', data: cultures.map(c=>avg(rows.filter(r=>r.culture===c).map(r=>n(r.efficiency)))), backgroundColor: '#2d8b68', borderRadius: 5}]
  });
  makeChart('c4', 'bar', {
    labels: ['Уборка', 'Предпосевная обработка', 'Внесение удобрений'],
    datasets: [{label: 'кг CO₂-экв./га', data: [2422, 2236, 2024], backgroundColor: '#1e7655', borderRadius: 5}]
  }, {indexAxis: 'y'});
  makeChart('c5', 'scatter', {
    datasets: [{label:'Выбранные поля', data:rows.filter(r=>n(r.yield)>0).map(r=>({x:n(r.yield),y:n(r.footprint)})), backgroundColor:'#4e91ad', pointRadius:4}]
  }, {scales:{x:{title:{display:true,text:'Урожайность, т/га'}},y:{title:{display:true,text:'След, кг CO₂/т'}}}});
  makeChart('c6', 'bar', {
    labels: cultures,
    datasets: [
      {label: 'Удобрения', data: cultures.map(c=>avg(rows.filter(r=>r.culture===c).map(r=>n(r.fert)))), backgroundColor: '#e49a27'},
      {label: 'Пестициды', data: cultures.map(c=>avg(rows.filter(r=>r.culture===c).map(r=>n(r.pest)))), backgroundColor: '#a93d72'},
      {label: 'Топливо', data: cultures.map(c=>avg(rows.filter(r=>r.culture===c).map(r=>n(r.fuel)))), backgroundColor: '#4e91ad'}
    ]
  });
  makeChart('c7', 'line', {
    labels: ['Уборка', 'Предпосевная обработка', 'Внесение удобрений'],
    datasets: [{label: 'Изменение следа', data: [77.2, 0, 0], borderColor: '#2f7657', backgroundColor: 'rgba(47,118,87,.12)', fill: true, tension: .35}]
  });
  makeChart('c8', 'bar', {
    labels: cultures,
    datasets: [{label: 'Себестоимость тыс. руб./га', data: cultures.map(c=>avg(rows.filter(r=>r.culture===c).map(r=>n(r.cost)))), backgroundColor: '#7a6fb1', borderRadius: 5}]
  });
}

function renderOrganicViews(){
  const ring = (id, pct, okLabel, badLabel) => {
    document.getElementById(id).innerHTML = `
    <div class="ring-layout">
      <div class="ring" style="background:conic-gradient(#2d8b68 ${pct}%, #a93d72 ${pct}% 100%)">
        <div class="ring-center"><strong>${pct}%</strong><span style="font-size:11px;color:#71817b">соответствие</span></div>
      </div>
      <div class="ring-legend">
        <div style="font-size:13px"><b style="color:#2d8b68">■ ${pct}%</b> — ${okLabel}</div>
        <div style="font-size:13px"><b style="color:#a93d72">■ ${100-pct}%</b> — ${badLabel}</div>
      </div>
    </div>`;
  };
  ring('orgCompRing', 68, 'Глубина ≤ 5 см', 'Превышение глубины');
  ring('orgFertRing', 74, 'Органическое сырье', 'Запрещенная химия');

  const yields = [{c:'Озимая пшеница',y:5.5,u:4.9},{c:'Кукуруза',y:4.2,u:3.6},{c:'Многолетние травы',y:4.5,u:4.0},{c:'Горох',y:2.1,u:1.8},{c:'Подсолнечник',y:1.6,u:1.2},{c:'Лён',y:1.1,u:0.8}];
  document.getElementById('orgYieldBars').innerHTML = `<div class="comparison">` + yields.map(d => `
    <div class="comparison-row">
      <div style="font-weight:600;font-size:13px">${d.c}</div>
      <div class="measure-row">
        <div class="measure-track"><div class="measure-fill" style="width:${d.u/6*100}%;background:#2d8b68"></div></div>
        <div class="measure-number">${d.u} <small style="color:#71817b">т/га</small></div>
      </div>
    </div>`).join('') + `</div>`;

  const losses = [{s:'Жатва',min:0.12,mean:0.29,max:0.61},{s:'Обмолот',min:0.04,mean:0.08,max:0.15},{s:'Сепарация',min:0.08,mean:0.26,max:0.61}];
  document.getElementById('orgLossSummary').innerHTML = `<div class="loss-summary">` + losses.map(l => `
    <div class="loss-stage">
      <div style="display:flex;justify-content:space-between;font-size:13px"><b>${l.s}</b><small style="color:#71817b">т/га</small></div>
      <div class="loss-track">
        <div class="loss-range" style="left:${l.min/0.7*100}%;width:${(l.max-l.min)/0.7*100}%"></div>
        <div class="loss-mean" style="left:${l.mean/0.7*100}%"></div>
      </div>
      <div class="loss-values" style="font-size:11px">
        <div>Мин: <b>${l.min}</b></div><div style="text-align:center;color:#a93d72">Ср: <b>${l.mean}</b></div><div style="text-align:right">Макс: <b>${l.max}</b></div>
      </div>
    </div>`).join('') + `</div>`;

  const nitros = [{c:'Люцерна',v:175.2},{c:'Клевер',v:148.5},{c:'Соя',v:112.4},{c:'Горох',v:68.9}];
  document.getElementById('orgNitroBars').innerHTML = `<div class="comparison">` + nitros.map(d => `
    <div class="comparison-row">
      <div style="font-weight:600;font-size:13px">${d.c}</div>
      <div class="measure-row">
        <div class="measure-track"><div class="measure-fill" style="width:${d.v/200*100}%;background:#e49a27"></div></div>
        <div class="measure-number">${d.v} <small style="color:#71817b">кг/га</small></div>
      </div>
    </div>`).join('') + `</div>`;
}

function loadXlsx(e){
  const file = e.target.files[0];
  if(!file) return;
  const reader = new FileReader();
  reader.onload = evt => {
    const wb = XLSX.read(new Uint8Array(evt.target.result), {type:'array'});
    const isOrganic = wb.SheetNames.some(s => s.includes('280') || s.toLowerCase().includes('органик'));
    if(isOrganic){
      switchDashboard('organic');
    } else {
      const s4 = wb.Sheets["F4"], s5 = wb.Sheets["F5"], s6 = wb.Sheets["F6"];
      if(s4 && s5){
        const a4 = XLSX.utils.sheet_to_json(s4, {header:1, defval:null});
        const a5 = XLSX.utils.sheet_to_json(s5, {header:1, defval:null});
        const a6 = s6 ? XLSX.utils.sheet_to_json(s6, {header:1, defval:null}) : [];
        DATA.length = 0;
        for(let i=2; i<a4.length; i++){
          const r = a4[i]||[], r5 = a5[i]||[], r6 = a6[i]||[];
          const culture = String(r[1]||"").trim(), tech = String(r[2]||"").toLowerCase().startsWith("класс")?"Классическая":"No-Till";
          if(!culture) continue;
          DATA.push({culture, technology:tech, area:Number(r[10])||100, footprint:Number(r[14])||15, yield:Number(r[8])||4, operation_cf:Number(r[6])||50, tech_cf:Number(r[7])||100, rotation_cf:Number(r[8])||10, operation:String(r5[2]||"Уборка"), gross:Number(r5[6])||2200, fert:Number(r5[7])||12, pest:Number(r5[8])||2, fuel:Number(r5[9])||8, change_cf:Number(r5[10])||0, efficiency:Number(r6[2])||8, cost:Number(r6[25])||50});
        }
      }
      switchDashboard('carbon');
      renderFilters();
      renderCarbonCharts();
    }
  };
  reader.readAsArrayBuffer(file);
}

renderFilters();
renderTopCalc();
renderFunctions();
renderCarbonCharts();
</script>
</body>
</html>"""
