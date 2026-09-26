"""
Bhashini WebSocket ASR POC (updated with verified protocol).

This script tests the Bhashini WebSocket ASR endpoint directly
using the verified protocol from the official Bhashini Python SDK.

Verified protocol:
    URL: wss://dhruva-api.bhashini.gov.in/ws/v1/asr/stream?api_key=<key>
    Auth: query parameter api_key
    Start: JSON {"type": "start", "config": {...}, "streamingConfig": {...}}
    Audio: binary float32 PCM chunks
    End: JSON {"type": "end"}
    Response: JSON {"type": "ready"} / {"type": "transcript"} / {"type": "error"}

Requirements:
    pip install websockets

Usage:
    python test_bhashini_ws_asr.py /path/to/audio.wav hi
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import struct
import sys
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


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
    """Convert audio to WAV 16kHz mono if needed."""
    if audio_path.suffix.lower() == ".wav":
        return audio_path

    wav_path = audio_path.with_suffix(".wav")
    try:
        import subprocess
        subprocess.run(
            [
                "ffmpeg",
                "-i", str(audio_path),
                "-ar", "16000",
                "-ac", "1",
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
        logger.warning("Failed to convert audio to WAV: %s", exc)
    raise ValueError(f"Could not convert {audio_path} to WAV format")


def convert_to_float32_pcm(data: bytes) -> bytes:
    """Convert int16 PCM bytes to float32 PCM bytes."""
    int16_samples = struct.unpack(f"<{len(data)//2}h", data)
    float32_samples = [
        max(-1.0, min(1.0, sample / 32768.0)) for sample in int16_samples
    ]
    return struct.pack(f"<{len(float32_samples)}f", *float32_samples)


async def test_bhashini_websocket(audio_path: Path, language_code: str = "hi"):
    """
    Test Bhashini WebSocket ASR with a real audio file.

    Args:
        audio_path: Path to audio file (WAV, MP3, etc.)
        language_code: ISO-639 language code (hi, en, bn, ta, etc.)
    """
    _, user_id, inference_api_key, _ = load_env_credentials()
    wav_path = convert_to_wav(audio_path)

    # Read and convert audio to float32 PCM
    import wave
    with wave.open(str(wav_path), "rb") as w:
        raw_data = w.readframes(w.getnframes())
    audio_float32 = convert_to_float32_pcm(raw_data)
    logger.info("Audio file: %s (%d bytes float32)", wav_path, len(audio_float32))

    # Build WebSocket URL with inference API key
    websocket_url = (
        f"wss://dhruva-api.bhashini.gov.in/ws/v1/asr/stream"
        f"?api_key={inference_api_key}"
    )

    # Build ASR task config
    start_config = {
        "type": "start",
        "controlConfig": {"dataTracking": False},
        "config": {
            "serviceId": "bhashini/ai4b/indic-conformer/grpc",
            "language": {"sourceLanguage": language_code},
            "audioFormat": "pcm",
            "encoding": "raw",
            "samplingRate": 16000,
            "transcriptionFormat": {"value": "transcript"},
            "profanityFilter": True,
            "postProcessors": ["itn", "punctuation"],
        },
        "streamingConfig": {
            "chunkDurationMs": 200,
            "interimResults": True,
            "endOfStreamPolicy": "client_signal",
        },
    }

    logger.info("Connecting to %s", websocket_url)
    logger.info("Language: %s", language_code)

    import websockets
    async with websockets.connect(websocket_url, max_size=16 * 1024 * 1024) as ws:
        logger.info("WebSocket connected")

        # Send ASR config
        await ws.send(json.dumps(start_config))
        logger.info("ASR config sent")

        # Wait for ready or error
        while True:
            msg = await ws.recv()
            if isinstance(msg, str):
                data = json.loads(msg)
                logger.info("Received: %s", msg[:200])
                if data.get("type") == "ready":
                    logger.info("Server ready, session=%s", data.get("sessionId"))
                    break
                if data.get("type") == "error":
                    raise RuntimeError(f"Server error: {data}")

        # Send audio in chunks
        logger.info("Sending audio...")
        chunk_size = 16000 * 4 * 200 // 1000  # float32 = 4 bytes, 200ms
        for i in range(0, len(audio_float32), chunk_size):
            chunk = audio_float32[i:i + chunk_size]
            await ws.send(chunk)
            await asyncio.sleep(0.2)

        # Send end
        await ws.send(json.dumps({"type": "end"}))
        logger.info("End sent")

        # Collect responses
        final_transcript = None
        error = None

        try:
            while True:
                msg = await asyncio.wait_for(ws.recv(), timeout=10)
                if isinstance(msg, str):
                    data = json.loads(msg)
                    logger.info("Received: %s", msg[:200])

                    if data.get("type") == "transcript":
                        text = (data.get("output") or [{}])[0].get("source", "")
                        logger.info("Transcript: %s (isFinal=%s)", text, data.get("isFinal"))
                        if data.get("isFinal"):
                            final_transcript = text
                            break

                    if data.get("type") == "error":
                        error = data.get("message")
                        break
                else:
                    logger.info("Binary message: %d bytes", len(msg))

        except asyncio.TimeoutError:
            logger.info("Response collection timeout")

        logger.info("=" * 60)
        logger.info("RESULTS:")
        logger.info("Final transcript: %s", final_transcript)
        logger.info("Error: %s", error)

        return {
            "transcript": final_transcript,
            "error": error,
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
