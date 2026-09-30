"""
Consumer Order Tests.

Validates:
1. GET /api/v1/orders/my — consumer order history (auth required, own orders only)
2. GET /api/v1/orders/my/{id} — consumer order detail with full data
3. Ownership: another user's order returns 404
4. PATCH /orders/{id}/status — seller-only authorization
5. Shipment stays in sync with order status
6. Cart stock validation errors
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


def _create_user(db, phone="9876543210", role="customer"):
    user = ArtisanDB(
        id=f"user_{phone[-4:]}",
        name=f"Test {role.title()}",
        phone=phone,
        craft_type="Test Craft",
        location_cluster="Test Cluster",
        state="Test State",
        preferred_language="en",
        role=role,
    )
    db.add(user)
    db.commit()
    return user


def _create_product(db, artisan_id, price=500.0, stock=10):
    product = ProductDB(
        id=f"prod_{artisan_id}_{int(price)}",
        artisan_id=artisan_id,
        title=f"Product {int(price)}",
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


def _checkout(client, token, address_id, items):
    return client.post(
        "/api/v1/orders/checkout",
        json={
            "items": items,
            "address_id": address_id,
            "payment_method": "cod",
        },
        headers=_headers(token),
    )


# ── Consumer Order History (/orders/my) ──────────────────────────────────────


def test_my_orders_requires_auth(client):
    response = client.get("/api/v1/orders/my")
    assert response.status_code == 401


def test_my_orders_empty_initially(client, db):
    user = _create_user(db)
    token = _auth_token(user.phone)

    response = client.get("/api/v1/orders/my", headers=_headers(token))
    assert response.status_code == 200
    assert response.json() == {"total": 0, "orders": []}


def test_my_orders_returns_only_own_orders(client, db):
    seller = _create_user(db, phone="9000000001", role="artisan")
    buyer1 = _create_user(db, phone="9000000002")
    buyer2 = _create_user(db, phone="9000000003")
    product = _create_product(db, seller.id)
    addr1 = _create_address(db, buyer1.id)
    addr2 = _create_address(db, buyer2.id)

    r1 = _checkout(
        client, _auth_token(buyer1.phone), addr1.id,
        [{"product_id": product.id, "quantity": 1}],
    )
    assert r1.status_code == 201
    r2 = _checkout(
        client, _auth_token(buyer2.phone), addr2.id,
        [{"product_id": product.id, "quantity": 1}],
    )
    assert r2.status_code == 201

    # buyer1 sees only their own order
    response = client.get(
        "/api/v1/orders/my", headers=_headers(_auth_token(buyer1.phone))
    )
    data = response.json()
    assert data["total"] == 1
    assert len(data["orders"]) == 1
    assert data["orders"][0]["id"] == r1.json()["id"]


def test_my_orders_summary_shape(client, db):
    seller = _create_user(db, phone="9000000001", role="artisan")
    buyer = _create_user(db, phone="9000000002")
    p1 = _create_product(db, seller.id, price=100.0)
    p2 = _create_product(db, seller.id, price=200.0)
    address = _create_address(db, buyer.id)

    r = _checkout(
        client, _auth_token(buyer.phone), address.id,
        [
            {"product_id": p1.id, "quantity": 2},
            {"product_id": p2.id, "quantity": 1},
        ],
    )
    assert r.status_code == 201

    response = client.get(
        "/api/v1/orders/my", headers=_headers(_auth_token(buyer.phone))
    )
    order = response.json()["orders"][0]
    assert order["item_count"] == 2
    assert order["quantity"] == 3
    assert order["total_amount"] == 400.0
    assert order["status"] == "new"
    assert order["first_item_title"] == "Product 100"
    assert order["placed_at"] is not None


def test_my_orders_supports_pagination(client, db):
    seller = _create_user(db, phone="9000000001", role="artisan")
    buyer = _create_user(db, phone="9000000002")
    product = _create_product(db, seller.id)
    address = _create_address(db, buyer.id)

    for _ in range(3):
        r = _checkout(
            client, _auth_token(buyer.phone), address.id,
            [{"product_id": product.id, "quantity": 1}],
        )
        assert r.status_code == 201

    page = client.get(
        "/api/v1/orders/my?limit=2&offset=0",
        headers=_headers(_auth_token(buyer.phone)),
    ).json()
    assert page["total"] == 3
    assert len(page["orders"]) == 2


# ── Consumer Order Detail (/orders/my/{id}) ──────────────────────────────────


def test_my_order_detail_returns_full_data(client, db):
    seller = _create_user(db, phone="9000000001", role="artisan")
    buyer = _create_user(db, phone="9000000002")
    product = _create_product(db, seller.id, price=300.0)
    address = _create_address(db, buyer.id)

    r = _checkout(
        client, _auth_token(buyer.phone), address.id,
        [{"product_id": product.id, "quantity": 2}],
    )
    order_id = r.json()["id"]

    response = client.get(
        f"/api/v1/orders/my/{order_id}",
        headers=_headers(_auth_token(buyer.phone)),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["status"] == "new"
    assert data["total_amount"] == 600.0
    assert len(data["items"]) == 1
    assert data["items"][0]["product_title"] == "Product 300"
    assert data["items"][0]["total_price"] == 600.0
    # Payment + shipment + address present
    assert data["payment"]["method"] == "cod"
    assert data["payment"]["status"] == "pending"
    assert data["shipment"]["status"] == "pending"
    assert data["address"]["city"] == "Delhi"


def test_my_order_detail_forbidden_for_other_user(client, db):
    """Another user's order must return 404, never leak data."""
    seller = _create_user(db, phone="9000000001", role="artisan")
    buyer = _create_user(db, phone="9000000002")
    intruder = _create_user(db, phone="9000000003")
    product = _create_product(db, seller.id)
    address = _create_address(db, buyer.id)

    r = _checkout(
        client, _auth_token(buyer.phone), address.id,
        [{"product_id": product.id, "quantity": 1}],
    )
    order_id = r.json()["id"]

    response = client.get(
        f"/api/v1/orders/my/{order_id}",
        headers=_headers(_auth_token(intruder.phone)),
    )
    assert response.status_code == 404


def test_my_order_detail_nonexistent_returns_404(client, db):
    user = _create_user(db)
    response = client.get(
        "/api/v1/orders/my/ord_doesnotexist",
        headers=_headers(_auth_token(user.phone)),
    )
    assert response.status_code == 404


# ── Artisan status update + shipment sync ────────────────────────────────────


def test_status_update_requires_auth(client, db):
    seller = _create_user(db, phone="9000000001", role="artisan")
    buyer = _create_user(db, phone="9000000002")
    product = _create_product(db, seller.id)
    address = _create_address(db, buyer.id)

    r = _checkout(
        client, _auth_token(buyer.phone), address.id,
        [{"product_id": product.id, "quantity": 1}],
    )
    order_id = r.json()["id"]

    response = client.patch(f"/api/v1/orders/{order_id}/status?status=confirmed")
    assert response.status_code == 401


def test_status_update_rejected_for_non_seller(client, db):
    seller = _create_user(db, phone="9000000001", role="artisan")
    buyer = _create_user(db, phone="9000000002")
    intruder = _create_user(db, phone="9000000003", role="artisan")
    product = _create_product(db, seller.id)
    address = _create_address(db, buyer.id)

    r = _checkout(
        client, _auth_token(buyer.phone), address.id,
        [{"product_id": product.id, "quantity": 1}],
    )
    order_id = r.json()["id"]

    response = client.patch(
        f"/api/v1/orders/{order_id}/status?status=confirmed",
        headers=_headers(_auth_token(intruder.phone)),
    )
    assert response.status_code == 403


def test_status_update_by_seller_syncs_shipment(client, db):
    seller = _create_user(db, phone="9000000001", role="artisan")
    buyer = _create_user(db, phone="9000000002")
    product = _create_product(db, seller.id)
    address = _create_address(db, buyer.id)

    r = _checkout(
        client, _auth_token(buyer.phone), address.id,
        [{"product_id": product.id, "quantity": 1}],
    )
    order_id = r.json()["id"]

    # Seller confirms → packs → ships → delivers
    for status in ("confirmed", "packed", "shipped", "delivered"):
        resp = client.patch(
            f"/api/v1/orders/{order_id}/status?status={status}",
            headers=_headers(_auth_token(seller.phone)),
        )
        assert resp.status_code == 200

    # Consumer sees final state with shipment in step
    detail = client.get(
        f"/api/v1/orders/my/{order_id}",
        headers=_headers(_auth_token(buyer.phone)),
    ).json()
    assert detail["status"] == "delivered"
    assert detail["shipment"]["status"] == "delivered"
    assert detail["delivered_at"] is not None


# ── Cart stock validation ────────────────────────────────────────────────────


def test_add_to_cart_rejects_non_live_product(client, db):
    seller = _create_user(db, phone="9000000001", role="artisan")
    product = _create_product(db, seller.id)
    product.status = "draft"
    db.commit()

    response = client.post(
        "/api/v1/cart/items",
        json={"product_id": product.id, "quantity": 1},
        headers=_headers(_auth_token(seller.phone)),
    )
    assert response.status_code == 400


def test_add_to_cart_rejects_insufficient_stock(client, db):
    seller = _create_user(db, phone="9000000001", role="artisan")
    buyer = _create_user(db, phone="9000000002")
    product = _create_product(db, seller.id, stock=2)

    response = client.post(
        "/api/v1/cart/items",
        json={"product_id": product.id, "quantity": 5},
        headers=_headers(_auth_token(buyer.phone)),
    )
    assert response.status_code == 409


def test_cart_includes_product_details_and_subtotal(client, db):
    seller = _create_user(db, phone="9000000001", role="artisan")
    buyer = _create_user(db, phone="9000000002")
    p1 = _create_product(db, seller.id, price=100.0)
    p2 = _create_product(db, seller.id, price=250.0)

    client.post(
        "/api/v1/cart/items",
        json={"product_id": p1.id, "quantity": 2},
        headers=_headers(_auth_token(buyer.phone)),
    )
    client.post(
        "/api/v1/cart/items",
        json={"product_id": p2.id, "quantity": 1},
        headers=_headers(_auth_token(buyer.phone)),
    )

    response = client.get(
        "/api/v1/cart", headers=_headers(_auth_token(buyer.phone))
    )
    data = response.json()
    assert data["subtotal"] == 450.0
    item1 = next(i for i in data["items"] if i["product_id"] == p1.id)
    assert item1["title"] == "Product 100"
    assert item1["image_url"] == "https://example.com/image.jpg"
    assert item1["stock"] == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
