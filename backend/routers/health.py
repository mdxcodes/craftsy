"""
Health and Status Router.

Endpoints:
    GET /api/v1/health        — full service status (fast, no AI calls)
    GET /api/v1/health/live   — liveness probe (process is up)
    GET /api/v1/health/ready  — readiness probe (database reachable)

None of these call Groq, Gemini, Bhashini, embeddings, or ChromaDB.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..config import get_settings
from ..database import check_database_connection, describe_database

router = APIRouter(prefix="/api/v1/health", tags=["Health"])
settings = get_settings()


@router.get("")
async def health_check():
    """Service health and version status."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "database": describe_database(),
    }


@router.get("/live")
async def liveness():
    """Liveness probe — confirms the process is serving requests."""
    return {"status": "alive"}


@router.get("/ready")
async def readiness():
    """Readiness probe — confirms the database is reachable.

    Returns 200 when ready, 503 when the database cannot be reached.
    """
    ok, detail = check_database_connection()
    payload = {
        "status": "ready" if ok else "not_ready",
        "database": describe_database(),
        "database_connected": ok,
    }
    if not ok:
        payload["detail"] = detail
        return JSONResponse(status_code=503, content=payload)
    return payload
