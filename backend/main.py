"""
Craftsy FastAPI Application Entrypoint.

AI-Driven Market Linkage & Smart Cataloging Backend for Marginalized Artisans.

Deployment notes:
    - Runs on Railway with `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.
    - Databases: SQLite locally, PostgreSQL in production (via DATABASE_URL).
    - No optional AI provider is required to boot; heavy models are lazy-loaded.
"""

import logging
import sys
import warnings
from pathlib import Path
from contextlib import asynccontextmanager

# Silence upstream 3rd-party vendor deprecations on Python 3.14+
warnings.filterwarnings("ignore", category=DeprecationWarning, module="google.genai")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="chromadb")

# Fix Windows console encoding for emoji output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Ensure project root is in sys.path when running directly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import get_settings, ensure_upload_dir
from backend.database import init_db, describe_database, check_database_connection
from backend.routers import (
    health_router,
    pricing_router,
    products_router,
    catalog_router,
    auth_router,
    voice_router,
    social_router,
    chat_router,
    commerce_router,
    orders_router,
    commerce_hub_router,
    bhashini_router,
    cart_router,
    address_router,
    checkout_router,
    marketplace_router,
)

settings = get_settings()


def _configure_logging() -> None:
    """Configure application logging once, at import time.

    Production logs identify startup, database status, and provider failures
    without ever emitting secrets (keys/tokens are never logged by the app).
    """
    level = getattr(logging, (settings.log_level or "INFO").upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        stream=sys.stdout,
        force=True,
    )
    # Reduce noisy third-party logs in production
    if settings.is_production:
        for noisy in ("chromadb", "httpx", "httpcore", "urllib3"):
            logging.getLogger(noisy).setLevel(logging.WARNING)


logger = logging.getLogger("craftsy.startup")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown event lifecycle."""
    _configure_logging()

    # 1. Ensure upload directory exists (ephemeral on Railway — object storage
    #    is a documented production requirement, see the readiness report).
    ensure_upload_dir()

    # 2. Initialize database tables
    init_db()
    ok, detail = check_database_connection()
    logger.info("Database: %s — connection %s", describe_database(), "OK" if ok else f"FAILED ({detail})")

    # 3. Optionally pre-warm the rembg ONNX model.
    #    Disabled by default: downloading a model on every container cold start is
    #    wasteful on Railway. The session is created lazily on first request instead.
    if settings.warmup_models_enabled:
        def _warmup_models():
            try:
                from ML.image_pipeline.processors.background_removal import get_rembg_session
                get_rembg_session()
                logger.info("rembg model warm-up complete.")
            except Exception as exc:  # noqa: BLE001
                logger.warning("rembg model warm-up skipped: %s", exc)

        import threading
        threading.Thread(target=_warmup_models, daemon=True).start()
    else:
        logger.info("Model warm-up disabled (lazy-load on first request).")

    base = f"http://{settings.host}:{settings.port}"
    logger.info(
        "✨ %s v%s started | env=%s | db=%s",
        settings.app_name,
        settings.app_version,
        settings.environment,
        describe_database(),
    )
    logger.info("Swagger UI: %s/docs | Health: %s/api/v1/health", base, base)

    yield

    logger.info("%s shutting down.", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS Middleware ──────────────────────────────────────────────────────────
# Origins are configurable via CORS_ORIGINS. Credentials are automatically
# disabled if a wildcard origin is configured (guarded in Settings).
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# ── Mount Uploaded Static Files ──────────────────────────────────────────────
upload_path = ensure_upload_dir()
app.mount(settings.static_url_prefix, StaticFiles(directory=str(upload_path)), name="uploads")

# ── Register Routers ─────────────────────────────────────────────────────────
app.include_router(health_router)
app.include_router(voice_router)
app.include_router(pricing_router)
app.include_router(products_router)
app.include_router(catalog_router)
app.include_router(auth_router)
app.include_router(social_router)
app.include_router(chat_router)
app.include_router(commerce_router)
app.include_router(orders_router)
app.include_router(commerce_hub_router)
app.include_router(bhashini_router)
app.include_router(cart_router)
app.include_router(address_router)
app.include_router(checkout_router)
app.include_router(marketplace_router)


@app.get("/", tags=["Root"])
async def root():
    """Welcome index endpoint."""
    return {
        "message": "Welcome to Craftsy API Gateway",
        "version": settings.app_version,
        "environment": settings.environment,
        "docs": "/docs",
        "health": "/api/v1/health",
        "voice_pipeline": "/api/v1/voice/process",
        "pricing_status": "/api/v1/pricing/status",
        "products": "/api/v1/products",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=settings.port,
        reload=True,
    )
