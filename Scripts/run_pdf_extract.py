from pathlib import Path

from app.pdf_reader import PDFReader
from app.text_cleaner import TextCleaner


def main():
    pdf_path = "data/input/sample.pdf"
    raw_output_path = "data/extracted/sample_raw.txt"
    clean_output_path = "data/extracted/sample_clean.txt"

    reader = PDFReader()
    cleaner = TextCleaner()

    raw_text = reader.extract_text(pdf_path)
    Path(raw_output_path).write_text(raw_text, encoding="utf-8")

    clean_text = cleaner.clean(raw_text)
    Path(clean_output_path).write_text(clean_text, encoding="utf-8")

    print("PDF processed successfully.")
    print(f"Raw text length: {len(raw_text)} characters")
    print(f"Clean text length: {len(clean_text)} characters")

    print("\nFirst 1000 characters of cleaned text:\n")
    print(clean_text[:1000])


if __name__ == "__main__":
    main()