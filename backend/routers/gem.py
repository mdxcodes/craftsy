"""
GeM Integration Router.

Endpoints:
- GET  /api/v1/gem/products/{product_id}/readiness
- POST /api/v1/gem/products/{product_id}/prepare
- POST /api/v1/gem/products/{product_id}/listing-draft
- GET  /api/v1/gem/products/{product_id}/listing-kit
- GET  /api/v1/gem/registration-options
- GET  /api/v1/gem/registration-guidance
- POST /api/v1/gem/products/{product_id}/open
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.gem.assisted_provider import assisted_provider
from ..services.gem.readiness_service import gem_readiness_service
from ..services.gem.registration_service import gem_registration_service
from ..services.gem.schemas import GeMReadinessResponse, GeMListingKit, GeMOpenResponse

router = APIRouter(prefix="/api/v1/gem", tags=["GeM"])


@router.get("/products/{product_id}/readiness", response_model=GeMReadinessResponse)
async def get_gem_readiness(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Get GeM seller readiness assessment for a product."""
    try:
        result = await assisted_provider.validate_product(product_id, db)
        return GeMReadinessResponse(
            ready=result.get("product_ready", False),
            missing_fields=result.get("missing_information", []),
            warnings=result.get("warnings", []),
            available_fields=result.get("available_fields", []),
            category=result.get("category"),
            readiness_status=result.get("readiness_status", "unknown"),
            next_actions=result.get("next_actions", []),
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/products/{product_id}/prepare")
async def prepare_gem_listing(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Prepare a GeM listing draft from verified product data."""
    try:
        result = await assisted_provider.prepare_listing(product_id, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/products/{product_id}/listing-draft")
async def create_listing_draft(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Generate a GeM Listing Draft."""
    try:
        result = await assisted_provider.prepare_listing(product_id, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/{product_id}/listing-kit", response_model=GeMListingKit)
async def get_listing_kit(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Get a human-readable GeM Listing Kit for a product."""
    try:
        result = await assisted_provider.generate_listing_kit(product_id, db)
        return GeMListingKit(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/registration-options")
async def get_registration_options():
    """Get available GeM registration paths."""
    try:
        return gem_registration_service.get_registration_options()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/registration-guidance")
async def get_registration_guidance(path: str):
    """Get step-by-step guidance for a specific registration path."""
    try:
        return gem_registration_service.get_guidance(path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/products/{product_id}/open", response_model=GeMOpenResponse)
async def open_gem_portal(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Get the official GeM portal URL for manual listing submission."""
    try:
        result = await assisted_provider.open_official_gem()
        assisted_provider.update_gem_status(db, product_id, "ready_for_submission")
        return GeMOpenResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
