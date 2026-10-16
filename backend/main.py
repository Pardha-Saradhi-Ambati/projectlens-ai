"""
ProjectLens AI — ASGI Application Entry Point
Re-exports the FastAPI 'app' instance from app.main for deployment platforms
(e.g., Render, Railway, Uvicorn CLI default: main:app).
"""

from app.main import app

__all__ = ["app"]
