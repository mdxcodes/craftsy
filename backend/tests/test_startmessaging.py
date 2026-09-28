"""
StartMessaging Service Tests.

Validates:
1. Phone normalization
2. StartMessaging send OTP flow
3. StartMessaging verify OTP flow
4. StartMessaging resend OTP flow
5. Provider failure handling
6. Missing configuration handling
7. Rate limiting / cooldown
8. No secret leakage in responses/logs
9. Integration with Craftsy auth router
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.config import get_settings
from backend.database import Base, get_db
from backend.models.db_models import ArtisanDB
from backend.services.startmessaging_service import (
    OtpProviderConfigError,
    OtpProviderError,
    StartMessagingOtpProvider,
    OtpSendResult,
    OtpVerifyResult,
    _normalize_indian_phone,
)
from backend.routers.auth import router as auth_router


# ── Phone normalization ───────────────────────────────────────────────────────


class TestPhoneNormalization:
    def test_ten_digit(self):
        assert _normalize_indian_phone("9876543210") == "+919876543210"

    def test_with_country_code(self):
        assert _normalize_indian_phone("+919876543210") == "+919876543210"

    def test_with_double_country_code(self):
        assert _normalize_indian_phone("919876543210") == "+919876543210"

    def test_with_spaces(self):
        assert _normalize_indian_phone("+91 98765 43210") == "+919876543210"

    def test_invalid_empty(self):
        with pytest.raises(ValueError):
            _normalize_indian_phone("")

    def test_invalid_too_short(self):
        with pytest.raises(ValueError):
            _normalize_indian_phone("12345")

    def test_invalid_start_digit(self):
        with pytest.raises(ValueError):
            _normalize_indian_phone("1234567890")


# ── StartMessagingOtpProvider unit tests ─────────────────────────────────────


class TestStartMessagingOtpProvider:
    def setup_method(self):
        self.settings = get_settings()
        self.settings.startmessaging_api_key = "sm_test_key"
        self.provider = StartMessagingOtpProvider()

    def test_is_configured_true(self):
        assert self.provider.is_configured() is True

    def test_is_configured_false(self):
        provider = StartMessagingOtpProvider()
        provider.settings.startmessaging_api_key = ""
        assert provider.is_configured() is False

    def test_require_configured_raises_when_missing(self):
        provider = StartMessagingOtpProvider()
        provider.settings.startmessaging_api_key = ""
        with pytest.raises(OtpProviderConfigError):
            provider.require_configured()

    @patch("backend.services.startmessaging_service.requests.post")
    def test_send_otp_success(self, mock_post):
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {
            "success": True,
            "requestId": "req_123",
        }
        mock_post.return_value.text = '{"success":true,"requestId":"req_123"}'

        result = self.provider.send_otp("+919876543210")
        assert result.success is True
        assert result.request_id == "req_123"

    @patch("backend.services.startmessaging_service.requests.post")
    def test_send_otp_provider_failure(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "success": False,
            "code": "INVALID_NUMBER",
            "message": "Invalid mobile number",
        }
        mock_post.return_value.text = '{"success":false,"code":"INVALID_NUMBER","message":"Invalid mobile number"}'

        result = self.provider.send_otp("+919876543210")
        assert result.success is False
        assert result.error_code == "INVALID_NUMBER"

    @patch("backend.services.startmessaging_service.requests.post")
    def test_send_otp_network_error(self, mock_post):
        import requests
        mock_post.side_effect = requests.RequestException("Network down")

        result = self.provider.send_otp("+919876543210")
        assert result.success is False
        assert result.error_code == "OTP_PROVIDER_UNAVAILABLE"

    @patch("backend.services.startmessaging_service.requests.post")
    def test_verify_otp_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "success": True,
            "data": {"verified": True},
        }
        mock_post.return_value.text = '{"success":true,"data":{"verified":true}}'

        result = self.provider.verify_otp("req_123", "123456")
        assert result.success is True

    @patch("backend.services.startmessaging_service.requests.post")
    def test_verify_otp_invalid(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "success": False,
            "message": "Invalid OTP",
        }
        mock_post.return_value.text = '{"success":false,"message":"Invalid OTP"}'

        result = self.provider.verify_otp("req_123", "000000")
        assert result.success is False
        assert result.error_code == "OTP_INVALID"

    @patch("backend.services.startmessaging_service.requests.post")
    def test_verify_otp_expired(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "success": False,
            "message": "OTP expired",
        }
        mock_post.return_value.text = '{"success":false,"message":"OTP expired"}'

        result = self.provider.verify_otp("req_123", "123456")
        assert result.success is False
        assert result.error_code == "OTP_EXPIRED"

    @patch("backend.services.startmessaging_service.requests.post")
    def test_verify_otp_network_error(self, mock_post):
        import requests
        mock_post.side_effect = requests.RequestException("Network down")

        result = self.provider.verify_otp("req_123", "123456")
        assert result.success is False
        assert result.error_code == "OTP_PROVIDER_UNAVAILABLE"

    def test_send_otp_rate_limit_cooldown(self):
        self.provider._last_send_ts["+919876543210"] = 9999999999
        result = self.provider.send_otp("+919876543210")
        assert result.success is False
        assert result.error_code == "RATE_LIMITED"

    @patch("backend.services.startmessaging_service.requests.post")
    def test_resend_otp_success(self, mock_post):
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {
            "success": True,
            "requestId": "req_resend",
        }
        mock_post.return_value.text = '{"success":true,"requestId":"req_resend"}'

        result = self.provider.resend_otp("+919876543210")
        assert result.success is True
        assert result.request_id == "req_resend"

    def test_no_otp_leakage_in_logs(self):
        with patch("backend.services.startmessaging_service.logger") as mock_logger:
            try:
                self.provider.verify_otp("req_123", "123456")
            except Exception:
                pass
            for call in mock_logger.info.call_args_list:
                log_msg = str(call)
                assert "123456" not in log_msg


# ── Auth router integration tests ─────────────────────────────────────────────


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    from backend.main import app

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def _create_artisan(db, phone="9876543210"):
    artisan = ArtisanDB(
        id=f"artisan_{phone[-4:]}",
        name="Test Artisan",
        phone=phone,
        craft_type="Test Craft",
        location_cluster="Test Cluster",
        state="Test State",
        experience_years="5",
        preferred_language="en",
        role="artisan",
    )
    db.add(artisan)
    db.commit()
    return artisan


class TestAuthRouterStartMessaging:
    def test_login_without_provider_returns_501(self, client, db, monkeypatch):
        _create_artisan(db, phone="9876543210")
        monkeypatch.setenv("STARTMESSAGING_API_KEY", "")
        from backend.config import get_settings
        get_settings.cache_clear()

        response = client.post(
            "/api/v1/auth/login",
            json={"phone": "9876543210"},
        )
        assert response.status_code == 501

    def test_resend_otp_without_provider_returns_501(self, client, monkeypatch):
        monkeypatch.setenv("STARTMESSAGING_API_KEY", "")
        from backend.config import get_settings
        get_settings.cache_clear()

        response = client.post(
            "/api/v1/auth/resend-otp",
            json={"phone": "9876543210"},
        )
        assert response.status_code == 501

    @patch("backend.routers.auth.StartMessagingOtpProvider")
    def test_login_with_provider_calls_send_otp(self, mock_provider_cls, client, db):
        _create_artisan(db, phone="9876543210")
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.send_otp.return_value = OtpSendResult(
            success=True, request_id="req_123"
        )
        mock_provider_cls.return_value = mock_provider

        response = client.post(
            "/api/v1/auth/login",
            json={"phone": "9876543210"},
        )
        assert response.status_code == 200
        mock_provider.send_otp.assert_called_once()

    @patch("backend.routers.auth.StartMessagingOtpProvider")
    def test_login_with_provider_missing_key_returns_501(
        self, mock_provider_cls, client, db
    ):
        _create_artisan(db, phone="9876543210")
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.send_otp.return_value = OtpSendResult(
            success=False,
            error_code="AUTHENTICATION_FAILED",
            message="StartMessaging authentication failed.",
        )
        mock_provider_cls.return_value = mock_provider

        response = client.post(
            "/api/v1/auth/login",
            json={"phone": "9876543210"},
        )
        assert response.status_code == 501

    @patch("backend.routers.auth.StartMessagingOtpProvider")
    def test_verify_otp_with_provider_success(self, mock_provider_cls, client, db):
        _create_artisan(db, phone="9876543210")
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.verify_otp.return_value = OtpVerifyResult(success=True)
        mock_provider_cls.return_value = mock_provider

        response = client.post(
            "/api/v1/auth/verify-otp",
            json={"phone": "9876543210", "request_id": "req_123", "otp": "123456"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "access_token" in data

    @patch("backend.routers.auth.StartMessagingOtpProvider")
    def test_verify_otp_with_provider_invalid_otp(self, mock_provider_cls, client, db):
        _create_artisan(db, phone="9876543210")
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.verify_otp.return_value = OtpVerifyResult(
            success=False,
            error_code="OTP_INVALID",
            message="Invalid OTP.",
        )
        mock_provider_cls.return_value = mock_provider

        response = client.post(
            "/api/v1/auth/verify-otp",
            json={"phone": "9876543210", "request_id": "req_123", "otp": "000000"},
        )
        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["error_code"] == "OTP_INVALID"

    @patch("backend.routers.auth.StartMessagingOtpProvider")
    def test_verify_otp_with_provider_expired_otp(self, mock_provider_cls, client, db):
        _create_artisan(db, phone="9876543210")
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.verify_otp.return_value = OtpVerifyResult(
            success=False,
            error_code="OTP_EXPIRED",
            message="OTP has expired.",
        )
        mock_provider_cls.return_value = mock_provider

        response = client.post(
            "/api/v1/auth/verify-otp",
            json={"phone": "9876543210", "request_id": "req_123", "otp": "123456"},
        )
        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["error_code"] == "OTP_EXPIRED"

    @patch("backend.routers.auth.StartMessagingOtpProvider")
    def test_resend_otp_with_provider_success(self, mock_provider_cls, client):
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.resend_otp.return_value = OtpSendResult(
            success=True, request_id="req_resend"
        )
        mock_provider_cls.return_value = mock_provider

        response = client.post(
            "/api/v1/auth/resend-otp",
            json={"phone": "9876543210"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["request_id"] == "req_resend"

    @patch("backend.routers.auth.StartMessagingOtpProvider")
    def test_resend_otp_rate_limited(self, mock_provider_cls, client):
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.resend_otp.return_value = OtpSendResult(
            success=False,
            error_code="RATE_LIMITED",
            message="Please wait 25 seconds before resending OTP.",
        )
        mock_provider_cls.return_value = mock_provider

        response = client.post(
            "/api/v1/auth/resend-otp",
            json={"phone": "9876543210"},
        )
        assert response.status_code == 502
        data = response.json()
        assert data["detail"]["error_code"] == "RATE_LIMITED"
