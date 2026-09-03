import pandas as pd
import numpy as np
from scipy import stats

CANONICAL_COLUMNS = [
    "ID",
    "F6_1_Efficiency",
    "CF_Harvest",
    "B_Carbon",
    "B_Econ",
    "P_Carbon",
    "Risk_1_R",
    "C_Total_Costs",
    "F6_2_Efficiency_Coeff",
    "PI_Priority_Index",
    "C_Total_Agrosrok",
    "Net_Carbon_Footprint",
    "CF_Leaf_Operations",
    "F6_3_Index",
    "C_Abs_F6_4",
    "Temp_Avg_Apr_Jun",
    "Precipitation_P",
    "F5_Yield_Forecast",
    "KPI_Field",
    "Carbon_Intensity_Unit",
    "OP_Total_Losses",
    "E_Rotation_Efficiency",
    "Cost_Price_Season",
    "Fertilizer_Costs_Neutral"
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

def parse_agro_excel(file_source) -> dict:
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
    
    stats_dict = {}
    for col in df_main.columns:
        valid_vals = df_main[col].dropna()
        if len(valid_vals) > 1:
            mean = np.mean(valid_vals)
            std = np.std(valid_vals, ddof=1)
            var = np.var(valid_vals, ddof=1)
            se = std / np.sqrt(len(valid_vals))
            rel_err = (se / mean * 100) if mean != 0 else np.nan
            ci = se * stats.t.ppf((1 + 0.95) / 2, len(valid_vals) - 1)
            stats_dict[col] = {
                "Среднее": mean,
                "Стандартное отклонение": std,
                "Дисперсия": var,
                "Стандартная ошибка": se,
                "Относительная ошибка (%)": rel_err,
                "Ширина дов. интервала": ci,
                "Верхняя граница (95%)": mean + ci,
                "Нижняя граница (95%)": mean - ci
            }
            
    df_stats = pd.DataFrame(stats_dict)
    
    return {
        "data": df_main,
        "stats": df_stats,
        "total_rows": len(df_main),
        "status": "success"
    }

def generate_sample_dataset(rows: int = 1000) -> pd.DataFrame:
    np.random.seed(42)
    df = pd.DataFrame({
        "ID": np.arange(1, rows + 1),
        "F6_1_Efficiency": np.random.uniform(1.5, 25.0, rows).round(2),
        "CF_Harvest": np.random.randint(-20, 120, rows),
        "B_Carbon": np.random.uniform(1.0, 300.0, rows).round(2),
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
        "OP_Total_Losses": np.random.uniform(-1.0, 5.0, rows).round(2),
        "E_Rotation_Efficiency": np.random.uniform(0.3, 1.3, rows).round(3),
        "Cost_Price_Season": np.random.randint(40, 66, rows),
        "Fertilizer_Costs_Neutral": np.random.randint(15, 26, rows)
    })
    return df
