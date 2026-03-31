from app.localization.decision_report_builder import load_decision_report
from app.localization.manual_review_extractor import (
    extract_manual_review_items,
    extract_short_version_candidates,
)

# Путь к уже сохраненному decision report
report_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\output\decision_report.json"

# 1. Загружаем готовый decision report
decision_report = load_decision_report(report_path)

# 2. Вытаскиваем только manual review
manual_review_items = extract_manual_review_items(decision_report)

# 3. Вытаскиваем кандидатов на short version
short_version_candidates = extract_short_version_candidates(decision_report)

print("=== MANUAL REVIEW ITEMS ===")
print(f"Total: {len(manual_review_items)}")

for item in manual_review_items:
    print("\nITEM:")
    print("  frame_name:", item["frame_name"])
    print("  language:", item["language"])
    print("  node_name:", item["node_name"])
    print("  translation_key:", item["translation_key"])
    print("  decision:", item["decision"])
    print("  fit_status:", item["fit_status"])
    print("  length:", item["length"])
    print("  estimated_max_chars:", item["estimated_max_chars"])
    print("  text:", item["text"])

print("\n=== SHORT VERSION CANDIDATES ===")
print(f"Total: {len(short_version_candidates)}")

for item in short_version_candidates:
    print("\nITEM:")
    print("  frame_name:", item["frame_name"])
    print("  language:", item["language"])
    print("  node_name:", item["node_name"])
    print("  translation_key:", item["translation_key"])
    print("  decision:", item["decision"])
    print("  text:", item["text"])