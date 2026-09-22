"""
Pricing Models.

Defines the structured output from the ML pricing pipeline.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ComparableProduct:
    """A comparable product found in the market."""
    id: str
    title: str
    selling_price: float
    category: str
    source_platform: str
    similarity_score: float
    product_url: str


@dataclass
class PricingResult:
    """Result from the ML pricing pipeline."""
    suggested_price: float
    price_range_low: float
    price_range_high: float
    cost_floor: float
    confidence_score: float = 0.85
    market_position: str = "competitive"
    reasoning: str = ""
    comparable_products: List[ComparableProduct] = field(default_factory=list)
