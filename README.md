# 🚀 Local AI Assistant Platform

Modular AI system for document understanding, semantic search and workflow automation.

Originally built as a legal document assistant, the system evolved into a multi-purpose AI platform with RAG pipelines, API access and external tool integrations (e.g. Figma plugin).

---

## 🧠 Overview

This project implements a full AI backend system capable of:

- processing and understanding documents
- answering questions using RAG (Retrieval-Augmented Generation)
- acting as an assistant that can control external tools (e.g. Figma plugin)
- integrating into real workflows via API

The system is designed not as a script, but as a **service-oriented AI backend**.

---

## ⚙️ Core Capabilities

### 📄 Document Intelligence
- PDF parsing and text extraction  
- smart chunking with overlap  
- semantic embeddings  

### 🔍 Semantic Search
- similarity-based retrieval  
- context-aware chunk selection  

### 🤖 RAG (Question Answering)
- LLM-based answer generation  
- answers grounded in retrieved context  
- source-aware responses  

### 🔌 API-first Architecture
- REST API for integration  
- document management  
- query endpoints  

### 🎨 AI + Design Workflow (Figma Integration)
- generation of structured payloads for Figma  
- assistant capable of controlling plugin actions  
- automation of design workflows  

---

## 🧩 Architecture
Document → Cleaning → Chunking → Embeddings → Vector Search → LLM → Answer

## Extended flow:
User → API → Assistant → RAG Pipeline → External Tool (Figma) → Result

---

## 🌐 API

### Health
GET /health
GET /health/ready
### Documents
GET /documents
GET /documents/{doc_id}
DELETE /documents/{doc_id}
### Processing
POST /process
### Query
POST /ask

- orchestrating RAG pipelines  
- generating structured outputs  
- interacting with external tools (plugin execution)  

This enables building **AI-driven workflows**, not just Q&A systems.

---

## ⚡ Tech Stack

- Python 3.10+
- FastAPI
- SentenceTransformers
- Vector search (cosine similarity / extendable to DB)
- Local / API-based LLM
- Modular service architecture

---

## 📂 Project Structure

app/
assistants/
services/
vectorstore/
pipeline_service.py
rag_answerer.py
retriever.py
embedder.py

localization/
(figma plugin integration logic)

---

## 🚀 Use Cases

- Legal document assistant  
- Knowledge base search  
- AI-powered internal tools  
- Design workflow automation (via Figma plugin)  
- Multi-agent AI systems  

---

## 🧠 Engineering Highlights

- Built full RAG pipeline from scratch  
- Designed modular service architecture  
- Implemented API-first system for integration  
- Extended system to support tool usage (plugin control)  
- Transition from single-purpose assistant → platform  

---

## 🔮 Roadmap

- Hybrid search (BM25 + embeddings)  
- vector DB (FAISS / Qdrant)  
- retrieval reranking  
- evaluation metrics (latency, recall)  
- multi-agent orchestration  
- production deployment  

---

## 👨‍💻 Author

Backend developer building real-world systems at the intersection of:

- APIs  
- data processing  
- AI (RAG, LLM integration)  
- automation  

---
