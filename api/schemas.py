from pydantic import BaseModel, Field
from typing import List


class HealthResponse(BaseModel):
    status: str
    base_url: str
    chat_model: str
    embedding_model: str
    vault_dir: str
    processed_data_dir: str
    assistant_type: str
    embedder_loaded: bool
    rag_loaded: bool


class ProcessRequest(BaseModel):
    filename: str = Field(..., description="PDF filename from local_brain/data/input")
    summary_limit: int = Field(default=4000, ge=500, le=50000)
    chunk_size: int = Field(default=500, ge=100, le=5000)
    overlap: int = Field(default=100, ge=0, le=1000)
    force_rebuild: bool = False


class ProcessResponse(BaseModel):
    status: str
    source_document: str
    summary: str
    key_points: List[str]
    action_items: List[str]
    document_note_path: str
    raw_text_path: str
    clean_text_path: str
    summary_path: str
    chunks_path: str
    embeddings_path: str
    chunks_count: int


class AskRequest(BaseModel):
    filename: str
    question: str
    top_k: int = 3
    chunk_size: int = 500
    overlap: int = 100
    auto_process: bool = True
    response_mode: str = Field(default="detailed")


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


class DocumentInfo(BaseModel):
    id: str
    has_embeddings: bool
    has_chunks: bool
    has_summary: bool


class DocumentDetail(BaseModel):
    id: str
    summary: str | None
    chunks_count: int
    has_embeddings: bool
    has_summary: bool
    has_chunks: bool


class DeleteDocumentResponse(BaseModel):
    id: str
    deleted: bool