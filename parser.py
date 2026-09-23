"""
parser.py - Обработка входных Excel файлов и встроенных наборов данных
"""
import pandas as pd
import numpy as np

DEFAULT_DATA = [
    {"culture":"Лён","technology":"No-Till","area":243.0,"footprint":95.18,"yield":1.3,"operation_cf":64.0,"tech_cf":142.0,"rotation_cf":12.0,"operation":"Уборка","gross":2422.0,"fert":13.0,"pest":1.0,"fuel":9.0,"change_cf":77.24,"efficiency":4.16,"cost":65.0},
    {"culture":"Лён","technology":"Классическая","area":466.0,"footprint":440.0,"yield":1.1,"operation_cf":99.0,"tech_cf":140.0,"rotation_cf":5.0,"operation":"Внесение удобрений","gross":2380.0,"fert":14.0,"pest":1.0,"fuel":9.0,"change_cf":0.0,"efficiency":1.83,"cost":52.0},
    {"culture":"Озимая пшеница","technology":"No-Till","area":227.0,"footprint":7.45,"yield":5.7,"operation_cf":34.0,"tech_cf":82.0,"rotation_cf":8.0,"operation":"Предпосевная обработка","gross":2236.0,"fert":13.0,"pest":2.0,"fuel":7.0,"change_cf":0.0,"efficiency":9.82,"cost":44.0},
    {"culture":"Горох","technology":"Классическая","area":344.0,"footprint":5.17,"yield":1.9,"operation_cf":7.0,"tech_cf":63.0,"rotation_cf":5.0,"operation":"Внесение удобрений","gross":2024.0,"fert":11.0,"pest":2.0,"fuel":9.0,"change_cf":0.0,"efficiency":3.80,"cost":51.0},
    {"culture":"Кукуруза","technology":"Классическая","area":176.0,"footprint":16.96,"yield":3.9,"operation_cf":54.0,"tech_cf":104.0,"rotation_cf":10.0,"operation":"Предпосевная обработка","gross":2210.0,"fert":13.0,"pest":1.0,"fuel":8.0,"change_cf":0.0,"efficiency":6.50,"cost":58.0},
    {"culture":"Многолетние травы","technology":"No-Till","area":168.0,"footprint":16.69,"yield":4.4,"operation_cf":50.0,"tech_cf":85.0,"rotation_cf":5.0,"operation":"Уборка","gross":2116.0,"fert":12.0,"pest":1.0,"fuel":9.0,"change_cf":0.0,"efficiency":9.10,"cost":56.0},
    {"culture":"Подсолнечник","technology":"Классическая","area":215.0,"footprint":54.35,"yield":1.6,"operation_cf":60.0,"tech_cf":136.0,"rotation_cf":10.0,"operation":"Предпосевная обработка","gross":2221.0,"fert":14.0,"pest":2.0,"fuel":9.0,"change_cf":0.0,"efficiency":4.80,"cost":53.0}
]

CULTURES_LIST = ["Озимая пшеница", "Горох", "Кукуруза", "Многолетние травы", "Подсолнечник", "Лён"]
TECHS_LIST = ["Классическая", "No-Till"]

def get_default_dataframe():
    return pd.DataFrame(DEFAULT_DATA)

def parse_carbon_excel(uploaded_file):
    """
    Парсинг загруженного файла Excel с листами F4, F5, F6
    """
    try:
        xls = pd.ExcelFile(uploaded_file)
        if not all(sheet in xls.sheet_names for sheet in ["F4", "F5", "F6"]):
            return None, "В Excel файле должны присутствовать листы: F4, F5, F6."

        df4 = pd.read_excel(xls, sheet_name="F4", header=1)
        df5 = pd.read_excel(xls, sheet_name="F5", header=1)
        df6 = pd.read_excel(xls, sheet_name="F6", header=1)

        canon_culture = {
            "лён": "Лён", "Лён": "Лён",
            "озимая пшеница": "Озимая пшеница", "Озимая пшеница": "Озимая пшеница",
            "горох": "Горох", "Горох": "Горох",
            "кукуруза": "Кукуруза", "Кукуруза": "Кукуруза",
            "многолетние травы": "Многолетние травы", "Многолетние травы": "Многолетние травы",
            "подсолнечник": "Подсолнечник", "Подсолнечник": "Подсолнечник"
        }

        records = []
        min_len = min(len(df4), len(df5), len(df6))

        for i in range(min_len):
            r4 = df4.iloc[i]
            r5 = df5.iloc[i]
            r6 = df6.iloc[i]

            raw_cult = str(r4.get("Культура", "")).strip()
            cult = canon_culture.get(raw_cult, raw_cult)
            if cult not in CULTURES_LIST:
                continue

            raw_tech = str(r4.get("Технология", "")).strip().lower()
            tech = "Классическая" if raw_tech.startswith("класс") else "No-Till"

            records.append({
                "culture": cult,
                "technology": tech,
                "area": float(r4.get("Площадь поля, F, га", 0) or 0),
                "footprint": float(r4.get(" показатель углеродного следа на тонну зерна получаемого в процессе уборки, кг СО2 -экв./т CFитого", 0) or 0),
                "yield": float(r4.get("Фактический урожайность, т/га, Уфакт", 0) or 0),
                "operation_cf": float(r4.get(" Показатель углеродного след технологической операции, кг -СО2 экв./га, CFуб.", 0) or 0),
                "tech_cf": float(r4.get("  Углеродный след от работы техники,CFтех., кг -экв./га", 0) or 0),
                "rotation_cf": float(r4.get(" Углеродный след логистики,CFлог., кг -экв./га", 0) or 0),
                "operation": str(r5.get("Операция", "")).strip(),
                "gross": float(r5.get("Общие валовые выбросы углерода, кгСО2-экв/га", 0) or 0),
                "fert": float(r5.get("эмиссия углерода от удобрений (кг CO2 эквивалента, Cfert", 0) or 0),
                "pest": float(r5.get("эмиссия углерода от пестицидов (кг CO2 эквивалента), Cpest", 0) or 0),
                "fuel": float(r5.get("эмиссия углерода от топлива (кг CO2 эквивалента, Cfuel", 0) or 0),
                "change_cf": float(r5.get("Изменение углеродного следа (Сводный отчет), минимальный показатель", 0) or 0),
                "efficiency": float(r6.get("Эффективность", 0) or 0),
                "cost": float(r6.get("Себестоимость по заданным полям в агросезон тыс руб/га", 0) or 0)
            })

        parsed_df = pd.DataFrame(records)
        return parsed_df, None
    except Exception as e:
        return None, f"Ошибка при разборе Excel: {str(e)}"