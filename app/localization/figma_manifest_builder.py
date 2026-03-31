def build_figma_manifest(payload: list[dict]) -> dict:
    """
    Строит краткую сводку (manifest) по готовому Figma payload.

    Зачем это нужно:
    - быстро понять, что именно собралось
    - увидеть количество frame и node
    - получить список языков
    - получить список использованных translation keys
    - в будущем можно прикладывать manifest к отчету или API-ответу

    Параметры:
    payload: list[dict]
        Список frame payload-ов, который мы уже собрали ранее.

    Возвращает:
    dict
        Краткую сводку по payload.
    """

    # Считаем общее количество frame.
    total_frames = len(payload)

    # Это будет общее количество текстовых узлов во всех frame.
    total_nodes = 0

    # Множества используем, чтобы не было дублей.
    # Потом превратим их в отсортированные списки.
    languages = set()
    format_ids = set()
    translation_keys = set()
    frame_names = []

    # Проходим по каждому frame в payload.
    for frame in payload:
        # Забираем базовую информацию по frame.
        frame_name = frame["frame_name"]
        format_id = frame["format_id"]
        language = frame["language"]
        nodes = frame["nodes"]

        frame_names.append(frame_name)
        format_ids.add(format_id)
        languages.add(language)

        # Увеличиваем общее число узлов.
        total_nodes += len(nodes)

        # Из каждого узла собираем translation_key.
        for node in nodes:
            translation_keys.add(node["translation_key"])

    # Собираем итоговый manifest.
    # sorted(...) нужен, чтобы результат был стабильным и аккуратным.
    manifest = {
        "total_frames": total_frames,
        "total_nodes": total_nodes,
        "languages": sorted(languages),
        "format_ids": sorted(format_ids),
        "frame_names": sorted(frame_names),
        "translation_keys": sorted(translation_keys),
    }

    return manifest