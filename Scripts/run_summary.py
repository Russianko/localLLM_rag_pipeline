import argparse

from app.vault_manager import VaultManager
from app.summarizer import Summarizer
from app.config import (
    OBSIDIAN_VAULT_DIR,
    build_clean_text_path,
    build_note_title,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Generate summary and save it to Obsidian.")
    parser.add_argument(
        "--file",
        required=True,
        help="PDF filename from local_brain/data/input, for example: sample.pdf",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    pdf_filename = args.file
    clean_text_path = build_clean_text_path(pdf_filename)

    print("Looking for:", clean_text_path)
    print("Exists:", clean_text_path.exists())

    if not clean_text_path.exists():
        raise FileNotFoundError(
            f"File not found: {clean_text_path}\nRun run_pdf_extract.py first."
        )

    document_text = clean_text_path.read_text(encoding="utf-8")
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

    vault = VaultManager(OBSIDIAN_VAULT_DIR)

    saved_path = vault.save_document_note(
        title=build_note_title(pdf_filename),
        source=pdf_filename,
        summary=summary,
        key_points=key_points if isinstance(key_points, list) else [str(key_points)],
        action_items=action_items if isinstance(action_items, list) else [str(action_items)],
    )

    print("\nSaved to Obsidian:")
    print(saved_path.resolve())


if __name__ == "__main__":
    main()