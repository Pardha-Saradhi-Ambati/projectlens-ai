import urllib.request
import urllib.parse
import json
import io
import mimetypes
import uuid

BASE_URL = "http://127.0.0.1:8000"

def log_test(title, passed, details=""):
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {title}")
    if details:
        print(f"       {details}")

def test_health():
    url = f"{BASE_URL}/api/health"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        bandit_ready = data.get("tools", {}).get("bandit", {}).get("available") is True
        eslint_ready = data.get("tools", {}).get("eslint", {}).get("available") is True
        log_test("Health Check Endpoint (GET /api/health)", 
                 resp.status == 200 and bandit_ready and eslint_ready, 
                 f"Status: {data.get('status')}, Bandit: {bandit_ready}, ESLint: {eslint_ready}")
        return data

def multipart_post(url, filename, content_bytes, content_type="text/plain"):
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    body = io.BytesIO()
    
    body.write(f"--{boundary}\r\n".encode("utf-8"))
    body.write(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode("utf-8"))
    body.write(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
    body.write(content_bytes)
    body.write(b"\r\n")
    body.write(f"--{boundary}--\r\n".encode("utf-8"))
    
    req = urllib.request.Request(
        url,
        data=body.getvalue(),
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Origin": "http://localhost:5173"
        },
        method="POST"
    )
    return req

def test_upload_python_vulnerable():
    url = f"{BASE_URL}/api/analyze"
    py_code = b'''import os
password = "supersecretpassword123"
os.system("ls " + password)
'''
    req = multipart_post(url, "vulnerable_test.py", py_code)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        findings = data.get("findings", [])
        total = data.get("summary", {}).get("total_issues", 0)
        has_bandit = "Bandit" in data.get("tool_used", "")
        # Check CORS header in response
        cors_header = resp.headers.get("access-control-allow-origin")
        log_test("Python File Upload & Bandit Analysis (POST /api/analyze)",
                 resp.status == 200 and total >= 2 and has_bandit,
                 f"Tool: {data.get('tool_used')}, Findings: {total}, CORS: {cors_header}")
        for f in findings:
            print(f"       - [{f.get('severity')}] {f.get('rule_id')}: {f.get('title')} (Line {f.get('line_number')})")

def test_upload_js_vulnerable():
    url = f"{BASE_URL}/api/analyze"
    js_code = b'''function test(input) {
    eval(input);
    if (input == 10) {
        undeclaredVar = true;
    }
}
'''
    req = multipart_post(url, "vulnerable_test.js", js_code)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        findings = data.get("findings", [])
        total = data.get("summary", {}).get("total_issues", 0)
        has_eslint = "ESLint" in data.get("tool_used", "")
        log_test("JavaScript File Upload & ESLint Analysis (POST /api/analyze)",
                 resp.status == 200 and total >= 2 and has_eslint,
                 f"Tool: {data.get('tool_used')}, Findings: {total}")
        for f in findings:
            print(f"       - [{f.get('severity')}] {f.get('rule_id')}: {f.get('title')} (Line {f.get('line_number')})")

def test_upload_clean_file():
    url = f"{BASE_URL}/api/analyze"
    clean_code = b'''def add(a: int, b: int) -> int:
    """Safely adds two numbers."""
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Arguments must be integers")
    return a + b
'''
    req = multipart_post(url, "clean_test.py", clean_code)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        total = data.get("summary", {}).get("total_issues", 0)
        log_test("Clean Code Upload (0 Findings handling)",
                 resp.status == 200 and total == 0,
                 f"Total findings: {total}, Message: {data.get('message')}")

def test_invalid_extension():
    url = f"{BASE_URL}/api/analyze"
    bad_code = b"Hello world text file"
    req = multipart_post(url, "notes.txt", bad_code)
    try:
        urllib.request.urlopen(req)
        log_test("Reject Unsupported File Extension (.txt)", False, "Expected HTTP 400 error")
    except urllib.error.HTTPError as e:
        err_data = json.loads(e.read().decode())
        log_test("Reject Unsupported File Extension (.txt)", 
                 e.code == 400, 
                 f"HTTP {e.code}: {err_data.get('detail')}")

def test_empty_file():
    url = f"{BASE_URL}/api/analyze"
    req = multipart_post(url, "empty.py", b"")
    try:
        urllib.request.urlopen(req)
        log_test("Reject Empty File (0 bytes)", False, "Expected HTTP 400 error")
    except urllib.error.HTTPError as e:
        err_data = json.loads(e.read().decode())
        log_test("Reject Empty File (0 bytes)", 
                 e.code == 400, 
                 f"HTTP {e.code}: {err_data.get('detail')}")

def test_file_size_limit():
    url = f"{BASE_URL}/api/analyze"
    # Ensure payload exceeds 2MB limit (2.4MB)
    oversized = b"# padding\n" + (b"x = 1\n" * 400000)
    req = multipart_post(url, "large.py", oversized)
    try:
        urllib.request.urlopen(req)
        log_test("Reject File Exceeding Size Limit (>2MB)", False, "Expected HTTP 413 error")
    except urllib.error.HTTPError as e:
        err_data = json.loads(e.read().decode())
        log_test("Reject File Exceeding Size Limit (>2MB)", 
                 e.code == 413, 
                 f"HTTP {e.code}: {err_data.get('detail')}")

if __name__ == "__main__":
    print("=== Testing ProjectLens AI FastAPI Backend Endpoints ===")
    test_health()
    test_upload_python_vulnerable()
    test_upload_js_vulnerable()
    test_upload_clean_file()
    test_invalid_extension()
    test_empty_file()
    test_file_size_limit()
    print("=== All Tests Completed ===")
