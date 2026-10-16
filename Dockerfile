# ==========================================
# ProjectLens AI — Production Dockerfile
# ==========================================
# Combines Python 3.13 (FastAPI + Bandit) and Node.js 20 (ESLint)
FROM python:3.13-slim

# Avoid writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Node.js for JavaScript static analysis (ESLint)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g eslint \
    && apt-get purge -y --auto-remove curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application source
COPY backend/ .

# Create temporary scan directory
RUN mkdir -p /app/.temp

# Set default binding variables (Render/Railway/Heroku override PORT)
ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

CMD ["python", "run.py"]
