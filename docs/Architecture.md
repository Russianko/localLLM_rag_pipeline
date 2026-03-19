Локальная AI-система управления знаниями

1. Общая идея системы

Система представляет собой локальный RAG-ассистент для работы с документами.

Основная задача системы:

превращать документы в структурированное знание и позволять задавать вопросы по этим знаниям.

Система работает полностью локально через LM Studio, что обеспечивает:

контроль над данными

возможность работы без облака

воспроизводимость проекта для портфолио.

Базовый контекст проекта описан в PROJECT_CONTEXT.md.

2. Архитектурная схема

Общая схема обработки данных:

PDF
 ↓
Text extraction
 ↓
Text cleaning
 ↓
Chunking
 ↓
Embeddings
 ↓
Vector storage
 ↓
Retrieval
 ↓
LLM reasoning
 ↓
Answer / Summary
 ↓
Markdown note
3. Основные компоненты системы

Система состоит из 6 ключевых модулей.

3.1 Document Ingestion

Модуль отвечает за загрузку документов.

Файл:

pdf_reader.py

Задачи:

открыть PDF

извлечь текст

очистить текст

сохранить raw текст

Пайплайн:

PDF → raw text

На этом этапе LLM не используется.

3.2 Text Chunking

Модуль разрезает текст на логические части.

Файл:

chunker.py

Почему это важно:

LLM и поисковые системы плохо работают с длинными текстами.

Поэтому текст делится на chunk'и.

Пример:

Документ: 20 страниц

→ chunk 1
→ chunk 2
→ chunk 3
→ chunk 4
...

Типичный размер:

500 – 1000 токенов
3.3 Embeddings

Embeddings переводят текст в векторное представление смысла.

Файл:

embedder.py

Пример:

Текст:
"Финансовые риски стартапа"

→ embedding vector

[0.12, -0.44, 0.87, ...]

Этот вектор позволяет искать схожие тексты по смыслу.

3.4 Vector Storage

Хранилище embeddings.

Варианты:

FAISS
или
Chroma

Файл:

vector_store.py

Там хранится:

chunk
embedding
source_document
page
metadata
3.5 Retrieval

Retrieval ищет релевантные куски текста.

Файл:

retriever.py

Процесс:

user question
 ↓
embedding(question)
 ↓
vector search
 ↓
top_k chunks

Эти chunk'и передаются в LLM.

3.6 LLM Reasoning

Модель анализирует найденные фрагменты.

Файл:

llm_client.py

Используется локальная модель через LM Studio.

Модель выполняет:

summary

извлечение тезисов

ответы на вопросы

3.7 Note Generation

Формирование markdown заметки.

Файл:

note_writer.py

Создаётся структура:

Title
Source
Date

Summary

Key points

Action items

Заметка сохраняется в Obsidian-совместимом формате.

4. Потоки данных системы

В системе есть 2 основных pipeline.

4.1 Document Processing Pipeline

Обработка нового документа.

PDF
 ↓
extract text
 ↓
chunk text
 ↓
generate summary
 ↓
extract key points
 ↓
extract action items
 ↓
save markdown note
 ↓
store chunks + embeddings
4.2 Question Answering Pipeline

Ответ на вопрос пользователя.

User question
 ↓
embedding(question)
 ↓
vector search
 ↓
retrieve chunks
 ↓
LLM prompt
 ↓
generated answer
 ↓
show sources
5. Prompt Architecture

Все инструкции модели хранятся отдельно.

Файл:

prompts.py

Это позволит:

менять поведение модели

тестировать разные шаблоны

избегать “магии в коде”.

6. Структура проекта

Расширенная структура:

local_brain/

app/
 ├── config.py
 ├── llm_client.py
 ├── pdf_reader.py
 ├── chunker.py
 ├── embedder.py
 ├── vector_store.py
 ├── retriever.py
 ├── summarizer.py
 ├── note_writer.py
 └── prompts.py

data/
 ├── input/
 ├── extracted/
 ├── chunks/
 ├── embeddings/
 └── notes/

main.py
requirements.txt
PROJECT_CONTEXT.md
ARCHITECTURE.md
README.md
7. Типы ассистентов системы

В будущем система будет состоять из нескольких ассистентов.

7.1 Document Processor

Обрабатывает документы.

Функции:

extract text
summary
key points
action items
note generation
7.2 Knowledge Navigator

Отвечает на вопросы.

Функции:

semantic search
RAG answering
source attribution
8. Интерфейс

В первой версии используется CLI интерфейс.

Команды:

python main.py ingest file.pdf
python main.py summarize file.pdf
python main.py ask "вопрос"

Позже возможны:

GUI (PyQt)
Web UI
Telegram bot
9. Расширяемость системы

Система проектируется так, чтобы легко добавить:

MCP серверы
filesystem
knowledge base
web research
внешние источники
RSS
web scraping
APIs
агенты
research agent
summarization agent
task extraction agent
10. Принципы разработки

Основные правила проекта:

1. Простота

Сначала рабочая версия
потом усложнение.

2. Модульность

Каждый компонент отдельный файл.

3. Прозрачность

Каждый шаг pipeline должен быть понятен.

4. Локальность

Проект должен работать без облака.

11. Ключевые знания проекта

Этот проект демонстрирует:

RAG architecture

local LLM usage

vector search

embeddings

document processing

AI assisted knowledge management

Это делает его сильным портфолио-проектом.

12. Следующий шаг разработки

Следующий этап:

интеграция Python и LM Studio

Цель:

создать модуль

llm_client.py

который умеет:

отправлять prompt

получать ответ

работать через локальный API.