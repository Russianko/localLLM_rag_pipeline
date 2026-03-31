import json
from pathlib import Path


def save_layout_plan(plans: list[dict], output_path: str) -> None:
    """
    Сохраняет layout adjustment plans в JSON-файл.

    Что такое plans:
    - это результат работы layout_adjustment_planner.py
    - список frame-планов
    - внутри каждого frame есть планы по node

    Зачем это нужно:
    - чтобы зафиксировать результат планирования
    - чтобы потом использовать его без повторного расчета
    - чтобы на следующем этапе строить действия для Figma plugin

    Параметры:
    plans: list[dict]
        Список frame-планов

    output_path: str
        Путь, куда сохранить JSON
    """

    # Превращаем строковый путь в Path-объект.
    file_path = Path(output_path)

    # Создаем папку, если её ещё нет.
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Сохраняем JSON в UTF-8.
    # ensure_ascii=False нужен для нормального отображения кириллицы.
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(plans, f, ensure_ascii=False, indent=2)


def load_layout_plan(input_path: str) -> list[dict]:
    """
    Загружает layout plan обратно из JSON-файла.

    Это полезно:
    - для проверки, что файл сохранился корректно
    - для следующего этапа пайплайна
    - для будущего UI или Figma plugin integration

    Параметры:
    input_path: str
        Путь к сохраненному JSON-файлу

    Возвращает:
    list[dict]
        Загруженные планы
    """

    file_path = Path(input_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Layout plan file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def build_layout_plan_summary(plans: list[dict]) -> dict:
    """
    Строит краткую сводку по layout adjustment plans.

    Что считаем:
    - сколько всего frame
    - сколько всего node
    - сколько node имеют план со статусом planned
    - сколько node имеют статус not_applicable
    - какие action встречаются в adjustment_plan

    Параметры:
    plans: list[dict]
        Список frame-планов

    Возвращает:
    dict
        Краткая сводка по планам
    """

    total_frames = len(plans)
    total_nodes = 0

    plan_status_counts = {}
    action_counts = {}
    languages = set()
    frame_names = []

    for frame in plans:
        frame_names.append(frame["frame_name"])
        languages.add(frame["language"])

        node_plans = frame["node_plans"]
        total_nodes += len(node_plans)

        for node in node_plans:
            plan_status = node["plan_status"]
            plan_status_counts[plan_status] = plan_status_counts.get(plan_status, 0) + 1

            for step in node["adjustment_plan"]:
                action = step["action"]
                action_counts[action] = action_counts.get(action, 0) + 1

    summary = {
        "total_frames": total_frames,
        "total_nodes": total_nodes,
        "languages": sorted(languages),
        "frame_names": sorted(frame_names),
        "plan_status_counts": plan_status_counts,
        "action_counts": action_counts,
    }

    return summary