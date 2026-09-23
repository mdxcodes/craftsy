"""
Order Router.

API endpoints for unified order management across all channels.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.order_models import OrderCreate, OrderResponse, OrderChannelSummary
from ..services.order_service import order_service

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.get("/artisan/{artisan_id}", response_model=list[OrderResponse])
async def get_artisan_orders(
    artisan_id: str,
    channel: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Get orders for an artisan, optionally filtered by channel and status."""
    try:
        return order_service.get_orders(db, artisan_id, channel, status, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/artisan/{artisan_id}/summary", response_model=list[OrderChannelSummary])
async def get_order_channel_summary(
    artisan_id: str,
    db: Session = Depends(get_db),
):
    """Get order summary grouped by channel."""
    try:
        return order_service.get_channel_summary(db, artisan_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
):
    """Create a new order."""
    try:
        new_order = order_service.create_order(db, order)
        return OrderResponse(
            id=new_order.id,
            product_title=new_order.product_title,
            product_image_url=new_order.product_image_url,
            buyer_name=new_order.buyer_name,
            buyer_location=new_order.buyer_location,
            quantity=new_order.quantity,
            total_amount=new_order.total_amount,
            status=new_order.status,
            channel=new_order.channel,
            channel_label=new_order.channel_label,
            external_order_id=new_order.external_order_id,
            tracking_id=new_order.tracking_id,
            placed_at=new_order.placed_at,
            shipped_at=new_order.shipped_at,
            delivered_at=new_order.delivered_at,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    status: str,
    tracking_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Update order status."""
    try:
        order = order_service.update_order_status(db, order_id, status, tracking_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return OrderResponse(
            id=order.id,
            product_title=order.product_title,
            product_image_url=order.product_image_url,
            buyer_name=order.buyer_name,
            buyer_location=order.buyer_location,
            quantity=order.quantity,
            total_amount=order.total_amount,
            status=order.status,
            channel=order.channel,
            channel_label=order.channel_label,
            external_order_id=order.external_order_id,
            tracking_id=order.tracking_id,
            placed_at=order.placed_at,
            shipped_at=order.shipped_at,
            delivered_at=order.delivered_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
