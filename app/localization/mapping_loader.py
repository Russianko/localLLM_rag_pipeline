import json
from pathlib import Path


def load_mapping(path: str) -> dict:
    """
    Загружает mapping.json.

    Этот файл отвечает за связь:
    - какой frame в Figma мы используем
    - какие текстовые слои внутри него есть
    - какие ключи из xlsx туда подставлять

    Пример:
    headline -> promo.headline

    Параметры:
    path: путь к mapping.json

    Возвращает:
    dict с содержимым mapping
    """

    file_path = Path(path)

    # Проверяем, существует ли файл
    if not file_path.exists():
        raise FileNotFoundError(f"Mapping file not found: {file_path}")

    # Читаем JSON
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Базовая проверка структуры (очень важно для отладки)
    if "frames" not in data:
        raise ValueError("Invalid mapping.json: 'frames' field is missing")

    return data


def get_frames(mapping: dict) -> list:
    """
    Возвращает список фреймов из mapping.

    Удобно, чтобы не писать каждый раз mapping["frames"]
    """
    return mapping["frames"]