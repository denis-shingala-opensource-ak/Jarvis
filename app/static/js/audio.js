/**
 * Audio recording and playback utilities.
 */
class AudioManager {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.stream = null;
        this.onRecordingComplete = null;
        this.onRecordingStart = null;
        this.onRecordingStop = null;
    }

    async init() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 16000,
                },
            });
            return true;
        } catch (error) {
            console.error("Microphone access denied:", error);
            return false;
        }
    }

    async startRecording() {
        if (this.isRecording) return;

        if (!this.stream) {
            const success = await this.init();
            if (!success) return;
        }

        this.audioChunks = [];
        this.mediaRecorder = new MediaRecorder(this.stream, {
            mimeType: this._getSupportedMimeType(),
        });

        this.mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                this.audioChunks.push(event.data);
            }
        };

        this.mediaRecorder.onstop = () => {
            const blob = new Blob(this.audioChunks, {
                type: this.mediaRecorder.mimeType,
            });
            this._blobToBase64(blob).then((base64) => {
                if (this.onRecordingComplete) {
                    this.onRecordingComplete(base64);
                }
            });
        };

        this.mediaRecorder.start();
        this.isRecording = true;

        if (this.onRecordingStart) {
            this.onRecordingStart();
        }
    }

    stopRecording() {
        if (!this.isRecording || !this.mediaRecorder) return;

        this.mediaRecorder.stop();
        this.isRecording = false;

        if (this.onRecordingStop) {
            this.onRecordingStop();
        }
    }

    playAudio(base64String) {
        const audioData = atob(base64String);
        const arrayBuffer = new ArrayBuffer(audioData.length);
        const view = new Uint8Array(arrayBuffer);
        for (let i = 0; i < audioData.length; i++) {
            view[i] = audioData.charCodeAt(i);
        }

        const blob = new Blob([arrayBuffer], { type: "audio/mp3" });
        const url = URL.createObjectURL(blob);
        const audio = new Audio(url);

        audio.onended = () => {
            URL.revokeObjectURL(url);
        };

        audio.play().catch((err) => {
            console.error("Audio playback failed:", err);
        });
    }

    _getSupportedMimeType() {
        const types = [
            "audio/webm;codecs=opus",
            "audio/webm",
            "audio/ogg;codecs=opus",
            "audio/mp4",
        ];
        for (const type of types) {
            if (MediaRecorder.isTypeSupported(type)) {
                return type;
            }
        }
        return "audio/webm";
    }

    _blobToBase64(blob) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onloadend = () => {
                const base64 = reader.result.split(",")[1];
                resolve(base64);
            };
            reader.readAsDataURL(blob);
        });
    }
}

// Global instance
const audioManager = new AudioManager();
