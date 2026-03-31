from pathlib import Path
from app.localization.mapping_loader import load_mapping, get_frames
from app.localization.rules_loader import load_rules, get_format_rules

mapping_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\mapping.json"
rules_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\config\layout_rules.json"

print("RULES PATH:", rules_path)
print("EXISTS:", Path(rules_path).exists())

mapping = load_mapping(mapping_path)
rules = load_rules(rules_path)

print("=== MAPPING ===")
frames = get_frames(mapping)

for frame in frames:
    print(f"Frame: {frame['frame_name']}")
    print(f"  Language: {frame['language']}")
    print(f"  Fields: {frame['fields']}")

print("\n=== RULES ===")
format_rules = get_format_rules(rules, "1080x1080")

for field_name, rule in format_rules.items():
    print(f"\nField: {field_name}")
    for k, v in rule.items():
        print(f"  {k}: {v}")