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

    let currentConversationId = null;

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
        addMessage("user", text);
        messageInput.value = "";
        autoResize();

        jarvisWS.sendText(text, {
            conversationId: currentConversationId,
            ttsEnabled: ttsToggle.checked,
        });
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
                const item = document.createElement("button");
                item.className = `w-full text-left px-3 py-2 rounded-lg text-sm truncate transition-colors ${
                    conv.conversation_id === currentConversationId
                        ? "bg-jarvis-surface text-jarvis-accent"
                        : "text-gray-400 hover:bg-jarvis-surface hover:text-gray-200"
                }`;
                item.textContent = conv.title || "Untitled";
                item.title = conv.title;
                item.addEventListener("click", () => loadConversation(conv.conversation_id));
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
