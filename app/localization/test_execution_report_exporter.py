from app.localization.figma_payload_builder import build_figma_payload
from app.localization.figma_mock_executor import execute_mock_figma_update
from app.localization.execution_report_exporter import (
    save_execution_report,
    load_execution_report,
    build_execution_summary,
)

# Пути к входным файлам
xlsx_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\input\March 2026.xlsx"
mapping_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\mapping.json"
rules_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\layout_rules.json"

# Путь, куда сохранять execution report
output_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\output\figma_execution_report.json"

# 1. Собираем payload
payload = build_figma_payload(
    xlsx_path=xlsx_path,
    mapping_path=mapping_path,
    rules_path=rules_path,
)

# 2. Делаем mock execution
results = execute_mock_figma_update(payload)

# 3. Сохраняем execution report
save_execution_report(results, output_path)
print(f"\nExecution report saved to: {output_path}")

# 4. Загружаем report обратно
loaded_results = load_execution_report(output_path)

# 5. Строим summary
summary = build_execution_summary(loaded_results)

print("\n=== EXECUTION SUMMARY ===")
for key, value in summary.items():
    print(f"{key}: {value}")