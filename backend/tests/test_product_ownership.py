"""
Product Ownership & Authorization Tests.

Validates:
1. Authenticated artisans can only manage their own products.
2. Unauthenticated requests to product endpoints return 401.
3. Marketplace returns products from all artisans.
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
from backend.middleware.auth import create_access_token


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


def _create_artisan(db, phone="9876543210"):
    artisan = ArtisanDB(
        id=f"artisan_{phone[-4:]}",
        name=f"Test Artisan {phone[-4:]}",
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


def _create_product(db, artisan_id, title="Test Product", price=500.0,
                    category="Pottery", status="live", stock=10):
    product = ProductDB(
        id=f"prod_{title.replace(' ', '_').lower()}_{int(price)}",
        artisan_id=artisan_id,
        title=title,
        description=f"Description for {title}",
        price=price,
        image_url="https://example.com/image.jpg",
        category=category,
        tags='["handmade"]',
        status=status,
        stock=stock,
    )
    db.add(product)
    db.commit()
    return product


def _headers(phone: str) -> dict:
    return {"X-User-Id": f"artisan_{phone[-4:]}"}


# ── Product Listing Ownership ─────────────────────────────────────────────────


def test_list_products_requires_auth(client, db):
    """GET /api/v1/products without X-User-Id returns 401."""
    response = client.get("/api/v1/products")
    assert response.status_code == 401


def test_list_products_returns_only_own_products(client, db):
    """Artisan A sees only their own products."""
    artisan_a = _create_artisan(db, phone="9876543210")
    artisan_b = _create_artisan(db, phone="9876543220")
    _create_product(db, artisan_a.id, title="Product A1", price=100.0)
    _create_product(db, artisan_a.id, title="Product A2", price=200.0)
    _create_product(db, artisan_b.id, title="Product B1", price=300.0)

    response = client.get("/api/v1/products", headers=_headers("9876543210"))
    assert response.status_code == 200
    data = response.json()
    titles = [p["title"] for p in data]
    assert "Product A1" in titles
    assert "Product A2" in titles
    assert "Product B1" not in titles


def test_list_products_different_artisans_isolated(client, db):
    """Artisan B does not see Artisan A's products."""
    artisan_a = _create_artisan(db, phone="9876543210")
    artisan_b = _create_artisan(db, phone="9876543220")
    _create_product(db, artisan_a.id, title="Product A1", price=100.0)
    _create_product(db, artisan_b.id, title="Product B1", price=300.0)

    response = client.get("/api/v1/products", headers=_headers("9876543220"))
    assert response.status_code == 200
    data = response.json()
    titles = [p["title"] for p in data]
    assert "Product B1" in titles
    assert "Product A1" not in titles


# ── Product Creation Ownership ────────────────────────────────────────────────


def test_create_product_ignores_client_artisan_id(client, db):
    """Client-supplied artisan_id is ignored; product is owned by authenticated artisan."""
    artisan_a = _create_artisan(db, phone="9876543210")
    artisan_b = _create_artisan(db, phone="9876543220")

    payload = {
        "id": "prod_client_override",
        "title": "Override Test",
        "description": "Should be owned by A",
        "price": 500.0,
        "image_url": "https://example.com/img.jpg",
        "category": "Pottery",
        "tags": ["test"],
        "status": "live",
        "artisan_id": artisan_b.id,
    }

    response = client.post("/api/v1/products", json=payload, headers=_headers("9876543210"))
    assert response.status_code == 201
    data = response.json()
    assert data["artisan_id"] == artisan_a.id


def test_create_product_requires_auth(client, db):
    """POST /api/v1/products without X-User-Id returns 401."""
    payload = {
        "title": "No Auth Product",
        "description": "Test",
        "price": 500.0,
        "image_url": "https://example.com/img.jpg",
        "category": "Pottery",
        "tags": ["test"],
        "status": "live",
    }

    response = client.post("/api/v1/products", json=payload)
    assert response.status_code == 401


# ── Product Update Ownership ──────────────────────────────────────────────────


def test_update_own_product_succeeds(client, db):
    """Artisan A can update their own product."""
    artisan_a = _create_artisan(db, phone="9876543210")
    product = _create_product(db, artisan_a.id, title="Original Title")

    response = client.put(
        f"/api/v1/products/{product.id}",
        json={"title": "Updated Title"},
        headers=_headers("9876543210"),
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


def test_update_other_artisan_product_returns_403(client, db):
    """Artisan B cannot update Artisan A's product."""
    artisan_a = _create_artisan(db, phone="9876543210")
    artisan_b = _create_artisan(db, phone="9876543220")
    product = _create_product(db, artisan_a.id, title="Product A")

    response = client.put(
        f"/api/v1/products/{product.id}",
        json={"title": "Hacked Title"},
        headers=_headers("9876543220"),
    )
    assert response.status_code == 403


# ── Product Delete Ownership ──────────────────────────────────────────────────


def test_delete_own_product_succeeds(client, db):
    """Artisan A can delete their own product."""
    artisan_a = _create_artisan(db, phone="9876543210")
    product = _create_product(db, artisan_a.id, title="To Delete")

    response = client.delete(f"/api/v1/products/{product.id}", headers=_headers("9876543210"))
    assert response.status_code == 200
    assert response.json()["deleted_id"] == product.id


def test_delete_other_artisan_product_returns_403(client, db):
    """Artisan B cannot delete Artisan A's product."""
    artisan_a = _create_artisan(db, phone="9876543210")
    artisan_b = _create_artisan(db, phone="9876543220")
    product = _create_product(db, artisan_a.id, title="Protected Product")

    response = client.delete(f"/api/v1/products/{product.id}", headers=_headers("9876543220"))
    assert response.status_code == 403


def test_delete_product_requires_auth(client, db):
    """DELETE /api/v1/products/{id} without X-User-Id returns 401."""
    response = client.delete("/api/v1/products/nonexistent")
    assert response.status_code == 401


# ── Product Sync Ownership ────────────────────────────────────────────────────


def test_sync_products_sets_authenticated_artisan_id(client, db):
    """Synced products are owned by the authenticated artisan, not the client-supplied artisan_id."""
    artisan_a = _create_artisan(db, phone="9876543210")
    artisan_b = _create_artisan(db, phone="9876543220")

    payload = {
        "products": [
            {
                "id": "sync_prod_1",
                "title": "Synced Product",
                "description": "From offline",
                "price": 1000.0,
                "image_url": "https://example.com/img.jpg",
                "category": "Pottery",
                "tags": ["offline"],
                "status": "live",
            }
        ]
    }

    response = client.post("/api/v1/products/sync", json=payload, headers=_headers("9876543210"))
    assert response.status_code == 200
    data = response.json()
    assert data["synced_count"] == 1
    assert data["products"][0]["artisan_id"] == artisan_a.id


def test_sync_products_requires_auth(client, db):
    """POST /api/v1/products/sync without X-User-Id returns 401."""
    payload = {"products": []}
    response = client.post("/api/v1/products/sync", json=payload)
    assert response.status_code == 401


# ── Marketplace Public Access ─────────────────────────────────────────────────


def test_marketplace_returns_products_from_all_artisans(client, db):
    """Marketplace returns products from all artisans, not just the authenticated one."""
    artisan_a = _create_artisan(db, phone="9876543210")
    artisan_b = _create_artisan(db, phone="9876543220")
    _create_product(db, artisan_a.id, title="A Product", price=100.0, status="live")
    _create_product(db, artisan_b.id, title="B Product", price=200.0, status="live")

    response = client.get("/api/v1/marketplace/products")
    assert response.status_code == 200
    data = response.json()
    titles = [p["title"] for p in data]
    assert "A Product" in titles
    assert "B Product" in titles


def test_marketplace_ignores_x_user_id_filter(client, db):
    """Marketplace does not filter by X-User-Id."""
    artisan_a = _create_artisan(db, phone="9876543210")
    artisan_b = _create_artisan(db, phone="9876543220")
    _create_product(db, artisan_a.id, title="A Product", price=100.0, status="live")
    _create_product(db, artisan_b.id, title="B Product", price=200.0, status="live")

    # Even with X-User-Id for artisan A, marketplace should still return B's product
    response = client.get("/api/v1/marketplace/products", headers=_headers("9876543210"))
    assert response.status_code == 200
    data = response.json()
    titles = [p["title"] for p in data]
    assert "A Product" in titles
    assert "B Product" in titles


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
