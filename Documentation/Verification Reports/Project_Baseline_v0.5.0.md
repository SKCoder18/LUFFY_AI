# Project Baseline
**Version**: v0.5.0  
**Date**: July 2026

## 1. Completed Phases
- **Phase 1**: Scaffolding (COMPLETED)
- **Phase 2**: Design Language (COMPLETED)
- **Phase 3**: Backend Core (COMPLETED)
- **Phase 4**: Chat (COMPLETED)
- **Phase 5**: Memory (COMPLETED)

## 2. Current Architecture Summary
LUFFY AI is a desktop application utilizing an Electron/React frontend and a FastAPI backend, enabling privacy-first local AI inference.

- **Frontend (Electron/React/Vite)**: Provides the user interface featuring the Kinetic Obsidian design system. State is managed via Zustand. Communicates with the backend using REST APIs for chat and health monitoring.
- **Backend (FastAPI)**: Serves as the core logic engine. It interacts with the local Ollama provider for LLM generation and embedding.
- **Memory System**: Implements a complete RAG (Retrieval-Augmented Generation) pipeline. It uses SQLite for storing conversation metadata, relationships, and duplicate handling, while ChromaDB is utilized for vector persistence. A background task queue ensures that heavy embedding operations do not block the chat streaming pipeline.

## 3. Technologies Used
- **Frontend**: Electron, React, TypeScript, Vite, Tailwind CSS, Zustand, Lucide React.
- **Backend**: Python, FastAPI, Uvicorn, httpx, aiosqlite, ChromaDB.
- **AI/LLM Provider**: Ollama (`llama3.2:3b` for chat, `nomic-embed-text` for embeddings).

## 4. Known Limitations
- **Time To First Token (TTFT)**: Currently ranges approximately 12–15 seconds during local Ollama generation on certain hardware setups. This is accepted for now, and optimization is deferred to Phase 11.
- *(Note: The previous `/api/embeddings` limitation was fully resolved in Phase 5 by swapping the embedding model to `nomic-embed-text`.)*

## 5. Directory Structure
```text
Source Code/
├── backend
│   ├── api
│   │   ├── chat.py
│   │   ├── health.py
│   │   └── routes.py
│   ├── config
│   │   └── settings.py
│   ├── core
│   │   ├── intent_engine.py
│   │   ├── logger.py
│   │   ├── memory
│   │   │   ├── chroma_store.py
│   │   │   ├── cleanup.py
│   │   │   ├── conversation_manager.py
│   │   │   ├── embedding_provider.py
│   │   │   ├── extractor.py
│   │   │   ├── manager.py
│   │   │   ├── queue.py
│   │   │   ├── search_api.py
│   │   │   └── sqlite_store.py
│   │   ├── provider_engine.py
│   │   ├── rag
│   │   │   ├── prompt_builder.py
│   │   │   └── retriever.py
│   │   └── reasoning_engine.py
│   ├── main.py
│   ├── providers
│   │   └── ollama.py
│   ├── requirements.txt
│   └── schemas
│       └── chat.py
├── data
│   └── luffy_memory.sqlite
└── frontend
    ├── .gitignore
    ├── .oxlintrc.json
    ├── README.md
    ├── index.html
    ├── package-lock.json
    ├── package.json
    ├── public
    │   ├── favicon.svg
    │   └── icons.svg
    ├── src
    │   ├── App.css
    │   ├── App.tsx
    │   ├── assets
    │   │   ├── hero.png
    │   │   ├── react.svg
    │   │   └── vite.svg
    │   ├── components
    │   │   ├── ChatBubble.tsx
    │   │   ├── ChatPage.tsx
    │   │   ├── ConnectionIndicator.tsx
    │   │   ├── Layout.tsx
    │   │   ├── MarkdownRenderer.tsx
    │   │   └── SpecialWindows.tsx
    │   ├── index.css
    │   ├── main.tsx
    │   ├── pages
    │   │   └── PlaceholderPages.tsx
    │   ├── services
    │   │   └── ChatService.ts
    │   └── stores
    │       └── useChatStore.ts
    ├── tsconfig.app.json
    ├── tsconfig.json
    ├── tsconfig.node.json
    └── vite.config.ts
```
