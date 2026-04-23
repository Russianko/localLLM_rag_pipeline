from pathlib import Path
import os


def get_env(name: str, default=None):
    return os.getenv(name, default)

MAX_UPLOAD_SIZE_MB = int(get_env("MAX_UPLOAD_SIZE_MB", "50"))
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024

# === REDIS CONFIG ===
REDIS_HOST = get_env("REDIS_HOST", "localhost")
REDIS_PORT = int(get_env("REDIS_PORT", "6379"))
REDIS_DB = int(get_env("REDIS_DB", "0"))
REDIS_QUEUE_PROCESS = get_env("REDIS_QUEUE_PROCESS", "jobs:process")
REDIS_JOB_TTL_SECONDS = int(get_env("REDIS_JOB_TTL_SECONDS", "86400"))

# === ENV MODE ===
ENV = get_env("ENV", "dev")  # dev | docker | k8s


# === ASSISTANT ===
ASSISTANT_TYPE = get_env("ASSISTANT_TYPE", "rag")


# === LLM CONFIG ===
CHAT_MODEL = get_env("CHAT_MODEL", "qwen2.5-vl-3b-instruct")
EMBEDDING_MODEL = get_env("EMBEDDING_MODEL", "nomic-ai/nomic-embed-text-v1.5")

LM_STUDIO_BASE_URL = get_env("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
LM_STUDIO_API_KEY = get_env("LM_STUDIO_API_KEY", "lm-studio")

RAG_SCORE_THRESHOLD = float(get_env("RAG_SCORE_THRESHOLD", "0.45"))


# === PATHS ===

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = Path(get_env("DATA_DIR", PROJECT_ROOT / "local_brain/data"))
INPUT_DIR = DATA_DIR / "input"
EXTRACTED_DIR = DATA_DIR / "extracted"

OBSIDIAN_VAULT_DIR = Path(
    get_env("OBSIDIAN_VAULT_DIR", PROJECT_ROOT / "local_brain/obsidian_vault")
)


# === MODES ===

DEV_FAST_MODE = get_env("DEV_FAST_MODE", "true").lower() == "true"

DEFAULT_SUMMARY_LIMIT = 2000 if DEV_FAST_MODE else 4000
DEFAULT_CHUNK_SIZE = 400 if DEV_FAST_MODE else 500
DEFAULT_OVERLAP = 80 if DEV_FAST_MODE else 100
DEFAULT_TOP_K = 2 if DEV_FAST_MODE else 3
DEFAULT_RESPONSE_MODE = "short" if DEV_FAST_MODE else "detailed"


# === HELPERS ===

def build_pdf_path(filename: str) -> Path:
    return INPUT_DIR / filename


def build_raw_text_path(filename: str) -> Path:
    return EXTRACTED_DIR / f"{Path(filename).stem}_raw.txt"


def build_clean_text_path(filename: str) -> Path:
    return EXTRACTED_DIR / f"{Path(filename).stem}_clean.txt"


def build_note_title(filename: str) -> str:
    return Path(filename).stem


def get_default_pipeline_params():
    return {
        "summary_limit": DEFAULT_SUMMARY_LIMIT,
        "chunk_size": DEFAULT_CHUNK_SIZE,
        "overlap": DEFAULT_OVERLAP,
        "top_k": DEFAULT_TOP_K,
    }


# === ASR CONFIG ===
ASR_MODEL = get_env("ASR_MODEL", "small")
ASR_DEVICE = get_env("ASR_DEVICE", "cuda")   # cuda | cpu
ASR_COMPUTE_TYPE = get_env("ASR_COMPUTE_TYPE", "int8")
ASR_LANGUAGE = get_env("ASR_LANGUAGE", "ru")


# === VECTOR STORE ===

VECTOR_DB_TYPE = get_env("VECTOR_DB_TYPE", "chroma")
CHROMA_DIR = DATA_DIR / "chroma"
CHROMA_COLLECTION = get_env("CHROMA_COLLECTION", "documents_nomic_768")