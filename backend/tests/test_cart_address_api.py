"""
Cart and Address API Tests.

Validates:
1. Cart creation and retrieval
2. Cart item add/update/remove
3. Address CRUD operations
4. Auth protection on all endpoints
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
from backend.models.db_models import ArtisanDB, ProductDB
from backend.models.order_models import OrderDB  # noqa: F401 — needed for FK resolution
from backend.models.commerce_foundation_models import (  # noqa: F401
    CartDB, CartItemDB, AddressDB, OrderItemDB, PaymentDB, ShipmentDB,
)


@pytest.fixture
def db():
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


def _create_artisan(db, role="customer", phone="9876543210"):
    artisan = ArtisanDB(
        id=f"artisan_{role}_{phone[-4:]}",
        name=f"Test {role.title()}",
        phone=phone,
        craft_type="Test Craft",
        location_cluster="Test Cluster",
        state="Test State",
        preferred_language="en",
        role=role,
    )
    db.add(artisan)
    db.commit()
    return artisan


def _create_product(db, artisan_id=None):
    product = ProductDB(
        id=f"prod_{artisan_id or 'test'}",
        artisan_id=artisan_id,
        title="Test Product",
        description="A test product description",
        price=500.0,
        image_url="https://example.com/image.jpg",
        category="Pottery",
        tags='["handmade"]',
        status="live",
        stock=10,
    )
    db.add(product)
    db.commit()
    return product


def _headers(token):
    return {"Authorization": f"Bearer {token}"}


# ── Cart Tests ───────────────────────────────────────────────────────────────


def test_get_cart_creates_cart_if_not_exists(client, db):
    artisan = _create_artisan(db)
    token = f"mock_jwt_token_{artisan.phone}"

    response = client.get("/api/v1/cart", headers=_headers(token))
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == artisan.id
    assert data["items"] == []


def test_add_item_to_cart(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan_id=artisan.id)
    token = f"mock_jwt_token_{artisan.phone}"

    response = client.post(
        "/api/v1/cart/items",
        json={"product_id": product.id, "quantity": 2},
        headers=_headers(token),
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product.id
    assert data["items"][0]["quantity"] == 2
    assert data["items"][0]["unit_price"] == 500.0


def test_add_item_to_cart_requires_auth(client, db):
    response = client.post(
        "/api/v1/cart/items",
        json={"product_id": "prod_test", "quantity": 1},
    )
    assert response.status_code == 401


def test_update_cart_item_quantity(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan_id=artisan.id)
    token = f"mock_jwt_token_{artisan.phone}"

    client.post(
        "/api/v1/cart/items",
        json={"product_id": product.id, "quantity": 1},
        headers=_headers(token),
    )

    cart_response = client.get("/api/v1/cart", headers=_headers(token))
    item_id = cart_response.json()["items"][0]["id"]

    response = client.put(
        f"/api/v1/cart/items/{item_id}",
        json={"quantity": 5},
        headers=_headers(token),
    )
    assert response.status_code == 200
    assert response.json()["items"][0]["quantity"] == 5


def test_remove_cart_item(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan_id=artisan.id)
    token = f"mock_jwt_token_{artisan.phone}"

    client.post(
        "/api/v1/cart/items",
        json={"product_id": product.id, "quantity": 1},
        headers=_headers(token),
    )

    cart_response = client.get("/api/v1/cart", headers=_headers(token))
    item_id = cart_response.json()["items"][0]["id"]

    response = client.delete(
        f"/api/v1/cart/items/{item_id}",
        headers=_headers(token),
    )
    assert response.status_code == 200
    assert response.json()["items"] == []


def test_clear_cart(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan_id=artisan.id)
    token = f"mock_jwt_token_{artisan.phone}"

    client.post(
        "/api/v1/cart/items",
        json={"product_id": product.id, "quantity": 1},
        headers=_headers(token),
    )

    response = client.delete("/api/v1/cart", headers=_headers(token))
    assert response.status_code == 200

    cart_response = client.get("/api/v1/cart", headers=_headers(token))
    assert cart_response.json()["items"] == []


# ── Address Tests ────────────────────────────────────────────────────────────


def test_list_addresses(client, db):
    artisan = _create_artisan(db)
    token = f"mock_jwt_token_{artisan.phone}"

    response = client.get("/api/v1/addresses", headers=_headers(token))
    assert response.status_code == 200
    assert response.json() == []


def test_create_address(client, db):
    artisan = _create_artisan(db)
    token = f"mock_jwt_token_{artisan.phone}"

    response = client.post(
        "/api/v1/addresses",
        json={
            "label": "home",
            "name": "Test User",
            "phone": "9876543210",
            "line1": "123 Main Street",
            "city": "Delhi",
            "state": "Delhi",
            "pincode": "110001",
            "is_default": True,
        },
        headers=_headers(token),
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["city"] == "Delhi"
    assert data["is_default"] is True


def test_update_address(client, db):
    artisan = _create_artisan(db)
    token = f"mock_jwt_token_{artisan.phone}"

    create_response = client.post(
        "/api/v1/addresses",
        json={
            "name": "Test User",
            "phone": "9876543210",
            "line1": "123 Main Street",
            "city": "Delhi",
            "state": "Delhi",
            "pincode": "110001",
        },
        headers=_headers(token),
    )
    address_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/addresses/{address_id}",
        json={"city": "Mumbai", "state": "Maharashtra"},
        headers=_headers(token),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Mumbai"
    assert data["state"] == "Maharashtra"


def test_delete_address(client, db):
    artisan = _create_artisan(db)
    token = f"mock_jwt_token_{artisan.phone}"

    create_response = client.post(
        "/api/v1/addresses",
        json={
            "name": "Test User",
            "phone": "9876543210",
            "line1": "123 Main Street",
            "city": "Delhi",
            "state": "Delhi",
            "pincode": "110001",
        },
        headers=_headers(token),
    )
    address_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/addresses/{address_id}",
        headers=_headers(token),
    )
    assert response.status_code == 200

    list_response = client.get("/api/v1/addresses", headers=_headers(token))
    assert len(list_response.json()) == 0


def test_address_requires_auth(client, db):
    response = client.get("/api/v1/addresses")
    assert response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
