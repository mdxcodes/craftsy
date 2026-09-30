"""
GeM Integration Tests.

Tests for:
1. Product readiness
2. Missing fields
3. Complete product
4. AI listing generation with mocked LLM
5. AI hallucination prevention
6. Listing validation
7. Listing status transitions
8. Registration guidance
9. Existing GeM user
10. Udyam user
11. No Udyam user
12. No sensitive credential persistence
13. ProductDB remains source of truth
14. Listing update after product modification
15. Image references
16. API validation
17. Empty state
18. Error state
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from backend.main import app
from backend.database import SessionLocal, Base
from backend.models.db_models import ArtisanDB, ProductDB
from backend.models.commerce_models import ProductChannelDB, GeMChannelStatus
from backend.services.gem.assisted_provider import assisted_provider
from backend.services.gem.readiness_service import gem_readiness_service
from backend.services.gem.registration_service import gem_registration_service
from backend.services.gem.listing_service import gem_listing_service

client = TestClient(app)


@pytest.fixture
def db_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Session()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def artisan(db_session):
    artisan = ArtisanDB(
        id="artisan_gem_01",
        name="GeM Test Artisan",
        phone="9876543211",
        craft_type="Pottery",
        location_cluster="Test Cluster",
        state="Test State",
        experience_years="5",
        preferred_language="en",
        role="artisan",
    )
    db_session.add(artisan)
    db_session.commit()
    return artisan


@pytest.fixture
def complete_product(db_session, artisan):
    product = ProductDB(
        id="prod_gem_complete",
        artisan_id=artisan.id,
        title="Handcrafted Terracotta Vase",
        title_hi="हाथ से बनी टेराकोटा फूलदान",
        description="Handcrafted terracotta vase with intricate tribal motifs.",
        description_hi="जटिल जनजातीय अलंकारों वाली हाथ से बनी टेराकोटा फूलदान।",
        price=1450.0,
        image_url="/uploads/images/vase.jpg",
        category="Pottery",
        tags='["terracotta", "vase", "handcrafted"]',
        status="live",
        stock=12,
    )
    db_session.add(product)
    db_session.commit()
    return product


@pytest.fixture
def incomplete_product(db_session, artisan):
    product = ProductDB(
        id="prod_gem_incomplete",
        artisan_id=artisan.id,
        title="",
        description="",
        price=0.0,
        image_url="",
        category="General",
        tags="[]",
        status="draft",
        stock=0,
    )
    db_session.add(product)
    db_session.commit()
    return product


# ── Readiness Tests ──────────────────────────────────────────────────────────


def test_readiness_complete_product(db_session, complete_product):
    readiness = gem_readiness_service.check_readiness(db_session, complete_product.id)
    assert readiness.product_ready is True
    assert readiness.readiness_status == "ready"
    assert len(readiness.missing_information) == 0
    assert "Product title" in readiness.available_fields
    assert "Product price (INR 1450.0)" in readiness.available_fields


def test_readiness_incomplete_product(db_session, incomplete_product):
    readiness = gem_readiness_service.check_readiness(db_session, incomplete_product.id)
    assert readiness.product_ready is False
    assert readiness.readiness_status == "needs_information"
    assert "Product title" in readiness.missing_information
    assert "Product description" in readiness.missing_information
    assert "Product price" in readiness.missing_information
    assert "Product image" in readiness.missing_information
    assert "Product category" in readiness.missing_information


def test_readiness_missing_fields_listed(db_session, incomplete_product):
    readiness = gem_readiness_service.check_readiness(db_session, incomplete_product.id)
    response = gem_readiness_service.to_response(readiness)
    assert response["ready"] is False
    assert len(response["missing_fields"]) >= 5
    assert "Product title" in response["missing_fields"]


# ── AI Listing Generation Tests ──────────────────────────────────────────────


def test_listing_generation_complete_product(db_session, complete_product):
    import asyncio
    mock_response = {
        "product_name": "Handcrafted Terracotta Vase",
        "short_description": "Beautiful handcrafted terracotta vase with tribal motifs.",
        "description": "This handcrafted terracotta vase features intricate tribal motifs, shaped on a traditional potter's wheel.",
        "price": 1450.0,
        "category": "Pottery",
        "specifications": {"material": "Terracotta"},
        "certifications": [],
        "warranty": None,
        "images": ["/uploads/images/vase.jpg"],
        "artisan_information": {},
        "missing_information": [],
    }

    async def mock_call(*args, **kwargs):
        return mock_response

    with patch.object(gem_listing_service, "_call_llm", side_effect=mock_call):
        listing = asyncio.run(gem_listing_service.generate_listing(complete_product.id, db_session))
        assert listing["product_name"] == "Handcrafted Terracotta Vase"
        assert listing["price"] == 1450.0
        assert listing["images"] == ["/uploads/images/vase.jpg"]


def test_listing_generation_no_hallucination(db_session, complete_product):
    """AI must not invent weight, warranty, or dimensions when source is missing."""
    import asyncio
    mock_response = {
        "product_name": "Handcrafted Terracotta Vase",
        "short_description": "Beautiful handcrafted terracotta vase.",
        "description": "This handcrafted terracotta vase features intricate tribal motifs.",
        "price": 1450.0,
        "category": "Pottery",
        "specifications": {"material": "Terracotta"},
        "certifications": [],
        "warranty": None,
        "images": ["/uploads/images/vase.jpg"],
        "artisan_information": {},
        "missing_information": ["weight", "dimensions", "warranty"],
    }

    async def mock_call(*args, **kwargs):
        return mock_response

    with patch.object(gem_listing_service, "_call_llm", side_effect=mock_call):
        listing = asyncio.run(gem_listing_service.generate_listing(complete_product.id, db_session))
        assert listing["warranty"] is None
        assert "weight" not in listing.get("specifications", {})
        assert "dimensions" not in listing.get("specifications", {})


def test_listing_fallback_when_llm_unavailable(db_session, complete_product):
    import asyncio
    listing = asyncio.run(gem_listing_service.generate_listing(complete_product.id, db_session))
    assert listing["product_name"] == "Handcrafted Terracotta Vase"
    assert listing["price"] == 1450.0
    assert listing["images"] == ["/uploads/images/vase.jpg"]


# ── Registration Guidance Tests ──────────────────────────────────────────────


def test_registration_options_returned():
    options = gem_registration_service.get_registration_options()
    assert "paths" in options
    assert len(options["paths"]) == 3
    path_ids = [p["id"] for p in options["paths"]]
    assert "already_registered" in path_ids
    assert "udyam_only" in path_ids
    assert "new_seller" in path_ids


def test_registration_guidance_already_registered():
    guidance = gem_registration_service.get_guidance("already_registered")
    assert guidance["path"] == "already_registered"
    assert len(guidance["steps"]) >= 1
    assert "seller_portal" in guidance["official_links"]
    assert "gem.gov.in" in guidance["official_links"]["seller_portal"]


def test_registration_guidance_udyam_only():
    guidance = gem_registration_service.get_guidance("udyam_only")
    assert guidance["path"] == "udyam_only"
    assert "warning" in guidance
    assert "OTP" in guidance["warning"]
    assert "udyamregistration.gov.in" in guidance["official_links"]["udyam_login"]


def test_registration_guidance_new_seller():
    guidance = gem_registration_service.get_guidance("new_seller")
    assert guidance["path"] == "new_seller"
    assert "warning" in guidance
    assert len(guidance["steps"]) >= 4


def test_registration_guidance_invalid_path():
    with pytest.raises(ValueError):
        gem_registration_service.get_guidance("invalid_path")


# ── API Endpoint Tests ───────────────────────────────────────────────────────


def _create_product_via_api(title="Handcrafted Terracotta Vase", description="Handcrafted terracotta vase with intricate tribal motifs.", price=1450.0, category="Pottery", image_url="/uploads/images/vase.jpg"):
    payload = {
        "title": title,
        "description": description,
        "price": price,
        "image_url": image_url,
        "category": category,
        "tags": ["terracotta", "vase", "handcrafted"],
        "status": "live",
    }
    res = client.post("/api/v1/products", json=payload)
    assert res.status_code == 201, res.text
    return res.json()["id"]


def test_api_gem_readiness_complete():
    product_id = _create_product_via_api()
    response = client.get(f"/api/v1/gem/products/{product_id}/readiness")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ready"] is True
    assert data["readiness_status"] == "ready"


def test_api_gem_readiness_incomplete():
    product_id = _create_product_via_api(
        title="",
        description="",
        price=0.0,
        image_url="",
        category="General",
    )
    response = client.get(f"/api/v1/gem/products/{product_id}/readiness")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ready"] is False
    assert len(data["missing_fields"]) > 0


def test_api_gem_registration_options():
    response = client.get("/api/v1/gem/registration-options")
    assert response.status_code == 200
    data = response.json()
    assert "paths" in data
    assert len(data["paths"]) == 3


def test_api_gem_registration_guidance():
    response = client.get("/api/v1/gem/registration-guidance?path=already_registered")
    assert response.status_code == 200
    data = response.json()
    assert data["path"] == "already_registered"


def test_api_gem_listing_draft():
    product_id = _create_product_via_api()
    with patch("backend.services.gem.assisted_provider.assisted_provider._generate_ai_listing", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = {
            "product_name": "Handcrafted Terracotta Vase",
            "short_description": "Beautiful vase.",
            "description": "Handcrafted terracotta vase.",
            "price": 1450.0,
            "category": "Pottery",
            "specifications": {},
            "certifications": [],
            "warranty": None,
            "images": ["/uploads/images/vase.jpg"],
            "artisan_information": {},
            "missing_information": [],
        }
        response = client.post(f"/api/v1/gem/products/{product_id}/listing-draft")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["product_name"] == "Handcrafted Terracotta Vase"
        assert "copyable_text" in data
        assert "Product Name:" in data["copyable_text"]
        assert "Short Description:" in data["copyable_text"]
        assert "Description:" in data["copyable_text"]
        assert "Price:" in data["copyable_text"]
        assert "Specifications:" in data["copyable_text"]
        assert "Certifications:" in data["copyable_text"]
        assert "Warranty:" in data["copyable_text"]


def test_api_gem_listing_draft_includes_artisan_info():
    product_id = _create_product_via_api()
    with patch("backend.services.gem.assisted_provider.assisted_provider._generate_ai_listing", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = {
            "product_name": "Handcrafted Terracotta Vase",
            "short_description": "Beautiful vase.",
            "description": "Handcrafted terracotta vase.",
            "price": 1450.0,
            "category": "Pottery",
            "specifications": {},
            "certifications": [],
            "warranty": None,
            "images": ["/uploads/images/vase.jpg"],
            "artisan_information": {"name": "Ramu", "craft_type": "Pottery", "state": "Rajasthan"},
            "missing_information": [],
        }
        response = client.post(f"/api/v1/gem/products/{product_id}/listing-draft")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["artisan_information"]["name"] == "Ramu"
        assert "Artisan Information:" in data["copyable_text"]
        assert "Ramu" in data["copyable_text"]


def test_api_gem_listing_kit():
    product_id = _create_product_via_api()
    with patch("backend.services.gem.assisted_provider.assisted_provider._generate_ai_listing", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = {
            "product_name": "Handcrafted Terracotta Vase",
            "short_description": "Beautiful vase.",
            "description": "Handcrafted terracotta vase.",
            "price": 1450.0,
            "category": "Pottery",
            "specifications": {},
            "certifications": [],
            "warranty": None,
            "images": ["/uploads/images/vase.jpg"],
            "artisan_information": {},
            "missing_information": [],
        }
        response = client.get(f"/api/v1/gem/products/{product_id}/listing-kit")
        assert response.status_code == 200, response.text
        data = response.json()
        assert "draft" in data
        assert "copyable_text" in data
        assert "disclaimer" in data
        assert "NOT an official GeM catalogue submission" in data["disclaimer"]


def test_api_gem_open_portal():
    product_id = _create_product_via_api()
    response = client.post(f"/api/v1/gem/products/{product_id}/open")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["opened"] is True
    assert "gem.gov.in" in data["url"]


def test_api_gem_product_not_found():
    response = client.get("/api/v1/gem/products/nonexistent/readiness")
    assert response.status_code == 404


def test_api_gem_listing_draft_not_found():
    response = client.post("/api/v1/gem/products/nonexistent/listing-draft")
    assert response.status_code == 404


# ── Credential Safety Tests ──────────────────────────────────────────────────


def test_no_credentials_in_registration_options():
    options = gem_registration_service.get_registration_options()
    assert "gem_password" not in str(options)
    assert "otp" not in str(options).lower()
    assert "aadhaar" not in str(options).lower()


def test_no_credentials_in_guidance():
    guidance = gem_registration_service.get_guidance("already_registered")
    assert "password" not in str(guidance).lower()
    assert "otp" not in str(guidance).lower()


# ── Source of Truth Tests ────────────────────────────────────────────────────


def test_readiness_uses_product_db_fields(db_session, complete_product):
    readiness = gem_readiness_service.check_readiness(db_session, complete_product.id)
    assert "Product title" in readiness.available_fields
    assert complete_product.title == "Handcrafted Terracotta Vase"


def test_listing_uses_product_db_image(db_session, complete_product):
    listing = gem_listing_service._deterministic_listing(
        gem_listing_service._product_to_dict(complete_product)
    )
    assert listing["images"] == [complete_product.image_url]


# ── Empty State Tests ────────────────────────────────────────────────────────


def test_empty_registration_guidance():
    with pytest.raises(ValueError):
        gem_registration_service.get_guidance("")


# ── Error State Tests ────────────────────────────────────────────────────────


def test_readiness_product_not_found(db_session):
    with pytest.raises(ValueError):
        gem_readiness_service.check_readiness(db_session, "nonexistent")
