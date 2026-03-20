from pathlib import Path
import os



# === ASSISTANT CONFIG ===
ASSISTANT_TYPE = os.getenv("ASSISTANT_TYPE", "dummy")


# === LLM CONFIG ===

CHAT_MODEL = "qwen2.5-vl-3b-instruct"
EMBEDDING_MODEL = "text-embedding-nomic-embed-text-v1.5"
BASE_URL = "http://localhost:1234/v1"
API_KEY = "lm-studio"


# === PATHS ===

PROJECT_ROOT = Path(__file__).resolve().parent.parent

LOCAL_BRAIN_DIR = PROJECT_ROOT / "local_brain"

DATA_DIR = LOCAL_BRAIN_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
EXTRACTED_DIR = DATA_DIR / "extracted"

OBSIDIAN_VAULT_DIR = LOCAL_BRAIN_DIR / "obsidian_vault"


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