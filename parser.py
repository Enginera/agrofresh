import streamlit as st
import pandas as pd
import numpy as np

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
    """Сверхгибкий парсер, собирающий данные даже при отсутствии части колонок."""
    if file_buffer is None:
        return None
    try:
        df_sheet = pd.read_excel(file_buffer, header=None)
        parsed_fields = {}
        current_field_name = None
        accumulated_rows = []
        
        # Словарь индексов. По умолчанию выставляем -1 (значит колонка не найдена)
        col_idx = {"год": -1, "культура": -1, "урожайность": -1, "cinputs": -1, "cnet": -1, "ravg": -1, "площадь": -1, "глубина": -1}
        
        for idx, row in df_sheet.iterrows():
            # Очищаем ячейки строки для текстового анализа заголовков
            cells = [str(c).strip() for c in row.values if pd.notna(c) and str(c).strip() != ""]
            if not cells:
                continue
            row_text_line = " ".join(cells).lower()
            
            # 1. ТРИГГЕР ОБНАРУЖЕНИЯ НОВОГО ПОЛЯ
            if "поле" in row_text_line or "field" in row_text_line or "участок" in row_text_line:
                if current_field_name and accumulated_rows:
                    parsed_fields[current_field_name] = pd.DataFrame(accumulated_rows)
                found_name = "Поле"
                for c in cells:
                    c_low = c.lower()
                    if "поле" in c_low or "field" in c_low or "участок" in c_low:
                        found_name = c.strip()
                        break
                current_field_name = found_name
                accumulated_rows = []
                continue
                
            # 2. СКАН ЗАГОЛОВКОВ (Находим реальное положение колонок в файле)
            if "год" in row_text_line or "культура" in row_text_line or "урожай" in row_text_line:
                for i, val in enumerate(row.values):
                    if pd.isna(val): continue
                    v_low = str(val).lower().strip()
                    for key in col_idx.keys():
                        if key in v_low:
                            col_idx[key] = i
                continue
            
            # Если базовые колонки (Год, Культура, Урожайность) еще не привязаны к индексам,
            # пробуем использовать стандартную расстановку (0, 1, 2, 3...)
            if col_idx["год"] == -1:
                # Временная жесткая привязка, если в файле нет строки заголовка
                col_idx_working = {"год": 0, "культура": 1, "урожайность": 2, "cinputs": 3, "cnet": 4, "ravg": 5, "площадь": 6, "глубина": 7}
            else:
                col_idx_working = col_idx.copy()

            # 3. СБОР ДАННЫХ ИЗ СТРОКИ
            # Проверяем индекс года. Он должен быть валидным числом
            g_idx = col_idx_working["год"]
            if 0 <= g_idx < len(row):
                year_cell = str(row.iloc[g_idx]).strip().replace('.0', '')
                if year_cell.isdigit() and len(year_cell) == 4:
                    try:
                        year_val = int(year_cell)
                        if 2020 <= year_val <= 2035:
                            
                            # Безопасное извлечение ячеек с проверкой на существование индекса
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
                                "Площадь": clean_float(get_cell_val("площадь", 118.06)), # Если нет колонки, ставим 118.06
                                "Глубина": clean_float(get_cell_val("глубина", 0.3))    # Если нет колонки, ставим 0.3
                            })
                    except Exception:
                        continue
                        
        if current_field_name and accumulated_rows:
            parsed_fields[current_field_name] = pd.DataFrame(accumulated_rows)
            
        if not parsed_fields and accumulated_rows:
            parsed_fields["Поле 1"] = pd.DataFrame(accumulated_rows)

        # Расчет индекса эффективности E для всех найденных таблиц
        standardized_fields = {}
        for f_name, df_field in parsed_fields.items():
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
            {"Год": 2023, "Культура": "Кукуруза на силос", "Урожайность": 35.0, "Cinputs": 920.0, "Cnet": 590.0, "Ravg": 0.08, "Площаff": 118.06, "Глубина": 0.3},
            {"Год": 2024, "Культура": "Соя зерновая", "Урожайность": 3.1, "Cinputs": 510.0, "Cnet": 120.0, "Ravg": 0.10, "Площадь": 118.06, "Глубина": 0.3},
            {"Год": 2025, "Культура": "Пшеница Озимая", "Урожайность": 4.5, "Cinputs": 880.0, "Cnet": 510.0, "Ravg": 0.11, "Площадь": 118.06, "Глубина": 0.3}
        ])
    }
    for f_name, df in mock_dict.items():
        df["Эффективность"] = df.apply(
            lambda r: round(((r["Урожайность"] * (1.0 - r["Ravg"])) / r["Cnet"]) * 10000) / 10000 if r["Cnet"] != 0 else 0.0, axis=1
        )
    return mock_dict
