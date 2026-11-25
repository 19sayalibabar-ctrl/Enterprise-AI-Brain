# Enterprise AI Brain

A multi-agent knowledge assistant that lets a team upload its own documents
and ask questions grounded in them. Under the hood it combines Retrieval
Augmented Generation (RAG), a five-agent workflow, and short-term
conversation memory — built as a lightweight prototype that runs entirely on
a local Windows 11 machine, CPU only.

> **Status:** Phase 3 of 6 complete — Chat is live: ask a question, get an
> answer grounded in your uploaded documents, with sources and memory of
> the conversation. See [Roadmap](#roadmap) below.

## Project overview

Enterprise AI Brain is not a chatbot wrapper. It's a small, working
demonstration of how an AI knowledge system is actually architected:

- **Document intelligence** — PDF/DOCX/TXT parsing, chunking, embeddings
- **Retrieval Augmented Generation** — FAISS vector search over your own documents
- **Multi-agent orchestration** — Manager, Planning, Retriever, Analysis, and
  Report agents, each with a narrow responsibility
- **Memory** — per-user conversation history
- **A real full-stack app** — FastAPI backend, React + Tailwind frontend, JWT auth

It's intentionally scoped to run on a laptop with no Docker, no message
queues, and no paid cloud services — see [Future scope](#future-scope) for
what's deliberately left out of this version.

## Architecture

```
                     ┌─────────────┐
   Browser  ───────▶ │   FastAPI   │ ───▶ SQLite (users, documents, chunks, messages)
  (React/Vite)  ◀─── │   backend   │ ───▶ FAISS (one index per user)
                     └──────┬──────┘        │
                            │               ▼
                            │        ┌──────────────┐
                            └───────▶│ Retriever    │──▶ LLM (OpenAI/Gemini)
                                     │ Agent        │      answers + memory
                                     └──────────────┘
```

**Chat flow (Phase 3, now live):**

```
Question ─▶ recent history (memory) ─▶ Retriever Agent
   (condenses follow-ups, searches FAISS) ─▶ LLM answers from retrieved
   excerpts, citing sources ─▶ stored back into memory
```

Phase 4 doesn't replace this — it splits "reason over retrieved context"
and "format the final answer" out of the single LLM call above into their
own Analysis and Report agents, with a Manager/Planning layer in front for
multi-step questions. Retrieval and memory stay exactly as built here.

## Folder structure

```
enterprise-ai-brain/
├── backend/
│   ├── main.py               # FastAPI app entry point
│   ├── config/                 # Settings loaded from .env
│   ├── database/                # SQLAlchemy models: User, Document,
│   │                             #   DocumentChunk, Message
│   ├── schemas/                  # Pydantic request/response models
│   ├── api/                       # auth.py, documents.py, chat.py
│   ├── utils/                      # security.py, extraction.py, chunking.py
│   ├── embeddings/                  # embedder.py (sentence-transformers, CPU)
│   ├── vectorstore/                  # store.py (FAISS) + generated *.faiss (gitignored)
│   ├── agents/                        # llm_client.py, retriever_agent.py
│   │                                   #   (Manager/Planning/Analysis/Report: Phase 4)
│   ├── memory/                          # conversation_memory.py (recency window)
│   ├── uploads/                          # uploaded source files — gitignored
│   ├── tests/                             # pytest suite (auth, documents, chat)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── src/
│       ├── pages/            # Login, Register, Dashboard, Upload, Chat
│       ├── components/       # AppShell, ProtectedRoute, ThemeToggle, SignalMark
│       ├── context/          # AuthContext
│       └── api/              # client.js, documents.js, chat.js
├── docs/                     # Architecture notes (expanded in Phase 6)
└── README.md
```

## Installation

Requirements: **Windows 11**, **Python 3.12**, **Node.js LTS**, **Git**, run
from **PowerShell**. Also, an API key for **either** OpenAI or Gemini —
Chat won't answer without one (retrieval and everything else still works).

### 1. Backend

```powershell
cd enterprise-ai-brain\backend
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

> If PowerShell blocks the activation script with an execution-policy error,
> run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first,
> then re-run `.\venv\Scripts\Activate.ps1`.

> **Already set up Phase 1/2?** Just re-run `pip install -r requirements.txt`
> in the same venv — this phase adds the `openai` and `google-generativeai`
> SDKs (both install; only the one you configure below is actually called).

**Set your LLM key in `backend\.env`:**

```
LLM_PROVIDER=openai        # or: gemini
OPENAI_API_KEY=sk-...      # if using OpenAI
GEMINI_API_KEY=...         # if using Gemini instead
```

Leave the provider you're *not* using blank. OpenAI needs a billed account;
Gemini has a free tier and a key from [Google AI Studio](https://aistudio.google.com/app/apikey)
— either works, this is purely which one you have access to.

Start the API:

```powershell
uvicorn main:app --reload --port 8000
```

The API is now at `http://localhost:8000` and interactive docs at
`http://localhost:8000/docs`.

### 2. Frontend

```powershell
cd enterprise-ai-brain\frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

### 3. Run the tests

```powershell
cd enterprise-ai-brain\backend
.\venv\Scripts\Activate.ps1
pytest -v
```

Expect **21 passed**: 7 auth + 9 documents + 5 chat. The chat tests stub out
the LLM call entirely (no API key or network needed to pass) — they check
retrieval, memory, and the endpoint contract, not answer quality. The
document tests still download the embedding model on first run.

## Usage

1. Register / sign in.
2. **Upload** a PDF, DOCX, or TXT file — wait for its status to reach *ready*.
3. Go to **Chat** and ask a question about it. The answer cites the source
   filename(s) it drew on, shown as badges under the reply.
4. Ask a follow-up ("what about the pricing?") — the Retriever Agent
   rewrites it into a standalone query using the last few turns before
   searching, so pronouns and implicit references still resolve.
5. **Clear** wipes your conversation history; deleting a document (on
   Upload) removes it from future answers immediately.

## Screenshots

_Add screenshots of the login, dashboard, upload, and chat pages here once
the UI is running locally — e.g. `docs/screenshots/chat.png`._

## Roadmap

| Phase | Scope |
|---|---|
| 1 ✅ | Repo setup, backend, frontend, authentication |
| 2 ✅ | Document upload, text extraction, chunking, embeddings, FAISS |
| 3 ✅ | Retriever agent, conversation memory, chat interface |
| 4 | Manager, Planning, Analysis, and Report agents (LangGraph) |
| 5 | Dashboard widgets, history, settings, report export |
| 6 | Testing, documentation, cleanup |

## Future scope

Deliberately excluded from this prototype to keep it simple and fully
runnable on a laptop: live web crawling, Slack/Teams/email integrations,
calendar automation, cloud deployment, continuous learning, and enterprise
RBAC. These are natural extensions once the core prototype is solid.

OCR, image analysis, speech recognition, and a knowledge graph appear in the
overall feature list but aren't assigned to any of the six phases — still
flagging that rather than guessing where to slot them in.

## License

MIT — see `LICENSE` (add one before publishing).

## Credits

Built by [your name] as a demonstration of applied multi-agent RAG
architecture.
