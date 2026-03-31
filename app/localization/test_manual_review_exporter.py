from app.localization.decision_report_builder import load_decision_report
from app.localization.manual_review_extractor import extract_manual_review_items
from app.localization.manual_review_exporter import (
    save_items_to_json,
    load_items_from_json,
    build_items_summary,
)

# Путь к уже сохраненному decision report
report_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\output\decision_report.json"

# Куда сохранять список manual review items
output_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\output\manual_review_items.json"

# 1. Загружаем decision report
decision_report = load_decision_report(report_path)

# 2. Вытаскиваем manual review items
manual_review_items = extract_manual_review_items(decision_report)

# 3. Сохраняем их в отдельный JSON
save_items_to_json(manual_review_items, output_path)
print(f"Manual review items saved to: {output_path}")

# 4. Загружаем обратно для проверки
loaded_items = load_items_from_json(output_path)

# 5. Строим summary
summary = build_items_summary(loaded_items)

print("\n=== MANUAL REVIEW SUMMARY ===")
for key, value in summary.items():
    print(f"{key}: {value}")

print("\n=== ITEMS PREVIEW ===")
for item in loaded_items:
    print("\nITEM:")
    print("  frame_name:", item["frame_name"])
    print("  language:", item["language"])
    print("  node_name:", item["node_name"])
    print("  decision:", item["decision"])
    print("  text:", item["text"])