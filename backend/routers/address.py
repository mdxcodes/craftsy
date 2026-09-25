"""
Address Router.

API endpoints for user address management.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models.db_models import ArtisanDB
from ..middleware.auth import get_current_artisan
from ..services.address_service import address_service

router = APIRouter(prefix="/api/v1/addresses", tags=["Addresses"])


class AddressCreateRequest(BaseModel):
    label: str = Field(default="home", description="Address label (home, work, other)")
    name: str = Field(..., description="Recipient full name")
    phone: str = Field(..., description="Contact phone number")
    line1: str = Field(..., description="Street address")
    line2: Optional[str] = Field(default="", description="Apartment, suite, etc.")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State")
    pincode: str = Field(..., description="PIN code")
    is_default: bool = Field(default=False, description="Is this the default address?")


class AddressUpdateRequest(BaseModel):
    label: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    line1: Optional[str] = None
    line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    is_default: Optional[bool] = None


@router.get("")
async def list_addresses(
    db: Session = Depends(get_db),
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    """List all addresses for the current user."""
    return address_service.list_addresses(db, current_artisan.id)


@router.post("", status_code=201)
async def create_address(
    request: AddressCreateRequest,
    db: Session = Depends(get_db),
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    """Create a new address."""
    address = address_service.create_address(
        db,
        user_id=current_artisan.id,
        label=request.label,
        name=request.name,
        phone=request.phone,
        line1=request.line1,
        line2=request.line2 or "",
        city=request.city,
        state=request.state,
        pincode=request.pincode,
        is_default=request.is_default,
    )
    return address


@router.put("/{address_id}")
async def update_address(
    address_id: str,
    request: AddressUpdateRequest,
    db: Session = Depends(get_db),
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    """Update an existing address."""
    updates = {k: v for k, v in request.model_dump().items() if v is not None}
    address = address_service.update_address(db, address_id, current_artisan.id, **updates)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.delete("/{address_id}")
async def delete_address(
    address_id: str,
    db: Session = Depends(get_db),
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    """Delete an address."""
    deleted = address_service.delete_address(db, address_id, current_artisan.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"status": "success", "message": "Address deleted"}
