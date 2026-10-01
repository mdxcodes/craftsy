"""
Craftsy Backend Configuration.

Loads environment variables from the root .env file and provides
centralized application settings.

Environment strategy:
    - Local development : SQLite + permissive defaults, no external keys needed.
    - Production        : PostgreSQL via DATABASE_URL, explicit CORS origins,
                          optional AI keys supplied as environment variables.

Nothing here makes a network call or requires an API key at import time.
"""

import logging
from functools import lru_cache
from pathlib import Path
from typing import Annotated, List

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode

logger = logging.getLogger(__name__)

# Directories
BACKEND_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_ROOT.parent
UPLOAD_DIR = BACKEND_ROOT / "uploads"


def _split_env_list(value):
    """Accept both JSON arrays and comma-separated strings for list settings."""
    if value is None or isinstance(value, list):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        if text.startswith("["):
            import json

            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass
        return [part.strip() for part in text.split(",") if part.strip()]
    return value


class Settings(BaseSettings):
    """Application settings with environment variable overrides."""

    app_name: str = "Craftsy API"
    app_version: str = "1.0.0"
    app_description: str = "AI-Driven Market Linkage & Smart Cataloging Backend for Marginalized Artisans"

    # Deployment environment: "development" or "production"
    environment: str = Field(
        default="development",
        description="Deployment environment (development | production).",
    )
    debug: bool = Field(
        default=False,
        description="Enable verbose SQLAlchemy echo / debug behaviour.",
    )
    log_level: str = Field(
        default="INFO",
        description="Root log level (DEBUG, INFO, WARNING, ERROR).",
    )

    # Server
    host: str = Field(default="0.0.0.0", description="Bind host.")
    port: int = Field(default=8000, description="Bind port. Railway supplies this via PORT.")

    # API Keys (all optional — the app degrades gracefully without them)
    gemini_api_key: str = Field(
        default="",
        description="Google Gemini API key for multimodal embeddings and LLM pricing/cataloging.",
    )
    whisper_api_key: str = Field(
        default="",
        description="API key for Whisper speech-to-text transcription endpoint.",
    )

    # Voice Pipeline / Speech-to-Text Settings
    whisper_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="Base URL of OpenAI-compatible Whisper transcription API.",
    )
    whisper_model: str = Field(
        default="whisper-large-v3",
        description="Whisper model identifier for audio transcription.",
    )
    stt_provider: str = Field(
        default="whisper",
        description="Transcription backend provider (whisper).",
    )
    default_language: str = Field(
        default="hi",
        description="Default source language code for voice notes.",
    )
    supported_languages: List[str] = Field(
        default=["hi", "ta", "bn", "mr", "te", "gu", "kn", "ml", "pa", "or"],
        description="Language codes accepted by the voice pipeline.",
    )
    silence_threshold_db: float = Field(
        default=-50.0,
        description=(
            "Maximum volume in dB below which audio is considered silent. "
            "Mobile recordings in noisy environments may have max_volume between -40dB and -50dB."
        ),
    )

    # Groq Cloud LLM Settings
    groq_api_key: str = Field(
        default="",
        description="API key for Groq Cloud chat completions.",
    )
    groq_base_url: str = Field(
        default="https://api.groq.com/openai/v1",
        description="Base URL for Groq Cloud API.",
    )
    groq_chat_model: str = Field(
        default="openai/gpt-oss-120b",
        description="Primary Groq model identifier for chat, cataloging, and assistance.",
    )
    groq_model_primary: str = Field(
        default="",
        description="Override primary Groq model for catalog generation (defaults to groq_chat_model if empty).",
    )
    groq_model_fallback: str = Field(
        default="",
        description="Fallback Groq model for catalog generation when primary is unavailable.",
    )
    llm_provider: str = Field(
        default="groq",
        description="Primary LLM provider: groq or gemini.",
    )
    llm_model: str = Field(
        default="gemini-2.0-flash",
        description="Primary LLM model identifier for cataloging, pricing, and social media.",
    )

    def get_active_groq_key(self) -> str:
        """Resolve active Groq API key from groq_api_key or whisper_api_key."""
        return self.groq_api_key.strip() or self.whisper_api_key.strip()

    # Bhashini Language Services (optional; server-side only)
    bhashini_user_id: str = Field(default="", description="Bhashini Udyat user identifier.")
    bhashini_ulca_api_key: str = Field(default="", description="ULCA API key for Pipeline Config authentication.")
    bhashini_inference_api_key: str = Field(default="", description="Inference API key for Bhashini compute endpoint.")
    bhashini_inference_api_key_name: str = Field(
        default="Authorization",
        description="HTTP header name for Bhashini inference API key.",
    )
    bhashini_base_url: str = Field(
        default="https://api.bhashini.gov.in",
        description="Bhashini API base URL.",
    )

    # StartMessaging OTP Service (optional; server-side only)
    startmessaging_api_key: str = Field(
        default="",
        description="StartMessaging API key for OTP delivery and verification.",
    )
    startmessaging_template_id: str = Field(
        default="",
        description="StartMessaging OTP template ID for SMS delivery (optional).",
    )

    # OTP verification mode: "provider" or "demo"
    otp_verification_mode: str = Field(
        default="provider",
        description="OTP verification mode: 'provider' uses StartMessaging verify, 'demo' accepts any valid 6-digit OTP.",
    )

    # Cloudinary Image Storage (optional; falls back to local uploads if absent)
    cloudinary_cloud_name: str = Field(
        default="",
        description="Cloudinary cloud name for persistent image storage.",
    )
    cloudinary_api_key: str = Field(
        default="",
        description="Cloudinary API key.",
    )
    cloudinary_api_secret: str = Field(
        default="",
        description="Cloudinary API secret.",
    )

    # Authentication
    auth_secret_key: str = Field(
        default="",
        description="Secret key for signing and verifying authentication tokens. "
                    "Must be set in production.",
    )
    auth_token_expiry_minutes: int = Field(
        default=60 * 24,
        description="Authentication token expiry in minutes (default 24 hours).",
    )

    # Database — defaults to local SQLite, overridden by DATABASE_URL in production.
    database_url: str = f"sqlite:///{BACKEND_ROOT / 'craftsy.db'}"
    database_echo: bool = Field(
        default=False,
        description="Echo SQL statements (dev only). Defaults to `debug` when unset.",
    )

    # Media Storage
    upload_dir: str = str(UPLOAD_DIR)
    static_url_prefix: str = "/uploads"

    # Startup behaviour
    warmup_models_enabled: bool = Field(
        default=False,
        description=(
            "Pre-download / pre-warm the rembg ONNX model on startup. "
            "Disabled by default so production containers do not download models on boot; "
            "the model is loaded lazily on first image-enhancement request instead."
        ),
    )

    # CORS — comma-separated list or JSON array. Never `*` with credentials.
    cors_origins: Annotated[List[str], NoDecode] = Field(
        default=["*"],
        description="Allowed CORS origins (comma-separated). Narrow this in production.",
    )
    cors_allow_credentials: bool = Field(
        default=False,
        description="Allow credentials. Forced off whenever a wildcard origin is present.",
    )
    cors_allow_methods: Annotated[List[str], NoDecode] = Field(
        default=["*"],
        description="Allowed CORS methods (comma-separated).",
    )
    cors_allow_headers: Annotated[List[str], NoDecode] = Field(
        default=["*"],
        description="Allowed CORS headers (comma-separated).",
    )

    model_config = {
        "env_file": str(PROJECT_ROOT / ".env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    @field_validator(
        "cors_origins",
        "cors_allow_methods",
        "cors_allow_headers",
        "supported_languages",
        mode="before",
    )
    @classmethod
    def _parse_list_settings(cls, value):
        return _split_env_list(value)

    @model_validator(mode="after")
    def _guard_cors_wildcard_credentials(self):
        """Never combine a wildcard origin with credentialed requests."""
        if "*" in self.cors_origins and self.cors_allow_credentials:
            logger.warning(
                "CORS: wildcard origin with credentials is unsafe; disabling credentials."
            )
            self.cors_allow_credentials = False
        return self

    # ── Derived helpers ──────────────────────────────────────────────────────

    @property
    def is_production(self) -> bool:
        return self.environment.strip().lower() in {"production", "prod"}

    @property
    def resolved_database_url(self) -> str:
        """Normalise the database URL for SQLAlchemy.

        Railway historically exposes `postgres://`, which SQLAlchemy does not
        recognise as a dialect prefix. Map it to `postgresql://` (psycopg2).
        """
        url = (self.database_url or "").strip()
        if url.startswith("postgres://"):
            url = "postgresql://" + url[len("postgres://"):]
        if url.startswith("postgresql+psycopg://"):
            # A psycopg (v3) URL requires the psycopg driver; keep as-is.
            return url
        return url

    @property
    def uses_sqlite(self) -> bool:
        return self.resolved_database_url.startswith("sqlite")


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


def ensure_upload_dir() -> Path:
    """Ensure media upload directory exists and is writable.

    Falls back to ``/tmp/uploads`` when the configured path cannot be
    created or written to (for example, when a Railway volume mount is
    owned by root but the container user is unprivileged).
    """
    try:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        test_file = UPLOAD_DIR / ".write_test"
        test_file.touch()
        test_file.unlink()
        return UPLOAD_DIR
    except (PermissionError, OSError):
        fallback = Path("/tmp/uploads")
        fallback.mkdir(parents=True, exist_ok=True)
        logger.warning(
            "Configured upload dir %s is not writable; falling back to %s",
            UPLOAD_DIR,
            fallback,
        )
        return fallback
