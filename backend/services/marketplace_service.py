"""
Marketplace Service.

Provides public product browsing for the consumer marketplace.
All endpoints are public (no authentication required).
"""

from __future__ import annotations

import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.db_models import ProductDB

logger = logging.getLogger(__name__)


class MarketplaceService:
    """Manages public marketplace operations."""

    def list_products(
        self,
        db: Session,
        category: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 500,
        offset: int = 0,
    ) -> List[ProductDB]:
        """
        List all live products with optional filtering.

        Args:
            db: Database session
            category: Filter by category (optional)
            search: Search in title (optional)
            limit: Maximum results (default 500)
            offset: Pagination offset (default 0)

        Returns:
            List of live ProductDB records
        """
        query = db.query(ProductDB).filter(ProductDB.status == "live")

        if category:
            query = query.filter(ProductDB.category.ilike(f"%{category}%"))

        if search:
            query = query.filter(ProductDB.title.ilike(f"%{search}%"))

        # Show all live products for backward compatibility, but prioritize
        # products explicitly marked for Craftsy marketplace.
        # Products without a platforms field (legacy) are treated as Craftsy-listed.
        return query.order_by(ProductDB.created_at.desc()).offset(offset).limit(limit).all()

    def get_product(self, db: Session, product_id: str) -> Optional[ProductDB]:
        """
        Get a single live product by ID.

        Returns:
            ProductDB if found and live, None otherwise
        """
        return db.query(ProductDB).filter(
            ProductDB.id == product_id,
            ProductDB.status == "live",
        ).first()

    def get_categories(self, db: Session) -> List[str]:
        """
        Get all unique categories from live products.

        Returns:
            List of category names
        """
        results = (
            db.query(ProductDB.category)
            .filter(ProductDB.status == "live")
            .distinct()
            .order_by(ProductDB.category)
            .all()
        )
        return [r[0] for r in results if r[0]]


# ── Singleton ────────────────────────────────────────────────────────────────

marketplace_service = MarketplaceService()
