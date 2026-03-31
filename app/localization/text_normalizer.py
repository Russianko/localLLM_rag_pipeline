def normalize_text(text: str) -> str:
    """
    Нормализует текст перед дальнейшей обработкой.

    Задачи:
    - удалить или заменить нежелательные слова (например, бренд)
    - привести текст к более чистому виду
    - подготовить к вставке в Figma

    Пока реализуем простую версию:
    - удаляем MOSTBET
    """

    if not text:
        return text

    # Список слов/паттернов, которые нужно убрать
    unwanted_phrases = [
        "MOSTBET",
    ]

    cleaned_text = text

    for phrase in unwanted_phrases:
        cleaned_text = cleaned_text.replace(phrase, "")

    # Убираем двойные пробелы, которые могли появиться
    cleaned_text = " ".join(cleaned_text.split())

    return cleaned_text