"""
StartMessaging OTP Service.

Thin wrapper around StartMessaging's OTP APIs:
  - Send OTP:    POST https://api.startmessaging.com/otp/send
  - Verify OTP:  POST https://api.startmessaging.com/otp/verify

Design:
  - Craftsy generates the OTP and passes it to StartMessaging for delivery.
  - StartMessaging stores the OTP and verifies it on /otp/verify.
  - Phone numbers are normalized before any external request.
  - Provider failures are translated to stable application error codes.
  - Missing configuration degrades gracefully.
"""

from __future__ import annotations

import logging
import re
import secrets
import string
import time
from dataclasses import dataclass
from typing import Dict, Optional

import requests

from ..config import get_settings

logger = logging.getLogger(__name__)

# StartMessaging Auth API endpoints
# Official docs: https://startmessaging.com/auth-api
# Base URL: https://api.startmessaging.com
STARTMESSAGING_SEND_OTP_URL = "https://api.startmessaging.com/otp/send"
STARTMESSAGING_VERIFY_OTP_URL = "https://api.startmessaging.com/otp/verify"


class OtpProviderConfigError(Exception):
    """Raised when StartMessaging is not configured."""


class OtpProviderError(Exception):
    """Raised when StartMessaging returns a provider-side failure."""


@dataclass
class OtpSendResult:
    success: bool
    request_id: Optional[str] = None
    error_code: Optional[str] = None
    message: Optional[str] = None


@dataclass
class OtpVerifyResult:
    success: bool
    error_code: Optional[str] = None
    message: Optional[str] = None


def _normalize_indian_phone(phone: str) -> str:
    """Normalize an Indian phone number to E.164 format (+91XXXXXXXXXX).

    Accepts:
      9876543210
      +919876543210
      919876543210

    Raises ValueError on obviously invalid numbers.
    """
    digits = re.sub(r"\D", "", phone or "")
    if not digits:
        raise ValueError("Phone number is empty")

    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]

    if len(digits) != 10:
        raise ValueError(
            f"Invalid Indian phone number: expected 10 digits, got {len(digits)}"
        )

    if not digits[0] in "6789":
        raise ValueError(
            f"Invalid Indian phone number: must start with 6/7/8/9, got {digits[0]}"
        )

    return f"+91{digits}"


def _generate_otp(length: int = 6) -> str:
    """Generate a numeric OTP of the requested length."""
    return "".join(secrets.choice(string.digits) for _ in range(length))


class StartMessagingOtpProvider:
    """Client for StartMessaging OTP APIs.

    Usage:
        provider = StartMessagingOtpProvider()
        provider.require_configured()

        send_result = provider.send_otp("+919876543210")
        verify_result = provider.verify_otp(send_result.request_id, "123456")
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self._send_cooldown_seconds = 30
        self._last_send_ts: Dict[str, float] = {}

    # ── Configuration helpers ──────────────────────────────────────────────────

    def _default_template_id(self) -> Optional[str]:
        return (self.settings.startmessaging_template_id or "").strip() or None

    def _api_key(self) -> str:
        key = (self.settings.startmessaging_api_key or "").strip()
        if not key:
            raise OtpProviderConfigError(
                "STARTMESSAGING_API_KEY is not configured. Set it in environment variables."
            )
        return key

    def require_configured(self) -> None:
        """Raise if StartMessaging credentials are missing."""
        try:
            self._api_key()
        except OtpProviderConfigError:
            raise

    def is_configured(self) -> bool:
        """Return True if StartMessaging credentials are present."""
        return bool((self.settings.startmessaging_api_key or "").strip())

    # ── Rate limiting / cooldown ────────────────────────────────────────────────

    def _check_send_cooldown(self, phone: str) -> Optional[int]:
        """Return seconds until next send is allowed, or 0."""
        last = self._last_send_ts.get(phone)
        if last is None:
            return 0
        elapsed = time.time() - last
        remaining = int(self._send_cooldown_seconds - elapsed)
        return max(0, remaining)

    def _record_send(self, phone: str) -> None:
        self._last_send_ts[phone] = time.time()

    # ── StartMessaging API calls ───────────────────────────────────────────────

    def send_otp(self, phone: str) -> OtpSendResult:
        """Send an OTP via StartMessaging.

        Args:
            phone: E.164 phone number (+91XXXXXXXXXX).

        Returns:
            OtpSendResult indicating success or structured failure.
        """
        self.require_configured()

        normalized = _normalize_indian_phone(phone)
        cooldown = self._check_send_cooldown(normalized)
        if cooldown > 0:
            return OtpSendResult(
                success=False,
                error_code="RATE_LIMITED",
                message=f"Please wait {cooldown} seconds before resending OTP.",
            )

        otp = _generate_otp(6)
        api_key = self._api_key()
        payload: Dict[str, object] = {
            "phoneNumber": normalized,
            "variables": {
                "otp": otp,
                "appName": "Craftsy",
            },
        }

        effective_template = self._default_template_id()
        if effective_template:
            payload["templateId"] = effective_template

        logger.info(
            "StartMessaging send OTP request: phone=%s",
            normalized[:6] + "****" + normalized[-4:],
        )

        try:
            response = requests.post(
                STARTMESSAGING_SEND_OTP_URL,
                headers={
                    "X-API-Key": api_key,
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=15,
            )
            logger.info(
                "StartMessaging send OTP response status=%s body=%s",
                response.status_code,
                response.text[:200],
            )
        except requests.RequestException as exc:
            logger.error("StartMessaging send OTP network error: %s", exc)
            return OtpSendResult(
                success=False,
                error_code="OTP_PROVIDER_UNAVAILABLE",
                message="Unable to reach StartMessaging. Please try again later.",
            )

        if response.status_code in (200, 201):
            try:
                data = response.json()
            except ValueError:
                return OtpSendResult(
                    success=False,
                    error_code="OTP_SEND_FAILED",
                    message="Invalid response from StartMessaging.",
                )

            request_id = data.get("requestId") or data.get("request_id")
            if request_id:
                self._record_send(normalized)
                return OtpSendResult(success=True, request_id=str(request_id))

            message = data.get("message") or data.get("msg") or "OTP send failed."
            error_code = data.get("code") or data.get("error_code") or "OTP_SEND_FAILED"
            return OtpSendResult(
                success=False,
                error_code=str(error_code),
                message=str(message),
            )

        if response.status_code == 401:
            return OtpSendResult(
                success=False,
                error_code="AUTHENTICATION_FAILED",
                message="StartMessaging authentication failed.",
            )

        return OtpSendResult(
            success=False,
            error_code="OTP_SEND_FAILED",
            message=f"StartMessaging returned HTTP {response.status_code}.",
        )

    def verify_otp(self, request_id: str, otp: str) -> OtpVerifyResult:
        """Verify an OTP via StartMessaging.

        Args:
            request_id: OTP request ID returned by send_otp.
            otp: OTP code entered by the user.

        Returns:
            OtpVerifyResult indicating success or structured failure.
        """
        self.require_configured()

        if not request_id or not request_id.strip():
            return OtpVerifyResult(
                success=False,
                error_code="OTP_INVALID",
                message="Missing OTP request ID.",
            )

        if not re.fullmatch(r"\d{4,8}", otp or ""):
            return OtpVerifyResult(
                success=False,
                error_code="OTP_INVALID",
                message="Invalid OTP format.",
            )

        api_key = self._api_key()
        payload = {
            "requestId": request_id.strip(),
            "otpCode": otp.strip(),
        }

        logger.info(
            "StartMessaging verify OTP request: request_id=%s",
            request_id,
        )

        try:
            response = requests.post(
                STARTMESSAGING_VERIFY_OTP_URL,
                headers={
                    "X-API-Key": api_key,
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=15,
            )
            logger.info(
                "StartMessaging verify OTP response status=%s body=%s",
                response.status_code,
                response.text[:200],
            )
        except requests.RequestException as exc:
            logger.error("StartMessaging verify OTP network error: %s", exc)
            return OtpVerifyResult(
                success=False,
                error_code="OTP_PROVIDER_UNAVAILABLE",
                message="Unable to reach StartMessaging. Please try again later.",
            )

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                return OtpVerifyResult(
                    success=False,
                    error_code="OTP_INVALID",
                    message="Invalid response from StartMessaging.",
                )

            verified = data.get("verified") or (
                isinstance(data.get("data"), dict) and data["data"].get("verified")
            )
            if verified:
                return OtpVerifyResult(success=True)

            message = data.get("message") or data.get("msg") or ""
            message_lower = str(message).lower()

            if "expired" in message_lower:
                return OtpVerifyResult(
                    success=False,
                    error_code="OTP_EXPIRED",
                    message="OTP has expired. Please request a new one.",
                )

            if "invalid" in message_lower or "incorrect" in message_lower:
                return OtpVerifyResult(
                    success=False,
                    error_code="OTP_INVALID",
                    message="Invalid OTP. Please check and try again.",
                )

            return OtpVerifyResult(
                success=False,
                error_code="OTP_INVALID",
                message="OTP verification failed.",
            )

        if response.status_code == 401:
            return OtpVerifyResult(
                success=False,
                error_code="AUTHENTICATION_FAILED",
                message="StartMessaging authentication failed.",
            )

        return OtpVerifyResult(
            success=False,
            error_code="OTP_INVALID",
            message=f"StartMessaging returned HTTP {response.status_code}.",
        )

    def resend_otp(self, phone: str) -> OtpSendResult:
        """Resend OTP via StartMessaging.

        Args:
            phone: E.164 phone number (+91XXXXXXXXXX).

        Returns:
            OtpSendResult indicating success or structured failure.
        """
        # StartMessaging resend is the same as a fresh send with a new OTP.
        return self.send_otp(phone)
