import argparse

from app.chunker import TextChunker
from app.embedder import Embedder
from app.rag_answerer import RAGAnswerer
from app.vault_manager import VaultManager
from app.config import (
    OBSIDIAN_VAULT_DIR,
    build_clean_text_path,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Ask a question about a PDF via RAG.")
    parser.add_argument(
        "--file",
        required=True,
        help="PDF filename from local_brain/data/input, for example: sample.pdf",
    )
    parser.add_argument(
        "--question",
        required=False,
        default="Для какой из сторон этот документ сильнее?",
        help="Question for RAG.",
    )
    return parser.parse_args()


def normalize_chunks(top_chunks):
    normalized = []

    for i, item in enumerate(top_chunks):
        normalized.append({
            "chunk_id": i,
            "text": item["chunk"],
            "score": item["score"],
        })

    return normalized


def main():
    args = parse_args()

    pdf_filename = args.file
    question = args.question
    clean_text_path = build_clean_text_path(pdf_filename)

    print("Looking for:", clean_text_path)
    print("Exists:", clean_text_path.exists())

    if not clean_text_path.exists():
        raise FileNotFoundError(
            f"File not found: {clean_text_path}\nRun run_pdf_extract.py first."
        )

    text = clean_text_path.read_text(encoding="utf-8")

    chunker = TextChunker(chunk_size=500, overlap=100)
    chunks = chunker.chunk_text(text)

    embedder = Embedder()
    chunk_embeddings = embedder.embed_chunks(chunks)

    rag = RAGAnswerer(embedder=embedder)
    result = rag.answer_question(
        question=question,
        chunks=chunks,
        chunk_embeddings=chunk_embeddings,
        top_k=3,
    )

    vault = VaultManager(OBSIDIAN_VAULT_DIR)
    normalized_chunks = normalize_chunks(result["top_chunks"])

    saved_path = vault.save_rag_answer(
        question=question,
        answer=result["answer"],
        used_chunks=normalized_chunks,
        source_document=pdf_filename,
    )

    print(f"\nQUESTION:\n{question}\n")
    print("ANSWER:\n")
    print(result["answer"])

    print("\nTOP CHUNKS USED:\n")
    for i, item in enumerate(result["top_chunks"], start=1):
        print(f"===== CHUNK {i} | score={item['score']:.4f} =====")
        print(item["chunk"][:700])
        print("\n")

    print("Saved to Obsidian:")
    print(saved_path.resolve())


if __name__ == "__main__":
    main()