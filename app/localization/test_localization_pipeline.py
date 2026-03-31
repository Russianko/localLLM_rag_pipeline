from app.localization.localization_pipeline import run_localization_check

file_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\input\March 2026.xlsx"

limits = {
    "gameHistory.sell.question": 45,
    "gameHistory.sell.title": 25,
    "resetting.request.subtitle_email": 60,
}

result = run_localization_check(file_path, limits)

for key, langs in result.items():
    print(f"\nKEY: {key}")
    for lang, data in list(langs.items())[:5]:
        print(
            f"  {lang}: len={data['length']} / {data['max_chars']} -> {data['fit_status']}"
        )