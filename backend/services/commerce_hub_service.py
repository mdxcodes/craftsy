"""
Unified Commerce Hub Service.

Provides a single entry point for all commerce operations across channels:
- Craftsy Marketplace
- ONDC
- GeM (Government Selling)

This service unifies:
- ONE product model
- ONE inventory source
- ONE order experience
- ONE artisan profile
- MULTIPLE channel adapters

Architecture:
    Flutter App → CommerceHubService → Channel Adapters
                                          ├── CraftsyChannel
                                          ├── ONDCChannel
                                          └── GeMChannel
"""

from __future__ import annotations

import json
import uuid
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from ..models.commerce_models import (
    ChannelType,
    CraftsyChannelStatus,
    ONDCChannelStatus,
    GeMChannelStatus,
    ChannelStatusInfo,
    ChannelRequirements,
    ProductChannelDB,
    ChannelAuditLogDB,
    ONDC_REQUIRED_FIELDS,
    GEM_REQUIRED_FIELDS,
    CRAFTSY_REQUIRED_FIELDS,
)
from ..models.order_models import (
    OrderDB,
    OrderCreate,
    OrderResponse,
    OrderChannelSummary,
    OrderChannel,
)
from ..models.db_models import ProductDB, ArtisanDB
from ..services.commerce_service import commerce_service
from ..services.order_service import order_service
from ..services.ondc_adapter import ondc_adapter
from ..services.gem_adapter import gem_adapter

logger = logging.getLogger(__name__)


class CommerceHubService:
    """
    Unified Commerce Hub — single entry point for all commerce operations.

    Coordinates between channels while keeping one source of truth for
    products, inventory, and orders.
    """

    # ── User-Facing Status Vocabulary ─────────────────────────────────

    STATUS_LABELS = {
        # Craftsy
        CraftsyChannelStatus.ACTIVE.value: "Active",
        CraftsyChannelStatus.INACTIVE.value: "Inactive",
        CraftsyChannelStatus.DRAFT.value: "Draft",
        # ONDC
        ONDCChannelStatus.NOT_CONFIGURED.value: "Not Configured",
        ONDCChannelStatus.PENDING_ONBOARDING.value: "Setup in Progress",
        ONDCChannelStatus.CREDENTIALS_REQUIRED.value: "Account Needed",
        ONDCChannelStatus.VALIDATION_REQUIRED.value: "Validation Needed",
        ONDCChannelStatus.READY_TO_PUBLISH.value: "Ready",
        ONDCChannelStatus.PUBLISHED.value: "Live",
        ONDCChannelStatus.SYNCING.value: "Updating",
        ONDCChannelStatus.SYNCED.value: "Up to Date",
        ONDCChannelStatus.ERROR.value: "Problem",
        ONDCChannelStatus.NOT_CONNECTED.value: "Not Connected",
        ONDCChannelStatus.NEEDS_INFORMATION.value: "Needs Information",
        ONDCChannelStatus.READY.value: "Ready",
        ONDCChannelStatus.PENDING.value: "Pending",
        ONDCChannelStatus.FAILED.value: "Failed",
        ONDCChannelStatus.DISCONNECTED.value: "Disconnected",
        # GeM
        GeMChannelStatus.NOT_CONNECTED.value: "Not Started",
        GeMChannelStatus.NOT_STARTED.value: "Not Started",
        GeMChannelStatus.PROFILE_INCOMPLETE.value: "Profile Incomplete",
        GeMChannelStatus.DOCUMENTS_REQUIRED.value: "Documents Needed",
        GeMChannelStatus.VERIFICATION_REQUIRED.value: "Verification Needed",
        GeMChannelStatus.PRODUCT_REQUIREMENTS_MISSING.value: "Product Info Needed",
        GeMChannelStatus.READY_FOR_SUBMISSION.value: "Ready",
        GeMChannelStatus.SUBMISSION_PENDING.value: "Pending",
        GeMChannelStatus.PUBLISHED.value: "Live",
        GeMChannelStatus.ACTIVE.value: "Active",
        GeMChannelStatus.ACTION_REQUIRED.value: "Action Needed",
        GeMChannelStatus.ERROR.value: "Problem",
        GeMChannelStatus.ELIGIBILITY_REQUIRED.value: "Eligibility Check",
        GeMChannelStatus.NEEDS_INFORMATION.value: "Needs Information",
        GeMChannelStatus.READY.value: "Ready",
        GeMChannelStatus.PENDING.value: "Pending",
        GeMChannelStatus.REJECTED.value: "Rejected",
        GeMChannelStatus.DISCONNECTED.value: "Disconnected",
        GeMChannelStatus.ASSISTED_WORKFLOW.value: "Guided Setup",
    }

    # ── Commerce Hub Summary ──────────────────────────────────────────

    def get_commerce_summary(
        self,
        db: Session,
        artisan_id: str,
    ) -> Dict[str, Any]:
        """Get a unified commerce summary for the artisan dashboard."""
        # Product counts
        total_products = (
            db.query(ProductDB)
            .filter(ProductDB.artisan_id == artisan_id)
            .count()
        )
        live_products = (
            db.query(ProductDB)
            .filter(
                ProductDB.artisan_id == artisan_id,
                ProductDB.status == "live",
            )
            .count()
        )

        # Channel counts
        channel_counts = {}
        for channel in ChannelType:
            channel_counts[channel.value] = (
                db.query(ProductChannelDB)
                .join(ProductDB)
                .filter(
                    ProductDB.artisan_id == artisan_id,
                    ProductChannelDB.channel == channel.value,
                )
                .count()
            )

        # Orders
        total_orders = (
            db.query(OrderDB)
            .filter(OrderDB.artisan_id == artisan_id)
            .count()
        )

        # Products needing attention
        products_needing_attention = 0
        products = (
            db.query(ProductDB)
            .filter(ProductDB.artisan_id == artisan_id)
            .all()
        )
        product_ids = [p.id for p in products]
        all_pcs = (
            db.query(ProductChannelDB)
            .filter(ProductChannelDB.product_id.in_(product_ids))
            .all()
        ) if product_ids else []
        pc_map = {}
        for pc in all_pcs:
            pc_map.setdefault(pc.product_id, []).append(pc)

        for product in products:
            for channel in ChannelType:
                if channel == ChannelType.CRAFTSY:
                    continue
                pcs = pc_map.get(product.id, [])
                if not pcs:
                    continue
                pc = next((p for p in pcs if p.channel == channel.value), None)
                if pc and pc.status in [
                    ONDCChannelStatus.NEEDS_INFORMATION.value,
                    ONDCChannelStatus.ERROR.value,
                    GeMChannelStatus.NEEDS_INFORMATION.value,
                    GeMChannelStatus.ERROR.value,
                    GeMChannelStatus.DOCUMENTS_REQUIRED.value,
                    GeMChannelStatus.PROFILE_INCOMPLETE.value,
                ]:
                    products_needing_attention += 1
                    break

        # Low stock products
        low_stock = (
            db.query(ProductDB)
            .filter(
                ProductDB.artisan_id == artisan_id,
                ProductDB.stock <= 5,
                ProductDB.status == "live",
            )
            .count()
        )

        return {
            "total_products": total_products,
            "live_products": live_products,
            "channel_counts": channel_counts,
            "total_orders": total_orders,
            "products_needing_attention": products_needing_attention,
            "low_stock": low_stock,
        }

    # ── Product Channel Status ────────────────────────────────────────

    def get_product_channels(
        self,
        db: Session,
        product_id: str,
    ) -> List[Dict[str, Any]]:
        """Get channel statuses for a product with user-facing labels."""
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        channels = []
        for channel_type in ChannelType:
            status_info = commerce_service.get_channel_status(
                db, product_id, channel_type
            )
            channels.append({
                "channel": channel_type.value,
                "status": status_info.status,
                "label": status_info.label,
                "icon": status_info.icon,
                "color": status_info.color,
                "is_connected": status_info.is_connected,
                "can_publish": status_info.can_publish,
                "missing_requirements": status_info.missing_requirements,
                "display_status": self.STATUS_LABELS.get(
                    status_info.status, status_info.status
                ),
            })

        return channels

    def get_product_detail_with_channels(
        self,
        db: Session,
        product_id: str,
    ) -> Dict[str, Any]:
        """Get product detail with channel information."""
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        return {
            "id": product.id,
            "title": product.title,
            "title_hi": product.title_hi,
            "description": product.description,
            "description_hi": product.description_hi,
            "price": product.price,
            "image_url": product.image_url,
            "category": product.category,
            "status": product.status,
            "stock": product.stock,
            "tags": product.tags_list,
            "channels": self.get_product_channels(db, product_id),
        }

    # ── Unified Inventory ─────────────────────────────────────────────

    def get_inventory(
        self,
        db: Session,
        product_id: str,
    ) -> Dict[str, Any]:
        """Get unified inventory for a product (one source of truth)."""
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        return {
            "product_id": product_id,
            "available": product.stock,
            "reserved": 0,
            "committed": 0,
            "fulfilled": 0,
        }

    def update_stock(
        self,
        db: Session,
        product_id: str,
        new_stock: int,
    ) -> ProductDB:
        """Update product stock (single source of truth for all channels)."""
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        old_stock = product.stock
        product.stock = max(0, new_stock)
        product.updated_at = datetime.now()

        # Log the change
        commerce_service._log_audit(
            db, product_id, ChannelType.CRAFTSY, "stock_update",
            str(old_stock), str(product.stock),
            message=f"Stock updated from {old_stock} to {product.stock}",
            success=True,
        )

        db.commit()
        db.refresh(product)
        return product

    # ── Unified Orders ────────────────────────────────────────────────

    def get_unified_orders(
        self,
        db: Session,
        artisan_id: str,
        channel: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> List[OrderResponse]:
        """Get all orders for an artisan across all channels."""
        return order_service.get_orders(db, artisan_id, channel, status, limit)

    def get_order_channel_summary(
        self,
        db: Session,
        artisan_id: str,
    ) -> List[OrderChannelSummary]:
        """Get order summary grouped by channel."""
        return order_service.get_channel_summary(db, artisan_id)

    # ── Cross-Channel Product Sync ────────────────────────────────────

    def get_sync_status(
        self,
        db: Session,
        product_id: str,
    ) -> Dict[str, Any]:
        """Get sync status across all channels for a product."""
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        sync_status = {}
        for channel in ChannelType:
            pc = (
                db.query(ProductChannelDB)
                .filter(
                    ProductChannelDB.product_id == product_id,
                    ProductChannelDB.channel == channel.value,
                )
                .first()
            )

            if pc:
                sync_status[channel.value] = {
                    "status": pc.status,
                    "last_synced": pc.last_synced.isoformat() if pc.last_synced else None,
                    "external_id": pc.external_id,
                    "sync_state": self._get_sync_state(pc.status),
                }
            else:
                sync_status[channel.value] = {
                    "status": "not_configured",
                    "last_synced": None,
                    "external_id": None,
                    "sync_state": "not_configured",
                }

        return {
            "product_id": product_id,
            "product_updated": product.updated_at.isoformat(),
            "channels": sync_status,
        }

    def _get_sync_state(self, channel_status: str) -> str:
        """Map channel status to a user-facing sync state."""
        # Craftsy
        if channel_status == CraftsyChannelStatus.ACTIVE.value:
            return "synced"
        if channel_status == CraftsyChannelStatus.DRAFT.value:
            return "draft"

        # ONDC
        if channel_status == ONDCChannelStatus.PUBLISHED.value:
            return "synced"
        if channel_status == ONDCChannelStatus.SYNCING.value:
            return "syncing"
        if channel_status == ONDCChannelStatus.ERROR.value:
            return "error"
        if channel_status in [
            ONDCChannelStatus.NEEDS_INFORMATION.value,
            ONDCChannelStatus.CREDENTIALS_REQUIRED.value,
        ]:
            return "needs_attention"

        # GeM
        if channel_status == GeMChannelStatus.PUBLISHED.value:
            return "synced"
        if channel_status == GeMChannelStatus.ACTIVE.value:
            return "synced"
        if channel_status == GeMChannelStatus.ERROR.value:
            return "error"
        if channel_status in [
            GeMChannelStatus.DOCUMENTS_REQUIRED.value,
            GeMChannelStatus.PROFILE_INCOMPLETE.value,
            GeMChannelStatus.NEEDS_INFORMATION.value,
            GeMChannelStatus.ASSISTED_WORKFLOW.value,
        ]:
            return "needs_attention"

        return "not_configured"

    # ── Channel Actions ───────────────────────────────────────────────

    def enable_channel(
        self,
        db: Session,
        product_id: str,
        channel: ChannelType,
    ) -> Dict[str, Any]:
        """Enable a channel for a product."""
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        pc = commerce_service.get_or_create_product_channel(
            db, product_id, channel
        )

        return {
            "product_id": product_id,
            "channel": channel.value,
            "status": pc.status,
            "display_status": self.STATUS_LABELS.get(pc.status, pc.status),
        }

    def disable_channel(
        self,
        db: Session,
        product_id: str,
        channel: ChannelType,
    ) -> Dict[str, Any]:
        """Disable a channel for a product."""
        pc = (
            db.query(ProductChannelDB)
            .filter(
                ProductChannelDB.product_id == product_id,
                ProductChannelDB.channel == channel.value,
            )
            .first()
        )

        if not pc:
            raise ValueError(f"Channel {channel.value} not enabled for product {product_id}")

        if channel == ChannelType.CRAFTSY:
            pc.status = CraftsyChannelStatus.INACTIVE.value
        elif channel == ChannelType.ONDC:
            pc.status = ONDCChannelStatus.DISCONNECTED.value
        elif channel == ChannelType.GEM:
            pc.status = GeMChannelStatus.DISCONNECTED.value

        pc.updated_at = datetime.now()

        commerce_service._log_audit(
            db, product_id, channel, "disable",
            pc.status, pc.status,
            message=f"Channel {channel.value} disabled",
            success=True,
        )

        db.commit()
        return {
            "product_id": product_id,
            "channel": channel.value,
            "status": pc.status,
            "display_status": self.STATUS_LABELS.get(pc.status, pc.status),
        }


# ── Singleton ────────────────────────────────────────────────────────────────

commerce_hub_service = CommerceHubService()
