let currentFile = null;
let currentJobId = null;
let pollTimer = null;

const chatEl = document.getElementById("chat");
const fileInputEl = document.getElementById("fileInput");
const selectedFileNameEl = document.getElementById("selectedFileName");
const messageInputEl = document.getElementById("messageInput");
const sendBtnEl = document.getElementById("sendBtn");
const jobStatusEl = document.getElementById("jobStatus");
const currentDocumentEl = document.getElementById("currentDocument");
const documentsListEl = document.getElementById("documentsList");
const refreshDocsBtnEl = document.getElementById("refreshDocsBtn");
const sourcesPanelEl = document.getElementById("sourcesPanel");
const sourcesListEl = document.getElementById("sourcesList");

function escapeHtml(str) {
    return String(str)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;");
}

function setStatus(statusText, cssClass = "idle") {
    jobStatusEl.textContent = statusText;
    jobStatusEl.className = `status-pill ${cssClass}`;
}

function setCurrentDocument(filename) {
    currentFile = filename;
    currentDocumentEl.textContent = filename || "Не выбран";
    renderDocumentsActiveState();
}

function addMessage(text, sender = "assistant") {
    const row = document.createElement("div");
    row.className = `message-row ${sender}`;

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.textContent = text;

    row.appendChild(bubble);
    chatEl.appendChild(row);
    chatEl.scrollTop = chatEl.scrollHeight;
}

function showSources(chunks = []) {
    if (!chunks || chunks.length === 0) {
        sourcesPanelEl.classList.add("hidden");
        sourcesListEl.innerHTML = "";
        return;
    }

    sourcesPanelEl.classList.remove("hidden");
    sourcesListEl.innerHTML = chunks.map((chunk) => `
        <div class="source-card">
            <div class="source-card-header">
                <span>Chunk #${chunk.chunk_id}</span>
                <span>score: ${Number(chunk.score).toFixed(4)}</span>
            </div>
            <div class="source-text">${escapeHtml(chunk.text)}</div>
        </div>
    `).join("");
}

function setLoadingState(isLoading) {
    sendBtnEl.disabled = isLoading;
    fileInputEl.disabled = isLoading;
    messageInputEl.disabled = isLoading;
}

function renderDocuments(documents) {
    documentsListEl.innerHTML = "";

    if (!documents || documents.length === 0) {
        documentsListEl.innerHTML = `<div class="document-meta">Документов пока нет</div>`;
        return;
    }

    documents.forEach((doc) => {
        const item = document.createElement("div");
        item.className = "document-item";
        item.dataset.docId = doc.id;

        item.innerHTML = `
            <div class="document-name">${escapeHtml(doc.id)}</div>
            <div class="document-meta">
                status: ${escapeHtml(doc.status)} · processed: ${doc.is_processed ? "yes" : "no"}
            </div>
        `;

        item.addEventListener("click", () => {
            const filename = doc.id.endsWith(".pdf") ? doc.id : `${doc.id}.pdf`;
            setCurrentDocument(filename);
            addMessage(`Выбран документ: ${filename}`, "system");
        });

        documentsListEl.appendChild(item);
    });

    renderDocumentsActiveState();
}

function renderDocumentsActiveState() {
    const items = documentsListEl.querySelectorAll(".document-item");
    items.forEach((item) => {
        const possibleFilename = `${item.dataset.docId}.pdf`;
        item.classList.toggle(
            "active",
            currentFile === item.dataset.docId || currentFile === possibleFilename
        );
    });
}

async function loadDocuments() {
    try {
        const res = await fetch("/documents");
        const data = await res.json();
        renderDocuments(data);
    } catch (err) {
        console.error(err);
    }
}

async function pollStatusChat(jobId) {
    if (pollTimer) {
        clearInterval(pollTimer);
    }

    pollTimer = setInterval(async () => {
        try {
            const res = await fetch(`/jobs/${jobId}`);
            const data = await res.json();

            if (data.status === "queued") {
                setStatus("В очереди", "queued");
                return;
            }

            if (data.status === "running") {
                setStatus("Обработка...", "running");
                return;
            }

            if (data.status === "done") {
                setStatus("Готово", "done");
                addMessage("Документ обработан и готов к вопросам.", "system");
                clearInterval(pollTimer);
                pollTimer = null;
                await loadDocuments();
                return;
            }

            if (data.status === "failed") {
                setStatus("Ошибка", "failed");
                addMessage(`Ошибка обработки: ${data.error || "неизвестная ошибка"}`, "error");
                clearInterval(pollTimer);
                pollTimer = null;
            }
        } catch (err) {
            setStatus("Ошибка", "error");
            addMessage(`Ошибка получения статуса: ${err.message}`, "error");
            clearInterval(pollTimer);
            pollTimer = null;
        }
    }, 2000);
}

async function uploadAndProcess(file) {
    const formData = new FormData();
    formData.append("file", file);

    setLoadingState(true);
    setStatus("Загрузка...", "running");
    addMessage(`Файл: ${file.name}`, "user");
    addMessage("Загружаю и запускаю обработку...", "system");

    try {
        const res = await fetch("/upload-and-process", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "Upload failed");
        }

        setCurrentDocument(data.filename);
        currentJobId = data.job.job_id;
        setStatus("В очереди", "queued");
        addMessage(`Документ сохранён как ${data.filename}`, "system");

        await pollStatusChat(currentJobId);
    } catch (err) {
        setStatus("Ошибка", "failed");
        addMessage(`Ошибка загрузки: ${err.message}`, "error");
    } finally {
        setLoadingState(false);
        fileInputEl.value = "";
        selectedFileNameEl.textContent = "Файл не выбран";
    }
}

async function askQuestion(question) {
    if (!currentFile) {
        addMessage("Сначала загрузите или выберите документ.", "error");
        return;
    }

    setLoadingState(true);
    showSources([]);
    addMessage(question, "user");
    addMessage("Думаю...", "system");

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                filename: currentFile,
                question: question,
                top_k: 2,
                auto_process: true,
                response_mode: "short"
            })
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "Ask failed");
        }

        addMessage(data.answer || "Ответ не получен.", "assistant");
        showSources(data.top_chunks || []);
    } catch (err) {
        addMessage(`Ошибка запроса: ${err.message}`, "error");
    } finally {
        setLoadingState(false);
    }
}

function autoResizeTextarea() {
    messageInputEl.style.height = "auto";
    messageInputEl.style.height = `${Math.min(messageInputEl.scrollHeight, 180)}px`;
}

sendBtnEl.addEventListener("click", async () => {
    const file = fileInputEl.files[0];
    const text = messageInputEl.value.trim();

    if (file) {
        await uploadAndProcess(file);
        messageInputEl.value = "";
        autoResizeTextarea();
        return;
    }

    if (text) {
        await askQuestion(text);
        messageInputEl.value = "";
        autoResizeTextarea();
    }
});

fileInputEl.addEventListener("change", () => {
    const file = fileInputEl.files[0];
    selectedFileNameEl.textContent = file ? file.name : "Файл не выбран";
});

messageInputEl.addEventListener("input", autoResizeTextarea);

messageInputEl.addEventListener("keydown", async (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendBtnEl.click();
    }
});

refreshDocsBtnEl.addEventListener("click", loadDocuments);

addMessage("Привет. Загрузи PDF или выбери документ слева и задай вопрос.", "system");
loadDocuments();
setStatus("Ожидание", "idle");
autoResizeTextarea();