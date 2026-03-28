<div align="center">

<!-- Animated Header -->
<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=900&size=45&duration=3000&pause=500&color=00D4FF&center=true&vCenter=true&multiline=true&repeat=true&width=600&height=100&lines=%E2%9A%A1+J.A.R.V.I.S.+%E2%9A%A1" alt="JARVIS" />

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=18&duration=4000&pause=1000&color=7C3AED&center=true&vCenter=true&repeat=true&width=500&lines=Your+Intelligent+AI+Voice+Assistant;Real-time+Streaming+Conversations;PDF+Analysis+%26+Semantic+Search;Multi-Provider+LLM+Support" alt="Typing SVG" />

<br/><br/>

<!-- Badges -->
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-FF6F61?style=for-the-badge&logo=databricks&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-Real_Time-010101?style=for-the-badge&logo=socketdotio&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-UI-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

<br/>

```
     ╔══════════════════════════════════════════╗
     ║   "Good evening. I am J.A.R.V.I.S."      ║
     ║   "How may I assist you today?"          ║
     ╚══════════════════════════════════════════╝
```

<br/>

<!-- Divider -->
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

</div>

## Overview

**Jarvis** is a full-stack AI voice assistant built with **FastAPI** and **WebSocket** for real-time, streaming conversations. It supports text, voice input, PDF analysis, and leverages a vector database for semantic memory across conversations.

<div align="center">

```
 ┌──────────────┐     WebSocket      ┌──────────────────┐
 │   Browser    │ ◄════════════════► │  FastAPI Server  │
 │  (Tailwind)  │    Real-time       │                  │
 └──────────────┘    Streaming       │  ┌────────────┐  │
                                     │  │ LLM Service│  │
 ┌──────────────┐                    │  └─────┬──────┘  │
 │    MySQL     │◄───── ORM ─────────│        │         │
 │  (Messages)  │                    │  ┌─────▼──────┐  │
 └──────────────┘                    │  │  ChromaDB  │  │
                                     │  │ (Vectors)  │  │
 ┌──────────────┐                    │  └────────────┘  │
 │   Ollama /   │◄─── API ───────────│                  │
 │ OpenAI / etc │                    └──────────────────┘
 └──────────────┘                                        

```

</div>

<br/>

<div align="center">
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">
</div>

## Features

<table>
<tr>
<td width="50%">

### Core
| Feature | Description |
|---------|------------|
| **Real-time Chat** | WebSocket-powered streaming responses |
| **Voice I/O** | Speech-to-Text & Text-to-Speech |
| **PDF Analysis** | Upload & chat about PDF documents |
| **Semantic Memory** | ChromaDB vector search over history |
| **Multi-LLM** | Ollama, OpenAI, Anthropic, Gemini |

</td>
<td width="50%">

### Experience
| Feature | Description |
|---------|------------|
| **Dark/Light Theme** | Toggle with persisted preference |
| **Streaming UI** | Token-by-token response display |
| **Conversation Mgmt** | Create, switch, delete chats |
| **JWT Auth** | Secure user authentication |
| **Auto-Reconnect** | WebSocket reconnection with backoff |

</td>
</tr>
</table>

<br/>

<div align="center">
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">
</div>

## Tech Stack

<div align="center">

| Layer | Technology |
|:-----:|:-----------|
| **Backend** | ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) ![Uvicorn](https://img.shields.io/badge/-Uvicorn-2C2C2C?style=flat-square&logo=gunicorn&logoColor=white) |
| **Database** | ![MySQL](https://img.shields.io/badge/-MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white) ![ChromaDB](https://img.shields.io/badge/-ChromaDB-FF6F61?style=flat-square) |
| **AI/LLM** | ![Ollama](https://img.shields.io/badge/-Ollama-000000?style=flat-square) ![OpenAI](https://img.shields.io/badge/-OpenAI-412991?style=flat-square&logo=openai&logoColor=white) ![Anthropic](https://img.shields.io/badge/-Anthropic-191919?style=flat-square) ![Gemini](https://img.shields.io/badge/-Gemini-4285F4?style=flat-square&logo=google&logoColor=white) |
| **Speech** | ![STT](https://img.shields.io/badge/-SpeechRecognition-green?style=flat-square) ![TTS](https://img.shields.io/badge/-gTTS-orange?style=flat-square) ![Whisper](https://img.shields.io/badge/-Whisper-412991?style=flat-square&logo=openai&logoColor=white) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) ![TailwindCSS](https://img.shields.io/badge/-TailwindCSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white) ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) |
| **Auth** | ![JWT](https://img.shields.io/badge/-JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white) ![bcrypt](https://img.shields.io/badge/-bcrypt-003A70?style=flat-square) |

</div>

<br/>

<div align="center">
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">
</div>

## Project Structure

```
Jarvis/
├── app/
│   ├── api/
│   │   ├── api.py                 # REST endpoints (health, conversations)
│   │   ├── auth.py                # Login & registration
│   │   ├── websocket.py           # Real-time chat via WebSocket
│   │   ├── user.py                # User management
│   │   └── common.py              # Page routes (login, register, logout)
│   ├── core/
│   │   ├── config.py              # App settings & env config
│   │   ├── exceptions.py          # Custom exceptions
│   │   └── logging_config.py      # Logging setup
│   ├── models/
│   │   ├── database.py            # SQLAlchemy models
│   │   └── schemas.py             # Pydantic schemas
│   ├── services/
│   │   ├── chat_manager.py        # Chat orchestration
│   │   ├── llm_service.py         # Multi-provider LLM abstraction
│   │   ├── speech_service.py      # STT & TTS services
│   │   └── vector_embeddings.py   # ChromaDB vector search
│   ├── utils/
│   │   └── auth.py                # JWT utilities
│   ├── static/                    # Frontend assets (JS, CSS, images)
│   ├── templates/                 # HTML templates
│   └── main.py                    # FastAPI app factory
├── jarvis_db/                     # Alembic migrations
├── chroma/                        # ChromaDB persistent storage
├── run.py                         # Entry point
├── requirements.txt               # Python dependencies
├── alembic.ini                    # Migration config
└── .env.example                   # Environment template
```

<br/>

<div align="center">
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">
</div>

## Getting Started

### Prerequisites

- **Python 3.10+**
- **MySQL** server
- **Ollama** (for local LLM) or API keys for OpenAI/Anthropic/Gemini

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/Jarvis.git
cd Jarvis

# 2. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your database credentials and preferences
```

### Database Setup

```bash
# Run Alembic migrations
alembic upgrade head
```

### LLM Setup (Ollama - Local)

```bash
# Start Ollama server
ollama serve

# Pull required models
ollama pull llama3.1
ollama pull qwen3-embedding:0.6b
```

### Run

```bash
python run.py
```

> Open **http://localhost:8000** in your browser

<br/>

<div align="center">
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">
</div>

## Configuration

<details>
<summary><b>Environment Variables</b></summary>

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `ollama` | LLM provider: `ollama`, `openai`, `anthropic`, `gemini` |
| `LLM_HOST` | `http://localhost:11434` | Ollama server URL |
| `LLM_MODEL` | `llama3.1` | Model name |
| `EMBEDDING_LLM_MODEL` | `qwen3-embedding:0.6b` | Embedding model |
| `STT_PROVIDER` | `google_free` | STT: `google_free` or `openai_whisper` |
| `TTS_PROVIDER` | `google_free` | TTS: `google_free` or `openai_tts` |
| `DATABASE_URL` | - | MySQL connection string |
| `SECRET_KEY` | - | App secret key |
| `JWT_SECRET_KEY` | - | JWT signing key |
| `JWT_ALGORITHM` | `HS256` | JWT algorithm |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `DEBUG` | `true` | Debug mode |

</details>

<br/>

<div align="center">
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">
</div>

## API Reference

<details>
<summary><b>REST Endpoints</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main dashboard (auth required) |
| `GET` | `/login` | Login page |
| `GET` | `/register` | Registration page |
| `POST` | `/auth/` | Authenticate user |
| `POST` | `/auth/register` | Register new user |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/conversations` | List conversations |
| `GET` | `/api/conversations/{id}/messages` | Get messages |
| `DELETE` | `/api/conversations/{id}` | Delete conversation |

</details>

<details>
<summary><b>WebSocket</b></summary>

| Endpoint | Description |
|----------|-------------|
| `WS /ws/chat` | Real-time bidirectional chat |

**Message Types (Client -> Server):**
- `text` - Text message
- `audio` - Voice recording (base64)
- `control` - Control commands

**Response Types (Server -> Client):**
- `text_response` - Streamed text chunks
- `voice_response` - TTS audio (base64)
- `async_response` - Async results
- `typing` - Typing indicator

</details>

<br/>

<div align="center">
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">
</div>

## How It Works

```
 User Input (Text/Voice/PDF)
         │
         ▼
 ┌───────────────┐
 │   WebSocket   │──── Authentication (JWT)
 └───────┬───────┘
         │
         ▼
 ┌───────────────┐     ┌────────────────┐
 │ Chat Manager  │────►│  Vector Search │ ◄── ChromaDB
 └───────┬───────┘     │ (RAG Context)  │
         │             └────────────────┘
         ▼
 ┌───────────────┐
 │  LLM Service  │──── Ollama / OpenAI / Anthropic / Gemini
 └───────┬───────┘
         │
         ▼
 ┌───────────────┐     ┌────────────────┐
 │   Streaming   │     │   Persist to   │
 │   Response    │────►│  MySQL + Chroma│
 └───────┬───────┘     └────────────────┘
         │
         ▼
 ┌───────────────┐
 │  TTS (opt.)   │──── gTTS / OpenAI TTS
 └───────┬───────┘
         │
         ▼
    Client Display
```

<br/>

<div align="center">
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">
</div>

## Contributing

Contributions are welcome! Feel free to open issues and pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

<br/>

<div align="center">
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">
</div>

<div align="center">

## License

This project is open source and available under the [MIT License](LICENSE).

<br/>

```
 ╔════════════════════════════════════════════════════╗
 ║                                                    ║
 ║   Built with FastAPI, WebSockets & AI              ║
 ║   Powered by Ollama, OpenAI, Anthropic & Gemini    ║
 ║                                                    ║
 ╚════════════════════════════════════════════════════╝
```

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=00D4FF&center=true&vCenter=true&repeat=true&width=400&lines=%E2%AD%90+Star+this+repo!+%E2%AD%90" alt="Star" />

<br/><br/>

**[Back to Top](#overview)**

</div>
