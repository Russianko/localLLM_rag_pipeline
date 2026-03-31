from app.localization.localization_pipeline import run_localization_check
from app.localization.report_builder import save_report_to_json

file_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\input\March 2026.xlsx"

limits = {
    "gameHistory.sell.question": 45,
    "gameHistory.sell.title": 25,
    "resetting.request.subtitle_email": 60,
}

result = run_localization_check(file_path, limits)

output_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\output\localization_report.json"
save_report_to_json(result, output_path)

print(f"Report saved to: {output_path}")