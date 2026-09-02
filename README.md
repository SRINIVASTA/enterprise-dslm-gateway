# 🔀 Enterprise AI Gateway & Control Plane (Google Gemini Layer)

An advanced, multi-tier AI model orchestration framework built to optimize enterprise workloads, automate in-flight data anonymization, enforce role-based access control (RBAC), and maintain strict session budgetary guardrails.

This architecture addresses a critical corporate challenge: **Scaling agentic AI utility while ensuring absolute data sovereignty, high precision, and predictable, sub-penny cost tracking metrics.**

---

## 🚀 Architectural Business Case & Capabilities

General-purpose, out-of-the-box LLM API requests introduce massive token cost overheads, leak sensitive infrastructure details across corporate boundaries, and fail to respect distinct employee access clearings. 

This project mirrors **Enterprise Architectural Philosophies** (such as the Lyzr AI framework) by providing a completely self-contained, lightweight gateway that wraps requests in strict governance layers prior to execution.

*   **🎯 Telecom MTTR Optimization:** Pre-configured natively to act as an automated network diagnostic engine, translating complex telemetry fault logs (OSS, Open RAN, IMS, LTE) into structured remediation steps in seconds.
*   **🛡️ Zero-Leak Data Governance:** Implements a localized regex-driven scraping layer that purges internal corporate IP addresses from user inputs *before* payloads travel across external network boundaries.
*   **🔌 Smart Network Isolation Fallback:** Features an automated, non-destructive connection handling loop. If the Streamlit Cloud deployment container encounters a DNS blackout or network timeout to the endpoint server, it instantly downgrades to an in-memory **Local Sandbox Simulation Engine** so the user experience never crashes.
*   **👥 State-Aware RBAC Matrix:** Dynamically alters interface controls, validation buttons, and sub-tab privileges based on active metadata profiles (`Administrator`, `Engineer`, `Auditor`).
*   **💳 Budgetary Cost Guardrails:** Tracks continuous query accumulation fees in real-time, enforcing a hard gateway cutoff (e.g., a `$0.05` maximum test ceiling) to prevent runaway cloud provider infrastructure bills.

---

## 📁 System Repository Tree

This project follows a streamlined, production-ready directory schema built and managed entirely within web-native runtime environments (GitHub Web + Streamlit Community Cloud).

```text
enterprise-dslm-gateway/
│
├── .gitignore               # Excludes python bytecode, cache, and system storage files
├── requirements.txt         # Ultra-lightweight package dependencies file
├── app.py                   # Central multi-tier UI orchestrator and control plane
│
├── .streamlit/
│   └── config.toml          # Server-hardening configurations (CORS/XSRF protection blocks)
│
└── scripts/
    ├── data_masker.py       # Localized regular expression string scrubbing module
    └── dataset_uploader.py  # Stream-based private dataset migration handler (Inlined)
```

---

## 🛠️ Lightweight Dependency Strategy (Zero SDK Bloat)

A key design choice in this application is the complete omission of heavy, version-unstable official framework libraries like `google-genai` or `google-generativeai`.

### 📄 `requirements.txt`
```text
streamlit>=1.35.0
requests>=2.31.0
```

### 💡 The FDE Engineering Advantage:
By building the core interaction pipeline using pure Python `requests` structures targeted directly at Google's native REST endpoints (`https://googleapis.com`), this codebase achieves:
1.  **Maximum Portability:** The entire workspace can be dropped instantly into highly restricted, air-gapped corporate sub-servers without requiring extensive package installations.
2.  **Ultra-Fast Container Boot Times:** Streamlit Cloud installs the complete package environment in under 10 seconds, providing an optimal live review loop for technical auditors.
3.  **Immunity to Version Collisions:** Bypasses downstream breaking changes often introduced by rapid third-party SDK updates.

---

## 💻 Technical Code Architecture & Inlining

### 1. In-Flight Privacy Scraper (`scripts/data_masker.py`)
Utilizes compiled regular expressions running locally on the application thread to intercept input strings before prompt payload construction:
*   **Target Scope:** Evaluates character strings via `\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b` to isolate IPv4 metrics.
*   **Action:** Swaps target assets with secure opaque indicators: `[MASKED_IP_ADDRESS]`.

### 2. The UI Control Plane & Fallback State Machine (`app.py`)
Manages authentication inputs via hidden runtime text elements (`type="password"`), preventing keys from being hardcoded or committed to global variables. It maintains persistent session counters (`st.session_state.total_spend`) across page updates and routes strings dynamically depending on network status.

---

## 📊 Live Cloud Execution Trace Journey

1.  **Handshake Triage:** The administrator enters their Google API credential key. The app attempts a 5-second verification ping to the Google models endpoint. If a network block or DNS error occurs, it switches seamlessly to `Sandbox Engine Mode`.
2.  **Scrubbing Evaluation:** The user pastes raw, sensitive telecom error metrics into the terminal interface. The script scrubs the true database network location (`10.145.22.89`) instantaneously.
3.  **Prompt Vector Generation:** The system replaces the `{user_input}` variable inside the enterprise blueprint template with the sanitised data block.
4.  **Telemetry Reporting:** The mock engine executes local text synthesis parsing, metrics calculations, latency profiles (**1.5s** simulation), and updates the financial wallet tracking meter.
