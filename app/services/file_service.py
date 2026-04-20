from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.config import INPUT_DIR


def _sanitize_pdf_filename(filename: str) -> str:
    if not filename:
        raise HTTPException(status_code=400, detail="Filename is empty.")

    safe_name = Path(filename).name.strip()

    if not safe_name:
        raise HTTPException(status_code=400, detail="Filename is invalid.")

    if not safe_name.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    return safe_name


def _build_unique_filename(filename: str) -> str:
    target = INPUT_DIR / filename
    if not target.exists():
        return filename

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    return f"{stem}_{uuid4().hex[:8]}{suffix}"


def save_upload_file(file: UploadFile) -> dict:
    original_filename = file.filename or "uploaded.pdf"
    safe_filename = _sanitize_pdf_filename(original_filename)
    final_filename = _build_unique_filename(safe_filename)

    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = INPUT_DIR / final_filename

    with destination.open("wb") as buffer:
        buffer.write(file.file.read())

    file.file.close()

    return {
        "filename": final_filename,
        "original_filename": original_filename,
        "content_type": file.content_type or "application/pdf",
        "saved_to": str(destination.resolve()),
    }