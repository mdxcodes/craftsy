"""
Bhashini Language API Provider (Backend Proxy).

This module provides the backend-side proxy for Bhashini APIs.
All Bhashini credentials stay server-side — Flutter never sees them.

Architecture:
    Flutter App → Craftsy Backend (this module) → Bhashini API

Services:
    - ASR (Automatic Speech Recognition)
    - NMT (Neural Machine Translation)
    - TTS (Text-to-Speech)

Configuration:
    Set BHASHINI_USER_ID, BHASHINI_ULCA_API_KEY in environment variables.
    Optionally set BHASHINI_INFERENCE_API_KEY and BHASHINI_INFERENCE_API_KEY_NAME
    for compute endpoint authentication. Without credentials, all endpoints
    return 503 with clear status.

Reference:
    https://dibd-bhashini.gitbook.io/bhashini-apis
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Response, UploadFile, File
from pydantic import BaseModel, Field

from ..config import get_settings
from ..services.bhashini_service import (
    BhashiniAPIError,
    BhashiniConfigError,
    BhashiniService,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/bhashini", tags=["Bhashini Language Services"])


# ── Schemas ──────────────────────────────────────────────────────────────────


class LanguageInfo(BaseModel):
    code: str = Field(..., description="ISO-639 language code.")
    name: str = Field(..., description="English language name.")
    nativeName: str = Field(..., description="Native language name.")
    asr: bool = Field(..., description="ASR supported.")
    nmt: bool = Field(..., description="Translation supported.")
    tts: bool = Field(..., description="TTS supported.")


class TranscribeResponse(BaseModel):
    transcript: str = Field(..., description="Recognized speech text.")
    language_code: str = Field(..., description="Language code used.")
    confidence: Optional[float] = Field(default=None, description="Confidence score.")


class TranslateResponse(BaseModel):
    translated_text: str = Field(..., description="Translated text.")
    source_language: str = Field(..., description="Source language code.")
    target_language: str = Field(..., description="Target language code.")


class DetectLanguageResponse(BaseModel):
    detected_language: str = Field(..., description="Detected language code.")
    confidence: Optional[float] = Field(default=None, description="Confidence score.")


# ── Language Configuration ───────────────────────────────────────────────────
# These are the languages Craftsy actively supports in the UI.
# Bhashini capability for each language is verified against the ULCA pipeline.

BHASHINI_LANGUAGES: Dict[str, Dict[str, Any]] = {
    "en": {
        "name": "English",
        "nativeName": "English",
        "asr": True,
        "nmt": True,
        "tts": True,
    },
    "hi": {
        "name": "Hindi",
        "nativeName": "हिन्दी",
        "asr": True,
        "nmt": True,
        "tts": True,
    },
    "bn": {
        "name": "Bengali",
        "nativeName": "বাংলা",
        "asr": True,
        "nmt": True,
        "tts": False,
    },
    "ta": {
        "name": "Tamil",
        "nativeName": "தமிழ்",
        "asr": True,
        "nmt": True,
        "tts": False,
    },
    "te": {
        "name": "Telugu",
        "nativeName": "తెలుగు",
        "asr": True,
        "nmt": True,
        "tts": False,
    },
    "mr": {
        "name": "Marathi",
        "nativeName": "मराठी",
        "asr": True,
        "nmt": True,
        "tts": False,
    },
    "gu": {
        "name": "Gujarati",
        "nativeName": "ગુજરાતી",
        "asr": True,
        "nmt": True,
        "tts": False,
    },
    "kn": {
        "name": "Kannada",
        "nativeName": "ಕನ್ನಡ",
        "asr": True,
        "nmt": True,
        "tts": False,
    },
    "ml": {
        "name": "Malayalam",
        "nativeName": "മലയാളം",
        "asr": True,
        "nmt": True,
        "tts": False,
    },
    "pa": {
        "name": "Punjabi",
        "nativeName": "ਪੰਜਾਬੀ",
        "asr": True,
        "nmt": True,
        "tts": False,
    },
    "or": {
        "name": "Odia",
        "nativeName": "ଓଡ଼ିଆ",
        "asr": True,
        "nmt": True,
        "tts": False,
    },
    "as": {
        "name": "Assamese",
        "nativeName": "অসমীয়া",
        "asr": True,
        "nmt": True,
        "tts": False,
    },
    "ur": {
        "name": "Urdu",
        "nativeName": "اردو",
        "asr": True,
        "nmt": True,
        "tts": False,
    },
}

SUPPORTED_LANGUAGE_CODES = set(BHASHINI_LANGUAGES.keys())


# ── Helpers ──────────────────────────────────────────────────────────────────


def _get_bhashini_service() -> BhashiniService:
    """Create a BhashiniService from app settings."""
    settings = get_settings()
    if not settings.bhashini_user_id or not settings.bhashini_ulca_api_key:
        raise HTTPException(
            status_code=503,
            detail=(
                "Bhashini credentials not configured. "
                "Set BHASHINI_USER_ID and BHASHINI_ULCA_API_KEY environment variables."
            ),
        )
    return BhashiniService(
        user_id=settings.bhashini_user_id,
        ulca_api_key=settings.bhashini_ulca_api_key,
        inference_api_key=settings.bhashini_inference_api_key,
        inference_api_key_name=settings.bhashini_inference_api_key_name,
    )


def _is_configured() -> bool:
    settings = get_settings()
    return bool(settings.bhashini_ulca_api_key and settings.bhashini_user_id)


# ── Endpoints ────────────────────────────────────────────────────────────────


@router.get("/languages", response_model=Dict[str, Any])
async def get_supported_languages():
    """Return Bhashini-supported languages with capability flags."""
    return {
        "configured": _is_configured(),
        "languages": [
            {
                "code": code,
                **info,
            }
            for code, info in BHASHINI_LANGUAGES.items()
        ],
    }


@router.get("/status", response_model=Dict[str, Any])
async def get_service_status():
    """Check if Bhashini services are configured."""
    settings = get_settings()
    return {
        "configured": _is_configured(),
        "ulca_api_key_set": bool(settings.bhashini_ulca_api_key),
        "user_id_set": bool(settings.bhashini_user_id),
        "inference_api_key_set": bool(settings.bhashini_inference_api_key),
        "inference_api_key_name": settings.bhashini_inference_api_key_name,
        "base_url": settings.bhashini_base_url,
        "services": {
            "asr": _is_configured(),
            "nmt": _is_configured(),
            "tts": _is_configured(),
        },
        "message": (
            "Bhashini credentials configured"
            if _is_configured()
            else "Bhashini credentials not configured."
        ),
    }


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(
    audio: UploadFile = File(..., description="Audio file (.wav, .mp3, .m4a)"),
    language_code: str = Query(default="hi", description="ISO-639 language code."),
):
    """Transcribe audio using Bhashini ASR via ULCA pipeline.

    Sends audio through the Bhashini ULCA pipeline:
      1. Pipeline Config Call → obtain ASR service ID + callback URL
      2. Pipeline Compute Call → send base64 audio, receive transcript
    """
    service = _get_bhashini_service()

    if language_code not in SUPPORTED_LANGUAGE_CODES:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported language code '{language_code}'. "
                f"Supported: {sorted(SUPPORTED_LANGUAGE_CODES)}"
            ),
        )

    audio_bytes = await audio.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio file.")

    try:
        transcript = await service.transcribe_audio(
            audio_bytes=audio_bytes,
            language=language_code,
        )
    except BhashiniConfigError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except BhashiniAPIError as exc:
        logger.error("Bhashini ASR failed: %s", exc)
        raise HTTPException(status_code=502, detail=f"Bhashini ASR failed: {exc}") from exc
    except httpx.HTTPError as exc:
        logger.error("Bhashini ASR HTTP error: %s", exc)
        raise HTTPException(status_code=502, detail=f"Bhashini ASR network error: {exc}") from exc

    return TranscribeResponse(
        transcript=transcript,
        language_code=language_code,
        confidence=None,
    )


@router.post("/translate", response_model=TranslateResponse)
async def translate_text(
    text: str = Query(..., description="Text to translate."),
    source_language: str = Query(..., description="ISO-639 source language code."),
    target_language: str = Query(..., description="ISO-639 target language code."),
):
    """Translate text using Bhashini NMT via ULCA pipeline."""
    if not text.strip():
        raise HTTPException(status_code=400, detail="Empty text.")

    service = _get_bhashini_service()

    try:
        translated = await service.translate_text(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )
    except BhashiniConfigError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except BhashiniAPIError as exc:
        logger.error("Bhashini translation failed: %s", exc)
        raise HTTPException(status_code=502, detail=f"Bhashini translation failed: {exc}") from exc
    except httpx.HTTPError as exc:
        logger.error("Bhashini translation HTTP error: %s", exc)
        raise HTTPException(status_code=502, detail=f"Bhashini translation network error: {exc}") from exc

    return TranslateResponse(
        translated_text=translated,
        source_language=source_language,
        target_language=target_language,
    )


@router.post("/synthesize")
async def synthesize_speech(
    text: str = Query(..., description="Text to synthesize."),
    language_code: str = Query(default="hi", description="ISO-639 language code."),
):
    """Synthesize speech using Bhashini TTS via ULCA pipeline.

    Returns raw WAV audio bytes.
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Empty text.")

    service = _get_bhashini_service()

    try:
        audio_bytes = await service.synthesize_speech(
            text=text,
            language=language_code,
        )
    except BhashiniConfigError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except BhashiniAPIError as exc:
        logger.error("Bhashini TTS failed: %s", exc)
        raise HTTPException(status_code=502, detail=f"Bhashini TTS failed: {exc}") from exc
    except httpx.HTTPError as exc:
        logger.error("Bhashini TTS HTTP error: %s", exc)
        raise HTTPException(status_code=502, detail=f"Bhashini TTS network error: {exc}") from exc

    return Response(
        content=audio_bytes,
        media_type="audio/wav",
        headers={"Content-Disposition": f"attachment; filename=tts_{language_code}.wav"},
    )


@router.post("/detect-language", response_model=DetectLanguageResponse)
async def detect_language(
    text: str = Query(..., description="Text to detect language for."),
):
    """Detect the language of input text.

    NOTE: Bhashini does not expose a standalone ALD endpoint in the ULCA pipeline.
    This endpoint uses a lightweight heuristic based on Unicode script detection
    as a fallback when the translator cannot determine language.
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Empty text.")

    # Use simple Unicode-range heuristic for common Indian scripts.
    # This is a pragmatic fallback since Bhashini ULCA does not have a
    # dedicated text-language-detection compute endpoint.
    detected = _detect_language_heuristic(text)
    return DetectLanguageResponse(
        detected_language=detected,
        confidence=None,
    )


def _detect_language_heuristic(text: str) -> str:
    """Lightweight Unicode script-based language detection.

    Returns an ISO-639 language code or 'en' as fallback.
    """
    if not text:
        return "en"

    # Check for Devanagari script (Hindi, Marathi, Sanskrit, etc.)
    for ch in text:
        cp = ord(ch)
        if 0x0900 <= cp <= 0x097F:
            return "hi"
        if 0x0980 <= cp <= 0x09FF:
            return "bn"
        if 0x0A00 <= cp <= 0x0A7F:
            return "pa"
        if 0x0A80 <= cp <= 0x0AFF:
            return "gu"
        if 0x0B00 <= cp <= 0x0B7F:
            return "or"
        if 0x0B80 <= cp <= 0x0BFF:
            return "ta"
        if 0x0C00 <= cp <= 0x0C7F:
            return "te"
        if 0x0C80 <= cp <= 0x0CFF:
            return "kn"
        if 0x0D00 <= cp <= 0x0D7F:
            return "ml"
        if 0x0600 <= cp <= 0x06FF:
            return "ur"

    return "en"
