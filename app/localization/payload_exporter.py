import json
from pathlib import Path


def save_payload_to_json(payload: list[dict], output_path: str) -> None:
    """
    Сохраняет готовый Figma payload в JSON-файл.

    Зачем это нужно:
    - чтобы видеть итоговую структуру не только в print()
    - чтобы потом этот файл мог читать Figma plugin
    - чтобы проще было отлаживать пайплайн шаг за шагом

    Параметры:
    payload: list[dict]
        Список frame payload-ов, который вернул build_figma_payload()

    output_path: str
        Путь, куда сохранить итоговый JSON

    Что делает функция:
    1. Создает родительскую папку, если её ещё нет
    2. Сохраняет payload в UTF-8
    3. Делает JSON "красивым" через indent=2,
       чтобы его можно было нормально читать глазами
    """

    # Path удобен для работы с путями и делает код чище.
    file_path = Path(output_path)

    # Если папки ещё нет, создаём её.
    # parents=True позволяет создать сразу всю цепочку папок,
    # если они отсутствуют.
    # exist_ok=True не даст ошибку, если папка уже существует.
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Открываем файл на запись в UTF-8.
    # ensure_ascii=False нужен, чтобы кириллица и другие символы
    # сохранялись нормально, а не в виде \uXXXX.
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def load_payload_from_json(input_path: str) -> list[dict]:
    """
    Загружает payload обратно из JSON-файла.

    Это полезно:
    - для проверки, что файл сохранился корректно
    - для будущего Figma plugin / промежуточных тестов
    - для повторного использования уже собранного payload
      без повторной генерации

    Параметры:
    input_path: str
        Путь к JSON-файлу с payload

    Возвращает:
    list[dict]
        Payload в том же виде, в каком он был сохранён
    """

    file_path = Path(input_path)

    # Если файла нет, сразу отдаём понятную ошибку.
    if not file_path.exists():
        raise FileNotFoundError(f"Payload file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data