from typing import Dict, Any, Optional

BANDIT_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "B101": {
        "title": "Use of assert detected",
        "risk": "In Python, `assert` statements are stripped out completely when code runs with optimizations (`python -O`). Relying on asserts for access control or security validation means checks can be silently bypassed in production.",
        "recommendation": "Use explicit `if` statements and raise specific exceptions like `ValueError` or `PermissionError` instead of `assert`.",
        "example": "# Instead of:\n# assert user.is_admin, 'Unauthorized'\n\n# Secure alternative:\nif not user.is_admin:\n    raise PermissionError('Unauthorized access denied')",
        "reference": "https://bandit.readthedocs.io/en/latest/plugins/b101_assert_used.html"
    },
    "B102": {
        "title": "Use of exec() detected",
        "risk": "`exec()` dynamically executes arbitrary Python code strings with the current process privileges. If any untrusted or user-supplied input reaches `exec()`, attackers can achieve Remote Code Execution (RCE).",
        "recommendation": "Never pass untrusted data to `exec()`. Restructure the logic using standard functions, dictionaries, or declarative data structures.",
        "example": "# Instead of:\n# exec(f'result = {user_input}')\n\n# Safe alternative:\nOPERATIONS = {'add': lambda a, b: a + b}\nresult = OPERATIONS[op_name](a, b)",
        "reference": "https://bandit.readthedocs.io/en/latest/plugins/b102_exec_used.html"
    },
    "B105": {
        "title": "Possible hardcoded password detected",
        "risk": "Hardcoding secrets or passwords directly in source code allows anyone with repository access to discover credentials. If pushed to GitHub or shared with classmates, secrets will be permanently exposed in commit history.",
        "recommendation": "Load credentials from environment variables using `os.getenv()` or a `.env` file with `python-dotenv`.",
        "example": "# Instead of:\n# DB_PASSWORD = 'supersecretpassword123'\n\n# Secure alternative:\nimport os\nDB_PASSWORD = os.getenv('DB_PASSWORD')\nif not DB_PASSWORD:\n    raise RuntimeError('DB_PASSWORD environment variable is not configured')",
        "reference": "https://bandit.readthedocs.io/en/latest/plugins/b105_hardcoded_password_string.html"
    },
    "B106": {
        "title": "Hardcoded password in function default argument",
        "risk": "Default argument values are evaluated when the module is imported and stored in function metadata, exposing credentials in introspection and bytecode.",
        "recommendation": "Use `None` as the default argument and retrieve the secret at runtime from secure environment variables.",
        "example": "# Instead of:\n# def login(username, password='default_password'):\n\n# Secure alternative:\ndef login(username, password=None):\n    auth_pass = password or os.getenv('APP_SECRET')",
        "reference": "https://bandit.readthedocs.io/en/latest/plugins/b106_hardcoded_password_funcarg.html"
    },
    "B108": {
        "title": "Probable insecure usage of temporary file or directory",
        "risk": "Using predictable hardcoded paths in `/tmp` makes the application vulnerable to symlink attacks and race conditions where another local process can tamper with or replace the file.",
        "recommendation": "Always use the standard `tempfile.NamedTemporaryFile` or `tempfile.TemporaryDirectory` module with secure file permissions.",
        "example": "# Instead of:\n# f = open('/tmp/myapp_cache.txt', 'w')\n\n# Secure alternative:\nimport tempfile\nwith tempfile.NamedTemporaryFile(mode='w', delete=True) as temp_file:\n    temp_file.write(data)",
        "reference": "https://bandit.readthedocs.io/en/latest/plugins/b108_hardcoded_tmp_directory.html"
    },
    "B301": {
        "title": "Pickle deserialization vulnerability",
        "risk": "Python's `pickle` format is not secure against untrusted data. Unpickling malicious data can execute arbitrary arbitrary machine code via `__reduce__` exploit payloads.",
        "recommendation": "Use safer serialization formats like JSON, MessagePack, or Protocol Buffers when communicating or storing data.",
        "example": "# Instead of:\n# data = pickle.loads(raw_input_bytes)\n\n# Secure alternative:\nimport json\ndata = json.loads(raw_input_string)",
        "reference": "https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html#b301-pickle"
    },
    "B303": {
        "title": "Insecure cryptographic hash function (MD5)",
        "risk": "MD5 has practical collision vulnerabilities. Attackers can generate two distinct inputs that yield the identical MD5 digest, breaking integrity and signature verification.",
        "recommendation": "Use modern cryptographic hash algorithms like SHA-256 (`hashlib.sha256()`) or Argon2 / bcrypt for passwords.",
        "example": "# Instead of:\n# digest = hashlib.md5(data.encode()).hexdigest()\n\n# Secure alternative:\nimport hashlib\ndigest = hashlib.sha256(data.encode()).hexdigest()",
        "reference": "https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html#b303-md5"
    },
    "B307": {
        "title": "Use of eval() detected",
        "risk": "`eval()` parses arbitrary strings as Python code and evaluates them immediately. If any external user input is passed, an adversary can execute commands or inspect private memory.",
        "recommendation": "Avoid `eval()`. For parsing literal data, use `ast.literal_eval()`. For mathematical evaluations, use a constrained parser.",
        "example": "# Instead of:\n# val = eval(user_str)\n\n# Safe alternative for literals:\nimport ast\nsafe_data = ast.literal_eval(user_str)",
        "reference": "https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html#b307-eval"
    },
    "B311": {
        "title": "Standard pseudo-random generator used in sensitive context",
        "risk": "Python's `random` module uses the Mersenne Twister PRNG, which is completely deterministic and predictable once 624 outputs are observed. It must never be used for tokens, session IDs, or encryption keys.",
        "recommendation": "Use the cryptographically secure `secrets` module in Python 3.6+ for generating tokens and random passwords.",
        "example": "# Instead of:\n# import random\n# token = str(random.randint(100000, 999999))\n\n# Secure alternative:\nimport secrets\ntoken = secrets.token_hex(16)",
        "reference": "https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html#b311-random"
    },
    "B404": {
        "title": "Subprocess module imported",
        "risk": "Importing subprocess indicates potential process execution. If parameters passed to subprocess functions are dynamically built from user inputs without sanitization, command injection can occur.",
        "recommendation": "Audit all subprocess call sites. Never set `shell=True` and pass arguments as lists rather than formatted strings.",
        "example": "# Safe practice:\nimport subprocess\nsubprocess.run(['ls', '-l', safe_path], shell=False, check=True)",
        "reference": "https://bandit.readthedocs.io/en/latest/blacklists/blacklist_imports.html#b404-import-subprocess"
    },
    "B602": {
        "title": "Subprocess call with shell=True",
        "risk": "Passing `shell=True` to `subprocess.Popen` or `subprocess.run` invokes the system shell (`sh` on Linux, `cmd.exe` on Windows). String concatenation allows attackers to append arbitrary shell commands (e.g. `; rm -rf /`).",
        "recommendation": "Set `shell=False` and pass arguments as a sequence (list) of strings where each element represents one argument.",
        "example": "# Instead of:\n# subprocess.run(f'ping {host}', shell=True)\n\n# Secure alternative:\nsubprocess.run(['ping', '-c', '4', host], shell=False, check=True)",
        "reference": "https://bandit.readthedocs.io/en/latest/plugins/b602_subprocess_popen_with_shell_equals_true.html"
    },
    "B605": {
        "title": "Starting a process with a shell",
        "risk": "Functions like `os.system()` or `os.popen()` execute commands inside a shell. If untrusted input is included in the command string, attackers can inject shell metacharacters like `&`, `|`, or `;` to run unintended commands.",
        "recommendation": "Replace `os.system()` with `subprocess.run([...], shell=False)` and pass arguments as a list.",
        "example": "# Instead of:\n# os.system('tar -czf ' + filename + ' /data')\n\n# Secure alternative:\nimport subprocess\nsubprocess.run(['tar', '-czf', filename, '/data'], check=True)",
        "reference": "https://bandit.readthedocs.io/en/latest/plugins/b605_start_process_with_a_shell.html"
    },
    "B603": {
        "title": "Subprocess call without shell=True",
        "risk": "Even when invoking subprocess without a shell, if the executable path or input arguments are derived from untrusted user input without sanitization, an attacker could manipulate options or binary targets.",
        "recommendation": "Hardcode trusted binary names or validate all arguments against strict whitelists before invoking subprocess.",
        "example": "# Safe practice:\nimport subprocess\nsubprocess.run(['/usr/bin/git', 'status'], check=True)",
        "reference": "https://bandit.readthedocs.io/en/latest/plugins/b603_subprocess_without_shell_equals_true.html"
    },
    "B607": {
        "title": "Starting a process with a partial executable path",
        "risk": "Invoking a program using a relative or partial executable path relies on the PATH environment variable. If PATH is modified or points to an insecure directory, an attacker could plant a malicious binary with the same name.",
        "recommendation": "Use absolute paths to binaries (e.g., `/usr/bin/tar` or `shutil.which('git')`) or ensure the PATH variable is strictly controlled.",
        "example": "# Instead of:\n# subprocess.run(['tar', '-cf', 'out.tar', 'files'])\n\n# Secure alternative:\nimport shutil, subprocess\ntar_bin = shutil.which('tar')\nsubprocess.run([tar_bin, '-cf', 'out.tar', 'files'], check=True)",
        "reference": "https://bandit.readthedocs.io/en/latest/plugins/b607_start_process_with_partial_path.html"
    },
    "B608": {
        "title": "Possible SQL injection detected",
        "risk": "Building SQL queries using string formatting (`%`, `.format()`, or f-strings) allows attackers to alter query logic, extract sensitive records, or drop tables (SQL Injection).",
        "recommendation": "Use parameterized queries or prepared statements provided by your database driver (e.g., `cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))`).",
        "example": "# Instead of:\n# cursor.execute(f'SELECT * FROM users WHERE name = \"{username}\"')\n\n# Secure alternative:\ncursor.execute('SELECT * FROM users WHERE name = %s', (username,))",
        "reference": "https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html"
    }
}

ESLINT_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "no-eval": {
        "title": "Dangerous use of eval()",
        "risk": "`eval()` executes string code in the current lexical scope. It exposes applications to Cross-Site Scripting (XSS), arbitrary code execution, and impairs JavaScript engine optimization (like V8 de-optimizations).",
        "recommendation": "Do not use `eval()`. Parse structured data using `JSON.parse()` or use native mathematical operators and objects.",
        "example": "// Instead of:\n// const data = eval('(' + responseString + ')');\n\n// Safe alternative:\nconst data = JSON.parse(responseString);",
        "reference": "https://eslint.org/docs/latest/rules/no-eval"
    },
    "no-implied-eval": {
        "title": "Implied eval via setTimeout or setInterval",
        "risk": "Passing strings instead of functions to `setTimeout()`, `setInterval()`, or `setImmediate()` triggers dynamic code interpretation identical to `eval()`, enabling code injection.",
        "recommendation": "Pass a callback function or arrow function reference instead of a string.",
        "example": "// Instead of:\n// setTimeout('doWork(' + id + ')', 1000);\n\n// Safe alternative:\nsetTimeout(() => doWork(id), 1000);",
        "reference": "https://eslint.org/docs/latest/rules/no-implied-eval"
    },
    "no-new-func": {
        "title": "Use of Function constructor",
        "risk": "Calling `new Function('code')` parses code at runtime similarly to `eval()` and can bypass security linters while opening vectors for remote script execution.",
        "recommendation": "Define standard function declarations or arrow functions instead of constructing code strings dynamically.",
        "example": "// Instead of:\n// const add = new Function('a', 'b', 'return a + b');\n\n// Safe alternative:\nconst add = (a, b) => a + b;",
        "reference": "https://eslint.org/docs/latest/rules/no-new-func"
    },
    "no-undef": {
        "title": "Use of undeclared variable",
        "risk": "Referencing variables that have not been explicitly declared with `const`, `let`, or `var` will throw a runtime `ReferenceError` or implicitly create unexpected global variables.",
        "recommendation": "Declare all variables with `const` or `let` before use, or ensure proper module imports.",
        "example": "// Instead of:\n// count = 10; // Implicit global leak!\n\n// Correct:\nlet count = 10;",
        "reference": "https://eslint.org/docs/latest/rules/no-undef"
    },
    "no-unused-vars": {
        "title": "Unused variable detected",
        "risk": "Unused variables usually indicate leftover debugging code, incomplete refactorings, or typos where a wrong variable name was referenced elsewhere in the code.",
        "recommendation": "Remove unused variables or prefix them with an underscore (`_var`) if required by an interface.",
        "example": "// Instead of:\n// const [data, extraUnused] = getResults();\n\n// Clean alternative:\nconst [data] = getResults();",
        "reference": "https://eslint.org/docs/latest/rules/no-unused-vars"
    },
    "eqeqeq": {
        "title": "Loose equality operator used (== instead of ===)",
        "risk": "JavaScript's `==` and `!=` perform implicit type coercion (e.g. `0 == ''` is true, `false == []` is true). This causes subtle bugs and unexpected truthy/falsy evaluation flaws.",
        "recommendation": "Always use strict equality `===` and strict inequality `!==` to compare both value and type.",
        "example": "// Instead of:\n// if (userRole == 'admin')\n\n// Safe alternative:\nif (userRole === 'admin')",
        "reference": "https://eslint.org/docs/latest/rules/eqeqeq"
    },
    "no-caller": {
        "title": "Use of deprecated arguments.caller / arguments.callee",
        "risk": "These properties are deprecated, break strict mode (`'use strict'`), and prevent compiler optimizations.",
        "recommendation": "Give the function a name and refer to it directly rather than using `arguments.callee`.",
        "example": "// Instead of:\n// [1,2,3].map(function(n) { return n <= 1 ? 1 : n * arguments.callee(n - 1); });\n\n// Correct:\nconst factorial = (n) => (n <= 1 ? 1 : n * factorial(n - 1));",
        "reference": "https://eslint.org/docs/latest/rules/no-caller"
    },
    "no-script-url": {
        "title": "javascript: URL detected",
        "risk": "Using `javascript:` pseudo-protocols in links or URLs is a common Cross-Site Scripting (XSS) anti-pattern and can execute unauthorized scripts when clicked.",
        "recommendation": "Use clean event listeners like `onClick={handleClick}` with proper button elements.",
        "example": "// Instead of:\n// <a href=\"javascript:doSomething()\">Click</a>\n\n// Safe alternative:\n// <button type=\"button\" onClick={doSomething}>Click</button>",
        "reference": "https://eslint.org/docs/latest/rules/no-script-url"
    },
    "no-proto": {
        "title": "Direct access to __proto__",
        "risk": "Mutating or accessing `__proto__` directly is deprecated and is the root cause of Prototype Pollution attacks, which can compromise the entire Node runtime.",
        "recommendation": "Use standard `Object.getPrototypeOf()` or `Object.create()` instead of `__proto__`.",
        "example": "// Instead of:\n// obj.__proto__ = parentProto;\n\n// Safe alternative:\nconst obj = Object.create(parentProto);",
        "reference": "https://eslint.org/docs/latest/rules/no-proto"
    },
    "no-debugger": {
        "title": "Debugger statement left in code",
        "risk": "Leaving `debugger` in code halts execution when Developer Tools are open, which can disrupt user experience or reveal implementation details in production.",
        "recommendation": "Remove `debugger;` statements prior to submitting or deploying your project.",
        "example": "// Remove any standalone debugger statements before submitting code:\n// debugger;",
        "reference": "https://eslint.org/docs/latest/rules/no-debugger"
    }
}


def get_bandit_guidance(rule_id: str, default_description: str) -> Dict[str, Any]:
    """Retrieve educational guidance for a Bandit rule."""
    clean_id = (rule_id or "").upper().strip()
    if clean_id in BANDIT_KNOWLEDGE_BASE:
        return BANDIT_KNOWLEDGE_BASE[clean_id]

    # Dynamic fallback heuristic
    return {
        "title": f"Security Rule {clean_id or 'Finding'}",
        "risk": f"This pattern ({default_description}) was flagged as a potential security risk by Bandit static analysis. Heuristic patterns like this often correlate with common vulnerabilities.",
        "recommendation": "Review the flagged line, ensure all inputs are strictly validated, and avoid unconstrained system or network calls.",
        "example": "# Verify input validity and apply defensive coding practices:\n# Ensure all arguments are validated against strict whitelists before usage.",
        "reference": "https://bandit.readthedocs.io/en/latest/plugins/index.html"
    }


def get_eslint_guidance(rule_id: str, default_description: str) -> Dict[str, Any]:
    """Retrieve educational guidance for an ESLint rule."""
    clean_id = (rule_id or "").lower().strip()
    if clean_id in ESLINT_KNOWLEDGE_BASE:
        return ESLINT_KNOWLEDGE_BASE[clean_id]

    # Dynamic fallback heuristic
    return {
        "title": f"Linting Rule: {clean_id or 'Issue'}",
        "risk": f"ESLint detected a syntax, style, or potential runtime defect: {default_description}. This can lead to unexpected exceptions or maintainability challenges.",
        "recommendation": f"Resolve the condition flagged by `{clean_id}` by adhering to modern ECMAScript standards and clean coding practices.",
        "example": "// Ensure strict syntax, proper declarations, and explicit type comparisons.",
        "reference": f"https://eslint.org/docs/latest/rules/{clean_id}" if clean_id else "https://eslint.org"
    }
