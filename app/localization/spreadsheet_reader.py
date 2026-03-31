import pandas as pd
from app.localization.text_normalizer import normalize_text


SERVICE_COLUMNS = ["Task", "domain", "key_name"]
SKIP_KEYS = {"geo", "currency", "nan", "none", ""}


def read_translations(filepath: str) -> dict[str, dict[str, str]]:
    df = pd.read_excel(filepath)

    # чистим названия колонок
    df.columns = [str(col).strip() for col in df.columns]

    if "key_name" not in df.columns:
        raise ValueError("Column 'key_name' not found in spreadsheet")

    language_columns = [
        col for col in df.columns
        if col not in SERVICE_COLUMNS
    ]

    translations: dict[str, dict[str, str]] = {}

    for _, row in df.iterrows():
        key = str(row.get("key_name", "")).strip()

        if key.lower() in SKIP_KEYS:
            continue

        values: dict[str, str] = {}

        for lang in language_columns:
            cell_value = row.get(lang)

            if pd.isna(cell_value):
                continue

            text = normalize_text(row[lang])
            if not text:
                continue

            values[lang.strip()] = text

        if values:
            translations[key] = values

    return translations