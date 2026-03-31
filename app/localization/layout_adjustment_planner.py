def build_node_adjustment_plan(node_decision: dict, rules: dict) -> dict:
    """
    Строит пошаговый план layout-adjustments для одного текстового узла.

    Когда используется:
    - если fit_decision_engine выдал decision = "try_layout_adjustments"

    Что делает:
    - на основе правил слоя собирает список шагов,
      которые можно безопасно попробовать в Figma

    Параметры:
    node_decision: dict
        Решение по одному узлу из decision report.
        Пример:
        {
          "node_name": "headline",
          "decision": "try_layout_adjustments",
          ...
        }

    rules: dict
        Правила для этого узла из payload/rules.
        Пример:
        {
          "min_font_size": 20,
          "max_font_size": 26,
          "allow_line_height_reduce": True,
          ...
        }

    Возвращает:
    dict
        План корректировок для одного узла.
    """

    node_name = node_decision["node_name"]
    decision = node_decision["decision"]

    # Если для узла не нужен layout-adjustment,
    # просто возвращаем пустой план.
    if decision != "try_layout_adjustments":
        return {
            "node_name": node_name,
            "decision": decision,
            "adjustment_plan": [],
            "plan_status": "not_applicable",
        }

    adjustment_plan = []

    # 1. Сначала пробуем уменьшать font size.
    # Это обычно самый ожидаемый и безопасный шаг.
    min_font_size = rules.get("min_font_size")
    max_font_size = rules.get("max_font_size")
    font_step = rules.get("font_step", 1)

    if min_font_size is not None and max_font_size is not None:
        adjustment_plan.append(
            {
                "action": "reduce_font_size",
                "from": max_font_size,
                "to": min_font_size,
                "step": font_step,
                "priority": 1,
            }
        )

    # 2. Если разрешено уменьшать line-height,
    # добавляем это как второй шаг.
    allow_line_height_reduce = rules.get("allow_line_height_reduce", False)
    default_line_height = rules.get("default_line_height")
    min_line_height = rules.get("min_line_height")

    if allow_line_height_reduce and default_line_height is not None and min_line_height is not None:
        adjustment_plan.append(
            {
                "action": "reduce_line_height",
                "from": default_line_height,
                "to": min_line_height,
                "priority": 2,
            }
        )

    # 3. Если разрешено увеличивать текстовый блок по высоте,
    # добавляем auto resize как следующий шаг.
    allow_auto_resize_height = rules.get("allow_auto_resize_height", False)

    if allow_auto_resize_height:
        adjustment_plan.append(
            {
                "action": "enable_auto_resize_height",
                "value": True,
                "priority": 3,
            }
        )

    # 4. Если short-version разрешен, но мы сюда еще не дошли,
    # можно добавить это как запасной шаг после layout.
    allow_short_version = rules.get("allow_short_version", False)

    if allow_short_version:
        adjustment_plan.append(
            {
                "action": "fallback_to_short_version",
                "value": True,
                "priority": 4,
            }
        )

    # Если план пустой, значит у нас нет разрешенных действий.
    # Тогда это уже почти manual review.
    if not adjustment_plan:
        plan_status = "no_adjustments_available"
    else:
        plan_status = "planned"

    return {
        "node_name": node_name,
        "decision": decision,
        "adjustment_plan": adjustment_plan,
        "plan_status": plan_status,
    }


def build_frame_adjustment_plan(frame_decision: dict, frame_payload: dict) -> dict:
    """
    Строит план корректировок для всех узлов одного frame.

    Параметры:
    frame_decision: dict
        Один frame из decisions
    frame_payload: dict
        Соответствующий frame из payload

    Возвращает:
    dict
        План корректировок по frame
    """

    frame_name = frame_decision["frame_name"]
    format_id = frame_decision["format_id"]
    language = frame_decision["language"]

    node_decisions = frame_decision["node_decisions"]
    payload_nodes = frame_payload["nodes"]

    # Чтобы быстро находить rules по node_name,
    # строим словарь:
    # {
    #   "headline": {...rules...},
    #   "cta": {...rules...}
    # }
    payload_rules_by_node = {
        node["node_name"]: node["rules"]
        for node in payload_nodes
    }

    node_plans = []

    for node_decision in node_decisions:
        node_name = node_decision["node_name"]

        if node_name not in payload_rules_by_node:
            raise ValueError(
                f"Rules not found in payload for node: {node_name}"
            )

        rules = payload_rules_by_node[node_name]

        node_plan = build_node_adjustment_plan(
            node_decision=node_decision,
            rules=rules,
        )

        # Добавим ещё немного контекста,
        # чтобы потом было проще читать итоговый план.
        node_plan["translation_key"] = node_decision["translation_key"]
        node_plan["fit_status"] = node_decision["fit_status"]
        node_plan["length"] = node_decision["length"]
        node_plan["estimated_max_chars"] = node_decision["estimated_max_chars"]
        node_plan["text"] = node_decision["text"]

        node_plans.append(node_plan)

    return {
        "frame_name": frame_name,
        "format_id": format_id,
        "language": language,
        "node_plans": node_plans,
    }


def build_payload_adjustment_plan(
    decisions: list[dict],
    payload: list[dict],
) -> list[dict]:
    """
    Строит план корректировок для всего payload.

    Параметры:
    decisions: list[dict]
        Результат decide_payload_actions()

    payload: list[dict]
        Исходный figma payload

    Возвращает:
    list[dict]
        Список frame-планов
    """

    results = []

    # Чтобы быстро находить соответствующий payload по frame_name,
    # строим индекс.
    payload_by_frame_name = {
        frame["frame_name"]: frame
        for frame in payload
    }

    for frame_decision in decisions:
        frame_name = frame_decision["frame_name"]

        if frame_name not in payload_by_frame_name:
            raise ValueError(
                f"Payload frame not found for frame_name: {frame_name}"
            )

        frame_payload = payload_by_frame_name[frame_name]

        frame_plan = build_frame_adjustment_plan(
            frame_decision=frame_decision,
            frame_payload=frame_payload,
        )

        results.append(frame_plan)

    return results