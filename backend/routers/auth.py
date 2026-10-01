"""
Authentication and User Profile Router for Craftsy.

Integrates with StartMessaging for real OTP delivery and verification.
Craftsy remains responsible for its own users, sessions, and JWTs;
StartMessaging is used only for OTP delivery and verification.
"""

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..config import get_settings
from ..database import get_db
from ..middleware.auth import get_current_artisan
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
    OtpVerifyResult,
    StartMessagingOtpProvider,
)
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, description="Full name")
    craft_type: Optional[str] = Field(default=None, description="Primary craft category")
    location_cluster: Optional[str] = Field(default=None, description="Artisan cluster / town location")
    state: Optional[str] = Field(default=None, description="State / Region")
    experience_years: Optional[str] = Field(default=None, description="Craft experience in years")
    pehchan_id: Optional[str] = Field(default=None, description="Pehchan card / Artisan ID")
    preferred_language: Optional[str] = Field(default=None, description="Preferred app language")


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


from ..middleware.auth import create_access_token


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
    description="Sends a real OTP to the phone number via StartMessaging. "
                "Creates a new user if the phone number is not registered.",
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
    is_new_user = artisan is None

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
        "is_new_user": is_new_user,
    }


@router.post(
    "/verify-otp",
    response_model=AuthResponse,
    summary="Verify phone OTP",
    description="Verifies OTP with StartMessaging and returns artisan session profile. "
                "Creates a new user if the phone number is not registered.",
)
async def verify_otp(
    request: OtpVerifyRequest,
    db: Session = Depends(get_db),
):
    phone_clean = _normalize_phone(request.phone)
    masked_phone = phone_clean[:6] + "****" + phone_clean[-4:] if len(phone_clean) >= 10 else "****"
    logger.info(
        "verify_otp request received: masked_phone=%s request_id_present=%s otp_length=%s",
        masked_phone,
        bool(request.request_id and str(request.request_id).strip()),
        len(request.otp or ""),
    )

    if len(phone_clean) != 10:
        logger.warning("verify_otp rejecting invalid phone length: %s", len(phone_clean))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. Must be exactly 10 digits.",
        )

    if not request.request_id or not str(request.request_id).strip():
        logger.warning("verify_otp rejecting missing request_id")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP request ID.",
        )

    if not request.otp or not request.otp.isdigit() or len(request.otp) != 6:
        logger.warning("verify_otp rejecting invalid OTP format")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP format. Must be 6 digits.",
        )

    artisan = db.query(ArtisanDB).filter(ArtisanDB.phone == phone_clean).first()
    is_new_user = artisan is None
    logger.info(
        "verify_otp user lookup: masked_phone=%s is_new_user=%s artisan_id=%s",
        masked_phone,
        is_new_user,
        artisan.id if artisan else None,
    )

    if is_new_user:
        artisan = ArtisanDB(
            id=f"artisan_{phone_clean}",
            name=None,
            phone=phone_clean,
            preferred_language="en",
            role="customer",
            created_at=datetime.now(),
        )
        db.add(artisan)
        db.commit()
        db.refresh(artisan)
        logger.info("verify_otp created new user: artisan_id=%s", artisan.id)

    settings = get_settings()
    otp_mode = (settings.otp_verification_mode or "provider").strip().lower()
    logger.info("verify_otp otp_mode=%s", otp_mode)

    if otp_mode == "demo":
        logger.info("verify_otp demo mode: accepting OTP without provider verification")
        verify_result = OtpVerifyResult(success=True)
    else:
        provider = _get_otp_provider()
        logger.info(
            "verify_otp provider configured=%s",
            provider.is_configured(),
        )
        if not provider.is_configured():
            logger.warning("verify_otp rejecting: provider not configured")
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="OTP service is not configured on the server.",
            )

        try:
            verify_result = provider.verify_otp(
                request_id=str(request.request_id).strip(),
                otp=request.otp,
            )
        except Exception as exc:
            logger.error("verify_otp provider raised unexpected exception: %s", exc)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={
                    "error_code": "OTP_PROVIDER_UNAVAILABLE",
                    "message": "OTP verification service failed.",
                },
            )

        logger.info(
            "verify_otp provider result: success=%s error_code=%s message=%s",
            verify_result.success,
            verify_result.error_code,
            verify_result.message,
        )

        if not verify_result.success:
            status_code = status.HTTP_400_BAD_REQUEST
            if verify_result.error_code == "OTP_PROVIDER_UNAVAILABLE":
                status_code = status.HTTP_502_BAD_GATEWAY
            detail = {
                "error_code": verify_result.error_code,
                "message": verify_result.message,
            }
            logger.warning("verify_otp rejecting failed verification: %s", detail)
            raise HTTPException(status_code=status_code, detail=detail)

    logger.info("verify_otp success: artisan_id=%s", artisan.id)
    return AuthResponse(
        status="success",
        access_token=create_access_token(artisan.phone),
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


@router.patch(
    "/profile",
    response_model=ArtisanProfileResponse,
    summary="Update current user profile",
    description="Update the authenticated user's own profile fields.",
)
async def update_own_profile(
    request: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_artisan: ArtisanDB = Depends(get_current_artisan),
):
    update_data = request.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update.",
        )

    for field, value in update_data.items():
        if hasattr(current_artisan, field):
            setattr(current_artisan, field, value)

    db.commit()
    db.refresh(current_artisan)
    return current_artisan
