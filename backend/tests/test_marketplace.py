"""
Marketplace API Tests.

Validates:
1. Public product listing (no auth required)
2. Public product detail
3. Category listing
4. Search/filter functionality
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


def _create_artisan(db, phone="9876543210"):
    artisan = ArtisanDB(
        id=f"artisan_{phone[-4:]}",
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


# ── Public Product Listing Tests ─────────────────────────────────────────────


def test_marketplace_products_returns_live_products(client, db):
    """GET /api/v1/marketplace/products should return only live products."""
    artisan = _create_artisan(db)
    p1 = _create_product(db, artisan.id, title="Vase", price=500.0, status="live")
    p2 = _create_product(db, artisan.id, title="Bowl", price=300.0, status="live")
    p3 = _create_product(db, artisan.id, title="Draft Item", price=100.0, status="draft")
    p4 = _create_product(db, artisan.id, title="Archived Item", price=200.0, status="archived")

    response = client.get("/api/v1/marketplace/products")
    assert response.status_code == 200
    data = response.json()
    titles = [p["title"] for p in data]
    assert "Vase" in titles
    assert "Bowl" in titles
    assert "Draft Item" not in titles
    assert "Archived Item" not in titles


def test_marketplace_products_no_auth_required(client, db):
    """Marketplace products should be accessible without authentication."""
    artisan = _create_artisan(db)
    _create_product(db, artisan.id)

    # No Authorization header
    response = client.get("/api/v1/marketplace/products")
    assert response.status_code == 200


def test_marketplace_products_empty_list(client, db):
    """Should return empty list when no live products exist."""
    response = client.get("/api/v1/marketplace/products")
    assert response.status_code == 200
    assert response.json() == []


def test_marketplace_products_filter_by_category(client, db):
    """Should filter products by category."""
    artisan = _create_artisan(db)
    _create_product(db, artisan.id, title="Pottery Vase", category="Pottery")
    _create_product(db, artisan.id, title="Silk Scarf", category="Textile")

    response = client.get("/api/v1/marketplace/products?category=Pottery")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Pottery Vase"


def test_marketplace_products_search_by_title(client, db):
    """Should search products by title."""
    artisan = _create_artisan(db)
    _create_product(db, artisan.id, title="Terracotta Vase")
    _create_product(db, artisan.id, title="Silk Scarf")

    response = client.get("/api/v1/marketplace/products?search=vase")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Terracotta Vase"


# ── Public Product Detail Tests ─────────────────────────────────────────────


def test_marketplace_product_detail_returns_product(client, db):
    """GET /api/v1/marketplace/products/{id} should return product details."""
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id)

    response = client.get(f"/api/v1/marketplace/products/{product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product.id
    assert data["title"] == product.title
    assert data["price"] == product.price


def test_marketplace_product_detail_no_auth_required(client, db):
    """Product detail should be accessible without authentication."""
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id)

    response = client.get(f"/api/v1/marketplace/products/{product.id}")
    assert response.status_code == 200


def test_marketplace_product_detail_returns_404_for_nonexistent(client, db):
    """Should return 404 for nonexistent product."""
    response = client.get("/api/v1/marketplace/products/nonexistent")
    assert response.status_code == 404


def test_marketplace_product_detail_returns_404_for_draft(client, db):
    """Should return 404 for non-live products."""
    artisan = _create_artisan(db)
    product = _create_product(db, artisan.id, status="draft")

    response = client.get(f"/api/v1/marketplace/products/{product.id}")
    assert response.status_code == 404


# ── Category Tests ───────────────────────────────────────────────────────────


def test_marketplace_categories_returns_unique_categories(client, db):
    """GET /api/v1/marketplace/categories should return unique categories."""
    artisan = _create_artisan(db)
    _create_product(db, artisan.id, title="Vase 1", category="Pottery")
    _create_product(db, artisan.id, title="Vase 2", category="Pottery")
    _create_product(db, artisan.id, title="Scarf", category="Textile")

    response = client.get("/api/v1/marketplace/categories")
    assert response.status_code == 200
    data = response.json()
    assert "Pottery" in data
    assert "Textile" in data


def test_marketplace_categories_no_auth_required(client, db):
    """Categories should be accessible without authentication."""
    artisan = _create_artisan(db)
    _create_product(db, artisan.id)

    response = client.get("/api/v1/marketplace/categories")
    assert response.status_code == 200


def test_marketplace_categories_empty_list(client, db):
    """Should return empty list when no products exist."""
    response = client.get("/api/v1/marketplace/categories")
    assert response.status_code == 200
    assert response.json() == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
