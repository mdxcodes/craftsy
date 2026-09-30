"""
Assisted GeM provider implementation.

This is the current production implementation. It does NOT make real API calls
to GeM. It provides:
- Registration guidance (Path A, B, C)
- Product readiness checking
- AI-assisted listing draft generation (with strict hallucination prevention)
- Listing kit generation
- Official portal handoff

Future:
- OfficialGeMApiProvider may replace assisted workflows once authorized API access exists.
"""

from __future__ import annotations

import json
import uuid
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

from sqlalchemy.orm import Session

from ..gem_adapter import gem_adapter
from ..gem.prompts import GEM_LISTING_SYSTEM_PROMPT, GEM_READINESS_SYSTEM_PROMPT
from ..gem.schemas import (
    GeMRegistrationOptions,
    GeMRegistrationGuidance,
    GeMReadinessResponse,
    GeMListingDraft,
    GeMListingKit,
    GeMOpenResponse,
)
from ...models.commerce_models import (
    GeMChannelStatus,
    ProductChannelDB,
    ChannelAuditLogDB,
    GEM_STATE_TRANSITIONS,
)
from ...models.db_models import ProductDB
from ...config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

# Official government links (centralized)
OFFICIAL_GEM_LINKS = {
    "seller_portal": "https://www.gem.gov.in/",
    "seller_learning": "https://www.gem.gov.in/seller-learning",
    "udyam_registration": "https://udyamregistration.gov.in/",
    "udyam_login": "https://udyamregistration.gov.in/",
}


class AssistedGeMProvider:
    """Assisted GeM provider — no direct API calls."""

    def __init__(self):
        pass

    # ── Registration ────────────────────────────────────────────────────────

    async def get_registration_options(self, artisan_id: str) -> dict:
        options = GeMRegistrationOptions(
            has_gem_account=None,
            has_udyam=None,
            seller_type=None,
            paths=[
                {
                    "id": "already_registered",
                    "label": "I already have a GeM seller account",
                    "description": "You have completed GeM seller registration and can list products directly.",
                },
                {
                    "id": "udyam_only",
                    "label": "I have Udyam/MSME but no GeM account",
                    "description": "You can use your Udyam registration to create a GeM seller account.",
                },
                {
                    "id": "new_seller",
                    "label": "I have neither Udyam nor GeM account",
                    "description": "You will need to register for Udyam/MSME and then GeM seller account.",
                },
            ],
        )
        return options.model_dump()

    async def get_registration_guidance(self, path: str, artisan_id: str) -> dict:
        if path == "already_registered":
            return GeMRegistrationGuidance(
                path=path,
                title="You are already registered on GeM",
                description="Open the official GeM seller portal and log in with your credentials. Craftsy will never ask for your GeM password or OTP.",
                steps=[
                    {"step": 1, "title": "Open GeM Seller Portal", "url": OFFICIAL_GEM_LINKS["seller_portal"]},
                    {"step": 2, "title": "Log in with your GeM credentials", "manual": True},
                    {"step": 3, "title": "Navigate to Product Catalogue", "manual": True},
                    {"step": 4, "title": "Use the Craftsy listing data to fill the form", "manual": True},
                ],
                official_links=OFFICIAL_GEM_LINKS,
            ).model_dump()

        if path == "udyam_only":
            return GeMRegistrationGuidance(
                path=path,
                title="Use your Udyam registration for GeM",
                description="GeM supports auto-registration using your Udyam Registration Number. Open the official Udyam portal to authenticate.",
                steps=[
                    {"step": 1, "title": "Open Udyam Login", "url": OFFICIAL_GEM_LINKS["udyam_login"]},
                    {"step": 2, "title": "Log in with Udyam Registration Number + OTP", "manual": True, "warning": "Never share your OTP with anyone."},
                    {"step": 3, "title": "Complete GeM seller onboarding on official portal", "manual": True},
                    {"step": 4, "title": "Return to Craftsy and prepare your listing", "manual": False},
                ],
                official_links=OFFICIAL_GEM_LINKS,
                warning="Craftsy does not collect or store Udyam OTP. Authentication happens entirely on the official government website.",
            ).model_dump()

        if path == "new_seller":
            return GeMRegistrationGuidance(
                path=path,
                title="Register for Udyam and GeM",
                description="You need both Udyam/MSME registration and a GeM seller account. Start with Udyam registration.",
                steps=[
                    {"step": 1, "title": "Start Udyam Registration", "url": OFFICIAL_GEM_LINKS["udyam_registration"]},
                    {"step": 2, "title": "Complete Udyam registration on official portal", "manual": True},
                    {"step": 3, "title": "Open GeM Seller Portal and register", "url": OFFICIAL_GEM_LINKS["seller_portal"]},
                    {"step": 4, "title": "Complete GeM seller onboarding", "manual": True},
                    {"step": 5, "title": "Return to Craftsy and prepare your listing", "manual": False},
                ],
                official_links=OFFICIAL_GEM_LINKS,
                warning="Udyam registration is free on the official government website. Avoid unofficial agents.",
            ).model_dump()

        raise ValueError(f"Unknown registration path: {path}")

    # ── Readiness ───────────────────────────────────────────────────────────

    async def validate_product(self, product_id: str, db: Optional[Session] = None) -> dict:
        if db is None:
            from ...database import SessionLocal
            db = SessionLocal()
        try:
            from .readiness_service import gem_readiness_service
            readiness = gem_readiness_service.check_readiness(db, product_id)
            return {
                "seller_ready": readiness.seller_ready,
                "product_ready": readiness.product_ready,
                "missing_information": readiness.missing_information,
                "missing_documents": readiness.missing_documents,
                "warnings": readiness.warnings,
                "category_requirements": readiness.category_requirements,
                "next_actions": readiness.next_actions,
                "ready_for_workflow": readiness.ready_for_workflow,
                "readiness_status": readiness.readiness_status,
                "available_fields": readiness.available_fields,
            }
        finally:
            if db is not None:
                db.close()

    async def prepare_listing(self, product_id: str, db: Optional[Session] = None) -> dict:
        draft = await self._generate_ai_listing(product_id, db)
        return {
            **draft,
            "copyable_text": self._build_copyable_text(draft),
        }

    # ── Listing Generation ──────────────────────────────────────────────────

    async def _generate_ai_listing(self, product_id: str, db: Optional[Session] = None) -> dict:
        """Generate a GeM listing draft from verified product data only."""
        from .listing_service import GeMListingService

        service = GeMListingService()
        return await service.generate_listing(product_id, db)

    async def generate_listing_kit(self, product_id: str, db: Optional[Session] = None) -> dict:
        draft = await self._generate_ai_listing(product_id, db)
        kit = GeMListingKit(
            draft=GeMListingDraft(**draft),
            copyable_text=self._build_copyable_text(draft),
            structured_data=draft,
            generated_at=datetime.now().isoformat(),
        )
        return kit.model_dump()

    def _build_copyable_text(self, draft: dict) -> str:
        lines = [
            "Product Name:",
            draft.get("product_name", "") or "Not provided",
            "",
            "Short Description:",
            draft.get("short_description", "") or "Not provided",
            "",
            "Description:",
            draft.get("description", "") or "Not provided",
            "",
            "Category:",
            draft.get("category", "") or "Not provided",
            "",
            "Price:",
            f"INR {draft.get('price', '')}" if draft.get("price") else "Not provided",
            "",
            "Specifications:",
        ]
        specs = draft.get("specifications", {})
        if specs:
            for key, value in specs.items():
                lines.append(f"{key}: {value}")
        else:
            lines.append("Not provided")
        lines.append("")

        artisan = draft.get("artisan_information", {})
        if artisan:
            lines.append("Artisan Information:")
            for key, value in artisan.items():
                if value:
                    lines.append(f"{key}: {value}")
            lines.append("")

        images = draft.get("images", [])
        if images:
            lines.append("Images:")
            for url in images:
                lines.append(url)
            lines.append("")

        certs = draft.get("certifications", [])
        if certs:
            lines.append("Certifications:")
            for c in certs:
                lines.append(c)
            lines.append("")
        else:
            lines.extend(["Certifications:", "Not provided", ""])

        warranty = draft.get("warranty")
        if warranty:
            lines.extend(["Warranty:", warranty, ""])
        else:
            lines.extend(["Warranty:", "Not provided", ""])

        missing = draft.get("missing_information", [])
        if missing:
            lines.append("Missing Information:")
            for item in missing:
                lines.append(f"- {item}")

        return "\n".join(lines)

    # ── Official Handoff ────────────────────────────────────────────────────

    async def open_official_gem(self) -> dict:
        return GeMOpenResponse(
            opened=True,
            url=OFFICIAL_GEM_LINKS["seller_portal"],
            message="Open the official GeM seller portal to complete your listing. Craftsy has prepared your listing data — use it on the GeM website.",
        ).model_dump()

    async def get_listing_status(self, product_id: str, db: Optional[Session] = None) -> dict:
        from ...database import SessionLocal
        from .readiness_service import gem_readiness_service

        local_db = db
        if local_db is None:
            local_db = SessionLocal()
        try:
            readiness = gem_readiness_service.check_readiness(local_db, product_id)
            return {
                "product_id": product_id,
                "status": "not_started",
                "readiness_status": readiness.readiness_status,
                "ready_for_workflow": readiness.ready_for_workflow,
                "message": "Assisted workflow — final submission must be completed by the artisan on the official GeM portal.",
            }
        finally:
            if db is None and local_db is not None:
                local_db.close()

    # ── State Management ────────────────────────────────────────────────────

    def update_gem_status(
        self,
        db: Session,
        product_id: str,
        status: str,
        error: Optional[str] = None,
        submission_reference: Optional[str] = None,
        listing_reference: Optional[str] = None,
    ) -> ProductChannelDB:
        product_channel = (
            db.query(ProductChannelDB)
            .filter(
                ProductChannelDB.product_id == product_id,
                ProductChannelDB.channel == "gem",
            )
            .first()
        )
        if not product_channel:
            product_channel = ProductChannelDB(
                id=f"pc_{uuid.uuid4().hex[:12]}",
                product_id=product_id,
                channel="gem",
                status=status,
            )
            db.add(product_channel)
        else:
            product_channel.status = status
            product_channel.updated_at = datetime.now()

        product_channel.gem_status = status
        if error:
            product_channel.gem_last_error = error
        if submission_reference:
            product_channel.gem_submission_reference = submission_reference
        if listing_reference:
            product_channel.gem_listing_reference = listing_reference
        if status in ("ready_for_submission", "submitted_by_seller"):
            product_channel.gem_prepared_at = datetime.now()
        product_channel.gem_last_opened_at = datetime.now()

        db.commit()
        db.refresh(product_channel)
        return product_channel


assisted_provider = AssistedGeMProvider()
