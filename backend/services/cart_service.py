"""
Cart Service.

Manages shopping cart operations for users.
"""

from __future__ import annotations

import uuid
import logging
from typing import Optional, List
from sqlalchemy.orm import Session

from ..models.commerce_foundation_models import CartDB, CartItemDB
from ..models.db_models import ArtisanDB, ProductDB

logger = logging.getLogger(__name__)


class CartItemError(ValueError):
    """Base error for cart item operations."""


class ProductNotFoundError(CartItemError):
    """The product does not exist."""


class ProductNotAvailableError(CartItemError):
    """The product is not live/available for purchase."""


class InsufficientStockError(CartItemError):
    """Requested quantity exceeds available stock."""


class CartService:
    """Manages shopping cart operations."""

    def get_or_create_cart(self, db: Session, user_id: str) -> CartDB:
        """Get the user's cart, creating one if it doesn't exist."""
        cart = db.query(CartDB).filter(CartDB.user_id == user_id).first()
        if not cart:
            cart = CartDB(
                id=f"cart_{uuid.uuid4().hex[:12]}",
                user_id=user_id,
            )
            db.add(cart)
            db.commit()
            db.refresh(cart)
        return cart

    def get_cart_with_items(self, db: Session, user_id: str) -> dict:
        """Get the user's cart with items.

        Item prices are snapshots for display only. Checkout re-reads
        ProductDB.price as the authoritative price.
        """
        cart = self.get_or_create_cart(db, user_id)
        items = db.query(CartItemDB).filter(CartItemDB.cart_id == cart.id).all()

        subtotal = 0.0
        item_dicts = []
        for item in items:
            product = db.query(ProductDB).filter(ProductDB.id == item.product_id).first()
            item_total = item.unit_price * item.quantity
            subtotal += item_total
            item_dicts.append({
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "title": product.title if product else "",
                "image_url": product.image_url if product else "",
                "stock": product.stock if product else 0,
            })

        return {
            "id": cart.id,
            "user_id": cart.user_id,
            "items": item_dicts,
            "subtotal": subtotal,
        }

    def add_item(
        self,
        db: Session,
        user_id: str,
        product_id: str,
        quantity: int = 1,
    ) -> dict:
        """Add a product to the user's cart."""
        cart = self.get_or_create_cart(db, user_id)

        # Check if product exists
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ProductNotFoundError(f"Product {product_id} not found")

        # Only live products can be added to the cart
        if product.status != "live":
            raise ProductNotAvailableError(f"{product.title} is not available")

        # Check if item already exists in cart
        existing = db.query(CartItemDB).filter(
            CartItemDB.cart_id == cart.id,
            CartItemDB.product_id == product_id,
        ).first()

        if existing:
            new_quantity = existing.quantity + quantity
            if product.stock < new_quantity:
                raise InsufficientStockError(
                    f"Only {product.stock} left for {product.title}"
                )
            existing.quantity = new_quantity
            db.commit()
            db.refresh(existing)
        else:
            if product.stock < quantity:
                raise InsufficientStockError(
                    f"Only {product.stock} left for {product.title}"
                )
            item = CartItemDB(
                id=f"item_{uuid.uuid4().hex[:12]}",
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
                unit_price=product.price,
            )
            db.add(item)
            db.commit()
            db.refresh(item)

        return self.get_cart_with_items(db, user_id)

    def update_item_quantity(
        self,
        db: Session,
        user_id: str,
        item_id: str,
        quantity: int,
    ) -> dict:
        """Update the quantity of a cart item."""
        cart = self.get_or_create_cart(db, user_id)

        item = db.query(CartItemDB).filter(
            CartItemDB.id == item_id,
            CartItemDB.cart_id == cart.id,
        ).first()

        if not item:
            raise ValueError(f"Cart item {item_id} not found")

        # Validate stock when increasing quantity (display data refreshed below)
        if quantity > 0:
            product = db.query(ProductDB).filter(
                ProductDB.id == item.product_id
            ).first()
            if product and product.stock < quantity:
                raise InsufficientStockError(
                    f"Only {product.stock} left for {product.title}"
                )

        if quantity <= 0:
            db.delete(item)
        else:
            item.quantity = quantity

        db.commit()
        return self.get_cart_with_items(db, user_id)

    def remove_item(self, db: Session, user_id: str, item_id: str) -> dict:
        """Remove an item from the cart."""
        cart = self.get_or_create_cart(db, user_id)

        item = db.query(CartItemDB).filter(
            CartItemDB.id == item_id,
            CartItemDB.cart_id == cart.id,
        ).first()

        if item:
            db.delete(item)
            db.commit()

        return self.get_cart_with_items(db, user_id)

    def clear_cart(self, db: Session, user_id: str) -> None:
        """Remove all items from the cart."""
        cart = self.get_or_create_cart(db, user_id)
        db.query(CartItemDB).filter(CartItemDB.cart_id == cart.id).delete()
        db.commit()


# ── Singleton ────────────────────────────────────────────────────────────────

cart_service = CartService()
