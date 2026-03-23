/**
 * WebSocket connection management with auto-reconnect.
 */
class JarvisWebSocket {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        this.reconnectDelay = 1000;
        this.onMessageCallback = null;
        this.onStatusChange = null;
    }

    connect() {
        const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
        const url = `${protocol}//${window.location.host}/ws/chat`;

        this.ws = new WebSocket(url);

        this.ws.onopen = () => {
            console.log("WebSocket connected");
            this.reconnectAttempts = 0;
            this.reconnectDelay = 1000;
            if (this.onStatusChange) {
                this.onStatusChange(true);
            }
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (this.onMessageCallback) {
                this.onMessageCallback(data);
            }
        };

        this.ws.onclose = (event) => {
            console.log("WebSocket closed:", event.code);
            if (this.onStatusChange) {
                this.onStatusChange(false);
            }
            this._reconnect();
        };

        this.ws.onerror = (error) => {
            console.error("WebSocket error:", error);
        };
    }

    _reconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error("Max reconnection attempts reached");
            return;
        }

        this.reconnectAttempts++;
        const delay = this.reconnectDelay * Math.pow(1.5, this.reconnectAttempts - 1);
        console.log(`Reconnecting in ${Math.round(delay)}ms (attempt ${this.reconnectAttempts})`);

        setTimeout(() => this.connect(), delay);
    }

    send(type, content, options = {}) {
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
            console.error("WebSocket not connected");
            return false;
        }

        const message = {
            type: type,
            content: content,
            conversation_id: options.conversationId || null,
            tts_enabled: options.ttsEnabled !== undefined ? options.ttsEnabled : true,
        };

        this.ws.send(JSON.stringify(message));
        return true;
    }

    sendText(text, options = {}) {
        return this.send("text", text, options);
    }

    sendAudio(base64Audio, options = {}) {
        return this.send("audio", base64Audio, options);
    }

    sendControl(command) {
        return this.send("control", command);
    }

    isConnected() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }
}

// Global instance
const jarvisWS = new JarvisWebSocket();
