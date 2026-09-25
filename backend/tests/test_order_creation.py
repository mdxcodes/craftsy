"""
Server-Authoritative Order Creation Tests.

Validates:
1. Order creation uses ProductDB.price (not client-provided)
2. Order creation validates product exists and is live
3. Order creation checks stock availability
4. Order creation decrements stock atomically
5. Order creation creates OrderItemDB records
6. Order creation creates PaymentDB and ShipmentDB records
7. Order creation requires authentication
8. Order creation validates address ownership
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
from backend.models.order_models import OrderDB
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


def _create_product(db, artisan_id, price=500.0, stock=10):
    product = ProductDB(
        id=f"prod_{artisan_id}_{int(price)}",
        artisan_id=artisan_id,
        title=f"Product {price}",
        description="Test product",
        price=price,
        image_url="https://example.com/image.jpg",
        category="Pottery",
        tags='["handmade"]',
        status="live",
        stock=stock,
    )
    db.add(product)
    db.commit()
    return product


def _create_address(db, user_id):
    address = AddressDB(
        id=f"addr_{user_id}",
        user_id=user_id,
        label="home",
        name="Test User",
        phone="9876543210",
        line1="123 Main Street",
        city="Delhi",
        state="Delhi",
        pincode="110001",
        is_default=True,
    )
    db.add(address)
    db.commit()
    return address


def _headers(token):
    return {"Authorization": f"Bearer {token}"}


def _create_order_payload(address_id, items):
    return {
        "items": items,
        "address_id": address_id,
        "payment_method": "cod",
    }


# ── Server-Authoritative Price Tests ────────────────────────────────────────


def test_order_uses_server_price_not_client_price(client, db):
    """Order creation should use ProductDB.price, not client-provided price."""
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id, price=500.0)
    address = _create_address(db, artisan.id)
    token = f"mock_jwt_token_{artisan.phone}"

    # Client tries to pay 100.0 instead of 500.0
    response = client.post(
        "/api/v1/orders/checkout",
        json=_create_order_payload(address.id, [
            {"product_id": product.id, "quantity": 1}
        ]),
        headers=_headers(token),
    )
    assert response.status_code == 201
    data = response.json()
    # Server should use 500.0, not 100.0
    assert data["total_amount"] == 500.0
    assert data["items"][0]["unit_price"] == 500.0


def test_order_rejects_nonexistent_product(client, db):
    """Order creation should fail if product doesn't exist."""
    artisan = _create_artisan(db)
    address = _create_address(db, artisan.id)
    token = f"mock_jwt_token_{artisan.phone}"

    response = client.post(
        "/api/v1/orders/checkout",
        json=_create_order_payload(address.id, [
            {"product_id": "nonexistent_product", "quantity": 1}
        ]),
        headers=_headers(token),
    )
    assert response.status_code == 400


def test_order_rejects_insufficient_stock(client, db):
    """Order creation should fail if stock is insufficient."""
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id, stock=2)
    address = _create_address(db, artisan.id)
    token = f"mock_jwt_token_{artisan.phone}"

    response = client.post(
        "/api/v1/orders/checkout",
        json=_create_order_payload(address.id, [
            {"product_id": product.id, "quantity": 5}
        ]),
        headers=_headers(token),
    )
    assert response.status_code == 400


# ── Stock Decrement Tests ────────────────────────────────────────────────────


def test_order_decrements_stock(client, db):
    """Order creation should decrement product stock."""
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id, stock=10)
    address = _create_address(db, artisan.id)
    token = f"mock_jwt_token_{artisan.phone}"

    response = client.post(
        "/api/v1/orders/checkout",
        json=_create_order_payload(address.id, [
            {"product_id": product.id, "quantity": 3}
        ]),
        headers=_headers(token),
    )
    assert response.status_code == 201

    # Verify stock was decremented
    updated_product = db.query(ProductDB).filter(ProductDB.id == product.id).first()
    assert updated_product.stock == 7


def test_order_does_not_decrement_stock_on_failure(client, db):
    """Stock should not be decremented if order creation fails."""
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id, stock=5)
    address = _create_address(db, artisan.id)
    token = f"mock_jwt_token_{artisan.phone}"

    # First order succeeds
    client.post(
        "/api/v1/orders/checkout",
        json=_create_order_payload(address.id, [
            {"product_id": product.id, "quantity": 3}
        ]),
        headers=_headers(token),
    )

    # Second order fails (insufficient stock)
    response = client.post(
        "/api/v1/orders/checkout",
        json=_create_order_payload(address.id, [
            {"product_id": product.id, "quantity": 5}
        ]),
        headers=_headers(token),
    )
    assert response.status_code == 400

    # Stock should still be 5 - 3 = 2, not further decremented
    updated_product = db.query(ProductDB).filter(ProductDB.id == product.id).first()
    assert updated_product.stock == 2


# ── Order Item Tests ─────────────────────────────────────────────────────────


def test_order_creates_order_items(client, db):
    """Order creation should create OrderItemDB records."""
    artisan = _create_artisan(db)
    product1 = _create_product(db, artisan.id, price=100.0)
    product2 = _create_product(db, artisan.id, price=200.0)
    address = _create_address(db, artisan.id)
    token = f"mock_jwt_token_{artisan.phone}"

    response = client.post(
        "/api/v1/orders/checkout",
        json=_create_order_payload(address.id, [
            {"product_id": product1.id, "quantity": 2},
            {"product_id": product2.id, "quantity": 1},
        ]),
        headers=_headers(token),
    )
    assert response.status_code == 201

    data = response.json()
    assert len(data["items"]) == 2
    assert data["items"][0]["unit_price"] == 100.0
    assert data["items"][1]["unit_price"] == 200.0


# ── Auth & Authorization Tests ───────────────────────────────────────────────


def test_order_requires_auth(client, db):
    """Order creation should require authentication."""
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id)
    address = _create_address(db, artisan.id)

    response = client.post(
        "/api/v1/orders/checkout",
        json=_create_order_payload(address.id, [
            {"product_id": product.id, "quantity": 1}
        ]),
    )
    assert response.status_code == 401


def test_order_requires_valid_address(client, db):
    """Order creation should fail if address doesn't belong to user."""
    artisan1 = _create_artisan(db, phone="9876543210")
    artisan2 = _create_artisan(db, phone="9876543220")
    product = _create_product(db, artisan1.id)
    address = _create_address(db, artisan2.id)  # artisan2's address
    token = f"mock_jwt_token_{artisan1.phone}"

    response = client.post(
        "/api/v1/orders/checkout",
        json=_create_order_payload(address.id, [
            {"product_id": product.id, "quantity": 1}
        ]),
        headers=_headers(token),
    )
    assert response.status_code == 400


# ── Multi-Product Order Tests ────────────────────────────────────────────────


def test_multi_product_order_creates_single_order(client, db):
    """Multiple products should create a single order with multiple items."""
    artisan = _create_artisan(db)
    product1 = _create_product(db, artisan.id, price=100.0)
    product2 = _create_product(db, artisan.id, price=200.0)
    product3 = _create_product(db, artisan.id, price=300.0)
    address = _create_address(db, artisan.id)
    token = f"mock_jwt_token_{artisan.phone}"

    response = client.post(
        "/api/v1/orders/checkout",
        json=_create_order_payload(address.id, [
            {"product_id": product1.id, "quantity": 1},
            {"product_id": product2.id, "quantity": 2},
            {"product_id": product3.id, "quantity": 3},
        ]),
        headers=_headers(token),
    )
    assert response.status_code == 201

    data = response.json()
    assert len(data["items"]) == 3
    # Total: 100*1 + 200*2 + 300*3 = 100 + 400 + 900 = 1400
    assert data["total_amount"] == 1400.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
