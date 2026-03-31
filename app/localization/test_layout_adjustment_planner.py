from app.localization.figma_payload_builder import build_figma_payload
from app.localization.fit_decision_engine import decide_payload_actions
from app.localization.layout_adjustment_planner import build_payload_adjustment_plan

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

# 2. Временные лимиты по символам
char_limits_by_format = {
    "1080x1080": {
        "headline": 25,
        "subheadline": 45,
        "cta": 18,
    }
}

# 3. Получаем решения
decisions = decide_payload_actions(
    payload=payload,
    char_limits_by_format=char_limits_by_format,
)

# 4. Строим план корректировок
plans = build_payload_adjustment_plan(
    decisions=decisions,
    payload=payload,
)

# 5. Печатаем результат
for frame in plans:
    print("\n=== FRAME ADJUSTMENT PLAN ===")
    print("frame_name:", frame["frame_name"])
    print("language:", frame["language"])

    for node in frame["node_plans"]:
        print("\n  NODE:")
        print("   node_name:", node["node_name"])
        print("   decision:", node["decision"])
        print("   plan_status:", node["plan_status"])

        for step in node["adjustment_plan"]:
            print("    STEP:", step)