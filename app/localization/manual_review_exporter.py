import json
from pathlib import Path


def save_items_to_json(items: list[dict], output_path: str) -> None:
    """
    Сохраняет список extracted items в JSON-файл.

    Что это за items:
    - manual review items
    - short version candidates
    - или любой другой отфильтрованный список узлов

    Зачем это нужно:
    - чтобы сохранить отдельный рабочий список проблемных кейсов
    - чтобы не вырезать их каждый раз заново из decision report
    - чтобы использовать этот файл как артефакт пайплайна

    Параметры:
    items: list[dict]
        Список элементов, который вернул extractor

    output_path: str
        Путь, куда сохранить JSON-файл
    """

    # Превращаем строку пути в Path-объект.
    file_path = Path(output_path)

    # Создаем папку назначения, если её еще нет.
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Сохраняем в UTF-8 и в красивом JSON-формате.
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def load_items_from_json(input_path: str) -> list[dict]:
    """
    Загружает ранее сохраненный список items из JSON-файла.

    Это полезно:
    - для проверки, что файл сохранился корректно
    - для следующего этапа обработки
    - для ручного просмотра или UI

    Параметры:
    input_path: str
        Путь к JSON-файлу

    Возвращает:
    list[dict]
        Список загруженных элементов
    """

    file_path = Path(input_path)

    # Если файла нет, сразу даем понятную ошибку.
    if not file_path.exists():
        raise FileNotFoundError(f"Items file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def build_items_summary(items: list[dict]) -> dict:
    """
    Строит краткую сводку по списку extracted items.

    Что считаем:
    - общее количество элементов
    - по каким языкам они распределены
    - по каким node_name
    - по каким decision
    - по каким frame

    Параметры:
    items: list[dict]
        Список extracted items

    Возвращает:
    dict
        Краткая сводка
    """

    total_items = len(items)

    languages = {}
    node_names = {}
    decisions = {}
    frame_names = {}

    for item in items:
        language = item["language"]
        node_name = item["node_name"]
        decision = item["decision"]
        frame_name = item["frame_name"]

        languages[language] = languages.get(language, 0) + 1
        node_names[node_name] = node_names.get(node_name, 0) + 1
        decisions[decision] = decisions.get(decision, 0) + 1
        frame_names[frame_name] = frame_names.get(frame_name, 0) + 1

    summary = {
        "total_items": total_items,
        "languages": languages,
        "node_names": node_names,
        "decisions": decisions,
        "frame_names": frame_names,
    }

    return summary