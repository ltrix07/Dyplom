from typing import Dict, List, Optional

import numpy as np
import pandas as pd


def min_max_normalize(
    df: pd.DataFrame,
    columns: List[str],
) -> pd.DataFrame:
    out = df.copy()

    for col in columns:
        norm_col = f"{col}_norm"
        col_min = out[col].min()
        col_max = out[col].max()

        if pd.isna(col_min) or pd.isna(col_max):
            raise ValueError(f"Column {col} contains only NaN values")

        if col_max == col_min:
            out[norm_col] = 0.5
        else:
            out[norm_col] = (out[col] - col_min) / (col_max - col_min)

    return out


def build_base_year_index(
    df: pd.DataFrame,
    year_column: str,
    indicator_columns: List[str],
    index_column: str = "digital_index",
    base_year: int = 2018,
    weights: Optional[Dict[str, float]] = None,
) -> pd.DataFrame:
    """
    Строит індекс відносно базового року:
    I_j(t) = X_j(t) / X_j(base_year)

    Далі інтегральний індекс — середнє (зважене) по I_j(t).

    :param df: DataFrame з вихідними значеннями показників
    :param year_column: назва колонки з роком
    :param indicator_columns: список показників
    :param index_column: назва колонки для інтегрального індексу
    :param base_year: базовий рік (I(base_year) = 1)
    :param weights: словник ваг {column: weight} або None для рівних
    """
    out = df.copy()

    # шукаємо рядок базового року
    base_row = out[out[year_column] == base_year]
    if base_row.empty:
        raise ValueError(f"Base year {base_year} not found in data")

    base_row = base_row.iloc[0]

    rel_cols = []
    for col in indicator_columns:
        base_value = base_row[col]
        if base_value == 0 or pd.isna(base_value):
            raise ValueError(f"Base value for {col} is zero or NaN")

        rel_col = f"{col}_rel"
        out[rel_col] = out[col] / base_value
        rel_cols.append(rel_col)

    # Веса
    if weights is None:
        w = np.ones(len(rel_cols), dtype=float) / len(rel_cols)
    else:
        # порядок той самий, що indicator_columns
        w = np.array([weights[c] for c in indicator_columns], dtype=float)
        w_sum = w.sum()
        if w_sum == 0:
            raise ValueError("Sum of weights must be non-zero")
        w = w / w_sum

    rel_values = out[rel_cols].values
    index_values = (rel_values * w).sum(axis=1)

    out[index_column] = index_values
    return out
