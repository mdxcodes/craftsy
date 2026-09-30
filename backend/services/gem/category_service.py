"""
GeM Category Service.

Provides Craftsy's preparation layer for GeM category mapping.
Architecture is ready to replace local rules with official GeM category/API data later.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Craftsy preparation schema — can be extended.
# These are NOT official GeM taxonomy mappings unless sourced from official docs.
CRAFTSY_GEM_CATEGORY_SCHEMA: Dict[str, Dict[str, Any]] = {
    "Handicrafts": {
        "gem_category_hint": "Handicrafts",
        "required_fields": ["title", "description", "price", "image_url", "category"],
        "optional_fields": ["material", "dimensions", "weight", "origin"],
        "certification_fields": ["handicraft_certificate", "geographical_indication"],
    },
    "Handloom Products": {
        "gem_category_hint": "Handloom Products",
        "required_fields": ["title", "description", "price", "image_url", "category"],
        "optional_fields": ["fabric_type", "dimensions", "weight", "origin"],
        "certification_fields": ["handloom_mark", "silkmark"],
    },
    "Pottery and Ceramics": {
        "gem_category_hint": "Pottery and Ceramics",
        "required_fields": ["title", "description", "price", "image_url", "category"],
        "optional_fields": ["material", "dimensions", "weight", "origin"],
        "certification_fields": ["pottery_certificate"],
    },
    "Textiles and Fabrics": {
        "gem_category_hint": "Textiles and Fabrics",
        "required_fields": ["title", "description", "price", "image_url", "category"],
        "optional_fields": ["fabric_type", "dimensions", "weight", "origin"],
        "certification_fields": ["textile_certificate", "silkmark", "cotton_certificate"],
    },
    "Jewellery and Ornaments": {
        "gem_category_hint": "Jewellery and Ornaments",
        "required_fields": ["title", "description", "price", "image_url", "category"],
        "optional_fields": ["material", "dimensions", "weight", "origin", "hallmark"],
        "certification_fields": ["hallmark_certificate", "bis_certification"],
    },
    "Wood and Wood Products": {
        "gem_category_hint": "Wood and Wood Products",
        "required_fields": ["title", "description", "price", "image_url", "category"],
        "optional_fields": ["wood_type", "dimensions", "weight", "origin"],
        "certification_fields": ["wood_certificate", "fsc_certificate"],
    },
    "Metal Crafts": {
        "gem_category_hint": "Metal Crafts",
        "required_fields": ["title", "description", "price", "image_url", "category"],
        "optional_fields": ["metal_type", "dimensions", "weight", "origin"],
        "certification_fields": ["metal_certificate"],
    },
    "Paintings and Artwork": {
        "gem_category_hint": "Paintings and Artwork",
        "required_fields": ["title", "description", "price", "image_url", "category"],
        "optional_fields": ["medium", "dimensions", "weight", "origin"],
        "certification_fields": ["artist_certificate"],
    },
    "Bamboo and Cane Products": {
        "gem_category_hint": "Bamboo and Cane Products",
        "required_fields": ["title", "description", "price", "image_url", "category"],
        "optional_fields": ["material", "dimensions", "weight", "origin"],
        "certification_fields": ["bamboo_certificate"],
    },
}


class GeMCategoryService:
    """Craftsy preparation layer for GeM categories."""

    def get_schema(self, category: str) -> Dict[str, Any]:
        key = category.strip()
        if key in CRAFTSY_GEM_CATEGORY_SCHEMA:
            return CRAFTSY_GEM_CATEGORY_SCHEMA[key]
        return {
            "gem_category_hint": key,
            "required_fields": ["title", "description", "price", "image_url", "category"],
            "optional_fields": ["dimensions", "weight", "origin"],
            "certification_fields": [],
            "note": "Generic fallback — replace with official GeM category schema when available.",
        }

    def list_categories(self) -> List[str]:
        return list(CRAFTSY_GEM_CATEGORY_SCHEMA.keys())

    def map_category(self, craftsy_category: str) -> Optional[str]:
        schema = self.get_schema(craftsy_category)
        return schema.get("gem_category_hint")


gem_category_service = GeMCategoryService()
