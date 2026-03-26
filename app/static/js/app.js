/**
 * Jarvis Dashboard - Main Application Controller
 */
window.addEventListener("load", () => {
    // DOM elements
    const messagesEl = document.getElementById("messages");
    const welcomeMsg = document.getElementById("welcome-msg");
    const messageInput = document.getElementById("message-input");
    const sendBtn = document.getElementById("send-btn");
    const micBtn = document.getElementById("mic-btn");
    const newChatBtn = document.getElementById("new-chat-btn");
    const typingIndicator = document.getElementById("typing-indicator");
    const typingText = document.getElementById("typing-text");
    const connectionDot = document.getElementById("connection-dot");
    const connectionStatus = document.getElementById("connection-status");
    const chatTitle = document.getElementById("chat-title");
    const ttsToggle = document.getElementById("tts-toggle");
    const settingsBtn = document.getElementById("settings-btn");
    const settingsModal = document.getElementById("settings-modal");
    const closeSettings = document.getElementById("close-settings");
    const conversationList = document.getElementById("conversation-list");

    const fileBtn = document.getElementById("file-btn");
    const fileInput = document.getElementById("file-input");
    const filePreviewBar = document.getElementById("file-preview-bar");

    let currentConversationId = null;
    let pendingFiles = []; // {name, type, size, base64}

    // ========================
    // Theme Toggle
    // ========================
    const themeToggle = document.getElementById("theme-toggle");
    const themeSun = document.getElementById("theme-sun");
    const themeMoon = document.getElementById("theme-moon");

    function applyTheme(theme) {
        if (theme === "light") {
            document.documentElement.classList.remove("dark");
            document.documentElement.classList.add("light");
            document.body.style.backgroundColor = "#f8fafc";
            document.body.style.color = "#1e293b";
            themeSun.classList.add("hidden");
            themeMoon.classList.remove("hidden");
        } else {
            document.documentElement.classList.remove("light");
            document.documentElement.classList.add("dark");
            document.body.style.backgroundColor = "";
            document.body.style.color = "";
            themeMoon.classList.add("hidden");
            themeSun.classList.remove("hidden");
        }
        localStorage.setItem("jarvis-theme", theme);
    }

    // Initialize theme icons
    applyTheme(localStorage.getItem("jarvis-theme") || "dark");

    themeToggle.addEventListener("click", () => {
        const current = localStorage.getItem("jarvis-theme") || "dark";
        applyTheme(current === "dark" ? "light" : "dark");
    });

    // ========================
    // File Upload
    // ========================
    fileBtn.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", () => {
        const files = Array.from(fileInput.files);
        files.forEach((file) => {
            if (file.size > 10 * 1024 * 1024) {
                addMessage("assistant", `File "${file.name}" exceeds 10MB limit.`, true);
                return;
            }
            const reader = new FileReader();
            reader.onload = () => {
                const base64 = reader.result.split(",")[1];
                pendingFiles.push({
                    name: file.name,
                    type: file.type,
                    size: file.size,
                    base64: base64,
                });
                renderFilePreview();
            };
            reader.readAsDataURL(file);
        });
        fileInput.value = "";
    });

    // Drag & drop on message input area
    const inputArea = messageInput.closest(".border-t");
    inputArea.addEventListener("dragover", (e) => {
        e.preventDefault();
        inputArea.classList.add("border-jarvis-accent");
    });
    inputArea.addEventListener("dragleave", () => {
        inputArea.classList.remove("border-jarvis-accent");
    });
    inputArea.addEventListener("drop", (e) => {
        e.preventDefault();
        inputArea.classList.remove("border-jarvis-accent");
        const files = Array.from(e.dataTransfer.files);
        files.forEach((file) => {
            if (file.size > 10 * 1024 * 1024) {
                addMessage("assistant", `File "${file.name}" exceeds 10MB limit.`, true);
                return;
            }
            const reader = new FileReader();
            reader.onload = () => {
                const base64 = reader.result.split(",")[1];
                pendingFiles.push({
                    name: file.name,
                    type: file.type,
                    size: file.size,
                    base64: base64,
                });
                renderFilePreview();
            };
            reader.readAsDataURL(file);
        });
    });

    function renderFilePreview() {
        filePreviewBar.innerHTML = "";
        if (pendingFiles.length === 0) {
            filePreviewBar.classList.add("hidden");
            return;
        }
        filePreviewBar.classList.remove("hidden");

        pendingFiles.forEach((file, index) => {
            const tag = document.createElement("div");
            tag.className = "flex items-center gap-2 bg-jarvis-surface border border-gray-700 rounded-lg px-3 py-1.5 text-xs text-gray-300";

            const isImage = file.type.startsWith("image/");
            if (isImage) {
                const thumb = document.createElement("img");
                thumb.src = `data:${file.type};base64,${file.base64}`;
                thumb.className = "w-6 h-6 rounded object-cover";
                tag.appendChild(thumb);
            } else {
                const icon = document.createElement("span");
                icon.innerHTML = `<svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>`;
                tag.appendChild(icon);
            }

            const nameSpan = document.createElement("span");
            nameSpan.textContent = file.name.length > 20 ? file.name.slice(0, 17) + "..." : file.name;
            nameSpan.title = file.name;
            tag.appendChild(nameSpan);

            const sizeSpan = document.createElement("span");
            sizeSpan.className = "text-gray-500";
            sizeSpan.textContent = formatFileSize(file.size);
            tag.appendChild(sizeSpan);

            const removeBtn = document.createElement("button");
            removeBtn.className = "text-gray-500 hover:text-red-400 transition-colors ml-1";
            removeBtn.innerHTML = `<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>`;
            removeBtn.addEventListener("click", () => {
                pendingFiles.splice(index, 1);
                renderFilePreview();
            });
            tag.appendChild(removeBtn);

            filePreviewBar.appendChild(tag);
        });
    }

    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
        return (bytes / (1024 * 1024)).toFixed(1) + " MB";
    }

    // ========================
    // WebSocket Setup
    // ========================
    jarvisWS.onStatusChange = (connected) => {
        connectionDot.className = `w-2 h-2 rounded-full ${connected ? "bg-green-500" : "bg-red-500"}`;
        connectionStatus.textContent = connected ? "Connected" : "Disconnected";
    };

    jarvisWS.onMessageCallback = (data) => {
        switch (data.type) {
            case "text_response":
            case "voice_response":
                hideTyping();
                addMessage("assistant", data.message);
                currentConversationId = data.conversation_id;
                // Play TTS audio if available
                if (data.audio_base64) {
                    audioManager.playAudio(data.audio_base64);
                }
                loadConversations();
                break;

            case "typing":
                if (data.status) {
                    showTyping(data.message || "Jarvis is thinking...");
                } else {
                    hideTyping();
                }
                break;

            case "control_response":
                currentConversationId = null;
                clearMessages();
                chatTitle.textContent = "New Conversation";
                break;

            case "error":
                hideTyping();
                addMessage("assistant", `Error: ${data.message}`, true);
                break;
        }
    };

    jarvisWS.connect();

    // ========================
    // Message Handling
    // ========================
    function sendMessage() {
        const text = messageInput.value.trim();
        if (!text) return;

        hideWelcome();

        // Build display message
        let displayMsg = text;
        if (pendingFiles.length > 0) {
            const fileNames = pendingFiles.map(f => f.name).join(", ");
            displayMsg = text ? `${text}\n📎 ${fileNames}` : `📎 ${fileNames}`;
        }
        addMessage("user", displayMsg);

        // Send files as array of {name, type, size, base64}
        const filesToSend = pendingFiles.length > 0
            ? pendingFiles.map(f => ({ name: f.name, type: f.type, size: f.size, content: f.base64 }))
            : null;

        jarvisWS.sendText(text || "", {
            conversationId: currentConversationId,
            ttsEnabled: ttsToggle.checked,
            files: filesToSend,
        });

        // Clear pending files
        pendingFiles = [];
        renderFilePreview();
        messageInput.value = "";
        autoResize();
    }

    function addMessage(role, content, isError = false) {
        hideWelcome();

        const wrapper = document.createElement("div");
        wrapper.className = `flex ${role === "user" ? "justify-end" : "justify-start"}`;

        const bubble = document.createElement("div");
        const baseClasses = "max-w-[70%] rounded-2xl px-4 py-3 text-sm leading-relaxed";

        if (isError) {
            bubble.className = `${baseClasses} bg-red-900/30 border border-red-800 text-red-300`;
        } else if (role === "user") {
            bubble.className = `${baseClasses} bg-jarvis-accent/20 border border-jarvis-accent/30 text-gray-100`;
        } else {
            bubble.className = `${baseClasses} bg-jarvis-surface2 border border-gray-700 text-gray-200`;
        }

        bubble.innerHTML = formatMessage(content);
        wrapper.appendChild(bubble);
        messagesEl.appendChild(wrapper);

        messagesEl.scrollTo({ top: messagesEl.scrollHeight, behavior: "smooth" });
    }

    function formatMessage(text) {
        // Basic markdown-like formatting
        return text
            .replace(/```([\s\S]*?)```/g, '<pre class="bg-jarvis-dark rounded-lg p-3 my-2 overflow-x-auto text-xs"><code>$1</code></pre>')
            .replace(/`([^`]+)`/g, '<code class="bg-jarvis-dark px-1.5 py-0.5 rounded text-jarvis-accent text-xs">$1</code>')
            .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
            .replace(/\n/g, "<br>");
    }

    function clearMessages() {
        messagesEl.innerHTML = "";
        showWelcome();
    }

    function hideWelcome() {
        if (welcomeMsg) welcomeMsg.style.display = "none";
    }

    function showWelcome() {
        if (welcomeMsg) welcomeMsg.style.display = "flex";
    }

    function showTyping(text = "Jarvis is thinking...") {
        typingText.textContent = text;
        typingIndicator.classList.remove("hidden");
    }

    function hideTyping() {
        typingIndicator.classList.add("hidden");
    }

    // ========================
    // Input Handling
    // ========================
    sendBtn.addEventListener("click", sendMessage);

    messageInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Auto-resize textarea
    function autoResize() {
        messageInput.style.height = "auto";
        messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + "px";
    }
    messageInput.addEventListener("input", autoResize);

    // ========================
    // Voice Recording
    // ========================
    audioManager.onRecordingComplete = (base64Audio) => {
        jarvisWS.sendAudio(base64Audio, {
            conversationId: currentConversationId,
            ttsEnabled: true,
        });
        addMessage("user", "[Voice message]");
    };

    audioManager.onRecordingStart = () => {
        micBtn.classList.add("recording");
        micBtn.querySelector("svg").classList.remove("text-gray-400");
        micBtn.querySelector("svg").classList.add("text-red-400");
    };

    audioManager.onRecordingStop = () => {
        micBtn.classList.remove("recording");
        micBtn.querySelector("svg").classList.remove("text-red-400");
        micBtn.querySelector("svg").classList.add("text-gray-400");
    };

    // Click to toggle recording
    micBtn.addEventListener("click", () => {
        if (audioManager.isRecording) {
            audioManager.stopRecording();
        } else {
            hideWelcome();
            audioManager.startRecording();
        }
    });

    // ========================
    // New Conversation
    // ========================
    newChatBtn.addEventListener("click", () => {
        jarvisWS.sendControl("new_conversation");
    });

    // ========================
    // Conversations Sidebar
    // ========================
    async function loadConversations() {
        try {
            const response = await fetch("/api/conversations");
            const conversations = await response.json();

            conversationList.innerHTML = "";
            conversations.forEach((conv) => {
                const item = document.createElement("div");
                const isActive = conv.conversation_id === currentConversationId;
                item.className = `group flex items-center gap-1 rounded-lg transition-colors ${
                    isActive
                        ? "bg-jarvis-surface text-jarvis-accent"
                        : "text-gray-400 hover:bg-jarvis-surface hover:text-gray-200"
                }`;

                const titleBtn = document.createElement("button");
                titleBtn.className = "flex-1 text-left px-3 py-2 text-sm truncate";
                titleBtn.textContent = conv.title || "Untitled";
                titleBtn.title = conv.title;
                titleBtn.addEventListener("click", () => loadConversation(conv.conversation_id));

                const deleteBtn = document.createElement("button");
                deleteBtn.className = "shrink-0 p-1.5 mr-1 rounded-md opacity-0 group-hover:opacity-100 text-gray-500 hover:text-red-400 hover:bg-red-500/10 transition-all";
                deleteBtn.title = "Delete conversation";
                deleteBtn.innerHTML = `<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>`;
                deleteBtn.addEventListener("click", (e) => {
                    e.stopPropagation();
                    deleteConversation(conv.conversation_id);
                });

                item.appendChild(titleBtn);
                item.appendChild(deleteBtn);
                conversationList.appendChild(item);
            });
        } catch (err) {
            console.error("Failed to load conversations:", err);
        }
    }

    async function loadConversation(conversationId) {
        try {
            const response = await fetch(`/api/conversations/${conversationId}/messages`);
            const messages = await response.json();

            clearMessages();
            hideWelcome();
            currentConversationId = conversationId;

            messages.forEach((msg) => {
                if (msg.role !== "system") {
                    addMessage(msg.role, msg.content);
                }
            });

            chatTitle.textContent = conversationId.slice(0, 8) + "...";
            loadConversations();
        } catch (err) {
            console.error("Failed to load conversation:", err);
        }
    }

    async function deleteConversation(conversationId) {
        try {
            const res = await fetch(`/api/conversations/${conversationId}`, { method: "DELETE" });
            if (!res.ok) return;

            if (currentConversationId === conversationId) {
                currentConversationId = null;
                clearMessages();
                chatTitle.textContent = "New Conversation";
            }
            loadConversations();
        } catch (err) {
            console.error("Failed to delete conversation:", err);
        }
    }

    // Load conversations on startup
    loadConversations();

    // ========================
    // Settings Modal
    // ========================
    settingsBtn.addEventListener("click", async () => {
        settingsModal.classList.remove("hidden");
        // Load health status
        try {
            const resp = await fetch("/api/health");
            const health = await resp.json();
            document.getElementById("system-status").textContent =
                `Status: ${health.status}\nLLM: ${health.llm_provider}\nSTT: ${health.stt_provider}\nTTS: ${health.tts_provider}\nVersion: ${health.version}`;
        } catch {
            document.getElementById("system-status").textContent = "Failed to load status";
        }
    });

    closeSettings.addEventListener("click", () => {
        settingsModal.classList.add("hidden");
    });

    settingsModal.addEventListener("click", (e) => {
        if (e.target === settingsModal) {
            settingsModal.classList.add("hidden");
        }
    });
});
