from typing import List
import pandas as pd


def preprocess_data(
    df: pd.DataFrame,
    year_column: str,
    indicator_columns: List[str],
) -> pd.DataFrame:
    """
    Базова передобробка:
    - залишає лише рік та необхідні показники;
    - видаляє рядки з перепустками за ключовими показниками;
    - Наводить рік до int і сортує за зростанням.

    :param df: вихідний DataFrame
    :param year_column: назва колонки з роком
    :param indicator_columns: перелік показників
    :return: очищений DataFrame
    """
    required_cols = [year_column] + indicator_columns
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    out = df[required_cols].copy()

    # Видаляємо рядки, де хоча б один із показників відсутній
    out = out.dropna(subset=indicator_columns)

    # Рік у int
    out[year_column] = out[year_column].astype(int)

    # Сортування за роком
    out = out.sort_values(by=year_column).reset_index(drop=True)

    return out
