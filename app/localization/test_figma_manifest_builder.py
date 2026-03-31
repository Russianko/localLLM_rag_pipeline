from app.localization.figma_payload_builder import build_figma_payload
from app.localization.figma_manifest_builder import build_figma_manifest

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

# 2. На основе payload строим manifest
manifest = build_figma_manifest(payload)

print("=== FIGMA MANIFEST ===")
for key, value in manifest.items():
    print(f"{key}: {value}")