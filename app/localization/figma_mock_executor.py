def execute_mock_figma_update(payload: list[dict]) -> list[dict]:
    """
    Имитирует применение payload к Figma, но без реального подключения к Figma.

    Зачем это нужно:
    - проверить, что payload собран правильно
    - увидеть последовательность будущих действий
    - понять, какие frame и node будут обновляться
    - получить "сухой прогон" перед написанием Figma plugin

    Параметры:
    payload: list[dict]
        Список frame payload-ов, собранный build_figma_payload()

    Возвращает:
    list[dict]
        Список результатов mock-выполнения.
        Один элемент = один frame с результатами по node.
    """

    # Здесь будем собирать результат "выполнения".
    execution_results = []

    # Проходим по каждому frame, который пришел в payload.
    for frame in payload:
        frame_name = frame["frame_name"]
        format_id = frame["format_id"]
        language = frame["language"]
        nodes = frame["nodes"]

        print("\n=== MOCK FIGMA EXECUTION ===")
        print(f"Frame: {frame_name}")
        print(f"Format: {format_id}")
        print(f"Language: {language}")

        # Здесь будем хранить результат по узлам конкретного frame.
        node_results = []

        # Проходим по каждому текстовому узлу внутри frame.
        for node in nodes:
            node_name = node["node_name"]
            translation_key = node["translation_key"]
            text = node["text"]
            rules = node["rules"]

            print(f"\n  Updating node: {node_name}")
            print(f"    translation_key: {translation_key}")
            print(f"    text: {text}")
            print(f"    max_lines: {rules['max_lines']}")
            print(f"    font_range: {rules['min_font_size']} - {rules['max_font_size']}")
            print(f"    allow_short_version: {rules['allow_short_version']}")

            # Пока это mock, поэтому считаем, что обновление прошло успешно.
            # Позже на месте этого блока будет реальный вызов Figma API/plugin API.
            node_result = {
                "node_name": node_name,
                "translation_key": translation_key,
                "status": "mock_updated",
                "text_applied": text,
            }

            node_results.append(node_result)

        # Итог по frame
        frame_result = {
            "frame_name": frame_name,
            "format_id": format_id,
            "language": language,
            "status": "mock_completed",
            "nodes": node_results,
        }

        execution_results.append(frame_result)

    return execution_results