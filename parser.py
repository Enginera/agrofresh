import io
import pandas as pd
import numpy as np

def detect_workbook_type(excel_file):
    try:
        if excel_file is None:
            return "carbon"
        if isinstance(excel_file, bytes):
            excel_file = io.BytesIO(excel_file)
        xl = pd.ExcelFile(excel_file)
        sheet_names = [s.strip().upper() for s in xl.sheet_names]
        if "F6" in sheet_names or any("F6" in s for s in sheet_names):
            return "carbon"
        target_sheet = next((s for s in xl.sheet_names if "F5" in s.upper()), xl.sheet_names[0])
        df_sample = xl.parse(target_sheet, nrows=5)
        text_dump = " ".join([str(c) for c in df_sample.columns] + [str(v) for v in df_sample.values.flatten()]).lower()
        if "280" in text_dump or "азотфиксац" in text_dump or "органическ" in text_dump:
            return "organic"
        elif "co2" in text_dump or "углерод" in text_dump or "секвестр" in text_dump:
            return "carbon"
        return "organic" if len(sheet_names) <= 5 and "F6" not in sheet_names else "carbon"
    except Exception:
        return "carbon"

def parse_carbon_data(excel_file=None):
    data = {"fields_stat": {}, "records": pd.DataFrame(), "sheets": {}}
    data["fields_stat"] = {
        "1": {"records": 5, "area_avg": 118.1, "yield_avg": 4.70, "cf_avg": 13.54, "gross_avg": 2184.8, "eff_avg": 6.70, "cost_avg": 52.0, "cultures": ["Лён", "многолетние травы", "озимая пшеница", "подсолнечник"], "techs": ["No-Till", "Классическая"]},
        "2": {"records": 5, "area_avg": 113.0, "yield_avg": 5.70, "cf_avg": 6.44, "gross_avg": 2147.6, "eff_avg": 7.48, "cost_avg": 52.0, "cultures": ["Горох", "многолетние травы", "озимая пшеница"], "techs": ["No-Till", "Классическая"]},
        "3": {"records": 5, "area_avg": 126.0, "yield_avg": 4.18, "cf_avg": 20.64, "gross_avg": 2257.8, "eff_avg": 5.68, "cost_avg": 50.6, "cultures": ["Горох", "озимая пшеница", "подсолнечник"], "techs": ["No-Till", "Классическая"]},
        "4": {"records": 5, "area_avg": 121.1, "yield_avg": 6.16, "cf_avg": 14.92, "gross_avg": 2200.8, "eff_avg": 6.33, "cost_avg": 52.6, "cultures": ["Горох", "многолетние травы", "озимая пшеница"], "techs": ["No-Till", "Классическая"]},
        "5": {"records": 5, "area_avg": 115.0, "yield_avg": 4.23, "cf_avg": 36.67, "gross_avg": 2279.2, "eff_avg": 5.86, "cost_avg": 51.2, "cultures": ["Горох", "Лён", "озимая пшеница", "подсолнечник"], "techs": ["No-Till"]},
    }
    
    mock = [
        {"culture": "Лён", "technology": "No-Till", "area": 243.0, "yield": 1.3, "footprint": 95.18, "operation_cf": 64.0, "tech_cf": 142.0, "rotation_cf": 12.0, "operation": "Уборка", "gross": 2422.0, "fert": 13.0, "pest": 1.0, "fuel": 9.0, "change_cf": 77.2, "efficiency": 4.16, "cost": 65.0},
        {"culture": "Озимая пшеница", "technology": "No-Till", "area": 227.0, "yield": 5.7, "footprint": 7.46, "operation_cf": 34.0, "tech_cf": 82.0, "rotation_cf": 8.0, "operation": "Предпосевная обработка", "gross": 2236.0, "fert": 13.0, "pest": 2.0, "fuel": 7.0, "change_cf": 0.0, "efficiency": 9.83, "cost": 44.0},
        {"culture": "Горох", "technology": "Классическая", "area": 344.0, "yield": 1.9, "footprint": 5.17, "operation_cf": 7.0, "tech_cf": 63.0, "rotation_cf": 5.0, "operation": "Внесение удобрений", "gross": 2024.0, "fert": 11.0, "pest": 2.0, "fuel": 9.0, "change_cf": 0.0, "efficiency": 3.80, "cost": 51.0},
        {"culture": "Кукуруза", "technology": "Классическая", "area": 176.0, "yield": 3.9, "footprint": 16.96, "operation_cf": 54.0, "tech_cf": 104.0, "rotation_cf": 10.0, "operation": "Предпосевная обработка", "gross": 2210.0, "fert": 13.0, "pest": 1.0, "fuel": 8.0, "change_cf": 0.0, "efficiency": 6.50, "cost": 58.0},
        {"culture": "Многолетние травы", "technology": "No-Till", "area": 168.0, "yield": 4.4, "footprint": 16.70, "operation_cf": 50.0, "tech_cf": 85.0, "rotation_cf": 5.0, "operation": "Уборка", "gross": 2116.0, "fert": 12.0, "pest": 1.0, "fuel": 9.0, "change_cf": 0.0, "efficiency": 9.10, "cost": 56.0},
        {"culture": "Подсолнечник", "technology": "Классическая", "area": 215.0, "yield": 1.6, "footprint": 54.35, "operation_cf": 60.0, "tech_cf": 136.0, "rotation_cf": 10.0, "operation": "Предпосевная обработка", "gross": 2221.0, "fert": 14.0, "pest": 2.0, "fuel": 9.0, "change_cf": 0.0, "efficiency": 4.80, "cost": 53.0},
        {"culture": "Озимая пшеница", "technology": "Классическая", "area": 371.0, "yield": 4.0, "footprint": 13.53, "operation_cf": 44.0, "tech_cf": 100.0, "rotation_cf": 12.0, "operation": "Уборка", "gross": 2455.0, "fert": 13.0, "pest": 1.0, "fuel": 8.0, "change_cf": 0.0, "efficiency": 10.37, "cost": 46.0},
        {"culture": "Горох", "technology": "No-Till", "area": 363.0, "yield": 2.1, "footprint": 6.24, "operation_cf": 8.0, "tech_cf": 50.0, "rotation_cf": 9.0, "operation": "Предпосевная обработка", "gross": 2300.0, "fert": 11.0, "pest": 2.0, "fuel": 8.0, "change_cf": 0.0, "efficiency": 5.25, "cost": 50.0},
        {"culture": "Кукуруза", "technology": "No-Till", "area": 434.0, "yield": 3.7, "footprint": 34.55, "operation_cf": 98.0, "tech_cf": 135.0, "rotation_cf": 10.0, "operation": "Внесение удобрений", "gross": 2049.0, "fert": 10.0, "pest": 2.0, "fuel": 9.0, "change_cf": 0.0, "efficiency": 7.66, "cost": 54.0}
    ]

    if excel_file is None:
        data["records"] = pd.DataFrame(mock)
        return data

    try:
        if isinstance(excel_file, bytes):
            excel_file = io.BytesIO(excel_file)
        xl = pd.ExcelFile(excel_file)
        for i in range(1, 7):
            sheet = next((s for s in xl.sheet_names if f"F{i}" in s.upper()), None)
            if sheet:
                data["sheets"][f"F{i}"] = xl.parse(sheet)
        if "F4" in data["sheets"] and "F5" in data["sheets"]:
            df4, df5 = data["sheets"]["F4"], data["sheets"]["F5"]
            df6 = data["sheets"].get("F6", pd.DataFrame())
            records = []
            for idx in range(len(df4)):
                r4 = df4.iloc[idx]
                r5 = df5.iloc[idx] if idx < len(df5) else {}
                r6 = df6.iloc[idx] if idx < len(df6) else {}
                culture = str(r4.get("Культура", r4.iloc[1] if len(r4)>1 else "Озимая пшеница")).strip()
                tech = str(r4.get("Технология", r4.iloc[2] if len(r4)>2 else "No-Till")).strip()
                records.append({
                    "culture": culture,
                    "technology": "Классическая" if "класс" in tech.lower() else "No-Till",
                    "area": pd.to_numeric(r4.get("Площадь поля, F, га", r4.iloc[10] if len(r4)>10 else 100), errors="coerce") or 100.0,
                    "yield": pd.to_numeric(r4.get("Фактический урожайность, т/га, Уфакт", r4.iloc[8] if len(r4)>8 else 4.0), errors="coerce") or 4.0,
                    "footprint": pd.to_numeric(r4.get("CFитого", r4.iloc[14] if len(r4)>14 else 15.0), errors="coerce") or 15.0,
                    "operation_cf": pd.to_numeric(r4.get("CFуб.", r4.iloc[6] if len(r4)>6 else 50.0), errors="coerce") or 50.0,
                    "tech_cf": pd.to_numeric(r4.get("CFтех.", r4.iloc[7] if len(r4)>7 else 100.0), errors="coerce") or 100.0,
                    "rotation_cf": pd.to_numeric(r4.get("CFлог.", r4.iloc[8] if len(r4)>8 else 10.0), errors="coerce") or 10.0,
                    "operation": str(r5.get("Операция", r5.iloc[2] if len(r5)>2 else "Уборка")).strip(),
                    "gross": pd.to_numeric(r5.get("Общие валовые выбросы углерода, кгСО2-экв/га", r5.iloc[6] if len(r5)>6 else 2200), errors="coerce") or 2200,
                    "fert": pd.to_numeric(r5.get("Cfert", r5.iloc[7] if len(r5)>7 else 12.0), errors="coerce") or 12.0,
                    "pest": pd.to_numeric(r5.get("Cpest", r5.iloc[8] if len(r5)>8 else 2.0), errors="coerce") or 2.0,
                    "fuel": pd.to_numeric(r5.get("Cfuel", r5.iloc[9] if len(r5)>9 else 8.0), errors="coerce") or 8.0,
                    "change_cf": pd.to_numeric(r5.get("Изменение углеродного следа", r5.iloc[10] if len(r5)>10 else 0.0), errors="coerce") or 0.0,
                    "efficiency": pd.to_numeric(r6.get("Эффективность", r6.iloc[2] if len(r6)>2 else 8.0), errors="coerce") or 8.0,
                    "cost": pd.to_numeric(r6.get("Себестоимость", r6.iloc[25] if len(r6)>25 else 50.0), errors="coerce") or 50.0,
                })
            data["records"] = pd.DataFrame(records)
        else:
            data["records"] = pd.DataFrame(mock)
    except Exception:
        data["records"] = pd.DataFrame(mock)
    return data

def parse_organic_data(excel_file=None):
    data = {"f1": pd.DataFrame(), "f2": pd.DataFrame(), "f3": pd.DataFrame(), "f4": pd.DataFrame(), "f5": pd.DataFrame()}
    mock_f4 = pd.DataFrame({
        "№": [1, 2, 3, 4, 5, 6],
        "Культура": ["Озимая пшеница", "Горох", "Кукуруза", "Многолетние травы", "Подсолнечник", "Лён"],
        "Технология": ["No-Till", "Классическая", "Strip-till", "Mini-till", "No-Till", "Плоскорезная"],
        "Жатва": [0.12, 0.17, 0.30, 0.40, 0.33, 0.32],
        "Обмолот": [0.08, 0.05, 0.06, 0.10, 0.04, 0.04],
        "Сепарация": [0.20, 0.17, 0.18, 0.40, 0.08, 0.12],
        "Общие потери": [0.40, 0.39, 0.54, 0.90, 0.45, 0.48],
        "Уфин": [5.30, 1.51, 3.36, 3.50, 1.15, 0.82],
        "Уфакт": [5.70, 1.90, 3.90, 4.40, 1.60, 1.30],
        "Qindex": [94.0, 91.0, 95.0, 86.0, 97.0, 90.0]
    })
    mock_f1 = pd.DataFrame({"E": [9.18, 3.55, 6.07, 8.50, 4.48, 3.88]})
    mock_f5 = pd.DataFrame({"Статус": ["Соответствует", "Соответствует", "Не соответствует", "Соответствует", "Не соответствует"]})
    
    if excel_file is None:
        data["f4"] = mock_f4
        data["f1"] = mock_f1
        data["f5"] = mock_f5
        return data

    try:
        if isinstance(excel_file, bytes):
            excel_file = io.BytesIO(excel_file)
        xl = pd.ExcelFile(excel_file)
        for i in range(1, 6):
            sheet = next((s for s in xl.sheet_names if f"F{i}" in s.upper()), None)
            if sheet:
                data[f"f{i}"] = xl.parse(sheet)
        if data["f4"].empty:
            data["f4"] = mock_f4
        if data["f1"].empty:
            data["f1"] = mock_f1
        if data["f5"].empty:
            data["f5"] = mock_f5
    except Exception:
        data["f4"] = mock_f4
        data["f1"] = mock_f1
        data["f5"] = mock_f5
    return data
