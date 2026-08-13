import streamlit as st
import pandas as pd
import numpy as np
import re

def clean_float(val):
    """Безопасное приведение ячейки Excel к числу с плавающей точкой."""
    if pd.isna(val): 
        return 0.0
    s = str(val).replace(',', '.').strip()
    try: 
        return float(s)
    except ValueError: 
        return 0.0

def advanced_multi_field_parser(file_buffer):
    """Ультимативный неубиваемый парсер. Читает все листы и любые структуры таблиц."""
    if file_buffer is None:
        return None
    try:
        # ЧИТАЕМ СРАЗУ ВСЕ ЛИСТЫ EXCEL (sheet_name=None возвращает словарь {Имя_Листа: Датафрейм})
        excel_file = pd.read_excel(file_buffer, sheet_name=None, header=None)
        
        parsed_fields = {}
        
        # Перебираем все вкладки по очереди
        for sheet_name, df_sheet in excel_file.items():
            current_field_name = None
            accumulated_rows = []
            
            # Базовые индексы колонок
            col_idx = {"год": -1, "культура": -1, "урожайность": -1, "cinputs": -1, "cnet": -1, "ravg": -1, "площадь": -1, "глубина": -1}
            
            for idx, row in df_sheet.iterrows():
                cells = [str(c).strip() for c in row.values if pd.notna(c) and str(c).strip() != ""]
                if not cells:
                    continue
                row_text_line = " ".join(cells).lower()
                
                # 1. ТРИГГЕР ОБНАРУЖЕНИЯ МАРКЕРА ПОЛЯ (Ищем регулярным выражением "поле", "участок", "field", "поле1")
                if re.search(r'(поле|field|участок|subfield|id_field)\s*\d*', row_text_line):
                    if current_field_name and accumulated_rows:
                        parsed_fields[current_field_name] = pd.DataFrame(accumulated_rows)
                    
                    found_name = f"Лист {sheet_name}"
                    for c in cells:
                        c_low = c.lower()
                        if any(k in c_low for k in ["поле", "field", "участок"]):
                            found_name = c.strip()
                            break
                    current_field_name = found_name
                    accumulated_rows = []
                    continue
                    
                # 2. СКАН ЗАГОЛОВКОВ КЛОНОК
                if any(k in row_text_line for k in ["год", "культура", "урожай"]):
                    for i, val in enumerate(row.values):
                        if pd.isna(val): continue
                        v_low = str(val).lower().strip()
                        for key in col_idx.keys():
                            if key in v_low:
                                col_idx[key] = i
                    continue
                
                # Защита: если заголовков нет, ставим стандартный порядок столбцов
                col_idx_working = col_idx.copy()
                if col_idx_working["год"] == -1:
                    col_idx_working = {"год": 0, "культура": 1, "урожайность": 2, "cinputs": 3, "cnet": 4, "ravg": 5, "площадь": 6, "глубина": 7}
                
                # 3. СБОР СТРОКИ ДАННЫХ
                g_idx = col_idx_working["год"]
                if 0 <= g_idx < len(row):
                    year_cell = str(row.iloc[g_idx]).strip().replace('.0', '')
                    if year_cell.isdigit() and len(year_cell) == 4:
                        try:
                            year_val = int(year_cell)
                            if 2020 <= year_val <= 2035:
                                
                                def get_cell_val(key, default_fallback=0.0):
                                    idx_val = col_idx_working[key]
                                    if 0 <= idx_val < len(row):
                                        return row.iloc[idx_val]
                                    return default_fallback

                                kul_idx = col_idx_working["культура"]
                                kul_val = str(row.iloc[kul_idx]).strip() if (0 <= kul_idx < len(row) and pd.notna(row.iloc[kul_idx])) else "Не указано"

                                accumulated_rows.append({
                                    "Год": year_val,
                                    "Культура": kul_val,
                                    "Урожайность": clean_float(get_cell_val("урожайность")),
                                    "Cinputs": clean_float(get_cell_val("cinputs")),
                                    "Cnet": clean_float(get_cell_val("cnet")),
                                    "Ravg": clean_float(get_cell_val("ravg")),
                                    "Площадь": clean_float(get_cell_val("площадь", 118.06)),
                                    "Глубина": clean_float(get_cell_val("глубина", 0.3)),
                                    "RawField": sheet_name # Запоминаем имя листа на случай автогруппировки
                                })
                        except Exception:
                            continue
            
            # Сохраняем остатки данных с текущего листа
            if accumulated_rows:
                name = current_field_name if current_field_name else f"Поле {sheet_name}"
                parsed_fields[name] = pd.DataFrame(accumulated_rows)
        
        # 4. ПЛАН В (ГРУППИРОВКА): Если листов много, но внутри они сплошные без маркеров
        # Проверяем, нет ли внутри колонки "Культура" названий полей, которые склеились
        final_fields = {}
        for f_name, df_f in parsed_fields.items():
            if df_f.empty: continue
            
            # Если внутри колонки "Культура" спрятались маркеры полей (например пользователь вбил туда "Поле 2")
            if df_f["Культура"].str.contains("поле|field|участок", case=False).any():
                for sub_name, sub_group in df_f.groupby("Культура"):
                    final_fields[sub_name] = sub_group.copy()
            else:
                final_fields[f_name] = df_f
                
        # Расчет индекса эффективности E
        standardized_fields = {}
        for f_name, df_field in final_fields.items():
            if df_field.empty:
                continue
            df_field["Эффективность"] = df_field.apply(
                lambda r: round(((r["Урожайность"] * (1.0 - r["Ravg"])) / r["Cnet"]) * 10000) / 10000 if r["Cnet"] != 0 else 0.0,
                axis=1
            )
            standardized_fields[f_name] = df_field
            
        return standardized_fields if standardized_fields else None
    except Exception as e:
        st.sidebar.error(f"Ошибка чтения структуры: {e}")
        return None

def get_mock_data():
    """Возвращает демонстрационные данные по умолчанию (строго Поле 1)."""
    mock_dict = {
        "Поле 1": pd.DataFrame([
            {"Год": 2021, "Культура": "Пшеница Озимая", "Урожайность": 4.2, "Cinputs": 850.0, "Cnet": 565.0, "Ravg": 0.12, "Площадь": 118.06, "Глубина": 0.3},
            {"Год": 2022, "Культура": "Многолетние травы", "Урожайность": 12.4, "Cinputs": 410.0, "Cnet": -215.0, "Ravg": 0.05, "Площадь": 118.06, "Глубина": 0.3},
            {"Год": 2023, "Культура": "Кукуруза на силос", "Урожайность": 35.0, "Cinputs": 920.0, "Cnet": 590.0, "Ravg": 0.08, "Площадь": 118.06, "Глубина": 0.3},
            {"Год": 2024, "Культура": "Соя зерновая", "Урожайность": 3.1, "Cinputs": 510.0, "Cnet": 120.0, "Ravg": 0.10, "Площадь": 118.06, "Глубина": 0.3},
            {"Год": 2025, "Культура": "Пшеница Озимая", "Урожайность": 4.5, "Cinputs": 880.0, "Cnet": 510.0, "Ravg": 0.11, "Площадь": 118.06, "Глубина": 0.3}
        ])
    }
    for f_name, df in mock_dict.items():
        df["Эффективность"] = df.apply(
            lambda r: round(((r["Урожайность"] * (1.0 - r["Ravg"])) / r["Cnet"]) * 10000) / 10000 if r["Cnet"] != 0 else 0.0, axis=1
        )
    return mock_dict
