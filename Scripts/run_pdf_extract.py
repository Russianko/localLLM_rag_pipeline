from app.pdf_reader import PDFReader
from app.text_cleaner import TextCleaner
from app.config import (
    CURRENT_SOURCE_PDF,
    CURRENT_RAW_TEXT_PATH,
    CURRENT_CLEAN_TEXT_PATH,
)
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Extract and clean text from PDF.")
    parser.add_argument(
        "--file",
        required=True,
        help="PDF filename from local_brain/data/input, for example: sample.pdf",
    )
    return parser.parse_args()



def main():
    args = parse_args()

    pdf_filename = args.file
    pdf_path = build_pdf_path(pdf_filename)
    raw_output_path = build_raw_text_path(pdf_filename)
    clean_output_path = build_clean_text_path(pdf_filename)

    raw_output_path.parent.mkdir(parents=True, exist_ok=True)

    print("PDF path:", pdf_path)
    print("Exists:", pdf_path.exists())

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    reader = PDFReader()
    cleaner = TextCleaner()

    raw_text = reader.extract_text(pdf_path)
    raw_output_path.write_text(raw_text, encoding="utf-8")

    clean_text = cleaner.clean(raw_text)
    clean_output_path.write_text(clean_text, encoding="utf-8")

    print("PDF processed successfully.")
    print(f"Raw text length: {len(raw_text)} characters")
    print(f"Clean text length: {len(clean_text)} characters")
    print(f"Saved raw text to: {raw_output_path}")
    print(f"Saved clean text to: {clean_output_path}")


if __name__ == "__main__":
    main()