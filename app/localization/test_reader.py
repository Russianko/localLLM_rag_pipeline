from app.localization.spreadsheet_reader import read_translations

file_path = r"C:\Users\ADMINSKY\Desktop\Личная LLM\data\input\March 2026.xlsx"

translations = read_translations(file_path)

print("Всего ключей:", len(translations))

for i, (key, values) in enumerate(translations.items()):
    print(f"\nKEY: {key}")
    for lang, text in list(values.items())[:5]:
        print(f"  {lang}: {text}")

    if i == 2:
        break