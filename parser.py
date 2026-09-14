import pandas as pd
import numpy as np
from scipy import stats

CANONICAL_COLUMNS = [
    "ID",
    "F6_1_Efficiency",           # К эф F6
    "CF_Harvest",                 # Выбросы при уборке
    "B_Carbon",                   # Углеродоемкость / выгода
    "B_Econ",                     # Экономический эффект
    "P_Carbon",                   # Углеродный потенциал
    "Risk_1_R",                   # Риск (1-R)
    "C_Total_Costs",              # Общие затраты C
    "F6_2_Efficiency_Coeff",      # Коэфф. F6.2
    "PI_Priority_Index",          # Индекс приоритета PI
    "C_Total_Agrosrok",           # Показатель Ctotal
    "Net_Carbon_Footprint",       # Изменение углеродного следа
    "CF_Leaf_Operations",         # Эмиссия операций на листе
    "F6_3_Index",                 # Индекс F6.3
    "C_Abs_F6_4",                 # Абсорбция F6.4
    "Temp_Avg_Apr_Jun",           # Температура апр-июн
    "Precipitation_P",            # Осадки P
    "F5_Yield_Forecast",          # Прогноз урожайности Ynet / F5
    "KPI_Field",                  # KPI поля
    "Carbon_Intensity_Unit",      # Средняя углеродоемкость C поле
    "OP_Total_Losses",            # Общие потери ОП
    "E_Rotation_Efficiency",      # Интегральный коэфф. севооборота E
    "Cost_Price_Season",          # Себестоимость агросезона
    "Fertilizer_Costs_Neutral",   # Затраты на удобрения с нейтр. З уд.агросрок
    "C_Sequestered",              # Csequestered (F1)
    "C_Net",                      # Cnet (F1)
    "K_Temp_Soil",                # Ktemp почвы (F2)
    "K_Moisture",                 # Kвлаги (F2)
    "W_Fact",                     # Wфакт % (F2)
    "W_Crit",                     # Wкрит % (F2)
    "W_Opt",                      # Wопт % (F2)
    "I_Agrotech",                 # Iат (F2)
    "Delta_C_Tillage",            # ΔСобработка (F2)
    "Infection_Level_UZ",         # УЗ % (F3)
    "Infestation_Rate_IP",        # ИП % (F3)
    "Damage_Index_IPV",           # ИПВ (F3)
    "Interval_Days_I",            # I интервал (F3)
    "Dosage_D",                   # D дозировка (F3)
    "CF_Protection_Season",       # Cсезон (F3)
    "Delta_C_Straw",              # ΔСсолом (F4)
    "U_Fin_Yield",                # Уфин (F4)
    "S_CO2_Residues",             # SCO2 (F4)
    "CF_Tech_Operation",          # CFу.след (F4)
    "QF_Quality",                 # QF % (F4)
    "CF_Grain_Total"              # CFитог (F4)
]

def clean_numeric_value(val):
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
    """Единая функция расчета описательной статистики и 95% CI."""
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
                "Среднее": mean,
                "Стандартное отклонение": std,
                "Дисперсия": var,
                "Стандартная ошибка": se,
                "Относительная ошибка (%)": rel_err,
                "Ширина дов. интервала (95%)": ci,
                "Верхняя граница (95%)": mean + ci,
                "Нижняя граница (95%)": mean - ci
            }
    return pd.DataFrame(stats_dict)

def parse_agro_excel(file_source) -> tuple:
    """Парсит загруженную Excel-таблицу."""
    df_raw = pd.read_excel(file_source, header=None)
    
    start_row_idx = None
    for idx, row in df_raw.iterrows():
        first_cell = str(row.iloc[0]).strip().replace(",", ".")
        if first_cell in ["1", "1.0"]:
            start_row_idx = idx
            break
            
    if start_row_idx is None:
        start_row_idx = 1

    df_body = df_raw.iloc[start_row_idx:].copy()
    df_body['temp_id'] = df_body.iloc[:, 0].astype(str).str.replace(',', '.').str.strip()
    df_body['temp_id'] = pd.to_numeric(df_body['temp_id'], errors='coerce')
    
    df_main = df_body[df_body['temp_id'].notna() & (df_body['temp_id'] <= 1000)].copy()
    df_main = df_main.drop(columns=['temp_id'])
    
    for col in df_main.columns:
        df_main[col] = df_main[col].apply(clean_numeric_value)
        
    assigned_cols = CANONICAL_COLUMNS[:len(df_main.columns)]
    if len(df_main.columns) > len(CANONICAL_COLUMNS):
        assigned_cols += [f"Extra_Col_{i}" for i in range(len(CANONICAL_COLUMNS), len(df_main.columns))]
    df_main.columns = assigned_cols
    df_main.reset_index(drop=True, inplace=True)
    
    df_stats = calculate_ci_statistics(df_main)
    return df_main, df_stats, len(df_main)

def generate_sample_dataset(rows: int = 1000) -> tuple:
    """Генерация демо-датасета 1000 полей со всеми переменными F1–F6."""
    np.random.seed(42)
    df = pd.DataFrame({
        "ID": np.arange(1, rows + 1),
        "F6_1_Efficiency": np.random.uniform(1.5, 25.0, rows).round(2),
        "CF_Harvest": np.random.randint(10, 120, rows),
        "B_Carbon": np.random.uniform(2.0, 250.0, rows).round(2),
        "B_Econ": np.random.uniform(75000, 85000, rows).round(0),
        "P_Carbon": np.random.choice([400, 450, 500], rows),
        "Risk_1_R": np.random.choice([0.5, 0.6, 0.7, 0.8], rows),
        "C_Total_Costs": np.random.uniform(40000, 65000, rows).round(0),
        "F6_2_Efficiency_Coeff": np.random.uniform(0.5, 4.0, rows).round(2),
        "PI_Priority_Index": np.random.uniform(0.01, 10.0, rows).round(4),
        "C_Total_Agrosrok": np.random.uniform(100, 2500, rows).round(2),
        "Net_Carbon_Footprint": np.full(rows, 0.65),
        "CF_Leaf_Operations": np.random.choice([50, 100, 350, 1893], rows),
        "F6_3_Index": np.random.uniform(200, 4000, rows).round(2),
        "C_Abs_F6_4": np.random.choice([110, 115, 120, 125], rows),
        "Temp_Avg_Apr_Jun": np.random.randint(16, 23, rows),
        "Precipitation_P": np.random.randint(160, 201, rows),
        "F5_Yield_Forecast": np.random.uniform(4.3, 5.5, rows).round(2),
        "KPI_Field": np.random.uniform(0.4, 1.0, rows).round(4),
        "Carbon_Intensity_Unit": np.random.uniform(3.5, 8.0, rows).round(1),
        "OP_Total_Losses": np.random.uniform(0.1, 4.5, rows).round(2),
        "E_Rotation_Efficiency": np.random.uniform(0.3, 1.3, rows).round(3),
        "Cost_Price_Season": np.random.randint(40, 66, rows),
        "Fertilizer_Costs_Neutral": np.random.randint(15, 26, rows),
        "C_Sequestered": np.random.uniform(0.8, 3.5, rows).round(2),
        "C_Net": np.random.uniform(0.3, 1.8, rows).round(2),
        "K_Temp_Soil": np.random.uniform(0.9, 1.4, rows).round(2),
        "K_Moisture": np.random.uniform(0.85, 1.25, rows).round(2),
        "W_Fact": np.random.uniform(18.0, 32.0, rows).round(1),
        "W_Crit": np.random.uniform(12.0, 15.0, rows).round(1),
        "W_Opt": np.random.uniform(22.0, 28.0, rows).round(1),
        "I_Agrotech": np.random.uniform(0.7, 1.6, rows).round(2),
        "Delta_C_Tillage": np.random.uniform(40.0, 180.0, rows).round(1),
        "Infection_Level_UZ": np.random.uniform(2.0, 25.0, rows).round(1),
        "Infestation_Rate_IP": np.random.uniform(1.0, 15.0, rows).round(1),
        "Damage_Index_IPV": np.random.uniform(0.05, 0.45, rows).round(3),
        "Interval_Days_I": np.random.randint(10, 25, rows),
        "Dosage_D": np.random.uniform(0.5, 3.2, rows).round(2),
        "CF_Protection_Season": np.random.uniform(15.0, 75.0, rows).round(1),
        "Delta_C_Straw": np.random.uniform(120.0, 450.0, rows).round(1),
        "U_Fin_Yield": np.random.uniform(3.5, 6.2, rows).round(2),
        "S_CO2_Residues": np.random.uniform(80.0, 320.0, rows).round(1),
        "CF_Tech_Operation": np.random.uniform(25.0, 95.0, rows).round(1),
        "QF_Quality": np.random.uniform(85.0, 99.0, rows).round(1),
        "CF_Grain_Total": np.random.uniform(45.0, 110.0, rows).round(1)
    })
    
    df_stats = calculate_ci_statistics(df)
    return df, df_stats, len(df)