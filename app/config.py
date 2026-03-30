from pathlib import Path
import os



# === ASSISTANT CONFIG ===
ASSISTANT_TYPE = os.getenv("ASSISTANT_TYPE", "rag")


# === LLM CONFIG ===

CHAT_MODEL = "qwen2.5-vl-3b-instruct"
EMBEDDING_MODEL = "text-embedding-nomic-embed-text-v1.5"
BASE_URL = "http://localhost:1234/v1"
API_KEY = "lm-studio"
RAG_SCORE_THRESHOLD = 0.02


# === PATHS ===

PROJECT_ROOT = Path(__file__).resolve().parent.parent

LOCAL_BRAIN_DIR = PROJECT_ROOT / "local_brain"

DATA_DIR = LOCAL_BRAIN_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
EXTRACTED_DIR = DATA_DIR / "extracted"

OBSIDIAN_VAULT_DIR = LOCAL_BRAIN_DIR / "obsidian_vault"


DEV_FAST_MODE = True

DEFAULT_SUMMARY_LIMIT = 2000 if DEV_FAST_MODE else 4000
DEFAULT_CHUNK_SIZE = 400 if DEV_FAST_MODE else 500
DEFAULT_OVERLAP = 80 if DEV_FAST_MODE else 100
DEFAULT_TOP_K = 2 if DEV_FAST_MODE else 3
DEFAULT_RESPONSE_MODE = "short" if DEV_FAST_MODE else "detailed"

# === BUILDERS ===

def build_pdf_path(filename: str) -> Path:
    return INPUT_DIR / filename


def build_raw_text_path(filename: str) -> Path:
    stem = Path(filename).stem
    return EXTRACTED_DIR / f"{stem}_raw.txt"


def build_clean_text_path(filename: str) -> Path:
    stem = Path(filename).stem
    return EXTRACTED_DIR / f"{stem}_clean.txt"


def build_note_title(filename: str) -> str:
    return Path(filename).stem

def get_default_pipeline_params():
    return {
        "summary_limit": DEFAULT_SUMMARY_LIMIT,
        "chunk_size": DEFAULT_CHUNK_SIZE,
        "overlap": DEFAULT_OVERLAP,
        "top_k": DEFAULT_TOP_K,
    }

# === VECTOR STORE ===

VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "chroma")
CHROMA_DIR = DATA_DIR / "chroma"
CHROMA_COLLECTION = "documents"