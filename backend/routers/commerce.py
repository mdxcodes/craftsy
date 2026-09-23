"""Commerce Channel Router.

API endpoints for multi-channel commerce operations:
- Channel status management
- Channel validation
- Publishing (foundation)
- Audit logging
- ONDC-specific operations (foundation)
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.commerce_models import (
    ChannelType,
    GeMChannelStatus,
    ONDCChannelStatus,
    ONDCError,
    ChannelPublishRequest,
    ChannelPublishResponse,
    ChannelStatusResponse,
    ChannelStatusInfo,
)
from ..services.commerce_service import commerce_service
from ..services.ondc_adapter import ondc_adapter
from ..services.gem_adapter import gem_adapter

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


# ONDC-Specific Endpoints (Foundation)


@router.get("/ondc/onboarding-checklist")
async def get_ondc_onboarding_checklist(
    db: Session = Depends(get_db),
):
    """Get ONDC onboarding checklist for Craftsy."""
    try:
        return ondc_adapter.get_ondc_onboarding_checklist(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ondc/validate-state-transition")
async def validate_ondc_state_transition(
    current_status: ONDCChannelStatus,
    new_status: ONDCChannelStatus,
):
    """Validate an ONDC state transition."""
    try:
        is_valid = ondc_adapter.validate_state_transition(current_status, new_status)
        return {"valid": is_valid, "current": current_status, "new": new_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ondc/error/{error_code}")
async def get_ondc_error(
    error_code: str,
    details: Optional[str] = None,
):
    """Get human-readable ONDC error for artisan display."""
    try:
        return ondc_adapter.get_ondc_error(error_code, details)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ondc/sync-catalogue/{product_id}")
async def sync_ondc_catalogue(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Sync product to ONDC catalogue (foundation - no real API call)."""
    try:
        return ondc_adapter.sync_ondc_catalogue(db, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ondc/orders")
async def get_ondc_orders(
    artisan_id: str,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Get orders from ONDC (foundation - no real API call)."""
    try:
        return ondc_adapter.get_ondc_orders(db, artisan_id, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ondc/orders/{order_id}/status")
async def update_ondc_order_status(
    order_id: str,
    new_status: str,
    db: Session = Depends(get_db),
):
    """Update order status on ONDC (foundation - no real API call)."""
    try:
        return ondc_adapter.update_ondc_order_status(db, order_id, new_status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ondc/orders/{order_id}/cancel")
async def cancel_ondc_order(
    order_id: str,
    reason: str,
    db: Session = Depends(get_db),
):
    """Handle ONDC order cancellation (foundation - no real API call)."""
    try:
        return ondc_adapter.handle_ondc_cancellation(db, order_id, reason)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ondc/inventory/{product_id}")
async def sync_ondc_inventory(
    product_id: str,
    stock_quantity: int,
    db: Session = Depends(get_db),
):
    """Sync inventory to ONDC (foundation - no real API call)."""
    try:
        return ondc_adapter.sync_ondc_inventory(db, product_id, stock_quantity)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ondc/orders/{order_id}/reconcile")
async def reconcile_ondc_order(
    order_id: str,
    db: Session = Depends(get_db),
):
    """Reconcile ONDC order state with Craftsy order state (foundation)."""
    try:
        return ondc_adapter.reconcile_ondc_order_state(db, order_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GeM-Specific Endpoints (Foundation)


@router.get("/gem/readiness/{product_id}")
async def get_gem_readiness(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Get GeM seller readiness assessment for a product."""
    try:
        return gem_adapter.get_gem_readiness(db, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gem/seller-checklist")
async def get_gem_seller_checklist(
    db: Session = Depends(get_db),
):
    """Get GeM seller registration checklist."""
    try:
        return gem_adapter.get_gem_seller_checklist(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gem/guided-workflow/{product_id}")
async def get_gem_guided_workflow(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Get guided workflow for GeM selling preparation."""
    try:
        return gem_adapter.get_gem_guided_workflow(db, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gem/validate-state-transition")
async def validate_gem_state_transition(
    current_status: GeMChannelStatus,
    new_status: GeMChannelStatus,
):
    """Validate a GeM state transition."""
    try:
        is_valid = gem_adapter.validate_state_transition(current_status, new_status)
        return {"valid": is_valid, "current": current_status, "new": new_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gem/error/{error_code}")
async def get_gem_error(
    error_code: str,
    details: Optional[str] = None,
):
    """Get human-readable GeM error for artisan display."""
    try:
        return gem_adapter.get_gem_error(error_code, details)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
