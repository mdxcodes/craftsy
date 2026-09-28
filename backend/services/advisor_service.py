"""
Advisor Service.

Generates per-product business advice using the existing pricing engine,
catalog metadata, and Gemini LLM for natural-language recommendations.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from ..config import get_settings

logger = logging.getLogger(__name__)


@dataclass
class ProductAdvice:
    product_id: str
    product_title: str
    advice_type: str  # price_review | low_stock | slow_moving | festival_opportunity | ok
    priority: str  # high | medium | low
    title: str
    description: str
    suggested_action: str
    suggested_price: Optional[float] = None
    suggested_stock: Optional[int] = None
    current_price: Optional[float] = None
    current_stock: Optional[int] = None
    category: Optional[str] = None


class AdvisorService:
    """Generates actionable business advice for artisan product catalogs."""

    def __init__(self):
        self.settings = get_settings()
        self._pricing_service = None

    @property
    def pricing_service(self):
        if self._pricing_service is None:
            from .pricing_service import PricingService
            self._pricing_service = PricingService()
        return self._pricing_service

    def analyze_catalog(self, products: List[dict]) -> List[ProductAdvice]:
        """Return one advice item per product that needs attention."""
        if not products:
            return []

        advice_list: List[ProductAdvice] = []
        now = datetime.utcnow()

        category_prices: dict[str, List[float]] = {}
        for product in products:
            category = (product.get("category") or "Handicrafts").strip()
            if not category:
                category = "Handicrafts"
            category_prices.setdefault(category, []).append(float(product.get("price") or 0))

        category_avg: dict[str, float] = {}
        for category, prices in category_prices.items():
            valid = [p for p in prices if p > 0]
            category_avg[category] = sum(valid) / len(valid) if valid else 0.0

        for product in products:
            product_id = str(product.get("id") or product.get("product_id") or "")
            title = str(product.get("title") or product.get("title_en") or "Untitled Product")
            description = str(product.get("description") or product.get("description_en") or "")
            category = str(product.get("category") or "Handicrafts")
            price = float(product.get("price") or 0)
            stock = int(product.get("stock") or 0)
            status = str(product.get("status") or "draft")
            created_at = product.get("createdAt") or product.get("created_at")
            product_dt = (
                datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                if isinstance(created_at, str)
                else (created_at or now)
            )
            age_days = max((now - product_dt).days, 0)

            candidate_advices: List[ProductAdvice] = []

            # Low stock
            if stock > 0 and stock < 5:
                suggested_stock = max(stock * 3, 10)
                candidate_advices.append(
                    ProductAdvice(
                        product_id=product_id,
                        product_title=title,
                        advice_type="low_stock",
                        priority="high" if stock == 1 else "medium",
                        title="Low Stock Alert",
                        description=(
                            f"{title}\n"
                            f"Current Stock: {stock}\n"
                            f"Demand is expected to increase during the upcoming season.\n"
                            f"Suggested Stock: {suggested_stock}"
                        ),
                        suggested_action="update_stock",
                        suggested_stock=suggested_stock,
                        current_stock=stock,
                        category=category,
                    )
                )

            # Price review
            avg_price = category_avg.get(category, 0)
            if avg_price > 0 and price > 0 and price < avg_price * 0.7:
                suggested_price = round(avg_price * 1.1, 0)
                candidate_advices.append(
                    ProductAdvice(
                        product_id=product_id,
                        product_title=title,
                        advice_type="price_review",
                        priority="high",
                        title="Price Review Needed",
                        description=(
                            f"{title}\n"
                            f"Current Price: ₹{price:.0f}\n"
                            f"Suggested Price: ₹{suggested_price:.0f}\n"
                            f"Reason: Similar products in {category} are priced higher."
                        ),
                        suggested_action="update_price",
                        suggested_price=suggested_price,
                        current_price=price,
                        category=category,
                    )
                )

            # Slow moving
            if status in {"draft", "listing_removed"} and age_days > 30:
                candidate_advices.append(
                    ProductAdvice(
                        product_id=product_id,
                        product_title=title,
                        advice_type="slow_moving",
                        priority="medium",
                        title="Slow Moving Product",
                        description=(
                            f"{title}\n"
                            f"This product has been in your catalog for {age_days} days.\n"
                            f"AI suggests refreshing the photos or adjusting the price."
                        ),
                        suggested_action="refresh_listing",
                        current_price=price,
                        category=category,
                    )
                )

            # Festival opportunity
            current_month = now.month
            is_festival_season = current_month in {9, 10, 11, 12, 1, 2}
            if is_festival_season and status == "live":
                candidate_advices.append(
                    ProductAdvice(
                        product_id=product_id,
                        product_title=title,
                        advice_type="festival_opportunity",
                        priority="low",
                        title="Festival Demand Opportunity",
                        description=(
                            f"{title}\n"
                            f"This product may have higher demand during the upcoming festival season.\n"
                            f"Consider highlighting it in your storefront."
                        ),
                        suggested_action="boost_listing",
                        current_price=price,
                        category=category,
                    )
                )

            if candidate_advices:
                best = sorted(candidate_advices, key=lambda a: ["high", "medium", "low"].index(a.priority))[0]
                advice_list.append(best)

        return advice_list
