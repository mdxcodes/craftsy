"""
MSG91 OTP Service.

Thin wrapper around MSG91's OTP APIs:
  - Send OTP:  POST https://control.msg91.com/api/v5/otp
  - Verify OTP: GET https://control.msg91.com/api/v5/otp/verify
  - Resend OTP: GET https://control.msg91.com/api/v5/otp/retry

Design:
  - No OTP values are ever logged or returned to the client beyond
    application-level success/failure responses.
  - Phone numbers are normalized before any external request.
  - Provider failures are translated to stable application error codes.
  - Missing configuration degrades gracefully: the app starts, but
    OTP endpoints return a clear configuration error.
"""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass, field
from typing import Dict, Optional
from urllib.parse import urlencode

import requests

from ..config import get_settings

logger = logging.getLogger(__name__)

# MSG91 OTP endpoints
MSG91_SEND_OTP_URL = "https://control.msg91.com/api/v5/otp"
MSG91_VERIFY_OTP_URL = "https://control.msg91.com/api/v5/otp/verify"
MSG91_RESEND_OTP_URL = "https://control.msg91.com/api/v5/otp/retry"


class Msg91ConfigError(Exception):
    """Raised when MSG91 is not configured."""


class Msg91ProviderError(Exception):
    """Raised when MSG91 returns a provider-side failure."""


@dataclass
class Msg91SendResult:
    success: bool
    request_id: Optional[str] = None
    error_code: Optional[str] = None
    message: Optional[str] = None


@dataclass
class Msg91VerifyResult:
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


class Msg91Service:
    """Client for MSG91 OTP APIs.

    Usage:
        service = Msg91Service()
        service.require_configured()

        send_result = service.send_otp("+919876543210", template_id="12345")
        verify_result = service.verify_otp("+919876543210", "123456")
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self._send_cooldown_seconds = 30
        self._last_send_ts: Dict[str, float] = {}

    # ── Configuration helpers ──────────────────────────────────────────────────

    def _auth_key(self) -> str:
        key = (self.settings.msg91_auth_key or "").strip()
        if not key:
            raise Msg91ConfigError(
                "MSG91_AUTH_KEY is not configured. Set it in environment variables."
            )
        return key

    def _default_template_id(self) -> Optional[str]:
        return (
            (self.settings.msg91_template_id or "").strip() or None
        )

    def require_configured(self) -> None:
        """Raise if MSG91 credentials are missing."""
        try:
            self._auth_key()
        except Msg91ConfigError:
            raise

    def is_configured(self) -> bool:
        """Return True if MSG91 credentials are present."""
        return bool((self.settings.msg91_auth_key or "").strip())

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

    # ── MSG91 API calls ────────────────────────────────────────────────────────

    def send_otp(
        self,
        phone: str,
        template_id: Optional[str] = None,
        otp_expire_seconds: Optional[int] = None,
    ) -> Msg91SendResult:
        """Send an OTP via MSG91.

        Args:
            phone: E.164 phone number (+91XXXXXXXXXX).
            template_id: MSG91 OTP template ID. Falls back to configured default.
            otp_expire_seconds: Optional OTP validity duration.

        Returns:
            Msg91SendResult indicating success or structured failure.
        """
        self.require_configured()

        normalized = _normalize_indian_phone(phone)
        cooldown = self._check_send_cooldown(normalized)
        if cooldown > 0:
            return Msg91SendResult(
                success=False,
                error_code="RATE_LIMITED",
                message=f"Please wait {cooldown} seconds before resending OTP.",
            )

        effective_template = template_id or self._default_template_id()
        if not effective_template:
            return Msg91SendResult(
                success=False,
                error_code="MISSING_CONFIG",
                message="MSG91 template ID is not configured.",
            )

        auth_key = self._auth_key()
        params = {
            "template_id": effective_template,
            "mobile": normalized,
            "authkey": auth_key,
        }
        if otp_expire_seconds:
            params["otp_expire"] = str(otp_expire_seconds)

        url = f"{MSG91_SEND_OTP_URL}?{urlencode(params)}"
        logger.info(
            "MSG91 send OTP request: phone=%s, template=%s",
            normalized[:6] + "****" + normalized[-4:],
            effective_template,
        )

        try:
            response = requests.get(url, timeout=15)
            logger.info(
                "MSG91 send OTP response status=%s body=%s",
                response.status_code,
                response.text[:200],
            )
        except requests.RequestException as exc:
            logger.error("MSG91 send OTP network error: %s", exc)
            return Msg91SendResult(
                success=False,
                error_code="OTP_PROVIDER_UNAVAILABLE",
                message="Unable to reach MSG91. Please try again later.",
            )

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                return Msg91SendResult(
                    success=False,
                    error_code="OTP_SEND_FAILED",
                    message="Invalid response from MSG91.",
                )

            request_id = data.get("request_id") or data.get("reqId") or data.get("requestid")
            if request_id:
                self._record_send(normalized)
                return Msg91SendResult(success=True, request_id=str(request_id))

            message = data.get("message") or data.get("msg") or "OTP send failed."
            error_code = data.get("code") or data.get("error_code") or "OTP_SEND_FAILED"
            return Msg91SendResult(
                success=False,
                error_code=str(error_code),
                message=str(message),
            )

        if response.status_code == 401:
            return Msg91SendResult(
                success=False,
                error_code="AUTHENTICATION_FAILED",
                message="MSG91 authentication failed.",
            )

        return Msg91SendResult(
            success=False,
            error_code="OTP_SEND_FAILED",
            message=f"MSG91 returned HTTP {response.status_code}.",
        )

    def verify_otp(self, phone: str, otp: str) -> Msg91VerifyResult:
        """Verify an OTP via MSG91.

        Args:
            phone: E.164 phone number (+91XXXXXXXXXX).
            otp: 6-digit OTP code entered by the user.

        Returns:
            Msg91VerifyResult indicating success or structured failure.
        """
        self.require_configured()
        normalized = _normalize_indian_phone(phone)

        if not re.fullmatch(r"\d{4,8}", otp or ""):
            return Msg91VerifyResult(
                success=False,
                error_code="OTP_INVALID",
                message="Invalid OTP format.",
            )

        auth_key = self._auth_key()
        params = {
            "mobile": normalized,
            "otp": otp,
            "authkey": auth_key,
        }
        url = f"{MSG91_VERIFY_OTP_URL}?{urlencode(params)}"

        logger.info(
            "MSG91 verify OTP request: phone=%s",
            normalized[:6] + "****" + normalized[-4:],
        )

        try:
            response = requests.get(url, timeout=15)
            logger.info(
                "MSG91 verify OTP response status=%s body=%s",
                response.status_code,
                response.text[:200],
            )
        except requests.RequestException as exc:
            logger.error("MSG91 verify OTP network error: %s", exc)
            return Msg91VerifyResult(
                success=False,
                error_code="OTP_PROVIDER_UNAVAILABLE",
                message="Unable to reach MSG91. Please try again later.",
            )

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                return Msg91VerifyResult(
                    success=False,
                    error_code="OTP_INVALID",
                    message="Invalid response from MSG91.",
                )

            message = data.get("message") or data.get("msg") or ""
            message_lower = str(message).lower()

            if "otp expired" in message_lower or "expired" in message_lower:
                return Msg91VerifyResult(
                    success=False,
                    error_code="OTP_EXPIRED",
                    message="OTP has expired. Please request a new one.",
                )

            if "invalid" in message_lower or "incorrect" in message_lower:
                return Msg91VerifyResult(
                    success=False,
                    error_code="OTP_INVALID",
                    message="Invalid OTP. Please check and try again.",
                )

            # MSG91 typically returns a successful payload when OTP is valid
            return Msg91VerifyResult(success=True)

        if response.status_code == 401:
            return Msg91VerifyResult(
                success=False,
                error_code="AUTHENTICATION_FAILED",
                message="MSG91 authentication failed.",
            )

        return Msg91VerifyResult(
            success=False,
            error_code="OTP_INVALID",
            message=f"MSG91 returned HTTP {response.status_code}.",
        )

    def resend_otp(self, phone: str, retry_type: str = "text") -> Msg91SendResult:
        """Resend OTP via MSG91.

        Args:
            phone: E.164 phone number (+91XXXXXXXXXX).
            retry_type: "text" for SMS, "voice" for voice call.

        Returns:
            Msg91SendResult indicating success or structured failure.
        """
        self.require_configured()
        normalized = _normalize_indian_phone(phone)

        cooldown = self._check_send_cooldown(normalized)
        if cooldown > 0:
            return Msg91SendResult(
                success=False,
                error_code="RATE_LIMITED",
                message=f"Please wait {cooldown} seconds before resending OTP.",
            )

        auth_key = self._auth_key()
        params = {
            "mobile": normalized,
            "authkey": auth_key,
            "retrytype": retry_type,
        }
        url = f"{MSG91_RESEND_OTP_URL}?{urlencode(params)}"

        logger.info(
            "MSG91 resend OTP request: phone=%s, retry_type=%s",
            normalized[:6] + "****" + normalized[-4:],
            retry_type,
        )

        try:
            response = requests.get(url, timeout=15)
            logger.info(
                "MSG91 resend OTP response status=%s body=%s",
                response.status_code,
                response.text[:200],
            )
        except requests.RequestException as exc:
            logger.error("MSG91 resend OTP network error: %s", exc)
            return Msg91SendResult(
                success=False,
                error_code="OTP_PROVIDER_UNAVAILABLE",
                message="Unable to reach MSG91. Please try again later.",
            )

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                return Msg91SendResult(
                    success=False,
                    error_code="OTP_SEND_FAILED",
                    message="Invalid response from MSG91.",
                )

            request_id = data.get("request_id") or data.get("reqId") or data.get("requestid")
            if request_id:
                self._record_send(normalized)
                return Msg91SendResult(success=True, request_id=str(request_id))

            message = data.get("message") or data.get("msg") or "Resend OTP failed."
            error_code = data.get("code") or data.get("error_code") or "OTP_SEND_FAILED"
            return Msg91SendResult(
                success=False,
                error_code=str(error_code),
                message=str(message),
            )

        if response.status_code == 401:
            return Msg91SendResult(
                success=False,
                error_code="AUTHENTICATION_FAILED",
                message="MSG91 authentication failed.",
            )

        return Msg91SendResult(
            success=False,
            error_code="OTP_SEND_FAILED",
            message=f"MSG91 returned HTTP {response.status_code}.",
        )
