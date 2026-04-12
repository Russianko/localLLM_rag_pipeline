from mapping_loader import get_target


def build_node_plugin_actions(node_plan: dict, mapping: dict) -> list[dict]:
    """
    Превращает план корректировок одного узла в список action-объектов
    для будущего Figma plugin.
    """

    node_name = node_plan["node_name"]
    translation_key = node_plan["translation_key"]
    text = node_plan["text"]
    plan_status = node_plan["plan_status"]
    adjustment_plan = node_plan["adjustment_plan"]

    target = get_target(mapping, translation_key)

    plugin_actions = []

    # Всегда сначала пытаемся установить текст
    plugin_actions.append(
        {
            "type": "SET_TEXT",
            "node_name": node_name,
            "translation_key": translation_key,
            "target": target,
            "text": text,
            "priority": 0,
        }
    )

    # Если план корректировок не требуется, возвращаем только SET_TEXT
    if plan_status != "planned":
        return plugin_actions

    for step in adjustment_plan:
        action_name = step["action"]

        if action_name == "reduce_font_size":
            plugin_actions.append(
                {
                    "type": "TRY_REDUCE_FONT_SIZE",
                    "node_name": node_name,
                    "translation_key": translation_key,
                    "target": target,
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
                    "target": target,
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
                    "target": target,
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
                    "target": target,
                    "text": text,
                    "value": step["value"],
                    "priority": step["priority"],
                }
            )

        else:
            plugin_actions.append(
                {
                    "type": "UNKNOWN_ACTION",
                    "node_name": node_name,
                    "translation_key": translation_key,
                    "target": target,
                    "text": text,
                    "raw_step": step,
                }
            )

    return plugin_actions


def build_frame_plugin_actions(frame_plan: dict, mapping: dict) -> dict:
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
            "actions": build_node_plugin_actions(node_plan, mapping),
        }

        node_actions.append(node_action_block)

    return {
        "frame_name": frame_name,
        "format_id": format_id,
        "language": language,
        "node_actions": node_actions,
    }


def build_plugin_actions_from_layout_plan(plans: list[dict], mapping: dict) -> list[dict]:
    results = []

    for frame_plan in plans:
        frame_actions = build_frame_plugin_actions(frame_plan, mapping)
        results.append(frame_actions)

    return results