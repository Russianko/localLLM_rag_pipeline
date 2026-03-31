from app.localization.figma_payload_builder import build_figma_payload

# Укажи реальные пути к своим файлам
xlsx_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\input\March 2026.xlsx"
mapping_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\mapping.json"
rules_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\layout_rules.json"

payload = build_figma_payload(
    xlsx_path=xlsx_path,
    mapping_path=mapping_path,
    rules_path=rules_path,
)

print("TOTAL FRAMES:", len(payload))

for frame in payload:
    print("\n=== FRAME ===")
    print("frame_name:", frame["frame_name"])
    print("format_id:", frame["format_id"])
    print("language:", frame["language"])

    for node in frame["nodes"]:
        print("\n  NODE:")
        print("   node_name:", node["node_name"])
        print("   translation_key:", node["translation_key"])
        print("   text:", node["text"])
        print("   rules:", node["rules"])