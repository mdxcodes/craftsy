"""
Marketplace Router.

API endpoints for public product browsing.
All endpoints are public (no authentication required).
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.db_models import ArtisanDB, ProductDB
from ..services.marketplace_service import marketplace_service

router = APIRouter(prefix="/api/v1/marketplace", tags=["Marketplace"])


@router.get("/products")
async def list_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in product title"),
    limit: int = Query(500, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """
    List all live products with optional filtering.

    Public endpoint — no authentication required.
    """
    products = marketplace_service.list_products(db, category, search, limit, offset)
    artisan_ids = {p.artisan_id for p in products if p.artisan_id}
    artisans = {
        a.id: a
        for a in db.query(ArtisanDB).filter(ArtisanDB.id.in_(artisan_ids)).all()
    } if artisan_ids else {}
    return [
        {
            "id": product.id,
            "title": product.title,
            "title_hi": product.title_hi or "",
            "description": product.description or "",
            "description_hi": product.description_hi or "",
            "price": product.price,
            "image_url": product.image_url,
            "cloudinary_public_id": product.cloudinary_public_id,
            "category": product.category,
            "tags": product.tags_list,
            "stock": product.stock,
            "artisan_id": product.artisan_id,
            "artisan_name": artisans.get(product.artisan_id).name if product.artisan_id and product.artisan_id in artisans else None,
            "artisan_craft": artisans.get(product.artisan_id).craft_type if product.artisan_id and product.artisan_id in artisans else None,
            "created_at": product.created_at.isoformat() if product.created_at else None,
        }
        for product in products
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

    artisan = db.query(ArtisanDB).filter(ArtisanDB.id == product.artisan_id).first()
    return {
        "id": product.id,
        "title": product.title,
        "title_hi": product.title_hi or "",
        "description": product.description or "",
        "description_hi": product.description_hi or "",
        "price": product.price,
        "image_url": product.image_url,
        "cloudinary_public_id": product.cloudinary_public_id,
        "category": product.category,
        "tags": product.tags_list,
        "stock": product.stock,
        "artisan_id": product.artisan_id,
        "artisan_name": artisan.name if artisan else None,
        "artisan_craft": artisan.craft_type if artisan else None,
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
