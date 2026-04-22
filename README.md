🧠 Local AI Station

Self-hosted multi-agent AI platform for document understanding and question answering using local LLMs.
Локальная мультиагентная AI-платформа для анализа документов и ответов на вопросы с использованием локальных LLM.

🚀 Overview / Обзор

Local AI Station is a local AI platform that turns documents into structured knowledge and allows users to work with them through a unified chat interface.
Local AI Station — это локальная AI-платформа, которая превращает документы в структурированное знание и позволяет работать с ними через единый чат-интерфейс.

The system supports / Система поддерживает:

PDF document processing / обработку PDF-документов
knowledge extraction (summary, key points, actions) / извлечение знаний
semantic search / семантический поиск
question answering (RAG) / ответы на вопросы
multi-agent architecture / мультиагентную архитектуру
Obsidian-compatible storage / хранение в формате Obsidian

Everything runs locally via LM Studio, without external APIs.
Всё работает полностью локально через LM Studio, без внешних API.

🧠 Core Idea / Основная идея

This is not a “single universal AI”, but a system of agents with clear responsibilities.
Это не “один универсальный AI”, а система агентов с четкими ролями.

Current agents / Текущие агенты:

rag — document-based answering / ответы по документам
dummy — testing agent / тестовый агент
auto — automatic routing / автоматический выбор

Planned / Планируется:

analyst — structured document intelligence / аналитический агент

🏗 Architecture / Архитектура
LM Studio (LLM Runtime)
        ↓
FastAPI (API + Router)
        ↓
Redis (Queue / Job State)
        ↓
Worker (Async Processing)
        ↓
Document / Query Pipelines
        ↓
Chroma (Vector Store)
        ↓
Obsidian Vault
Architectural Principles / Принципы
models are not embedded into application logic
модели не зашиты в код
orchestration is separated from inference
разделение orchestration и inference
async ingestion via queue
асинхронная обработка через очередь
persistent retrieval
постоянное хранение и поиск
multi-agent routing
маршрутизация между агентами
explainable answers
объяснимые ответы через chunks

🤖 Multi-Agent System / Мультиагентная система

Supported assistants / Доступные ассистенты:

rag — RAG ответы
dummy — тестовый
auto — авто-режим

Router:

select_assistant(question, filename, forced)

Logic / Логика:

forced → override
filename → rag
otherwise → fallback

🔁 Pipelines / Пайплайны

📥 Document Processing / Обработка документов
POST /process
    ↓
Redis queue
    ↓
Worker
    ↓
PDF → Clean → Summary → Chunk → Embeddings
    ↓
Chroma + Storage + Obsidian

❓ Question Answering (RAG) / Ответы на вопросы
POST /ask
    ↓
Router
    ↓
Embed query
    ↓
Vector search
    ↓
Top-K chunks
    ↓
LLM answer

Response includes / Ответ содержит:

answer
selected_assistant
top_chunks

⚙️ Tech Stack / Технологии
Python / FastAPI — API и orchestration
LM Studio — локальные LLM
Redis — очередь
Worker — async обработка
Chroma — vector DB
Sentence Transformers — embeddings
Obsidian — knowledge storage
JS UI — интерфейс

📡 API
Health
GET /health
GET /health/ready
Assistants
GET /assistants
Documents
GET /documents
GET /documents/{doc_id}
DELETE /documents/{doc_id}
Processing
POST /process
GET /jobs/{job_id}
RAG
POST /ask

🧪 Example Flow / Пример
Upload document / Загрузка:
POST /upload-and-process
Check status / Проверка:
GET /jobs/{job_id}
Ask question / Вопрос:
POST /ask

🖥 UI

Includes / Включает:

chat
assistant selection
file upload
chunk sources

🐳 Docker

The system runs fully in containers.
Система полностью запускается в контейнерах.

docker compose build
docker compose up -d

Includes:

API
Worker
Redis

☸️ Kubernetes

The project includes ready-to-use manifests:

namespace.yaml
redis.yaml
storage.yaml
api.yaml
worker.yaml

Готово для деплоя в k8s / k3s.

📁 Project Structure
/api          → FastAPI
/app          → core logic
/web          → UI
/k8s          → manifests
/local_brain  → data + vault

🎯 Current Status
end-to-end pipeline
async ingestion
vector search
local LLM
multi-agent system
router
UI
Docker
k8s manifests

🔮 Roadmap
Analyst Assistant
smarter routing
memory
tools layer
retrieval improvements
k8s runtime
model specialization

💡 Why This Project

Demonstrates / Показывает:

RAG architecture
async backend
event-driven design
multi-agent systems
local LLM integration
production-style engineering

🧭 Philosophy

Build not a universal AI, but a system where each agent does one job well.
Не делать универсальный AI, а строить систему специализированных агентов.
