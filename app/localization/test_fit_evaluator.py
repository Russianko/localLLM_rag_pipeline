from app.localization.fit_evaluator import evaluate_text

samples = [
    ("Shop now", 12),
    ("Big Summer Sale", 12),
    ("Введите адрес электронной почты", 20),
]

for text, limit in samples:
    result = evaluate_text(text, limit)
    print(result)