from app.localization.localization_pipeline import run_localization_check
from app.localization.overflow_extractor import extract_overflows

file_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\input\March 2026.xlsx"

limits = {
    "gameHistory.sell.question": 45,
    "gameHistory.sell.title": 25,
    "resetting.request.subtitle_email": 60,
}

result = run_localization_check(file_path, limits)

overflows = extract_overflows(result)

print("TOTAL OVERFLOWS:", len(overflows))

for item in overflows[:5]:
    print(item)