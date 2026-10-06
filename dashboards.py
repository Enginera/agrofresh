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

.comparison{display:grid;gap:14px;padding-top:6px}.comparison-row{display:grid;grid-template-columns:150px 1fr;gap:14px;align-items:center}.measure-row{display:flex;align-items:center;gap:10px}.measure-track{height:16px;flex:1;background:#edf3ef;border-radius:5px;overflow:hidden}.measure-fill{height:100%;border-radius:5px}.measure-number{font-size:14px;font-weight:750;min-width:90px;text-align:right}
.ring-layout{display:flex;align-items:center;gap:20px;padding:10px 0}.ring{width:160px;height:160px;border-radius:50%;display:grid;place-items:center;flex-shrink:0}.ring-center{width:115px;height:115px;border-radius:50%;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center}.ring-center strong{font-size:24px}.ring-legend{display:grid;gap:12px;flex:1}
.loss-summary{padding:6px 0}.loss-stage{padding:0 6px 14px}.loss-track{position:relative;height:6px;background:#f0f1ed;border-radius:4px;margin:14px 0 10px}.loss-range{position:absolute;top:0;height:6px;background:#dba5c2;border-radius:4px}.loss-mean{position:absolute;top:-4px;width:14px;height:14px;border:3px solid white;background:#a93d72;border-radius:50%;transform:translateX(-50%)}.loss-values{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}

.view-container{display:none}.view-container.active{display:block}
@media(max-width:1100px){.app{grid-template-columns:1fr}.sidebar{height:auto;position:relative}.field-summary{grid-template-columns:repeat(3,1fr)}}
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
    <a class="active" href="#dashboard">Главная</a>
    <a href="#charts">Аналитика выбросов</a>
    <a href="#tables">Культура и технологии</a>
  </nav>
  <nav class="nav" id="organicNav" style="display:none">
    <a class="active" href="#orgOverview">Обзор норм</a>
    <a href="#orgHarvest">Урожай и потери</a>
    <a href="#orgCompliance">ФЗ-280 регламент</a>
  </nav>
  <div class="side-note">Файлы переключают режим на лету.<br>Пересчёт формул без перезагрузки страницы.</div>
</aside>

<main id="carbonView" class="view-container active">
  <div class="top">
    <div><div class="eyebrow">Модуль углеродной нейтральности</div><h1>Углеродно-нейтральное земледелие (F1–F6)</h1><div class="subtitle">Анализ углеродного следа, секвестрации и себестоимости по полям</div></div>
    <div class="actions"><label class="btn">Загрузить Excel<input type="file" onchange="loadXlsx(event)" accept=".xlsx,.xls" hidden></label><button class="btn" onclick="renderCarbonCharts()">Сбросить</button><button class="btn primary" onclick="window.print()">Печать</button></div>
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

  <section class="kpis">
    <div class="kpi"><div class="label">Средний чистый след</div><div class="value" id="kpiFoot">13.5</div><div class="hint">кг CO₂-экв./т</div></div>
    <div class="kpi"><div class="label">Средняя эффективность</div><div class="value" id="kpiEff">6.70</div><div class="hint">показатель F6</div></div>
    <div class="kpi"><div class="label">Площадь выборки</div><div class="value" id="kpiArea">118.1</div><div class="hint">га, в среднем</div></div>
    <div class="kpi"><div class="label">Себестоимость</div><div class="value" id="kpiCost">52.0</div><div class="hint">тыс. руб./га</div></div>
  </section>

  <section id="charts" class="grid">
    <article class="card wide"><div class="head"><h2>Удельный след: No-Till vs Классическая</h2><p>кг CO₂-экв./т</p></div><div class="chartbox"><canvas id="c1"></canvas></div></article>
    <article class="card"><div class="head"><h2>Структура выбросов по ресурсам</h2></div><div class="chartbox"><canvas id="c2"></canvas></div></article>
    <article class="card"><div class="head"><h2>Эффективность по культуре (F6)</h2></div><div class="chartbox"><canvas id="c3"></canvas></div></article>
    <article class="card wide"><div class="head"><h2>Выбросы CO₂ по технологическим операциям</h2><p>кг CO₂-экв./га</p></div><div class="chartbox"><canvas id="c4"></canvas></div></article>
  </section>
</main>

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

  <section class="grid">
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
    <article class="card">
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
  "1": {cultures: ["Лён", "Многолетние травы", "Озимая пшеница", "Подсолнечник"], techs: ["No-Till", "Классическая"], area: "118.1 га", yield: "4.70 т/га", cf: "13.54", gross: "2 184.8", eff: "6.70"},
  "2": {cultures: ["Горох", "Многолетние травы", "Озимая пшеница"], techs: ["No-Till", "Классическая"], area: "113.0 га", yield: "5.70 т/га", cf: "6.44", gross: "2 147.6", eff: "7.48"},
  "3": {cultures: ["Горох", "Озимая пшеница", "Подсолнечник"], techs: ["No-Till", "Классическая"], area: "126.0 га", yield: "4.18 т/га", cf: "20.64", gross: "2 257.8", eff: "5.68"},
  "4": {cultures: ["Горох", "Многолетние травы", "Озимая пшеница"], techs: ["No-Till", "Классическая"], area: "121.1 га", yield: "6.16 т/га", cf: "14.92", gross: "2 200.8", eff: "6.33"},
  "5": {cultures: ["Горох", "Лён", "Озимая пшеница", "Подсолнечник"], techs: ["No-Till"], area: "115.0 га", yield: "4.23 т/га", cf: "36.67", gross: "2 279.2", eff: "5.86"}
};

const CULTURES = ["Озимая пшеница","Горох","Кукуруза","Многолетние травы","Подсолнечник","Лён"];
const TECHS = ["Классическая","No-Till"];
const charts = {};

function switchDashboard(mode){
  document.getElementById("btnCarbon").classList.toggle("active", mode==="carbon");
  document.getElementById("btnOrganic").classList.toggle("active", mode==="organic");
  document.getElementById("carbonView").classList.toggle("active", mode==="carbon");
  document.getElementById("organicView").classList.toggle("active", mode==="organic");
  document.getElementById("carbonNav").style.display = mode==="carbon"?"grid":"none";
  document.getElementById("organicNav").style.display = mode==="organic"?"grid":"none";
  if(mode==="organic") renderOrganicViews(); else renderCarbonCharts();
}

function renderFieldStats(){
  const f = document.getElementById("fieldSelector").value;
  const s = FIELD_STATS[f] || FIELD_STATS["1"];
  document.getElementById("fieldName").textContent = "Поле " + f;
  document.getElementById("fieldCultures").textContent = s.cultures.join(" · ");
  document.getElementById("fieldTechs").textContent = "Технологии: " + s.techs.join(" · ");
  document.getElementById("fsArea").textContent = s.area;
  document.getElementById("fsYield").textContent = s.yield;
  document.getElementById("fsCf").textContent = s.cf;
  document.getElementById("fsGross").textContent = s.gross;
  document.getElementById("fsEff").textContent = s.eff;
}

function renderFilters(){
  document.getElementById("cultureFilter").innerHTML = CULTURES.map(c => `<label class="chip"><input type="checkbox" value="${c}" checked>${c}</label>`).join("");
  document.getElementById("techFilter").innerHTML = TECHS.map(t => `<label class="chip"><input type="checkbox" value="${t}" checked>${t}</label>`).join("");
}

function makeChart(id, type, data, options={}){
  if(charts[id]) charts[id].destroy();
  charts[id] = new Chart(document.getElementById(id), {type, data, options:{responsive:true,maintainAspectRatio:false,...options}});
}

function renderCarbonCharts(){
  renderFieldStats();
  makeChart("c1", "bar", {
    labels: CULTURES,
    datasets: [
      {label: "No-Till", data: [7.46, 6.24, 12.5, 16.70, 45.2, 95.18], backgroundColor: "#4e91ad", borderRadius: 4},
      {label: "Классическая", data: [13.53, 16.56, 16.96, 22.4, 54.35, 120.4], backgroundColor: "#a93d72", borderRadius: 4}
    ]
  });
  makeChart("c2", "doughnut", {
    labels: ["Операции", "Техника", "Севооборот"],
    datasets: [{data: [50, 100, 10], backgroundColor: ["#4e91ad", "#a93d72", "#e49a27"], borderWidth: 2}]
  }, {cutout: "65%"});
  makeChart("c3", "bar", {
    labels: CULTURES,
    datasets: [{label: "Эффективность F6", data: [10.37, 5.60, 6.50, 9.10, 4.80, 4.16], backgroundColor: "#2d8b68", borderRadius: 5}]
  });
  makeChart("c4", "bar", {
    labels: ["Уборка", "Предпосевная обработка", "Внесение удобрений"],
    datasets: [{label: "кг CO₂-экв./га", data: [2422, 2236, 2024], backgroundColor: "#1e7655", borderRadius: 5}]
  }, {indexAxis: "y"});
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
  ring("orgCompRing", 68, "Глубина ≤ 5 см", "Превышение глубины");
  ring("orgFertRing", 74, "Органическое сырье", "Запрещенная химия");

  const yields = [{c:"Озимая пшеница",u:4.9},{c:"Кукуруза",u:3.6},{c:"Многолетние травы",u:4.0},{c:"Горох",u:1.8},{c:"Подсолнечник",u:1.2},{c:"Лён",u:0.8}];
  document.getElementById("orgYieldBars").innerHTML = `<div class="comparison">` + yields.map(d => `
    <div class="comparison-row">
      <div style="font-weight:600;font-size:13px">${d.c}</div>
      <div class="measure-row">
        <div class="measure-track"><div class="measure-fill" style="width:${d.u/6*100}%;background:#2d8b68"></div></div>
        <div class="measure-number">${d.u} <small style="color:#71817b">т/га</small></div>
      </div>
    </div>`).join("") + `</div>`;

  const losses = [{s:"Жатва",min:0.12,mean:0.29,max:0.61},{s:"Обмолот",min:0.04,mean:0.08,max:0.15},{s:"Сепарация",min:0.08,mean:0.26,max:0.61}];
  document.getElementById("orgLossSummary").innerHTML = `<div class="loss-summary">` + losses.map(l => `
    <div class="loss-stage">
      <div style="display:flex;justify-content:space-between;font-size:13px"><b>${l.s}</b><small style="color:#71817b">т/га</small></div>
      <div class="loss-track">
        <div class="loss-range" style="left:${l.min/0.7*100}%;width:${(l.max-l.min)/0.7*100}%"></div>
        <div class="loss-mean" style="left:${l.mean/0.7*100}%"></div>
      </div>
      <div class="loss-values" style="font-size:11px">
        <div>Мин: <b>${l.min}</b></div><div style="text-align:center;color:#a93d72">Ср: <b>${l.mean}</b></div><div style="text-align:right">Макс: <b>${l.max}</b></div>
      </div>
    </div>`).join("") + `</div>`;

  const nitros = [{c:"Люцерна",v:175.2},{c:"Клевер",v:148.5},{c:"Соя",v:112.4},{c:"Горох",v:68.9}];
  document.getElementById("orgNitroBars").innerHTML = `<div class="comparison">` + nitros.map(d => `
    <div class="comparison-row">
      <div style="font-weight:600;font-size:13px">${d.c}</div>
      <div class="measure-row">
        <div class="measure-track"><div class="measure-fill" style="width:${d.v/200*100}%;background:#e49a27"></div></div>
        <div class="measure-number">${d.v} <small style="color:#71817b">кг/га</small></div>
      </div>
    </div>`).join("") + `</div>`;
}

function loadXlsx(e){
  const file = e.target.files[0];
  if(!file) return;
  const reader = new FileReader();
  reader.onload = evt => {
    const wb = XLSX.read(new Uint8Array(evt.target.result), {type:"array"});
    const isOrganic = wb.SheetNames.some(s => s.includes("280") || s.toLowerCase().includes("органик"));
    switchDashboard(isOrganic ? "organic" : "carbon");
  };
  reader.readAsArrayBuffer(file);
}

renderFilters();
renderCarbonCharts();
</script>
</body>
</html>"""
