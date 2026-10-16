import os
from pathlib import Path
from typing import List

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
ESLINT_CONFIG_PATH = str(BASE_DIR / "eslint.config.mjs")
TEMP_DIR = BASE_DIR / ".temp"

# Ensure isolated temporary scan directory exists
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# File Upload Constraints
MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024  # 2 Megabytes limit
ALLOWED_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
}

# Subprocess Constraints
ANALYSIS_TIMEOUT_SECONDS = 25

# Server Binding Constraints for Deployment (PaaS like Render, Railway, Fly.io, Heroku)
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Security Disclaimer Notice
SECURITY_DISCLAIMER = (
    "Security Notice: Static analysis evaluates source code against predefined heuristic patterns "
    "and known risk rules. Zero detected findings does NOT guarantee that the code is completely secure, "
    "free of logic vulnerabilities, or suitable for production. Always perform defensive input validation "
    "and peer review."
)

# CORS Configuration
# Supports ALLOWED_ORIGINS (comma-separated) or FRONTEND_URL environment variables
DEFAULT_CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

env_origins = os.getenv("ALLOWED_ORIGINS", os.getenv("FRONTEND_URL", "")).strip()
if env_origins:
    CORS_ORIGINS: List[str] = [origin.strip() for origin in env_origins.split(",") if origin.strip()]
    for default_origin in DEFAULT_CORS_ORIGINS:
        if default_origin not in CORS_ORIGINS:
            CORS_ORIGINS.append(default_origin)
else:
    # Default for local development
    CORS_ORIGINS: List[str] = DEFAULT_CORS_ORIGINS + ["*"]
