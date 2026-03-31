import json
from pathlib import Path


def load_rules(path: str) -> dict:
    """
    Загружает layout_rules.json.

    Этот файл описывает:
    - какие ограничения есть у текста
    - что можно менять (font size, line height и т.д.)

    Параметры:
    path: путь к layout_rules.json

    Возвращает:
    dict с правилами
    """

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Rules file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if "formats" not in data:
        raise ValueError("Invalid layout_rules.json: 'formats' field is missing")

    return data


def get_format_rules(rules: dict, format_id: str) -> dict:
    """
    Возвращает правила для конкретного формата.

    Например:
    format_id = "1080x1080"

    Если формат не найден, показываем список доступных форматов,
    чтобы было проще понять, что именно не так в конфиге.
    """

    formats = rules["formats"]

    if format_id not in formats:
        available_formats = list(formats.keys())
        raise ValueError(
            f"Format rules not found for: {format_id}. "
            f"Available formats: {available_formats}"
        )

    return formats[format_id]