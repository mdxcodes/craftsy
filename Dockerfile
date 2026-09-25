# ============================================================
# Craftsy Backend — Production Dockerfile
# ============================================================
# Python 3.12-slim is used because every runtime dependency
# (chromadb, onnxruntime, rembg, opencv-python-headless, psycopg2-binary)
# publishes pre-built wheels for it, keeping the image reproducible.
# No secrets are baked into the image — all configuration is injected
# through environment variables at runtime.
# ============================================================

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000

WORKDIR /app

# System packages:
#   ffmpeg       — voice-pipeline silence detection (subprocess)
#   libgomp1     — onnxruntime (rembg) OpenMP runtime
#   libglib2.0-0 — OpenCV runtime dependency
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        libgomp1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first so Docker layer caching survives code edits.
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Application code (backend + ML pipelines). frontend/, docs/, and local
# runtime data are excluded via .dockerignore.
COPY backend ./backend
COPY ML ./ML

# Run as an unprivileged user.
RUN useradd --create-home --uid 10001 craftsy \
    && chown -R craftsy:craftsy /app
USER craftsy

EXPOSE 8000

# Railway injects $PORT; fall back to 8000 for local docker runs.
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
