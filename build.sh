#!/usr/bin/env bash
# ==========================================
# ProjectLens AI — Render / Production Build Script
# ==========================================
set -o errexit

echo "==> Step 1: Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "==> Step 2: Installing Node.js dependencies (ESLint)..."
npm install --omit=dev

echo "==> Step 3: Verifying analyzer engine installations..."
python -m bandit --version
node -v
npm list eslint || true

echo "==> Build complete!"
