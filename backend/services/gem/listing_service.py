"""
GeM Listing Service.

Generates a GeM Listing Draft from verified Craftsy product data only.
AI may improve wording and organize information, but MUST NOT invent
specifications, certifications, warranty, dimensions, material, etc.

Uses the existing Groq/Gemini infrastructure.
"""

from __future__ import annotations

import json
import logging
from typing import Optional, Dict, Any, List

from sqlalchemy.orm import Session

from ...models.db_models import ProductDB
from .prompts import GEM_LISTING_SYSTEM_PROMPT
from ...config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


class GeMListingService:
    """Generate GeM listing drafts from verified product data."""

    async def generate_listing(self, product_id: str, db: Session) -> Dict[str, Any]:
        product = self._get_product(db, product_id)
        product_data = self._product_to_dict(product)

        prompt = self._build_prompt(product_data)
        listing = await self._call_llm(prompt, product_data)

        if listing is None:
            listing = self._deterministic_listing(product_data)

        listing = self._sanitize_listing(listing, product_data)
        return listing

    async def _call_llm(self, prompt: str, product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        from ...services.groq_client import GroqClient
        from google import genai

        # Try Groq first
        if settings.groq_api_key:
            try:
                groq = GroqClient()
                if groq.is_available():
                    raw = await groq.chat_json(
                        [
                            {"role": "system", "content": GEM_LISTING_SYSTEM_PROMPT},
                            {"role": "user", "content": prompt},
                        ],
                        max_tokens=1024,
                    )
                    return self._parse_llm_response(raw, product_data)
            except Exception as exc:
                logger.warning("[GeMListingService] Groq failed: %s", exc)

        # Fallback to Gemini
        if settings.gemini_api_key:
            try:
                client = genai.Client(api_key=settings.gemini_api_key)
                response = client.models.generate_content(
                    model=settings.llm_model,
                    contents=[
                        {"role": "user", "parts": [{"text": prompt}]},
                    ],
                    config=genai.types.GenerateContentConfig(
                        system_instruction=GEM_LISTING_SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        temperature=0.2,
                    ),
                )
                raw = json.loads(response.text)
                return self._parse_llm_response(raw, product_data)
            except Exception as exc:
                logger.warning("[GeMListingService] Gemini failed: %s", exc)

        return None

    def _get_product(self, db: Session, product_id: str) -> ProductDB:
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")
        return product

    def _product_to_dict(self, product: ProductDB) -> Dict[str, Any]:
        artisan_info: Dict[str, Any] = {}
        if product.artisan:
            artisan_info = {
                "name": product.artisan.name,
                "craft_type": product.artisan.craft_type,
                "location_cluster": product.artisan.location_cluster,
                "state": product.artisan.state,
                "experience_years": product.artisan.experience_years,
            }

        images: List[str] = []
        if product.image_url:
            images.append(product.image_url)
        if product.cloudinary_public_id:
            artisan_info["cloudinary_public_id"] = product.cloudinary_public_id

        return {
            "product_name": product.title,
            "description": product.description,
            "price": product.price,
            "category": product.category,
            "image_url": product.image_url,
            "cloudinary_public_id": product.cloudinary_public_id,
            "tags": product.tags_list,
            "title_hi": product.title_hi,
            "description_hi": product.description_hi,
            "artisan_information": artisan_info,
            # Fields NOT in ProductDB — must not be invented
            "material": None,
            "dimensions": None,
            "weight": None,
            "origin": None,
            "warranty": None,
            "certifications": [],
            "manufacturer": None,
            "business_name": None,
            "business_address": None,
            "seller_gst": None,
            "seller_pan": None,
        }

    def _build_prompt(self, product_data: Dict[str, Any]) -> str:
        return f"""
Generate a GeM Listing Draft for the following verified product data.

VERIFIED PRODUCT DATA (do not invent beyond this):
{json.dumps(product_data, indent=2)}

INSTRUCTIONS:
- product_name: use the exact product title
- short_description: 1-2 sentences
- description: professional detailed description
- price: {product_data['price']}
- category: {product_data['category']}
- specifications: include only known values from the data
- certifications: empty list unless provided in data
- warranty: null unless provided in data
- images: use the image_url if present
- artisan_information: empty dict unless provided in data
- missing_information: list any fields that are null/empty in the source data
"""

    def _parse_llm_response(self, raw: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(raw, dict):
            return {}
        return {
            "product_name": raw.get("product_name", source.get("product_name", "")),
            "short_description": raw.get("short_description", ""),
            "description": raw.get("description", source.get("description", "")),
            "price": float(raw.get("price", source.get("price", 0))),
            "category": raw.get("category", source.get("category", "")),
            "specifications": raw.get("specifications", {}),
            "certifications": raw.get("certifications", []),
            "warranty": raw.get("warranty"),
            "images": raw.get("images", []),
            "artisan_information": raw.get("artisan_information", {}),
            "missing_information": raw.get("missing_information", []),
        }

    def _deterministic_listing(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback listing when LLM is unavailable."""
        missing = []
        if not product_data.get("description"):
            missing.append("description")
        if not product_data.get("price"):
            missing.append("price")
        if not product_data.get("image_url"):
            missing.append("image")

        return {
            "product_name": product_data.get("product_name", ""),
            "short_description": product_data.get("description", "")[:120] if product_data.get("description") else "Information not provided",
            "description": product_data.get("description", "") or "Information not provided",
            "price": product_data.get("price", 0.0),
            "category": product_data.get("category", ""),
            "specifications": {},
            "certifications": [],
            "warranty": None,
            "images": [product_data["image_url"]] if product_data.get("image_url") else [],
            "artisan_information": {},
            "missing_information": missing,
        }

    def _sanitize_listing(self, listing: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
        """Remove any fields that were not in the source data."""
        sanitized = dict(listing)

        # If source has no material, ensure specs don't include it
        if not source.get("material"):
            if "material" in sanitized.get("specifications", {}):
                del sanitized["specifications"]["material"]

        # Ensure missing_information includes fields that are null in source
        missing = list(sanitized.get("missing_information", []))
        for field in ["material", "dimensions", "weight", "origin", "warranty", "certifications"]:
            if not source.get(field) and field not in missing:
                missing.append(field)
        sanitized["missing_information"] = missing

        return sanitized


gem_listing_service = GeMListingService()
