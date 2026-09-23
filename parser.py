"""
parser.py - Парсинг расширенной структуры Excel (листы F4, F5, F6) и генерация базовых данных
"""
import pandas as pd
import numpy as np

CULTURES_LIST = ["Озимая пшеница", "Горох", "Кукуруза", "Многолетние травы", "Подсолнечник", "Лён"]
TECHS_LIST = ["Классическая", "No-Till"]

def get_default_dataframe():
    """Генерация реалистичного набора данных на основе структуры F4-F6"""
    np.random.seed(42)
    n = 200
    records = []
    
    for i in range(n):
        culture = np.random.choice(CULTURES_LIST)
        tech = np.random.choice(TECHS_LIST)
        area = float(np.random.randint(100, 500))
        yfact = round(float(np.random.uniform(1.0, 7.0)), 2)
        footprint = round(float(np.random.uniform(2.0, 150.0)), 2)
        
        # F6 параметры из таблицы
        eff = round(float(np.random.uniform(2.0, 24.0)), 2)
        cost = round(float(np.random.uniform(40.0, 65.0)), 1)
        fert_cost = round(float(np.random.uniform(14.0, 26.0)), 1)
        keff = round(float(np.random.uniform(0.7, 2.5)), 2)
        pi = round(float(np.random.uniform(0.1, 4.5)), 4)
        ctotal = round(float(np.random.uniform(150.0, 2500.0)), 2)
        cabs = float(np.random.choice([13200, 13440, 13800, 14160, 14520, 14880, 15000]))
        temp = float(np.random.randint(16, 23))
        precip = float(np.random.randint(160, 201))
        ynet = round(float(np.random.uniform(4.3, 5.5)), 2)
        cfield = round(float(np.random.uniform(0.1, 8.0)), 2)
        op = round(float(np.random.uniform(0.3, 1.2)), 3)
        rot_e = round(float(np.random.uniform(1.5, 20.0)), 2)
        risk = float(np.random.choice([0.5, 0.6, 0.7, 0.8]))

        # F5 параметры
        operation = np.random.choice(["Внесение удобрений", "Предпосевная обработка", "Уборка"])
        gross = round(float(np.random.uniform(2000.0, 2500.0)), 1)
        fert = round(float(np.random.uniform(10.0, 15.0)), 1)
        pest = round(float(np.random.uniform(1.0, 2.0)), 1)
        fuel = round(float(np.random.uniform(7.0, 9.0)), 1)
        change_cf = round(float(np.random.uniform(-15.0, 60.0)), 2)
        
        # F4 параметры
        op_cf = round(float(np.random.uniform(10.0, 110.0)), 1)
        tech_cf = round(float(np.random.uniform(50.0, 150.0)), 1)
        rot_cf = round(float(np.random.uniform(5.0, 15.0)), 1)

        records.append({
            "culture": culture, "technology": tech, "area": area, "yield": yfact,
            "footprint": footprint, "efficiency": eff, "cost": cost, "fert_cost": fert_cost,
            "keff": keff, "pi": pi, "ctotal": ctotal, "cabs": cabs, "temp": temp,
            "precip": precip, "ynet": ynet, "cfield": cfield, "op": op, "rot_e": rot_e,
            "risk": risk, "operation": operation, "gross": gross, "fert": fert,
            "pest": pest, "fuel": fuel, "change_cf": change_cf, "operation_cf": op_cf,
            "tech_cf": tech_cf, "rotation_cf": rot_cf
        })
        
    return pd.DataFrame(records)

def parse_carbon_excel(uploaded_file):
    """Чтение листов F4, F5, F6 из загруженного Excel"""
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = [s.strip() for s in xls.sheet_names]
        
        # Проверяем наличие листов
        has_f4 = any("F4" in s for s in sheet_names)
        has_f5 = any("F5" in s for s in sheet_names)
        has_f6 = any("F6" in s for s in sheet_names)
        
        if not (has_f4 and has_f5 and has_f6):
            return None, "В Excel файле должны присутствовать листы F4, F5 и F6."

        s4_name = next(s for s in xls.sheet_names if "F4" in s)
        s5_name = next(s for s in xls.sheet_names if "F5" in s)
        s6_name = next(s for s in xls.sheet_names if "F6" in s)

        df4 = pd.read_excel(xls, sheet_name=s4_name, header=1)
        df5 = pd.read_excel(xls, sheet_name=s5_name, header=1)
        df6 = pd.read_excel(xls, sheet_name=s6_name, header=1)

        canon = {
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
            r4, r5, r6 = df4.iloc[i], df5.iloc[i], df6.iloc[i]

            raw_cult = str(r4.get("Культура", "")).strip()
            cult = canon.get(raw_cult, raw_cult)
            if cult not in CULTURES_LIST:
                continue

            raw_tech = str(r4.get("Технология", "")).strip().lower()
            tech = "Классическая" if raw_tech.startswith("класс") else "No-Till"

            records.append({
                "culture": cult,
                "technology": tech,
                "area": float(pd.to_numeric(r4.get("Площадь поля, F, га", 0), errors="coerce") or 0),
                "footprint": float(pd.to_numeric(r4.get(" показатель углеродного следа на тонну зерна получаемого в процессе уборки, кг СО2 -экв./т CFитого", 0), errors="coerce") or 0),
                "yield": float(pd.to_numeric(r4.get("Фактический урожайность, т/га, Уфакт", 0), errors="coerce") or 0),
                "operation_cf": float(pd.to_numeric(r4.get(" Показатель углеродного след технологической операции, кг -СО2 экв./га, CFуб.", 0), errors="coerce") or 0),
                "tech_cf": float(pd.to_numeric(r4.get("  Углеродный след от работы техники,CFтех., кг -экв./га", 0), errors="coerce") or 0),
                "rotation_cf": float(pd.to_numeric(r4.get(" Углеродный след логистики,CFлог., кг -экв./га", 0), errors="coerce") or 0),
                "operation": str(r5.get("Операция", "Уборка")).strip(),
                "gross": float(pd.to_numeric(r5.get("Общие валовые выбросы углерода, кгСО2-экв/га", 0), errors="coerce") or 0),
                "fert": float(pd.to_numeric(r5.get("эмиссия углерода от удобрений (кг CO2 эквивалента, Cfert", 0), errors="coerce") or 0),
                "pest": float(pd.to_numeric(r5.get("эмиссия углерода от пестицидов (кг CO2 эквивалента), Cpest", 0), errors="coerce") or 0),
                "fuel": float(pd.to_numeric(r5.get("эмиссия углерода от топлива (кг CO2 эквивалента, Cfuel", 0), errors="coerce") or 0),
                "change_cf": float(pd.to_numeric(r5.get("Изменение углеродного следа (Сводный отчет), минимальный показатель", 0), errors="coerce") or 0),
                "efficiency": float(pd.to_numeric(r6.get("Эффективность", 0), errors="coerce") or 0),
                "cost": float(pd.to_numeric(r6.get("Себестоимость по заданным полям в агросезон тыс руб/га", 0), errors="coerce") or 0),
                "fert_cost": float(pd.to_numeric(r6.get("затраты на удобрения по заданным полям с учетом углеродной нейтральности тыс руб/га за агросезон", 18.6), errors="coerce") or 18.6),
                "keff": float(pd.to_numeric(r6.get("F6.2 Коэффициент эффективности углеродной нейтральности с учётом стоимости мероприятий", 0.86), errors="coerce") or 0.86),
                "pi": float(pd.to_numeric(r6.get("Индекс приоритета, на 1 рубль затрат производства приходится поглощения , кг СО2-экв/ руб за год, (PI)", 0.42), errors="coerce") or 0.42),
                "ctotal": float(pd.to_numeric(r6.get("Углеродный след для і-го агросрока, Ctotal", 750.0), errors="coerce") or 750.0),
                "cabs": float(pd.to_numeric(r6.get("F6.4 Прогноз поглощения углерода (Cabs)", 14160.0), errors="coerce") or 14160.0),
                "temp": float(pd.to_numeric(r6.get("средняя температура за апрель–июнь (°C)", 18.0), errors="coerce") or 18.0),
                "precip": float(pd.to_numeric(r6.get("P – осадки за тот же период (мм).", 180.0), errors="coerce") or 180.0),
                "ynet": float(pd.to_numeric(r6.get(" F5 Прогноз урожайности (по температуре и осадкам) кг/га", 4.8), errors="coerce") or 4.8),
                "cfield": float(pd.to_numeric(r6.get("Расчет средней углеродоёмкости единицы продукции по заданым полям, кг СО2 -экв./т ", 1.3), errors="coerce") or 1.3),
                "op": float(pd.to_numeric(r6.get("Общие потери, т/га, ОП", 0.65), errors="coerce") or 0.65),
                "rot_e": float(pd.to_numeric(r6.get("Интегральный коэффициент Эффективности севооборота E", 7.89), errors="coerce") or 7.89),
                "risk": float(pd.to_numeric(r6.get("Риск (1-R)", 0.65), errors="coerce") or 0.65)
            })

        parsed_df = pd.DataFrame(records)
        return parsed_df, None
    except Exception as e:
        return None, f"Ошибка при разборе Excel: {str(e)}"