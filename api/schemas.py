from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Any

from app.config import get_default_pipeline_params, DEFAULT_RESPONSE_MODE

defaults = get_default_pipeline_params()


class ProcessRequest(BaseModel):
    filename: str = Field(..., description="PDF filename from local_brain/data/input")
    summary_limit: int = Field(default=defaults["summary_limit"], ge=500, le=50000)
    chunk_size: int = Field(default=defaults["chunk_size"], ge=100, le=5000)
    overlap: int = Field(default=defaults["overlap"], ge=0, le=1000)
    force_rebuild: bool = False


class ProcessJobAcceptedResponse(BaseModel):
    job_id: str
    status: Literal["queued"]
    queue: str


class AskRequest(BaseModel):
    filename: str
    question: str = Field(..., min_length=2)
    top_k: int = Field(default=defaults["top_k"], ge=1, le=10)
    chunk_size: int = Field(default=defaults["chunk_size"], ge=100, le=5000)
    overlap: int = Field(default=defaults["overlap"], ge=0, le=1000)
    auto_process: bool = True
    response_mode: str = Field(default=DEFAULT_RESPONSE_MODE)
    assistant_type: str = Field(default="auto")


class ChunkResult(BaseModel):
    chunk_id: int
    text: str
    score: float


class AskResponse(BaseModel):
    source_document: str
    question: str
    answer: str
    rag_note_path: str
    top_chunks: List[ChunkResult]
    selected_assistant: str


class DocumentInfo(BaseModel):
    id: str
    status: str
    has_clean_text: bool
    has_summary: bool
    has_chunks: bool
    has_embeddings: bool
    is_processed: bool
    has_error: bool


class DocumentDetail(BaseModel):
    id: str
    summary: str | None
    chunks_count: int
    has_clean_text: bool
    has_summary: bool
    has_chunks: bool
    has_embeddings: bool
    is_processed: bool
    has_error: bool


class DeleteDocumentResponse(BaseModel):
    id: str
    deleted: bool


class ErrorResponse(BaseModel):
    detail: str


class DefaultsInfo(BaseModel):
    summary_limit: int
    chunk_size: int
    overlap: int
    top_k: int
    response_mode: str


class StorageInfo(BaseModel):
    vault_dir: str
    vault_dir_exists: bool
    processed_data_dir: str
    processed_data_dir_exists: bool
    processed_documents_count: int


class RuntimeInfo(BaseModel):
    embedder_loaded: bool
    rag_loaded: bool


class LLMConnectionInfo(BaseModel):
    reachable: bool
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    service: str
    assistant_type: str
    dev_fast_mode: bool
    base_url: str
    chat_model: str
    embedding_model: str
    defaults: DefaultsInfo
    storage: StorageInfo
    runtime: RuntimeInfo
    llm_connection: LLMConnectionInfo


class JobStatusResponse(BaseModel):
    job_id: str
    status: Literal["queued", "running", "done", "failed"]
    created_at: str
    updated_at: str
    payload: dict[str, Any]
    result: Optional[dict[str, Any]] = None
    error: Optional[str] = None


class UploadResponse(BaseModel):
    filename: str
    original_filename: str
    content_type: str
    size_bytes: int
    saved_to: str

class AssistantInfo(BaseModel):
    type: str
    name: str
    description: str

class AssistantsResponse(BaseModel):
    assistants: List[AssistantInfo]
    default: str
