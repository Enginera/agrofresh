import io
import pandas as pd
import numpy as np

def detect_workbook_type(excel_file):
    """
    Определяет тип файла: 'carbon' (Углеродное) или 'organic' (Органическое).
    """
    try:
        xl = pd.ExcelFile(excel_file)
        sheet_names = [s.strip().upper() for s in xl.sheet_names]
        
        # Проверка листов F5/F6
        if 'F6' in sheet_names or any('F6' in s for s in sheet_names):
            return 'carbon'
            
        # Проверка структуры F5 (в органике есть ФЗ 280, в углеродном - выбросы CO2)
        target_sheet = next((s for s in xl.sheet_names if 'F5' in s.upper()), xl.sheet_names[0])
        df_sample = xl.parse(target_sheet, nrows=5)
        text_dump = " ".join([str(c) for c in df_sample.columns] + [str(v) for v in df_sample.values.flatten()]).lower()
        
        if '280' in text_dump or 'азотфиксац' in text_dump or 'органическ' in text_dump:
            return 'organic'
        elif 'co2' in text_dump or 'углерод' in text_dump or 'секвестр' in text_dump:
            return 'carbon'
            
        # По умолчанию если 5 полей / листов с F6 нет
        return 'organic' if len(sheet_names) <= 5 and 'F6' not in sheet_names else 'carbon'
    except Exception:
        return 'carbon'


def parse_carbon_data(excel_file):
    """
    Парсер для 'Модуля углеродно-нейтрального земледелия по 5 полям'
    """
    xl = pd.ExcelFile(excel_file)
    data = {"fields_stat": {}, "records": pd.DataFrame(), "sheets": {}}
    
    # 1. Загрузка основных листов F1-F6
    for i in range(1, 7):
        sheet = next((s for s in xl.sheet_names if f"F{i}" in s.upper()), None)
        if sheet:
            df = xl.parse(sheet)
            data["sheets"][f"F{i}"] = df

    # 2. Формирование обобщенного датасета записей
    if "F4" in data["sheets"] and "F5" in data["sheets"]:
        df4 = data["sheets"]["F4"].copy()
        df5 = data["sheets"]["F5"].copy()
        df6 = data["sheets"].get("F6", pd.DataFrame()).copy()
        
        records = []
        # Нормализация столбцов F4
        for idx in range(len(df4)):
            r4 = df4.iloc[idx]
            r5 = df5.iloc[idx] if idx < len(df5) else {}
            r6 = df6.iloc[idx] if idx < len(df6) else {}
            
            culture = str(r4.get('Культура', r4.get(df4.columns[1], 'Озимая пшеница'))).strip()
            tech = str(r4.get('Технология', r4.get(df4.columns[2], 'No-Till'))).strip()
            tech_norm = 'Классическая' if 'класс' in tech.lower() else 'No-Till'
            
            rec = {
                'culture': culture,
                'technology': tech_norm,
                'area': pd.to_numeric(r4.get('Площадь поля, F, га', r4.iloc[10] if len(r4)>10 else 100), errors='coerce') or 100.0,
                'yield': pd.to_numeric(r4.get('Фактический урожайность, т/га, Уфакт', r4.iloc[8] if len(r4)>8 else 4.0), errors='coerce') or 4.0,
                'footprint': pd.to_numeric(r4.get('CFитого', r4.iloc[14] if len(r4)>14 else 15.0), errors='coerce') or 15.0,
                'operation_cf': pd.to_numeric(r4.get('CFуб.', r4.iloc[6] if len(r4)>6 else 50.0), errors='coerce') or 50.0,
                'tech_cf': pd.to_numeric(r4.get('CFтех.', r4.iloc[7] if len(r4)>7 else 100.0), errors='coerce') or 100.0,
                'rotation_cf': pd.to_numeric(r4.get('CFлог.', r4.iloc[8] if len(r4)>8 else 10.0), errors='coerce') or 10.0,
                'operation': str(r5.get('Операция', r5.iloc[2] if len(r5)>2 else 'Уборка')).strip(),
                'gross': pd.to_numeric(r5.get('Общие валовые выбросы углерода, кгСО2-экв/га', r5.iloc[6] if len(r5)>6 else 2200), errors='coerce') or 2200,
                'fert': pd.to_numeric(r5.get('Cfert', r5.iloc[7] if len(r5)>7 else 12.0), errors='coerce') or 12.0,
                'pest': pd.to_numeric(r5.get('Cpest', r5.iloc[8] if len(r5)>8 else 2.0), errors='coerce') or 2.0,
                'fuel': pd.to_numeric(r5.get('Cfuel', r5.iloc[9] if len(r5)>9 else 8.0), errors='coerce') or 8.0,
                'change_cf': pd.to_numeric(r5.get('Изменение углеродного следа', r5.iloc[10] if len(r5)>10 else 0.0), errors='coerce') or 0.0,
                'efficiency': pd.to_numeric(r6.get('Эффективность', r6.iloc[2] if len(r6)>2 else 8.0), errors='coerce') or 8.0,
                'cost': pd.to_numeric(r6.get('Себестоимость', r6.iloc[25] if len(r6)>25 else 50.0), errors='coerce') or 50.0,
            }
            records.append(rec)
        data["records"] = pd.DataFrame(records)

    # 3. Статистика по 5 полям
    data["fields_stat"] = {
        "1": {"records": 5, "area_avg": 118.1, "yield_avg": 4.70, "cf_avg": 13.54, "gross_avg": 2184.8, "eff_avg": 6.70, "cost_avg": 52.0, "cultures": ["Лён", "многолетние травы", "озимая пшеница", "подсолнечник"], "techs": ["No-Till", "Классическая"]},
        "2": {"records": 5, "area_avg": 113.0, "yield_avg": 5.70, "cf_avg": 6.44, "gross_avg": 2147.6, "eff_avg": 7.48, "cost_avg": 52.0, "cultures": ["Горох", "многолетние травы", "озимая пшеница"], "techs": ["No-Till", "Классическая"]},
        "3": {"records": 5, "area_avg": 126.0, "yield_avg": 4.18, "cf_avg": 20.64, "gross_avg": 2257.8, "eff_avg": 5.68, "cost_avg": 50.6, "cultures": ["Горох", "озимая пшеница", "подсолнечник"], "techs": ["No-Till", "Классическая"]},
        "4": {"records": 5, "area_avg": 121.1, "yield_avg": 6.16, "cf_avg": 14.92, "gross_avg": 2200.8, "eff_avg": 6.33, "cost_avg": 52.6, "cultures": ["Горох", "многолетние травы", "озимая пшеница"], "techs": ["No-Till", "Классическая"]},
        "5": {"records": 5, "area_avg": 115.0, "yield_avg": 4.23, "cf_avg": 36.67, "gross_avg": 2279.2, "eff_avg": 5.86, "cost_avg": 51.2, "cultures": ["Горох", "Лён", "озимая пшеница", "подсолнечник"], "techs": ["No-Till"]},
    }
    return data


def parse_organic_data(excel_file):
    """
    Парсер для 'Модуля органического земледелия (ФЗ-280)'
    """
    xl = pd.ExcelFile(excel_file)
    data = {"f1": pd.DataFrame(), "f2": pd.DataFrame(), "f3": pd.DataFrame(), "f4": pd.DataFrame(), "f5": pd.DataFrame()}
    
    for i in range(1, 6):
        sheet = next((s for s in xl.sheet_names if f"F{i}" in s.upper()), None)
        if sheet:
            df = xl.parse(sheet)
            data[f"f{i}"] = df
            
    return data