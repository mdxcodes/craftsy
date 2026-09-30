"""GeM integration provider abstraction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class GeMIntegrationProvider(ABC):
    """Abstract interface for GeM integration providers."""

    @abstractmethod
    async def get_registration_options(self, artisan_id: str) -> dict:
        """Return available registration paths for an artisan."""
        raise NotImplementedError

    @abstractmethod
    async def get_registration_guidance(self, path: str, artisan_id: str) -> dict:
        """Return step-by-step guidance for a specific registration path."""
        raise NotImplementedError

    @abstractmethod
    async def validate_product(self, product_id: str) -> dict:
        """Validate a product against GeM requirements."""
        raise NotImplementedError

    @abstractmethod
    async def prepare_listing(self, product_id: str) -> dict:
        """Prepare a GeM listing draft from verified product data."""
        raise NotImplementedError

    @abstractmethod
    async def generate_listing_kit(self, product_id: str) -> dict:
        """Generate a human-readable GeM Listing Kit."""
        raise NotImplementedError

    @abstractmethod
    async def open_official_gem(self) -> dict:
        """Return the official GeM seller portal URL and metadata."""
        raise NotImplementedError

    @abstractmethod
    async def get_listing_status(self, product_id: str) -> dict:
        """Get the current GeM listing status for a product."""
        raise NotImplementedError
