"""
Cart Router.

API endpoints for shopping cart management.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models.db_models import ArtisanDB
from ..middleware.auth import get_current_artisan
from ..services.cart_service import (
    cart_service,
    CartItemError,
    ProductNotFoundError,
    ProductNotAvailableError,
    InsufficientStockError,
)

router = APIRouter(prefix="/api/v1/cart", tags=["Cart"])


class AddItemRequest(BaseModel):
    product_id: str = Field(..., description="Product ID to add")
    quantity: int = Field(default=1, ge=1, description="Quantity to add")


class UpdateItemRequest(BaseModel):
    quantity: int = Field(..., ge=1, description="New quantity")


@router.get("")
async def get_cart(
    db: Session = Depends(get_db),
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    """Get the current user's cart."""
    return cart_service.get_cart_with_items(db, current_artisan.id)


@router.post("/items")
async def add_item(
    request: AddItemRequest,
    db: Session = Depends(get_db),
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    """Add a product to the cart."""
    try:
        return cart_service.add_item(
            db, current_artisan.id, request.product_id, request.quantity
        )
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ProductNotAvailableError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InsufficientStockError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except CartItemError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/items/{item_id}")
async def update_item(
    item_id: str,
    request: UpdateItemRequest,
    db: Session = Depends(get_db),
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    """Update a cart item's quantity."""
    try:
        return cart_service.update_item_quantity(
            db, current_artisan.id, item_id, request.quantity
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InsufficientStockError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/items/{item_id}")
async def remove_item(
    item_id: str,
    db: Session = Depends(get_db),
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    """Remove an item from the cart."""
    try:
        return cart_service.remove_item(db, current_artisan.id, item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("")
async def clear_cart(
    db: Session = Depends(get_db),
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    """Clear all items from the cart."""
    cart_service.clear_cart(db, current_artisan.id)
    return {"status": "success", "message": "Cart cleared"}
