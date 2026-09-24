"""
GeM (Government e-Marketplace) Integration Adapter (Foundation).

This module provides the architectural scaffold for GeM integration.
It does NOT make real API calls — it provides:
- GeM eligibility validation
- Seller registration requirements
- Guided workflow for assisted GeM onboarding
- Clear documentation of limitations

GeM Architecture (assisted workflow, NOT direct API):
    Flutter App
        ↓
    Craftsy Backend
        ↓
    GeM Integration Service (this module)
        ↓
    Government Selling Assistant (guided workflow)
        ↓
    Official GeM Portal (manual completion by artisan)

GeM Seller Registration Requirements (from official docs):
- Aadhaar of authorized person
- PAN of business/individual
- Mobile number linked with Aadhaar
- Registered email ID
- Udyam Registration (mandatory for MSMEs)
- GST Certificate
- Bank account details with cancelled cheque
- Business address proof
- ITR (sometimes required for OEM approvals)

GeM Seller Types:
- OEM (manufacturer/original producer)
- Reseller
- Service Provider
- Startup

References:
- https://www.gem.gov.in/
- https://leegal.in/how-to-register-on-gem-as-a-seller/
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
    GeMChannelStatus,
    GeMError,
    GeMReadiness,
    GEM_STATE_TRANSITIONS,
    ChannelRequirement,
    ChannelRequirements,
    ChannelPublishRequest,
    ChannelPublishResponse,
    ChannelStatusInfo,
    ProductChannelDB,
    ChannelAuditLogDB,
    GEM_REQUIRED_FIELDS,
)
from ..models.db_models import ProductDB

logger = logging.getLogger(__name__)


class GeMAdapter:
    """
    GeM Integration Adapter.

    Foundation scaffold — does NOT make real API calls.
    Provides guided workflow for artisan-assisted GeM onboarding.

    Real integration requires:
    1. Seller registration on GeM portal
    2. Document verification (GST, PAN, Aadhaar, Udyam)
    3. Product catalogue approval
    4. OEM/vendor assessment (if applicable)
    """

    # GeM-specific field descriptions
    GEM_FIELD_DESCRIPTIONS = {
        "title": "Product title (English)",
        "title_hi": "Product title (Hindi)",
        "description": "Product description (English)",
        "description_hi": "Product description (Hindi)",
        "price": "Selling price in INR (must be competitive)",
        "image_url": "Product image URL (white background required)",
        "category": "Craft category (must match GeM taxonomy)",
        "seller_gst": "Seller GST registration number",
        "seller_pan": "Seller PAN number",
        "seller_aadhaar": "Seller Aadhaar number",
        "business_name": "Registered business/legal entity name",
        "business_address": "Registered business address",
        "country_of_origin": "Country of manufacture",
        "make_in_india": "Make in India certification (if applicable)",
    }

    # GeM seller registration documents
    GEM_REQUIRED_DOCUMENTS = [
        "Aadhaar of Authorized Person",
        "PAN Card of Business/Individual",
        "Udyam Registration Certificate (MSME)",
        "GST Registration Certificate",
        "Bank Account Details with Cancelled Cheque",
        "Business Address Proof",
        "Mobile Number Linked with Aadhaar",
        "Registered Email ID",
        "Income Tax Return (last 3 years, if applicable)",
        "Certificate of Incorporation (if Pvt Ltd/LLP)",
    ]

    # GeM product categories relevant to crafts
    GEM_CRAFT_CATEGORIES = [
        "Handicrafts",
        "Handloom Products",
        "Pottery and Ceramics",
        "Textiles and Fabrics",
        "Jewellery and Ornaments",
        "Wood and Wood Products",
        "Metal Crafts",
        "Paintings and Artwork",
        "Carpets and Rugs",
        "Bamboo and Cane Products",
    ]

    def __init__(self):
        pass

    def validate_product_for_gem(
        self,
        db: Session,
        product_id: str,
    ) -> ChannelRequirements:
        """Validate a product against GeM catalogue requirements."""
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        product_data = self._product_to_dict(product)
        requirements = []
        missing_fields = []

        for field in GEM_REQUIRED_FIELDS:
            value = product_data.get(field)
            satisfied = value is not None and value != "" and value != 0

            req = ChannelRequirement(
                field=field,
                description=self.GEM_FIELD_DESCRIPTIONS.get(field, field),
                required=True,
                satisfied=satisfied,
                value=str(value) if satisfied else None,
            )
            requirements.append(req)
            if not satisfied:
                missing_fields.append(field)

        # Determine status
        if not missing_fields:
            status = GeMChannelStatus.READY.value
        else:
            status = GeMChannelStatus.NEEDS_INFORMATION.value

        return ChannelRequirements(
            channel=ChannelType.GEM,
            status=status,
            requirements=requirements,
            missing_fields=missing_fields,
        )

    def _product_to_dict(self, product: ProductDB) -> Dict[str, Any]:
        """Convert ProductDB to dict for GeM field validation."""
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
            # GeM-specific (not yet in ProductDB)
            "seller_gst": None,
            "seller_pan": None,
            "seller_aadhaar": None,
            "business_name": None,
            "business_address": None,
            "country_of_origin": None,
            "make_in_india": None,
        }

    def validate_state_transition(
        self,
        current_status: GeMChannelStatus,
        new_status: GeMChannelStatus,
    ) -> bool:
        """Check if a state transition is valid."""
        allowed = GEM_STATE_TRANSITIONS.get(current_status, [])
        return new_status in allowed

    def get_gem_error(
        self,
        error_code: str,
        details: Optional[str] = None,
    ) -> GeMError:
        """Get human-readable GeM error for artisan display."""
        error_map = {
            "GEM_NOT_CONNECTED": GeMError(
                error_code="GEM_NOT_CONNECTED",
                title="Government Selling not connected",
                message="Connect your GeM account to start selling.",
                action_required="Complete GeM seller registration",
                is_retryable=False,
            ),
            "GEM_REGISTRATION_REQUIRED": GeMError(
                error_code="GEM_REGISTRATION_REQUIRED",
                title="Seller registration required",
                message="You must register as a GeM seller to continue.",
                action_required="Complete GeM seller registration",
                is_retryable=False,
            ),
            "GEM_DOCUMENTS_REQUIRED": GeMError(
                error_code="GEM_DOCUMENTS_REQUIRED",
                title="Documents required",
                message="Please upload the required documents.",
                action_required="Upload required documents",
                is_retryable=True,
            ),
            "GEM_VERIFICATION_REQUIRED": GeMError(
                error_code="GEM_VERIFICATION_REQUIRED",
                title="Verification required",
                message="Your documents need to be verified by GeM.",
                action_required="Wait for GeM verification",
                is_retryable=False,
            ),
            "GEM_PRODUCT_REQUIREMENTS_MISSING": GeMError(
                error_code="GEM_PRODUCT_REQUIREMENTS_MISSING",
                title="Product requirements incomplete",
                message="Some required product information is missing.",
                action_required="Complete product details",
                is_retryable=True,
            ),
            "GEM_SUBMISSION_FAILED": GeMError(
                error_code="GEM_SUBMISSION_FAILED",
                title="Submission failed",
                message="Your product submission to GeM failed. Please try again.",
                action_required="Try again",
                is_retryable=True,
            ),
            "GEM_REJECTED": GeMError(
                error_code="GEM_REJECTED",
                title="GeM rejected the request",
                message="GeM did not accept your product. Please review and try again.",
                action_required="Review product information",
                is_retryable=True,
            ),
            "GEM_SERVICE_UNAVAILABLE": GeMError(
                error_code="GEM_SERVICE_UNAVAILABLE",
                title="GeM temporarily unavailable",
                message="GeM is currently unavailable. Please try again later.",
                action_required="Try again later",
                is_retryable=True,
            ),
            "GEM_UNKNOWN_ERROR": GeMError(
                error_code="GEM_UNKNOWN_ERROR",
                title="Something went wrong",
                message="An unexpected error occurred. Please try again.",
                action_required="Try again",
                is_retryable=True,
            ),
        }
        return error_map.get(error_code, error_map["GEM_UNKNOWN_ERROR"])

    def get_gem_readiness(
        self,
        db: Session,
        product_id: str,
    ) -> GeMReadiness:
        """Get GeM seller readiness assessment for a product."""
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        missing_information = []
        missing_documents = []
        warnings = []
        category_requirements = []
        next_actions = []

        # Check product information
        if not product.title:
            missing_information.append("Product title")
        if not product.description:
            missing_information.append("Product description")
        if not product.price or product.price <= 0:
            missing_information.append("Product price")
        if not product.image_url:
            missing_information.append("Product image")

        # Check GeM-specific fields (not yet in ProductDB)
        missing_documents.extend([
            "GST Certificate",
            "PAN Card",
            "Aadhaar Card",
            "Business Address Proof",
        ])

        # Category requirements
        category_requirements.append("Category must match GeM approved categories")

        # Determine readiness
        seller_ready = len(missing_documents) == 0
        product_ready = len(missing_information) == 0
        ready_for_workflow = seller_ready and product_ready

        # Next actions
        if missing_information:
            next_actions.append("Complete product information")
        if missing_documents:
            next_actions.append("Upload required documents")
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
            readiness_status="ready" if ready_for_workflow else "not_ready",
        )

    def get_gem_seller_checklist(
        self,
        db: Session,
    ) -> Dict[str, Any]:
        """
        Get GeM seller registration checklist.

        Based on official GeM documentation.
        """
        return {
            "title": "GeM Seller Registration",
            "description": "Complete the following steps to register as a GeM seller",
            "seller_types": [
                {
                    "name": "OEM (Manufacturer)",
                    "description": "Original Equipment Manufacturer — you make the product",
                    "requirements": ["Factory address proof", "Brand ownership", "Production capacity"],
                },
                {
                    "name": "Reseller",
                    "description": "You sell products made by others",
                    "requirements": ["Trade license", "Brand authorization"],
                },
                {
                    "name": "Service Provider",
                    "description": "You provide services",
                    "requirements": ["Service registration", "Qualification proof"],
                },
                {
                    "name": "Startup",
                    "description": "Registered startup",
                    "requirements": ["DPIIT recognition", "Startup certificate"],
                },
            ],
            "documents": [
                {
                    "name": doc,
                    "required": True,
                    "status": "pending",
                }
                for doc in self.GEM_REQUIRED_DOCUMENTS
            ],
            "steps": [
                {
                    "step": 1,
                    "title": "Visit GeM Portal",
                    "url": "https://www.gem.gov.in/",
                    "status": "not_started",
                },
                {
                    "step": 2,
                    "title": "Sign Up as Seller",
                    "status": "not_started",
                },
                {
                    "step": 3,
                    "title": "Aadhaar & Email Verification",
                    "status": "not_started",
                },
                {
                    "step": 4,
                    "title": "Business Profile Creation",
                    "status": "not_started",
                },
                {
                    "step": 5,
                    "title": "Bank Account Verification",
                    "status": "not_started",
                },
                {
                    "step": 6,
                    "title": "Upload Documents",
                    "status": "not_started",
                },
                {
                    "step": 7,
                    "title": "Category Selection",
                    "status": "not_started",
                },
                {
                    "step": 8,
                    "title": "Product Catalogue Upload",
                    "status": "not_started",
                },
                {
                    "step": 9,
                    "title": "OEM/Brand Approval (if applicable)",
                    "status": "not_started",
                },
                {
                    "step": 10,
                    "title": "Final KYC & Verification",
                    "status": "not_started",
                },
                {
                    "step": 11,
                    "title": "Start Selling",
                    "status": "not_started",
                },
            ],
            "automation_limitations": {
                "can_automate": [
                    "Product data preparation",
                    "Category mapping suggestions",
                    "Document checklist tracking",
                    "Eligibility validation",
                ],
                "cannot_automate": [
                    "Seller registration on GeM portal",
                    "Document upload to GeM",
                    "GST/PAN/Aadhaar verification",
                    "OEM/vendor assessment",
                    "Bid participation",
                    "Invoice generation",
                ],
                "reason": "GeM does not provide a public API for seller registration or catalogue management. Sellers must complete registration on the official GeM portal.",
            },
        }

    def get_gem_guided_workflow(
        self,
        db: Session,
        product_id: str,
    ) -> Dict[str, Any]:
        """
        Get guided workflow for GeM selling preparation.

        This prepares the artisan for the manual steps they need to take
        on the official GeM portal.
        """
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        validation = self.validate_product_for_gem(db, product_id)

        return {
            "product_id": product_id,
            "product_title": product.title,
            "readiness_status": validation.status,
            "missing_fields": validation.missing_fields,
            "workflow": [
                {
                    "phase": 1,
                    "title": "Eligibility Check",
                    "status": "pending",
                    "tasks": [
                        "Verify business type (Proprietorship/Partnership/Pvt Ltd/LLP)",
                        "Check Udyam Registration status",
                        "Verify GST registration",
                        "Confirm Aadhaar-linked mobile number",
                    ],
                },
                {
                    "phase": 2,
                    "title": "Document Preparation",
                    "status": "pending",
                    "tasks": [
                        "Scan PAN card",
                        "Scan Aadhaar card",
                        "Scan GST certificate",
                        "Scan Udyam certificate (if MSME)",
                        "Prepare cancelled cheque",
                        "Gather business address proof",
                    ],
                },
                {
                    "phase": 3,
                    "title": "GeM Portal Registration",
                    "status": "pending",
                    "manual": True,
                    "tasks": [
                        "Visit https://www.gem.gov.in/",
                        "Click Sign Up → Seller",
                        "Complete Aadhaar & email verification",
                        "Fill business profile",
                        "Upload documents",
                        "Complete bank verification",
                    ],
                },
                {
                    "phase": 4,
                    "title": "Product Listing on GeM",
                    "status": "pending",
                    "manual": True,
                    "tasks": [
                        "Select category",
                        "Fill product details from Craftsy data",
                        "Upload product images (white background)",
                        "Set pricing",
                        "Submit for approval",
                    ],
                },
            ],
            "craftsy_data_ready": {
                "title": product.title,
                "description": product.description,
                "price": product.price,
                "category": product.category,
                "image_url": product.image_url,
                "tags": product.tags_list,
            },
            "next_action": "Complete GeM seller registration on the official portal",
            "estimated_time": "2-5 working days for verification",
        }


# ── Singleton ────────────────────────────────────────────────────────────────

gem_adapter = GeMAdapter()
