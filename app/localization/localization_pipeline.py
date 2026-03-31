from app.localization.spreadsheet_reader import read_translations
from app.localization.fit_evaluator import evaluate_text


def run_localization_check(filepath: str, limits: dict[str, int]) -> dict:
    translations = read_translations(filepath)

    result = {}

    for key, language_map in translations.items():
        if key not in limits:
            continue

        max_chars = limits[key]
        result[key] = {}

        for lang, text in language_map.items():
            result[key][lang] = evaluate_text(text, max_chars)

    return result