from app.localization.figma_payload_builder import build_figma_payload
from app.localization.fit_decision_engine import decide_payload_actions
from app.localization.layout_adjustment_planner import build_payload_adjustment_plan
from app.localization.layout_plan_exporter import (
    save_layout_plan,
    load_layout_plan,
    build_layout_plan_summary,
)

# Пути к входным файлам
xlsx_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\input\March 2026.xlsx"
mapping_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\mapping.json"
rules_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\layout_rules.json"

# Куда сохранять layout plan
output_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\output\layout_adjustment_plan.json"

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

# 3. Получаем decisions
decisions = decide_payload_actions(
    payload=payload,
    char_limits_by_format=char_limits_by_format,
)

# 4. Строим планы корректировок
plans = build_payload_adjustment_plan(
    decisions=decisions,
    payload=payload,
)

# 5. Сохраняем план в JSON
save_layout_plan(plans, output_path)
print(f"Layout plan saved to: {output_path}")

# 6. Загружаем обратно
loaded_plans = load_layout_plan(output_path)

# 7. Строим summary
summary = build_layout_plan_summary(loaded_plans)

print("\n=== LAYOUT PLAN SUMMARY ===")
for key, value in summary.items():
    print(f"{key}: {value}")