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
    """Интеллектуальный всеядный парсер агрономических таблиц Excel."""
    if file_buffer is None:
        return None
    try:
        # Читаем весь Excel-лист без заголовков для построчного анализа
        df_sheet = pd.read_excel(file_buffer, header=None)
        parsed_fields = {}
        current_field_name = None
        accumulated_rows = []
        
        # Шаг 1: Пробуем найти блоки по ключевым словам (Поле, Участок, Field)
        for idx, row in df_sheet.iterrows():
            cells = [str(c).strip() for c in row.values if pd.notna(c) and str(c).strip() != ""]
            if not cells:
                continue
            row_text_line = " ".join(cells).lower()
            
            # Расширенный фильтр триггеров разделения на новые поля
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
                
            # Пропускаем строки заголовков внутри блоков данные
            if "год" in row_text_line or "культура" in row_text_line:
                continue
                
            # Проверяем, что строка содержит агро-данные (длина строки и валидный год в первой ячейке)
            if len(row) >= 6:
                first_cell = str(row.iloc[0]).strip().replace('.0', '')
                if first_cell.isdigit() and len(first_cell) == 4:
                    try:
                        year_val = int(first_cell)
                        if 2020 <= year_val <= 2035:
                            accumulated_rows.append({
                                "Год": year_val,
                                "Культура": str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "Не указано",
                                "Урожайность": clean_float(row.iloc[2]),
                                "Cinputs": clean_float(row.iloc[3]),
                                "Cnet": clean_float(row.iloc[4]),
                                "Ravg": clean_float(row.iloc[5]),
                                "Площадь": clean_float(row.iloc[6]) if len(row) > 6 else 118.06,
                                "Глубина": clean_float(row.iloc[7]) if len(row) > 7 else 0.3
                            })
                    except Exception:
                        continue
                        
        if current_field_name and accumulated_rows:
            parsed_fields[current_field_name] = pd.DataFrame(accumulated_rows)
            
        # Шаг 2: ПЛАН Б — Если ключевые слова не найдены, но таблица сплошная
        # Проверяем, удалось ли нам вытащить хоть какие-то данные
        if not parsed_fields and accumulated_rows:
            df_flat = pd.DataFrame(accumulated_rows)
            # Если в таблице есть колонка с именами полей, группируем по ней
            if "Культура" in df_flat.columns and df_flat["Культура"].str.contains("Поле|Участок|Field", case=False).any():
                # Переносим ошибочно определенные имена полей из Культуры в ключи
                for name, group in df_flat.groupby("Культура"):
                    parsed_fields[name] = group
            else:
                # Если деления нет совсем, отдаем как единое Поле 1
                parsed_fields["Поле 1"] = df_flat

        # Шаг 3: Стандартизация и расчет индекса эффективности E для всех найденных полей
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
    """Возвращает демонстрационные данные по умолчанию."""
    mock_dict = {
        "Поле 1": pd.DataFrame([
            {"Год": 2021, "Культура": "Пшеница Озимая", "Урожайность": 4.2, "Cinputs": 850.0, "Cnet": 565.0, "Ravg": 0.12, "Площадь": 118.06, "Глубина": 0.3},
            {"Год": 2022, "Культура": "Многолетние травы", "Урожайность": 12.4, "Cinputs": 410.0, "Cnet": -215.0, "Ravg": 0.05, "Площадь": 118.06, "Глубина": 0.3},
            {"Год": 2023, "Культура": "Кукуруза на силос", "Урожайность": 35.0, "Cinputs": 920.0, "Cnet": 590.0, "Ravg": 0.08, "Площадь": 118.06, "Глубина": 0.3},
            {"Год": 2024, "Культура": "Соя зерновая", "Урожайность": 3.1, "Cinputs": 510.0, "Cnet": 120.0, "Ravg": 0.10, "Площадь": 118.06, "Глубина": 0.3},
            {"Год": 2025, "Культура": "Пшеница Озимая", "Урожайность": 4.5, "Cinputs": 880.0, "Cnet": 510.0, "Ravg": 0.11, "Площадь": 118.06, "Глубина": 0.3}
        ]),
        "Поле 2": pd.DataFrame([
            {"Год": 2022, "Культура": "Подсолнечник", "Урожайность": 2.8, "Cinputs": 600.0, "Cnet": 310.0, "Ravg": 0.09, "Площадь": 85.5, "Глубина": 0.3},
            {"Год": 2023, "Культура": "Пшеница Озимая", "Урожайность": 4.0, "Cinputs": 820.0, "Cnet": 490.0, "Ravg": 0.11, "Площадь": 85.5, "Глубина": 0.3},
            {"Год": 2024, "Культура": "Рапс озимый", "Урожайность": 3.5, "Cinputs": 750.0, "Cnet": 410.0, "Ravg": 0.07, "Площадь": 85.5, "Глубина": 0.3}
        ])
    }
    for f_name, df in mock_dict.items():
        df["Эффективность"] = df.apply(
            lambda r: round(((r["Урожайность"] * (1.0 - r["Ravg"])) / r["Cnet"]) * 10000) / 10000 if r["Cnet"] != 0 else 0.0, axis=1
        )
    return mock_dict
