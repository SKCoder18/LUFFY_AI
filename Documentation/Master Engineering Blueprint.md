# LUFFY AI 2.0 - Master Engineering Blueprint

## 1. Product Vision

LUFFY is **NOT** another ChatGPT desktop app wrapper.

LUFFY is a premium **Windows AI Operating Assistant**. Its primary goal is to become an intelligent desktop companion that can naturally communicate, deeply understand the desktop environment, perform local tasks autonomously, remember contextual information over time, and automate workflows. 

The assistant must feel like a native, intrinsic part of the Windows OS rather than just another chatbot application installed on the side.

---

## 2. Core Principles

The development of LUFFY AI 2.0 is guided strictly by the following core principles:

*   **Offline-First:** The primary modes of operation must function without an internet connection.
*   **Privacy-First:** User data, conversation history, and desktop context never leave the local machine unless explicitly routed to a configured cloud provider by the user.
*   **Local AI by Default:** Powered by local models (e.g., Ollama) acting as the primary brain.
*   **Cloud APIs Optional:** Cloud providers are strictly optional. They must *never* be required for normal usage.
*   **Premium UI/UX:** The interface must be stunning, responsive, and seamlessly integrated into the Windows desktop environment.
*   **Fast Response:** Optimized for low latency, especially for voice and tool execution.
*   **Natural Conversation:** Interactions should feel fluid, human-like, and contextually aware.
*   **Stable Architecture:** Built on robust, proven technologies capable of handling long-running background processes.
*   **Modular Design:** Every system (Voice, Vision, Tools, Memory) must be decoupled and independently testable.
*   **Production-Ready:** Code quality, error handling, and security must reflect enterprise-grade software.

---

## 3. Technology Stack & Framework

### Desktop Framework: Electron
**Electron** is the chosen framework for the desktop shell.
*Reasoning:* LUFFY requires deep OS integration that Electron's mature ecosystem provides reliably:
*   Global shortcuts (registration and listening)
*   Screen capture APIs
*   Microphone and audio stream access (for Wake Word and Voice)
*   System notifications and tray integration
*   Advanced window management (transparency, always-on-top, click-through)
*   Auto-start on boot
*   Desktop overlays (Floating Orb, Mini Overlay)
*   Direct bindings to native Windows APIs.

### Backend Services & AI Core
*   **Backend:** Python (FastAPI/Local Microservices) for AI orchestration, memory management, and OS automation scripts.
*   **Local AI Engine:** Ollama (defaulting to `llama3.2:3b`).

---

## 4. System Architecture

The architecture is divided into specialized, single-responsibility subsystems.

### 4.1. AI Core
The brain of LUFFY, replacing the monolithic orchestrator. It consists of independent modules:
*   **Intent Engine:** Analyzes user input (text or transcribed voice) to determine the goal (e.g., casual chat, tool execution, memory retrieval).
*   **Memory Engine:** Interfaces with the Memory System to inject relevant context into the prompt before generation.
*   **Reasoning Engine:** Manages complex, multi-step tasks. Decides when to break down a request and coordinates the sequence of actions.
*   **Provider Engine:** An abstraction layer managing LLM interactions. Defaults to Ollama, but capable of routing to optional cloud APIs if configured.
*   **Tool Engine:** Resolves intents into concrete tool executions (e.g., triggering a desktop automation script) and feeds the result back to the Reasoning Engine.

### 4.2. Memory System
Separated into three distinct, hierarchical layers:
*   **Short-Term Memory:** Tracks the immediate context of the current active session or conversation thread. Extremely fast, stored in RAM or lightweight cache.
*   **Long-Term Memory:** Semantic memory of past conversations, user preferences, and historical context. Stored in a local **Vector Database** (e.g., ChromaDB or Qdrant).
*   **Knowledge Memory:** Structured, explicit facts and settings (e.g., "User's name is John", "User prefers dark mode"). Stored in a local **SQLite** database.

### 4.3. Voice System
A fully independent subsystem composed of dedicated modules:
*   **Wake Word Engine:** Continuously listens for the trigger phrase locally with minimal CPU overhead.
*   **Speech Recognition (STT):** High-accuracy local transcription (e.g., Whisper).
*   **Conversation Engine:** Manages the back-and-forth dialogue pacing and turn-taking.
*   **Text To Speech (TTS):** Generates natural-sounding voice responses locally.
*   **Microphone Control:** Manages audio input device streams.
*   **Echo Prevention:** Ensures the assistant *never* listens to its own TTS output.
*   **Interrupt Handling:** Detects when the user speaks over the assistant and immediately halts the current TTS output and AI generation.
*   **Voice Streaming:** Processes audio in chunks for near-instantaneous STT and TTS playback.

### 4.4. Vision System
An independent subsystem providing LUFFY with eyes on the OS:
*   **Screenshot Understanding:** Capturing and analyzing the entire active display.
*   **OCR (Optical Character Recognition):** Extracting text from images or unselectable UI elements.
*   **UI Understanding:** Parsing the structure of active windows to understand context (e.g., recognizing buttons, input fields).
*   **Image Understanding:** Analyzing specific image files provided by the user.
*   **Window Recognition:** Identifying which application is currently in focus.
*   **Clipboard Image Analysis:** Automatically processing images copied to the clipboard if requested.

### 4.5. Desktop Tools (Tool System)
Independent, modular tools that the AI Core can invoke to perform actions.
*   **Browser:** Web search and page reading.
*   **File Explorer:** File creation, deletion, moving, and searching.
*   **VS Code:** Project management, code reading/writing.
*   **Terminal:** Executing shell commands.
*   **Calculator:** Performing precise math operations.
*   **Clipboard:** Reading from and writing to the system clipboard.
*   **Windows Settings:** Toggling OS settings (Wi-Fi, Bluetooth, Volume, Theme).
*   **Email:** Drafting and reading local email clients.
*   **WhatsApp:** Interacting with the WhatsApp desktop app.
*   **Spotify:** Media control (play, pause, skip, search).

### 4.6. Permissions System
A dedicated security layer managing what LUFFY is allowed to do.
*   **Microphone:** Access to listen.
*   **Camera:** Access to webcam (if needed for vision).
*   **Screen Capture:** Permission to read the screen.
*   **Automation:** Permission to simulate keyboard/mouse and execute commands.
*   **Notifications:** Permission to send OS-level alerts.
*   **Accessibility:** Deep OS hooks for window management.

### 4.7. System Manager Subsystem
Monitors the health and lifecycle of the entire application to ensure self-healing and high reliability.
*   **Health Monitor:** Continuously monitors every subsystem (AI, Voice, Vision, Memory, Tools) and the AI provider status.
*   **Service Manager:** Detects crashes or unexpected failures and restarts *only* the failed subsystem. Never restarts the whole application unless absolutely required.
*   **Performance Monitor:** Tracks CPU usage, RAM usage, and active threads in real-time.
*   **Crash Recovery:** Implements graceful recovery protocols for catastrophic failures.
*   **Diagnostics:** Generates structured diagnostic logs to aid in debugging.

---

## 5. UI/UX & Personality

### 5.1. Personality Profile
LUFFY's persona is defined by the following traits:
*   **Professional:** Respectful and competent.
*   **Friendly:** Approachable but not overly casual.
*   **Natural:** Conversational, avoiding rigid syntax.
*   **Confident:** Direct and clear in its answers.
*   **Concise:** Gets straight to the point without unnecessary filler.
*   **Never Robotic:** Avoids typical AI disclaimers (e.g., "As an AI...").
*   **Never Repetitive:** Varies greetings, acknowledgments, and conversational structures.

### 5.2. Premium UI Design
The UI must feel like premium desktop software, featuring **Glassmorphism**, a **Modern Dark Theme**, and **Smooth Animations**.
*   **Floating Orb:** A persistent, unobtrusive desktop widget representing LUFFY's presence.
*   **Sidebar:** A collapsible panel for quick interactions.
*   **Full Dashboard:** The main hub for deep work, settings, and complex chats.
*   **Mini Overlay:** A spotlight-like search/command bar.
*   **Voice Wave Animation:** A dynamic, fluid visualizer active during speaking/listening.
*   **Screen Overlay:** Subtle indicators when LUFFY is analyzing the screen.
*   **Notifications:** Custom, sleek toast notifications.

---

## 6. Development Roadmap

The project is broken down into 12 highly focused phases. Each phase builds upon the previous one.

### Phase 1: Architecture & Foundation
*   **Objective:** Establish the project scaffolding and core communication bridge.
*   **Scope:** Electron setup, Python backend setup, IPC/WebSocket bridge, basic folder structure.
*   **Deliverables:** A running Electron app that successfully communicates with a local Python FastAPI server.
*   **Acceptance Tests:** App launches. "Ping" sent from React triggers a "Pong" from Python visible in the UI.
*   **Dependencies:** None.
*   **Review Checkpoint:** Confirm IPC stability and process lifecycle management (Electron killing Python on exit).

### Phase 2: Premium UI
*   **Objective:** Implement the visual identity and core UI components.
*   **Scope:** Theming (Glassmorphism, Dark mode), Dashboard layout, Floating Orb, Mini Overlay, global shortcuts to toggle UI.
*   **Deliverables:** Fully styled, responsive UI shell without backend logic.
*   **Acceptance Tests:** UI matches design specs. Global shortcut `Alt+Space` opens the Mini Overlay. Floating Orb can be dragged.
*   **Dependencies:** Phase 1.
*   **Review Checkpoint:** UI/UX aesthetic review and animation smoothness check.

### Phase 3: Backend Core
*   **Objective:** Build the internal AI orchestration engine.
*   **Scope:** Intent Engine, Reasoning Engine, Provider Engine (Ollama integration).
*   **Deliverables:** Modular Python backend capable of receiving a prompt, routing it to Ollama, and streaming the response.
*   **Acceptance Tests:** API endpoints can receive a prompt and stream a response back from `llama3.2:3b`.
*   **Dependencies:** Phase 1.
*   **Review Checkpoint:** Engine modularity and Ollama latency benchmarking.

### Phase 4: Chat
*   **Objective:** Connect the UI to the AI Core for text-based interaction.
*   **Scope:** Chat UI, message rendering (Markdown/Code blocks), token streaming, conversation state management.
*   **Deliverables:** A fully functional text-based chat interface.
*   **Acceptance Tests:** User can type a message in the Dashboard, see streaming responses, and view properly formatted code.
*   **Dependencies:** Phase 2, Phase 3.
*   **Review Checkpoint:** Streaming performance and UI responsiveness during generation.

### Phase 5: Memory
*   **Objective:** Implement Short, Long, and Knowledge memory systems.
*   **Scope:** SQLite integration, Vector DB (ChromaDB) setup, RAG implementation in the AI Core.
*   **Deliverables:** AI that remembers context across sessions and restarts.
*   **Acceptance Tests:** Tell LUFFY a fact. Restart the app. Ask LUFFY about the fact, and it retrieves it from the Vector DB.
*   **Dependencies:** Phase 4.
*   **Review Checkpoint:** Memory retrieval accuracy and impact on prompt latency.

### Phase 6: Voice
*   **Objective:** Implement hands-free audio interaction.
*   **Scope:** Wake Word, STT (Whisper), TTS (Piper), Echo Prevention, Interrupt Handling, Voice UI Visualizer.
*   **Deliverables:** Full duplex voice conversation capabilities.
*   **Acceptance Tests:** User says wake word, asks a question, LUFFY responds with voice. User speaks while LUFFY is talking, LUFFY stops immediately and listens.
*   **Dependencies:** Phase 4.
*   **Review Checkpoint:** Audio latency, STT accuracy, and interrupt reliability.

### Phase 7: Desktop Tools
*   **Objective:** Implement the modular Tool Engine and core desktop tools.
*   **Scope:** Tool Engine framework, File Explorer tool, Terminal tool, Browser tool, Clipboard tool.
*   **Deliverables:** LUFFY can execute function calls to perform actual OS tasks.
*   **Acceptance Tests:** Prompt "Create a folder named test on my desktop". LUFFY creates the folder autonomously.
*   **Dependencies:** Phase 3.
*   **Review Checkpoint:** Tool execution security and reliability.

### Phase 8: Vision
*   **Objective:** Give LUFFY the ability to analyze the screen.
*   **Scope:** Screen capture API in Electron, OCR integration, Vision model (LLaVA) integration in AI Core.
*   **Deliverables:** Screen context awareness.
*   **Acceptance Tests:** Prompt "What is on my screen?". LUFFY captures the screen, processes it, and accurately describes the active window.
*   **Dependencies:** Phase 3.
*   **Review Checkpoint:** Capture performance and Vision model resource usage.

### Phase 9: Automation
*   **Objective:** Enable complex workflows and system-level control.
*   **Scope:** Windows API integration, VS Code tool, WhatsApp/Spotify integration, macro execution.
*   **Deliverables:** Advanced desktop automation capabilities.
*   **Acceptance Tests:** Prompt "Play my discover weekly on Spotify". LUFFY interacts with the Spotify app to start playback.
*   **Dependencies:** Phase 7, Phase 8.
*   **Review Checkpoint:** Reliability of UI automation and error handling for missing apps.

### Phase 10: Settings
*   **Objective:** Build the Permissions System and user configuration layer.
*   **Scope:** Settings UI, Permissions UI, Model selection, Voice profile selection, optional Cloud API key management.
*   **Deliverables:** A robust settings dashboard where the user controls LUFFY's bounds.
*   **Acceptance Tests:** User can revoke Automation permissions. Subsequent automation requests by the AI are blocked and explained to the user.
*   **Dependencies:** Phase 2.
*   **Review Checkpoint:** Security audit of permission enforcement.

### Phase 11: Optimization
*   **Objective:** Polish the application for production release.
*   **Scope:** Resource profiling (RAM/CPU), startup time optimization, database indexing, UI rendering optimization.
*   **Deliverables:** A highly performant, stable application.
*   **Acceptance Tests:** Application idles at < X MB RAM (excluding Ollama). Startup time is < 2 seconds.
*   **Dependencies:** Phases 1-10.
*   **Review Checkpoint:** Final performance metrics review.

### Phase 12: Production Release
*   **Objective:** Package and distribute LUFFY AI 2.0.
*   **Scope:** Electron builder configuration, PyInstaller configuration, code signing, auto-updater implementation.
*   **Deliverables:** An `.exe` installer for Windows.
*   **Acceptance Tests:** Clean install on a fresh Windows machine works flawlessly.
*   **Dependencies:** Phase 11.
*   **Review Checkpoint:** Final QA testing.
