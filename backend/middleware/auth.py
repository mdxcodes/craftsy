"""
Authentication Middleware and Dependencies.

Provides token-based authentication for the Craftsy backend.
Uses the existing mock JWT token format: mock_jwt_token_{phone}
"""

from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.db_models import ArtisanDB


def get_current_artisan(
    request: Request,
    db: Session = Depends(get_db),
) -> ArtisanDB:
    """
    FastAPI dependency that extracts and validates the current artisan
    from the Bearer token in the Authorization header.

    Token format: mock_jwt_token_{phone}

    Raises:
        HTTPException 401: If no token, invalid token, or artisan not found.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Expected format: "Bearer mock_jwt_token_{phone}"
    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = parts[1]

    # Extract phone from token format: mock_jwt_token_{phone}
    if not token.startswith("mock_jwt_token_"):
        raise HTTPException(status_code=401, detail="Invalid token")

    phone = token.replace("mock_jwt_token_", "")

    # Look up artisan by phone
    artisan = db.query(ArtisanDB).filter(ArtisanDB.phone == phone).first()
    if not artisan:
        raise HTTPException(status_code=401, detail="Invalid token")

    return artisan


def get_current_artisan_optional(
    request: Request,
    db: Session = Depends(get_db),
) -> ArtisanDB | None:
    """
    Optional authentication — returns None if no valid token.
    Useful for endpoints that work for both authenticated and anonymous users.
    """
    try:
        return get_current_artisan(request, db)
    except HTTPException:
        return None
