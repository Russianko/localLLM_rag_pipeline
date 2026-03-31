def build_node_plugin_actions(node_plan: dict) -> list[dict]:
    """
    Превращает план корректировок одного узла в список action-объектов
    для будущего Figma plugin.

    На входе:
    - node_plan из layout_adjustment_planner.py

    На выходе:
    - список стандартизированных команд, которые уже можно будет
      использовать как промежуточный контракт для плагина

    Пример action:
    {
      "type": "TRY_REDUCE_FONT_SIZE",
      "node_name": "headline",
      "from": 40,
      "to": 30,
      "step": 1
    }
    """

    node_name = node_plan["node_name"]
    translation_key = node_plan["translation_key"]
    text = node_plan["text"]
    plan_status = node_plan["plan_status"]
    adjustment_plan = node_plan["adjustment_plan"]

    # Если для узла нет плана действий,
    # возвращаем пустой список.
    if plan_status != "planned":
        return []

    plugin_actions = []

    # Превращаем каждый абстрактный шаг в более формальную plugin-команду.
    for step in adjustment_plan:
        action_name = step["action"]

        if action_name == "reduce_font_size":
            plugin_actions.append(
                {
                    "type": "TRY_REDUCE_FONT_SIZE",
                    "node_name": node_name,
                    "translation_key": translation_key,
                    "text": text,
                    "from": step["from"],
                    "to": step["to"],
                    "step": step["step"],
                    "priority": step["priority"],
                }
            )

        elif action_name == "reduce_line_height":
            plugin_actions.append(
                {
                    "type": "TRY_REDUCE_LINE_HEIGHT",
                    "node_name": node_name,
                    "translation_key": translation_key,
                    "text": text,
                    "from": step["from"],
                    "to": step["to"],
                    "priority": step["priority"],
                }
            )

        elif action_name == "enable_auto_resize_height":
            plugin_actions.append(
                {
                    "type": "TRY_ENABLE_AUTO_RESIZE_HEIGHT",
                    "node_name": node_name,
                    "translation_key": translation_key,
                    "text": text,
                    "value": step["value"],
                    "priority": step["priority"],
                }
            )

        elif action_name == "fallback_to_short_version":
            plugin_actions.append(
                {
                    "type": "TRY_FALLBACK_TO_SHORT_VERSION",
                    "node_name": node_name,
                    "translation_key": translation_key,
                    "text": text,
                    "value": step["value"],
                    "priority": step["priority"],
                }
            )

        else:
            # Если встретился неизвестный action,
            # лучше явно сохранить это в выходных данных,
            # чем молча потерять шаг.
            plugin_actions.append(
                {
                    "type": "UNKNOWN_ACTION",
                    "node_name": node_name,
                    "translation_key": translation_key,
                    "text": text,
                    "raw_step": step,
                }
            )

    return plugin_actions


def build_frame_plugin_actions(frame_plan: dict) -> dict:
    """
    Превращает план одного frame в набор plugin actions.

    На выходе:
    {
      "frame_name": "...",
      "format_id": "...",
      "language": "...",
      "node_actions": [...]
    }

    Где node_actions — это список узлов,
    а у каждого узла уже есть список plugin-команд.
    """

    frame_name = frame_plan["frame_name"]
    format_id = frame_plan["format_id"]
    language = frame_plan["language"]

    node_actions = []

    for node_plan in frame_plan["node_plans"]:
        node_action_block = {
            "node_name": node_plan["node_name"],
            "translation_key": node_plan["translation_key"],
            "decision": node_plan["decision"],
            "plan_status": node_plan["plan_status"],
            "actions": build_node_plugin_actions(node_plan),
        }

        node_actions.append(node_action_block)

    return {
        "frame_name": frame_name,
        "format_id": format_id,
        "language": language,
        "node_actions": node_actions,
    }


def build_plugin_actions_from_layout_plan(plans: list[dict]) -> list[dict]:
    """
    Превращает весь layout adjustment plan в plugin action payload.

    Это уже почти прямой мост к будущему Figma plugin.

    Параметры:
    plans: list[dict]
        Результат build_payload_adjustment_plan()

    Возвращает:
    list[dict]
        Список frame-блоков с plugin actions
    """

    results = []

    for frame_plan in plans:
        frame_actions = build_frame_plugin_actions(frame_plan)
        results.append(frame_actions)

    return results