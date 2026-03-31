from app.localization.fit_evaluator import evaluate_text


def decide_node_action(text: str, rules: dict, estimated_max_chars: int) -> dict:
    """
    Принимает решение, что делать с текстом перед применением в Figma.

    Это пока "логический движок", а не реальный layout engine.
    Он не знает реальную ширину текста в Figma, но уже может дать
    полезное предварительное решение на основе:
    - длины текста
    - лимита символов
    - правил слоя

    Параметры:
    text: str
        Текст, который собираемся вставить в слой.

    rules: dict
        Правила конкретного слоя, например:
        - min_font_size
        - max_font_size
        - allow_short_version
        - allow_line_height_reduce
        - allow_auto_resize_height

    estimated_max_chars: int
        Приблизительный лимит по символам для этого слоя.
        Это временная эвристика, пока у нас нет реального Figma layout check.

    Возвращает:
    dict
        Решение вида:
        {
          "text": "...",
          "length": 42,
          "estimated_max_chars": 35,
          "fit_status": "overflow",
          "decision": "try_reduce_font",
          "reason": "...",
          "allow_short_version": True
        }
    """

    # Сначала считаем базовую оценку текста:
    # длину, лимит и fit_status.
    evaluation = evaluate_text(text, estimated_max_chars)

    fit_status = evaluation["fit_status"]
    allow_short_version = rules.get("allow_short_version", False)
    allow_line_height_reduce = rules.get("allow_line_height_reduce", False)
    allow_auto_resize_height = rules.get("allow_auto_resize_height", False)

    # По умолчанию заполним переменные решения.
    decision = "unknown"
    reason = ""

    # Если текст явно влезает,
    # лучше ничего не трогать и применить как есть.
    if fit_status == "fit":
        decision = "apply_as_is"
        reason = "Text fits within the estimated character limit."

    # Если текст на грани, это не авария.
    # Можно применять как есть, но помечать как зону внимания.
    elif fit_status == "borderline":
        decision = "apply_with_caution"
        reason = (
            "Text is close to the estimated limit. "
            "It may still fit, but should be checked in layout."
        )

    # Если overflow, начинаем думать, что можно сделать.
    elif fit_status == "overflow":
        # Самый мягкий вариант:
        # если разрешено менять line-height или увеличивать блок по высоте,
        # пробуем сначала это, а не short-version.
        if allow_line_height_reduce or allow_auto_resize_height:
            decision = "try_layout_adjustments"
            reason = (
                "Text exceeds the estimated limit. "
                "Try layout adjustments first "
                "(line height reduction and/or auto resize)."
            )

        # Если layout adjustment не разрешены,
        # но short-version разрешен, можно предлагать short fallback.
        elif allow_short_version:
            decision = "try_short_version"
            reason = (
                "Text exceeds the estimated limit and layout adjustments "
                "are restricted. Short version may be needed."
            )

        # Если ни layout, ни short-version нельзя,
        # значит это уже ручная проверка.
        else:
            decision = "manual_review_required"
            reason = (
                "Text exceeds the estimated limit. "
                "No safe automatic adjustment is allowed."
            )

    result = {
        "text": evaluation["text"],
        "length": evaluation["length"],
        "estimated_max_chars": evaluation["max_chars"],
        "fit_status": fit_status,
        "decision": decision,
        "reason": reason,
        "allow_short_version": allow_short_version,
    }

    return result


def decide_frame_actions(frame_payload: dict, char_limits_by_node: dict[str, int]) -> dict:
    """
    Принимает решения по всем текстовым узлам внутри одного frame.

    Параметры:
    frame_payload: dict
        Один frame из figma payload.
        Например:
        {
          "frame_name": "...",
          "format_id": "...",
          "language": "...",
          "nodes": [...]
        }

    char_limits_by_node: dict[str, int]
        Пример:
        {
          "headline": 25,
          "subheadline": 45,
          "cta": 18
        }

        Это временные лимиты по символам для узлов.
        Потом они могут стать:
        - частью layout_rules.json
        - или результатом реального Figma measurement

    Возвращает:
    dict
        Frame с решениями по каждому node.
    """

    frame_name = frame_payload["frame_name"]
    format_id = frame_payload["format_id"]
    language = frame_payload["language"]
    nodes = frame_payload["nodes"]

    node_decisions = []

    for node in nodes:
        node_name = node["node_name"]
        text = node["text"]
        rules = node["rules"]
        translation_key = node["translation_key"]

        # Для каждого node нужен лимит по символам.
        # Если лимит не передан, сразу выдаем понятную ошибку.
        if node_name not in char_limits_by_node:
            raise ValueError(
                f"Character limit not provided for node: {node_name}"
            )

        estimated_max_chars = char_limits_by_node[node_name]

        # Получаем решение по конкретному node.
        decision_result = decide_node_action(
            text=text,
            rules=rules,
            estimated_max_chars=estimated_max_chars,
        )

        # Добавляем полезную мета-информацию.
        decision_result["node_name"] = node_name
        decision_result["translation_key"] = translation_key

        node_decisions.append(decision_result)

    frame_decision = {
        "frame_name": frame_name,
        "format_id": format_id,
        "language": language,
        "node_decisions": node_decisions,
    }

    return frame_decision


def decide_payload_actions(
    payload: list[dict],
    char_limits_by_format: dict[str, dict[str, int]],
) -> list[dict]:
    """
    Принимает решения по всему payload.

    Параметры:
    payload: list[dict]
        Список frame payload-ов.

    char_limits_by_format: dict[str, dict[str, int]]
        Пример:
        {
          "1080x1080": {
            "headline": 25,
            "subheadline": 45,
            "cta": 18
          }
        }

    Возвращает:
    list[dict]
        Список frame-решений.
    """

    results = []

    for frame in payload:
        format_id = frame["format_id"]

        if format_id not in char_limits_by_format:
            raise ValueError(
                f"Character limits not found for format: {format_id}"
            )

        char_limits_by_node = char_limits_by_format[format_id]

        frame_result = decide_frame_actions(
            frame_payload=frame,
            char_limits_by_node=char_limits_by_node,
        )

        results.append(frame_result)

    return results