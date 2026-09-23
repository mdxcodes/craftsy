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


# ── Singleton ────────────────────────────────────────────────────────────────

ondc_adapter = ONDCAdapter()
