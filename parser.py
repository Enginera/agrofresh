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

# ДОБАВЛЯЕМ УМНЫЙ КЭШ: Таблица весом в 1000+ строк обработается один раз,
# а кэш автоматически сбросится, только если пользователь загрузит другой файл.
@st.cache_data(show_spinner="Анализ и оптимизация агросроков...")
def advanced_multi_field_parser(file_buffer):
    """Интеллектуальный парсер, адаптированный под многоколонный формат агро-таблиц."""
    if file_buffer is None:
        return None
    try:
        excel_file = pd.read_excel(file_buffer, sheet_name=None, header=None)
        parsed_fields = {}
        
        for sheet_name, df_sheet in excel_file.items():
            accumulated_rows = []
            
            col_idx = {
                "год": -1, 
                "культура": -1, 
                "урожайность": -1, 
                "cinputs": -1, 
                "cnet": -1, 
                "ravg": -1, 
                "площадь": -1, 
                "глубина": -1
            }
            
            for idx, row in df_sheet.head(15).iterrows():
                cells_low = [str(c).lower().strip() for c in row.values if pd.notna(c)]
                row_text = " ".join(cells_low)
                
                if "урожай" in row_text or "культура" in row_text or "след" in row_text:
                    for i, val in enumerate(row.values):
                        if pd.isna(val): continue
                        v_low = str(val).lower().strip()
                        
                        if "год" in v_low or "№" == v_low:
                            col_idx["год"] = i
                        elif "культур" in v_low:
                            col_idx["культура"] = i
                        elif "урожай" in v_low:
                            col_idx["урожайность"] = i
                        elif "cinputs" in v_low or "внесение углерода" in v_low or "материал" in v_low:
                            col_idx["cinputs"] = i
                        elif "cnet" in v_low or "чистый углеродн" in v_low or "след" in v_low:
                            col_idx["cnet"] = i
                        elif "ravg" in v_low or "эмиссия" in v_low or "операция" in v_low:
                            col_idx["ravg"] = i
                        elif "площадь" in v_low or "га" in v_low:
                            col_idx["площадь"] = i
                        elif "глубин" in v_low or "пласт" in v_low:
                            col_idx["глубина"] = i
                    break
            
            if col_idx["год"] == -1:
                col_idx = {"год": 0, "урожайность": 1, "cnet": 2, "cinputs": 4, "ravg": 3, "культура": -1, "площадь": -1, "глубина": -1}
                
            for idx, row in df_sheet.iterrows():
                if len(row) <= max([v for v in col_idx.values() if v >= 0]):
                    continue
                    
                year_cell = str(row.iloc[col_idx["год"]]).strip().replace('.0', '')
                
                if year_cell.isdigit() and len(year_cell) <= 4 and int(year_cell) > 0:
                    try:
                        raw_year = int(year_cell)
                        final_year = raw_year if raw_year >= 2020 else (2020 + raw_year)
                        
                        def get_val(key, fallback=0.0):
                            i = col_idx[key]
                            return clean_float(row.iloc[i]) if i >= 0 else fallback
                            
                        k_i = col_idx["культура"]
                        cult_name = str(row.iloc[k_i]).strip() if k_i >= 0 else "Зерновые (Комплекс)"
                        
                        accumulated_rows.append({
                            "Год": final_year,
                            "Культура": cult_name,
                            "Урожайность": clean_float(row.iloc[col_idx["урожайность"]]),
                            "Cinputs": get_val("cinputs", 850.0),
                            "Cnet": clean_float(row.iloc[col_idx["cnet"]]),
                            "Ravg": clean_float(row.iloc[col_idx["ravg"]]),
                            "Площадь": get_val("площадь", 118.06),
                            "Глубина": get_val("глубина", 0.3)
                        })
                    except Exception:
                        continue
            
            if accumulated_rows:
                parsed_fields[f"Участок: {sheet_name}"] = pd.DataFrame(accumulated_rows)
                
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
