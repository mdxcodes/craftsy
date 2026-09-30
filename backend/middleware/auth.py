"""
Authentication Middleware and Dependencies.

Provides token-based authentication for the Craftsy backend.
Tokens are HMAC-SHA256 signed payloads containing the artisan phone and expiry.
"""

import base64
import hashlib
import hmac
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session

from ..config import get_settings
from ..database import get_db
from ..models.db_models import ArtisanDB

logger = logging.getLogger(__name__)

settings = get_settings()


def _get_secret_key() -> str:
    key = settings.auth_secret_key.strip()
    if not key:
        if settings.environment.lower() in {"development", "test"}:
            logger.warning("AUTH_SECRET_KEY is not set; using insecure development fallback.")
            return "dev-secret-key-do-not-use-in-production"
        raise RuntimeError(
            "AUTH_SECRET_KEY is not configured. "
            "Set it in the environment to enable secure token authentication."
        )
    return key


def _sign_token(payload: dict) -> str:
    key = _get_secret_key().encode()
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode()
    signature = hmac.new(key, payload_bytes, hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(payload_bytes + signature).decode()
    return token


def _verify_token(token: str) -> dict:
    try:
        raw = base64.urlsafe_b64decode(token.encode())
        payload_bytes = raw[:-32]
        signature = raw[-32:]
        key = _get_secret_key().encode()
        expected = hmac.new(key, payload_bytes, hashlib.sha256).digest()
        if not hmac.compare_digest(signature, expected):
            raise HTTPException(status_code=401, detail="Invalid token signature")
        payload = json.loads(payload_bytes.decode())
        return payload
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(phone: str, expiry_minutes: Optional[int] = None) -> str:
    minutes = expiry_minutes or settings.auth_token_expiry_minutes
    payload = {
        "phone": phone,
        "exp": (datetime.now(timezone.utc) + timedelta(minutes=minutes)).isoformat(),
    }
    return _sign_token(payload)


def get_current_artisan(
    request: Request,
    db: Session = Depends(get_db),
) -> ArtisanDB:
    """
    FastAPI dependency that extracts and validates the current artisan
    from the Bearer token in the Authorization header.

    Token is an HMAC-SHA256 signed payload containing phone and expiry.

    Raises:
        HTTPException 401: If no token, invalid token, or artisan not found.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Not authenticated")

    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = parts[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")

    payload = _verify_token(token)

    phone = payload.get("phone")
    if not phone:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    artisan = db.query(ArtisanDB).filter(ArtisanDB.phone == phone).first()
    if not artisan:
        raise HTTPException(status_code=401, detail="Invalid token")

    return artisan


def get_current_artisan_optional(
    request: Request,
    db: Session = Depends(get_db),
) -> Optional[ArtisanDB]:
    """
    Optional authentication — returns None if no valid token.
    Useful for endpoints that work for both authenticated and anonymous users.
    """
    try:
        return get_current_artisan(request, db)
    except HTTPException:
        return None
