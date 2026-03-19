from pathlib import Path

from app.summarizer import Summarizer


def main():
    clean_text_path = Path("data/extracted/sample_clean.txt")

    if not clean_text_path.exists():
        raise FileNotFoundError(f"File not found: {clean_text_path}")

    document_text = clean_text_path.read_text(encoding="utf-8")

    # Для первой версии ограничим объём текста,
    # чтобы не перегружать локальную модель
    document_text = document_text[:4000]

    summarizer = Summarizer()

    summary = summarizer.generate_summary(document_text)
    key_points = summarizer.extract_key_points(document_text)
    action_items = summarizer.extract_action_items(document_text)

    print("\n=== SUMMARY ===\n")
    print(summary)

    print("\n=== KEY POINTS ===\n")
    print(key_points)

    print("\n=== ACTION ITEMS ===\n")
    print(action_items)


if __name__ == "__main__":
    main()