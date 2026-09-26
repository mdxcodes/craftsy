"""Craftsy <-> ONDC payload mapping."""

from __future__ import annotations

import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from ...models.db_models import ProductDB

logger = logging.getLogger(__name__)


class ONDCMapper:
    """Maps Craftsy product/order data to/from ONDC Retail protocol format."""

    def __init__(self) -> None:
        self.bpp_id = "craftsy.bpp.hackathon"
        self.bpp_uri = "http://localhost:8000/api/v1/ondc"
        self.bpp_descriptor = {
            "name": "Craftsy BPP",
            "short_desc": "Handicrafts and artisan marketplace",
        }

    def map_product_to_ondc_item(
        self,
        product: ProductDB,
        fulfillment_id: str = "F1",
        location_id: str = "L1",
    ) -> Dict[str, Any]:
        """Map a Craftsy ProductDB to an ONDC catalog item."""
        return {
            "id": product.id,
            "descriptor": {
                "name": product.title,
                "short_desc": (product.description or "")[:200],
                "images": [product.image_url] if product.image_url else [],
            },
            "category_id": product.category or "General",
            "price": {
                "currency": "INR",
                "value": str(round(float(product.price or 0.0), 2)),
            },
            "fulfillment_id": fulfillment_id,
            "location_id": location_id,
        }

    def map_products_to_catalog(self, products: List[ProductDB]) -> Dict[str, Any]:
        """Map a list of Craftsy products to an ONDC catalog object."""
        categories = {}
        for p in products:
            cat = p.category or "General"
            categories[cat] = {
                "id": cat,
                "descriptor": {"name": cat},
            }

        return {
            "bpp/descriptor": self.bpp_descriptor,
            "bpp/categories": list(categories.values()),
            "bpp/items": [self.map_product_to_ondc_item(p) for p in products],
        }

    def map_order_to_ondc_status(self, order: Any) -> str:
        """Map Craftsy order status to ONDC order state."""
        status_map = {
            "new": "Created",
            "confirmed": "Confirmed",
            "packed": "Packed",
            "shipped": "Shipped",
            "delivered": "Delivered",
            "cancelled": "Cancelled",
        }
        return status_map.get(order.status, "Created")

    def build_context(
        self, context_data: Dict[str, Any], action: str
    ) -> Dict[str, Any]:
        """Build an ONDC response context."""
        return {
            "domain": context_data.get("domain", "ONDC:RET10"),
            "action": action,
            "version": context_data.get("version", "2.0.2"),
            "bap_id": context_data.get("bap_id", ""),
            "bap_uri": context_data.get("bap_uri", ""),
            "transaction_id": context_data.get("transaction_id", ""),
            "message_id": context_data.get("message_id", ""),
            "timestamp": context_data.get("timestamp", ""),
            "ttl": context_data.get("ttl", "PT30S"),
            "bpp_id": self.bpp_id,
            "bpp_uri": self.bpp_uri,
        }
