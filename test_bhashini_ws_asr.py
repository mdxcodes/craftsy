"""
Isolated Bhashini WebSocket ASR POC.

This script tests the Bhashini WebSocket ASR endpoint directly
without modifying any production code.

Requirements:
- websockets
- numpy (for audio conversion)

Install: pip install websockets numpy

Usage:
    python test_bhashini_ws_asr.py /path/to/audio.wav hi
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Bhashini WebSocket endpoint
BHASHINI_WS_URL = "wss://dhruva-api.bhashini.gov.in"

# Known service IDs from getModelsPipeline
KNOWN_SERVICE_IDS = {
    "hi": "ai4bharat/conformer-hi-gpu--t4",
    "en": "ai4bharat/whisper-medium-en--gpu--t4",
    "bn": "ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
    "ta": "ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
}


def load_env_credentials() -> tuple[str, str, str, str]:
    """Load Bhashini credentials from environment."""
    api_key = os.environ.get("BHASHINI_ULCA_API_KEY", "")
    user_id = os.environ.get("BHASHINI_USER_ID", "")
    inference_api_key = os.environ.get("BHASHINI_INFERENCE_API_KEY", "")
    inference_api_key_name = os.environ.get("BHASHINI_INFERENCE_API_KEY_NAME", "Authorization")
    if not api_key or not user_id:
        raise ValueError(
            "BHASHINI_ULCA_API_KEY and BHASHINI_USER_ID environment variables must be set"
        )
    return api_key, user_id, inference_api_key, inference_api_key_name


def convert_to_wav(audio_path: Path) -> Path:
    """
    Convert audio to Bhashini-required WAV format:
    - 8000 Hz
    - 16-bit PCM
    - mono
    """
    if audio_path.suffix.lower() == ".wav":
        # Check if already correct format
        import wave
        with wave.open(str(audio_path), "rb") as w:
            if (w.getnchannels() == 1 and
                w.getsampwidth() == 2 and
                w.getframerate() == 8000):
                return audio_path

    wav_path = audio_path.with_suffix(".wav")
    try:
        import subprocess
        result = subprocess.run(
            [
                "ffmpeg",
                "-i", str(audio_path),
                "-ar", "8000",
                "-ac", "1",
                "-sample_fmt", "s16",
                "-y",
                str(wav_path),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
        if wav_path.exists():
            return wav_path
    except Exception as exc:
        logger.warning("Failed to convert audio: %s", exc)

    raise ValueError(f"Could not convert {audio_path} to WAV format")


async def send_audio_chunk(ws, audio_data: bytes, chunk_size: int = 3200):
    """Send audio data in chunks (3200 bytes = 0.4s at 8000 Hz 16-bit mono)."""
    for i in range(0, len(audio_data), chunk_size):
        chunk = audio_data[i:i + chunk_size]
        await ws.send(chunk)
        await asyncio.sleep(0.2)


async def test_bhashini_websocket(audio_path: Path, language_code: str = "hi"):
    """
    Test Bhashini WebSocket ASR with a real audio file.

    Args:
        audio_path: Path to audio file (WAV, MP3, etc.)
        language_code: ISO-639 language code (hi, en, bn, ta, etc.)
    """
    api_key, user_id, inference_api_key, inference_api_key_name = load_env_credentials()
    wav_path = convert_to_wav(audio_path)

    # Read audio file
    audio_data = wav_path.read_bytes()
    logger.info("Audio file: %s (%d bytes)", wav_path, len(audio_data))

    # Get service ID for language
    service_id = KNOWN_SERVICE_IDS.get(language_code)
    if not service_id:
        raise ValueError(f"No known service ID for language '{language_code}'. Available: {list(KNOWN_SERVICE_IDS.keys())}")

    # Build ASR task config
    asr_task = {
        "taskType": "asr",
        "config": {
            "serviceId": service_id,
            "language": {
                "sourceLanguage": language_code
            },
            "samplingRate": 8000,
            "audioFormat": "wav",
            "encoding": None
        }
    }

    # Build streaming config
    streaming_config = {
        "responseFrequencyInSecs": 2.0,
        "responseTaskSequenceDepth": 1
    }

    # Build full config
    config_message = {
        "task": asr_task,
        "streamingConfig": streaming_config
    }

    logger.info("Connecting to %s", BHASHINI_WS_URL)
    logger.info("Service ID: %s", service_id)
    logger.info("Language: %s", language_code)

    import websockets
    # Try with additional headers
    extra_headers = {
        "userID": user_id,
        "ulcaApiKey": api_key,
    }
    async with websockets.connect(BHASHINI_WS_URL, extra_headers=extra_headers) as ws:
        logger.info("WebSocket connected")

        # Send auth
        auth_message = {
            "apiKey": api_key,
            "userId": user_id
        }
        await ws.send(json.dumps(auth_message))
        logger.info("Auth sent")

        # Wait for connect/ready
        connect_response = await ws.recv()
        logger.info("Connect response: %s", connect_response[:200])

        # Send ASR config
        await ws.send(json.dumps(config_message))
        logger.info("ASR config sent")

        # Wait for ready
        ready_response = await ws.recv()
        logger.info("Ready response: %s", ready_response[:200])

        # Send audio
        logger.info("Sending audio...")
        await send_audio_chunk(ws, audio_data)

        # Send terminate
        await ws.send(json.dumps({"event": "terminate"}))
        logger.info("Terminate sent")

        # Collect responses
        responses = []
        final_transcript = None
        error = None

        try:
            while True:
                response = await asyncio.wait_for(ws.recv(), timeout=10)
                logger.info("Received: %s", response[:200])

                try:
                    data = json.loads(response)
                    responses.append(data)

                    # Extract transcript from response
                    if isinstance(data, dict):
                        # Check for final transcript
                        if "pipelineResponse" in data:
                            for step in data.get("pipelineResponse", []):
                                if step.get("taskType") == "asr":
                                    output = step.get("output", [])
                                    if output:
                                        text = output[0].get("source", "")
                                        if text:
                                            final_transcript = text

                        # Check for error
                        if "error" in data or "message" in data:
                            error = data.get("error") or data.get("message")

                except json.JSONDecodeError:
                    pass

        except asyncio.TimeoutError:
            logger.info("Response collection timeout")

        logger.info("=" * 60)
        logger.info("RESULTS:")
        logger.info("Final transcript: %s", final_transcript)
        logger.info("Error: %s", error)
        logger.info("Total responses: %d", len(responses))

        return {
            "transcript": final_transcript,
            "error": error,
            "responses": len(responses),
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_bhashini_ws_asr.py <audio_file> [language_code]")
        print("Example: python test_bhashini_ws_asr.py test.wav hi")
        sys.exit(1)

    audio_file = Path(sys.argv[1])
    lang = sys.argv[2] if len(sys.argv) > 2 else "hi"

    if not audio_file.exists():
        print(f"Error: Audio file not found: {audio_file}")
        sys.exit(1)

    result = asyncio.run(test_bhashini_websocket(audio_file, lang))
    print("\n" + "=" * 60)
    print("FINAL RESULT:")
    print(f"Transcript: {result['transcript']}")
    print(f"Error: {result['error']}")
    print(f"Responses received: {result['responses']}")
