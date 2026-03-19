Local RAG Pipeline

A local document analysis system with semantic search and RAG-based question answering.

This project implements a full pipeline for processing documents, extracting meaning, and answering questions based on their content using Retrieval-Augmented Generation (RAG).

Features

PDF text extraction

Smart text chunking with overlap

Embeddings using SentenceTransformers

Semantic search (cosine similarity)

RAG (Retrieval-Augmented Generation)

Context-aware answers with source chunks

Architecture
Document (PDF)
      ↓
Text extraction
      ↓
Chunking
      ↓
Embeddings
      ↓
Semantic retrieval
      ↓
LLM (RAG)
      ↓
Answer + sources

Tech Stack

Python 3.10+

SentenceTransformers (paraphrase-multilingual-MiniLM-L12-v2)

Local LLM (via API / client)

NumPy (for similarity calculations)

Project Structure
local-rag-pipeline/
│
├── app/
│   ├── chunker.py
│   ├── embedder.py
│   ├── retriever.py
│   ├── rag_answerer.py
│   ├── llm_client.py
│   └── config.py
│
├── data/
│   └── extracted/
│
├── run_embeddings.py
├── run_semantic_search.py
├── run_rag_answer.py
│
└── README.md
Setup
git clone https://github.com/your-username/local-rag-pipeline.git
cd local-rag-pipeline

python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt

Usage
1. Generate embeddings
python run_embeddings.py
2. Run semantic search
python run_semantic_search.py
3. Ask questions (RAG)
python run_rag_answer.py

Example:

QUESTION:
Где в документе говорится о сокращении штата специалистов?

ANSWER:

How it works

Document is split into chunks

Each chunk is converted into vector embeddings

User question is also embedded

System finds most relevant chunks

LLM generates answer based only on retrieved context

Current Status

Integration with knowledge base (PARA / notes)

Future Improvements

Save embeddings to disk (avoid recomputation)

Add FAISS / vector DB

Improve answer quality (prompt tuning)

Telegram / web interface

Integration with personal knowledge system

