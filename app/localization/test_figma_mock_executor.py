from app.localization.figma_payload_builder import build_figma_payload
from app.localization.figma_mock_executor import execute_mock_figma_update

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

# 2. Запускаем mock execution
results = execute_mock_figma_update(payload)

print("\n=== MOCK EXECUTION SUMMARY ===")
print(f"Total frames processed: {len(results)}")

for frame in results:
    print(f"\nFrame: {frame['frame_name']}")
    print(f"Status: {frame['status']}")

    for node in frame["nodes"]:
        print(f"  Node: {node['node_name']} -> {node['status']}")