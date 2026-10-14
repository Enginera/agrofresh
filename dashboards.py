"""Сборка единой панели из эталонных HTML (carbon / organic)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / "assets"

# Пустые FIELD_STATS на 5 полей — без демо-цифр
_EMPTY_FIELD_STATS = {
    str(i): {
        "records": 0,
        "area_avg": None,
        "yield_avg": None,
        "cf_avg": None,
        "gross_avg": None,
        "eff_avg": None,
        "cost_avg": None,
        "cultures": [],
        "techs": [],
        "year_records": {},
    }
    for i in range(1, 6)
}

_EMPTY_ORGANIC_DATA = {"f1": [], "f2": [], "f3": [], "f4": [], "f5": []}

# Верхние F1–F6 = бывшие нижние расчётные функции (fnData), без дубля
_CARBON_RENDER_TOP_CALC = r"""
function renderTopCalc(){
  const root = document.getElementById('calcGrid');
  if(!root || typeof fnData === 'undefined') return;
  root.innerHTML = fnData.map((f, i) => {
    const code = 'F' + (i + 1);
    const subs = f[3] || [];
    const fields = subs.length
      ? `<div class="calc-desc">${f[2]}</div><div class="submods">${subs.map(x =>
          `<div class="submod"><h4>${x.title}</h4><div class="formula">${x.code}</div>` +
          `<div class="submod-row"><div><label>Изменяемое значение</label>` +
          `<input id="${x.id}" type="number" step="0.01" value="${x.value}">` +
          `<div class="unit">${x.unit}</div></div></div></div>`
        ).join('')}</div>` +
        `<div class="calc-actions">` +
        `<button class="calc-save" type="button" onclick="saveBottomFn('${f[0]}')">Сохранить параметры</button>` +
        `<button class="calc-clear" type="button" onclick="clearMergedFn('${f[0]}','${code}')">Очистить</button>` +
        `</div><div class="calc-result" id="result-${code}"></div>` +
        `<span class="fn-status" id="fn-status-${i}"></span>`
      : `<div class="calc-desc">${f[2]}</div>`;
    return `<article class="calc-card" id="calc-${code}">` +
      `<button class="calc-head" type="button" onclick="toggleCalc('${code}')">` +
      `<span><span class="code">${code}</span><span class="name">подмодуль «${f[1]}»</span></span>` +
      `<span class="chev">⌄</span></button><div class="calc-body">${fields}</div></article>`;
  }).join('');
  if(typeof restoreBottomFns === 'function') restoreBottomFns();
}
"""

_CARBON_RENDER_FUNCTIONS_NOP = r"""
function renderFunctions(){ /* нижний блок убран — всё в верхних F1–F6 */ }
"""

# Надёжный парсер углеродного модуля (F1/F1 1000, разные заголовки 5 полей / 1000)
_CARBON_LOAD_FN = r"""
function agroFindSheet(wb, code){
  const names = wb.SheetNames || [];
  const exact = names.find(n => String(n).trim().toUpperCase() === code);
  if(exact) return wb.Sheets[exact];
  const re = new RegExp('^' + code + '(?:\\b|\\s|$)', 'i');
  const hit = names.find(n => re.test(String(n).trim()));
  return hit ? wb.Sheets[hit] : null;
}
function agroNormHeader(v){
  return String(v ?? '')
    .toLowerCase()
    .replace(/ё/g, 'е')
    .replace(/[₂]/g, '2')
    .replace(/со2|co2/g, 'co2')
    .replace(/[^a-zа-я0-9]+/g, '');
}
function agroFindCol(headerRow, needles){
  const cells = (headerRow || []).map(agroNormHeader);
  for(const needle of needles){
    const n = agroNormHeader(needle);
    if(!n) continue;
    let i = cells.findIndex(h => h === n);
    if(i >= 0) return i;
    i = cells.findIndex(h => h && h.includes(n));
    if(i >= 0) return i;
  }
  return -1;
}
function agroNum(row, idx){
  if(idx < 0) return 0;
  const v = row[idx];
  return typeof v === 'number' && Number.isFinite(v) ? v : (Number(v) || 0);
}
function agroColMean(rows, colIdx){
  if(colIdx < 0) return null;
  const vals = [];
  for(let i = 0; i < rows.length; i++){
    const v = rows[i] && rows[i][colIdx];
    if(typeof v === 'number' && Number.isFinite(v)) vals.push(v);
  }
  return vals.length ? vals.reduce((a,b)=>a+b,0)/vals.length : null;
}
function agroSheetRows(arr){
  // строки данных: первая ячейка — число (№ записи), без заголовков «Поле N»
  const out = [];
  for(let i = 2; i < arr.length; i++){
    const r = arr[i] || [];
    if(typeof r[0] === 'number' && Number.isFinite(r[0])) out.push(r);
  }
  return out;
}
function agroSetInput(id, value, digits){
  if(value === null || value === undefined || !Number.isFinite(Number(value))) return;
  const el = document.getElementById(id);
  const n = Number(value);
  const text = (digits === 0) ? String(Math.round(n)) : n.toFixed(digits === undefined ? 2 : digits);
  if(el){ el.value = text; el.dataset.fromExcel = '1'; }
  // обновить fnData / чтобы повторный render не обнулял
  if(typeof fnData !== 'undefined'){
    fnData.forEach(block => (block[3]||[]).forEach(f => { if(f.id === id) f.value = text; }));
  }
}
function agroClearModuleStorage(){
  try{
    Object.keys(localStorage).forEach(k => {
      if(k.startsWith('agro-') || k.startsWith('bottom-')) localStorage.removeItem(k);
    });
  }catch(e){}
}
function fillAllModulesFromExcel(a1,a2,a3,a4,a5,a6){
  const r1 = agroSheetRows(a1), r2 = agroSheetRows(a2||[]), r3 = agroSheetRows(a3||[]);
  const mean = (arr, key) => {
    const src = arr === DATA
      ? DATA.filter(r => !window.agroFieldCount || !r.field || r.field <= window.agroFieldCount)
      : arr;
    const vals = src.map(x => Number(x[key])).filter(Number.isFinite);
    return vals.length ? vals.reduce((a,b)=>a+b,0)/vals.length : null;
  };
  // --- верхний блок CALC ---
  const area = mean(DATA, 'area'), yld = mean(DATA, 'yield'), foot = mean(DATA, 'footprint');
  const fert = mean(DATA, 'fert'), pest = mean(DATA, 'pest'), eff = mean(DATA, 'efficiency');
  const cost = mean(DATA, 'cost'), gross = mean(DATA, 'gross'), chg = mean(DATA, 'change_cf');
  const opcf = mean(DATA, 'operation_cf');
  agroSetInput('f1area', area, 1);
  agroSetInput('f1cseq', agroColMean(r1, 2), 2); // Csequestered
  agroSetInput('f1cnet', agroColMean(r1, 3), 2); // Cnet
  agroSetInput('f2fert', fert, 1);
  agroSetInput('f2soil', agroColMean(r2, 2), 1); // глубина H как интенсивность-прокси
  agroSetInput('f3pest', pest, 1);
  agroSetInput('f3risk', agroColMean(r3, 3), 1); // УЗ %
  agroSetInput('f4yield', yld, 2);
  agroSetInput('f4quality', 92, 0);
  agroSetInput('f5emission', gross, 0);
  agroSetInput('f5period', 1, 0);
  agroSetInput('f6target', 15, 0);
  // --- нижние подмодули F.1–F.6 ---
  agroSetInput('f1_cseq', agroColMean(r1, 2), 2);
  agroSetInput('f1_cnet', agroColMean(r1, 3), 2);
  agroSetInput('f1_e', agroColMean(r1, 7), 2);
  agroSetInput('f2_ktemp', agroColMean(r2, 4), 2);
  agroSetInput('f2_kvl', agroColMean(r2, 5), 2);
  agroSetInput('f2_wfact', agroColMean(r2, 18), 1);
  agroSetInput('f2_wopt', agroColMean(r2, 18) !== null ? agroColMean(r2, 18) * 1.1 : 27, 1);
  agroSetInput('f2_wcrit', agroColMean(r2, 19), 1);
  agroSetInput('f2_iat', agroColMean(r2, 6), 2);
  agroSetInput('f2_cf', agroColMean(r2, 14), 2);
  agroSetInput('f2_dc', agroColMean(r2, 11), 1);
  agroSetInput('f3_uz', agroColMean(r3, 3), 1);
  agroSetInput('f3_ipv', agroColMean(r3, 9), 2);
  agroSetInput('f3_d', agroColMean(r3, 20) ?? agroColMean(r3, 5), 2);
  agroSetInput('f3_ip', agroColMean(r3, 6), 1);
  agroSetInput('f3_i', agroColMean(r3, 16), 0);
  agroSetInput('f3_cseason', agroColMean(r3, 21) ?? agroColMean(r3, 12), 1);
  agroSetInput('f4_op', mean(DATA, 'rotation_cf') !== null ? (mean(DATA,'yield')||0)*0.08 : 0.4, 2);
  agroSetInput('f4_ufin', yld, 2);
  agroSetInput('f4_cfuy', opcf, 1);
  agroSetInput('f4_cfitog', foot, 1);
  agroSetInput('f4_dcs', -Math.abs(opcf||100)*1.5, 1);
  agroSetInput('f4_sco2', -Math.abs(opcf||100)*0.8, 1);
  agroSetInput('f4_qf', 92, 0);
  agroSetInput('f5_uco2', foot !== null ? foot/1000 : null, 2);
  agroSetInput('f5_eco2', opcf, 0);
  agroSetInput('f5_oco2', gross, 0);
  agroSetInput('f5_cem', gross !== null && opcf !== null ? gross*0.9 : null, 0);
  agroSetInput('f5_ctotal', gross, 0);
  agroSetInput('f5_change', chg, 1);
  agroSetInput('f5_effsec', cost !== null ? cost*1.2 : null, 1);
  agroSetInput('f6_keff', eff !== null ? Math.min(1, eff/10) : 0.86, 2);
  agroSetInput('f6_pi', foot !== null && cost !== null && cost !== 0 ? foot/cost : 0.42, 2);
  agroSetInput('f6_cfield', foot, 1);
  agroSetInput('f6_op', yld !== null ? yld*0.08 : 0.38, 2);
  agroSetInput('f6_ynet', yld !== null ? yld*1000 : null, 0);
  agroSetInput('f6_e', eff, 2);
  agroSetInput('f6_cost', cost, 1);
  agroSetInput('f6_fert', fert !== null ? fert/10 : null, 1);
  // если из Excel ничего нет — вернуть дефолты карточки, чтобы развёрнутый вид не был пустым
  if(typeof CALC_FUNCS !== 'undefined'){
    CALC_FUNCS.forEach(f => (f.fields || []).forEach(x => {
      const el = document.getElementById(x[0]);
      if(!el) return;
      if(x[2] === 'select'){
        if(!el.value && el.options && el.options.length) el.selectedIndex = 0;
        return;
      }
      if(String(el.value || '').trim() === '') el.value = x[3];
    }));
  }
  // подпись результата в calc-карточках
  ['F1','F2','F3','F4','F5','F6'].forEach(code => {
    const r = document.getElementById('result-'+code);
    if(r){ r.classList.add('visible'); r.textContent = 'Рассчитано из Excel. Можно править вручную.'; }
  });
  document.querySelectorAll('#calcGrid .fn-status, #fnGrid .fn-status').forEach(st => { st.textContent = 'Из Excel · можно править'; });
}
function agroFieldNo(cell){
  if(typeof cell !== 'string') return 0;
  const m = /^поле\s*(\d+)/i.exec(cell.trim());
  return m ? Number(m[1]) : 0;
}
function agroMaxFields(arrs){
  let max = 0;
  arrs.forEach(arr => (arr || []).forEach(r => { const n = agroFieldNo(r && r[0]); if(n > max) max = n; }));
  return max || 1;
}
function agroSliceFields(arr, count){
  const out = [];
  let field = 1, seen = false;
  (arr || []).forEach(r => {
    const row = r || [];
    const n = agroFieldNo(row[0]);
    if(n){ field = n; seen = true; if(field <= count) out.push(row); return; }
    if(!seen || field <= count) out.push(row);
  });
  return out;
}
function agroSyncFieldCount(count, refill){
  count = Math.max(1, Math.min(count, window.agroFieldMax || 1));
  window.agroFieldCount = count;
  const box = document.getElementById('agroFieldCount');
  if(box && box.value !== String(count)) box.value = String(count);
  const hint = document.getElementById('agroFieldCountHint');
  if(hint) hint.textContent = 'В таблице максимум ' + (window.agroFieldMax || 1);
  const pick = document.getElementById('fieldSelector');
  if(pick){
    const prev = Number(pick.value) || 1;
    pick.innerHTML = Array.from({length: count}, (_, i) => '<option value="' + (i + 1) + '">Поле ' + (i + 1) + '</option>').join('');
    pick.value = String(Math.min(prev, count));
  }
  const src = window.agroSheets;
  const cut = key => agroSliceFields(src ? src[key] : [], count);
  if(src && typeof buildFieldStatsFromArrays === 'function'){
    if(buildFieldStatsFromArrays.length >= 4) buildFieldStatsFromArrays(cut('a1'), cut('a4'), cut('a5'), cut('a6'));
    else buildFieldStatsFromArrays(cut('a4'), cut('a5'), cut('a6'));
  }
  if(refill && src && typeof fillAllModulesFromExcel === 'function'){
    if(typeof fnData !== 'undefined'){
      fnData.forEach(block => (block[3] || []).forEach(f => { f.value = ''; }));
    }
    document.querySelectorAll('#calcGrid input, #fnGrid input').forEach(el => {
      el.value = '';
      delete el.dataset.fromExcel;
    });
    fillAllModulesFromExcel(cut('a1'), cut('a2'), cut('a3'), cut('a4'), cut('a5'), cut('a6'));
  }
  if(typeof renderFieldStats === 'function') renderFieldStats();
  document.querySelectorAll('.agro-empty').forEach(el => el.remove());
  document.querySelectorAll('.chartbox canvas').forEach(cv => { cv.style.display = ''; });
  try { renderCharts(); } catch (err) {}
  const badge = document.getElementById('agroModeBadge');
  if(badge){
    const n = typeof filtered === 'function' ? filtered().length : DATA.length;
    badge.textContent = 'Углеродно-нейтральное земледелие · ' + count + ' пол. · ' + n + ' строк';
  }
}
function loadExternalExcel(file){
  if(window.parent !== window && !window.__agroShellLoad){
    file.arrayBuffer().then(buf => parent.postMessage({type:'agro-file', buffer: buf, name: file.name}, '*'));
    return;
  }
  const reader = new FileReader();
  reader.onload = e => {
    const wb = XLSX.read(new Uint8Array(e.target.result), {type: 'array'});
    const s1 = agroFindSheet(wb, 'F1');
    const s2 = agroFindSheet(wb, 'F2');
    const s3 = agroFindSheet(wb, 'F3');
    const s4 = agroFindSheet(wb, 'F4');
    const s5 = agroFindSheet(wb, 'F5');
    const s6 = agroFindSheet(wb, 'F6');
    if(!s1 || !s4 || !s5 || !s6){
      alert('В файле должны быть листы F1, F4, F5 и F6 (допустимо «F1 1000»).');
      return;
    }
    const a1 = XLSX.utils.sheet_to_json(s1, {header: 1, defval: null});
    const a2 = s2 ? XLSX.utils.sheet_to_json(s2, {header: 1, defval: null}) : [];
    const a3 = s3 ? XLSX.utils.sheet_to_json(s3, {header: 1, defval: null}) : [];
    const a4 = XLSX.utils.sheet_to_json(s4, {header: 1, defval: null});
    const a5 = XLSX.utils.sheet_to_json(s5, {header: 1, defval: null});
    const a6 = XLSX.utils.sheet_to_json(s6, {header: 1, defval: null});
    window.agroSheets = {a1, a2, a3, a4, a5, a6};
    const h4 = a4[1] || [];
    const h5 = a5[1] || [];
    const h6 = a6[1] || [];
    const cCulture = agroFindCol(h4, ['Культура']);
    const cTech = agroFindCol(h4, ['Технология']);
    const cArea = agroFindCol(h4, ['Площадь поля, F, га', 'Площадь поля']);
    const cYield = agroFindCol(h4, ['Уфакт', 'Фактическая урожайность', 'Фактический урожайность']);
    const cFoot = agroFindCol(h4, ['CFитого', 'CFитог', 'углеродного следа на тонну']);
    const cOpCf = agroFindCol(h4, ['CFуб', 'углеродного след технологической']);
    const cTechCf = agroFindCol(h4, ['CFтех', 'след от работы техники']);
    const cRotCf = agroFindCol(h4, ['CFлог', 'след логистики']);
    const cOp = agroFindCol(h5, ['Операция']);
    const cGross = agroFindCol(h5, ['Общие валовые выбросы', 'валовые выбросы']);
    const cFert = agroFindCol(h5, ['Cfert', 'от удобрений']);
    const cPest = agroFindCol(h5, ['Cpest', 'от пестицидов']);
    const cFuel = agroFindCol(h5, ['Cfuel', 'от топлива']);
    const cChange = agroFindCol(h5, ['Изменение углеродного следа', 'Сводный']);
    const cEff = agroFindCol(h6, ['Эффективность']);
    const cCost = agroFindCol(h6, ['Себестоимость по заданным полям', 'Себестоимость']);
    const canon = x => ({
      'Лён':'Лён','лён':'Лён',
      'озимая пшеница':'Озимая пшеница','Озимая пшеница':'Озимая пшеница',
      'Горох':'Горох','горох':'Горох',
      'кукуруза':'Кукуруза','Кукуруза':'Кукуруза',
      'многолетние травы':'Многолетние травы','Многолетние травы':'Многолетние травы',
      'подсолнечник':'Подсолнечник','Подсолнечник':'Подсолнечник'
    }[String(x || '').trim()] || String(x || '').trim());
    DATA.length = 0;
    let dataField = 1;
    for(let i = 2; i < a4.length; i++){
      const r = a4[i] || [], r5 = a5[i] || [], r6 = a6[i] || [];
      const marked = agroFieldNo(r[0]);
      if(marked){ dataField = marked; continue; }
      const culture = canon(cCulture >= 0 ? r[cCulture] : r[1]);
      if(!CULTURES.includes(culture)) continue;
      const techRaw = String((cTech >= 0 ? r[cTech] : r[2]) || '').toLowerCase();
      const tech = techRaw.startsWith('класс') ? 'Классическая' : 'No-Till';
      DATA.push({
        culture,
        technology: tech,
        area: agroNum(r, cArea >= 0 ? cArea : 10),
        footprint: agroNum(r, cFoot >= 0 ? cFoot : 14),
        yield: agroNum(r, cYield >= 0 ? cYield : 8),
        operation_cf: agroNum(r, cOpCf >= 0 ? cOpCf : 11),
        tech_cf: agroNum(r, cTechCf >= 0 ? cTechCf : 12),
        rotation_cf: agroNum(r, cRotCf >= 0 ? cRotCf : 13),
        operation: String((cOp >= 0 ? r5[cOp] : r5[2]) || ''),
        gross: agroNum(r5, cGross >= 0 ? cGross : 6),
        fert: agroNum(r5, cFert >= 0 ? cFert : 15),
        pest: agroNum(r5, cPest >= 0 ? cPest : 16),
        fuel: agroNum(r5, cFuel >= 0 ? cFuel : 17),
        change_cf: agroNum(r5, cChange >= 0 ? cChange : 19),
        efficiency: agroNum(r6, cEff >= 0 ? cEff : 2),
        cost: agroNum(r6, cCost >= 0 ? cCost : 25),
        field: dataField
      });
    }
    if(!DATA.length){
      alert('Не удалось разобрать строки Excel. Проверьте листы F4–F6.');
      return;
    }
    // предыдущий файл не должен оставаться в полях: fnData хранит последние числа
    if(typeof fnData !== 'undefined'){
      fnData.forEach(block => (block[3]||[]).forEach(f => { f.value = ''; }));
    }
    agroClearModuleStorage();
    active = {cultures: [...CULTURES], techs: [...TECHS]};
    const season = document.getElementById('season');
    if(season) season.selectedIndex = 0;
    renderFilters();
    renderTopCalc();
    renderFunctions();
    window.agroFieldMax = agroMaxFields([a1, a2, a3, a4, a5, a6]);
    const box = document.getElementById('agroFieldCount');
    if(box){
      box.innerHTML = Array.from({length: window.agroFieldMax}, (_, i) => '<option value="' + (i + 1) + '">' + (i + 1) + '</option>').join('');
      box.value = String(window.agroFieldMax);
      box.onchange = () => agroSyncFieldCount(Number(box.value), true);
    }
    agroSyncFieldCount(window.agroFieldMax, true);
  };
  reader.readAsArrayBuffer(file);
}
"""

_CARBON_MSG_JS = r"""
window.addEventListener('message', ev => {
  if(!ev.data || ev.data.type !== 'agro-load') return;
  const file = new File([ev.data.buffer], ev.data.name || 'data.xlsx');
  window.__agroShellLoad = true;
  try { loadExternalExcel(file); }
  finally { window.__agroShellLoad = false; }
});
"""

# Скролл внутри iframe + рабочие пункты бокового меню (F1–F6)
_CARBON_SCROLL_CSS = r"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
<style id="agro-scroll-fix">
/* ===== layout: сайдбар на месте, скролл только в main ===== */
html, body {
  height: 100% !important;
  max-height: 100% !important;
  overflow: hidden !important;
  scroll-behavior: smooth;
}
.app {
  height: 100vh !important;
  max-height: 100vh !important;
  overflow: hidden !important;
  align-items: stretch !important;
  grid-template-columns: 260px minmax(0, 1fr) !important;
}
.sidebar {
  position: relative !important;
  top: auto !important;
  height: 100% !important;
  max-height: 100vh !important;
  overflow-x: hidden !important;
  overflow-y: auto !important;
  overscroll-behavior: contain;
  display: flex !important;
  flex-direction: column !important;
}
main {
  height: 100% !important;
  max-height: 100vh !important;
  overflow-x: hidden !important;
  overflow-y: auto !important;
  overscroll-behavior: contain;
  background: transparent !important;
}
.nav a { cursor: pointer; }
.nav a.agro-sub { font-size: 12px; padding-left: 22px; opacity: .92; }

/* ===== dark carbon (по умолчанию) ===== */
:root, html.agro-theme-dark {
  --bg: #0a0e0c;
  --card: #141a17;
  --ink: #e8f0eb;
  --muted: #8fa399;
  --green: #1a9b63;
  --green2: #127a4d;
  --mint: #1a2a22;
  --line: #24302a;
  --shadow: 0 10px 28px rgba(0,0,0,.45);
  --carbon-edge: #2ee59d;
}
html.agro-theme-dark body, body {
  color: var(--ink) !important;
  font-family: Manrope, Segoe UI, sans-serif !important;
  background-color: #0a0e0c !important;
  background-image:
    radial-gradient(1200px 500px at 80% -10%, rgba(26,155,99,.16), transparent 55%),
    radial-gradient(900px 420px at 10% 0%, rgba(11,92,61,.18), transparent 50%),
    linear-gradient(180deg, #0a0e0c 0%, #0d1210 55%, #0a0e0c 100%) !important;
}
h1, h2, h3, .calc-head .code, .brand b, .kpi .value {
  font-family: Rajdhani, Manrope, sans-serif !important;
  letter-spacing: .02em;
}
html.agro-theme-dark .sidebar, .sidebar {
  color: #d7e6dd !important;
  border-right: 1px solid rgba(46,229,157,.12);
  background-color: #080c0a !important;
  background-image:
    linear-gradient(135deg, rgba(255,255,255,.045) 25%, transparent 25%),
    linear-gradient(225deg, rgba(255,255,255,.03) 25%, transparent 25%),
    linear-gradient(45deg, rgba(255,255,255,.03) 25%, transparent 25%),
    linear-gradient(315deg, rgba(0,0,0,.35) 25%, transparent 25%),
    linear-gradient(180deg, #0b110e 0%, #070a08 100%) !important;
  background-size: 14px 14px, 14px 14px, 14px 14px, 14px 14px, auto !important;
}
.logo {
  background: linear-gradient(145deg, #1a9b63, #0b5c3d) !important;
  box-shadow: inset 0 0 0 1px rgba(46,229,157,.35), 0 0 18px rgba(26,155,99,.25);
  border-radius: 10px !important;
}
.brand span { color: #7f978b !important; }
.nav a { color: #b7cbbf !important; border: 1px solid transparent; }
.nav a.active, .nav a:hover {
  background: linear-gradient(90deg, rgba(26,155,99,.28), rgba(26,155,99,.08)) !important;
  color: #fff !important;
  border-color: rgba(46,229,157,.22) !important;
  box-shadow: inset 3px 0 0 #2ee59d;
}
.side-note { color: #7f978b !important; border-top-color: rgba(46,229,157,.12) !important; }
.eyebrow { color: #2ee59d !important; }
.subtitle, .footer { color: #8fa399 !important; }
.top .actions .btn, #agroThemeToggle {
  background: #141a17 !important;
  border: 1px solid #2a3831 !important;
  color: #e8f0eb !important;
}
.btn.primary, .calc-save, .fn-save, #applyBtn {
  background: linear-gradient(180deg, #1fad6f 0%, #127a4d 100%) !important;
  border-color: #1a9b63 !important;
  color: #04110a !important;
  font-weight: 800 !important;
  box-shadow: 0 0 0 1px rgba(46,229,157,.25), 0 8px 18px rgba(18,122,77,.35);
}
.filters {
  grid-template-columns: minmax(110px,140px) minmax(0,1.6fr) minmax(0,1fr) minmax(120px,160px) auto !important;
  gap: 10px 12px !important;
  padding: 12px 14px !important;
  align-items: start !important;
  border-radius: 12px !important;
  background: #121815 !important;
  border: 1px solid #27332d !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.04), 0 10px 28px rgba(0,0,0,.35) !important;
}
.filters .field-picker { grid-column: auto !important; max-width: none !important; min-width: 0 !important; }
.filters .field-picker label, .filters .field label, .field label { color: #8fa399 !important; margin: 0 0 5px; }
.filters .field-picker select, .filters select, select,
.calc-field input, .calc-field select, .submod input {
  border: 1px solid #2d3b34 !important;
  background: #0e1411 !important;
  color: #e8f0eb !important;
  padding: 8px 10px;
}
.filters .select {
  min-height: 0 !important; max-height: 72px; overflow: auto;
  padding: 5px 6px !important; gap: 4px !important; align-content: flex-start;
  border: 1px solid #2d3b34 !important; background: #0e1411 !important;
}
.filters .chip, .chip {
  background: #1a2a22 !important; color: #bfe8d2 !important; border: 1px solid #2a4a3b;
  padding: 4px 7px; font-size: 11px; border-radius: 7px;
}
.chip input { accent-color: #1a9b63; }
.filters #applyBtn { align-self: end; padding: 8px 14px; }
.kpi, .card, .calc-card, .tables article, .fn {
  background: #141a17 !important;
  border: 1px solid #27332d !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.03), 0 10px 24px rgba(0,0,0,.28) !important;
  border-radius: 12px !important;
}
.kpi .label, .head p, .calc-desc, .calc-top-title p { color: #8fa399 !important; }
.kpi .value { color: #f2faf5 !important; }
.calc-head { background: #141a17 !important; color: #e8f0eb !important; }
.calc-head:hover { background: #1a221e !important; }
.calc-head .code { color: #2ee59d !important; }
.calc-body, .fn-body { background: #0f1512 !important; border-top-color: #27332d !important; }
.calc-clear { background: #1a2a22 !important; color: #bfe8d2 !important; }
.calc-result { background: #13261d !important; color: #bfe8d2 !important; }
.submod { background: #121815 !important; border: 1px solid #2a3831 !important; }
.submod h4 { color: #d7e6dd !important; }
.submod .formula, .submod .unit, .submod label { color: #8fa399 !important; }
.field-stat-card {
  background:
    linear-gradient(135deg, rgba(26,155,99,.22), transparent 48%),
    linear-gradient(180deg, #0f1a15 0%, #0a120e 100%) !important;
  border: 1px solid rgba(46,229,157,.28) !important;
  box-shadow: 0 0 0 1px rgba(0,0,0,.4), 0 16px 36px rgba(0,0,0,.45) !important;
  color: #e8f0eb !important;
}
.field-stat-head h2 { color: #fff !important; }
.field-stat-head p { color: #9db5a8 !important; }
.field-summary .stat, .field-main {
  background: rgba(8,14,11,.55) !important;
  border: 1px solid rgba(46,229,157,.16) !important;
}
table th { color: #8fa399 !important; }
table td, table th { border-bottom-color: #24302a !important; }
.status, #agroModeBadge { color: #2ee59d !important; }
.agro-field-count { margin: 16px 8px 4px; }
.agro-field-count label {
  display:block; font-size:11px; letter-spacing:.08em; text-transform:uppercase;
  color:#9db5a8; font-weight:800; margin-bottom:6px;
}
.agro-field-count select {
  width:100%; padding:10px 12px; border-radius:10px;
  border:1px solid rgba(46,229,157,.28); background:#0e1411; color:#e8f0eb; font-weight:700;
}
.agro-field-count small { display:block; margin-top:6px; color:#7f978b; font-size:11px; line-height:1.4; }
::selection { background: rgba(46,229,157,.35); color: #fff; }

/* ===== light carbon (тестовая): светлее, крупнее weave, racing green ===== */
html.agro-theme-light {
  --bg: #e7ece9;
  --card: #f7faf8;
  --ink: #15261e;
  --muted: #5f7469;
  --green: #1b7a52;
  --green2: #146344;
  --mint: #d9e8df;
  --line: #c9d6ce;
  --shadow: 0 10px 28px rgba(25,55,43,.10);
  --carbon-edge: #1b7a52;
}
html.agro-theme-light body {
  color: var(--ink) !important;
  background-color: #e7ece9 !important;
  background-image:
    radial-gradient(900px 420px at 85% -5%, rgba(27,122,82,.12), transparent 55%),
    linear-gradient(180deg, #eef3f0 0%, #e3eae6 100%) !important;
}
html.agro-theme-light .sidebar {
  color: #e7f2ec !important;
  border-right: 1px solid rgba(255,255,255,.14);
  background-color: #1a4d38 !important;
  background-image:
    repeating-linear-gradient(60deg, rgba(255,255,255,.07) 0 1px, transparent 1px 18px),
    repeating-linear-gradient(-60deg, rgba(0,0,0,.12) 0 1px, transparent 1px 18px),
    linear-gradient(165deg, #226848 0%, #163c2c 55%, #123226 100%) !important;
  background-size: auto, auto, auto !important;
}
html.agro-theme-light .logo {
  background: linear-gradient(145deg, #2f9b68, #1b7a52) !important;
}
html.agro-theme-light .brand span { color: #b7d0c4 !important; }
html.agro-theme-light .nav a { color: #d5e8de !important; }
html.agro-theme-light .nav a.active, html.agro-theme-light .nav a:hover {
  background: rgba(255,255,255,.12) !important;
  color: #fff !important;
  border-color: rgba(255,255,255,.18) !important;
  box-shadow: inset 3px 0 0 #8fe0b5;
}
html.agro-theme-light .side-note { color: #b7d0c4 !important; border-top-color: rgba(255,255,255,.14) !important; }
html.agro-theme-light .eyebrow { color: #1b7a52 !important; }
html.agro-theme-light .subtitle, html.agro-theme-light .footer { color: #5f7469 !important; }
html.agro-theme-light .top .actions .btn, html.agro-theme-light #agroThemeToggle {
  background: #fff !important;
  border: 1px solid #c9d6ce !important;
  color: #15261e !important;
}
html.agro-theme-light .btn.primary, html.agro-theme-light .calc-save,
html.agro-theme-light .fn-save, html.agro-theme-light #applyBtn {
  background: linear-gradient(180deg, #249664 0%, #1b7a52 100%) !important;
  border-color: #1b7a52 !important;
  color: #fff !important;
  box-shadow: 0 8px 18px rgba(27,122,82,.22);
}
html.agro-theme-light .filters {
  background: #f7faf8 !important;
  border: 1px solid #c9d6ce !important;
  box-shadow: 0 8px 22px rgba(25,55,43,.08) !important;
}
html.agro-theme-light .filters .field-picker label,
html.agro-theme-light .filters .field label,
html.agro-theme-light .field label { color: #5f7469 !important; }
html.agro-theme-light .filters .field-picker select,
html.agro-theme-light .filters select, html.agro-theme-light select,
html.agro-theme-light .calc-field input, html.agro-theme-light .calc-field select,
html.agro-theme-light .submod input {
  border: 1px solid #c9d6ce !important;
  background: #fff !important;
  color: #15261e !important;
}
html.agro-theme-light .filters .select {
  border: 1px solid #c9d6ce !important;
  background: #fff !important;
}
html.agro-theme-light .filters .chip, html.agro-theme-light .chip {
  background: #e4f0e9 !important;
  color: #1a4d38 !important;
  border: 1px solid #c5dbcd;
}
html.agro-theme-light .kpi, html.agro-theme-light .card,
html.agro-theme-light .calc-card, html.agro-theme-light .tables article, html.agro-theme-light .fn {
  background: #f7faf8 !important;
  border: 1px solid #c9d6ce !important;
  box-shadow: 0 8px 22px rgba(25,55,43,.08) !important;
}
html.agro-theme-light .kpi .label, html.agro-theme-light .head p,
html.agro-theme-light .calc-desc, html.agro-theme-light .calc-top-title p { color: #5f7469 !important; }
html.agro-theme-light .kpi .value { color: #15261e !important; }
html.agro-theme-light .calc-head { background: #f7faf8 !important; color: #15261e !important; }
html.agro-theme-light .calc-head:hover { background: #eef5f1 !important; }
html.agro-theme-light .calc-head .code { color: #1b7a52 !important; }
html.agro-theme-light .calc-body, html.agro-theme-light .fn-body {
  background: #eef4f1 !important; border-top-color: #c9d6ce !important;
}
html.agro-theme-light .calc-clear { background: #e4f0e9 !important; color: #1a4d38 !important; }
html.agro-theme-light .calc-result { background: #e4f0e9 !important; color: #1a4d38 !important; }
html.agro-theme-light .submod { background: #fff !important; border: 1px solid #c9d6ce !important; }
html.agro-theme-light .submod h4 { color: #15261e !important; }
html.agro-theme-light .submod .formula, html.agro-theme-light .submod .unit,
html.agro-theme-light .submod label { color: #5f7469 !important; }
html.agro-theme-light .field-stat-card {
  background:
    linear-gradient(135deg, rgba(27,122,82,.18), transparent 45%),
    linear-gradient(145deg, #1f5c44 0%, #174a37 100%) !important;
  border: 1px solid rgba(27,122,82,.35) !important;
  box-shadow: 0 14px 32px rgba(25,55,43,.18) !important;
  color: #f2faf6 !important;
}
html.agro-theme-light .field-stat-head h2 { color: #fff !important; }
html.agro-theme-light .field-stat-head p { color: #c9e2d6 !important; }
html.agro-theme-light .field-summary .stat, html.agro-theme-light .field-main {
  background: rgba(255,255,255,.10) !important;
  border: 1px solid rgba(255,255,255,.16) !important;
}
html.agro-theme-light table th { color: #5f7469 !important; }
html.agro-theme-light table td, html.agro-theme-light table th { border-bottom-color: #d5e0da !important; }
html.agro-theme-light .status, html.agro-theme-light #agroModeBadge { color: #1b7a52 !important; }
html.agro-theme-light .agro-field-count label { color: #c9e2d6; }
html.agro-theme-light .agro-field-count select {
  border: 1px solid rgba(255,255,255,.28); background: #fff; color: #15261e;
}
html.agro-theme-light .agro-field-count small { color: #b7d0c4; }
html.agro-theme-light ::selection { background: rgba(27,122,82,.28); color: #fff; }

@media (max-width:1100px) {
  .filters { grid-template-columns: 1fr 1fr !important; }
  .filters #applyBtn { grid-column: 1 / -1; justify-self: end; }
  .app { grid-template-columns: 220px minmax(0,1fr) !important; }
  .sidebar { display: flex !important; flex-direction: column; }
}
</style>
"""

_CARBON_SCROLL_JS = r"""
(function(){
  function go(id){
    const el = document.getElementById(id);
    if(!el) return false;
    el.scrollIntoView({behavior:'smooth', block:'start'});
    return true;
  }
  function markActive(a){
    document.querySelectorAll('.nav a, nav a').forEach(x => x.classList.remove('active'));
    if(a) a.classList.add('active');
  }
  function openF(i){
    const code = 'F' + (i + 1);
    const calc = document.getElementById('calc-' + code) || document.querySelector('#calcGrid .calc-card:nth-child(' + (i+1) + ')');
    const fn = document.getElementById('fn' + i) || document.querySelector('#fnGrid .fn:nth-child(' + (i+1) + ')');
    if(calc){
      const pairs = {F1:'F2',F2:'F1',F3:'F4',F4:'F3',F5:'F6',F6:'F5'};
      document.querySelectorAll('#calcGrid .calc-card').forEach(c => c.classList.remove('open'));
      calc.classList.add('open');
      const mate = pairs[code] && document.getElementById('calc-' + pairs[code]);
      if(mate) mate.classList.add('open');
      go('calcTop'); setTimeout(() => calc.scrollIntoView({behavior:'smooth', block:'center'}), 60); return;
    }
    if(fn){ fn.classList.add('open'); go('functions'); setTimeout(() => fn.scrollIntoView({behavior:'smooth', block:'center'}), 60); return; }
    go('functions');
  }
  function bindExtraFLinks(){
    const nav = document.querySelector('.nav') || document.querySelector('aside nav') || document.querySelector('nav');
    if(!nav || nav.querySelector('[data-agro-f]')) return;
    const block = document.createElement('div');
    block.style.cssText = 'display:grid;gap:4px;margin-top:8px;padding-top:8px;border-top:1px solid rgba(255,255,255,.12)';
    for(let i=0;i<6;i++){
      const a = document.createElement('a');
      a.href = 'javascript:void(0)';
      a.className = 'agro-sub';
      a.dataset.agroF = 'F' + (i+1);
      a.textContent = 'F' + (i+1) + ' · подмодуль';
      a.addEventListener('click', ev => { ev.preventDefault(); ev.stopPropagation(); markActive(a); openF(i); });
      block.appendChild(a);
    }
    nav.appendChild(block);
  }
  // capture: любое #... только скролл, без смены location (иначе контент пропадает)
  document.addEventListener('click', function(ev){
    const a = ev.target.closest && ev.target.closest('a[href^="#"]');
    if(!a) return;
    const href = a.getAttribute('href') || '';
    ev.preventDefault();
    ev.stopPropagation();
    if(href === '#' || href === '#/') return;
    const id = decodeURIComponent(href.slice(1));
    markActive(a);
    go(id);
  }, true);
  document.addEventListener('click', function(ev){
    const head = ev.target.closest && ev.target.closest('.calc-head, .fn > button');
    if(!head) return;
    setTimeout(() => {
      const card = head.closest('.calc-card, .fn');
      if(card && card.classList.contains('open')) card.scrollIntoView({behavior:'smooth', block:'nearest'});
    }, 40);
  }, true);
  function boot(){ bindExtraFLinks(); bindThemeToggle(); }
  function bindThemeToggle(){
    const KEY = 'agro-carbon-theme';
    const root = document.documentElement;
    function apply(theme){
      const light = theme === 'light';
      root.classList.toggle('agro-theme-light', light);
      root.classList.toggle('agro-theme-dark', !light);
      const btn = document.getElementById('agroThemeToggle');
      if(btn) btn.textContent = light ? 'Тема: светлый карбон' : 'Тема: тёмный карбон';
      try { localStorage.setItem(KEY, light ? 'light' : 'dark'); } catch(e) {}
    }
    let saved = 'dark';
    try { saved = localStorage.getItem(KEY) || 'dark'; } catch(e) {}
    apply(saved === 'light' ? 'light' : 'dark');
    const btn = document.getElementById('agroThemeToggle');
    if(btn && !btn.dataset.bound){
      btn.dataset.bound = '1';
      btn.addEventListener('click', () => {
        apply(root.classList.contains('agro-theme-light') ? 'dark' : 'light');
      });
    }
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
"""

_ORGANIC_BOOT_JS = r"""
function agroCollectFields(sheets){
  const norm = s => String(s ?? '').toLowerCase().replace(/ё/g,'е').replace(/[^а-яa-z0-9]/g,'');
  const map = new Map();
  let max = 0;
  (sheets || []).forEach(sheet => {
    const rows = sheet.rows || [];
    let header = -1, fieldCol = -1;
    for(let r = 0; r < Math.min(rows.length, 12); r++){
      const line = rows[r] || [];
      for(let c = 0; c < line.length; c++){
        const n = norm(line[c]);
        if(n === 'поля' || n === 'номерполя' || n === 'nполя'){ header = r; fieldCol = c; }
      }
    }
    if(fieldCol >= 0){
      const head = rows[header] || [];
      let idCol = head.findIndex(c => String(c || '').trim() === '№');
      if(idCol < 0) idCol = 0;
      for(let r = header + 1; r < rows.length; r++){
        const line = rows[r] || [];
        const field = Number(line[fieldCol]);
        const id = Number(line[idCol]);
        if(!Number.isFinite(field) || field < 1 || !Number.isFinite(id)) continue;
        map.set(id, field);
        if(field > max) max = field;
      }
    }
    rows.forEach(line => {
      const raw = line && line[0];
      const m = typeof raw === 'string' && /^поле\s*(\d+)/i.exec(String(raw).trim());
      if(m) max = Math.max(max, Number(m[1]));
    });
  });
  return {map, max};
}
function agroSetFieldCount(count, refresh){
  const max = window.agroFieldMax || 1;
  count = Math.max(1, Math.min(Number(count) || max, max));
  window.agroFieldCount = count;
  const map = window.agroFieldMap;
  if(map && map.size){
    const allow = new Set();
    map.forEach((field, id) => { if(field <= count) allow.add(id); });
    window.agroFieldIds = allow;
  } else window.agroFieldIds = null;
  const box = document.getElementById('agroFieldCount');
  if(box && box.value !== String(count)) box.value = String(count);
  if(refresh !== false && typeof handleFilterChange === 'function') handleFilterChange();
}
function agroBindFieldCount(sheets){
  const found = agroCollectFields(sheets);
  const max = found.max || 1;
  window.agroFieldMax = max;
  window.agroFieldMap = found.map;
  const box = document.getElementById('agroFieldCount');
  const hint = document.getElementById('agroFieldCountHint');
  if(box){
    box.innerHTML = Array.from({length: max}, (_, i) => '<option value="' + (i + 1) + '">' + (i + 1) + '</option>').join('');
    box.onchange = () => agroSetFieldCount(Number(box.value), true);
  }
  if(hint) hint.textContent = found.max ? ('В таблице максимум ' + max) : 'В таблице нет номеров полей';
  agroSetFieldCount(max, false);
}
function agroResetOrganic(ev){
  if(ev){ ev.preventDefault(); ev.stopPropagation(); }
  try{
    const culture = document.getElementById('culture');
    const technology = document.getElementById('technology');
    const legume = document.getElementById('legumeCulture');
    if(culture) culture.value = '';
    if(technology) technology.value = '';
    if(legume) legume.value = '';
    if(typeof agroSetFieldCount === 'function') agroSetFieldCount(window.agroFieldMax || 1, false);
    if(typeof handleFilterChange === 'function') handleFilterChange();
  }catch(err){ console.error('agroResetOrganic', err); }
}
function agroBindResetOrganic(){
  const btn = document.getElementById('reset');
  if(!btn) return;
  btn.type = 'button';
  btn.onclick = agroResetOrganic;
}
agroBindResetOrganic();
window.addEventListener('message', ev => {
  if(!ev.data || ev.data.type !== 'agro-load') return;
  const file = new File([ev.data.buffer], ev.data.name || 'data.xlsx');
  window.__agroShellLoad = true;
  try { if(typeof importFile === 'function') importFile(file); }
  finally { window.__agroShellLoad = false; agroBindResetOrganic(); }
});
// hash-ссылки в iframe не должны сбрасывать документ
document.addEventListener('click', function(ev){
  const a = ev.target.closest && ev.target.closest('a[href^="#"]');
  if(!a) return;
  const href = a.getAttribute('href') || '';
  ev.preventDefault();
  ev.stopPropagation();
  if(href.length < 2) return;
  const el = document.getElementById(href.slice(1));
  if(el){
    document.querySelectorAll('nav a').forEach(x => x.classList.remove('active'));
    a.classList.add('active');
    el.scrollIntoView({behavior:'smooth', block:'start'});
  }
}, true);
"""


def _replace_js_assignment(html: str, keyword: str, new_value: str) -> str:
    """Заменить `const|let|var NAME = ...;` по скобкам/скобкам массива."""
    m = re.search(rf"(?:const|let|var)\s+{re.escape(keyword)}\s*=\s*", html)
    if not m:
        raise ValueError(f"assignment not found: {keyword}")
    start = m.end()
    i = start
    while i < len(html) and html[i].isspace():
        i += 1
    if i >= len(html):
        raise ValueError(f"empty assignment: {keyword}")
    opener = html[i]
    if opener in "{[":
        closer = "}" if opener == "{" else "]"
        depth = 0
        in_str = None
        esc = False
        j = i
        while j < len(html):
            ch = html[j]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == in_str:
                    in_str = None
            else:
                if ch in ("'", '"', "`"):
                    in_str = ch
                elif ch == opener:
                    depth += 1
                elif ch == closer:
                    depth -= 1
                    if depth == 0:
                        j += 1
                        while j < len(html) and html[j].isspace():
                            j += 1
                        if j < len(html) and html[j] == ";":
                            j += 1
                        return html[: m.start()] + f"let {keyword} = {new_value};" + html[j:]
            j += 1
        raise ValueError(f"unbalanced assignment: {keyword}")
    # примитив до ;
    j = html.find(";", i)
    if j < 0:
        raise ValueError(f"no semicolon: {keyword}")
    return html[: m.start()] + f"let {keyword} = {new_value};" + html[j + 1 :]


def _replace_function(html: str, name: str, new_fn: str) -> str:
    m = re.search(rf"function\s+{re.escape(name)}\s*\(", html)
    if not m:
        raise ValueError(f"function not found: {name}")
    brace = html.find("{", m.end() - 1)
    depth = 0
    j = brace
    while j < len(html):
        if html[j] == "{":
            depth += 1
        elif html[j] == "}":
            depth -= 1
            if depth == 0:
                return html[: m.start()] + new_fn.strip() + html[j + 1 :]
        j += 1
    raise ValueError(f"unbalanced function: {name}")


def _extract_section(html: str, start_marker: str) -> tuple[str, int, int]:
    i = html.find(start_marker)
    if i < 0:
        raise ValueError(f"section not found: {start_marker[:48]}")
    depth = 0
    j = i
    while True:
        nxt_open = html.find("<section", j)
        nxt_close = html.find("</section>", j)
        if nxt_close < 0:
            raise ValueError(f"unclosed section: {start_marker[:48]}")
        if nxt_open >= 0 and nxt_open < nxt_close:
            depth += 1
            j = nxt_open + 8
            continue
        depth -= 1
        j = nxt_close + len("</section>")
        if depth == 0:
            return html[i:j], i, j


def _move_section_after_header(html: str, start_marker: str, header_end: str, next_block: str) -> str:
    """Вырезать <section>… и вставить сразу после шапки, перед next_block."""
    section, a, b = _extract_section(html, start_marker)
    html = html[:a] + html[b:]
    # убрать лишние пустые строки на месте выреза
    html = html.replace("\n\n\n", "\n\n")
    anchor = header_end + next_block
    if anchor not in html:
        raise ValueError(f"header anchor not found for {start_marker[:48]}")
    html = html.replace(anchor, header_end + section + "\n\n" + next_block, 1)
    return html


def _patch_carbon(html: str) -> str:
    html = _replace_js_assignment(html, "DATA", "[]")
    html = _replace_js_assignment(html, "FIELD_STATS", json.dumps(_EMPTY_FIELD_STATS, ensure_ascii=False))
    html = _replace_function(html, "loadExternalExcel", _CARBON_LOAD_FN)
    # параметры F1–F6 сразу под шапкой, до фильтров и KPI
    html = _move_section_after_header(
        html,
        '<section class="calc-top" id="calcTop">',
        'onclick="window.print()">Печать</button></div>\n  </div>\n\n  ',
        '<section class="filters">',
    )
    # нижние расчётные функции → в верхние F1–F6, нижний блок убрать
    html = _replace_function(html, "renderTopCalc", _CARBON_RENDER_TOP_CALC)
    html = _replace_function(html, "renderFunctions", _CARBON_RENDER_FUNCTIONS_NOP)
    if "function clearMergedFn" not in html:
        html = html.replace(
            "function toggleCalc(code){",
            "function clearMergedFn(fnCode, calcCode){"
            "const f=fnData.find(x=>x[0]===fnCode); if(!f)return;"
            "(f[3]||[]).forEach(x=>{const el=document.getElementById(x.id); if(el)el.value='';});"
            "try{localStorage.removeItem('bottom-'+fnCode);}catch(e){}"
            "const r=document.getElementById('result-'+calcCode);"
            "if(r){r.textContent='Поля очищены.';r.classList.add('visible');}"
            "const st=document.getElementById('fn-status-'+fnData.indexOf(f)); if(st)st.textContent='';"
            "}\nfunction toggleCalc(code){",
            1,
        )
    # соседние в ряду раскрываются парой: F1↔F2, F3↔F4, F5↔F6
    html = html.replace(
        "function toggleCalc(code){document.getElementById('calc-'+code).classList.toggle('open')}",
        "function toggleCalc(code){"
        "const pairs={F1:'F2',F2:'F1',F3:'F4',F4:'F3',F5:'F6',F6:'F5'};"
        "const card=document.getElementById('calc-'+code); if(!card)return;"
        "const open=!card.classList.contains('open');"
        "card.classList.toggle('open',open);"
        "const mate=pairs[code]&&document.getElementById('calc-'+pairs[code]);"
        "if(mate) mate.classList.toggle('open',open);"
        "}",
        1,
    )
    try:
        _sec, a, b = _extract_section(html, '<section id="functions" class="functions">')
        html = html[:a] + html[b:]
        html = html.replace("\n\n\n", "\n\n")
    except ValueError:
        pass
    html = html.replace('href="#functions"', 'href="#calcTop"')
    html = html.replace(
        "<h2>Расчётные функции F1–F6</h2><p>Функции раскрываются сверху; параметры можно вводить и сохранять без перезагрузки страницы.</p>",
        "<h2>Расчётные функции F1–F6</h2><p>Подмодули и параметры из Excel. Соседние карточки открываются парой.</p>",
        1,
    )
    html = html.replace(
        "function filtered(){return DATA.filter(r=>active.cultures.includes(r.culture)&&active.techs.includes(r.technology))}",
        "function filtered(){const n=window.agroFieldCount||0;return DATA.filter(r=>active.cultures.includes(r.culture)&&active.techs.includes(r.technology)&&(!n||!r.field||r.field<=n))}",
        1,
    )
    html = html.replace(
        '<nav class="nav">',
        '<div class="agro-field-count"><label for="agroFieldCount">Количество полей</label>'
        '<select id="agroFieldCount"></select><small id="agroFieldCountHint">Загрузите таблицу</small></div>'
        '<nav class="nav">',
        1,
    )
    # кнопка «Сбросить» из шапки не нужна
    html = html.replace(
        '<button class="btn" id="resetBtn">Сбросить</button>',
        '',
        1,
    )
    html = html.replace(
        'document.getElementById("resetBtn").onclick=()=>{active={cultures:[...CULTURES],techs:[...TECHS]};renderFilters();renderCharts()};',
        '',
        1,
    )
    html = html.replace(
        "renderFilters();renderFunctions();renderTopCalc();restoreCalc();renderCharts();",
        # не поднимаем пустой localStorage — иначе F1–F6 становятся пустыми
        "try{Object.keys(localStorage).forEach(k=>{if(k.startsWith('agro-')||k.startsWith('bottom-'))localStorage.removeItem(k)});}catch(e){}"
        "renderFilters();renderFunctions();renderTopCalc();"
        "if(DATA.length){renderCharts();renderFieldStats();}"
        "else{document.querySelectorAll('.chartbox canvas').forEach(cv=>{"
        "const note=document.createElement('p');note.className='agro-empty';"
        "note.style.cssText='padding:24px;color:#71817b;text-align:center';"
        "note.textContent='Загрузите Excel';cv.style.display='none';cv.after(note);});}",
    )
    html = html.replace(
        '<div class="actions">',
        '<div class="actions">'
        '<span id="agroModeBadge" style="font-size:12px;font-weight:700;margin-right:8px">Углеродно-нейтральное земледелие</span>'
        '<button type="button" class="btn" id="agroThemeToggle" title="Временный переключатель темы">Тема: тёмный карбон</button>',
        1,
    )
    if "agro-scroll-fix" not in html:
        html = html.replace("</head>", _CARBON_SCROLL_CSS + "</head>")
    if "agro-load" not in html:
        html = html.replace(
            "</body>",
            f"<script>{_CARBON_MSG_JS}\n{_CARBON_SCROLL_JS}</script></body>",
        )
    elif "agro-sub" not in html:
        html = html.replace("</body>", f"<script>{_CARBON_SCROLL_JS}</script></body>")
    return html


def _patch_organic(html: str) -> str:
    html = _replace_js_assignment(html, "DATA", json.dumps(_EMPTY_ORGANIC_DATA, ensure_ascii=False))
    html = re.sub(
        r"sourceName\s*=\s*'[^']*'",
        "sourceName='Файл не загружен'",
        html,
        count=1,
    )
    html = html.replace("Органика побаловаться.xlsx", "Файл не загружен")
    # в сайдбаре только название модуля, без буквы F
    html = html.replace(
        '<div class="brand"><div class="mark">F</div><br>Модуль органического<br>земледелия<small>Аналитическая панель</small></div>',
        '<div class="brand">Модуль органического<br>земледелия<small>Аналитическая панель</small></div>',
        1,
    )
    # параметры F1–F5 сразу под шапкой (заголовок + загрузка), до фильтров и KPI
    html = _move_section_after_header(
        html,
        '<section class="section parameter-section" id="parameters">',
        'type="button">Вернуть исходные данные</button></details></div></section></div>',
        '<div class="filters">',
    )
    # новая книга заменяет фильтры, ручные правки и прошлый файл целиком
    old_import = (
        "DATA=next;sourceName=file.name;rawSheets=sheets;updateSource();fillFromWorkbook(sheets,true);"
    )
    new_import = (
        "DATA=next;sourceName=file.name;rawSheets=sheets;"
        "if(typeof agroBindFieldCount==='function')agroBindFieldCount(sheets);"
        "if(typeof agroBindResetOrganic==='function')agroBindResetOrganic();"
        "drafts={};savedParams={};dirtyModules.clear();"
        "Object.keys(fieldSources).forEach(k=>delete fieldSources[k]);"
        "storage.remove('organica-parameters-v1');storage.remove('organica-workbook-v1');"
        "updateSource();"
        "culture.value='';technology.value='';legumeCulture.value='';"
        "renderAll();fillFromWorkbook(sheets,true);"
    )
    if old_import not in html:
        raise ValueError("organic importFile reset point not found")
    html = html.replace(old_import, new_import, 1)
    html = html.replace(
        "async function importFile(file){if(!file)return;",
        "async function importFile(file){if(!file)return;"
        "if(window.parent!==window&&!window.__agroShellLoad){"
        "file.arrayBuffer().then(buf=>parent.postMessage({type:'agro-file',buffer:buf,name:file.name},'*'));return}",
        1,
    )
    # не поднимать старые/демо-данные из localStorage при старте
    html = html.replace(
        "try{const saved=JSON.parse(storage.get('organica-workbook-v1')||'null');"
        "if(saved&&Object.keys(ORIGINAL_DATA).every(k=>Array.isArray(saved.data[k]))){"
        "DATA=saved.data;sourceName=saved.name;rawSheets=saved.sheets||null;"
        "status.textContent='Данные восстановлены из браузера'}}"
        "catch{storage.remove('organica-workbook-v1')}updateSource();",
        "storage.remove('organica-workbook-v1');updateSource();",
    )
    html = html.replace(
        "legumeCulture.value));return ids}",
        "legumeCulture.value));if(window.agroFieldIds){const allow=window.agroFieldIds;ids=ids===null?new Set(allow):new Set([...ids].filter(id=>allow.has(id)))}return ids}",
        1,
    )
    html = html.replace(
        '<nav><a class="active" href="#overview">',
        '<div class="agro-field-count"><label for="agroFieldCount">Количество полей</label>'
        '<select id="agroFieldCount"></select><small id="agroFieldCountHint">Загрузите таблицу</small></div>'
        '<nav><a class="active" href="#overview">',
        1,
    )
    html = html.replace(
        "document.getElementById('reset').addEventListener('click',()=>{culture.value='';technology.value='';legumeCulture.value='';handleFilterChange()})",
        "document.getElementById('reset').onclick=function(ev){if(typeof agroResetOrganic==='function')return agroResetOrganic(ev);"
        "culture.value='';technology.value='';legumeCulture.value='';"
        "if(typeof agroSetFieldCount==='function')agroSetFieldCount(window.agroFieldMax||1,false);handleFilterChange()};",
        1,
    )
    html = html.replace(
        '<button id="reset">Сбросить</button>',
        '<button type="button" id="reset">Сбросить</button>',
        1,
    )
    if "agro-field-count-style" not in html:
        html = html.replace(
            "</head>",
            "<style id=\"agro-field-count-style\">.agro-field-count{margin:0 0 18px}.agro-field-count label{display:block;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#c9e2d6;font-weight:800;margin-bottom:6px}.agro-field-count select{width:100%;padding:10px 12px;border-radius:10px;border:0;background:#fff;color:#143c2d;font-weight:700}.agro-field-count small{display:block;margin-top:6px;color:#a9c8b9;font-size:12px}</style></head>",
            1,
        )
    if "agro-load" not in html:
        html = html.replace("</body>", f"<script>{_ORGANIC_BOOT_JS}</script></body>")
    return html


def _load_patched(kind: str) -> str:
    names = {
        "carbon5": "carbon.html",
        "carbonFull": "carbon_full.html",
        "organic": "organic.html",
    }
    raw = (ASSETS / names[kind]).read_text(encoding="utf-8")
    return _patch_organic(raw) if kind == "organic" else _patch_carbon(raw)


def _js_string(value: str) -> str:
    """JSON-строка, безопасная внутри <script> (не закрывает тег)."""
    return json.dumps(value).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def build_unified_html() -> str:
    carbon5 = _load_patched("carbon5")
    carbon_full = _load_patched("carbonFull")
    organic = _load_patched("organic")
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Агрономическая Аналитическая Панель</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
<style>
  :root {{ --green:#1e7655; --ink:#20312b; --muted:#71817b; --line:#e2e9e5; }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin:0; padding:0; width:100%; height:100%; background:#eef4f1; color:var(--ink);
    font-family: Manrope, "Segoe UI", sans-serif; -webkit-font-smoothing: antialiased; overflow:hidden; }}
  #shell {{ min-height:100%; display:flex; flex-direction:column; align-items:center; justify-content:center;
    padding:32px 16px; }}
  #gate {{ width:min(720px, 100%); padding:40px 32px; text-align:center; background:#fff;
    border:1px solid var(--line); border-radius:20px; box-shadow:0 16px 40px rgba(25,55,43,.08); }}
  #gate .eyebrow {{ color:#5b8072; font-weight:700; font-size:12px; letter-spacing:.04em; text-transform:uppercase; }}
  #gate h1 {{ margin:8px 0 10px; font-size:28px; letter-spacing:-.03em; font-weight:800; }}
  #gate p {{ margin:0 0 18px; color:var(--muted); font-size:15px; line-height:1.5; font-weight:500; }}
  #gate .hint {{ font-size:12px; color:#8a9993; font-weight:500; margin-bottom:22px; }}
  #gate label.btn {{ display:inline-flex; align-items:center; justify-content:center; gap:8px; cursor:pointer;
    background:#2f8c69; color:#fff; border-radius:12px; padding:12px 18px; font-size:14px; font-weight:700; }}
  #gate input {{ display:none; }}
  #err {{ display:none; margin-top:14px; color:#a93d72; font-size:13px; }}
  /* после загрузки — только модуль на весь экран, без второй шапки */
  #frame {{ display:none; position:fixed; inset:0; width:100%; height:100%; border:0; background:#eef4f1; }}
  body.is-loaded #shell {{ display:none !important; }}
  body.is-loaded #frame {{ display:block !important; }}
</style>
</head>
<body>
<div id="shell">
  <section id="gate">
    <div class="eyebrow">Агро-Аналитика</div>
    <h1>Нет загруженных данных</h1>
    <p>Демо отключены. Загрузите Excel углеродно-нейтрального или органического земледелия — режим определится сам.</p>
    <p class="hint">Свой экран для органики, углерода на 5 полей и полного углеродного модуля.</p>
    <label class="btn">Загрузить Excel<input id="file" type="file" accept=".xlsx,.xls"></label>
    <div id="err"></div>
  </section>
</div>
<iframe id="frame" title="Модуль"></iframe>
<script>
const MODULES = {{
  carbon5: {_js_string(carbon5)},
  carbonFull: {_js_string(carbon_full)},
  organic: {_js_string(organic)}
}};
let blobUrl = null;

function detectMode(wb, filename){{
  const name = String(filename || '').toLowerCase();
  const sheetNames = wb.SheetNames || [];
  const sheets = sheetNames.join(' ').toLowerCase();
  if(/органик|organic/.test(name) || sheets.includes('главный') || sheets.includes('органик') ||
     sheets.includes('планирование севооборота') || sheets.includes('планирования удобрений')){{
    return 'organic';
  }}
  if(/5[\\s_\\-]*пол/.test(name)) return 'carbon5';
  const f4 = sheetNames.find(s => /^f4\\b/i.test(String(s).trim()));
  if(f4){{
    const rows = XLSX.utils.sheet_to_json(wb.Sheets[f4], {{header:1, defval:null}});
    const marked = rows.some(r => r && typeof r[0] === 'string' && String(r[0]).trim().toLowerCase().startsWith('поле'));
    if(marked) return 'carbon5';
  }}
  if(sheetNames.some(s => /f1\\s*1000/i.test(String(s).trim()))) return 'carbonFull';
  return 'carbon5';
}}

function showError(msg){{
  const el = document.getElementById('err');
  el.style.display = 'block';
  el.textContent = msg;
  document.body.classList.remove('is-loaded');
}}

async function openWorkbook(buf, filename){{
  const wb = XLSX.read(new Uint8Array(buf), {{type:'array'}});
  const mode = detectMode(wb, filename);
  const frame = document.getElementById('frame');
  if(blobUrl) URL.revokeObjectURL(blobUrl);
  blobUrl = URL.createObjectURL(new Blob([MODULES[mode]], {{type:'text/html;charset=utf-8'}}));
  const onLoad = () => {{
    frame.removeEventListener('load', onLoad);
    frame.contentWindow.postMessage({{type:'agro-load', buffer: buf.slice(0), name: filename}}, '*');
  }};
  frame.addEventListener('load', onLoad);
  frame.src = blobUrl;
  document.body.classList.add('is-loaded');
}}

document.getElementById('file').addEventListener('change', async (e) => {{
  const file = e.target.files && e.target.files[0];
  if(!file) return;
  document.getElementById('err').style.display = 'none';
  try {{
    await openWorkbook(await file.arrayBuffer(), file.name);
  }} catch (err) {{
    showError(err && err.message ? err.message : 'Не удалось прочитать файл');
  }} finally {{
    e.target.value = '';
  }}
}});

window.addEventListener('message', async (ev) => {{
  if(!ev.data || ev.data.type !== 'agro-file') return;
  document.getElementById('err').style.display = 'none';
  try {{
    await openWorkbook(ev.data.buffer, ev.data.name || 'data.xlsx');
  }} catch (err) {{
    showError(err && err.message ? err.message : 'Не удалось прочитать файл');
  }}
}});
</script>
</body>
</html>"""


def write_app_html(path: Path | None = None) -> Path:
    html = build_unified_html()
    out = path or (ASSETS / "app.html")
    out.write_text(html, encoding="utf-8")
    # remote entrypoint на :8510 открывает panel.html
    if out.name == "app.html":
        (out.parent / "panel.html").write_text(html, encoding="utf-8")
    return out


# лениво: Streamlit (app4.py) и внешние импорты берут HTML через get_unified_html()
_UNIFIED_CACHE: str | None = None


def get_unified_html() -> str:
    global _UNIFIED_CACHE
    if _UNIFIED_CACHE is None:
        _UNIFIED_CACHE = build_unified_html()
    return _UNIFIED_CACHE


# совместимость со старым app4: UNIFIED_AGRO_HTML
def __getattr__(name: str):
    if name == "UNIFIED_AGRO_HTML":
        return get_unified_html()
    raise AttributeError(name)
