DEVELOPMENT ROADMAP

Локальная AI-система управления знаниями

Связан с документами:

PROJECT_CONTEXT.md

ARCHITECTURE.md

0. Общая стратегия разработки

Проект строится слоями, от простого к сложному.

Стратегия:

foundation
↓
document processing
↓
knowledge extraction
↓
RAG search
↓
assistant layer

Главный принцип:

сначала сделать работающий pipeline
потом улучшать интеллект системы.

ЭТАП 1

Подготовка среды разработки

Цель

Создать минимальную инфраструктуру проекта.

Результат

Python может отправлять запросы в локальную LLM.

1.1 Создание проекта

Создать папку проекта:

local_brain/

Структура:

local_brain/
│
├── app/
├── data/
│   ├── input/
│   ├── extracted/
│   └── notes/
│
├── PROJECT_CONTEXT.md
├── ARCHITECTURE.md
├── DEVELOPMENT_ROADMAP.md
1.2 Python окружение

Создать виртуальное окружение:

python -m venv venv

Активировать:

Windows

venv\Scripts\activate
1.3 Базовые зависимости

Создать файл

requirements.txt

Содержимое:

openai
pymupdf
python-dotenv

Установка:

pip install -r requirements.txt
1.4 LM Studio API

В LM Studio включить:

Start Local Server

Обычно сервер работает:

http://localhost:1234
1.5 Первый тест модели

Создать файл:

app/llm_client.py

Он должен:

отправить prompt

получить ответ

вывести ответ в консоль

Успех этапа

Если команда:

python test_llm.py

возвращает ответ модели — этап завершён.

ЭТАП 2

Document Ingestion

Цель

Научить систему читать PDF.

2.1 Модуль чтения PDF

Создать файл:

app/pdf_reader.py

Функция:

extract_text_from_pdf()

Задачи:

открыть PDF

извлечь текст

вернуть строку

2.2 Сохранение текста

После извлечения:

PDF
↓
raw text
↓
data/extracted/

Формат:

document_name.txt
Успех этапа

Команда:

python main.py extract file.pdf

создаёт текстовый файл.

ЭТАП 3

AI Summary Pipeline

Цель

Научить систему извлекать знания.

3.1 Prompt template

Создать файл:

app/prompts.py

Шаблон:

SUMMARY_PROMPT
KEYPOINTS_PROMPT
ACTION_ITEMS_PROMPT
3.2 Модуль суммаризации

Создать файл:

app/summarizer.py

Функции:

generate_summary()
extract_key_points()
extract_action_items()
Pipeline
raw text
↓
LLM
↓
summary
key points
action items
Успех этапа

Команда:

python main.py summarize file.pdf

выводит результат в консоль.

ЭТАП 4

Генерация AI-заметок

Цель

Создавать Obsidian-совместимые заметки.

4.1 Модуль записи заметок

Создать файл:

app/note_writer.py
Структура заметки
# Title

Source:
Date:

## Summary

...

## Key Points

...

## Action Items

...
Путь сохранения
data/notes/
Успех этапа

После обработки документа появляется

data/notes/document.md
ЭТАП 5

Chunking

Цель

Разбить текст на смысловые части.

Модуль

Создать файл:

app/chunker.py
Логика
text
↓
split into chunks
↓
500–1000 tokens
Результат
chunks.json
ЭТАП 6

Embeddings

Цель

Создать векторное представление текста.

Модуль
app/embedder.py
Pipeline
chunk
↓
embedding
↓
vector
Хранилище
FAISS
или
Chroma
ЭТАП 7

Semantic Search

Цель

Поиск по смыслу.

Модуль
app/retriever.py
Pipeline
question
↓
embedding
↓
vector search
↓
top chunks
ЭТАП 8

RAG Question Answering

Цель

Ответы на вопросы по документу.

Pipeline
question
↓
retrieve chunks
↓
LLM prompt
↓
answer
Ответ должен содержать

ответ

источник текста

chunk

ЭТАП 9

CLI интерфейс

Цель

Сделать систему удобной.

Команды
python main.py ingest file.pdf
python main.py summarize file.pdf
python main.py ask "вопрос"
ЭТАП 10

Knowledge Navigator

Цель

Создать полноценного ассистента.

Он умеет:

анализировать документы
искать информацию
отвечать на вопросы
объяснять источник ответа
ЭТАП 11

Оптимизация системы

Будет добавлено:

кеширование

более быстрые embeddings

улучшенные prompt templates

ЭТАП 12

Расширение системы

После MVP можно добавить:

MCP серверы
filesystem
knowledge base
document tools
UI
PyQt
web interface
внешние данные
web research
APIs
Итоговая архитектура проекта

После завершения:

PDF knowledge base
+
RAG assistant
+
Obsidian knowledge vault
+
local LLM