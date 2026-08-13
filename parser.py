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

@st.cache_data
def advanced_multi_field_parser(file_buffer):
    """Интеллектуальный парсер, динамически находящий индексы колонок агро-таблицы."""
    if file_buffer is None:
        return None
    try:
        df_sheet = pd.read_excel(file_buffer, header=None)
        parsed_fields = {}
        current_field_name = None
        accumulated_rows = []
        
        # Индексы колонок по умолчанию
        col_idx = {"год": 0, "культура": 1, "урожайность": 2, "cinputs": 3, "cnet": 4, "ravg": 5, "площадь": 6, "глубина": 7}
        
        for idx, row in df_sheet.iterrows():
            cells = [str(c).strip() for c in row.values if pd.notna(c) and str(c).strip() != ""]
            if not cells:
                continue
            row_text_line = " ".join(cells).lower()
            
            # 1. ОБНАРУЖЕНИЕ НОВОГО БЛОКА ПОЛЯ
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
                
            # 2. ДИНАМИЧЕСКИЙ ПОИСК ИНДЕКСОВ КОЛОНОК
            if "год" in row_text_line or "культура" in row_text_line:
                for i, val in enumerate(row.values):
                    if pd.isna(val): continue
                    v_low = str(val).lower().strip()
                    for key in col_idx.keys():
                        if key in v_low:
                            col_idx[key] = i
                continue
                
            # 3. СБОР И ПАРСИНГ ДАННЫХ
            if len(row) >= max(col_idx.values()):
                year_cell = str(row.iloc[col_idx["год"]]).strip().replace('.0', '')
                if year_cell.isdigit() and len(year_cell) == 4:
                    try:
                        year_val = int(year_cell)
                        if 2020 <= year_val <= 2035:
                            accumulated_rows.append({
                                "Год": year_val,
                                "Культура": str(row.iloc[col_idx["культура"]]).strip() if pd.notna(row.iloc[col_idx["культура"]]) else "Не указано",
                                "Урожайность": clean_float(row.iloc[col_idx["урожайность"]]),
                                "Cinputs": clean_float(row.iloc[col_idx["cinputs"]]),
                                "Cnet": clean_float(row.iloc[col_idx["cnet"]]),
                                "Ravg": clean_float(row.iloc[col_idx["ravg"]]),
                                "Площадь": clean_float(row.iloc[col_idx["площадь"]]) if col_idx["площадь"] < len(row) else 118.06,
                                "Глубина": clean_float(row.iloc[col_idx["глубина"]]) if col_idx["глубина"] < len(row) else 0.3
                            })
                    except Exception:
                        continue
                        
        if current_field_name and accumulated_rows:
            parsed_fields[current_field_name] = pd.DataFrame(accumulated_rows)
            
        if not parsed_fields and accumulated_rows:
            parsed_fields["Поле 1"] = pd.DataFrame(accumulated_rows)

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
        st.sidebar.error(f"Ошибка структуры таблицы: {e}")
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
