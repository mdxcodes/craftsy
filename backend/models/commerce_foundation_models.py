"""
Commerce Foundation Database Models.

New models to support the unified commerce foundation:
- CartDB: User's shopping cart
- CartItemDB: Items within a cart
- AddressDB: User's shipping addresses
- OrderItemDB: Line items within an order
- PaymentDB: Payment records
- ShipmentDB: Shipment/delivery records

These models extend the existing ArtisanDB (as unified identity),
ProductDB, and OrderDB without modifying their existing fields.
"""

from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey, Integer, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

from ..database import Base


# ── Cart ─────────────────────────────────────────────────────────────────────


class CartDB(Base):
    """A user's shopping cart.

    One cart per user (enforced by unique constraint on user_id).
    """

    __tablename__ = "carts"

    id = Column(String(64), primary_key=True, index=True)
    user_id = Column(
        String(64),
        ForeignKey("artisans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        unique=True,  # One cart per user
    )
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    user = relationship("ArtisanDB", back_populates="cart")
    items = relationship(
        "CartItemDB",
        back_populates="cart",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )


# ── Cart Item ────────────────────────────────────────────────────────────────


class CartItemDB(Base):
    """An item within a shopping cart.

    Uniqueness constraint: one product per cart (prevents duplicate entries).
    """

    __tablename__ = "cart_items"

    id = Column(String(64), primary_key=True, index=True)
    cart_id = Column(
        String(64),
        ForeignKey("carts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id = Column(
        String(64),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    cart = relationship("CartDB", back_populates="items")
    product = relationship("ProductDB")

    # Unique constraint: one product per cart (prevents duplicate entries)
    __table_args__ = (
        # If a user adds the same product again, the quantity should be updated
        # rather than creating a new row
        UniqueConstraint("cart_id", "product_id", name="uq_cart_product"),
    )


# ── Address ──────────────────────────────────────────────────────────────────


class AddressDB(Base):
    """A user's shipping/delivery address."""

    __tablename__ = "addresses"

    id = Column(String(64), primary_key=True, index=True)
    user_id = Column(
        String(64),
        ForeignKey("artisans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    label = Column(String(32), default="home")
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    line1 = Column(String(512), nullable=False)
    line2 = Column(String(512), default="")
    city = Column(String(128), nullable=False)
    state = Column(String(128), nullable=False)
    pincode = Column(String(10), nullable=False)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    user = relationship("ArtisanDB", back_populates="addresses")


# ── Order Item ───────────────────────────────────────────────────────────────


class OrderItemDB(Base):
    """A line item within an order.

    Prices are historical snapshots of ProductDB.price at the time of order.
    They are NOT live ProductDB prices.
    """

    __tablename__ = "order_items"

    id = Column(String(64), primary_key=True, index=True)
    order_id = Column(
        String(64),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id = Column(
        String(64),
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
    )
    product_title = Column(String(255), nullable=False)
    product_image_url = Column(String(512), default="")
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    order = relationship("OrderDB", back_populates="items")
    product = relationship("ProductDB")


# ── Payment ──────────────────────────────────────────────────────────────────


class PaymentDB(Base):
    """Payment record for an order.

    Supported methods: cod, upi, card, netbanking
    Supported statuses: pending, processing, success, failed, refunded
    """

    __tablename__ = "payments"

    id = Column(String(64), primary_key=True, index=True)
    order_id = Column(
        String(64),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(
        String(64),
        ForeignKey("artisans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    amount = Column(Float, nullable=False)
    method = Column(String(32), default="cod")
    status = Column(String(32), default="pending")
    transaction_id = Column(String(255), nullable=True)
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    order = relationship("OrderDB", foreign_keys=[order_id], overlaps="payment,shipment")
    user = relationship("ArtisanDB", back_populates="payments")


# ── Shipment ─────────────────────────────────────────────────────────────────


class ShipmentDB(Base):
    """Shipment/delivery record for an order.

    Supported statuses: pending, picked_up, in_transit, delivered, returned
    """

    __tablename__ = "shipments"

    id = Column(String(64), primary_key=True, index=True)
    order_id = Column(
        String(64),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    artisan_id = Column(
        String(64),
        ForeignKey("artisans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status = Column(String(32), default="pending")
    carrier = Column(String(128), nullable=True)
    tracking_id = Column(String(255), nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    order = relationship("OrderDB", foreign_keys=[order_id], overlaps="payment,shipment")
    artisan = relationship("ArtisanDB", back_populates="shipments")
