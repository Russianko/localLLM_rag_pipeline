from app.localization.figma_payload_builder import build_figma_payload
from app.localization.fit_decision_engine import decide_payload_actions
from app.localization.layout_adjustment_planner import build_payload_adjustment_plan
from app.localization.figma_plugin_action_builder import build_plugin_actions_from_layout_plan
from app.localization.plugin_action_exporter import (
    save_plugin_actions,
    load_plugin_actions,
    build_plugin_actions_summary,
)

# Пути к входным файлам
xlsx_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\input\March 2026.xlsx"
mapping_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\mapping.json"
rules_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\layout_rules.json"

# Куда сохранять plugin actions
output_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\output\figma_plugin_actions.json"

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

# 4. Строим layout plan
plans = build_payload_adjustment_plan(
    decisions=decisions,
    payload=payload,
)

# 5. Строим plugin actions
actions = build_plugin_actions_from_layout_plan(plans)

# 6. Сохраняем actions
save_plugin_actions(actions, output_path)
print(f"Plugin actions saved to: {output_path}")

# 7. Загружаем обратно
loaded_actions = load_plugin_actions(output_path)

# 8. Строим summary
summary = build_plugin_actions_summary(loaded_actions)

print("\n=== PLUGIN ACTIONS SUMMARY ===")
for key, value in summary.items():
    print(f"{key}: {value}")