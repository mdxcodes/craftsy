"""
FastAPI Backend Integration Tests.

Validates:
1. Health check endpoint
2. Pricing status & suggestion (integrated with ML engine)
3. Product catalog CRUD & offline batch sync
4. AI catalog listing generation
"""

import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.main import app

client = TestClient(app)


def test_health():
    """Test /api/v1/health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_pricing_status():
    """Test /api/v1/pricing/status endpoint."""
    response = client.get("/api/v1/pricing/status")
    assert response.status_code == 200
    data = response.json()
    assert "indexed_benchmark_products" in data


def test_pricing_suggest():
    """Test /api/v1/pricing/suggest endpoint calling the ML engine."""
    payload = {
        "description": "Handcrafted terracotta floral vase sculpted on traditional potter wheel",
        "category": "Pottery",
        "raw_material_cost": 200.0,
        "labor_hours": 4.0,
        "hourly_wage": 60.0,
    }
    response = client.post("/api/v1/pricing/suggest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["suggested_price"] > 0
    assert data["floor_price"] == 440.0  # 200 + 4*60
    assert "reasoning" in data
    assert "reasoning_hi" in data
    assert len(data["comparable_products"]) > 0


def test_products_crud_and_sync():
    """Test product listing, creation, and offline batch sync."""
    res = client.get("/api/v1/products")
    assert res.status_code == 200
    initial_products = res.json()
    assert isinstance(initial_products, list)

    new_prod = {
        "title": "Test Dokra Brass Figurine",
        "description": "Lost wax cast brass craft",
        "price": 1500.0,
        "image_url": "/uploads/images/test.jpg",
        "category": "Jewelry",
        "tags": ["dokra", "brass", "tribal"],
        "status": "live",
    }
    res_create = client.post("/api/v1/products", json=new_prod)
    assert res_create.status_code == 201
    created = res_create.json()
    prod_id = created["id"]

    res_get = client.get(f"/api/v1/products/{prod_id}")
    assert res_get.status_code == 200
    assert res_get.json()["title"] == "Test Dokra Brass Figurine"

    sync_payload = {
        "products": [
            {
                "id": "offline_prod_101",
                "title": "Offline Queued Saree",
                "description": "Handloom silk saree captured offline",
                "price": 4200.0,
                "image_url": "/uploads/images/offline.jpg",
                "category": "Textiles",
                "tags": ["offline", "sync"],
                "status": "pendingSync",
            }
        ]
    }
    res_sync = client.post("/api/v1/products/sync", json=sync_payload)
    assert res_sync.status_code == 200
    sync_data = res_sync.json()
    assert sync_data["synced_count"] == 1
    assert sync_data["products"][0]["id"] == "offline_prod_101"

    res_del = client.delete(f"/api/v1/products/{prod_id}")
    assert res_del.status_code == 200


def test_catalog_listing_generation():
    """Test AI bilingual listing generator."""
    from unittest.mock import patch, MagicMock
    import asyncio

    payload = {
        "transcript": "यह हाथ से बुनी चंदेरी सिल्क साड़ी है जिसमें असली सुनहरी ज़री का काम है",
        "language_code": "hi",
        "category_hint": "Textiles",
    }

    async def mock_async_return(value):
        return value

    async def mock_async_raise(exc):
        raise exc

    # Test 1: When both providers fail, endpoint must NOT return HTTP 200 with fake data
    with patch("backend.routers.catalog.catalog_service") as mock_service:
        mock_service.generate_listing = MagicMock(
            side_effect=lambda *args, **kwargs: mock_async_raise(
                RuntimeError("AI_LISTING_GENERATION_FAILED")
            )
        )

        response = client.post("/api/v1/catalog/generate-listing", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert "error_code" in data.get("detail", {})

    # Test 2: When provider succeeds, endpoint returns HTTP 200 with listing data
    with patch("backend.routers.catalog.catalog_service") as mock_service:
        from backend.models.schemas import ListingGenerateResponse
        mock_service.generate_listing = MagicMock(
            side_effect=lambda *args, **kwargs: mock_async_return(
                ListingGenerateResponse(
                    title_en="Handwoven Pure Silk Dupatta",
                    title_hi="हाथ से बुना सिल्क दुपट्टा",
                    description_en="A beautiful handwoven dupatta.",
                    description_hi="एक सुंदर हाथ से बुना दुपट्टा।",
                    category="Textiles",
                    tags=["handwoven", "silk"],
                )
            )
        )

        response = client.post("/api/v1/catalog/generate-listing", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "title_en" in data
        assert "title_hi" in data


def test_voice_glossary_api():
    """Test /api/v1/voice/glossary endpoint."""
    response = client.get("/api/v1/voice/glossary?category=Pottery")
    assert response.status_code == 200
    data = response.json()
    assert data["total_terms"] > 0
    assert "Terracotta" in data["terms"]


if __name__ == "__main__":
    print("Running Craftsy backend integration tests...")
    test_health()
    test_pricing_status()
    test_products_crud_and_sync()
    test_catalog_listing_generation()
    test_pricing_suggest()
    test_voice_glossary_api()
    print("All backend integration tests passed.")

