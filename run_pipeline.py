import argparse
from pprint import pprint
from app.config import get_default_pipeline_params

from app.pipeline_service import PipelineService


defaults = get_default_pipeline_params()

parser.add_argument("--summary-limit", default=defaults["summary_limit"])
parser.add_argument("--chunk-size", default=defaults["chunk_size"])
parser.add_argument("--overlap", default=defaults["overlap"])
parser.add_argument("--top-k", default=defaults["top_k"])

def parse_args():
    parser = argparse.ArgumentParser(
        description="Run local assistant pipeline for a PDF document."
    )
    parser.add_argument(
        "--file",
        required=True,
        help="PDF filename from local_brain/data/input, for example: sample.pdf",
    )
    parser.add_argument(
        "--question",
        required=False,
        default="О чем этот документ?",
        help="Question for RAG.",
    )
    parser.add_argument(
        "--summary-limit",
        required=False,
        type=int,
        default=4000,
        help="Max number of characters passed to summarizer.",
    )
    parser.add_argument(
        "--chunk-size",
        required=False,
        type=int,
        default=500,
        help="Chunk size for RAG.",
    )
    parser.add_argument(
        "--overlap",
        required=False,
        type=int,
        default=100,
        help="Chunk overlap for RAG.",
    )
    parser.add_argument(
        "--top-k",
        required=False,
        type=int,
        default=3,
        help="Number of top chunks for RAG.",
    )
    parser.add_argument(
        "--response-mode",
        required=False,
        default="detailed",
        help="Response mode: short, detailed, expert.",
    )
    parser.add_argument(
        "--skip-process",
        action="store_true",
        help="Skip explicit processing step and rely on ask(auto_process=True).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    service = PipelineService()

    print("=== PIPELINE START ===")
    print(f"FILE: {args.file}")
    print(f"QUESTION: {args.question}")
    print(f"RESPONSE MODE: {args.response_mode}")

    if not args.skip_process:
        print("\n[1/2] Processing document...")
        process_result = service.process_document(
            filename=args.file,
            summary_limit=args.summary_limit,
            chunk_size=args.chunk_size,
            overlap=args.overlap,
        )

        print("Document processed.")
        print("Summary path:", process_result.get("summary_path"))
        print("Chunks path:", process_result.get("chunks_path"))
        print("Embeddings path:", process_result.get("embeddings_path"))
        print("Chunks count:", process_result.get("chunks_count"))

    print("\n[2/2] Asking question...")
    ask_result = service.ask_document(
        filename=args.file,
        question=args.question,
        top_k=args.top_k,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        auto_process=True,
        response_mode=args.response_mode,
    )

    print("\n=== RESULT ===")
    print(f"\nQUESTION:\n{ask_result['question']}\n")
    print("ANSWER:\n")
    print(ask_result["answer"])

    print("\nTOP CHUNKS USED:\n")
    for item in ask_result.get("top_chunks", []):
        print(f"===== CHUNK {item['chunk_id']} | score={item['score']:.4f} =====")
        print(item["text"][:700])
        print()

    print("RAG note saved to:")
    print(ask_result["rag_note_path"])

    print("\n=== PIPELINE DONE ===")


if __name__ == "__main__":
    main()