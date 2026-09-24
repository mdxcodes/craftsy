"""
Unified Commerce Hub Router.

API endpoints for the unified commerce experience:
- Commerce summary dashboard
- Product channel management
- Unified inventory
- Unified orders with channel filtering
- Cross-channel sync status
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.commerce_models import ChannelType
from ..services.commerce_hub_service import commerce_hub_service

router = APIRouter(prefix="/api/v1/commerce-hub", tags=["Unified Commerce Hub"])


@router.get("/summary/{artisan_id}")
async def get_commerce_summary(
    artisan_id: str,
    db: Session = Depends(get_db),
):
    """Get unified commerce summary for artisan dashboard."""
    try:
        return commerce_hub_service.get_commerce_summary(db, artisan_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/{product_id}/channels")
async def get_product_channels(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Get channel statuses for a product."""
    try:
        return commerce_hub_service.get_product_channels(db, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/{product_id}/detail")
async def get_product_detail_with_channels(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Get product detail with channel information."""
    try:
        return commerce_hub_service.get_product_detail_with_channels(db, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/{product_id}/inventory")
async def get_product_inventory(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Get unified inventory for a product."""
    try:
        return commerce_hub_service.get_inventory(db, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/{product_id}/sync-status")
async def get_product_sync_status(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Get cross-channel sync status for a product."""
    try:
        return commerce_hub_service.get_sync_status(db, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orders/{artisan_id}")
async def get_unified_orders(
    artisan_id: str,
    channel: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Get all orders for an artisan across all channels."""
    try:
        return commerce_hub_service.get_unified_orders(
            db, artisan_id, channel, status, limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orders/{artisan_id}/channel-summary")
async def get_order_channel_summary(
    artisan_id: str,
    db: Session = Depends(get_db),
):
    """Get order summary grouped by channel."""
    try:
        return commerce_hub_service.get_order_channel_summary(db, artisan_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/products/{product_id}/channels/{channel}/enable")
async def enable_channel(
    product_id: str,
    channel: str,
    db: Session = Depends(get_db),
):
    """Enable a channel for a product."""
    try:
        channel_type = ChannelType(channel)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid channel: {channel}")

    try:
        return commerce_hub_service.enable_channel(db, product_id, channel_type)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/products/{product_id}/channels/{channel}/disable")
async def disable_channel(
    product_id: str,
    channel: str,
    db: Session = Depends(get_db),
):
    """Disable a channel for a product."""
    try:
        channel_type = ChannelType(channel)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid channel: {channel}")

    try:
        return commerce_hub_service.disable_channel(db, product_id, channel_type)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
