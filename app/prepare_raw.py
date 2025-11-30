from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"


def prepare_households_from_itu() -> None:
    """
    З файлу ITU households_with_internet_itu.csv беремо лише Україну
    та зберігаємо year + internet_households_share.
    """
    src = RAW_DIR / "households_with_internet_itu.csv"
    if not src.exists():
        raise FileNotFoundError(src)

    df = pd.read_csv(src)

    df_ukr = df[df["entityIso"] == "UKR"][["dataYear", "dataValue"]].copy()
    df_ukr = df_ukr.rename(
        columns={
            "dataYear": "year",
            "dataValue": "internet_households_share",
        }
    )
    df_ukr["year"] = df_ukr["year"].astype(int)

    out_path = RAW_DIR / "households_internet_ua.csv"
    df_ukr.to_csv(out_path, index=False)
    print(f"Saved households data to {out_path}")


def prepare_internet_users_from_owid() -> None:
    """
    З share-of-individuals-using-the-internet.csv беремо лише Україну
    та зберігаємо year + internet_users_share.
    """
    src = RAW_DIR / "share-of-individuals-using-the-internet.csv"
    if not src.exists():
        raise FileNotFoundError(src)

    df = pd.read_csv(src)

    df_ukr = df[df["Code"] == "UKR"][
        ["Year", "Individuals using the Internet (% of population)"]
    ].copy()

    df_ukr = df_ukr.rename(
        columns={
            "Year": "year",
            "Individuals using the Internet (% of population)": "internet_users_share",
        }
    )
    df_ukr["year"] = df_ukr["year"].astype(int)

    out_path = RAW_DIR / "internet_users_ua.csv"
    df_ukr.to_csv(out_path, index=False)
    print(f"Saved internet users data to {out_path}")


def prepare_ict_ecommerce_from_sssu() -> None:
    """
    З датасету SSSU з ІКТ на підприємствах беремо:
    - Україна
    - всього по категорії розрізу
    - всього за кількістю працівників
    - всього за видом економічної діяльності

    І розгортаємо роки (2018..2024) у формат year+ecommerce_firms_share.
    """
    src = RAW_DIR / "dataset_2025-11-30T10_36_25.282819923Z_DEFAULT_INTEGRATION_SSSU_DF_INFORM_COMMUN_TECH_ENTRP_LATEST.csv"
    if not src.exists():
        raise FileNotFoundError(src)

    df = pd.read_csv(src)

    row = df[
        (df["Територіальний розріз"] == "Україна")
        & (df["Категорія розрізу"] == "Усього")
        & (df["Розріз"] == "Усього")
        & (df["Кількість працівників"] == "Усього")
        & (df["Вид економічної діяльності"] == "Усього")
    ]
    if row.empty:
        raise ValueError("Не нашёл агрегированную строку по е-комерції для всієї України")

    row = row.iloc[0]

    year_cols = [c for c in df.columns if c.isdigit()]

    out = pd.DataFrame(
        {
            "year": [int(y) for y in year_cols],
            "ecommerce_firms_share": [row[y] for y in year_cols],
        }
    )

    out_path = RAW_DIR / "ict_firms_ecommerce.csv"
    out.to_csv(out_path, index=False)
    print(f"Saved e-commerce firms data to {out_path}")


def prepare_ict_website_from_sssu() -> None:
    """
    Аналогічно для показника 'мають веб-сайт':
    - Україна
    - всього по працівниках
    - всього за видом діяльності
    """
    src = RAW_DIR / "dataset_2025-11-30T10_35_42.211050607Z_DEFAULT_INTEGRATION_SSSU_DF_INFORM_COMMUN_TECH_ENTRP_LATEST.csv"
    if not src.exists():
        raise FileNotFoundError(src)

    df = pd.read_csv(src)

    row = df[
        (df["Територіальний розріз"] == "Україна")
        & (df["Кількість працівників"] == "Усього")
        & (df["Вид економічної діяльності"] == "Усього")
    ]
    if row.empty:
        raise ValueError("Не нашёл агрегированную строку по веб-сайтам для всієї України")

    row = row.iloc[0]
    year_cols = [c for c in df.columns if c.isdigit()]

    out = pd.DataFrame(
        {
            "year": [int(y) for y in year_cols],
            "firm_website_share": [row[y] for y in year_cols],
        }
    )

    out_path = RAW_DIR / "ict_firms_website.csv"
    out.to_csv(out_path, index=False)
    print(f"Saved website firms data to {out_path}")


def prepare_all() -> None:
    prepare_households_from_itu()
    prepare_internet_users_from_owid()
    prepare_ict_ecommerce_from_sssu()
    prepare_ict_website_from_sssu()


if __name__ == "__main__":
    prepare_all()
