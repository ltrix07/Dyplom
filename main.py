from app.config import (
    RAW_SOURCES,
    BUILD_PANEL_FROM_RAW,
    PANEL_FILE,
    PANEL_SHEET_NAME,
    OUTPUT_DIR,
    YEAR_COLUMN,
    INDEX_INDICATORS,
    DIGITAL_INDEX_COLUMN,
    BASE_YEAR_FOR_INDEX,
)
from app.merge_sources import build_panel_from_raw
from app.data_loader import load_panel_from_file
from app.preprocessing import preprocess_data
from app.analytics import add_growth_rates
from app.index_builder import build_base_year_index
from app.reporter import save_results_table, plot_indicators, plot_digital_index


def main() -> None:
    """
    Головний сценарій роботи системи:
    1) формує або завантажує інформаційну панель показників;
    2) виконує попередню обробку та розрахунок темпів зростання;
    3) будує інтегральний індекс відносно базового року;
    4) зберігає таблицю результатів та будує графіки.
    """

    # 1. Формуємо або завантажуємо панель показників
    if BUILD_PANEL_FROM_RAW:
        df_panel = build_panel_from_raw(RAW_SOURCES)
        PANEL_FILE.parent.mkdir(parents=True, exist_ok=True)
        df_panel.to_excel(PANEL_FILE, sheet_name=PANEL_SHEET_NAME, index=False)
        print(f"Інформаційну панель сформовано та збережено у {PANEL_FILE}")
    else:
        df_panel = load_panel_from_file(PANEL_FILE, PANEL_SHEET_NAME)
        print(f"Інформаційну панель завантажено з {PANEL_FILE}")

    # 2. Попередня обробка (відбір років з повним набором показників)
    df_clean = preprocess_data(
        df_panel,
        year_column=YEAR_COLUMN,
        indicator_columns=INDEX_INDICATORS,
    )

    # 3. Додавання темпів зростання
    df_with_growth = add_growth_rates(
        df_clean,
        year_column=YEAR_COLUMN,
        indicator_columns=INDEX_INDICATORS,
    )

    # 4. Побудова інтегрального індексу відносно базового року
    df_indexed = build_base_year_index(
        df_with_growth,
        year_column=YEAR_COLUMN,
        indicator_columns=INDEX_INDICATORS,
        index_column=DIGITAL_INDEX_COLUMN,
        base_year=BASE_YEAR_FOR_INDEX,
        weights=None,  # рівні ваги для всіх показників
    )

    # 5. Збереження таблиці результатів
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results_file = OUTPUT_DIR / "results.xlsx"
    save_results_table(df_indexed, results_file)
    print(f"Підсумкову таблицю результатів збережено у {results_file}")

    # 6. Графік динаміки показників — по повній панелі (максимальний період)
    indicators_plot = OUTPUT_DIR / "indicators.png"
    plot_indicators(
        df_panel,
        year_column=YEAR_COLUMN,
        indicator_columns=INDEX_INDICATORS,
        output_file=indicators_plot,
    )
    print(f"Графік показників діджиталізації збережено у {indicators_plot}")

    # 7. Графік інтегрального індексу — по роках з повним набором даних
    index_plot = OUTPUT_DIR / "digital_index.png"
    plot_digital_index(
        df_indexed,
        year_column=YEAR_COLUMN,
        index_column=DIGITAL_INDEX_COLUMN,
        output_file=index_plot,
    )
    print(f"Графік інтегрального індексу збережено у {index_plot}")

    print("Готово.")


if __name__ == "__main__":
    main()
