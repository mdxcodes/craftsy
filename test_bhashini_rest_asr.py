#!/usr/bin/env python3
"""
Bhashini REST ASR Integration Test.

Tests the complete Pipeline Config → Compute → transcript flow
with real human audio.

Usage:
    python3 test_bhashini_rest_asr.py [audio_file.wav] [language_code]

Environment variables required:
    BHASHINI_USER_ID
    BHASHINI_ULCA_API_KEY
    BHASHINI_INFERENCE_API_KEY (optional fallback)
    BHASHINI_INFERENCE_API_KEY_NAME (default: Authorization)

Example:
    python3 test_bhashini_rest_asr.py recording.wav hi
"""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
import sys
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("bhashini_rest_asr_test")

sys.path.insert(0, str(Path(__file__).parent))
from backend.services.bhashini_service import (  # noqa: E402
    BhashiniAPIError,
    BhashiniAuthenticationError,
    BhashiniConfigError,
    BhashiniService,
)


def load_env_credentials() -> tuple[str, str, str, str]:
    """Load Bhashini credentials from environment."""
    user_id = os.environ.get("BHASHINI_USER_ID", "")
    ulca_api_key = os.environ.get("BHASHINI_ULCA_API_KEY", "")
    inference_api_key = os.environ.get("BHASHINI_INFERENCE_API_KEY", "")
    inference_api_key_name = os.environ.get("BHASHINI_INFERENCE_API_KEY_NAME", "Authorization")

    missing = []
    if not user_id:
        missing.append("BHASHINI_USER_ID")
    if not ulca_api_key:
        missing.append("BHASHINI_ULCA_API_KEY")

    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}. "
            "Set them in .env or export them before running this test."
        )

    return user_id, ulca_api_key, inference_api_key, inference_api_key_name


async def run_rest_asr_test(audio_path: Path, language: str = "hi") -> dict:
    """Run Bhashini REST ASR test with real audio."""
    user_id, ulca_api_key, inference_api_key, inference_api_key_name = load_env_credentials()

    service = BhashiniService(
        user_id=user_id,
        ulca_api_key=ulca_api_key,
        inference_api_key=inference_api_key,
        inference_api_key_name=inference_api_key_name,
    )

    audio_bytes = audio_path.read_bytes()
    logger.info(
        "Audio file: %s, size=%d bytes, language=%s",
        audio_path,
        len(audio_bytes),
        language,
    )

    start = time.perf_counter()
    try:
        transcript = await service.transcribe_audio(
            audio_bytes=audio_bytes,
            language=language,
        )
    except BhashiniConfigError as exc:
        logger.error("Configuration error: %s", exc)
        return {"success": False, "error": str(exc), "error_type": "config"}
    except BhashiniAuthenticationError as exc:
        logger.error("Authentication error: %s", exc)
        return {"success": False, "error": str(exc), "error_type": "auth"}
    except BhashiniUnsupportedLanguageError as exc:
        logger.error("Unsupported language error: %s", exc)
        return {"success": False, "error": str(exc), "error_type": "unsupported_language"}
    except BhashiniAPIError as exc:
        logger.error("API error: %s", exc)
        return {"success": False, "error": str(exc), "error_type": "api"}
    except Exception as exc:
        logger.error("Unexpected error: %s", exc)
        return {"success": False, "error": str(exc), "error_type": "unexpected"}
    finally:
        elapsed = time.perf_counter() - start

    if not transcript or not transcript.strip():
        logger.warning("Empty transcript returned.")
        return {
            "success": False,
            "error": "Empty transcript returned by Bhashini.",
            "error_type": "empty_transcript",
            "transcript": transcript,
            "latency_seconds": round(elapsed, 3),
        }

    logger.info("Transcript received in %.3fs: %r", elapsed, transcript)
    return {
        "success": True,
        "transcript": transcript,
        "language": language,
        "latency_seconds": round(elapsed, 3),
    }


def main() -> None:
    """CLI entry point."""
    audio_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("test_audio.wav")
    language = sys.argv[2] if len(sys.argv) > 2 else "hi"

    if not audio_path.exists():
        logger.error("Audio file not found: %s", audio_path)
        sys.exit(1)

    print("=" * 60)
    print("Bhashini REST ASR Integration Test")
    print("=" * 60)
    print(f"Audio file : {audio_path}")
    print(f"Language   : {language}")
    print(f"User ID    : {'*' * 8}... (hidden)")
    print()

    result = asyncio.run(run_rest_asr_test(audio_path, language))

    print("-" * 60)
    if result["success"]:
        print(f"SUCCESS")
        print(f"Transcript : {result['transcript']}")
        print(f"Language   : {result.get('language')}")
        print(f"Latency    : {result.get('latency_seconds')}s")
    else:
        print(f"FAILED")
        print(f"Error type : {result.get('error_type')}")
        print(f"Error      : {result.get('error')}")
    print("=" * 60)

    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
