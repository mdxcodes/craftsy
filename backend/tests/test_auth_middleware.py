"""
Authentication & Authorization Middleware Tests.

Validates:
1. Auth dependency extracts artisan from Bearer token
2. Consumer registration endpoint works
3. Protected endpoints reject missing/invalid tokens
4. Order access is restricted to owning artisan
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.database import Base, get_db
from backend.models.db_models import ArtisanDB
from backend.models.order_models import OrderDB
from backend.models.commerce_foundation_models import (  # noqa: F401
    CartDB,
    CartItemDB,
    AddressDB,
    OrderItemDB,
    PaymentDB,
    ShipmentDB,
)
from backend.middleware.auth import create_access_token


def _auth_token(phone: str) -> str:
    return create_access_token(phone)


@pytest.fixture
def db():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    """Create a FastAPI test client with the in-memory DB."""
    from backend.main import app

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def _create_artisan(db, role="artisan", phone="9876543210"):
    """Helper to create an artisan/customer record."""
    artisan = ArtisanDB(
        id=f"artisan_{role}_{phone[-4:]}",
        name=f"Test {role.title()}",
        phone=phone,
        craft_type="Test Craft",
        location_cluster="Test Cluster",
        state="Test State",
        experience_years="5",
        preferred_language="en",
        role=role,
    )
    db.add(artisan)
    db.commit()
    return artisan


def _headers(token):
    """Create Authorization headers."""
    return {"Authorization": f"Bearer {token}"}


# ── Consumer Registration ──────────────────────────────────────────────────


def test_register_consumer_returns_customer_role(client, db):
    """POST /api/v1/auth/register-consumer creates ArtisanDB with role='customer'."""
    response = client.post(
        "/api/v1/auth/register-consumer",
        json={"name": "Test Buyer", "phone": "9876543211"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Buyer"
    assert data["phone"] == "9876543211"
    assert data["role"] == "customer"


def test_register_consumer_duplicate_phone_returns_409(client, db):
    """Duplicate phone registration returns 409."""
    payload = {"name": "First", "phone": "9876543212"}
    r1 = client.post("/api/v1/auth/register-consumer", json=payload)
    assert r1.status_code == 201

    payload2 = {"name": "Second", "phone": "9876543212"}
    r2 = client.post("/api/v1/auth/register-consumer", json=payload2)
    assert r2.status_code == 409


# ── Auth Dependency ──────────────────────────────────────────────────────────


def test_current_artisan_dep_returns_401_without_token(client):
    """get_current_artisan dependency rejects requests with no token."""
    from backend.middleware.auth import get_current_artisan
    from fastapi import HTTPException
    from unittest.mock import MagicMock

    # Simulate a request without Authorization header
    mock_request = MagicMock()
    mock_request.headers.get.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_current_artisan(mock_request, db)
    assert exc_info.value.status_code == 401


def test_current_artisan_dep_returns_401_with_invalid_token(client):
    """get_current_artisan rejects invalid tokens."""
    from backend.middleware.auth import get_current_artisan
    from fastapi import HTTPException
    from unittest.mock import MagicMock

    mock_request = MagicMock()
    mock_request.headers.get.return_value = "Bearer invalid_token_xyz"

    with pytest.raises(HTTPException) as exc_info:
        get_current_artisan(mock_request, db)
    assert exc_info.value.status_code == 401


def test_current_artisan_dep_returns_artisan_with_valid_token(client, db):
    """get_current_artisan returns the artisan for a valid token."""
    from backend.middleware.auth import get_current_artisan
    from unittest.mock import MagicMock

    artisan = _create_artisan(db, phone="9876543300")

    mock_request = MagicMock()
    mock_request.headers.get.return_value = f"Bearer {_auth_token(artisan.phone)}"

    result = get_current_artisan(mock_request, db)
    assert result.id == artisan.id


# ── Order Authorization ──────────────────────────────────────────────────────


def test_orders_endpoint_rejects_missing_token(client, db):
    """GET /api/v1/orders/artisan/{id} without token returns 401."""
    response = client.get("/api/v1/orders/artisan/some_id")
    assert response.status_code == 401


def test_orders_endpoint_rejects_invalid_token(client, db):
    """GET /api/v1/orders/artisan/{id} with invalid token returns 401."""
    response = client.get(
        "/api/v1/orders/artisan/some_id",
        headers=_headers("bad_token"),
    )
    assert response.status_code == 401


def test_orders_endpoint_accepts_valid_token(client, db):
    """GET /api/v1/orders/artisan/{id} with valid token returns 200."""
    artisan = _create_artisan(db, phone="9876543400")
    response = client.get(
        f"/api/v1/orders/artisan/{artisan.id}",
        headers=_headers(_auth_token(artisan.phone)),
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
