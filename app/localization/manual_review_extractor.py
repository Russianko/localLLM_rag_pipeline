def extract_nodes_by_decision(
    decision_report: dict,
    target_decisions: list[str],
) -> list[dict]:
    """
    Вытаскивает из decision report только те узлы,
    у которых decision входит в список target_decisions.

    Пример:
    target_decisions = ["manual_review_required", "try_short_version"]

    Зачем это нужно:
    - быстро получить только проблемные кейсы
    - не перебирать руками весь большой report
    - подготовить список для ручной проверки или следующего пайплайна

    Параметры:
    decision_report: dict
        Полный decision report в формате:
        {
          "summary": {...},
          "items": [...]
        }

    target_decisions: list[str]
        Список решений, которые нас интересуют.
        Например:
        ["manual_review_required", "try_short_version"]

    Возвращает:
    list[dict]
        Список найденных узлов с полезной мета-информацией.
    """

    extracted_items = []

    # В report подробные данные лежат в поле "items".
    items = decision_report["items"]

    # Проходим по каждому frame.
    for frame in items:
        frame_name = frame["frame_name"]
        format_id = frame["format_id"]
        language = frame["language"]

        # Внутри frame лежат решения по узлам.
        node_decisions = frame["node_decisions"]

        for node in node_decisions:
            decision = node["decision"]

            # Если текущее решение входит в целевой список,
            # сохраняем этот узел в итоговый список.
            if decision in target_decisions:
                extracted_items.append(
                    {
                        "frame_name": frame_name,
                        "format_id": format_id,
                        "language": language,
                        "node_name": node["node_name"],
                        "translation_key": node["translation_key"],
                        "text": node["text"],
                        "length": node["length"],
                        "estimated_max_chars": node["estimated_max_chars"],
                        "fit_status": node["fit_status"],
                        "decision": node["decision"],
                        "reason": node["reason"],
                    }
                )

    return extracted_items


def extract_manual_review_items(decision_report: dict) -> list[dict]:
    """
    Специализированная функция для ручной проверки.

    Вытаскивает только те узлы, где decision = manual_review_required.
    Это самый частый практический сценарий.
    """

    return extract_nodes_by_decision(
        decision_report=decision_report,
        target_decisions=["manual_review_required"],
    )


def extract_short_version_candidates(decision_report: dict) -> list[dict]:
    """
    Специализированная функция для кандидатов на short version.

    Вытаскивает только те узлы, где decision = try_short_version.
    """
    return extract_nodes_by_decision(
        decision_report=decision_report,
        target_decisions=["try_short_version"],
    )