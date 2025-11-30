from typing import List
import pandas as pd


def add_growth_rates(
    df: pd.DataFrame,
    year_column: str,
    indicator_columns: List[str],
) -> pd.DataFrame:
    """
    Додає до датафрейму ланцюгові темпи зростання для кожного показника.

    Темп зростання розраховується як:
    (Xt - Xt-1) / Xt-1 * 100 (%)

    :param df: вхідний DataFrame (вже відсортований за роками)
    :param year_column: колонка з роком (не використовується в розрахунках,
    але залишається для сумісності)
    :param indicator_columns: перелік показників
    :return: DataFrame з доданими колонками *_growth_rate
    """
    out = df.copy()

    for col in indicator_columns:
        growth_col = f"{col}_growth_rate"
        out[growth_col] = out[col].pct_change() * 100.0

    return out
