import pandas as pd
import numpy as np
from scipy import stats

# 26 канонических колонок в точном порядке скриншотов F2.xlsx
CANONICAL_COLUMNS = [
    "ID",                         # 1: № поля (1..1000)
    "F6_1_Efficiency",           # 2: Эффективность F6.1
    "CF_Harvest",                 # 3: Углеродный след операции уборки, CFуб.
    "B_Carbon",                   # 4: Углеродная выгода, т СО2-экв/га за год, Bcarbon
    "B_Econ",                     # 5: Becon
    "P_Carbon",                   # 6: Pcarbon
    "P_Carbon_Opt",               # 7: Pcarbon доп. / 400
    "Risk_1_R",                   # 8: Риск (1-R)
    "C_Total_Costs",              # 9: C – общие затраты (тыс. руб./га)
    "F6_2_Efficiency_Coeff",      # 10: F6.2 Коэффициент эффективности с учётом стоимости
    "PI_Priority_Index",          # 11: Индекс приоритета PI (кг СО2-экв/ руб за год)
    "C_Total_Agrosrok",           # 12: Углеродный след для i-го агросрока, Ctotal
    "Net_Carbon_Footprint",       # 13: Чистый углеродный след (0.65)
    "CF_Leaf_Operations",         # 14: Углеродный след от операций на листе
    "F6_3_Index",                 # 15: F6.3 Индекс
    "C_Abs_Code",                 # 16: Код абсорбции
    "C_Abs_F6_4",                 # 17: F6.4 Прогноз поглощения углерода (Cabs)
    "Temp_Avg_Apr_Jun",           # 18: Средняя температура за апрель–июнь (°C)
    "Precipitation_P",            # 19: P – осадки за тот же период (мм)
    "F5_Yield_Forecast",          # 20: F5 Прогноз урожайности Ynet (т/га или кг/га)
    "KPI_Field",                  # 21: Ключевой показатель эффективности по отдельным полям
    "Carbon_Intensity_Unit",      # 22: Расчет средней углеродоёмкости продукции (кг СО2-экв./т)
    "OP_Total_Losses",            # 23: Общие потери, т/га, ОП
    "E_Rotation_Efficiency",      # 24: Интегральный коэффициент эффективности севооборота E
    "Cost_Price_Season",          # 25: Себестоимость по полям в агросезон (тыс. руб/га)
    "Fertilizer_Costs_Neutral"    # 26: Затраты на удобрения с учетом нейтр. (тыс. руб/га)
]

def clean_numeric_value(val):
    """Очищает числа от пробелов, запятых и спецсимволов Excel (###, #Н/Д)."""
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).strip().replace(" ", "").replace(",", ".").replace("###", "")
    try:
        return float(val_str)
    except ValueError:
        return np.nan

def calculate_ci_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Расчёт точной описательной статистики и 95% CI (как внизу таблицы на скриншотах)."""
    stats_dict = {}
    for col in df.columns:
        if not np.issubdtype(df[col].dtype, np.number):
            continue
        valid_vals = df[col].dropna()
        n = len(valid_vals)
        if n > 1:
            mean = float(np.mean(valid_vals))
            std = float(np.std(valid_vals, ddof=1))
            var = float(np.var(valid_vals, ddof=1))
            se = std / np.sqrt(n)
            rel_err = (se / mean * 100) if mean != 0 else 0.0
            t_crit = stats.t.ppf((1 + 0.95) / 2, n - 1)
            ci = se * t_crit
            stats_dict[col] = {
                "Среднее значение": mean,
                "Стандартное отклонение": std,
                "Дисперсия": var,
                "Стандартная ошибка среднего": se,
                "Относительная ошибка среднего (%)": rel_err,
                "Ширина дов. интервала (95%)": ci,
                "Граница дов. интервала (Верхняя)": mean + ci,
                "Граница дов. интервала (Нижняя)": mean - ci
            }
    return pd.DataFrame(stats_dict)

def parse_agro_excel(file_source) -> tuple:
    """
    Парсит Excel F2.xlsx:
    - Находит начало строк данных (ID = 1);
    - Отбирает только строки данных (ID 1..1000);
    - Отсекает нижние итоговые блоки статистик;
    - Присваивает канонические имена 26 колонкам;
    - Рассчитывает 95% CI.
    """
    df_raw = pd.read_excel(file_source, header=None)
    
    # Поиск первой строки данных
    start_row_idx = None
    for idx, row in df_raw.iterrows():
        first_cell = str(row.iloc[0]).strip().replace(",", ".")
        if first_cell in ["1", "1.0"]:
            start_row_idx = idx
            break
            
    if start_row_idx is None:
        start_row_idx = 1

    df_body = df_raw.iloc[start_row_idx:].copy()
    
    # Фильтрация только строк с числовыми ID от 1 до 1000 (исключая строки со статистиками внизу)
    df_body['temp_id'] = df_body.iloc[:, 0].astype(str).str.replace(',', '.').str.strip()
    df_body['temp_id'] = pd.to_numeric(df_body['temp_id'], errors='coerce')
    
    df_main = df_body[df_body['temp_id'].notna() & (df_body['temp_id'] >= 1) & (df_body['temp_id'] <= 1000)].copy()
    df_main = df_main.drop(columns=['temp_id'])
    
    # Приведение значений к float
    for col in df_main.columns:
        df_main[col] = df_main[col].apply(clean_numeric_value)
        
    # Сопоставление с каноническими колонками
    assigned_cols = CANONICAL_COLUMNS[:len(df_main.columns)]
    if len(df_main.columns) > len(CANONICAL_COLUMNS):
        assigned_cols += [f"Extra_Col_{i}" for i in range(len(CANONICAL_COLUMNS), len(df_main.columns))]
    df_main.columns = assigned_cols
    df_main.reset_index(drop=True, inplace=True)
    
    # Расчет статистики по выборке
    df_stats = calculate_ci_statistics(df_main)
    return df_main, df_stats, len(df_main)

def generate_sample_dataset(rows: int = 1000) -> tuple:
    """Генератор демо-датасета на 1000 полей с распределениями, в точности соответствующими F2.xlsx."""
    np.random.seed(42)
    df = pd.DataFrame({
        "ID": np.arange(1, rows + 1),
        "F6_1_Efficiency": np.random.uniform(1.4, 24.8, rows).round(2),
        "CF_Harvest": np.random.randint(10, 120, rows),
        "B_Carbon": np.random.uniform(2.0, 250.0, rows).round(2),
        "B_Econ": np.random.uniform(75000, 85000, rows).round(0),
        "P_Carbon": np.random.choice([400, 450, 500], rows),
        "P_Carbon_Opt": np.full(rows, 400),
        "Risk_1_R": np.random.choice([0.5, 0.6, 0.7, 0.8], rows),
        "C_Total_Costs": np.random.uniform(40000, 65000, rows).round(0),
        "F6_2_Efficiency_Coeff": np.random.uniform(0.5, 4.0, rows).round(2),
        "PI_Priority_Index": np.random.uniform(0.01, 10.0, rows).round(4),
        "C_Total_Agrosrok": np.random.uniform(100, 2500, rows).round(2),
        "Net_Carbon_Footprint": np.full(rows, 0.65),
        "CF_Leaf_Operations": np.random.choice([50, 60, 75, 90, 250, 450, 1893], rows),
        "F6_3_Index": np.random.uniform(200, 4000, rows).round(2),
        "C_Abs_Code": np.random.choice([110, 115, 120, 125], rows),
        "C_Abs_F6_4": np.random.choice([13200, 13440, 13560, 13680, 13800, 13920, 14040, 14160, 14280, 14400, 14520, 14640, 14760, 14880, 15000], rows),
        "Temp_Avg_Apr_Jun": np.random.randint(16, 23, rows),
        "Precipitation_P": np.random.randint(160, 201, rows),
        "F5_Yield_Forecast": np.random.uniform(4.3, 5.5, rows).round(2),
        "KPI_Field": np.random.uniform(0.4, 1.0, rows).round(4),
        "Carbon_Intensity_Unit": np.random.uniform(3.5, 8.0, rows).round(1),
        "OP_Total_Losses": np.random.uniform(0.1, 4.5, rows).round(2),
        "E_Rotation_Efficiency": np.random.uniform(0.3, 1.3, rows).round(3),
        "Cost_Price_Season": np.random.randint(40, 66, rows),
        "Fertilizer_Costs_Neutral": np.random.randint(15, 26, rows)
    })
    
    df_stats = calculate_ci_statistics(df)
    return df, df_stats, len(df)