import json
from pathlib import Path


def save_plugin_actions(actions: list[dict], output_path: str) -> None:
    """
    Сохраняет plugin actions в JSON-файл.

    Что это за actions:
    - это результат работы figma_plugin_action_builder.py
    - список frame-блоков
    - внутри каждого frame лежат node_actions
    - внутри node_actions лежат конкретные action-команды

    Зачем это нужно:
    - чтобы использовать actions как отдельный артефакт пайплайна
    - чтобы потом этот JSON можно было читать в Figma plugin
    - чтобы удобно дебажить и просматривать команды отдельно

    Параметры:
    actions: list[dict]
        Список frame actions

    output_path: str
        Путь, куда сохранить JSON-файл
    """

    file_path = Path(output_path)

    # Создаем папку назначения, если её ещё нет.
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Сохраняем JSON в UTF-8, чтобы кириллица не превращалась в \uXXXX.
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(actions, f, ensure_ascii=False, indent=2)


def load_plugin_actions(input_path: str) -> list[dict]:
    """
    Загружает plugin actions обратно из JSON-файла.

    Это полезно:
    - для проверки, что файл сохранился корректно
    - для следующего этапа пайплайна
    - для будущего Figma plugin executor

    Параметры:
    input_path: str
        Путь к JSON-файлу

    Возвращает:
    list[dict]
        Загруженные plugin actions
    """

    file_path = Path(input_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Plugin actions file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def build_plugin_actions_summary(actions: list[dict]) -> dict:
    """
    Строит краткую сводку по plugin actions.

    Что считаем:
    - сколько frame
    - сколько node всего
    - сколько action-команд всего
    - какие типы action встречаются
    - какие языки есть

    Параметры:
    actions: list[dict]
        Список frame-блоков с plugin actions

    Возвращает:
    dict
        Краткая сводка
    """

    total_frames = len(actions)
    total_nodes = 0
    total_actions = 0

    action_type_counts = {}
    languages = set()
    frame_names = []

    for frame in actions:
        frame_names.append(frame["frame_name"])
        languages.add(frame["language"])

        node_actions = frame["node_actions"]
        total_nodes += len(node_actions)

        for node in node_actions:
            for action in node["actions"]:
                total_actions += 1

                action_type = action["type"]
                action_type_counts[action_type] = action_type_counts.get(action_type, 0) + 1

    summary = {
        "total_frames": total_frames,
        "total_nodes": total_nodes,
        "total_actions": total_actions,
        "languages": sorted(languages),
        "frame_names": sorted(frame_names),
        "action_type_counts": action_type_counts,
    }

    return summary