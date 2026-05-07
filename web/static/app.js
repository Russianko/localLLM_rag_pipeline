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
const assistantSelectEl = document.getElementById("assistantSelect");
const assistantDescriptionEl = document.getElementById("assistantDescription");
const voiceBtnEl = document.getElementById("voiceBtn");

let sessionId = localStorage.getItem("local_ai_session_id");
if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem("local_ai_session_id", sessionId);
}
let currentAssistant = "auto";
let assistantsCache = [];
let isRecording = false;

voiceBtnEl.addEventListener("click", async () => {
    if (isRecording) {
        stopVoiceRecording();
        isRecording = false;
        voiceBtnEl.textContent = "🎤";
        voiceBtnEl.classList.remove("recording");
    } else {
        await startVoiceRecording();
        isRecording = true;
        voiceBtnEl.textContent = "⏹";
        voiceBtnEl.classList.add("recording");
    }
});

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

async function resetMemory() {
    try {
        const res = await fetch(`/memory/reset?session_id=${encodeURIComponent(sessionId)}`, {
            method: "POST"
        });

        const raw = await res.text();

        let data;
        try {
            data = JSON.parse(raw);
        } catch {
            throw new Error(raw || `HTTP ${res.status}`);
        }

        if (!res.ok) {
            throw new Error(data.detail || "Memory reset failed");
        }

        addMessage("Память текущего диалога очищена.", "system");
        await loadMemoryStatus();
    } catch (err) {
        addMessage(`Ошибка очистки памяти: ${err.message}`, "error");
    }
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

function isDocumentReady() {
    return jobStatusEl.textContent === "Готово" || currentJobId === null;
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
    showSources([]);
    addMessage(`Выбран документ: ${filename}`, "system");
});

        documentsListEl.appendChild(item);
    });

    renderDocumentsActiveState();
}

async function loadAssistants() {
    try {
        const res = await fetch("/assistants");
        const data = await res.json();

        assistantsCache = data.assistants || [];

        assistantSelectEl.innerHTML = "";

        assistantsCache.forEach((assistant) => {
            const option = document.createElement("option");
            option.value = assistant.type;
            option.textContent = assistant.name;
            assistantSelectEl.appendChild(option);
        });

        currentAssistant = data.default || "auto";
        assistantSelectEl.value = currentAssistant;
        updateAssistantDescription();
    } catch (err) {
        console.error(err);
        assistantSelectEl.innerHTML = `<option value="auto">Auto</option>`;
        assistantDescriptionEl.textContent = "Автоматический выбор агента недоступен.";
        currentAssistant = "auto";
        addMessage("Не удалось загрузить список ассистентов.", "error");
    }
}

function updateAssistantDescription() {
    const selected = assistantsCache.find(a => a.type === assistantSelectEl.value);
    currentAssistant = assistantSelectEl.value;
    assistantDescriptionEl.textContent = selected ? selected.description : "";
}

assistantSelectEl.addEventListener("change", () => {
    updateAssistantDescription();
    addMessage(`Режим агента: ${assistantSelectEl.options[assistantSelectEl.selectedIndex].text}`, "system");
});

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

let mediaRecorder;
let chunks = [];

async function startVoiceRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
  chunks = [];

  mediaRecorder.ondataavailable = (event) => {
    if (event.data.size > 0) chunks.push(event.data);
  };

  mediaRecorder.onstop = async () => {
    const blob = new Blob(chunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("file", blob, "voice.webm");
    formData.append("filename", currentFile || "");
    formData.append("assistant_type", currentAssistant);
    formData.append("session_id", sessionId);

    const response = await fetch("/voice", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (data.transcript) {
    addMessage(data.transcript, "user");
    }

    addMessage(data.answer || "Ответ не получен.", "assistant");
    // тут вставляешь transcript как user message
    // answer как assistant message
  };

  mediaRecorder.start();
}

function stopVoiceRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
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
                currentJobId = null;
                await loadDocuments();
                return;
            }

            if (data.status === "failed") {
                setStatus("Ошибка", "failed");
                addMessage(`Ошибка обработки: ${data.error || "неизвестная ошибка"}`, "error");
                clearInterval(pollTimer);
                pollTimer = null;
                currentJobId = null;
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
    showSources([]);

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

function isFigmaToolRequest(question) {
    const text = question.toLowerCase();

    return [
        "фигма",
        "figma",
        "локализация",
        "локализуй",
        "plugin actions",
        "figma actions"
    ].some(word => text.includes(word));
}

async function loadFigmaBridgeStatus() {
    try {
        const res = await fetch("/bridge/figma/status");
        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "Bridge status failed");
        }

        addMessage(
            `Figma bridge: actions=${data.actions_count}, frames=${data.frames_count}, nodes=${data.nodes_count}`,
            "system"
        );

        if (data.last_execution_result) {
            addMessage(
                `Last Figma execution: ${data.last_execution_result.status}`,
                "system"
            );
        }
    } catch (err) {
        addMessage(`Ошибка bridge status: ${err.message}`, "error");
    }
}

async function askQuestion(question) {
    const isToolRequest = isFigmaToolRequest(question);
    const needsDocument = currentAssistant === "rag" && !isToolRequest;

    if (needsDocument && !currentFile) {
        addMessage("Сначала загрузите или выберите документ.", "error");
        return;
    }

    if (needsDocument && !isDocumentReady()) {
        addMessage("Документ ещё обрабатывается. Дождитесь статуса 'Готово'.", "error");
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
                filename: isToolRequest ? null : currentFile,
                question: question,
                top_k: 2,
                auto_process: true,
                response_mode: "short",
                assistant_type: isToolRequest ? "chat" : currentAssistant,
                session_id: sessionId,
            })
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "Ask failed");
        }

        addMessage(data.answer || "Ответ не получен.", "assistant");

        if (isToolRequest) {
            await loadFigmaBridgeStatus();
        }

        if (data.selected_assistant) {
            const selected = assistantsCache.find(a => a.type === data.selected_assistant);
            const assistantName = selected ? selected.name : data.selected_assistant;
            addMessage(`Использован агент: ${assistantName}`, "system");
        }

        showSources(data.top_chunks || []);
        await loadMemoryStatus();
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

const resetMemoryBtn = document.createElement("button");
resetMemoryBtn.textContent = "Очистить память";
resetMemoryBtn.className = "secondary-btn";
resetMemoryBtn.style.marginTop = "12px";
resetMemoryBtn.style.width = "100%";
resetMemoryBtn.addEventListener("click", resetMemory);

const memoryStatusEl = document.createElement("div");
memoryStatusEl.className = "document-meta";
memoryStatusEl.style.marginTop = "8px";
memoryStatusEl.textContent = "Память: неизвестно";

async function loadMemoryStatus() {
    try {
        const res = await fetch(`/memory/status?session_id=${encodeURIComponent(sessionId)}`);
        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "Memory status failed");
        }

        memoryStatusEl.textContent = data.has_memory
            ? `Память: ${data.messages_count}/${data.max_messages}`
            : "Память: пусто";
    } catch (err) {
        memoryStatusEl.textContent = "Память: ошибка";
    }
}

documentsListEl.parentNode.insertBefore(resetMemoryBtn, documentsListEl);
documentsListEl.parentNode.insertBefore(memoryStatusEl, documentsListEl);


addMessage("Привет. Можешь просто задать вопрос или загрузить PDF и спросить по документу.", "system");
loadDocuments();
setStatus("Ожидание", "idle");
autoResizeTextarea();
loadAssistants();
loadMemoryStatus();