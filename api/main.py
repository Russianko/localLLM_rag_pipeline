from api.schemas import (
    HealthResponse, ProcessRequest, ProcessResponse, AskRequest,
    AskResponse, DocumentInfo, DocumentDetail, DeleteDocumentResponse
)
from app.pipeline_service import PipelineService
from fastapi import FastAPI, HTTPException
from app.assistants.factory import build_assistant
from app.config import ASSISTANT_TYPE


app = FastAPI(
    title="Local AI Assistant",
    description=f"Active assistant: {ASSISTANT_TYPE}",
)
assistant = build_assistant("rag")
service = PipelineService(assistant=assistant)



@app.get("/health", response_model=HealthResponse)
def health():
    return service.health()


@app.get("/documents", response_model=list[DocumentInfo])
def get_documents():
    return service.list_documents()


@app.post("/process", response_model=ProcessResponse)
def process_document(payload: ProcessRequest):
    try:
        return service.process_document(
            filename=payload.filename,
            summary_limit=payload.summary_limit,
            chunk_size=payload.chunk_size,
            overlap=payload.overlap,
            force_rebuild=payload.force_rebuild,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


@app.post("/ask", response_model=AskResponse)
def ask_document(payload: AskRequest):
    try:
        return service.ask_document(
            filename=payload.filename,
            question=payload.question,
            top_k=payload.top_k,
            chunk_size=payload.chunk_size,
            overlap=payload.overlap,
            auto_process=payload.auto_process,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


@app.get("/documents/{doc_id}", response_model=DocumentDetail)
def get_document(doc_id: str):
    try:
        return service.get_document(doc_id)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


@app.delete("/documents/{doc_id}", response_model=DeleteDocumentResponse)
def delete_document(doc_id: str):
    try:
        return service.delete_document(doc_id)
    except FileNotFoundError as     e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


