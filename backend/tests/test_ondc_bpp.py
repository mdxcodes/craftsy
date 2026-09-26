"""ONDC Retail BPP adapter tests."""

from __future__ import annotations

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
from backend.services.ondc.idempotency import idempotency_store


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
    idempotency_store.clear()


def _create_artisan(db, phone="9876543210"):
    artisan = ArtisanDB(
        id=f"artisan_ondc_{phone[-4:]}",
        name="Test Artisan",
        phone=phone,
        craft_type="Pottery",
        location_cluster="Test Cluster",
        state="Delhi",
        preferred_language="en",
        role="artisan",
    )
    db.add(artisan)
    db.commit()
    return artisan


def _create_product(db, artisan_id, title="Terracotta Vase", price=500.0, stock=10):
    product = ProductDB(
        id=f"prod_{artisan_id[-4:]}_{title.replace(' ', '_').lower()}",
        artisan_id=artisan_id,
        title=title,
        description="Handmade terracotta vase",
        price=price,
        image_url="https://example.com/image.jpg",
        category="Pottery",
        tags='["handmade", "terracotta"]',
        status="live",
        stock=stock,
    )
    db.add(product)
    db.commit()
    return product


def _base_context(product, action="search", txn="txn-001", msg="msg-001"):
    return {
        "context": {
            "domain": "ONDC:RET10",
            "action": action,
            "version": "2.0.2",
            "bap_id": "test-buyer",
            "bap_uri": "http://localhost:9000",
            "transaction_id": txn,
            "message_id": msg,
            "timestamp": "2026-09-26T18:00:00Z",
            "ttl": "PT30S",
        },
        "message": {},
    }


# ── Search ─────────────────────────────────────────────────────────────────────


def test_search_returns_catalog(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id, title="Terracotta Vase")

    payload = _base_context(product, action="search")
    payload["message"] = {"intent": {"item": {"descriptor": {"name": "terracotta"}}}}

    response = client.post("/api/v1/ondc/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["context"]["action"] == "on_search"
    assert "catalog" in data["message"]
    assert len(data["message"]["catalog"]["bpp/items"]) >= 1
    assert data["message"]["catalog"]["bpp/items"][0]["id"] == product.id


def test_on_search_alias_works(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id)

    payload = _base_context(product, action="search")
    payload["message"] = {"intent": {"item": {"descriptor": {"name": "vase"}}}}

    response = client.post("/api/v1/ondc/on_search", json=payload)
    assert response.status_code == 200
    assert "catalog" in response.json()["message"]


def test_search_without_query_returns_all_live_products(client, db):
    artisan = _create_artisan(db)
    _create_product(db, artisan.id, title="Vase A")
    _create_product(db, artisan.id, title="Vase B")

    payload = _base_context(None, action="search")
    payload["message"] = {"intent": {}}

    response = client.post("/api/v1/ondc/search", json=payload)
    assert response.status_code == 200
    assert len(response.json()["message"]["catalog"]["bpp/items"]) == 2


# ── Select ─────────────────────────────────────────────────────────────────────


def test_select_validates_stock_and_returns_quote(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id, price=500.0, stock=5)

    payload = _base_context(product, action="select")
    payload["message"] = {
        "order": {
            "items": [
                {
                    "id": product.id,
                    "quantity": 2,
                    "price": {"currency": "INR", "value": "500"},
                }
            ]
        }
    }

    response = client.post("/api/v1/ondc/select", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["context"]["action"] == "on_select"
    assert data["message"]["order"]["state"] == "Initialized"
    assert float(data["message"]["order"]["quote"]["price"]["value"]) == 1000.0


def test_select_rejects_insufficient_stock(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id, stock=2)

    payload = _base_context(product, action="select")
    payload["message"] = {
        "order": {
            "items": [
                {
                    "id": product.id,
                    "quantity": 5,
                    "price": {"currency": "INR", "value": "500"},
                }
            ]
        }
    }

    response = client.post("/api/v1/ondc/select", json=payload)
    assert response.status_code == 400
    assert "INSUFFICIENT_STOCK" in response.json()["detail"]["error"]["code"]


# ── Init ───────────────────────────────────────────────────────────────────────


def test_init_returns_payment_and_fulfillment(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id)

    payload = _base_context(product, action="init")
    payload["message"] = {
        "order": {
            "items": [
                {
                    "id": product.id,
                    "quantity": 1,
                    "price": {"currency": "INR", "value": "500"},
                }
            ]
        }
    }

    response = client.post("/api/v1/ondc/init", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["context"]["action"] == "on_init"
    assert data["message"]["order"]["payment"]["status"] == "NOT-PAID"
    assert data["message"]["order"]["fulfillment"]["type"] == "HOME-DELIVERY"


# ── Confirm ────────────────────────────────────────────────────────────────────


def test_confirm_creates_order_and_decrements_stock(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id, price=500.0, stock=10)

    payload = _base_context(product, action="confirm", txn="txn-100", msg="msg-100")
    payload["message"] = {
        "order": {
            "items": [
                {
                    "id": product.id,
                    "quantity": 2,
                    "price": {"currency": "INR", "value": "500"},
                }
            ],
            "billing": {
                "address": {"name": "Test Buyer", "city": "Delhi"}
            },
        }
    }

    response = client.post("/api/v1/ondc/confirm", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["context"]["action"] == "on_confirm"
    assert data["message"]["order"]["state"] == "Created"
    assert data["message"]["order"]["payment"]["status"] == "PAID"

    order_id = data["message"]["order"]["id"]
    db_order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    assert db_order is not None
    assert db_order.channel == "ondc"
    assert db_order.external_order_id == "ondc_txn-100"

    db_product = db.query(ProductDB).filter(ProductDB.id == product.id).first()
    assert db_product.stock == 8


def test_confirm_is_idempotent(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id, price=500.0, stock=10)

    payload = _base_context(product, action="confirm", txn="txn-200", msg="msg-200")
    payload["message"] = {
        "order": {
            "items": [
                {
                    "id": product.id,
                    "quantity": 1,
                    "price": {"currency": "INR", "value": "500"},
                }
            ]
        }
    }

    response1 = client.post("/api/v1/ondc/confirm", json=payload)
    assert response1.status_code == 200
    order_id_1 = response1.json()["message"]["order"]["id"]

    response2 = client.post("/api/v1/ondc/confirm", json=payload)
    assert response2.status_code == 200
    order_id_2 = response2.json()["message"]["order"]["id"]

    assert order_id_1 == order_id_2

    db_product = db.query(ProductDB).filter(ProductDB.id == product.id).first()
    assert db_product.stock == 9


def test_confirm_rejects_duplicate_external_order_id(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id, price=500.0, stock=10)

    payload1 = _base_context(product, action="confirm", txn="txn-201", msg="msg-201")
    payload1["message"] = {
        "order": {
            "items": [
                {
                    "id": product.id,
                    "quantity": 1,
                    "price": {"currency": "INR", "value": "500"},
                }
            ]
        }
    }

    response1 = client.post("/api/v1/ondc/confirm", json=payload1)
    assert response1.status_code == 200
    order_id_1 = response1.json()["message"]["order"]["id"]

    payload2 = _base_context(product, action="confirm", txn="txn-201", msg="msg-202")
    payload2["message"] = {
        "order": {
            "items": [
                {
                    "id": product.id,
                    "quantity": 1,
                    "price": {"currency": "INR", "value": "500"},
                }
            ]
        }
    }

    response2 = client.post("/api/v1/ondc/confirm", json=payload2)
    assert response2.status_code == 200
    order_id_2 = response2.json()["message"]["order"]["id"]

    assert order_id_1 == order_id_2

    db_product = db.query(ProductDB).filter(ProductDB.id == product.id).first()
    assert db_product.stock == 9


def test_confirm_rejects_insufficient_stock(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id, stock=1)

    payload = _base_context(product, action="confirm", txn="txn-300", msg="msg-300")
    payload["message"] = {
        "order": {
            "items": [
                {
                    "id": product.id,
                    "quantity": 2,
                    "price": {"currency": "INR", "value": "500"},
                }
            ]
        }
    }

    response = client.post("/api/v1/ondc/confirm", json=payload)
    assert response.status_code == 400
    assert "INSUFFICIENT_STOCK" in response.json()["detail"]["error"]["code"]


# ── Status ─────────────────────────────────────────────────────────────────────


def test_status_returns_existing_order(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id)

    order = OrderDB(
        id="ord_status_01",
        artisan_id=artisan.id,
        product_id=product.id,
        product_title=product.title,
        buyer_name="Status Buyer",
        quantity=1,
        unit_price=500.0,
        total_amount=500.0,
        status="new",
        channel="ondc",
        external_order_id="ondc_status_txn",
    )
    db.add(order)
    db.commit()

    payload = _base_context(product, action="status")
    payload["message"] = {"order_id": order.id}

    response = client.post("/api/v1/ondc/status", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"]["order"]["id"] == order.id
    assert data["message"]["order"]["state"] == "Created"


def test_status_lookup_by_external_order_id(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id)

    order = OrderDB(
        id="ord_status_02",
        artisan_id=artisan.id,
        product_id=product.id,
        product_title=product.title,
        buyer_name="External Buyer",
        quantity=1,
        unit_price=500.0,
        total_amount=500.0,
        status="shipped",
        channel="ondc",
        external_order_id="ondc_external_123",
    )
    db.add(order)
    db.commit()

    payload = _base_context(product, action="status")
    payload["message"] = {"order_id": "ondc_external_123"}

    response = client.post("/api/v1/ondc/status", json=payload)
    assert response.status_code == 200
    assert response.json()["message"]["order"]["state"] == "Shipped"


# ── Validation Errors ──────────────────────────────────────────────────────────


def test_missing_context_fields_returns_400(client):
    response = client.post("/api/v1/ondc/search", json={"message": {}})
    assert response.status_code == 400
    assert "MISSING_CONTEXT_FIELDS" in response.json()["detail"]["error"]["code"]


def test_unsupported_domain_returns_400(client):
    payload = _base_context(None, action="search")
    payload["context"]["domain"] = "ONDC:UNKNOWN"

    response = client.post("/api/v1/ondc/search", json=payload)
    assert response.status_code == 400
    assert "UNSUPPORTED_DOMAIN" in response.json()["detail"]["error"]["code"]


def test_unsupported_version_returns_400(client):
    payload = _base_context(None, action="search")
    payload["context"]["version"] = "1.0.0"

    response = client.post("/api/v1/ondc/search", json=payload)
    assert response.status_code == 400
    assert "UNSUPPORTED_VERSION" in response.json()["detail"]["error"]["code"]


def test_confirm_missing_items_returns_400(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id)

    payload = _base_context(product, action="confirm", txn="txn-400", msg="msg-400")
    payload["message"] = {"order": {}}

    response = client.post("/api/v1/ondc/confirm", json=payload)
    assert response.status_code == 400
    assert "NO_ITEMS" in response.json()["detail"]["error"]["code"]


def test_status_missing_order_id_returns_400(client):
    payload = _base_context(None, action="status")
    payload["message"] = {}

    response = client.post("/api/v1/ondc/status", json=payload)
    assert response.status_code == 400
    assert "MISSING_ORDER_ID" in response.json()["detail"]["error"]["code"]


# ── Full Flow ──────────────────────────────────────────────────────────────────


def test_full_ondc_flow(client, db):
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id, title="Terracotta Vase", price=500.0, stock=10)

    txn = "txn-full"
    msg = "msg-full"

    search_payload = _base_context(product, action="search", txn=txn, msg=msg)
    search_payload["message"] = {"intent": {"item": {"descriptor": {"name": "vase"}}}}
    search_response = client.post("/api/v1/ondc/search", json=search_payload)
    assert search_response.status_code == 200
    assert len(search_response.json()["message"]["catalog"]["bpp/items"]) == 1

    select_payload = _base_context(product, action="select", txn=txn, msg=msg)
    select_payload["message"] = {
        "order": {
            "items": [
                {
                    "id": product.id,
                    "quantity": 1,
                    "price": {"currency": "INR", "value": "500"},
                }
            ]
        }
    }
    select_response = client.post("/api/v1/ondc/select", json=select_payload)
    assert select_response.status_code == 200
    assert select_response.json()["message"]["order"]["state"] == "Initialized"

    init_payload = _base_context(product, action="init", txn=txn, msg=msg)
    init_payload["message"] = select_payload["message"]
    init_response = client.post("/api/v1/ondc/init", json=init_payload)
    assert init_response.status_code == 200
    assert init_response.json()["message"]["order"]["payment"]["status"] == "NOT-PAID"

    confirm_payload = _base_context(product, action="confirm", txn=txn, msg=msg)
    confirm_payload["message"] = {
        "order": {
            "items": [
                {
                    "id": product.id,
                    "quantity": 1,
                    "price": {"currency": "INR", "value": "500"},
                }
            ],
            "billing": {"address": {"name": "Flow Buyer", "city": "Mumbai"}},
        }
    }
    confirm_response = client.post("/api/v1/ondc/confirm", json=confirm_payload)
    assert confirm_response.status_code == 200
    order_id = confirm_response.json()["message"]["order"]["id"]

    status_payload = _base_context(product, action="status", txn=txn, msg=msg)
    status_payload["message"] = {"order_id": order_id}
    status_response = client.post("/api/v1/ondc/status", json=status_payload)
    assert status_response.status_code == 200
    assert status_response.json()["message"]["order"]["state"] == "Created"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
