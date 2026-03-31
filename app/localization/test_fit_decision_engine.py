from app.localization.figma_payload_builder import build_figma_payload
from app.localization.fit_decision_engine import decide_payload_actions

# Пути к входным файлам
xlsx_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\input\March 2026.xlsx"
mapping_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\mapping.json"
rules_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\layout_rules.json"

# 1. Собираем payload
payload = build_figma_payload(
    xlsx_path=xlsx_path,
    mapping_path=mapping_path,
    rules_path=rules_path,
)

# 2. Временные лимиты по символам для формата
# Это пока эвристика, не реальные измерения в Figma.
char_limits_by_format = {
    "1080x1080": {
        "headline": 25,
        "subheadline": 45,
        "cta": 18,
    }
}

# 3. Получаем решения по всему payload
decisions = decide_payload_actions(
    payload=payload,
    char_limits_by_format=char_limits_by_format,
)

# 4. Печатаем результат
for frame in decisions:
    print("\n=== FRAME DECISIONS ===")
    print("frame_name:", frame["frame_name"])
    print("format_id:", frame["format_id"])
    print("language:", frame["language"])

    for node in frame["node_decisions"]:
        print("\n  NODE:")
        print("   node_name:", node["node_name"])
        print("   translation_key:", node["translation_key"])
        print("   length:", node["length"])
        print("   estimated_max_chars:", node["estimated_max_chars"])
        print("   fit_status:", node["fit_status"])
        print("   decision:", node["decision"])
        print("   reason:", node["reason"])