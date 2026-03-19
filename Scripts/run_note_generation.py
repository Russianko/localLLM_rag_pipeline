from pathlib import Path

from app.note_writer import NoteWriter
from app.summarizer import Summarizer


def main():
    clean_text_path = Path("data/extracted/sample_clean.txt")
    source_pdf_path = "data/input/sample.pdf"
    output_note_path = "data/notes/sample.md"

    if not clean_text_path.exists():
        raise FileNotFoundError(f"File not found: {clean_text_path}")

    document_text = clean_text_path.read_text(encoding="utf-8")

    # Ограничиваем объём для первой версии
    document_text = document_text[:4000]

    summarizer = Summarizer()
    note_writer = NoteWriter()

    summary = summarizer.generate_summary(document_text)
    key_points = summarizer.extract_key_points(document_text)
    action_items = summarizer.extract_action_items(document_text)

    note_content = note_writer.save_note(
        output_path=output_note_path,
        title="sample",
        source=source_pdf_path,
        summary=summary,
        key_points=key_points,
        action_items=action_items,
    )

    print("Note generated successfully.")
    print(f"Saved to: {output_note_path}")
    print("\nFirst 1000 characters of note:\n")
    print(note_content[:1000])


if __name__ == "__main__":
    main()