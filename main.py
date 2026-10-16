"""
ProjectLens AI — Root ASGI Application Entry Point
Enables direct deployment from the repository root when Render's Root Directory
is left at the default (root) setting.
"""
import sys
from pathlib import Path

# Ensure 'backend' directory is on sys.path so 'app.main' can be imported
backend_path = Path(__file__).resolve().parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.main import app

__all__ = ["app"]
