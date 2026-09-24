"""
Commerce Channel Service.

Manages the multi-channel commerce abstraction:
- Craftsy Marketplace
- ONDC (Open Network for Digital Commerce)
- GeM (Government e-Marketplace)

This service does NOT implement real ONDC or GeM API calls.
It provides:
- Channel status management
- Channel-specific validation
- Product-channel relationship tracking
- Audit logging for all channel operations

Architecture:
    Flutter App → Craftsy Backend → CommerceService → Channel Adapters
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
    ChannelRequirement,
    ChannelRequirements,
    ChannelPublishRequest,
    ChannelPublishResponse,
    ChannelStatusResponse,
    ChannelStatusInfo,
    ProductWithChannels,
    ProductChannelDB,
    ChannelAuditLogDB,
    ONDC_REQUIRED_FIELDS,
    GEM_REQUIRED_FIELDS,
    CRAFTSY_REQUIRED_FIELDS,
)
from ..models.db_models import ProductDB
from ..models.schemas import ProductResponse

logger = logging.getLogger(__name__)


class CommerceService:
    """
    Manages the multi-commerce-channel layer.

    Provides channel abstraction, validation, status tracking,
    and audit logging. Does NOT implement real external API calls.
    """

    # ── Channel Configurations ──────────────────────────────────────────

    CHANNEL_LABELS = {
        ChannelType.CRAFTSY: "Craftsy Marketplace",
        ChannelType.ONDC: "ONDC",
        ChannelType.GEM: "Government Selling",
    }

    CHANNEL_ICONS = {
        ChannelType.CRAFTSY: "shopping_bag",
        ChannelType.ONDC: "public",
        ChannelType.GEM: "account_balance",
    }

    CHANNEL_COLORS = {
        ChannelType.CRAFTSY: "indigo",
        ChannelType.ONDC: "teal",
        ChannelType.GEM: "amber",
    }

    def __init__(self):
        pass

    # ── Product-Channel Relationship ────────────────────────────────────

    def get_or_create_product_channel(
        self,
        db: Session,
        product_id: str,
        channel: ChannelType,
    ) -> ProductChannelDB:
        """Get existing product-channel record or create a new one."""
        existing = (
            db.query(ProductChannelDB)
            .filter(
                ProductChannelDB.product_id == product_id,
                ProductChannelDB.channel == channel.value,
            )
            .first()
        )

        if existing:
            return existing

        # Determine initial status
        initial_status = self._get_initial_status(channel)

        product_channel = ProductChannelDB(
            id=f"pc_{uuid.uuid4().hex[:12]}",
            product_id=product_id,
            channel=channel.value,
            status=initial_status,
            channel_data="{}",
        )
        db.add(product_channel)
        db.commit()
        db.refresh(product_channel)
        return product_channel

    def _get_initial_status(self, channel: ChannelType) -> str:
        """Get initial status for a new product-channel record."""
        if channel == ChannelType.CRAFTSY:
            return CraftsyChannelStatus.DRAFT.value
        elif channel == ChannelType.ONDC:
            return ONDCChannelStatus.NOT_CONNECTED.value
        elif channel == ChannelType.GEM:
            return GeMChannelStatus.NOT_CONNECTED.value
        return "not_connected"

    # ── Channel Status ──────────────────────────────────────────────────

    def get_channel_status(
        self,
        db: Session,
        product_id: str,
        channel: ChannelType,
    ) -> ChannelStatusInfo:
        """Get the current status of a product on a specific channel."""
        product_channel = (
            db.query(ProductChannelDB)
            .filter(
                ProductChannelDB.product_id == product_id,
                ProductChannelDB.channel == channel.value,
            )
            .first()
        )

        if not product_channel:
            product_channel = self.get_or_create_product_channel(
                db, product_id, channel
            )

        status = product_channel.status
        is_connected = self._is_connected(channel, status)
        can_publish = self._can_publish(channel, status)
        missing = self._get_missing_requirements(db, product_id, channel)

        return ChannelStatusInfo(
            channel=channel.value,
            status=status,
            label=self.CHANNEL_LABELS[channel],
            icon=self.CHANNEL_ICONS[channel],
            color=self.CHANNEL_COLORS[channel],
            is_connected=is_connected,
            can_publish=can_publish,
            missing_requirements=missing,
            external_id=product_channel.external_id,
            external_url=product_channel.external_url,
            last_synced=product_channel.last_synced.isoformat()
            if product_channel.last_synced
            else None,
        )

    def get_all_channel_statuses(
        self,
        db: Session,
        product_id: str,
    ) -> List[ChannelStatusInfo]:
        """Get status for all channels for a product."""
        return [
            self.get_channel_status(db, product_id, channel)
            for channel in ChannelType
        ]

    def _is_connected(self, channel: ChannelType, status: str) -> bool:
        """Check if the channel is connected/active."""
        if channel == ChannelType.CRAFTSY:
            return status in [
                CraftsyChannelStatus.ACTIVE.value,
                CraftsyChannelStatus.DRAFT.value,
            ]
        elif channel == ChannelType.ONDC:
            return status not in [
                ONDCChannelStatus.NOT_CONNECTED.value,
                ONDCChannelStatus.DISCONNECTED.value,
            ]
        elif channel == ChannelType.GEM:
            return status not in [
                GeMChannelStatus.NOT_CONNECTED.value,
                GeMChannelStatus.DISCONNECTED.value,
            ]
        return False

    def _can_publish(self, channel: ChannelType, status: str) -> bool:
        """Check if the product can be published to this channel."""
        if channel == ChannelType.CRAFTSY:
            return status == CraftsyChannelStatus.DRAFT.value
        elif channel == ChannelType.ONDC:
            return status in [
                ONDCChannelStatus.READY.value,
                ONDCChannelStatus.NEEDS_INFORMATION.value,
            ]
        elif channel == ChannelType.GEM:
            return status in [
                GeMChannelStatus.READY.value,
                GeMChannelStatus.NEEDS_INFORMATION.value,
            ]
        return False

    # ── Validation ──────────────────────────────────────────────────────

    def validate_channel_requirements(
        self,
        db: Session,
        product_id: str,
        channel: ChannelType,
    ) -> ChannelRequirements:
        """Validate a product against channel-specific requirements."""
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        # Get required fields for this channel
        if channel == ChannelType.CRAFTSY:
            required_fields = CRAFTSY_REQUIRED_FIELDS
            status = CraftsyChannelStatus.DRAFT.value
        elif channel == ChannelType.ONDC:
            required_fields = ONDC_REQUIRED_FIELDS
            status = ONDCChannelStatus.NEEDS_INFORMATION.value
        elif channel == ChannelType.GEM:
            required_fields = GEM_REQUIRED_FIELDS
            status = GeMChannelStatus.NEEDS_INFORMATION.value
        else:
            required_fields = []
            status = "unknown"

        # Check each requirement
        requirements = []
        missing_fields = []
        product_data = self._product_to_dict(product)

        for field in required_fields:
            value = product_data.get(field)
            satisfied = value is not None and value != "" and value != 0
            req = ChannelRequirement(
                field=field,
                description=self._get_field_description(field),
                required=True,
                satisfied=satisfied,
                value=str(value) if satisfied else None,
            )
            requirements.append(req)
            if not satisfied:
                missing_fields.append(field)

        # Update status based on missing fields
        if not missing_fields:
            if channel == ChannelType.CRAFTSY:
                status = CraftsyChannelStatus.DRAFT.value
            elif channel == ChannelType.ONDC:
                status = ONDCChannelStatus.READY.value
            elif channel == ChannelType.GEM:
                status = GeMChannelStatus.READY.value

        return ChannelRequirements(
            channel=channel,
            status=status,
            requirements=requirements,
            missing_fields=missing_fields,
        )

    def _product_to_dict(self, product: ProductDB) -> Dict[str, Any]:
        """Convert ProductDB to dict for field checking."""
        return {
            "title": product.title,
            "title_hi": product.title_hi,
            "description": product.description,
            "description_hi": product.description_hi,
            "price": product.price,
            "image_url": product.image_url,
            "category": product.category,
            "tags": product.tags_list,
            "status": product.status,
            # ONDC-specific
            "weight": None,  # Not in current ProductDB
            "dimensions": None,
            "hsn_code": None,
            "country_of_origin": None,
            # GeM-specific
            "seller_gst": None,
            "seller_pan": None,
            "seller_aadhaar": None,
            "business_name": None,
            "business_address": None,
            "make_in_india": None,
        }

    def _get_field_description(self, field: str) -> str:
        """Get human-readable description for a field."""
        descriptions = {
            "title": "Product title",
            "description": "Product description",
            "price": "Selling price in INR",
            "image_url": "Product image URL",
            "category": "Craft category",
            "weight": "Product weight (grams)",
            "dimensions": "Product dimensions (L x W x H in cm)",
            "hsn_code": "HSN/SAC code for tax classification",
            "country_of_origin": "Country of manufacture",
            "seller_gst": "Seller GST number",
            "seller_pan": "Seller PAN number",
            "seller_aadhaar": "Seller Aadhaar number",
            "business_name": "Registered business name",
            "business_address": "Business address",
            "make_in_india": "Make in India certification",
        }
        return descriptions.get(field, field)

    def _get_missing_requirements(
        self,
        db: Session,
        product_id: str,
        channel: ChannelType,
    ) -> List[str]:
        """Get list of missing required fields for a channel."""
        validation = self.validate_channel_requirements(db, product_id, channel)
        return validation.missing_fields

    # ── Publishing (Foundation Only) ────────────────────────────────────

    def publish_to_channel(
        self,
        db: Session,
        product_id: str,
        channel: ChannelType,
        confirm: bool = False,
    ) -> ChannelPublishResponse:
        """
        Attempt to publish a product to a channel.

        This is the FOUNDATION implementation:
        - Craftsy: Updates internal status to ACTIVE
        - ONDC: Returns status indicating credentials needed
        - GeM: Returns status indicating eligibility/credentials needed

        Does NOT make real API calls.
        """
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        product_channel = self.get_or_create_product_channel(
            db, product_id, channel
        )
        status_before = product_channel.status

        # Validate requirements
        validation = self.validate_channel_requirements(db, product_id, channel)
        if validation.missing_fields:
            # Update status to needs_information
            new_status = self._get_needs_info_status(channel)
            self._log_audit(
                db, product_id, channel, "publish_attempt",
                status_before, new_status,
                message=f"Missing requirements: {', '.join(validation.missing_fields)}",
                success=False,
            )
            return ChannelPublishResponse(
                product_id=product_id,
                channel=channel,
                status=new_status,
                success=False,
                message=f"Product needs information: {', '.join(validation.missing_fields)}",
            )

        # Handle based on channel
        if channel == ChannelType.CRAFTSY:
            return self._publish_craftsy(
                db, product_id, product_channel, status_before, confirm
            )
        elif channel == ChannelType.ONDC:
            return self._publish_ondc_foundation(
                db, product_id, product_channel, status_before, confirm
            )
        elif channel == ChannelType.GEM:
            return self._publish_gem_foundation(
                db, product_id, product_channel, status_before, confirm
            )

        return ChannelPublishResponse(
            product_id=product_id,
            channel=channel,
            status="unknown",
            success=False,
            message="Unknown channel",
        )

    def _publish_craftsy(
        self,
        db: Session,
        product_id: str,
        product_channel: ProductChannelDB,
        status_before: str,
        confirm: bool,
    ) -> ChannelPublishResponse:
        """Publish to Craftsy marketplace (internal — just activates the product)."""
        if not confirm:
            return ChannelPublishResponse(
                product_id=product_id,
                channel=ChannelType.CRAFTSY,
                status=status_before,
                success=False,
                message="Confirmation required to publish to Craftsy",
            )

        # Activate the product on Craftsy
        product_channel.status = CraftsyChannelStatus.ACTIVE.value
        product_channel.updated_at = datetime.now()

        # Also update the product status
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if product:
            product.status = "live"
            product.updated_at = datetime.now()

        self._log_audit(
            db, product_id, ChannelType.CRAFTSY, "publish",
            status_before, CraftsyChannelStatus.ACTIVE.value,
            message="Product published to Craftsy marketplace",
            success=True,
        )

        db.commit()
        return ChannelPublishResponse(
            product_id=product_id,
            channel=ChannelType.CRAFTSY,
            status=CraftsyChannelStatus.ACTIVE.value,
            success=True,
            message="Product is now live on Craftsy marketplace",
        )

    def _publish_ondc_foundation(
        self,
        db: Session,
        product_id: str,
        product_channel: ProductChannelDB,
        status_before: str,
        confirm: bool,
    ) -> ChannelPublishResponse:
        """
        ONDC publishing foundation.

        Does NOT make real API calls. Returns status indicating
        that ONDC onboarding/credentials are required.
        """
        # Update status to indicate ready but not connected
        product_channel.status = ONDCChannelStatus.READY.value
        product_channel.updated_at = datetime.now()

        self._log_audit(
            db, product_id, ChannelType.ONDC, "publish_attempt",
            status_before, ONDCChannelStatus.READY.value,
            message="ONDC publish attempted — credentials/onboarding required",
            success=False,
        )

        db.commit()
        return ChannelPublishResponse(
            product_id=product_id,
            channel=ChannelType.ONDC,
            status=ONDCChannelStatus.READY.value,
            success=False,
            message="ONDC integration pending credentials. Complete ONDC onboarding to enable publishing.",
        )

    def _publish_gem_foundation(
        self,
        db: Session,
        product_id: str,
        product_channel: ProductChannelDB,
        status_before: str,
        confirm: bool,
    ) -> ChannelPublishResponse:
        """
        GeM publishing foundation.

        Does NOT make real API calls. Returns status indicating
        that GeM eligibility/credentials are required.
        """
        product_channel.status = GeMChannelStatus.ELIGIBILITY_REQUIRED.value
        product_channel.updated_at = datetime.now()

        self._log_audit(
            db, product_id, ChannelType.GEM, "publish_attempt",
            status_before, GeMChannelStatus.ELIGIBILITY_REQUIRED.value,
            message="GeM publish attempted — eligibility/credentials required",
            success=False,
        )

        db.commit()
        return ChannelPublishResponse(
            product_id=product_id,
            channel=ChannelType.GEM,
            status=GeMChannelStatus.ELIGIBILITY_REQUIRED.value,
            success=False,
            message="Government Selling requires seller eligibility verification and GeM onboarding.",
        )

    def _get_needs_info_status(self, channel: ChannelType) -> str:
        """Get the 'needs information' status for a channel."""
        if channel == ChannelType.CRAFTSY:
            return CraftsyChannelStatus.DRAFT.value
        elif channel == ChannelType.ONDC:
            return ONDCChannelStatus.NEEDS_INFORMATION.value
        elif channel == ChannelType.GEM:
            return GeMChannelStatus.NEEDS_INFORMATION.value
        return "needs_information"

    # ── Audit Logging ───────────────────────────────────────────────────

    def _log_audit(
        self,
        db: Session,
        product_id: str,
        channel: ChannelType,
        action: str,
        status_before: Optional[str],
        status_after: Optional[str],
        message: str = "",
        success: bool = True,
        external_id: Optional[str] = None,
    ) -> None:
        """Log a channel operation to the audit log."""
        audit = ChannelAuditLogDB(
            id=f"log_{uuid.uuid4().hex[:12]}",
            product_id=product_id,
            channel=channel.value,
            action=action,
            status_before=status_before,
            status_after=status_after,
            external_id=external_id,
            message=message[:1024] if message else None,
            success=1 if success else 0,
            created_at=datetime.now(),
        )
        db.add(audit)
        db.commit()

    def get_audit_logs(
        self,
        db: Session,
        product_id: Optional[str] = None,
        channel: Optional[ChannelType] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Get audit log entries, optionally filtered."""
        query = db.query(ChannelAuditLogDB)
        if product_id:
            query = query.filter(ChannelAuditLogDB.product_id == product_id)
        if channel:
            query = query.filter(ChannelAuditLogDB.channel == channel.value)
        query = query.order_by(ChannelAuditLogDB.created_at.desc()).limit(limit)

        logs = query.all()
        return [
            {
                "id": log.id,
                "product_id": log.product_id,
                "channel": log.channel,
                "action": log.action,
                "status_before": log.status_before,
                "status_after": log.status_after,
                "external_id": log.external_id,
                "message": log.message,
                "success": bool(log.success),
                "created_at": log.created_at.isoformat(),
            }
            for log in logs
        ]


# ── Singleton ────────────────────────────────────────────────────────────────

commerce_service = CommerceService()
