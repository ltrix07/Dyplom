from pathlib import Path
from typing import List
import matplotlib.pyplot as plt
import pandas as pd


def save_results_table(df: pd.DataFrame, output_file: Path) -> None:
    """
    Зберігає підсумкову таблицю Excel.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_file, index=False)


def plot_indicators(
    df: pd.DataFrame,
    year_column: str,
    indicator_columns: List[str],
    output_file: Path,
) -> None:
    """
    Будує графік динаміки кількох показників.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)

    plt.figure()
    for col in indicator_columns:
        plt.plot(df[year_column], df[col], marker="o", label=col)

    plt.xlabel("Рік")
    plt.ylabel("Значення, %")
    plt.title("Динаміка показників діджиталізації")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


def plot_digital_index(
    df: pd.DataFrame,
    year_column: str,
    index_column: str,
    output_file: Path,
) -> None:
    """
    Будує графік інтегрального індексу.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.plot(df[year_column], df[index_column], marker="o")
    plt.xlabel("Рік")
    plt.ylabel("Індекс (0–1)")
    plt.title("Інтегральний індекс розвитку діджитал процесів")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
