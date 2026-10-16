import shutil
import subprocess
import json
import logging
from typing import List, Tuple, Optional
from app.analyzers.base import BaseAnalyzer
from app.models import Finding, FindingSeverity
from app.config import ANALYSIS_TIMEOUT_SECONDS, ESLINT_CONFIG_PATH
from app.recommendation_engine import get_eslint_guidance

logger = logging.getLogger(__name__)


class JavaScriptESLintAnalyzer(BaseAnalyzer):
    """Executes ESLint static analysis on JavaScript source files safely in a subprocess."""

    def __init__(self):
        self._cmd_runner = self._resolve_runner()
        self._availability_cache: Optional[Tuple[bool, str]] = None

    def _resolve_runner(self) -> Optional[List[str]]:
        """Find the executable command to run eslint without shell=True."""
        # 1. Direct eslint binary
        eslint_bin = shutil.which("eslint") or shutil.which("eslint.cmd")
        if eslint_bin:
            return [eslint_bin]

        # 2. NPX runner
        npx_bin = shutil.which("npx") or shutil.which("npx.cmd")
        if npx_bin:
            return [npx_bin, "eslint"]

        return None

    def is_available(self) -> Tuple[bool, str]:
        """Check if ESLint can be invoked (with caching)."""
        if self._availability_cache is not None:
            return self._availability_cache

        runner = self._resolve_runner()
        if not runner:
            self._availability_cache = (False, "Neither 'eslint' nor 'npx' executable was found in system PATH.")
            return self._availability_cache

        try:
            cmd = runner + ["--version"]
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=15,
                shell=False
            )
            if res.returncode == 0:
                version = res.stdout.strip().split("\n")[-1]
                self._availability_cache = (True, f"ESLint {version} (via {runner[0]})")
            else:
                self._availability_cache = (False, f"ESLint check returned code {res.returncode}: {res.stderr.strip()}")
        except Exception as e:
            self._availability_cache = (False, f"ESLint runner error: {str(e)}")

        return self._availability_cache

    def analyze(self, file_path: str, original_filename: str) -> List[Finding]:
        """Run ESLint with curated flat config against target file and return parsed findings."""
        runner = self._resolve_runner()
        if not runner:
            raise RuntimeError("JavaScript analysis tool 'ESLint' is not installed or available on the server.")

        # Command arguments: safe array, no shell=True
        # Use --no-ignore so temporary files are always scanned
        cmd = runner + ["--config", ESLINT_CONFIG_PATH, "--no-ignore", "-f", "json", file_path]

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=ANALYSIS_TIMEOUT_SECONDS,
                shell=False
            )
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"JavaScript static analysis timed out after {ANALYSIS_TIMEOUT_SECONDS}s.")
        except Exception as e:
            raise RuntimeError(f"Failed to execute ESLint subprocess: {str(e)}")

        raw_output = proc.stdout.strip()
        
        # If no json output but error in stderr
        if not raw_output and proc.returncode != 0:
            err = proc.stderr.strip()
            raise RuntimeError(f"ESLint execution failed: {err}")

        try:
            reports = json.loads(raw_output)
        except json.JSONDecodeError as e:
            if "Parsing error" in proc.stderr:
                raise ValueError(f"JavaScript Syntax Error in uploaded file: {proc.stderr}")
            raise RuntimeError(f"Failed to parse ESLint output: {str(e)} -> Output: {raw_output[:200]}")

        findings: List[Finding] = []
        if not isinstance(reports, list) or len(reports) == 0:
            return findings

        file_report = reports[0]
        messages = file_report.get("messages", [])

        # Read source lines to extract snippets if not provided directly
        source_lines = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                source_lines = f.readlines()
        except Exception:
            pass

        finding_count = 0
        for item in messages:
            rule_id = item.get("ruleId")
            # Skip ignored-file informational warnings
            if not rule_id or "File ignored" in item.get("message", ""):
                continue

            raw_severity = item.get("severity", 1)  # 1 = warning, 2 = error
            line_num = item.get("line")
            col_num = item.get("column")
            message_text = item.get("message", "Lint warning")

            # Determine severity: Security-critical rules are HIGH
            high_security_rules = {"no-eval", "no-implied-eval", "no-new-func", "no-script-url", "no-proto"}
            if rule_id in high_security_rules or raw_severity == 2:
                severity = FindingSeverity.HIGH if rule_id in high_security_rules else FindingSeverity.MEDIUM
            elif raw_severity == 1:
                severity = FindingSeverity.LOW
            else:
                severity = FindingSeverity.INFO

            guidance = get_eslint_guidance(rule_id, message_text)

            # Code snippet extraction
            snippet = None
            if line_num and 1 <= line_num <= len(source_lines):
                snippet = source_lines[line_num - 1].strip()

            finding_count += 1
            finding = Finding(
                id=f"js-{rule_id.lower().replace('/', '-')}-{finding_count}",
                rule_id=rule_id,
                title=guidance.get("title", f"Rule {rule_id}"),
                severity=severity,
                line_number=line_num,
                column_number=col_num,
                code_snippet=snippet,
                description=message_text,
                risk_explanation=guidance.get("risk", ""),
                recommendation=guidance.get("recommendation", ""),
                code_fix_example=guidance.get("example"),
                reference_url=guidance.get("reference")
            )
            findings.append(finding)

        return findings
