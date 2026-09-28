"""
Authentication and User Profile Router for Craftsy.

Integrates with StartMessaging for real OTP delivery and verification.
Craftsy remains responsible for its own users, sessions, and JWTs;
StartMessaging is used only for OTP delivery and verification.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..config import get_settings
from ..database import get_db
from ..models.db_models import ArtisanDB
from ..models.schemas import (
    ArtisanRegisterRequest,
    ArtisanLoginRequest,
    OtpVerifyRequest,
    ArtisanProfileResponse,
)
from ..services.startmessaging_service import (
    OtpProviderConfigError,
    OtpProviderError,
    StartMessagingOtpProvider,
)
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class CustomerRegisterRequest(BaseModel):
    name: str = Field(..., description="Full name")
    phone: str = Field(..., description="10-digit mobile number")
    preferred_language: Optional[str] = Field(default="en", description="Preferred app language")


class ResendOtpRequest(BaseModel):
    phone: str = Field(..., description="10-digit mobile number")


class AuthResponse(BaseModel):
    status: str
    access_token: str
    token_type: str = "bearer"
    artisan: ArtisanProfileResponse


router = APIRouter(prefix="/api/v1/auth", tags=["Authentication & Artisans"])


def _normalize_phone(phone: str) -> str:
    """Normalize phone to a consistent 10-digit string."""
    digits = "".join(ch for ch in (phone or "") if ch.isdigit())
    if len(digits) >= 10:
        return digits[-10:]
    return digits


def _get_otp_provider() -> StartMessagingOtpProvider:
    return StartMessagingOtpProvider()


def _issue_token_for_artisan(artisan: ArtisanDB) -> str:
    """Return the existing mock token for the artisan."""
    return f"mock_jwt_token_{artisan.phone}"


@router.post(
    "/register",
    response_model=ArtisanProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new artisan",
    description="Registers a new artisan profile with craft details and initiates phone verification.",
)
async def register_artisan(
    request: ArtisanRegisterRequest,
    db: Session = Depends(get_db),
):
    phone_clean = _normalize_phone(request.phone)
    if len(phone_clean) != 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. Must be exactly 10 digits.",
        )

    existing = db.query(ArtisanDB).filter(ArtisanDB.phone == phone_clean).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An artisan with this phone number is already registered.",
        )

    artisan = ArtisanDB(
        id=f"artisan_{_normalize_phone(request.phone)}",
        name=request.name,
        phone=phone_clean,
        craft_type=request.craft_type,
        location_cluster=request.location_cluster,
        state=request.state or "",
        experience_years=request.experience_years or "",
        pehchan_id=request.pehchan_id,
        preferred_language=request.preferred_language or "en",
    )
    db.add(artisan)
    db.commit()
    db.refresh(artisan)

    return artisan


@router.post(
    "/register-consumer",
    response_model=ArtisanProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new consumer/buyer",
    description="Registers a new consumer account with role='customer'.",
)
async def register_consumer(
    request: CustomerRegisterRequest,
    db: Session = Depends(get_db),
):
    phone_clean = _normalize_phone(request.phone)
    if len(phone_clean) != 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. Must be exactly 10 digits.",
        )

    existing = db.query(ArtisanDB).filter(ArtisanDB.phone == phone_clean).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this phone number is already registered.",
        )

    artisan = ArtisanDB(
        id=f"customer_{phone_clean}",
        name=request.name,
        phone=phone_clean,
        preferred_language=request.preferred_language or "en",
        role="customer",
    )
    db.add(artisan)
    db.commit()
    db.refresh(artisan)

    return artisan


@router.post(
    "/login",
    summary="Request login OTP",
    description="Sends a real OTP to the registered phone number via StartMessaging.",
)
async def login_artisan(
    request: ArtisanLoginRequest,
    db: Session = Depends(get_db),
):
    phone_clean = _normalize_phone(request.phone)
    if len(phone_clean) != 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. Must be exactly 10 digits.",
        )

    artisan = db.query(ArtisanDB).filter(ArtisanDB.phone == phone_clean).first()
    if not artisan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No artisan registered with this phone number.",
        )

    provider = _get_otp_provider()
    if not provider.is_configured():
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="OTP service is not configured on the server.",
        )

    send_result = provider.send_otp(f"+91{phone_clean}")
    if not send_result.success:
        status_code = status.HTTP_502_BAD_GATEWAY
        if send_result.error_code in {"MISSING_CONFIG", "AUTHENTICATION_FAILED"}:
            status_code = status.HTTP_501_NOT_IMPLEMENTED
        raise HTTPException(
            status_code=status_code,
            detail={
                "error_code": send_result.error_code,
                "message": send_result.message,
            },
        )

    return {
        "status": "success",
        "message": "OTP sent successfully.",
        "phone": phone_clean,
        "request_id": send_result.request_id,
        "otp_sent": True,
    }


@router.post(
    "/verify-otp",
    response_model=AuthResponse,
    summary="Verify phone OTP",
    description="Verifies OTP with StartMessaging and returns artisan session profile.",
)
async def verify_otp(
    request: OtpVerifyRequest,
    db: Session = Depends(get_db),
):
    phone_clean = _normalize_phone(request.phone)
    if len(phone_clean) != 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. Must be exactly 10 digits.",
        )

    if not request.request_id or not str(request.request_id).strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP request ID.",
        )

    if not request.otp or not request.otp.isdigit() or len(request.otp) != 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP format. Must be 6 digits.",
        )

    artisan = db.query(ArtisanDB).filter(ArtisanDB.phone == phone_clean).first()
    if not artisan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No artisan registered with this phone number. Please register first.",
        )

    provider = _get_otp_provider()
    if not provider.is_configured():
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="OTP service is not configured on the server.",
        )

    verify_result = provider.verify_otp(
        request_id=str(request.request_id).strip(),
        otp=request.otp,
    )
    if not verify_result.success:
        status_code = status.HTTP_400_BAD_REQUEST
        if verify_result.error_code == "OTP_PROVIDER_UNAVAILABLE":
            status_code = status.HTTP_502_BAD_GATEWAY
        detail = {
            "error_code": verify_result.error_code,
            "message": verify_result.message,
        }
        raise HTTPException(status_code=status_code, detail=detail)

    return AuthResponse(
        status="success",
        access_token=_issue_token_for_artisan(artisan),
        artisan=ArtisanProfileResponse.model_validate(artisan),
    )


@router.post(
    "/resend-otp",
    summary="Resend OTP",
    description="Resends the current OTP to the registered phone number via StartMessaging.",
)
async def resend_otp(
    request: ResendOtpRequest,
):
    phone_clean = _normalize_phone(request.phone)
    if len(phone_clean) != 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. Must be exactly 10 digits.",
        )

    provider = _get_otp_provider()
    if not provider.is_configured():
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="OTP service is not configured on the server.",
        )

    send_result = provider.resend_otp(f"+91{phone_clean}")
    if not send_result.success:
        status_code = status.HTTP_502_BAD_GATEWAY
        if send_result.error_code in {"MISSING_CONFIG", "AUTHENTICATION_FAILED"}:
            status_code = status.HTTP_501_NOT_IMPLEMENTED
        raise HTTPException(
            status_code=status_code,
            detail={
                "error_code": send_result.error_code,
                "message": send_result.message,
            },
        )

    return {
        "status": "success",
        "message": "OTP resent successfully.",
        "phone": phone_clean,
        "request_id": send_result.request_id,
    }


@router.get(
    "/profile/{artisan_id}",
    response_model=ArtisanProfileResponse,
    summary="Get artisan profile",
    description="Fetch an artisan profile by their unique ID.",
)
async def get_artisan_profile(
    artisan_id: str,
    db: Session = Depends(get_db),
):
    artisan = db.query(ArtisanDB).filter(ArtisanDB.id == artisan_id).first()
    if not artisan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artisan not found.",
        )
    return artisan
