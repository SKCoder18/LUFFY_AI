# LUFFY AI Engineering Standards

## 1. Project Structure Standards
- **Folder organization:** Maintain clean separation of concerns. The frontend (Electron/React) and backend (Python API) must live in distinct directories (e.g., `/frontend`, `/backend`). Internal structures must be organized by domain (e.g., `/backend/core`, `/backend/modules/voice`, `/frontend/src/components`).
- **Module responsibilities:** Each module must have a single responsibility. The voice module must only handle audio streaming and transcription; it should not process conversational logic.
- **Import rules:** Avoid circular dependencies strictly. In Python, use absolute imports for clarity. Relative imports are only permitted within tightly coupled packages.
- **Dependency rules:** All dependencies must be strictly version-pinned (e.g., `requirements.txt` for Python, `package.json` for Node.js). Only production-grade, community-audited libraries are allowed.

## 2. Coding Standards
- **Python conventions:** Adhere to PEP 8 guidelines. Use `black` for automatic code formatting and `flake8` or `ruff` for linting.
- **TypeScript conventions:** Enable strict mode (`"strict": true` in `tsconfig.json`). Use `eslint` and `prettier` for linting and formatting. The use of the `any` type is strictly forbidden.
- **Naming conventions:**
  - *Python:* `snake_case` for variables and functions, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.
  - *TypeScript:* `camelCase` for variables and functions, `PascalCase` for classes and interfaces/types.
- **Type hints:** Mandatory in both languages. Python functions must have explicit argument and return type hints.
- **Documentation/comments:** Use docstrings for all public classes, methods, and modules. Google-style docstrings are preferred for Python; standard JSDoc for TypeScript. Inline comments should explain "why", not "what".
- **File organization:** Keep files focused and under 500 lines where possible. Export only necessary interfaces.

## 3. Architecture Rules
- **Single Responsibility Principle (SRP):** Classes, functions, and modules must do one thing well.
- **Modular design:** Subsystems (AI Core, Voice, Vision) must be decoupled. They should communicate via defined interfaces or events, not direct cross-module state manipulation.
- **No circular imports:** Strict enforcement to prevent initialization errors and tight coupling.
- **Dependency injection:** Inject dependencies where appropriate (e.g., passing a database connection interface into the Memory engine) to facilitate easier mock testing.
- **Configuration management:** All configurations must be centralized (e.g., in a `.env` file or structured `config.json`).
- **No hardcoded values:** Magic numbers, paths, and API endpoints must be defined in configuration or constant modules.

## 4. Logging Standards
- **Log levels:** 
  - `DEBUG` (development details)
  - `INFO` (general flow, startup/shutdown)
  - `WARNING` (recoverable issues)
  - `ERROR` (exceptions, operation failures)
  - `CRITICAL` (fatal application crashes)
- **Log format:** Logs should be JSON formatted for easy machine parsing, including fields for timestamp, log level, module name, message, and trace (if applicable).
- **Error logging:** Must capture and log stack traces for all `ERROR` and `CRITICAL` events.
- **Performance logging:** Core transactions (e.g., "LLM generation time", "STT latency") must log their execution duration.
- **Telemetry events:** Anonymous feature usage events must be logged locally to aid in debugging, governed strictly by user opt-in settings.

## 5. Error Handling Standards
- **Exception hierarchy:** Use custom, domain-specific exceptions (e.g., `LuffyVoiceError`, `LuffyMemoryError`) instead of generic base exceptions.
- **Recovery strategy:** Catch exceptions at architectural boundaries (e.g., the API route layer or IPC handler). A subsystem failure must never crash the main application process.
- **Retry policy:** Implement exponential backoff for transient failures (e.g., connecting to the local Ollama server).
- **Graceful degradation:** If a non-critical subsystem fails (e.g., the Vision model fails to load), the rest of the application must continue to function (e.g., reverting to text/voice only).
- **User-friendly error messages:** Never expose raw stack traces to the UI. Display clear, actionable, and non-technical error alerts to the user.

## 6. Performance Budget
Define measurable performance limits. These targets must be used throughout development.
- **Startup time:** ≤ 2 seconds
- **Idle CPU:** ≤ 3%
- **Idle RAM:** ≤ 400 MB (excluding Ollama footprint)
- **Wake word detection:** ≤ 300 ms
- **First AI token (latency):** ≤ 1.5 seconds
- **Voice interruption latency:** ≤ 200 ms
- **Screen capture latency:** ≤ 500 ms
- **Tool execution:** ≤ 2 seconds

## 7. Security Standards
- **Local-first architecture:** Processing happens locally. Cloud capabilities are strictly opt-in and off by default.
- **Encryption rules:** Sensitive data (such as optional Cloud API keys) must be encrypted at rest using OS-level secure storage (e.g., Windows Credential Manager).
- **Permission management:** Strict enforcement of the internal Permissions System before executing any tool or capturing data (Microphone, Screen, Automation).
- **Secure storage:** Local SQLite database files must be protected with appropriate restrictive file permissions.
- **Command validation:** All system commands executed by LUFFY (via the Tool Engine) must be heavily sanitized and validated against a safelist.
- **Safe automation execution:** Destructive or highly consequential actions (e.g., file deletion, sending an email) require explicit user confirmation before execution.

## 8. Testing Standards
- **Unit tests:** High test coverage required for core business logic, utilizing `pytest` (Python) and `jest`/`vitest` (TypeScript).
- **Integration tests:** Must verify the interactions between independent modules (e.g., the AI Core querying the Memory system).
- **Manual testing checklist:** Verify OS-level integrations (global shortcuts, wake word detection, window overlays) that cannot be easily mocked.
- **Acceptance testing for every phase:** A phase is not complete until all its defined acceptance tests pass successfully.
- **Regression testing:** The full automated test suite must run and pass before any code is merged into the main branch.

## 9. Git Workflow
- **Branch strategy:** 
  - `main`: Production-ready code.
  - `develop`: Integration branch for ongoing work.
  - `feature/*`: New features (e.g., `feature/voice-engine`).
  - `bugfix/*`: Bug fixes.
- **Commit message format:** Follow Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`).
- **Versioning:** Semantic Versioning (SemVer) format (MAJOR.MINOR.PATCH).
- **Pull request checklist:** PRs must pass CI (linting, type checking, tests) and include peer review prior to merging.

## 10. UI/UX Standards
- **Design language:** Premium Glassmorphism, Modern Dark Theme. Interfaces must feel native and high-end.
- **Animation guidelines:** Smooth, easing transitions (e.g., using Framer Motion). Target 60fps. Avoid jarring jumps or flashes.
- **Typography:** Premium, readable sans-serif fonts (e.g., Inter or Roboto). Clear visual hierarchy.
- **Colors:** Deep obsidian/dark backgrounds accented with vibrant, neon highlights for active states.
- **Accessibility:** Ensure keyboard navigability, screen reader support, scalable text, and high contrast ratios.
- **Responsive behavior:** The UI must adapt gracefully when resized, snapped to the edge, or minimized to the mini-overlay.
- **Loading states:** Utilize skeleton loaders and subtle pulsing animations rather than intrusive blocking spinners.
- **Error states:** Provide contextual retry buttons and clear, calm explanations of what went wrong.

## 11. Project Rules
These are mandatory engineering rules that every future phase must strictly follow:
- No implementation outside the current phase.
- No feature creep.
- One objective per phase.
- Every feature must have acceptance tests.
- Every bug fix must include a root cause analysis.
- No temporary hacks.
- Documentation must be updated before architectural changes.

## 13. Definition of Done
Every phase is complete only when:
- All acceptance tests pass.
- No critical bugs remain.
- No placeholder or TODO code remains.
- Documentation is updated.
- Verification Report is completed.
- Manual testing passes.
- Performance targets are achieved.

## 12. Verification Report Template
Every development phase must end with a formal Verification Report. No phase should continue into the next one until this report is completed and reviewed.

**Report Format:**
- **Phase Name:** 
- **Objective:** 
- **Files Modified:** 
- **Components Modified:** 
- **Acceptance Tests Performed:** 
- **Test Results:** 
- **Performance Measurements:** 
- **Known Issues:** 
- **Risks:** 
- **Dependencies for the Next Phase:** 
- **Final Status:** [Pass / Fail]
