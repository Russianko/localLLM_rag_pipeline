import json
from pathlib import Path


def build_decision_summary(decisions: list[dict]) -> dict:
    """
    Строит краткую сводку по решениям fit_decision_engine.

    Что считаем:
    - сколько всего frame
    - сколько всего node
    - какие есть языки
    - какие есть форматы
    - сколько раз встретилось каждое decision
    - сколько раз встретился каждый fit_status

    Параметры:
    decisions: list[dict]
        Список frame-решений, который вернул decide_payload_actions()

    Возвращает:
    dict
        Краткая сводка по решениям
    """

    total_frames = len(decisions)
    total_nodes = 0

    languages = set()
    format_ids = set()

    # Здесь будем считать, сколько раз встретилось каждое решение:
    # apply_as_is, try_layout_adjustments и т.д.
    decision_counts = {}

    # Здесь будем считать fit_status:
    # fit / borderline / overflow
    fit_status_counts = {}

    for frame in decisions:
        languages.add(frame["language"])
        format_ids.add(frame["format_id"])

        node_decisions = frame["node_decisions"]
        total_nodes += len(node_decisions)

        for node in node_decisions:
            decision = node["decision"]
            fit_status = node["fit_status"]

            decision_counts[decision] = decision_counts.get(decision, 0) + 1
            fit_status_counts[fit_status] = fit_status_counts.get(fit_status, 0) + 1

    summary = {
        "total_frames": total_frames,
        "total_nodes": total_nodes,
        "languages": sorted(languages),
        "format_ids": sorted(format_ids),
        "decision_counts": decision_counts,
        "fit_status_counts": fit_status_counts,
    }

    return summary


def build_decision_report(decisions: list[dict]) -> dict:
    """
    Собирает полный decision report.

    Структура:
    {
      "summary": {...},
      "items": [...]
    }

    Где:
    - summary = краткая сводка
    - items = подробные решения по frame и node
    """

    return {
        "summary": build_decision_summary(decisions),
        "items": decisions,
    }


def save_decision_report(report: dict, output_path: str) -> None:
    """
    Сохраняет decision report в JSON-файл.

    Параметры:
    report: dict
        Полный отчет, который вернул build_decision_report()

    output_path: str
        Куда сохранить JSON
    """

    file_path = Path(output_path)

    # Создаем папку, если её ещё нет.
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Сохраняем в UTF-8 и в красивом формате.
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


def load_decision_report(input_path: str) -> dict:
    """
    Загружает decision report обратно из JSON.

    Это полезно:
    - для проверки сохранения
    - для дальнейшего анализа
    - для будущего UI / API

    Параметры:
    input_path: str
        Путь к JSON-файлу

    Возвращает:
    dict
        Загруженный отчет
    """

    file_path = Path(input_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Decision report not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data