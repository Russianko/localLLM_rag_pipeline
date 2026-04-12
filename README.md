# 🧠 Local AI Station (RAG Platform)

Self-hosted AI system for document understanding and question answering using local LLMs.

---

## 🚀 Overview

Local AI Station is a **production-style RAG (Retrieval-Augmented Generation) platform** that allows you to:

- process PDF documents
- extract structured knowledge (summary, key points, actions)
- perform semantic search
- ask questions using local LLMs
- store knowledge in Obsidian-compatible format

The system runs **fully locally** using LM Studio — no external APIs required.

---

## 🏗 Architecture

The system is designed with **clear separation of concerns**:

LM Studio (Model Runtime)
↓
FastAPI (Orchestration Layer)
↓
Redis (Queue & Job State)
↓
Worker (Async Processing)
↓
Chroma (Vector Storage)



### Key Principles

- Models are NOT embedded into application logic
- Orchestration is separated from inference
- Async ingestion via queue
- Persistent vector retrieval
- Ready for containerization and Kubernetes

---

## 🔁 Pipelines

### 📥 Document Processing (Async)

POST /process
→ Redis queue
→ Worker
→ PDF → Clean → Summary → Chunk → Embeddings
→ Chroma + Storage + Obsidian


---

### ❓ Question Answering (RAG)

POST /ask
→ Embed query
→ Vector search (Chroma)
→ Top-K chunks
→ LLM answer


---

## ⚙️ Tech Stack

- **Python / FastAPI** — API & orchestration
- **LM Studio** — local LLM runtime
- **Redis** — queue & job coordination
- **Chroma** — vector database
- **Sentence Transformers** — embeddings
- **Obsidian** — knowledge storage

---

## 📡 API

### Health

GET /health
GET /health/ready


### Documents

GET /documents
GET /documents/{doc_id}
DELETE /documents/{doc_id}


### Processing

POST /process
GET /jobs/{job_id}


### RAG

POST /ask


---

## 🧪 Example Flow

1. Upload document:

```bash
POST /process

2. Check status:

GET /jobs/{job_id}

3. Ask question:

POST /ask

🐳 Docker & Deployment

The project is prepared for:

Docker (local setup)
Kubernetes / k3s (future scaling)

Included:

Dockerfile
rag-deployment.yaml
rag-service.yaml
📁 Project Structure

/api        → FastAPI endpoints
/app        → core logic (pipelines, assistants)
/config     → configs & mappings
/infra      → (recommended for k8s/docker)
/docs       → documentation

🎯 Current Status

✅ End-to-end working
✅ Async ingestion via Redis
✅ Persistent vector search
✅ Local LLM integration
⚠️ Docker/K8s setup in progress

🔮 Roadmap
Docker Compose setup
Kubernetes deployment
Embedding optimization
UI / dashboard
Multi-assistant support
💡 Why This Project

This project demonstrates:

RAG architecture
async backend design
queue-based processing
LLM integration
production-oriented system design