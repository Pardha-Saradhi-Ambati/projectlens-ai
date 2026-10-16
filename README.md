# ProjectLens AI — Student Source-Code Review Platform

**ProjectLens AI** is an AI-assisted source-code review platform built for computer science students and educators. Users can upload individual Python (`.py`) or JavaScript (`.js`) source files to receive automated static analysis findings, understand potential real-world security risks, and view concrete recommendations with before/after code fix patterns.

---

## 🚀 Key Features

* **Instant Static Code Review**: Analyzes single `.py` and `.js` source files with no manual setup.
* **Dual Static Analysis Engines**:
  * **Bandit (Python)**: Identifies security vulnerabilities such as shell injection, hardcoded passwords, unsafe asserts, weak cryptographic hashes, and unconstrained deserialization.
  * **ESLint (JavaScript)**: Flags dangerous patterns like `eval()`, implied evals, loose equality anti-patterns (`==` vs `===`), undeclared global variables, and unused code.
* **Educational Student Guidance**: Translates cryptic linter outputs into plain-English explanations of *why* an issue matters, what the concrete risk is, and how to fix it defensively.
* **Findings Severity Breakdown**: Real-time interactive summary cards for **High**, **Medium**, and **Low** severity issues that double as filter toggles.
* **1-Click Pre-Configured Samples**: Test the platform immediately with bundled student scenarios (vulnerable and hardened patterns for both Python and JavaScript).
* **Responsible Security Messaging**: Prominently highlights that 0 static findings do not constitute a guarantee of complete code security.

---

## 🛡️ Security Architecture & Non-Negotiable Guarantees

1. **Zero Code Execution**: Uploaded source code is **never** executed, imported, or dynamically evaluated.
2. **Subprocess Isolation**: Analysis engines are invoked in strictly isolated subprocesses with arguments passed as explicit string lists (`shell=False`).
3. **Execution Timeouts**: A hard timeout of 25 seconds is enforced on all subprocess runs.
4. **File Validation & Quotas**: 
   * Strict extension whitelist (`.py`, `.js`).
   * Maximum file size limit of 2MB (rejects oversized payloads with `HTTP 413 Content Too Large`).
   * Rejects empty 0-byte uploads with `HTTP 400 Bad Request`.
5. **Isolated Temporary Storage**: Uploads are written to a dedicated, managed directory (`backend/.temp/`) and immediately unlinked in a `finally:` block.
6. **No False Guarantees**: A clean scan with 0 issues explicitly displays a responsible security disclaimer noting that static analysis flags heuristic patterns and cannot guarantee immunity against runtime defects or business logic bugs.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React 19, Vite, Tailwind CSS v4 | Responsive, interactive student dashboard |
| **Icons** | Lucide React | Modern visual status & navigation indicators |
| **Backend** | Python 3.13, FastAPI, Uvicorn, Pydantic v2 | High-performance asynchronous REST API |
| **Python Analysis** | Bandit 1.9+ | AST-based security vulnerability scanner |
| **JavaScript Analysis** | ESLint 10+ (Flat Config) | Syntax and static rule linting engine |
| **HTTP Communication** | Native `Fetch` API | Lightweight client-server communication |

---

## 📂 Project Architecture

```
projectLens-AI/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app, endpoints (/health, /analyze, /samples), CORS
│   │   ├── config.py                # Server binding, CORS, quotas, temp directory paths
│   │   ├── models.py                # Pydantic schemas (Finding, SeveritySummary, AnalysisResponse)
│   │   ├── recommendation_engine.py # Educational risk breakdown & fix pattern knowledge base
│   │   └── analyzers/
│   │       ├── __init__.py
│   │       ├── base.py              # BaseAnalyzer abstract interface
│   │       ├── python_analyzer.py   # Bandit subprocess execution & result parser
│   │       └── js_analyzer.py       # ESLint subprocess execution & result parser
│   ├── eslint.config.mjs            # Curated ESLint flat config with security & quality rules
│   ├── test_samples/                # Preloaded sample files for instant test reviews
│   │   ├── insecure_sample.py       # Shell injection, hardcoded credentials, weak hashes
│   │   ├── clean_sample.py          # Clean math grading utility with zero findings
│   │   ├── insecure_sample.js       # Eval usage, loose equality, undeclared variables
│   │   └── clean_sample.js          # Strictly typed mathematical helper
│   ├── test_backend_api.py          # Automated test suite verifying all 7 backend endpoints
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Backend environment variable template
│   ├── Dockerfile                   # Isolated container build for backend
│   └── run.py                       # Standalone runner script
├── frontend/
│   ├── src/
│   │   ├── App.jsx                  # Main dashboard controller with filtering & search
│   │   ├── index.css                # Tailwind CSS v4 setup and slate design theme
│   │   ├── components/
│   │   │   ├── Navbar.jsx           # Header with real-time Bandit/ESLint engine status
│   │   │   ├── FileUploader.jsx     # Drag & drop upload zone with code preview & review trigger
│   │   │   ├── SeveritySummary.jsx  # Severity count cards (Total, High, Medium, Low) & filters
│   │   │   ├── FindingCard.jsx      # Diagnostic cards with risk breakdown & fix examples
│   │   │   ├── SampleCodeSelector.jsx # 1-click educational sample loaders
│   │   │   ├── SecurityDisclaimer.jsx # Responsible security advisory banner
│   │   │   ├── EmptyResultState.jsx # Zero-findings positive state with disclaimer
│   │   │   └── ErrorAlert.jsx       # Diagnostic error state with retry
│   │   └── utils/
│   │       └── api.js               # Fetch API wrappers with VITE_API_BASE_URL support
│   ├── package.json
│   ├── vite.config.js               # Vite config with Tailwind and backend proxy
│   ├── .env.example                 # Frontend environment variable template
│   └── index.html
├── .gitignore                       # Comprehensive root ignore rules
├── Dockerfile                       # Multi-runtime production container specification
└── README.md
```

---

## 💻 Local Installation & Setup

### Prerequisites

* **Python 3.10+** (Python 3.13 recommended)
* **Node.js 18+** & **npm** (for ESLint and Vite frontend)

---

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd projectLens-AI
```

---

### Step 2: Backend Setup

Open a terminal and navigate to `backend/`:

```bash
cd backend

# Create and activate a virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
# source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Start the FastAPI server
python run.py
# Alternatively:
# python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

* **API Base**: `http://127.0.0.1:8000`
* **Health Check**: `http://127.0.0.1:8000/api/health`
* **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`

---

### Step 3: Frontend Setup

Open a separate terminal and navigate to `frontend/`:

```bash
cd frontend

# Install npm dependencies
npm install

# Start the Vite development server
npm run dev
```

* **Frontend Dashboard**: `http://127.0.0.1:5173`

---

## 🧪 Testing

### Automated Backend Verification Suite

Run the automated integration tests verifying health checks, Python Bandit scans, JavaScript ESLint scans, clean 0-issue handling, extension rejections, empty file rejections, and 2MB payload limits:

```bash
python backend/test_backend_api.py
```

Expected output:
```text
=== Testing ProjectLens AI FastAPI Backend Endpoints ===
[PASS] Health Check Endpoint (GET /api/health)
[PASS] Python File Upload & Bandit Analysis (POST /api/analyze)
[PASS] JavaScript File Upload & ESLint Analysis (POST /api/analyze)
[PASS] Clean Code Upload (0 Findings handling)
[PASS] Reject Unsupported File Extension (.txt)
[PASS] Reject Empty File (0 bytes)
[PASS] Reject File Exceeding Size Limit (>2MB)
=== All Tests Completed ===
```

---

## 🚢 Deployment Considerations

### 1. Dual-Runtime Backend Requirement
Because ProjectLens AI performs static analysis on both Python and JavaScript files:
* The backend execution environment **must** have both **Python 3.10+** and **Node.js 18+ (with npm/npx)** installed.
* **Bandit** runs via Python.
* **ESLint** runs via Node (`npx` or `eslint` binary).
* **Docker Deployment (Recommended)**: Use the provided [Dockerfile](file:///c:/Users/HP/OneDrive/Documents/projectLens-AI/Dockerfile). It uses `python:3.13-slim` and installs `nodejs` and global `eslint`, ensuring both engines are ready out-of-the-box.
* **PaaS Buildpacks (e.g., Heroku, Render, Railway)**: If deploying without Docker, add both the **Node.js** buildpack and the **Python** buildpack to your project settings.

### 2. Environment Variables

#### Backend Environment Variables
| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `PORT` | `8000` | Port provided by hosting provider (Render, Railway, Fly.io, Heroku) |
| `HOST` | `0.0.0.0` | Host binding for cloud container/VM |
| `ALLOWED_ORIGINS` | `http://localhost:5173,...` | Comma-separated list of allowed frontend domains for CORS |
| `FRONTEND_URL` | *(optional)* | Single deployed frontend domain (e.g. `https://projectlens.vercel.app`) |

#### Frontend Environment Variables
| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `VITE_API_BASE_URL` | *(empty / proxied)* | Deployed backend URL (e.g. `https://projectlens-api.onrender.com`). In production, the client will send requests to this host without referencing localhost. |

---

## 🔒 Security Disclaimer

Static code analysis uses heuristic rules and Abstract Syntax Tree (AST) pattern matching to flag potential issues and common anti-patterns. **Zero reported findings does NOT guarantee that code is 100% secure, bug-free, or production-ready.** Dynamic runtime conditions, business logic flaws, and complex environment configurations cannot be determined solely by static analyzers. Always supplement automated static reviews with defensive input validation, least-privilege configurations, and peer review.
