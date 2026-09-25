"""
Checkout Router.

API endpoint for server-authoritative order creation.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models.db_models import ArtisanDB
from ..middleware.auth import get_current_artisan
from ..services.order_service import order_service

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


class OrderItemRequest(BaseModel):
    product_id: str = Field(..., description="Product ID to order")
    quantity: int = Field(default=1, ge=1, description="Quantity")


class CheckoutRequest(BaseModel):
    items: List[OrderItemRequest] = Field(..., description="Items to order")
    address_id: str = Field(..., description="Delivery address ID")
    payment_method: str = Field(default="cod", description="Payment method")


@router.post("/checkout", status_code=201)
async def checkout(
    request: CheckoutRequest,
    db: Session = Depends(get_db),
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    """
    Create an order from cart items (server-authoritative).

    This endpoint:
    1. Validates the address belongs to the customer
    2. Validates each product exists and is live
    3. Validates stock availability
    4. Uses ProductDB.price as the authoritative price (ignores client price)
    5. Calculates totals server-side
    6. Creates OrderDB, OrderItemDB, PaymentDB, ShipmentDB records
    7. Decrements stock atomically
    8. Uses a transaction (all-or-nothing)
    """
    try:
        order = order_service.create_order_from_cart(
            db,
            customer_id=current_artisan.id,
            address_id=request.address_id,
            items=[item.model_dump() for item in request.items],
            payment_method=request.payment_method,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Load related data for response
    from ..models.commerce_foundation_models import OrderItemDB, PaymentDB, ShipmentDB

    items = db.query(OrderItemDB).filter(OrderItemDB.order_id == order.id).all()
    payment = db.query(PaymentDB).filter(PaymentDB.order_id == order.id).first()
    shipment = db.query(ShipmentDB).filter(ShipmentDB.order_id == order.id).first()

    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "buyer_name": order.buyer_name,
        "buyer_location": order.buyer_location,
        "quantity": order.quantity,
        "total_amount": order.total_amount,
        "status": order.status,
        "channel": order.channel,
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
        } if payment else None,
        "shipment": {
            "id": shipment.id,
            "status": shipment.status,
            "carrier": shipment.carrier,
            "tracking_id": shipment.tracking_id,
        } if shipment else None,
        "placed_at": order.placed_at.isoformat() if order.placed_at else None,
    }
