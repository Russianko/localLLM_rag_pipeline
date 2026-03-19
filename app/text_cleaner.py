import re


class TextCleaner:
    def clean(self, text: str) -> str:
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Убираем лишние пробелы и табы
        text = re.sub(r"[ \t]+", " ", text)

        # Убираем пробелы в начале и конце строк
        text = re.sub(r" *\n *", "\n", text)

        # Схлопываем слишком много пустых строк
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()