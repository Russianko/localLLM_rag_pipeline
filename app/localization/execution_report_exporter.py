import json
from pathlib import Path


def save_execution_report(results: list[dict], output_path: str) -> None:
    """
    Сохраняет execution results в JSON-файл.

    Что такое execution results:
    - это результат работы mock executor
    - позже это будет и результат реального Figma executor

    Зачем это нужно:
    - чтобы не терять результат после завершения скрипта
    - чтобы можно было открыть отчет глазами
    - чтобы потом сравнивать "что планировалось" и "что реально применилось"
    - чтобы использовать этот отчет как артефакт пайплайна

    Параметры:
    results: list[dict]
        Список результатов выполнения по frame и node

    output_path: str
        Путь, куда сохранить JSON-отчет
    """

    # Превращаем строковый путь в Path-объект для более удобной работы с путями.
    file_path = Path(output_path)

    # Создаем родительскую папку, если она еще не существует.
    # parents=True создаст всю цепочку папок.
    # exist_ok=True не даст ошибку, если папка уже есть.
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Сохраняем JSON в UTF-8, чтобы кириллица и другие символы
    # хранились нормально и читались без мусора.
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def load_execution_report(input_path: str) -> list[dict]:
    """
    Загружает execution report обратно из JSON-файла.

    Это полезно:
    - для проверки, что файл сохранился корректно
    - для последующего анализа
    - для будущего UI / API / debugging flow

    Параметры:
    input_path: str
        Путь к execution report JSON

    Возвращает:
    list[dict]
        Загруженный отчет
    """

    file_path = Path(input_path)

    # Если файла нет, сразу даем понятную ошибку.
    if not file_path.exists():
        raise FileNotFoundError(f"Execution report not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def build_execution_summary(results: list[dict]) -> dict:
    """
    Строит краткую сводку по execution results.

    Зачем это нужно:
    - быстро понять, сколько frame обработано
    - сколько всего node прошло через executor
    - какие статусы получились

    Параметры:
    results: list[dict]
        Результаты mock или real execution

    Возвращает:
    dict
        Краткая сводка по выполнению
    """

    total_frames = len(results)
    total_nodes = 0

    frame_statuses = {}
    node_statuses = {}

    # Проходим по каждому frame-результату
    for frame in results:
        frame_status = frame["status"]

        # Считаем статусы frame
        frame_statuses[frame_status] = frame_statuses.get(frame_status, 0) + 1

        nodes = frame["nodes"]
        total_nodes += len(nodes)

        # Считаем статусы node
        for node in nodes:
            node_status = node["status"]
            node_statuses[node_status] = node_statuses.get(node_status, 0) + 1

    summary = {
        "total_frames": total_frames,
        "total_nodes": total_nodes,
        "frame_statuses": frame_statuses,
        "node_statuses": node_statuses,
    }

    return summary