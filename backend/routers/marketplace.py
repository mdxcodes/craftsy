"""
Marketplace Router.

API endpoints for public product browsing.
All endpoints are public (no authentication required).
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.marketplace_service import marketplace_service

router = APIRouter(prefix="/api/v1/marketplace", tags=["Marketplace"])


@router.get("/products")
async def list_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in product title"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """
    List all live products with optional filtering.

    Public endpoint — no authentication required.
    """
    products = marketplace_service.list_products(db, category, search, limit, offset)
    return [
        {
            "id": p.id,
            "title": p.title,
            "title_hi": p.title_hi or "",
            "description": p.description or "",
            "description_hi": p.description_hi or "",
            "price": p.price,
            "image_url": p.image_url,
            "category": p.category,
            "tags": p.tags_list,
            "stock": p.stock,
            "artisan_id": p.artisan_id,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in products
    ]


@router.get("/products/{product_id}")
async def get_product(
    product_id: str,
    db: Session = Depends(get_db),
):
    """
    Get a single live product by ID.

    Public endpoint — no authentication required.
    Returns 404 for non-live or nonexistent products.
    """
    product = marketplace_service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "id": product.id,
        "title": product.title,
        "title_hi": product.title_hi or "",
        "description": product.description or "",
        "description_hi": product.description_hi or "",
        "price": product.price,
        "image_url": product.image_url,
        "category": product.category,
        "tags": product.tags_list,
        "stock": product.stock,
        "artisan_id": product.artisan_id,
        "created_at": product.created_at.isoformat() if product.created_at else None,
    }


@router.get("/categories")
async def get_categories(
    db: Session = Depends(get_db),
):
    """
    Get all unique categories from live products.

    Public endpoint — no authentication required.
    """
    return marketplace_service.get_categories(db)
