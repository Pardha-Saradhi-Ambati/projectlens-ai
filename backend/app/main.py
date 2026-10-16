import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_BYTES,
    SECURITY_DISCLAIMER,
    CORS_ORIGINS,
    TEMP_DIR,
    HOST,
    PORT
)
from app.models import (
    AnalysisResponse,
    HealthResponse,
    ToolStatus,
    SampleItem
)
from app.analyzers.python_analyzer import PythonBanditAnalyzer
from app.analyzers.js_analyzer import JavaScriptESLintAnalyzer

app = FastAPI(
    title="ProjectLens AI - Code Review Engine",
    description="Static-analysis code review platform for students learning secure programming.",
    version="1.0.0"
)

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate analyzers
python_analyzer = PythonBanditAnalyzer()
js_analyzer = JavaScriptESLintAnalyzer()

# Preloaded Educational Sample Code for Instant Testing
SAMPLE_CODES: List[SampleItem] = [
    SampleItem(
        id="py-vulnerable",
        title="Python: Common Security Flaws",
        language="python",
        filename="student_service_vulnerable.py",
        description="Demonstrates hardcoded credentials, command injection via os.system, and unsafe assert statements.",
        code="""import os
import hashlib

# Educational demonstration of risky student code
DATABASE_PASSWORD = "my_secret_production_password_2026"

def authenticate_and_backup(user_id, backup_path):
    # Risky assert that is stripped in production (B101)
    assert user_id > 0, "Invalid student identifier"
    
    # Insecure MD5 hash calculation (B303)
    user_hash = hashlib.md5(str(user_id).encode()).hexdigest()
    
    # Severe Command Injection vulnerability via shell=True (B605)
    print(f"Creating backup for user {user_hash}")
    os.system("tar -czf /tmp/backup.tar.gz " + backup_path)
    
    return True
"""
    ),
    SampleItem(
        id="py-clean",
        title="Python: Hardened & Secure Pattern",
        language="python",
        filename="student_service_clean.py",
        description="Demonstrates strict typing, defensive input boundary checks, and safe mathematical evaluation without risky calls.",
        code="""def calculate_student_grade(scores: list[float], bonus_points: float = 0.0) -> dict:
    \"\"\"
    Computes weighted average and letter grade for a student.
    Follows secure coding standards with defensive validation.
    \"\"\"
    if not isinstance(scores, list) or len(scores) == 0:
        raise ValueError("Scores list must not be empty")

    for score in scores:
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            raise ValueError(f"Invalid score value: {score}. Must be between 0 and 100.")

    average = sum(scores) / len(scores) + max(0.0, bonus_points)
    
    if average >= 90.0:
        grade = "A"
    elif average >= 80.0:
        grade = "B"
    elif average >= 70.0:
        grade = "C"
    elif average >= 60.0:
        grade = "D"
    else:
        grade = "F"

    return {
        "average": round(average, 2),
        "letter_grade": grade,
        "total_assessments": len(scores)
    }
"""
    ),
    SampleItem(
        id="js-vulnerable",
        title="JavaScript: Eval & Type Coercion Flaws",
        language="javascript",
        filename="student_calculator_vulnerable.js",
        description="Demonstrates dangerous eval() usage, undeclared variables, loose equality, and debugger statements.",
        code="""// Educational demonstration of risky JavaScript patterns
function calculateExpression(rawFormula, role) {
    // Dangerous eval() allows arbitrary code execution
    const computedResult = eval(rawFormula);
    
    // Loose equality allows unexpected type coercion
    if (role == 0) {
        // Undeclared variable leak
        debugStatus = "Admin mode triggered";
        debugger;
    }
    
    return computedResult;
}
"""
    ),
    SampleItem(
        id="js-clean",
        title="JavaScript: Clean & Validated Pattern",
        language="javascript",
        filename="student_calculator_clean.js",
        description="Demonstrates strict equality, strict variable scoping, and safe arithmetic evaluation.",
        code="""// Secure JavaScript calculation module
function calculateSafeSum(a, b, role) {
    if (typeof a !== "number" || typeof b !== "number") {
        throw new TypeError("Both operands must be valid numbers");
    }

    // Strict equality check prevents type coercion
    if (role === "admin") {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] Admin calculation initiated`);
    }

    return a + b;
}

export { calculateSafeSum };
"""
    )
]


@app.get("/")
def root():
    return {
        "message": "ProjectLens AI API is running",
        "docs_url": "/docs",
        "health_url": "/api/health"
    }


@app.get("/api/health", response_model=HealthResponse)
def health_check():
    """Verify backend and static analysis tool availability."""
    bandit_ok, bandit_msg = python_analyzer.is_available()
    eslint_ok, eslint_msg = js_analyzer.is_available()

    return HealthResponse(
        status="healthy" if (bandit_ok and eslint_ok) else "degraded",
        tools={
            "bandit": ToolStatus(
                name="Bandit (Python Static Analyzer)",
                available=bandit_ok,
                version_or_path=bandit_msg if bandit_ok else None,
                error=bandit_msg if not bandit_ok else None
            ),
            "eslint": ToolStatus(
                name="ESLint (JavaScript Static Analyzer)",
                available=eslint_ok,
                version_or_path=eslint_msg if eslint_ok else None,
                error=eslint_msg if not eslint_ok else None
            )
        }
    )


@app.get("/api/samples", response_model=List[SampleItem])
def get_sample_codes():
    """Return educational code snippets for quick interactive testing."""
    return SAMPLE_CODES


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_file(file: UploadFile = File(...)):
    """
    Upload and analyze a single .py or .js source file.
    Security guarantees:
    - Code is NEVER executed or imported.
    - Code is analyzed in a strictly isolated subprocess with timeout.
    - Enforces file extension and size limits.
    """
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file was uploaded or filename is missing."
        )

    # 1. Validate File Extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        allowed_list = ", ".join(ALLOWED_EXTENSIONS.keys())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{file_ext}'. ProjectLens AI only accepts {allowed_list} files."
        )

    language = ALLOWED_EXTENSIONS[file_ext]

    # 2. Validate File Size safely (read up to MAX_FILE_SIZE_BYTES + 1)
    content = await file.read(MAX_FILE_SIZE_BYTES + 1)
    file_size = len(content)

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty (0 bytes). Please upload a valid source file."
        )

    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=f"Uploaded file exceeds the maximum allowed size limit of {MAX_FILE_SIZE_BYTES // (1024*1024)}MB."
        )

    # 3. Write securely to a temporary file
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(dir=str(TEMP_DIR), suffix=file_ext, delete=False) as tf:
            tf.write(content)
            temp_file_path = tf.name

        # 4. Execute the appropriate static analysis engine
        if language == "python":
            tool_name = "Bandit Security Scanner"
            findings = python_analyzer.analyze(temp_file_path, file.filename)
            summary = PythonBanditAnalyzer.calculate_summary(findings)
        else:
            tool_name = "ESLint Static Linter"
            findings = js_analyzer.analyze(temp_file_path, file.filename)
            summary = JavaScriptESLintAnalyzer.calculate_summary(findings)

        scan_time = datetime.now(timezone.utc).isoformat()

        return AnalysisResponse(
            success=True,
            file_name=file.filename,
            file_type=language,
            file_size_bytes=file_size,
            scan_timestamp=scan_time,
            tool_used=tool_name,
            summary=summary,
            findings=findings,
            disclaimer=SECURITY_DISCLAIMER,
            message="Analysis completed successfully." if findings else "Scan completed with 0 issues detected."
        )

    except TimeoutError as te:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail=str(te)
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except RuntimeError as re:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(re)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during static analysis: {str(e)}"
        )
    finally:
        # Secure cleanup: Ensure temporary file is always deleted
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception:
                pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=False)

