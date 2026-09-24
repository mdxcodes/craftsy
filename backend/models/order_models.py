"""
Unified Order Model with Channel Support.

Extends the existing order architecture to support multiple sales channels:
- Craftsy Marketplace
- ONDC
- Government/GeM

Every order retains its source channel and external reference.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..database import Base


class OrderChannel(str, Enum):
    """Source channel for an order."""
    CRAFTSY = "craftsy"
    ONDC = "ondc"
    GEM = "gem"


class OrderDB(Base):
    """
    Unified order model with multi-channel support.

    Extends the existing order concept with:
    - channel: Which marketplace/channel the order came from
    - external_order_id: Order ID from the external platform (if applicable)
    - channel_data: Channel-specific data (JSON)
    """

    __tablename__ = "orders"

    id = Column(String(64), primary_key=True, index=True)
    artisan_id = Column(
        String(64),
        ForeignKey("artisans.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Product info (denormalized for order history)
    product_id = Column(
        String(64),
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
    )
    product_title = Column(String(255), nullable=False)
    product_image_url = Column(String(512), default="")

    # Buyer info
    buyer_name = Column(String(255), nullable=False)
    buyer_location = Column(String(255), default="")
    buyer_email = Column(String(255), nullable=True)
    buyer_phone = Column(String(20), nullable=True)

    # Order details
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False, default=0.0)
    total_amount = Column(Float, nullable=False, default=0.0)
    status = Column(String(32), default="new", index=True)
    # Status values: new, confirmed, packed, shipped, delivered, cancelled

    # Channel info
    channel = Column(String(32), default="craftsy", index=True)
    external_order_id = Column(String(255), nullable=True, index=True)
    channel_data = Column(Text, default="{}")  # JSON blob

    # Tracking
    tracking_id = Column(String(255), nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)

    # Timestamps
    placed_at = Column(DateTime, default=datetime.now, index=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships (no backref to avoid lazy-load issues in tests)
    artisan = relationship("ArtisanDB")
    product = relationship("ProductDB")

    @property
    def channel_data_dict(self) -> dict:
        """Deserialize channel_data from JSON."""
        try:
            return json.loads(self.channel_data) if self.channel_data else {}
        except Exception:
            return {}

    @property
    def channel_label(self) -> str:
        """Get human-readable channel label."""
        labels = {
            "craftsy": "Craftsy",
            "ondc": "ONDC",
            "gem": "Government",
        }
        return labels.get(self.channel, self.channel)


# ── Schemas ──────────────────────────────────────────────────────────────────


class OrderCreate(BaseModel):
    """Create a new order."""
    artisan_id: str
    product_id: str
    product_title: str
    product_image_url: str = ""
    buyer_name: str
    buyer_location: str = ""
    buyer_email: Optional[str] = None
    buyer_phone: Optional[str] = None
    quantity: int = 1
    unit_price: float = 0.0
    total_amount: float = 0.0
    channel: str = "craftsy"
    external_order_id: Optional[str] = None
    channel_data: Optional[dict] = None


class OrderResponse(BaseModel):
    """Order response with channel info."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_title: str
    product_image_url: str
    buyer_name: str
    buyer_location: str
    quantity: int
    total_amount: float
    status: str
    channel: str
    channel_label: Optional[str] = None
    external_order_id: Optional[str] = None
    tracking_id: Optional[str] = None
    placed_at: datetime
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None


class OrderChannelSummary(BaseModel):
    """Summary of orders by channel."""
    channel: str
    channel_label: str
    order_count: int
    total_amount: float


class OrderFilter(BaseModel):
    """Filter orders by channel and status."""
    channel: Optional[str] = None
    status: Optional[str] = None
    artisan_id: Optional[str] = None
