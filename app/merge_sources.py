from pathlib import Path
from typing import Dict, List
import pandas as pd


def _load_single_source(
    path: Path,
    year_col: str,
    value_col: str,
    target_col: str,
    country_iso: str | None = None,
    entity_iso_col: str | None = None,
) -> pd.DataFrame:
    """
    Завантажує один сирий файл та приводть до формату:
    year | target_col

    Якщо вказан country_iso та entity_iso_col, спочатку фільтрує по країні,
    як в ITU-файлі.
    """
    if not path.exists():
        raise FileNotFoundError(f"Raw source not found: {path}")

    suffix = path.suffix.lower()
    if suffix in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)

    # Якщо джерело багатокраїновий (як ITU) – фільтруємо
    if country_iso is not None and entity_iso_col is not None:
        if entity_iso_col not in df.columns:
            raise ValueError(
                f"File {path} has no column '{entity_iso_col}' "
                f"for ISO country filter"
            )
        df = df[df[entity_iso_col] == country_iso]

    # Перевіряємо наявність потрібних колонок
    missing = [c for c in [year_col, value_col] if c not in df.columns]
    if missing:
        raise ValueError(
            f"File {path} is missing required columns: {missing}"
        )

    out = df[[year_col, value_col]].copy()
    out = out.rename(
        columns={
            year_col: "year",
            value_col: target_col,
        }
    )
    out["year"] = out["year"].astype(int)

    return out


def build_panel_from_raw(
    raw_sources: List[Dict],
) -> pd.DataFrame:
    merged_df: pd.DataFrame | None = None

    for src in raw_sources:
        df_src = _load_single_source(
            path=src["path"],
            year_col=src["year_col"],
            value_col=src["value_col"],
            target_col=src["target_col"],
            country_iso=src.get("country_iso"),
            entity_iso_col=src.get("entity_iso_col"),
        )

        if merged_df is None:
            merged_df = df_src
        else:
            merged_df = merged_df.merge(
                df_src,
                on="year",
                how="outer",
            )

    if merged_df is None:
        raise ValueError("No raw sources provided")

    merged_df = merged_df.sort_values("year").reset_index(drop=True)
    return merged_df
