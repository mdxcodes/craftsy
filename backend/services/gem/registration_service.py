"""
GeM Registration Service.

Provides registration guidance and official link handoff.
Does NOT collect credentials or attempt automated registration.
"""

from __future__ import annotations

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class GeMRegistrationService:
    """Registration guidance and official handoff."""

    OFFICIAL_LINKS = {
        "seller_portal": "https://www.gem.gov.in/",
        "seller_learning": "https://www.gem.gov.in/seller-learning",
        "udyam_registration": "https://udyamregistration.gov.in/",
        "udyam_login": "https://udyamregistration.gov.in/",
    }

    def get_registration_options(self) -> Dict[str, Any]:
        return {
            "paths": [
                {
                    "id": "already_registered",
                    "label": "I already have a GeM seller account",
                    "description": "Open GeM portal and log in directly.",
                },
                {
                    "id": "udyam_only",
                    "label": "I have Udyam/MSME registration but no GeM account",
                    "description": "Use your Udyam credentials to auto-register on GeM.",
                },
                {
                    "id": "new_seller",
                    "label": "I have neither Udyam nor GeM account",
                    "description": "Register for Udyam first, then create your GeM seller account.",
                },
            ],
            "official_links": self.OFFICIAL_LINKS,
        }

    def get_guidance(self, path: str) -> Dict[str, Any]:
        if path == "already_registered":
            return {
                "path": path,
                "title": "Open GeM Seller Portal",
                "description": "Log in with your existing GeM seller credentials.",
                "steps": [
                    {"step": 1, "title": "Open GeM Seller Portal", "url": self.OFFICIAL_LINKS["seller_portal"]},
                    {"step": 2, "title": "Log in with your credentials", "manual": True},
                    {"step": 3, "title": "Go to Product Catalogue", "manual": True},
                    {"step": 4, "title": "Use Craftsy listing data to create your listing", "manual": True},
                ],
                "official_links": self.OFFICIAL_LINKS,
            }

        if path == "udyam_only":
            return {
                "path": path,
                "title": "Use Udyam Registration for GeM",
                "description": "Authenticate on the official Udyam portal to start GeM onboarding.",
                "steps": [
                    {"step": 1, "title": "Open Udyam Login", "url": self.OFFICIAL_LINKS["udyam_login"]},
                    {"step": 2, "title": "Log in with Udyam Registration Number + OTP", "manual": True},
                    {"step": 3, "title": "Complete GeM onboarding on official portal", "manual": True},
                    {"step": 4, "title": "Return to Craftsy to prepare listing", "manual": False},
                ],
                "official_links": self.OFFICIAL_LINKS,
                "warning": "Never share your OTP. Authentication happens only on official government websites.",
            }

        if path == "new_seller":
            return {
                "path": path,
                "title": "Register for Udyam and GeM",
                "description": "You need both Udyam/MSME registration and a GeM seller account.",
                "steps": [
                    {"step": 1, "title": "Start Udyam Registration", "url": self.OFFICIAL_LINKS["udyam_registration"]},
                    {"step": 2, "title": "Complete Udyam registration", "manual": True},
                    {"step": 3, "title": "Register as GeM Seller", "url": self.OFFICIAL_LINKS["seller_portal"]},
                    {"step": 4, "title": "Complete GeM seller onboarding", "manual": True},
                    {"step": 5, "title": "Return to Craftsy to prepare listing", "manual": False},
                ],
                "official_links": self.OFFICIAL_LINKS,
                "warning": "Udyam registration is free on the official government website. Avoid unofficial agents.",
            }

        raise ValueError(f"Unknown registration path: {path}")

    def open_seller_portal(self) -> Dict[str, Any]:
        return {
            "url": self.OFFICIAL_LINKS["seller_portal"],
            "message": "Open the official GeM seller portal to complete your listing. Craftsy has prepared your listing data — use it on the GeM website.",
        }

    def open_udyam_portal(self) -> Dict[str, Any]:
        return {
            "url": self.OFFICIAL_LINKS["udyam_registration"],
            "message": "Open the official Udyam registration portal.",
        }


gem_registration_service = GeMRegistrationService()
