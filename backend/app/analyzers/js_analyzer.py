import os
import sys
import shutil
import subprocess
import json
import logging
from pathlib import Path
from typing import List, Tuple, Optional

from app.analyzers.base import BaseAnalyzer
from app.models import Finding, FindingSeverity
from app.config import (
    ANALYSIS_TIMEOUT_SECONDS,
    ESLINT_CONFIG_PATH,
    ESLINT_INIT_TIMEOUT_SECONDS,
    BASE_DIR,
    ROOT_DIR
)
from app.recommendation_engine import get_eslint_guidance

logger = logging.getLogger(__name__)


class JavaScriptESLintAnalyzer(BaseAnalyzer):
    """Executes ESLint static analysis on JavaScript source files safely in a subprocess."""

    def __init__(self):
        self._availability_cache: Optional[Tuple[bool, str]] = None

    @classmethod
    def _find_node_binary(cls) -> Optional[str]:
        """Find the Node.js executable binary across operating systems."""
        # 1. Custom NODE_BIN / NODE_PATH environment override
        custom_node = os.getenv("NODE_BIN") or os.getenv("NODE_PATH")
        if custom_node and os.path.isfile(custom_node) and os.access(custom_node, os.X_OK):
            return custom_node

        # 2. Check system PATH
        node_bin = shutil.which("node") or shutil.which("node.exe")
        if node_bin:
            return node_bin

        # 3. Known system locations (Render / Linux / macOS)
        known_system_nodes = [
            "/usr/bin/node",
            "/usr/local/bin/node",
            "/opt/render/project/nodes/default/bin/node",
            "/home/render/.nvm/versions/node/v20.0.0/bin/node",
            "/home/render/.nvm/versions/node/v18.0.0/bin/node",
        ]
        for loc in known_system_nodes:
            if os.path.isfile(loc) and os.access(loc, os.X_OK):
                return loc

        return None

    @classmethod
    def _resolve_runner_with_diagnostics(cls) -> Tuple[Optional[List[str]], str]:
        """
        Locates the local ESLint executable or Node runner safely without dynamic npx downloading.
        Returns:
            (runner_command_list, diagnostic_description)
        """
        is_windows = sys.platform.startswith("win")

        # 1. Explicit ESLINT_PATH environment variable override
        custom_eslint = os.getenv("ESLINT_PATH")
        if custom_eslint:
            custom_path = Path(custom_eslint).resolve()
            if custom_path.is_file():
                if custom_path.suffix.lower() == ".js":
                    node_bin = cls._find_node_binary()
                    if node_bin:
                        return [node_bin, str(custom_path)], f"Custom ESLint script ({custom_path}) via Node ({node_bin})"
                    return None, f"Custom ESLINT_PATH points to a .js script ({custom_path}), but Node.js was not found."
                return [str(custom_path)], f"Custom ESLint binary ({custom_path})"
            return None, f"Custom ESLINT_PATH '{custom_eslint}' does not exist on disk."

        node_bin = cls._find_node_binary()

        # 2. Project dependency: Execute local eslint.js via Node
        # This executes the locally installed package directly, works identically across
        # Linux, Windows, macOS, Render, and avoids .cmd wrappers or symlink differences.
        candidate_js_paths = [
            BASE_DIR / "node_modules" / "eslint" / "bin" / "eslint.js",
            ROOT_DIR / "node_modules" / "eslint" / "bin" / "eslint.js",
        ]
        for js_path in candidate_js_paths:
            if js_path.is_file():
                if node_bin:
                    return [node_bin, str(js_path.resolve())], f"Local ESLint package ({js_path.name}) via Node ({node_bin})"
                else:
                    return None, f"ESLint is installed at '{js_path}', but Node.js executable was not found in system PATH."

        # 3. Local node_modules/.bin binary (e.g. eslint or eslint.cmd)
        bin_name = "eslint.cmd" if is_windows else "eslint"
        candidate_bin_paths = [
            BASE_DIR / "node_modules" / ".bin" / bin_name,
            ROOT_DIR / "node_modules" / ".bin" / bin_name,
        ]
        if not is_windows:
            candidate_bin_paths.extend([
                BASE_DIR / "node_modules" / ".bin" / "eslint",
                ROOT_DIR / "node_modules" / ".bin" / "eslint",
            ])

        for bin_path in candidate_bin_paths:
            if bin_path.is_file() and os.access(bin_path, os.X_OK):
                return [str(bin_path.resolve())], f"Local binary ({bin_path})"

        # 4. Global ESLint binary in system PATH (e.g. Docker container global install)
        eslint_bin = shutil.which("eslint") or (shutil.which("eslint.cmd") if is_windows else None)
        if eslint_bin:
            return [eslint_bin], f"Global ESLint binary ({eslint_bin})"

        # 5. Not found: Return clear diagnostic error (DO NOT use npx to dynamically download)
        if node_bin:
            msg = (
                f"Node.js is available at '{node_bin}', but the 'eslint' package was not found in "
                f"project dependencies (checked '{BASE_DIR / 'node_modules'}' and '{ROOT_DIR / 'node_modules'}'). "
                "Please run 'npm install' in the project directory or update the deployment build command."
            )
        else:
            msg = (
                "Neither Node.js nor ESLint was found on the server. "
                "Please ensure Node.js (18+) is installed and run 'npm install' in the project root."
            )
        return None, msg

    def _resolve_runner(self) -> Optional[List[str]]:
        """Convenience method returning just the command runner list."""
        runner, _ = self._resolve_runner_with_diagnostics()
        return runner

    def is_available(self, force_refresh: bool = False) -> Tuple[bool, str]:
        """Check if ESLint can be invoked safely with timeout and caching."""
        if not force_refresh and self._availability_cache is not None and self._availability_cache[0] is True:
            return self._availability_cache

        runner, diag = self._resolve_runner_with_diagnostics()
        if not runner:
            self._availability_cache = (False, diag)
            return self._availability_cache

        # Prepare environment with local node_modules/.bin in PATH
        env = os.environ.copy()
        local_bin = str((BASE_DIR / "node_modules" / ".bin").resolve())
        root_bin = str((ROOT_DIR / "node_modules" / ".bin").resolve())
        env["PATH"] = f"{local_bin}{os.pathsep}{root_bin}{os.pathsep}{env.get('PATH', '')}"

        try:
            cmd = runner + ["--version"]
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=ESLINT_INIT_TIMEOUT_SECONDS,
                shell=False,
                cwd=str(BASE_DIR.resolve()),
                env=env
            )
            if res.returncode == 0:
                version = res.stdout.strip().split("\n")[-1]
                runner_label = runner[0] if len(runner) == 1 else f"{runner[0]} {Path(runner[1]).name}"
                self._availability_cache = (True, f"ESLint {version} ({runner_label})")
            else:
                err_text = res.stderr.strip() or res.stdout.strip()
                self._availability_cache = (
                    False,
                    f"ESLint check returned code {res.returncode}: {err_text}"
                )
        except subprocess.TimeoutExpired:
            self._availability_cache = (
                False,
                f"ESLint initialization timed out after {ESLINT_INIT_TIMEOUT_SECONDS}s."
            )
        except Exception as e:
            self._availability_cache = (False, f"ESLint runner error: {str(e)}")

        return self._availability_cache

    def analyze(self, file_path: str, original_filename: str) -> List[Finding]:
        """Run ESLint with curated flat config against target file and return parsed findings."""
        runner, diag = self._resolve_runner_with_diagnostics()
        if not runner:
            raise RuntimeError(f"JavaScript static analysis engine (ESLint) is not available: {diag}")

        abs_file_path = str(Path(file_path).resolve())
        abs_config_path = str(Path(ESLINT_CONFIG_PATH).resolve())
        cwd_path = str(BASE_DIR.resolve())

        if not os.path.exists(abs_config_path):
            raise RuntimeError(f"ESLint configuration file not found at: {abs_config_path}")

        # Command arguments: safe array, no shell=True
        # Use --no-ignore so temporary scan files are always evaluated
        cmd = runner + ["--config", abs_config_path, "--no-ignore", "-f", "json", abs_file_path]

        env = os.environ.copy()
        local_bin = str((BASE_DIR / "node_modules" / ".bin").resolve())
        root_bin = str((ROOT_DIR / "node_modules" / ".bin").resolve())
        env["PATH"] = f"{local_bin}{os.pathsep}{root_bin}{os.pathsep}{env.get('PATH', '')}"

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=ANALYSIS_TIMEOUT_SECONDS,
                shell=False,
                cwd=cwd_path,
                env=env
            )
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"JavaScript static analysis timed out after {ANALYSIS_TIMEOUT_SECONDS}s.")
        except Exception as e:
            raise RuntimeError(f"Failed to execute ESLint subprocess: {str(e)}")

        raw_output = proc.stdout.strip()

        # If no json output but non-zero return code
        if not raw_output and proc.returncode != 0:
            err = proc.stderr.strip()
            if "Parsing error" in err or "SyntaxError" in err:
                raise ValueError(f"JavaScript Syntax Error in uploaded file: {err}")
            raise RuntimeError(f"ESLint execution failed (code {proc.returncode}): {err}")

        try:
            reports = json.loads(raw_output)
        except json.JSONDecodeError as e:
            if "Parsing error" in proc.stderr or "SyntaxError" in proc.stderr:
                raise ValueError(f"JavaScript Syntax Error in uploaded file: {proc.stderr.strip()}")
            raise RuntimeError(f"Failed to parse ESLint JSON output: {str(e)} -> Raw: {raw_output[:200]}")

        findings: List[Finding] = []
        if not isinstance(reports, list) or len(reports) == 0:
            return findings

        file_report = reports[0]
        messages = file_report.get("messages", [])

        # Check for fatal syntax errors in messages
        for item in messages:
            if item.get("fatal") or "Parsing error" in item.get("message", ""):
                raise ValueError(f"JavaScript Syntax Error in uploaded file: {item.get('message')}")

        # Read source lines to extract snippets if not provided directly
        source_lines = []
        try:
            with open(abs_file_path, "r", encoding="utf-8", errors="replace") as f:
                source_lines = f.readlines()
        except Exception:
            pass

        finding_count = 0
        for item in messages:
            rule_id = item.get("ruleId")
            # Skip ignored-file informational warnings or messages without a rule_id
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
