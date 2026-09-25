"""
Order Router.

API endpoints for unified order management across all channels.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.order_models import OrderCreate, OrderResponse, OrderChannelSummary
from ..models.order_models import OrderDB
from ..models.db_models import ArtisanDB
from ..services.order_service import order_service
from ..middleware.auth import get_current_artisan

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.get("/artisan/{artisan_id}", response_model=list[OrderResponse])
async def get_artisan_orders(
    artisan_id: str,
    channel: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    """Get orders for an artisan, optionally filtered by channel and status."""
    # Authorization: artisans can only view their own orders
    if current_artisan.id != artisan_id:
        raise HTTPException(status_code=403, detail="Not authorized to view these orders")

    try:
        return order_service.get_orders(db, artisan_id, channel, status, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/my")
async def get_my_orders(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    """
    Get the authenticated user's consumer orders (orders they placed as a buyer).

    The customer_id is always taken from the authenticated token —
    never from a client-supplied parameter.
    """
    from ..models.commerce_foundation_models import OrderItemDB

    query = db.query(OrderDB).filter(OrderDB.customer_id == current_artisan.id)
    if status:
        query = query.filter(OrderDB.status == status)

    total = query.count()
    orders = (
        query.order_by(OrderDB.placed_at.desc())
        .offset(offset)
        .limit(max(1, min(limit, 100)))
        .all()
    )

    results = []
    for order in orders:
        items = (
            db.query(OrderItemDB)
            .filter(OrderItemDB.order_id == order.id)
            .all()
        )
        results.append(_serialize_order_summary(order, items))

    return {"total": total, "orders": results}


@router.get("/my/{order_id}")
async def get_my_order_detail(
    order_id: str,
    db: Session = Depends(get_db),
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    """
    Get one of the authenticated user's consumer orders with full detail:
    items, payment, shipment, and delivery address.

    Returns 404 for orders that do not belong to the current user —
    other users' orders are never exposed.
    """
    order = db.query(OrderDB).filter(
        OrderDB.id == order_id,
        OrderDB.customer_id == current_artisan.id,
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return _serialize_order_detail(db, order)


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
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    """Update order status (seller/artisan action)."""
    # Authorization: only the seller of this order may update its status
    order = order_service.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_artisan.id != order.artisan_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this order's status",
        )

    try:
        order = order_service.update_order_status(db, order_id, status, tracking_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        _sync_shipment_for_order(db, order)
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


def _sync_shipment_for_order(db: Session, order) -> None:
    """Keep ShipmentDB in step with order status (internal delivery tracking).

    Only reflects states that actually exist in backend data — no courier
    scans or fabricated location data.
    """
    from ..models.commerce_foundation_models import ShipmentDB

    shipment = (
        db.query(ShipmentDB).filter(ShipmentDB.order_id == order.id).first()
    )
    if not shipment:
        return

    if order.status == "shipped":
        shipment.status = "in_transit"
        if not shipment.shipped_at:
            shipment.shipped_at = order.shipped_at
    elif order.status == "delivered":
        shipment.status = "delivered"
        shipment.delivered_at = order.delivered_at
    elif order.status == "cancelled":
        shipment.status = "returned" if order.shipped_at else "pending"
    db.commit()


def _serialize_order_summary(order, items) -> dict:
    """Serialize an order for the consumer 'my orders' list."""
    first_title = items[0].product_title if items else ""
    return {
        "id": order.id,
        "status": order.status,
        "total_amount": order.total_amount,
        "quantity": order.quantity,
        "item_count": len(items),
        "first_item_title": first_title,
        "first_item_image_url": items[0].product_image_url if items else "",
        "buyer_location": order.buyer_location or "",
        "placed_at": order.placed_at.isoformat() if order.placed_at else None,
        "shipped_at": order.shipped_at.isoformat() if order.shipped_at else None,
        "delivered_at": order.delivered_at.isoformat() if order.delivered_at else None,
        "tracking_id": order.tracking_id,
    }


def _serialize_order_detail(db: Session, order) -> dict:
    """Serialize an order with items, payment, shipment, and address."""
    from ..models.commerce_foundation_models import OrderItemDB, ShipmentDB

    items = (
        db.query(OrderItemDB).filter(OrderItemDB.order_id == order.id).all()
    )
    payment = order.payment
    shipment = (
        db.query(ShipmentDB).filter(ShipmentDB.order_id == order.id).first()
    )
    address = order.address

    return {
        "id": order.id,
        "status": order.status,
        "total_amount": order.total_amount,
        "quantity": order.quantity,
        "buyer_name": order.buyer_name,
        "buyer_location": order.buyer_location or "",
        "buyer_phone": order.buyer_phone or "",
        "placed_at": order.placed_at.isoformat() if order.placed_at else None,
        "shipped_at": order.shipped_at.isoformat() if order.shipped_at else None,
        "delivered_at": order.delivered_at.isoformat() if order.delivered_at else None,
        "tracking_id": order.tracking_id,
        "items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_title": item.product_title,
                "product_image_url": item.product_image_url,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
            }
            for item in items
        ],
        "payment": {
            "id": payment.id,
            "amount": payment.amount,
            "method": payment.method,
            "status": payment.status,
        }
        if payment
        else None,
        "shipment": {
            "id": shipment.id,
            "status": shipment.status,
            "carrier": shipment.carrier,
            "tracking_id": shipment.tracking_id,
        }
        if shipment
        else None,
        "address": {
            "id": address.id,
            "label": address.label,
            "name": address.name,
            "phone": address.phone,
            "line1": address.line1,
            "line2": address.line2,
            "city": address.city,
            "state": address.state,
            "pincode": address.pincode,
        }
        if address
        else None,
    }
