"""
Unified Order Service.

Manages orders from multiple channels:
- Craftsy Marketplace
- ONDC
- Government/GeM

Provides a single inbox for all orders regardless of channel.
"""

from __future__ import annotations

import json
import uuid
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from ..models.order_models import (
    OrderDB,
    OrderCreate,
    OrderResponse,
    OrderChannelSummary,
    OrderChannel,
)
from ..models.db_models import ProductDB

logger = logging.getLogger(__name__)


class OrderService:
    """Manages unified orders across all commerce channels."""

    CHANNEL_LABELS = {
        "craftsy": "Craftsy",
        "ondc": "ONDC",
        "gem": "Government",
    }

    def __init__(self):
        pass

    def create_order(self, db: Session, order_data: OrderCreate) -> OrderDB:
        """Create a new order."""
        order = OrderDB(
            id=f"ord_{uuid.uuid4().hex[:12]}",
            artisan_id=order_data.artisan_id,
            product_id=order_data.product_id,
            product_title=order_data.product_title,
            product_image_url=order_data.product_image_url,
            buyer_name=order_data.buyer_name,
            buyer_location=order_data.buyer_location,
            buyer_email=order_data.buyer_email,
            buyer_phone=order_data.buyer_phone,
            quantity=order_data.quantity,
            unit_price=order_data.unit_price,
            total_amount=order_data.total_amount,
            status="new",
            channel=order_data.channel,
            external_order_id=order_data.external_order_id,
            channel_data=json.dumps(order_data.channel_data or {}),
            placed_at=datetime.now(),
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    def get_orders(
        self,
        db: Session,
        artisan_id: str,
        channel: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> List[OrderResponse]:
        """Get orders for an artisan, optionally filtered by channel/status."""
        query = db.query(OrderDB).filter(OrderDB.artisan_id == artisan_id)

        if channel:
            query = query.filter(OrderDB.channel == channel)
        if status:
            query = query.filter(OrderDB.status == status)

        query = query.order_by(OrderDB.placed_at.desc()).limit(limit)
        orders = query.all()

        return [
            OrderResponse(
                id=order.id,
                product_title=order.product_title,
                product_image_url=order.product_image_url,
                buyer_name=order.buyer_name,
                buyer_location=order.buyer_location,
                quantity=order.quantity,
                total_amount=order.total_amount,
                status=order.status,
                channel=order.channel,
                channel_label=order.channel_label or order.channel,
                external_order_id=order.external_order_id,
                tracking_id=order.tracking_id,
                placed_at=order.placed_at,
                shipped_at=order.shipped_at,
                delivered_at=order.delivered_at,
            )
            for order in orders
        ]

    def get_order_by_id(self, db: Session, order_id: str) -> Optional[OrderDB]:
        """Get a single order by ID."""
        return db.query(OrderDB).filter(OrderDB.id == order_id).first()

    def update_order_status(
        self,
        db: Session,
        order_id: str,
        new_status: str,
        tracking_id: Optional[str] = None,
    ) -> Optional[OrderDB]:
        """Update order status."""
        order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
        if not order:
            return None

        order.status = new_status
        order.updated_at = datetime.now()

        if tracking_id:
            order.tracking_id = tracking_id

        if new_status == "shipped":
            order.shipped_at = datetime.now()
        elif new_status == "delivered":
            order.delivered_at = datetime.now()

        db.commit()
        db.refresh(order)
        return order

    def get_channel_summary(
        self,
        db: Session,
        artisan_id: str,
    ) -> List[OrderChannelSummary]:
        """Get order summary grouped by channel."""
        from sqlalchemy import func

        results = (
            db.query(
                OrderDB.channel,
                func.count(OrderDB.id).label("order_count"),
                func.sum(OrderDB.total_amount).label("total_amount"),
            )
            .filter(OrderDB.artisan_id == artisan_id)
            .group_by(OrderDB.channel)
            .all()
        )

        return [
            OrderChannelSummary(
                channel=row.channel,
                channel_label=self.CHANNEL_LABELS.get(row.channel, row.channel),
                order_count=row.order_count,
                total_amount=float(row.total_amount or 0),
            )
            for row in results
        ]


# ── Singleton ────────────────────────────────────────────────────────────────

order_service = OrderService()
