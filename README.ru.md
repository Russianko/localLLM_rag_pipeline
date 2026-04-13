🧠 Обзор

Local AI Station — это локальная AI-платформа для работы с документами:

обработка PDF
извлечение знаний (summary, key points, action items)
семантический поиск
ответы на вопросы (RAG)
сохранение в Obsidian

Система полностью работает локально через LM Studio.

🏗 Архитектура

LM Studio (модели)
        ↓
FastAPI (оркестрация)
        ↓
Redis (очередь)
        ↓
Worker (обработка)
        ↓
Chroma (векторное хранилище)

🔁 Pipeline
Обработка документа

PDF → очистка → summary → чанки → embeddings → сохранение

Ответ на вопрос
вопрос → embedding → поиск → LLM → ответ

⚙️ Стек
Python / FastAPI
LM Studio
Redis
Chroma
Sentence Transformers
Obsidian
📡 API
POST /process — обработка документа (async)
GET /jobs/{job_id} — статус
POST /ask — задать вопрос
GET /documents — список документов
🎯 Статус
система полностью работает
асинхронная обработка через Redis
RAG через Chroma
локальные LLM
🚀 Цель проекта

Показать:

архитектуру RAG
работу с локальными LLM
async backend
production-подход к AI системам