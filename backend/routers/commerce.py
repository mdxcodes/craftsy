"""
Commerce Channel Router.

API endpoints for multi-channel commerce operations:
- Channel status management
- Channel validation
- Publishing (foundation)
- Audit logging
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.commerce_models import (
    ChannelType,
    ChannelPublishRequest,
    ChannelPublishResponse,
    ChannelStatusResponse,
    ChannelStatusInfo,
)
from ..services.commerce_service import commerce_service

router = APIRouter(prefix="/api/v1/commerce", tags=["Commerce Channels"])


@router.get("/channels/{product_id}/status", response_model=list[ChannelStatusInfo])
async def get_product_channel_statuses(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Get channel status for all channels for a product."""
    try:
        return commerce_service.get_all_channel_statuses(db, product_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/channels/{product_id}/{channel}", response_model=ChannelStatusInfo)
async def get_channel_status(
    product_id: str,
    channel: str,
    db: Session = Depends(get_db),
):
    """Get status for a specific channel."""
    try:
        channel_type = ChannelType(channel)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid channel: {channel}")

    try:
        return commerce_service.get_channel_status(db, product_id, channel_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/channels/{product_id}/{channel}/requirements")
async def get_channel_requirements(
    product_id: str,
    channel: str,
    db: Session = Depends(get_db),
):
    """Get validation requirements for a specific channel."""
    try:
        channel_type = ChannelType(channel)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid channel: {channel}")

    try:
        return commerce_service.validate_channel_requirements(
            db, product_id, channel_type
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/channels/publish", response_model=ChannelPublishResponse)
async def publish_to_channel(
    request: ChannelPublishRequest,
    db: Session = Depends(get_db),
):
    """Attempt to publish a product to a channel."""
    try:
        return commerce_service.publish_to_channel(
            db,
            request.product_id,
            request.channel,
            request.confirm,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/audit-logs")
async def get_audit_logs(
    product_id: Optional[str] = None,
    channel: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Get channel audit logs."""
    channel_type = None
    if channel:
        try:
            channel_type = ChannelType(channel)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid channel: {channel}")

    try:
        return commerce_service.get_audit_logs(db, product_id, channel_type, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
