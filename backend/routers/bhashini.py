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
    - ALD (Automatic Language Detection)

Configuration:
    Set BHASHINI_API_KEY and BHASHINI_USER_ID in environment variables.
    Without credentials, all endpoints return 503 with clear status.
"""

from __future__ import annotations

import os
import httpx
import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from ..database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/bhashini", tags=["Bhashini Language Services"])


# ── Configuration ────────────────────────────────────────────────────────────


def _get_bhashini_config() -> Dict[str, str]:
    """Get Bhashini credentials from environment."""
    return {
        "api_key": os.getenv("BHASHINI_API_KEY", ""),
        "user_id": os.getenv("BHASHINI_USER_ID", ""),
        "base_url": os.getenv("BHASHINI_BASE_URL", "https://api.bhashini.gov.in"),
    }


def _is_configured() -> bool:
    """Check if Bhashini credentials are configured."""
    config = _get_bhashini_config()
    return bool(config["api_key"] and config["user_id"])


def _get_headers() -> Dict[str, str]:
    """Get request headers with credentials."""
    config = _get_bhashini_config()
    return {
        "Authorization": f"Bearer {config['api_key']}",
        "X-User-Id": config["user_id"],
        "Content-Type": "application/json",
    }


# ── Language Configuration ───────────────────────────────────────────────────


# Bhashini-supported languages with capability flags
# Source: https://bhashini.gov.in/
BHASHINI_LANGUAGES = {
    "en": {"name": "English", "nativeName": "English", "asr": True, "nmt": True, "tts": True, "ald": True},
    "hi": {"name": "Hindi", "nativeName": "हिन्दी", "asr": True, "nmt": True, "tts": True, "ald": True},
    "bn": {"name": "Bengali", "nativeName": "বাংলা", "asr": True, "nmt": True, "tts": False, "ald": True},
    "ta": {"name": "Tamil", "nativeName": "தமிழ்", "asr": True, "nmt": True, "tts": False, "ald": True},
    "te": {"name": "Telugu", "nativeName": "తెలుగు", "asr": True, "nmt": True, "tts": False, "ald": True},
    "mr": {"name": "Marathi", "nativeName": "मराठी", "asr": True, "nmt": True, "tts": False, "ald": True},
    "gu": {"name": "Gujarati", "nativeName": "ગુજરાતી", "asr": True, "nmt": True, "tts": False, "ald": True},
    "kn": {"name": "Kannada", "nativeName": "ಕನ್ನಡ", "asr": True, "nmt": True, "tts": False, "ald": True},
    "ml": {"name": "Malayalam", "nativeName": "മലയാളം", "asr": True, "nmt": True, "tts": False, "ald": True},
    "pa": {"name": "Punjabi", "nativeName": "ਪੰਜਾਬੀ", "asr": True, "nmt": True, "tts": False, "ald": True},
    "or": {"name": "Odia", "nativeName": "ଓଡ଼ିଆ", "asr": True, "nmt": True, "tts": False, "ald": True},
    "as": {"name": "Assamese", "nativeName": "অসমীয়া", "asr": True, "nmt": True, "tts": False, "ald": True},
    "ur": {"name": "Urdu", "nativeName": "اردو", "asr": True, "nmt": True, "tts": False, "ald": True},
    "sd": {"name": "Sindhi", "nativeName": "سنڌي", "asr": False, "nmt": True, "tts": False, "ald": True},
    "ne": {"name": "Nepali", "nativeName": "नेपाली", "asr": False, "nmt": True, "tts": False, "ald": True},
    "sa": {"name": "Sanskrit", "nativeName": "संस्कृतम्", "asr": False, "nmt": True, "tts": False, "ald": True},
    "kok": {"name": "Konkani", "nativeName": "कोंकणी", "asr": False, "nmt": True, "tts": False, "ald": True},
    "mni": {"name": "Manipuri", "nativeName": "মৈতৈলোন", "asr": False, "nmt": True, "tts": False, "ald": True},
    "sat": {"name": "Santali", "nativeName": "ᱥᱟᱱᱛᱟᱲᱤ", "asr": False, "nmt": True, "tts": False, "ald": True},
    "doi": {"name": "Dogri", "nativeName": "डोगरी", "asr": False, "nmt": True, "tts": False, "ald": True},
    "brx": {"name": "Bodo", "nativeName": "बर'", "asr": False, "nmt": True, "tts": False, "ald": True},
    "ks": {"name": "Kashmiri", "nativeName": "कश्मीरी", "asr": False, "nmt": True, "tts": False, "ald": True},
    "gom": {"name": "Goan Konkani", "nativeName": "गोंयची कोंकणी", "asr": False, "nmt": True, "tts": False, "ald": True},
    "mai": {"name": "Maithili", "nativeName": "मैथिली", "asr": False, "nmt": True, "tts": False, "ald": True},
}


@router.get("/languages")
async def get_supported_languages():
    """Get all Bhashini-supported languages with capabilities."""
    return {
        "configured": _is_configured(),
        "languages": BHASHINI_LANGUAGES,
    }


@router.get("/status")
async def get_service_status():
    """Check if Bhashini services are configured and available."""
    config = _get_bhashini_config()
    return {
        "configured": _is_configured(),
        "api_key_set": bool(config["api_key"]),
        "user_id_set": bool(config["user_id"]),
        "base_url": config["base_url"],
        "services": {
            "asr": _is_configured(),
            "nmt": _is_configured(),
            "tts": _is_configured(),
            "ald": _is_configured(),
        },
        "message": "Bhashini credentials configured" if _is_configured() else "Bhashini credentials not configured. Set BHASHINI_API_KEY and BHASHINI_USER_ID environment variables.",
    }


@router.post("/transcribe")
async def transcribe_audio(
    audio: UploadFile = File(..., description="Audio file (.m4a, .wav, .mp3)"),
    language_code: str = "hi",
):
    """
    Transcribe audio using Bhashini ASR.

    Requires Bhashini credentials configured server-side.
    """
    if not _is_configured():
        raise HTTPException(
            status_code=503,
            detail="Bhashini ASR not configured. Set BHASHINI_API_KEY and BHASHINI_USER_ID.",
        )

    # Read audio bytes
    audio_bytes = await audio.read()

    # Map to Bhashini language code
    bhashini_code = BHASHINI_LANGUAGES.get(language_code, {}).get("code", language_code)

    # Call Bhashini ASR API
    config = _get_bhashini_config()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{config['base_url']}/asr/transcribe",
                headers=_get_headers(),
                files={"audio": (audio.filename or "audio.m4a", audio_bytes, "audio/m4a")},
                data={"language_code": bhashini_code},
            )
            response.raise_for_status()
            result = response.json()
            return {
                "transcript": result.get("transcript", ""),
                "language_code": language_code,
                "confidence": result.get("confidence", 0.0),
            }
    except httpx.HTTPError as e:
        logger.error(f"Bhashini ASR error: {e}")
        raise HTTPException(status_code=502, detail=f"Bhashini ASR failed: {str(e)}")


@router.post("/translate")
async def translate_text(
    text: str,
    source_language: str,
    target_language: str,
):
    """
    Translate text using Bhashini NMT.

    Requires Bhashini credentials configured server-side.
    """
    if not _is_configured():
        raise HTTPException(
            status_code=503,
            detail="Bhashini NMT not configured. Set BHASHINI_API_KEY and BHASHINI_USER_ID.",
        )

    config = _get_bhashini_config()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{config['base_url']}/nmt/translate",
                headers=_get_headers(),
                json={
                    "text": text,
                    "source_language": source_language,
                    "target_language": target_language,
                },
            )
            response.raise_for_status()
            result = response.json()
            return {
                "translated_text": result.get("translated_text", ""),
                "source_language": source_language,
                "target_language": target_language,
            }
    except httpx.HTTPError as e:
        logger.error(f"Bhashini NMT error: {e}")
        raise HTTPException(status_code=502, detail=f"Bhashini NMT failed: {str(e)}")


@router.post("/synthesize")
async def synthesize_speech(
    text: str,
    language_code: str,
):
    """
    Synthesize speech using Bhashini TTS.

    Requires Bhashini credentials configured server-side.
    """
    if not _is_configured():
        raise HTTPException(
            status_code=503,
            detail="Bhashini TTS not configured. Set BHASHINI_API_KEY and BHASHINI_USER_ID.",
        )

    config = _get_bhashini_config()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{config['base_url']}/tts/synthesize",
                headers=_get_headers(),
                json={
                    "text": text,
                    "language_code": language_code,
                },
                response_type="bytes",
            )
            response.raise_for_status()
            return Response(
                content=response.content,
                media_type="audio/mpeg",
                headers={"Content-Disposition": f"attachment; filename=tts_{language_code}.mp3"},
            )
    except httpx.HTTPError as e:
        logger.error(f"Bhashini TTS error: {e}")
        raise HTTPException(status_code=502, detail=f"Bhashini TTS failed: {str(e)}")


@router.post("/detect-language")
async def detect_language(
    text: str,
):
    """
    Detect language using Bhashini ALD.

    Requires Bhashini credentials configured server-side.
    """
    if not _is_configured():
        raise HTTPException(
            status_code=503,
            detail="Bhashini ALD not configured. Set BHASHINI_API_KEY and BHASHINI_USER_ID.",
        )

    config = _get_bhashini_config()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{config['base_url']}/ald/detect",
                headers=_get_headers(),
                json={"text": text},
            )
            response.raise_for_status()
            result = response.json()
            return {
                "detected_language": result.get("language_code", "unknown"),
                "confidence": result.get("confidence", 0.0),
            }
    except httpx.HTTPError as e:
        logger.error(f"Bhashini ALD error: {e}")
        raise HTTPException(status_code=502, detail=f"Bhashini ALD failed: {str(e)}")
