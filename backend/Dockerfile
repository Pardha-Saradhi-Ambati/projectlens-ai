# ==========================================
# ProjectLens AI — Backend Dockerfile
# ==========================================
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Node.js for ESLint
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
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source files
COPY . .

# Ensure isolated temp directory exists
RUN mkdir -p /app/.temp

ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

CMD ["python", "run.py"]
