"""Pydantic schemas for GeM integration."""

from __future__ import annotations

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class GeMRegistrationOptions(BaseModel):
    has_gem_account: Optional[bool] = None
    has_udyam: Optional[bool] = None
    seller_type: Optional[str] = None
    paths: List[Dict[str, Any]] = Field(default_factory=list)


class GeMRegistrationGuidance(BaseModel):
    path: str
    title: str
    description: str
    steps: List[Dict[str, Any]]
    official_links: Dict[str, str]
    warning: Optional[str] = None


class GeMReadinessResponse(BaseModel):
    ready: bool
    missing_fields: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    available_fields: List[str] = Field(default_factory=list)
    category: Optional[str] = None
    readiness_status: str
    next_actions: List[str] = Field(default_factory=list)


class GeMListingDraft(BaseModel):
    product_name: str
    short_description: str
    description: str
    price: float
    category: str
    specifications: Dict[str, Any] = Field(default_factory=dict)
    certifications: List[str] = Field(default_factory=list)
    warranty: Optional[str] = None
    images: List[str] = Field(default_factory=list)
    artisan_information: Dict[str, Any] = Field(default_factory=dict)
    missing_information: List[str] = Field(default_factory=list)
    provenance: List[Dict[str, Any]] = Field(default_factory=list)


class GeMListingKit(BaseModel):
    draft: GeMListingDraft
    copyable_text: str
    structured_data: Dict[str, Any]
    generated_at: str
    disclaimer: str = (
        "This is a GeM Listing Draft prepared by Craftsy for artisan review. "
        "It is NOT an official GeM catalogue submission. Final listing must be created by the seller on the official GeM portal."
    )


class GeMOpenResponse(BaseModel):
    opened: bool
    url: str
    message: str
