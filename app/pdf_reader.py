from pathlib import Path
import fitz

class PDFReader:
    def extract_text(self, pdf_path: str) -> str:
        pdf_file = Path(pdf_path)

        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        text_parts = []

        with fitz.open(pdf_file) as doc:
            for page_num, page in enumerate(doc, start=1):
                page_text = page.get_text()

                text_parts.append(f"\n--- Page {page_num} ---")
                text_parts.append(page_text)

        return "\n".join(text_parts)


    def save_extracted_text(self, pdf_path: str, output_path: str) -> str:
        text = self.extract_text(pdf_path)

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        output_file.write_text(text, encoding="utf-8")

        return text