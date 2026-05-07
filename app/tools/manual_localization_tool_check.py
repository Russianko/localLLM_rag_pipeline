from app.tools.localization_tool import LocalizationTool


tool = LocalizationTool()

result = tool.execute(
    xlsx_path=r"C:\Users\ADMINSKY\Desktop\local_ai_station\data\input\March 2026.xlsx",
    mapping_path=r"C:\Users\ADMINSKY\Desktop\local_ai_station\config\mapping.json",
    rules_path=r"C:\Users\ADMINSKY\Desktop\local_ai_station\config\layout_rules.json",
)

print("success:", result.success)
print("message:", result.message)

if result.success:
    print("summary:", result.data["summary"])
else:
    print("error data:", result.data)