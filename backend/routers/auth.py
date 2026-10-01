"""
Authentication and User Profile Router for Craftsy.

DEMO OTP MODE:
  - /login sends a real SMS via StartMessaging and creates an OTP transaction.
  - /verify-otp accepts any valid 6-digit OTP during an active transaction.
  - StartMessaging VERIFY is NOT called in demo mode.
  - This is NOT production-secure authentication.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..config import get_settings
from ..database import get_db
from ..middleware.auth import create_access_token, get_current_artisan
from ..models.db_models import ArtisanDB, OtpTransactionDB
from ..models.schemas import (
    ArtisanRegisterRequest,
    ArtisanLoginRequest,
    OtpVerifyRequest,
    ArtisanProfileResponse,
)
from ..services.startmessaging_service import (
    OtpProviderConfigError,
    OtpProviderError,
    OtpSendResult,
    StartMessagingOtpProvider,
)
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication & Artisans"])
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


def _normalize_phone(phone: str) -> str:
    """Normalize an Indian phone number to 10-digit string.

    Accepts:
      9876543210
      +919876543210
      919876543210

    Raises ValueError on invalid numbers.
    """
    digits = "".join(ch for ch in (phone or "") if ch.isdigit())
    if not digits:
        raise ValueError("Phone number is empty")

    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]

    if len(digits) != 10:
        raise ValueError(
            f"Invalid Indian phone number: expected 10 digits, got {len(digits)}"
        )

    if digits[0] not in "6789":
        raise ValueError(
            f"Invalid Indian phone number: must start with 6/7/8/9, got {digits[0]}"
        )

    return digits


def _safe_normalize_phone(phone: str) -> tuple[str, Optional[HTTPException]]:
    """Normalize phone and return (phone, error)."""
    try:
        return _normalize_phone(phone), None
    except ValueError as exc:
        return "", HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


def _mask_phone(phone: str) -> str:
    if len(phone) >= 10:
        return phone[:6] + "****" + phone[-4:]
    return "****"


def _get_otp_provider() -> StartMessagingOtpProvider:
    return StartMessagingOtpProvider()


def _create_otp_transaction(db: Session, phone_clean: str, request_id: str) -> OtpTransactionDB:
    settings = get_settings()
    expire_seconds = getattr(settings, "otp_transaction_expire_seconds", 300)
    now = datetime.now(timezone.utc)
    transaction = OtpTransactionDB(
        id=f"otp_txn_{phone_clean}_{int(now.timestamp())}",
        phone=phone_clean,
        provider="startmessaging",
        request_id=request_id,
        created_at=now,
        expires_at=now + timedelta(seconds=expire_seconds),
        consumed=False,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


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
    phone_clean, phone_error = _safe_normalize_phone(request.phone)
    if phone_error:
        raise phone_error
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
        id=f"artisan_{phone_clean}",
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
    phone_clean, phone_error = _safe_normalize_phone(request.phone)
    if phone_error:
        raise phone_error
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
    phone_clean, phone_error = _safe_normalize_phone(request.phone)
    if phone_error:
        raise phone_error
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
        elif send_result.error_code == "RATE_LIMITED":
            status_code = status.HTTP_429_TOO_MANY_REQUESTS
        raise HTTPException(
            status_code=status_code,
            detail={
                "error_code": send_result.error_code,
                "message": send_result.message,
            },
        )

    transaction = _create_otp_transaction(db, phone_clean, send_result.request_id)
    logger.info(
        "login OTP transaction created: phone=%s request_id=%s txn_id=%s is_new_user=%s",
        _mask_phone(phone_clean),
        transaction.request_id,
        transaction.id,
        is_new_user,
    )

    return {
        "status": "success",
        "message": "OTP sent successfully.",
        "phone": phone_clean,
        "request_id": transaction.request_id,
        "otp_sent": True,
        "is_new_user": is_new_user,
    }


@router.post(
    "/verify-otp",
    response_model=AuthResponse,
    summary="Verify phone OTP",
    description="DEMO OTP MODE: accepts any valid 6-digit OTP during an active OTP transaction. "
                "Creates a new user if the phone number is not registered.",
)
async def verify_otp(
    request: OtpVerifyRequest,
    db: Session = Depends(get_db),
):
    phone_clean, phone_error = _safe_normalize_phone(request.phone)
    if phone_error:
        raise phone_error
    masked_phone = _mask_phone(phone_clean)
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

    transaction = (
        db.query(OtpTransactionDB)
        .filter(
            OtpTransactionDB.phone == phone_clean,
            OtpTransactionDB.request_id == str(request.request_id).strip(),
            OtpTransactionDB.consumed == False,  # noqa: E712
            OtpTransactionDB.expires_at > datetime.now(timezone.utc),
        )
        .first()
    )
    if not transaction:
        logger.warning(
            "verify_otp rejecting invalid/expired/consumed transaction: masked_phone=%s request_id=%s",
            masked_phone,
            request.request_id,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP session expired or invalid. Please request a new OTP.",
        )

    transaction.consumed = True
    db.commit()

    logger.info("verify_otp success: artisan_id=%s txn_id=%s", artisan.id, transaction.id)
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
    db: Session = Depends(get_db),
):
    phone_clean, phone_error = _safe_normalize_phone(request.phone)
    if phone_error:
        raise phone_error
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

    send_result = provider.send_otp(f"+91{phone_clean}")
    if not send_result.success:
        status_code = status.HTTP_502_BAD_GATEWAY
        if send_result.error_code in {"MISSING_CONFIG", "AUTHENTICATION_FAILED"}:
            status_code = status.HTTP_501_NOT_IMPLEMENTED
        elif send_result.error_code == "RATE_LIMITED":
            status_code = status.HTTP_429_TOO_MANY_REQUESTS
        raise HTTPException(
            status_code=status_code,
            detail={
                "error_code": send_result.error_code,
                "message": send_result.message,
            },
        )

    transaction = _create_otp_transaction(db, phone_clean, send_result.request_id)
    return {
        "status": "success",
        "message": "OTP resent successfully.",
        "phone": phone_clean,
        "request_id": transaction.request_id,
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
