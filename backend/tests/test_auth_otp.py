"""
Backend tests for Craftsy authentication flow with StartMessaging delivery.

Tests cover:
  - Phone normalization
  - OTP transaction creation
  - Demo-mode OTP acceptance (any valid 6-digit OTP)
  - Transaction expiry
  - Transaction consumption
  - New user creation
  - Existing user login
  - Duplicate user prevention
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient
from backend.routers.auth import router as auth_router
from backend.models.db_models import ArtisanDB, OtpTransactionDB
from backend.services.startmessaging_service import (
    OtpSendResult,
    OtpVerifyResult,
    StartMessagingOtpProvider,
)
from backend.database import Base, get_db


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

    app.include_router(auth_router, prefix="/api/v1/auth")
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


class TestPhoneNormalization:
    @patch("backend.routers.auth.StartMessagingOtpProvider")
    def test_plain_10_digits(self, mock_provider_cls, client, monkeypatch):
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.send_otp.return_value = OtpSendResult(
            success=True,
            request_id="req_phone_1",
        )
        mock_provider_cls.return_value = mock_provider
        monkeypatch.setenv("OTP_VERIFICATION_MODE", "demo")

        response = client.post("/api/v1/auth/login", json={"phone": "9876543210"})
        assert response.status_code == 200
        data = response.json()
        assert data["phone"] == "9876543210"

    @patch("backend.routers.auth.StartMessagingOtpProvider")
    def test_with_plus_91_prefix(self, mock_provider_cls, client, monkeypatch):
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.send_otp.return_value = OtpSendResult(
            success=True,
            request_id="req_phone_2",
        )
        mock_provider_cls.return_value = mock_provider
        monkeypatch.setenv("OTP_VERIFICATION_MODE", "demo")

        response = client.post("/api/v1/auth/login", json={"phone": "+919876543210"})
        assert response.status_code == 200
        data = response.json()
        assert data["phone"] == "9876543210"

    @patch("backend.routers.auth.StartMessagingOtpProvider")
    def test_with_91_prefix(self, mock_provider_cls, client, monkeypatch):
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.send_otp.return_value = OtpSendResult(
            success=True,
            request_id="req_phone_3",
        )
        mock_provider_cls.return_value = mock_provider
        monkeypatch.setenv("OTP_VERIFICATION_MODE", "demo")

        response = client.post("/api/v1/auth/login", json={"phone": "919876543210"})
        assert response.status_code == 200
        data = response.json()
        assert data["phone"] == "9876543210"

    def test_invalid_too_short(self, client):
        response = client.post("/api/v1/auth/login", json={"phone": "987654321"})
        assert response.status_code == 400

    def test_invalid_too_long(self, client):
        response = client.post("/api/v1/auth/login", json={"phone": "987654321012"})
        assert response.status_code == 400

    def test_invalid_start_digit(self, client):
        response = client.post("/api/v1/auth/login", json={"phone": "1234567890"})
        assert response.status_code == 400


class TestStartMessagingDelivery:
    @patch("backend.routers.auth.StartMessagingOtpProvider")
    def test_login_sends_real_otp_and_creates_transaction(
        self, mock_provider_cls, client, db, monkeypatch
    ):
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.send_otp.return_value = OtpSendResult(
            success=True,
            request_id="req_12345",
        )
        mock_provider_cls.return_value = mock_provider

        monkeypatch.setenv("OTP_VERIFICATION_MODE", "demo")

        response = client.post(
            "/api/v1/auth/login",
            json={"phone": "9876543210"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["request_id"] == "req_12345"
        assert data["is_new_user"] is True

        mock_provider.send_otp.assert_called_once_with("+919876543210")

        txn = db.query(OtpTransactionDB).filter(OtpTransactionDB.request_id == "req_12345").first()
        assert txn is not None
        assert txn.phone == "9876543210"
        assert txn.consumed is False
        assert txn.expires_at > datetime.utcnow() + timedelta(seconds=290)

    @patch("backend.routers.auth.StartMessagingOtpProvider")
    def test_login_rate_limit_from_provider(
        self, mock_provider_cls, client, monkeypatch
    ):
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.send_otp.return_value = OtpSendResult(
            success=False,
            error_code="RATE_LIMITED",
            message="Please wait 25 seconds before resending OTP.",
        )
        mock_provider_cls.return_value = mock_provider

        response = client.post(
            "/api/v1/auth/login",
            json={"phone": "9876543210"},
        )
        assert response.status_code == 429
        data = response.json()
        assert data["detail"]["error_code"] == "RATE_LIMITED"


class TestDemoOtpVerification:
    def _create_transaction(self, db, phone, request_id, *, expired=False, consumed=False):
        now = datetime.utcnow()
        txn = OtpTransactionDB(
            id=f"otp_txn_{phone}_{uuid4().hex[:8]}",
            phone=phone,
            provider="startmessaging",
            request_id=request_id,
            created_at=now,
            expires_at=now - timedelta(seconds=1) if expired else now + timedelta(seconds=300),
            consumed=consumed,
        )
        db.add(txn)
        db.commit()
        db.refresh(txn)
        return txn

    def test_any_otp_accepted_in_demo_mode(self, client, db, monkeypatch):
        monkeypatch.setenv("OTP_VERIFICATION_MODE", "demo")

        for idx, otp in enumerate(["123456", "482931", "999999"]):
            request_id = f"req_demo_{idx}"
            self._create_transaction(db, "9876543210", request_id)

            response = client.post(
                "/api/v1/auth/verify-otp",
                json={
                    "phone": "9876543210",
                    "request_id": request_id,
                    "otp": otp,
                },
            )
            assert response.status_code == 200, f"OTP {otp} was rejected"
            data = response.json()
            assert data["status"] == "success"
            assert "access_token" in data

    def test_verify_without_transaction_rejected(self, client, monkeypatch):
        monkeypatch.setenv("OTP_VERIFICATION_MODE", "demo")
        response = client.post(
            "/api/v1/auth/verify-otp",
            json={
                "phone": "9876543210",
                "request_id": "req_nonexistent",
                "otp": "123456",
            },
        )
        assert response.status_code == 400
        assert "expired" in response.json()["detail"].lower() or "invalid" in response.json()["detail"].lower()

    def test_verify_after_expiry_rejected(self, client, db, monkeypatch):
        monkeypatch.setenv("OTP_VERIFICATION_MODE", "demo")
        self._create_transaction(db, "9876543210", "req_expired", expired=True)

        response = client.post(
            "/api/v1/auth/verify-otp",
            json={
                "phone": "9876543210",
                "request_id": "req_expired",
                "otp": "123456",
            },
        )
        assert response.status_code == 400

    def test_verify_after_consumption_rejected(self, client, db, monkeypatch):
        monkeypatch.setenv("OTP_VERIFICATION_MODE", "demo")
        self._create_transaction(db, "9876543210", "req_consumed", consumed=True)

        response = client.post(
            "/api/v1/auth/verify-otp",
            json={
                "phone": "9876543210",
                "request_id": "req_consumed",
                "otp": "123456",
            },
        )
        assert response.status_code == 400


class TestUserFlows:
    @patch("backend.routers.auth.StartMessagingOtpProvider")
    def test_new_user_created_on_first_login(
        self, mock_provider_cls, client, db, monkeypatch
    ):
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.send_otp.return_value = OtpSendResult(
            success=True,
            request_id="req_new_user",
        )
        mock_provider_cls.return_value = mock_provider

        monkeypatch.setenv("OTP_VERIFICATION_MODE", "demo")

        login_response = client.post(
            "/api/v1/auth/login",
            json={"phone": "9999999999"},
        )
        assert login_response.status_code == 200

        verify_response = client.post(
            "/api/v1/auth/verify-otp",
            json={
                "phone": "9999999999",
                "request_id": "req_new_user",
                "otp": "111111",
            },
        )
        assert verify_response.status_code == 200
        data = verify_response.json()
        assert data["artisan"]["phone"] == "9999999999"

        artisan = db.query(ArtisanDB).filter(ArtisanDB.phone == "9999999999").first()
        assert artisan is not None
        assert artisan.id == "artisan_9999999999"

    @patch("backend.routers.auth.StartMessagingOtpProvider")
    def test_existing_user_login_returns_same_profile(
        self, mock_provider_cls, client, db, monkeypatch
    ):
        existing = ArtisanDB(
            id="artisan_9876543210",
            name="Test Artisan",
            phone="9876543210",
            craft_type="Pottery",
            location_cluster="Delhi",
            state="Delhi",
            role="artisan",
        )
        db.add(existing)
        db.commit()

        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.send_otp.return_value = OtpSendResult(
            success=True,
            request_id="req_existing",
        )
        mock_provider_cls.return_value = mock_provider

        monkeypatch.setenv("OTP_VERIFICATION_MODE", "demo")

        login_response = client.post(
            "/api/v1/auth/login",
            json={"phone": "9876543210"},
        )
        assert login_response.status_code == 200

        verify_response = client.post(
            "/api/v1/auth/verify-otp",
            json={
                "phone": "9876543210",
                "request_id": "req_existing",
                "otp": "222222",
            },
        )
        assert verify_response.status_code == 200
        data = verify_response.json()
        assert data["artisan"]["id"] == "artisan_9876543210"
        assert data["artisan"]["name"] == "Test Artisan"

    def test_duplicate_phone_does_not_create_duplicate(self, client, db, monkeypatch):
        existing = ArtisanDB(
            id="artisan_9876543210",
            name="Test Artisan",
            phone="9876543210",
            role="artisan",
        )
        db.add(existing)
        db.commit()

        with patch("backend.routers.auth.StartMessagingOtpProvider") as mock_provider_cls:
            mock_provider = MagicMock()
            mock_provider.is_configured.return_value = True
            mock_provider.send_otp.return_value = OtpSendResult(
                success=True,
                request_id="req_dup",
            )
            mock_provider_cls.return_value = mock_provider

            monkeypatch.setenv("OTP_VERIFICATION_MODE", "demo")

            login_response = client.post(
                "/api/v1/auth/login",
                json={"phone": "9876543210"},
            )
            assert login_response.status_code == 200

            verify_response = client.post(
                "/api/v1/auth/verify-otp",
                json={
                    "phone": "9876543210",
                    "request_id": "req_dup",
                    "otp": "333333",
                },
            )
            assert verify_response.status_code == 200

            count = db.query(ArtisanDB).filter(ArtisanDB.phone == "9876543210").count()
            assert count == 1
