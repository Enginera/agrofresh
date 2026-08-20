import io
import pandas as pd
import numpy as np
import streamlit as st

# ==========================================================
# СЛОВАРИ ДЛЯ НОРМАЛИЗАЦИИ СОКРАЩЕНИЙ ИЗ ТАБЛИЦ
# ==========================================================
CROP_MAPPING = {
    "лён": "Лён",
    "лен": "Лён",
    "озимая": "Озимая пшеница",
    "пшеница": "Озимая пшеница",
    "горох": "Горох",
    "кукуруза": "Кукуруза",
    "многолет": "Многолетние травы",
    "травы": "Многолетние травы",
    "подсолне": "Подсолнечник",
    "подсолнечник": "Подсолнечник"
}

TECH_MAPPING = {
    "no-till": "No-Till",
    "notill": "No-Till",
    "но-тилл": "No-Till",
    "классичес": "Классическая",
    "классиче": "Классическая",
    "классическая": "Классическая",
    "традиционная": "Классическая"
}

OPERATION_MAPPING = {
    "предпосев": "Предпосевная обработка",
    "обработка": "Предпосевная обработка",
    "внесение": "Внесение удобрений/СЗР",
    "удобрен": "Внесение удобрений/СЗР",
    "уборка": "Уборка урожая"
}

RESOURCE_MAPPING = {
    "минеральн": "Минеральные удобрения",
    "удобрен": "Минеральные удобрения",
    "бензин": "Бензин",
    "дизель": "Дизельное топливо",
    "дизельное": "Дизельное топливо",
    "дт": "Дизельное топливо",
    "пестицид": "Пестициды",
    "сзр": "Пестициды",
    "электроэн": "Электроэнергия",
    "электричество": "Электроэнергия"
}

# ==========================================================
# ДЕМО-ДАТАСЕТ (MOCK DATA)
# ==========================================================
@st.cache_data
def get_mock_data() -> pd.DataFrame:
    """Генерация демо-выборки на 1000 строк по структуре документа."""
    np.random.seed(42)
    n = 1000
    crops = ["Лён", "Озимая пшеница", "Горох", "Кукуруза", "Многолетние травы", "Подсолнечник"]
    techs = ["No-Till", "Классическая"]
    ops = ["Предпосевная обработка", "Внесение удобрений/СЗР", "Уборка урожая"]
    resources = ["Минеральные удобрения", "Бензин", "Дизельное топливо", "Пестициды", "Электроэнергия"]

    f_map = {
        ("Лён", "Классическая"): 0.48, ("Лён", "No-Till"): 0.70,
        ("Озимая пшеница", "Классическая"): 0.65, ("Озимая пшеница", "No-Till"): 0.82,
        ("Горох", "Классическая"): 0.55, ("Горох", "No-Till"): 0.80,
        ("Многолетние травы", "Классическая"): 0.55, ("Многолетние травы", "No-Till"): 0.70,
        ("Кукуруза", "Классическая"): 0.65, ("Кукуруза", "No-Till"): 0.85,
        ("Подсолнечник", "Классическая"): 0.68, ("Подсолнечник", "No-Till"): 0.75,
    }
    yield_map = {
        "Лён": (0.9, 1.4), "Озимая пшеница": (4.6, 7.1), "Горох": (1.5, 2.2),
        "Многолетние травы": (4.6, 5.3), "Кукуруза": (3.1, 5.6), "Подсолнечник": (0.9, 1.8)
    }

    data = []
    for i in range(1, n + 1):
        c = np.random.choice(crops)
        t = np.random.choice(techs)
        f_val = f_map.get((c, t), 0.65)
        y_min, y_max = yield_map[c]
        y_val = np.round(np.random.uniform(y_min, y_max), 1)
        e_val = np.random.choice([0.5, 0.89, 2.3, 2.6, 4.93])
        op = np.random.choice(ops)
        res = np.random.choice(resources)
        
        emission = 1893.00 if op == "Уборка урожая" else float(np.random.choice([54, 86, 94, 219, 248, 342, 418, 480]))

        data.append({
            "id": i,
            "crop": c,
            "technology": t,
            "f_razl": f_val,
            "yield_t_ha": y_val,
            "emission_coeff_e": e_val,
            "operation": op,
            "emission_type": res,
            "co2_emission_kg": emission,
            "co2_per_ton": np.round(emission / y_val, 2)
        })

    return pd.DataFrame(data)

# Алиасы
load_demo_carbon_dataset = get_mock_data
load_sample_data = get_mock_data

# ==========================================================
# ОСНОВНОЙ ПАРСЕР
# ==========================================================
def advanced_multi_field_parser(uploaded_file=None) -> pd.DataFrame:
    """
    Парсер для файлов Excel (.xlsx, .xls) и CSV.
    Очищает строки, сокращения, конвертирует числа с запятыми.
    """
    if uploaded_file is None:
        return get_mock_data()

    try:
        filename = uploaded_file.name.lower()
        if filename.endswith(".csv"):
            df_raw = pd.read_csv(uploaded_file, header=None)
        else:
            df_raw = pd.read_excel(uploaded_file, header=None)

        # Определение начала таблицы
        start_row = 0
        for idx, row in df_raw.iterrows():
            row_str = " ".join([str(val).lower() for val in row.values if pd.notna(val)])
            if any(k in row_str for k in ["культура", "технология", "урожайность", "выброс"]):
                start_row = idx + 1
                break
            if len(row.values) > 0 and str(row.values[0]).strip() == "1":
                start_row = idx
                break

        df = df_raw.iloc[start_row:].copy().reset_index(drop=True)

        column_names = [
            "id",                 # 1: №
            "crop",               # 2: Культура
            "technology",         # 3: Технология
            "f_razl",             # 4: Фактор разложения Fразл
            "yield_t_ha",         # 5: Урожайность (т/га)
            "emission_coeff_e",   # 6: Коэффициент эмиссии E
            "operation",          # 7: Операция
            "emission_type",      # 8: Вид углеродного выброса
            "co2_emission_kg"     # 9: Значение выброса (кг CO2/га)
        ]

        num_cols = min(len(df.columns), len(column_names))
        df = df.iloc[:, :num_cols]
        df.columns = column_names[:num_cols]

        df = df.dropna(subset=["crop", "technology"], how="all")

        # 1. Приведение чисел
        numeric_fields = ["f_razl", "yield_t_ha", "emission_coeff_e", "co2_emission_kg"]
        for col in numeric_fields:
            if col in df.columns:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(",", ".", regex=False)
                    .str.extract(r"([\d\.]+)", expand=False)
                    .astype(float)
                )

        # 2. Нормализация текстовых полей
        if "crop" in df.columns:
            def clean_crop(val):
                s = str(val).strip().lower()
                for key, full_name in CROP_MAPPING.items():
                    if key in s:
                        return full_name
                return str(val).strip().capitalize()
            df["crop"] = df["crop"].apply(clean_crop)

        if "technology" in df.columns:
            def clean_tech(val):
                s = str(val).strip().lower()
                for key, full_name in TECH_MAPPING.items():
                    if key in s:
                        return full_name
                return str(val).strip().capitalize()
            df["technology"] = df["technology"].apply(clean_tech)

        if "operation" in df.columns:
            def clean_op(val):
                s = str(val).strip().lower()
                for key, full_name in OPERATION_MAPPING.items():
                    if key in s:
                        return full_name
                return str(val).strip().capitalize()
            df["operation"] = df["operation"].apply(clean_op)

        if "emission_type" in df.columns:
            def clean_resource(val):
                s = str(val).strip().lower()
                for key, full_name in RESOURCE_MAPPING.items():
                    if key in s:
                        return full_name
                return str(val).strip().capitalize()
            df["emission_type"] = df["emission_type"].apply(clean_resource)

        # 3. Расчет удельного следа (кг CO2 / т продукции)
        if "co2_emission_kg" in df.columns and "yield_t_ha" in df.columns:
            df["co2_per_ton"] = np.where(
                df["yield_t_ha"] > 0,
                np.round(df["co2_emission_kg"] / df["yield_t_ha"], 2),
                0.0
            )

        return df

    except Exception as e:
        st.error(f"Ошибка при чтении Excel файла: {e}")
        return get_mock_data()

# Алиасы для полной совместимости
parse_carbon_excel = advanced_multi_field_parser
parse_uploaded_file = advanced_multi_field_parser