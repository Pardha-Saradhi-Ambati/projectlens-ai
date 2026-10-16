import sys
import subprocess
import json
import logging
from typing import List, Tuple
from app.analyzers.base import BaseAnalyzer
from app.models import Finding, FindingSeverity
from app.config import ANALYSIS_TIMEOUT_SECONDS
from app.recommendation_engine import get_bandit_guidance

logger = logging.getLogger(__name__)


class PythonBanditAnalyzer(BaseAnalyzer):
    """Executes Bandit static analysis on Python source files safely in a subprocess."""

    def __init__(self):
        self._python_exec = sys.executable

    def is_available(self) -> Tuple[bool, str]:
        """Check if Bandit is available via python -m bandit."""
        try:
            res = subprocess.run(
                [self._python_exec, "-m", "bandit", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=False
            )
            if res.returncode == 0:
                first_line = res.stdout.strip().split("\n")[0] if res.stdout else "Bandit available"
                return True, first_line
            return False, f"Bandit returned error code {res.returncode}: {res.stderr.strip()}"
        except Exception as e:
            return False, f"Bandit not available: {str(e)}"

    def analyze(self, file_path: str, original_filename: str) -> List[Finding]:
        """Run Bandit against target file and return parsed findings."""
        available, msg = self.is_available()
        if not available:
            raise RuntimeError(f"Python analysis tool 'Bandit' cannot be executed: {msg}")

        # Secure subprocess execution:
        # 1. No shell=True
        # 2. Controlled argument list
        # 3. Timeout applied
        cmd = [self._python_exec, "-m", "bandit", "-f", "json", file_path]

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=ANALYSIS_TIMEOUT_SECONDS,
                shell=False
            )
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Static analysis timed out after {ANALYSIS_TIMEOUT_SECONDS}s.")
        except Exception as e:
            raise RuntimeError(f"Failed to execute Bandit subprocess: {str(e)}")

        # Bandit returns code 0 (no issues) or 1 (issues found). Both mean execution succeeded.
        if proc.returncode not in (0, 1):
            error_details = proc.stderr.strip() or proc.stdout.strip()
            # If the user uploaded invalid syntax (e.g., SyntaxError in python file)
            if "syntax error" in error_details.lower():
                raise ValueError(f"Python Syntax Error detected in uploaded file: {error_details}")
            raise RuntimeError(f"Bandit execution failed (exit code {proc.returncode}): {error_details}")

        raw_output = proc.stdout
        if not raw_output.strip():
            return []

        try:
            data = json.loads(raw_output)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse Bandit JSON output: {str(e)}")

        bandit_results = data.get("results", [])
        findings: List[Finding] = []

        for idx, item in enumerate(bandit_results):
            test_id = item.get("test_id", "")
            raw_severity = (item.get("issue_severity") or "LOW").upper()
            
            # Map severity
            if raw_severity == "HIGH":
                severity = FindingSeverity.HIGH
            elif raw_severity == "MEDIUM":
                severity = FindingSeverity.MEDIUM
            else:
                severity = FindingSeverity.LOW

            issue_text = item.get("issue_text", "Security pattern flagged by Bandit")
            guidance = get_bandit_guidance(test_id, issue_text)

            finding = Finding(
                id=f"py-{test_id.lower()}-{idx + 1}",
                rule_id=test_id,
                title=guidance.get("title", f"Bandit {test_id}"),
                severity=severity,
                line_number=item.get("line_number"),
                column_number=item.get("col_offset"),
                code_snippet=(item.get("code") or "").strip(),
                description=issue_text,
                risk_explanation=guidance.get("risk", ""),
                recommendation=guidance.get("recommendation", ""),
                code_fix_example=guidance.get("example"),
                reference_url=item.get("more_info") or guidance.get("reference")
            )
            findings.append(finding)

        return findings
