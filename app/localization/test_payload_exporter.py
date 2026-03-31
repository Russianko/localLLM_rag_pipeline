from app.localization.figma_payload_builder import build_figma_payload
from app.localization.payload_exporter import save_payload_to_json, load_payload_from_json

# Пути к входным файлам
xlsx_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\input\March 2026.xlsx"
mapping_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\mapping.json"
rules_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\layout_rules.json"

# Куда сохранять итоговый payload
output_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\output\figma_payload.json"

# 1. Собираем payload из xlsx + mapping + rules
payload = build_figma_payload(
    xlsx_path=xlsx_path,
    mapping_path=mapping_path,
    rules_path=rules_path,
)

# 2. Сохраняем payload в JSON-файл
save_payload_to_json(payload, output_path)

print(f"Payload saved to: {output_path}")

# 3. Загружаем файл обратно для проверки
loaded_payload = load_payload_from_json(output_path)

print("Loaded frames:", len(loaded_payload))

# 4. Печатаем короткую проверку содержимого
for frame in loaded_payload:
    print("\n=== FRAME ===")
    print("frame_name:", frame["frame_name"])
    print("language:", frame["language"])

    for node in frame["nodes"]:
        print(f"  {node['node_name']}: {node['text']}")