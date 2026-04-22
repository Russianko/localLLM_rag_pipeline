from pathlib import Path
from uuid import uuid4
import shutil
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from api.schemas import (
    HealthResponse,
    ProcessRequest,
    ProcessJobAcceptedResponse,
    JobStatusResponse,
    AskRequest,
    AskResponse,
    DocumentInfo,
    DocumentDetail,
    DeleteDocumentResponse,
    UploadResponse,
    )
from app.services.file_service import save_upload_file
from app.pipeline_service import PipelineService
from app.assistants.factory import build_assistant, list_assistants
from app.config import ASSISTANT_TYPE
from fastapi import FastAPI, HTTPException, Request
from app.errors import (
    AppError,
    DocumentNotFoundError,
    DocumentNotProcessedError,
    InvalidRequestError,
)
from app.job_queue import enqueue_process_job
from app.job_status import get_job_status
from app.config import ASSISTANT_TYPE, INPUT_DIR, MAX_UPLOAD_SIZE_BYTES
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.config import get_default_pipeline_params
from api.schemas import AssistantsResponse
from app.assistants.router import select_assistant


app = FastAPI(
    title="Local AI Assistant",
    description=f"Active assistant: {ASSISTANT_TYPE}",
)
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

assistant = build_assistant(ASSISTANT_TYPE)
service = PipelineService(assistant=assistant)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health", response_model=HealthResponse)
def health():
    return service.health()

@app.get("/health/ready", response_model=HealthResponse)
def health_ready():
    return service.health()


@app.get("/documents", response_model=list[DocumentInfo])
def get_documents():
    return service.list_documents()


@app.post("/ask", response_model=AskResponse)
def ask_document(payload: AskRequest):
    selected_assistant = select_assistant(
        question=payload.question,
        filename=payload.filename,
        forced_assistant=payload.assistant_type,
    )

    if selected_assistant == ASSISTANT_TYPE:
        selected_service = service
    else:
        selected_service = PipelineService(
            assistant=build_assistant(selected_assistant)
        )

    result = selected_service.ask_document(
        filename=payload.filename,
        question=payload.question,
        top_k=payload.top_k,
        chunk_size=payload.chunk_size,
        overlap=payload.overlap,
        auto_process=payload.auto_process,
        response_mode=payload.response_mode,
    )

    result["selected_assistant"] = selected_assistant
    return result

@app.get("/assistants", response_model=AssistantsResponse)
def get_assistants():
    return {
        "assistants": list_assistants(),
        "default": "auto",
    }

@app.get("/documents/{doc_id}", response_model=DocumentDetail)
def get_document(doc_id: str):
    return service.get_document(doc_id)


@app.post("/process", status_code=202, response_model=ProcessJobAcceptedResponse)
def process_document(payload: ProcessRequest):
    return enqueue_process_job(
        filename=payload.filename,
        summary_limit=payload.summary_limit,
        chunk_size=payload.chunk_size,
        overlap=payload.overlap,
        force_rebuild=payload.force_rebuild,
    )


@app.get("/jobs/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str):
    job = get_job_status(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail=f"Job not found: {job_id}")

    return job


@app.delete("/documents/{doc_id}", response_model=DeleteDocumentResponse)
def delete_document(doc_id: str):
    return service.delete_document(doc_id)


@app.exception_handler(DocumentNotFoundError)
async def document_not_found_handler(request: Request, exc: DocumentNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(DocumentNotProcessedError)
async def document_not_processed_handler(request: Request, exc: DocumentNotProcessedError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(InvalidRequestError)
async def invalid_request_handler(request: Request, exc: InvalidRequestError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


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
    target_path = INPUT_DIR / filename
    if not target_path.exists():
        return filename

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    return f"{stem}_{uuid4().hex[:8]}{suffix}"


@app.post("/upload", response_model=UploadResponse, status_code=201)
def upload_pdf(file: UploadFile = File(...)):
    if file.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported content type: {file.content_type}. Only PDF is allowed.",
        )

    original_filename = file.filename or "uploaded.pdf"
    safe_filename = _sanitize_pdf_filename(original_filename)
    final_filename = _build_unique_filename(safe_filename)

    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = INPUT_DIR / final_filename

    size_bytes = 0

    try:
        with destination.open("wb") as buffer:
            while True:
                chunk = file.file.read(1024 * 1024)  # 1 MB
                if not chunk:
                    break

                size_bytes += len(chunk)

                if size_bytes > MAX_UPLOAD_SIZE_BYTES:
                    destination.unlink(missing_ok=True)
                    raise HTTPException(
                        status_code=413,
                        detail=f"File is too large. Max size is {MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)} MB.",
                    )

                buffer.write(chunk)

        if size_bytes == 0:
            destination.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        return {
            "filename": final_filename,
            "original_filename": original_filename,
            "content_type": file.content_type or "application/pdf",
            "size_bytes": size_bytes,
            "saved_to": str(destination.resolve()),
        }

    finally:
        file.file.close()

@app.post("/upload-and-process", status_code=202)
def upload_and_process(file: UploadFile = File(...)):
    upload_result = upload_pdf(file)

    filename = upload_result["filename"]
    defaults = get_default_pipeline_params()

    job = enqueue_process_job(
        filename=filename,
        summary_limit=defaults["summary_limit"],
        chunk_size=defaults["chunk_size"],
        overlap=defaults["overlap"],
        force_rebuild=False,
    )

    return {
        "filename": filename,
        "job": job,
    }