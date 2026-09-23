"""
Commerce Channel Models.

Defines the channel abstraction, channel status, and product-channel relationship.
These models extend the existing ProductDB with multi-channel selling support.

Architecture:
    CommerceChannel (abstract)
        ├── CraftsyChannel
        ├── ONDCChannel
        └── GeMChannel

Each product can have independent channel states.
"""

from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..database import Base


# ── Channel Types ────────────────────────────────────────────────────────────


class ChannelType(str, Enum):
    """Supported commerce channels."""
    CRAFTSY = "craftsy"
    ONDC = "ondc"
    GEM = "gem"


# ── Channel Status ───────────────────────────────────────────────────────────


class CraftsyChannelStatus(str, Enum):
    """Craftsy marketplace channel status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT = "draft"


class ONDCChannelStatus(str, Enum):
    """ONDC channel status."""
    NOT_CONNECTED = "not_connected"
    NEEDS_INFORMATION = "needs_information"
    READY = "ready"
    PENDING = "pending"
    PUBLISHED = "published"
    FAILED = "failed"
    DISCONNECTED = "disconnected"


class GeMChannelStatus(str, Enum):
    """GeM (Government e-Marketplace) channel status."""
    NOT_CONNECTED = "not_connected"
    ELIGIBILITY_REQUIRED = "eligibility_required"
    NEEDS_INFORMATION = "needs_information"
    READY = "ready"
    PENDING = "pending"
    PUBLISHED = "published"
    REJECTED = "rejected"
    DISCONNECTED = "disconnected"


# ── Channel Requirements ─────────────────────────────────────────────────────


class ChannelRequirement(BaseModel):
    """A single requirement that must be met before a product can be published to a channel."""
    field: str = Field(..., description="Product field this requirement applies to")
    description: str = Field(..., description="Human-readable description")
    required: bool = Field(default=True)
    satisfied: bool = Field(default=False)
    value: Optional[str] = Field(default=None, description="Current value if satisfied")


class ChannelRequirements(BaseModel):
    """Requirements for a specific channel."""
    channel: ChannelType
    status: str
    requirements: List[ChannelRequirement] = Field(default_factory=list)
    missing_fields: List[str] = Field(default_factory=list)


# ── Channel Publish Request/Response ────────────────────────────────────────


class ChannelPublishRequest(BaseModel):
    """Request to publish a product to a channel."""
    product_id: str
    channel: ChannelType
    confirm: bool = Field(default=False, description="Explicit confirmation for external publication")


class ChannelPublishResponse(BaseModel):
    """Response from a channel publish attempt."""
    product_id: str
    channel: ChannelType
    status: str
    success: bool
    message: str
    external_id: Optional[str] = None
    external_url: Optional[str] = None


class ChannelStatusResponse(BaseModel):
    """Current channel status for a product."""
    product_id: str
    channel: ChannelType
    status: str
    label: str
    icon: str
    color: str
    is_connected: bool
    can_publish: bool
    missing_requirements: List[str] = Field(default_factory=list)
    external_id: Optional[str] = None
    external_url: Optional[str] = None
    last_synced: Optional[datetime] = None


# ── DB Models ────────────────────────────────────────────────────────────────


class ProductChannelDB(Base):
    """
    Product-channel relationship table.

    Each row represents one product's state on one channel.
    """

    __tablename__ = "product_channels"

    id = Column(String(64), primary_key=True, index=True)
    product_id = Column(
        String(64),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    channel = Column(String(32), nullable=False)  # ChannelType value
    status = Column(String(32), nullable=False, default="not_connected")
    external_id = Column(String(255), nullable=True)
    external_url = Column(String(512), nullable=True)
    channel_data = Column(Text, default="{}")  # JSON blob for channel-specific data
    last_synced = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationship (no backref to avoid lazy-load issues in tests)
    product = relationship("ProductDB")


class ChannelAuditLogDB(Base):
    """Audit log for all channel operations.

    Tracks every publish, update, unpublish, and sync attempt.
    """

    __tablename__ = "channel_audit_logs"

    id = Column(String(64), primary_key=True, index=True)
    product_id = Column(String(64), ForeignKey("products.id", ondelete="SET NULL"), nullable=True, index=True)
    channel = Column(String(32), nullable=False)
    action = Column(String(64), nullable=False)  # publish, update, unpublish, sync, status_check
    status_before = Column(String(32), nullable=True)
    status_after = Column(String(32), nullable=True)
    external_id = Column(String(255), nullable=True)
    message = Column(String(1024), nullable=True)
    success = Column(Integer, default=0)  # 0 or 1 (SQLite boolean)
    created_at = Column(DateTime, default=datetime.now)

    # Relationship (no backref to avoid lazy-load issues in tests)
    product = relationship("ProductDB")


# ── Flutter-compatible Schemas ───────────────────────────────────────────────


class ChannelStatusInfo(BaseModel):
    """Simplified channel status for Flutter consumption."""
    model_config = ConfigDict(from_attributes=True)

    channel: str
    status: str
    label: str
    icon: str  # icon key for Flutter mapping
    color: str  # color key for Flutter mapping
    is_connected: bool
    can_publish: bool
    missing_requirements: List[str] = Field(default_factory=list)
    external_id: Optional[str] = None
    external_url: Optional[str] = None
    last_synced: Optional[str] = None  # ISO 8601 for Dart compatibility


class ProductWithChannels(BaseModel):
    """Product response with channel status information."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    price: float
    category: str
    status: str
    image_url: str
    channels: List[ChannelStatusInfo] = Field(default_factory=list)


# ── Validation Constants ─────────────────────────────────────────────────────

# ONDC required fields for catalogue publishing
ONDC_REQUIRED_FIELDS = [
    "title",
    "description",
    "price",
    "image_url",
    "category",
    "weight",
    "dimensions",
    "hsn_code",
    "country_of_origin",
]

# GeM required fields for seller registration and catalogue
GEM_REQUIRED_FIELDS = [
    "title",
    "description",
    "price",
    "image_url",
    "category",
    "seller_gst",
    "seller_pan",
    "seller_aadhaar",
    "business_name",
    "business_address",
    "country_of_origin",
    "make_in_india",
]

# Craftsy required fields (minimal — most are optional for internal marketplace)
CRAFTSY_REQUIRED_FIELDS = [
    "title",
    "description",
    "price",
    "image_url",
    "category",
]
