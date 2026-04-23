# 🧠 Local AI Station

Self-hosted multi-agent AI platform for document understanding, local chat, and voice-to-text interaction using local LLMs.  
Локальная мультиагентная AI-платформа для анализа документов, локального чата и voice-to-text взаимодействия с использованием локальных LLM.

---

## 🚀 Overview / Обзор

**Local AI Station** is a local AI platform that turns documents into structured knowledge and allows users to interact with the system through a unified chat interface.

**Local AI Station** — это локальная AI-платформа, которая превращает документы в структурированное знание и позволяет работать с системой через единый чат-интерфейс.

The system supports / Система поддерживает:

- PDF document processing / обработку PDF-документов
- knowledge extraction (summary, key points, actions) / извлечение знаний
- semantic search / семантический поиск
- RAG-based question answering / ответы на вопросы по документам
- general-purpose local chat / обычный локальный chat-режим
- multi-agent architecture / мультиагентную архитектуру
- voice input → text response / голосовой ввод → текстовый ответ
- Obsidian-compatible storage / хранение в формате Obsidian

Everything runs locally via **LM Studio**, without external LLM APIs.  
Всё работает локально через **LM Studio**, без внешних LLM API.

---

## 🧠 Core Idea / Основная идея

This is not a “single universal AI”, but a system of specialized agents with a shared orchestration layer.

Это не “один универсальный AI”, а система специализированных агентов с общим orchestration-слоем.

Current agents / Текущие агенты:

- `rag` — document-based answering / ответы по документам
- `chat` — general local assistant / универсальный локальный ассистент
- `dummy` — testing assistant / тестовый ассистент
- `auto` — automatic routing / автоматический выбор агента

Planned / Планируется:

- `analyst` — structured document intelligence / аналитический агент
- memory-aware assistants / ассистенты с памятью
- tool-enabled agents / агенты с инструментами

---

## 🏗 Architecture / Архитектура

```text
LM Studio (LLM Runtime)
        ↓
FastAPI (API + Router)
        ↓
Redis (Queue / Job State)
        ↓
Worker (Async Processing)
        ↓
Assistants Layer
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
orchestration отделён от inference
async ingestion via queue
асинхронная обработка через очередь
persistent retrieval
постоянное хранение и поиск
multi-agent routing
маршрутизация между агентами
explainable answers
объяснимые ответы через source chunks
unified assistant interface
единый интерфейс ассистентов

🤖 Multi-Agent System / Мультиагентная система

Supported assistants / Доступные ассистенты:

rag — document Q&A with retrieval / ответы по документам через retrieval
chat — general-purpose local chat / обычный чат без документов
dummy — testing and routing validation / тестирование UI и маршрутизации
auto — router-based automatic selection / авто-выбор агента

Routing logic / Логика роутинга:

forced assistant → override
if filename is present → rag
if question is clearly document-related → rag
otherwise → chat

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
❓ Question Answering / Ответы на вопросы
POST /ask
    ↓
Router
    ↓
Selected assistant
    ↓
RAG retrieval or direct LLM chat
    ↓
Answer + metadata

🎤 Voice Input / Голосовой ввод

POST /voice
    ↓
ASR (faster-whisper)
    ↓
Transcript
    ↓
Router
    ↓
Selected assistant
    ↓
Text answer

If ASR is temporarily unavailable, the pipeline currently supports fallback behavior for continued UI and API testing.
Если ASR временно недоступен, сейчас используется fallback-поведение, чтобы не ломать UI и API.

⚙️ Tech Stack / Технологии

Python / FastAPI — API и orchestration
LM Studio — локальные LLM
Redis — очередь и job state
Worker — async processing
Chroma — vector DB
Sentence Transformers — embeddings
faster-whisper — ASR / speech-to-text
Obsidian — local knowledge storage
HTML / CSS / JS — web UI

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
Upload / Processing
POST /upload
POST /upload-and-process
POST /process
GET /jobs/{job_id}
Interaction
POST /ask
POST /voice

🧪 Example Flow / Пример

Text chat / Текстовый чат
User question
    ↓
POST /ask
    ↓
Router selects assistant
    ↓
Assistant returns answer
Document workflow / Работа с документом
Upload PDF
    ↓
POST /upload-and-process
    ↓
Worker processes file
    ↓
Document becomes available for RAG queries
Voice workflow / Голосовой сценарий
Press microphone button
    ↓
Record short audio
    ↓
POST /voice
    ↓
Transcript appears as user message
    ↓
Assistant returns text response

🖥 UI

The web interface includes / Web-интерфейс включает:

chat window / чат
assistant selection / выбор ассистента
file upload / загрузку PDF
processed document list / список документов
source chunk panel / просмотр использованных чанков
voice button / кнопку голосового ввода

🐳 Docker

The system is containerized and can be launched locally.

Система контейнеризирована и может запускаться локально.

docker compose build
docker compose up -d

Includes / Включает:

API
Worker
Redis

☸️ Kubernetes

The repository includes Kubernetes manifests for deployment experiments.

Репозиторий включает Kubernetes-манифесты для дальнейших deployment-экспериментов.

Current manifests / Текущие манифесты:

namespace.yaml
redis.yaml
storage.yaml
api.yaml
worker.yaml

📁 Project Structure

/api          → FastAPI endpoints and schemas
/app          → assistants, services, pipelines, storage, vector retrieval
/web          → frontend UI
/k8s          → Kubernetes manifests
/local_brain  → local data + Obsidian vault

🎯 Current Status / Текущий статус

✅ end-to-end document pipeline
✅ async ingestion via Redis + worker
✅ vector retrieval with Chroma
✅ local LLM integration via LM Studio
✅ multi-agent architecture
✅ router with auto mode
✅ general chat assistant
✅ voice endpoint and voice UI
✅ Dockerized local deployment
✅ Kubernetes manifests included
⚠️ ASR still requires environment stabilization for full real-time usage

🔮 Roadmap / Дорожная карта

Analyst Assistant
conversational memory
smarter routing (LLM / hybrid)
stable ASR runtime
tool layer
retrieval improvements
model specialization by assistant type
better voice UX
k8s runtime validation

💡 Why This Project / Зачем этот проект

This project demonstrates / Этот проект демонстрирует:

production-style RAG architecture
async backend design
queue-based processing
multi-agent orchestration
local LLM integration
voice-to-text interaction
explainable answers
deployment-oriented engineering

🧭 Philosophy / Философия

Build not a universal AI blob, but a system where each agent does one job well.

Не делать один “универсальный AI-комбайн”, а строить систему, где каждый агент делает одну задачу хорошо.