"""
MSG91 Service Tests.

Validates:
1. Phone normalization
2. MSG91 send OTP flow
3. MSG91 verify OTP flow
4. MSG91 resend OTP flow
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
from backend.services.msg91_service import (
    Msg91ConfigError,
    Msg91Service,
    Msg91SendResult,
    Msg91VerifyResult,
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


# ── Msg91Service unit tests ───────────────────────────────────────────────────


class TestMsg91Service:
    def setup_method(self):
        self.settings = get_settings()
        self.settings.msg91_auth_key = "test_auth_key"
        self.settings.msg91_template_id = "test_template"
        self.service = Msg91Service()

    def test_is_configured_true(self):
        assert self.service.is_configured() is True

    def test_is_configured_false(self):
        service = Msg91Service()
        service.settings.msg91_auth_key = ""
        assert service.is_configured() is False

    def test_require_configured_raises_when_missing(self):
        service = Msg91Service()
        service.settings.msg91_auth_key = ""
        with pytest.raises(Msg91ConfigError):
            service.require_configured()

    @patch("backend.services.msg91_service.requests.get")
    def test_send_otp_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"request_id": "req_123"}
        mock_get.return_value.text = '{"request_id":"req_123"}'

        result = self.service.send_otp("+919876543210")
        assert result.success is True
        assert result.request_id == "req_123"

    @patch("backend.services.msg91_service.requests.get")
    def test_send_otp_provider_failure(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "code": "MSG_91",
            "message": "Invalid mobile number",
        }
        mock_get.return_value.text = '{"code":"MSG_91","message":"Invalid mobile number"}'

        result = self.service.send_otp("+919876543210")
        assert result.success is False
        assert result.error_code == "MSG_91"

    @patch("backend.services.msg91_service.requests.get")
    def test_send_otp_network_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.RequestException("Network down")

        result = self.service.send_otp("+919876543210")
        assert result.success is False
        assert result.error_code == "OTP_PROVIDER_UNAVAILABLE"

    @patch("backend.services.msg91_service.requests.get")
    def test_verify_otp_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"message": "OTP verified successfully"}
        mock_get.return_value.text = '{"message":"OTP verified successfully"}'

        result = self.service.verify_otp("+919876543210", "123456")
        assert result.success is True

    @patch("backend.services.msg91_service.requests.get")
    def test_verify_otp_invalid(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"message": "Invalid OTP"}
        mock_get.return_value.text = '{"message":"Invalid OTP"}'

        result = self.service.verify_otp("+919876543210", "000000")
        assert result.success is False
        assert result.error_code == "OTP_INVALID"

    @patch("backend.services.msg91_service.requests.get")
    def test_verify_otp_expired(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"message": "OTP Expired"}
        mock_get.return_value.text = '{"message":"OTP Expired"}'

        result = self.service.verify_otp("+919876543210", "123456")
        assert result.success is False
        assert result.error_code == "OTP_EXPIRED"

    @patch("backend.services.msg91_service.requests.get")
    def test_verify_otp_network_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.RequestException("Network down")

        result = self.service.verify_otp("+919876543210", "123456")
        assert result.success is False
        assert result.error_code == "OTP_PROVIDER_UNAVAILABLE"

    def test_send_otp_rate_limit_cooldown(self):
        self.service._last_send_ts["+919876543210"] = 9999999999
        result = self.service.send_otp("+919876543210")
        assert result.success is False
        assert result.error_code == "RATE_LIMITED"

    @patch("backend.services.msg91_service.requests.get")
    def test_resend_otp_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"request_id": "req_456"}
        mock_get.return_value.text = '{"request_id":"req_456"}'

        result = self.service.resend_otp("+919876543210")
        assert result.success is True
        assert result.request_id == "req_456"

    def test_no_otp_leakage_in_logs(self):
        with patch("backend.services.msg91_service.logger") as mock_logger:
            try:
                self.service.verify_otp("+919876543210", "123456")
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


class TestAuthRouterMsg91:
    @patch("backend.routers.auth.Msg91Service")
    def test_login_without_msg91_returns_501(self, mock_service_cls, client, db):
        _create_artisan(db, phone="9876543210")
        mock_service = MagicMock()
        mock_service.is_configured.return_value = False
        mock_service_cls.return_value = mock_service

        response = client.post(
            "/api/v1/auth/login",
            json={"phone": "9876543210"},
        )
        assert response.status_code == 501

    @patch("backend.routers.auth.Msg91Service")
    def test_resend_otp_without_msg91_returns_501(self, mock_service_cls, client):
        mock_service = MagicMock()
        mock_service.is_configured.return_value = False
        mock_service_cls.return_value = mock_service

        response = client.post(
            "/api/v1/auth/resend-otp",
            json={"phone": "9876543210"},
        )
        assert response.status_code == 501

    @patch("backend.routers.auth.Msg91Service")
    def test_login_with_msg91_calls_send_otp(self, mock_service_cls, client, db):
        _create_artisan(db, phone="9876543210")
        mock_service = MagicMock()
        mock_service.is_configured.return_value = True
        mock_service.send_otp.return_value = Msg91SendResult(
            success=True, request_id="req_123"
        )
        mock_service_cls.return_value = mock_service

        response = client.post(
            "/api/v1/auth/login",
            json={"phone": "9876543210"},
        )
        assert response.status_code == 200
        mock_service.send_otp.assert_called_once()

    @patch("backend.routers.auth.Msg91Service")
    def test_login_with_msg91_missing_template_returns_501(
        self, mock_service_cls, client, db
    ):
        _create_artisan(db, phone="9876543210")
        mock_service = MagicMock()
        mock_service.is_configured.return_value = True
        mock_service.send_otp.return_value = Msg91SendResult(
            success=False,
            error_code="MISSING_CONFIG",
            message="MSG91 template ID is not configured.",
        )
        mock_service_cls.return_value = mock_service

        response = client.post(
            "/api/v1/auth/login",
            json={"phone": "9876543210"},
        )
        assert response.status_code == 501

    @patch("backend.routers.auth.Msg91Service")
    def test_verify_otp_with_msg91_success(self, mock_service_cls, client, db):
        _create_artisan(db, phone="9876543210")
        mock_service = MagicMock()
        mock_service.is_configured.return_value = True
        mock_service.verify_otp.return_value = Msg91VerifyResult(success=True)
        mock_service_cls.return_value = mock_service

        response = client.post(
            "/api/v1/auth/verify-otp",
            json={"phone": "9876543210", "otp": "123456"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "access_token" in data

    @patch("backend.routers.auth.Msg91Service")
    def test_verify_otp_with_msg91_invalid_otp(self, mock_service_cls, client, db):
        _create_artisan(db, phone="9876543210")
        mock_service = MagicMock()
        mock_service.is_configured.return_value = True
        mock_service.verify_otp.return_value = Msg91VerifyResult(
            success=False,
            error_code="OTP_INVALID",
            message="Invalid OTP.",
        )
        mock_service_cls.return_value = mock_service

        response = client.post(
            "/api/v1/auth/verify-otp",
            json={"phone": "9876543210", "otp": "000000"},
        )
        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["error_code"] == "OTP_INVALID"

    @patch("backend.routers.auth.Msg91Service")
    def test_verify_otp_with_msg91_expired_otp(self, mock_service_cls, client, db):
        _create_artisan(db, phone="9876543210")
        mock_service = MagicMock()
        mock_service.is_configured.return_value = True
        mock_service.verify_otp.return_value = Msg91VerifyResult(
            success=False,
            error_code="OTP_EXPIRED",
            message="OTP has expired.",
        )
        mock_service_cls.return_value = mock_service

        response = client.post(
            "/api/v1/auth/verify-otp",
            json={"phone": "9876543210", "otp": "123456"},
        )
        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["error_code"] == "OTP_EXPIRED"

    @patch("backend.routers.auth.Msg91Service")
    def test_resend_otp_with_msg91_success(self, mock_service_cls, client):
        mock_service = MagicMock()
        mock_service.is_configured.return_value = True
        mock_service.resend_otp.return_value = Msg91SendResult(
            success=True, request_id="req_resend"
        )
        mock_service_cls.return_value = mock_service

        response = client.post(
            "/api/v1/auth/resend-otp",
            json={"phone": "9876543210"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    @patch("backend.routers.auth.Msg91Service")
    def test_resend_otp_rate_limited(self, mock_service_cls, client):
        mock_service = MagicMock()
        mock_service.is_configured.return_value = True
        mock_service.resend_otp.return_value = Msg91SendResult(
            success=False,
            error_code="RATE_LIMITED",
            message="Please wait 25 seconds before resending OTP.",
        )
        mock_service_cls.return_value = mock_service

        response = client.post(
            "/api/v1/auth/resend-otp",
            json={"phone": "9876543210"},
        )
        assert response.status_code == 502
        data = response.json()
        assert data["detail"]["error_code"] == "RATE_LIMITED"
