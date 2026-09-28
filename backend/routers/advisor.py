"""
Business Advisor Router.

Provides AI-driven per-product business advice for artisan catalogs.
"""

import logging
from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ..services.advisor_service import AdvisorService
from ..models.schemas import ProductAdviceResponse, AdvisorAnalyzeResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/advisor", tags=["Business Advisor"])


class ProductSummary(BaseModel):
    id: str = Field(..., description="Product ID")
    title: str = Field(..., description="Product title")
    description: str = Field(default="", description="Product description")
    category: str = Field(default="Handicrafts", description="Product category")
    price: float = Field(..., description="Current price in INR")
    stock: int = Field(default=0, description="Current stock quantity")
    status: str = Field(default="draft", description="Product status")
    createdAt: str = Field(default="", description="ISO-8601 creation timestamp")
    title_en: str = Field(default="", description="English title")
    description_en: str = Field(default="", description="English description")


class AdvisorAnalyzeRequest(BaseModel):
    products: List[ProductSummary] = Field(..., description="Catalog products to analyze")


@router.post("/analyze", response_model=AdvisorAnalyzeResponse)
async def analyze_catalog(request: AdvisorAnalyzeRequest):
    """
    Analyze artisan catalog and return per-product business advice.

    Returns one advice item per product that needs attention, tagged by:
    - price_review
    - low_stock
    - slow_moving
    - festival_opportunity
    """
    try:
        service = AdvisorService()
        products = [p.model_dump() for p in request.products]
        advice = service.analyze_catalog(products)
        response_advice = [
            ProductAdviceResponse(
                product_id=a.product_id,
                product_title=a.product_title,
                advice_type=a.advice_type,
                priority=a.priority,
                title=a.title,
                description=a.description,
                suggested_action=a.suggested_action,
                suggested_price=a.suggested_price,
                suggested_stock=a.suggested_stock,
                current_price=a.current_price,
                current_stock=a.current_stock,
                category=a.category,
            )
            for a in advice
        ]
        return AdvisorAnalyzeResponse(
            advice=response_advice,
            total_products=len(request.products),
            products_needing_attention=len(advice),
        )
    except Exception as e:
        logger.error("Advisor analysis failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Advisor analysis failed: {str(e)}")
