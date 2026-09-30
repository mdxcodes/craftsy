"""
GeM Readiness Service.

Examines the actual Craftsy ProductDB record and returns a structured
readiness assessment. Does not invent missing values.
"""

from __future__ import annotations

import logging
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from ...models.db_models import ProductDB
from ...models.commerce_models import GeMReadiness

logger = logging.getLogger(__name__)


class GeMReadinessService:
    """Examines ProductDB and returns GeM readiness assessment."""

    def check_readiness(self, db: Session, product_id: str) -> GeMReadiness:
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        missing_information: List[str] = []
        warnings: List[str] = []
        available_fields: List[str] = []
        category_requirements: List[str] = []
        next_actions: List[str] = []

        # Check product fields from ProductDB (canonical source)
        if not product.title or not product.title.strip():
            missing_information.append("Product title")
        else:
            available_fields.append("Product title")

        if not product.description or not product.description.strip():
            missing_information.append("Product description")
        else:
            available_fields.append("Product description")

        if not product.price or product.price <= 0:
            missing_information.append("Product price")
        else:
            available_fields.append(f"Product price (INR {product.price})")

        if not product.image_url or not product.image_url.strip():
            missing_information.append("Product image")
        else:
            available_fields.append("Product image")

        if not product.category or product.category == "General":
            warnings.append("Category is generic — please select a specific GeM-relevant category")
            missing_information.append("Product category")
        else:
            available_fields.append(f"Category: {product.category}")
            category_requirements.append(f"Category '{product.category}' must match GeM approved categories")

        # Additional product metadata from existing fields
        if hasattr(product, "tags_list") and product.tags_list:
            available_fields.append(f"Tags: {', '.join(product.tags_list)}")

        # Seller/document requirements — these are external to ProductDB
        missing_documents = [
            "GST Certificate",
            "PAN Card",
            "Aadhaar Card (of authorized person)",
            "Business Address Proof",
        ]

        # Determine readiness
        product_ready = len(missing_information) == 0
        seller_ready = False  # External — requires GeM portal verification
        ready_for_workflow = product_ready

        readiness_status = "ready" if product_ready else "needs_information"

        if missing_information:
            next_actions.append("Complete missing product information")
        if missing_documents:
            next_actions.append("Prepare seller documents for GeM registration")
        next_actions.append("Complete GeM seller registration on official portal")

        return GeMReadiness(
            seller_ready=seller_ready,
            product_ready=product_ready,
            missing_information=missing_information,
            missing_documents=missing_documents,
            warnings=warnings,
            category_requirements=category_requirements,
            next_actions=next_actions,
            ready_for_workflow=ready_for_workflow,
            readiness_status=readiness_status,
            available_fields=available_fields,
        )

    def to_response(self, readiness: GeMReadiness) -> Dict[str, Any]:
        return {
            "ready": readiness.ready_for_workflow,
            "missing_fields": readiness.missing_information,
            "warnings": readiness.warnings,
            "available_fields": readiness.available_fields,
            "category": None,  # derived from product
            "readiness_status": readiness.readiness_status,
            "next_actions": readiness.next_actions,
        }


gem_readiness_service = GeMReadinessService()
