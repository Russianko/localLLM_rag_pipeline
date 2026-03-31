from app.localization.figma_payload_builder import build_figma_payload
from app.localization.fit_decision_engine import decide_payload_actions
from app.localization.decision_report_builder import (
    build_decision_report,
    load_decision_report,
    save_decision_report,
)

# Пути к входным файлам
xlsx_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\input\March 2026.xlsx"
mapping_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\mapping.json"
rules_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\layout_rules.json"

# Куда сохранять decision report
output_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\output\decision_report.json"

# 1. Собираем payload
payload = build_figma_payload(
    xlsx_path=xlsx_path,
    mapping_path=mapping_path,
    rules_path=rules_path,
)

# 2. Задаем временные лимиты по символам
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

# 4. Собираем полный отчет
report = build_decision_report(decisions)

# 5. Сохраняем его
save_decision_report(report, output_path)
print(f"Decision report saved to: {output_path}")

# 6. Загружаем обратно
loaded_report = load_decision_report(output_path)

# 7. Печатаем summary
print("\n=== DECISION REPORT SUMMARY ===")
for key, value in loaded_report["summary"].items():
    print(f"{key}: {value}")