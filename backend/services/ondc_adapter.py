"""
ONDC Integration Adapter (Foundation).

This module provides the architectural scaffold for ONDC integration.
It does NOT make real API calls — it provides:
- ONDC requirement validation
- Status management
- Audit logging
- Clear documentation of what is needed for real integration

ONDC Architecture (from official docs):
    Flutter App
        ↓
    Craftsy Backend
        ↓
    ONDC Integration Service (this module)
        ↓
    ONDC Network (Beckn protocol)

ONDC Seller Roles (from official docs):
- ISN (Inventory Seller Node): Seller lists own inventory
- MSN (Marketplace Seller Node): Aggregator listing multiple sellers
- Buyer & Seller App: Both sides

ONDC Onboarding Requirements:
1. Register as Network Participant (subscriber_id)
2. Generate signing keys (Ed25519)
3. SSL certificate for domain
4. Complete /subscribe payload
5. Staging environment first
6. Pre-production certification
7. Production access

References:
- https://ondc.org/be/sellers
- https://github.com/ONDC-Official/developer-docs/blob/main/registry/Onboarding%20of%20Participants.md
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
    ONDCChannelStatus,
    ONDCError,
    ONDC_STATE_TRANSITIONS,
    ChannelRequirement,
    ChannelRequirements,
    ChannelPublishRequest,
    ChannelPublishResponse,
    ChannelStatusInfo,
    ProductChannelDB,
    ChannelAuditLogDB,
    ONDC_REQUIRED_FIELDS,
)
from ..models.db_models import ProductDB

logger = logging.getLogger(__name__)


class ONDCAdapter:
    """
    ONDC Integration Adapter.

    Foundation scaffold — does NOT make real API calls.
    Manages status, validation, and audit logging for ONDC integration.

    Real integration requires:
    1. ONDC Network Participant registration
    2. Signing key pair (Ed25519)
    3. SSL certificate
    4. Staging environment access
    5. Pre-production certification
    """

    # ONDC-specific field descriptions
    ONDC_FIELD_DESCRIPTIONS = {
        "title": "Product title (English)",
        "title_hi": "Product title (Hindi)",
        "description": "Product description (English)",
        "description_hi": "Product description (Hindi)",
        "price": "Selling price in INR",
        "image_url": "Product image URL (white background preferred)",
        "category": "Craft category (must match ONDC taxonomy)",
        "weight": "Product weight in grams (required for shipping)",
        "dimensions": "L x W x H in cm (required for shipping)",
        "hsn_code": "HSN/SAC code for tax classification",
        "country_of_origin": "Country of manufacture (e.g., India)",
        "brand": "Brand name (if applicable)",
        "model": "Product model number (if applicable)",
        "warranty": "Warranty period (if applicable)",
    }

    # ONDC catalogue categories relevant to crafts
    ONDC_CRAFT_CATEGORIES = [
        "Handicrafts",
        "Handloom",
        "Pottery",
        "Textiles",
        "Jewellery",
        "Woodwork",
        "Metalwork",
        "Paintings",
        "Carpets",
        "Bamboo Products",
    ]

    def __init__(self):
        pass

    def validate_product_for_ondc(
        self,
        db: Session,
        product_id: str,
    ) -> ChannelRequirements:
        """Validate a product against ONDC catalogue requirements."""
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        product_data = self._product_to_dict(product)
        requirements = []
        missing_fields = []

        for field in ONDC_REQUIRED_FIELDS:
            value = product_data.get(field)
            satisfied = value is not None and value != "" and value != 0

            req = ChannelRequirement(
                field=field,
                description=self.ONDC_FIELD_DESCRIPTIONS.get(field, field),
                required=True,
                satisfied=satisfied,
                value=str(value) if satisfied else None,
            )
            requirements.append(req)
            if not satisfied:
                missing_fields.append(field)

        # Determine status
        if not missing_fields:
            status = ONDCChannelStatus.READY.value
        else:
            status = ONDCChannelStatus.NEEDS_INFORMATION.value

        return ChannelRequirements(
            channel=ChannelType.ONDC,
            status=status,
            requirements=requirements,
            missing_fields=missing_fields,
        )

    def _product_to_dict(self, product: ProductDB) -> Dict[str, Any]:
        """Convert ProductDB to dict for ONDC field validation."""
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
            # ONDC-specific (not yet in ProductDB)
            "weight": None,
            "dimensions": None,
            "hsn_code": None,
            "country_of_origin": None,
            "brand": None,
            "model": None,
            "warranty": None,
        }

    def prepare_ondc_catalogue(
        self,
        db: Session,
        product_id: str,
    ) -> Dict[str, Any]:
        """
        Prepare ONDC catalogue payload (without sending).

        This maps Craftsy product fields to ONDC catalogue format.
        The actual API call would be made by the ONDC Integration Service
        once credentials are available.
        """
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        # ONDC catalogue item structure (simplified)
        catalogue_item = {
            "id": product.id,
            "descriptor": {
                "name": product.title,
                "short_desc": product.description[:200] if product.description else "",
                "long_desc": product.description,
            },
            "price": {
                "currency": "INR",
                "value": str(product.price),
            },
            "category_id": product.category,  # Would need ONDC category mapping
            "tags": product.tags_list or [],
        }

        return catalogue_item

    def sync_ondc_catalogue(
        self,
        db: Session,
        product_id: str,
    ) -> Dict[str, Any]:
        """
        Sync product to ONDC catalogue (foundation — no real API call).

        Returns the prepared payload and status indicating
        that real sync requires ONDC credentials.
        """
        catalogue_item = self.prepare_ondc_catalogue(db, product_id)
        return {
            "action": "sync_catalogue",
            "status": "not_configured",
            "message": "ONDC catalogue sync requires Network Participant credentials",
            "catalogue_item": catalogue_item,
            "external_id": None,
        }

    def get_ondc_orders(
        self,
        db: Session,
        artisan_id: str,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Get orders from ONDC (foundation — no real API call).

        Returns empty list with status indicating ONDC is not connected.
        Real implementation would poll ONDC for new orders.
        """
        return []

    def update_ondc_order_status(
        self,
        db: Session,
        order_id: str,
        new_status: str,
    ) -> Dict[str, Any]:
        """
        Update order status on ONDC (foundation — no real API call).

        Returns status indicating that real update requires ONDC credentials.
        """
        return {
            "action": "update_order_status",
            "status": "not_configured",
            "message": "ONDC order status update requires Network Participant credentials",
            "order_id": order_id,
            "requested_status": new_status,
        }

    def handle_ondc_cancellation(
        self,
        db: Session,
        order_id: str,
        reason: str,
    ) -> Dict[str, Any]:
        """
        Handle ONDC order cancellation (foundation — no real API call).

        Returns status indicating that real cancellation requires ONDC credentials.
        """
        return {
            "action": "cancel_order",
            "status": "not_configured",
            "message": "ONDC order cancellation requires Network Participant credentials",
            "order_id": order_id,
            "reason": reason,
        }

    def sync_ondc_inventory(
        self,
        db: Session,
        product_id: str,
        stock_quantity: int,
    ) -> Dict[str, Any]:
        """
        Sync inventory to ONDC (foundation — no real API call).

        Returns status indicating that real sync requires ONDC credentials.
        """
        return {
            "action": "sync_inventory",
            "status": "not_configured",
            "message": "ONDC inventory sync requires Network Participant credentials",
            "product_id": product_id,
            "stock_quantity": stock_quantity,
        }

    def reconcile_ondc_order_state(
        self,
        db: Session,
        order_id: str,
    ) -> Dict[str, Any]:
        """
        Reconcile ONDC order state with Craftsy order state (foundation).

        Returns status indicating that real reconciliation requires ONDC credentials.
        """
        return {
            "action": "reconcile_order",
            "status": "not_configured",
            "message": "ONDC order reconciliation requires Network Participant credentials",
            "order_id": order_id,
        }

    def get_ondc_onboarding_checklist(
        self,
        db: Session,
    ) -> Dict[str, Any]:
        """
        Get ONDC onboarding checklist for Craftsy.

        Based on official ONDC documentation.
        """
        return {
            "role": "Marketplace Seller Node (MSN)",
            "role_description": "Craftsy aggregates multiple artisans and lists their products",
            "environments": [
                {
                    "name": "Staging",
                    "url": "https://staging.registry.ondc.org",
                    "status": "not_started",
                    "description": "Initial integration and testing environment",
                },
                {
                    "name": "Pre-Production",
                    "url": "https://preprod.registry.ondc.org",
                    "status": "not_started",
                    "description": "Pre-production certification and readiness",
                },
                {
                    "name": "Production",
                    "url": "https://prod.registry.ondc.org",
                    "status": "not_started",
                    "description": "Live production environment",
                },
            ],
            "requirements": [
                {
                    "step": 1,
                    "title": "Register as Network Participant",
                    "description": "Create subscriber_id and complete /subscribe payload",
                    "status": "not_started",
                },
                {
                    "step": 2,
                    "title": "Generate Signing Keys",
                    "description": "Generate Ed25519 key pair for request signing",
                    "status": "not_started",
                },
                {
                    "step": 3,
                    "title": "SSL Certificate",
                    "description": "Obtain SSL certificate for your domain",
                    "status": "not_started",
                },
                {
                    "step": 4,
                    "title": "Domain Verification",
                    "description": "Host ondc-site-verification.html on your domain",
                    "status": "not_started",
                },
                {
                    "step": 5,
                    "title": "Staging Integration",
                    "description": "Complete staging environment testing",
                    "status": "not_started",
                },
                {
                    "step": 6,
                    "title": "Pre-Production Certification",
                    "description": "Pass pre-production certification",
                    "status": "not_started",
                },
                {
                    "step": 7,
                    "title": "Production Access",
                    "description": "Get production environment access",
                    "status": "not_started",
                },
            ],
            "api_reference": "https://app.swaggerhub.com/apis-docs/ONDC/ONDC-Registry-Onboarding/2.0.5",
            "documentation_url": "https://ondc.org/be/sellers",
            "contact": "ONDC Support Desk",
        }

    def validate_state_transition(
        self,
        current_status: ONDCChannelStatus,
        new_status: ONDCChannelStatus,
    ) -> bool:
        """Check if a state transition is valid."""
        allowed = ONDC_STATE_TRANSITIONS.get(current_status, [])
        return new_status in allowed

    def get_ondc_error(
        self,
        error_code: str,
        details: Optional[str] = None,
    ) -> ONDCError:
        """
        Get human-readable ONDC error for artisan display.

        Maps technical error codes to artisan-friendly messages.
        Never exposes raw JSON/protocol errors.
        """
        error_map = {
            "ONDC_NOT_CONFIGURED": ONDCError(
                error_code="ONDC_NOT_CONFIGURED",
                title="ONDC not connected",
                message="Connect your ONDC account to start selling.",
                action_required="Complete ONDC onboarding",
                is_retryable=False,
            ),
            "AUTH_FAILURE": ONDCError(
                error_code="AUTH_FAILURE",
                title="Connection problem",
                message="Could not connect to ONDC. Please check your credentials.",
                action_required="Re-enter ONDC credentials",
                is_retryable=True,
            ),
            "CREDENTIAL_MISSING": ONDCError(
                error_code="CREDENTIAL_MISSING",
                title="Account needed",
                message="ONDC account required. Complete setup to continue.",
                action_required="Complete ONDC onboarding",
                is_retryable=False,
            ),
            "VALIDATION_FAILED": ONDCError(
                error_code="VALIDATION_FAILED",
                title="Product information incomplete",
                message="Some required information is missing.",
                action_required="Complete product details",
                is_retryable=True,
            ),
            "CATEGORY_MAPPING_FAILED": ONDCError(
                error_code="CATEGORY_MAPPING_FAILED",
                title="Category not recognized",
                message="Your product category doesn't match ONDC categories.",
                action_required="Select a different category",
                is_retryable=True,
            ),
            "CATALOGUE_SYNC_FAILED": ONDCError(
                error_code="CATALOGUE_SYNC_FAILED",
                title="Could not share product",
                message="Your product could not be shared on ONDC. Please try again.",
                action_required="Try again",
                is_retryable=True,
            ),
            "INVENTORY_SYNC_FAILED": ONDCError(
                error_code="INVENTORY_SYNC_FAILED",
                title="Stock update failed",
                message="Could not update your stock on ONDC.",
                action_required="Try again",
                is_retryable=True,
            ),
            "ORDER_SYNC_FAILED": ONDCError(
                error_code="ORDER_SYNC_FAILED",
                title="Order sync problem",
                message="Could not sync your ONDC orders.",
                action_required="Try again",
                is_retryable=True,
            ),
            "NETWORK_TIMEOUT": ONDCError(
                error_code="NETWORK_TIMEOUT",
                title="Connection timed out",
                message="ONDC is not responding. Check your internet connection.",
                action_required="Check internet and try again",
                is_retryable=True,
            ),
            "SERVICE_UNAVAILABLE": ONDCError(
                error_code="SERVICE_UNAVAILABLE",
                title="ONDC temporarily unavailable",
                message="ONDC is currently unavailable. Please try again later.",
                action_required="Try again later",
                is_retryable=True,
            ),
            "EXTERNAL_REJECTION": ONDCError(
                error_code="EXTERNAL_REJECTION",
                title="ONDC rejected the request",
                message="ONDC did not accept your product. Please review and try again.",
                action_required="Review product information",
                is_retryable=True,
            ),
            "UNKNOWN_ERROR": ONDCError(
                error_code="UNKNOWN_ERROR",
                title="Something went wrong",
                message="An unexpected error occurred. Please try again.",
                action_required="Try again",
                is_retryable=True,
            ),
        }
        return error_map.get(error_code, error_map["UNKNOWN_ERROR"])


# ── Singleton ────────────────────────────────────────────────────────────────

ondc_adapter = ONDCAdapter()
