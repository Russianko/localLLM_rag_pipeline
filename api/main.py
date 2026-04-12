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
)
from app.pipeline_service import PipelineService
from app.assistants.factory import build_assistant
from app.config import ASSISTANT_TYPE
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.errors import (
    AppError,
    DocumentNotFoundError,
    DocumentNotProcessedError,
    InvalidRequestError,
)
from app.job_queue import enqueue_process_job
from app.job_status import get_job_status

app = FastAPI(
    title="Local AI Assistant",
    description=f"Active assistant: {ASSISTANT_TYPE}",
)
assistant = build_assistant(ASSISTANT_TYPE)
service = PipelineService(assistant=assistant)



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
    return service.ask_document(
        filename=payload.filename,
        question=payload.question,
        top_k=payload.top_k,
        chunk_size=payload.chunk_size,
        overlap=payload.overlap,
        auto_process=payload.auto_process,
        response_mode=payload.response_mode,
    )


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
