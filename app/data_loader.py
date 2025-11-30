from pathlib import Path
import pandas as pd


def load_panel_from_file(
    file_path: Path,
    sheet_name: str = "data",
) -> pd.DataFrame:
    """
    Читає вже готову панель (якщо ми заздалегідь її зберегли в Excel).
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Panel file not found: {file_path}")

    df = pd.read_excel(file_path, sheet_name=sheet_name)
    if df.empty:
        raise ValueError("Loaded panel is empty")

    return df
