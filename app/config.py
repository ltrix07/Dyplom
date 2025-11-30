from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
OUTPUT_DIR = BASE_DIR / "output"

# Якщо True — панель формуємо самостійно з сирих джерел
BUILD_PANEL_FROM_RAW = True
BASE_YEAR_FOR_INDEX = 2019

# Готовий файл панель
PANEL_FILE = DATA_DIR / "digital_indicators_ua.xlsx"
PANEL_SHEET_NAME = "data"

YEAR_COLUMN = "year"

# Які показники хочемо в спільній панелі
INDEX_INDICATORS = [
    "internet_users_share",
    "internet_households_share",
    "firm_website_share",
    "ecommerce_firms_share",
]

DIGITAL_INDEX_COLUMN = "digital_index"
RAW_SOURCES = [
    {
        "path": RAW_DIR / "households_internet_ua.csv",
        "year_col": "year",
        "value_col": "internet_households_share",
        "target_col": "internet_households_share",
    },
    {
        "path": RAW_DIR / "internet_users_ua.csv",
        "year_col": "year",
        "value_col": "internet_users_share",
        "target_col": "internet_users_share",
    },
    {
        "path": RAW_DIR / "ict_firms_website.csv",
        "year_col": "year",
        "value_col": "firm_website_share",
        "target_col": "firm_website_share",
    },
    {
        "path": RAW_DIR / "ict_firms_ecommerce.csv",
        "year_col": "year",
        "value_col": "ecommerce_firms_share",
        "target_col": "ecommerce_firms_share",
    },
]


