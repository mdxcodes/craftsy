"""
Artisan Voice Processor.

Processes voice notes through speech-to-text (Bhashini ASR) with craft glossary biasing.
"""

import asyncio
import logging
import os
from pathlib import Path
from typing import Optional

from ML.voice_pipeline.models import (
    Transcript,
    VoicePipelineResult,
    JobStatus,
    STTProvider,
)

logger = logging.getLogger(__name__)


class ArtisanVoiceProcessor:
    """Main processor for artisan voice note transcription."""

    def __init__(self):
        self._model = None

    def process_voice_note(
        self,
        audio_path: str,
        language_code: str = "auto",
        category_hint: Optional[str] = None,
        note_id: Optional[str] = None,
        product_draft_id: Optional[str] = None,
    ) -> VoicePipelineResult:
        """
        Transcribe a voice note using Bhashini ASR.

        Args:
            audio_path: Path to the audio file
            language_code: Language code (hi, en, bn, ta, or auto)
            category_hint: Optional craft category for glossary biasing
            note_id: Optional note identifier
            product_draft_id: Optional product draft identifier

        Returns:
            VoicePipelineResult with transcript
        """
        path = Path(audio_path)
        if not path.exists():
            return VoicePipelineResult(
                voice_note_id=note_id or "error",
                status=JobStatus.FAILED,
                error=f"Audio file not found: {audio_path}",
            )

        # Map "auto" to a default language for Bhashini.
        bhashini_language = language_code if language_code != "auto" else "hi"

        try:
            # Run async Bhashini client in a new event loop.
            # This method is called from run_in_threadpool, so there is no
            # running event loop in this thread.
            transcript_text = asyncio.run(
                self._transcribe_with_bhashini(path, bhashini_language)
            )
        except Exception as exc:
            logger.error("[ArtisanVoiceProcessor] Bhashini ASR failed: %s", exc)
            return VoicePipelineResult(
                voice_note_id=note_id or "error",
                status=JobStatus.FAILED,
                error=f"Voice transcription failed: {exc}",
            )

        if not transcript_text or not transcript_text.strip():
            return VoicePipelineResult(
                voice_note_id=note_id or "stub_note",
                status=JobStatus.COMPLETED,
                transcript=Transcript(
                    text="",
                    language_code=bhashini_language,
                    provider=STTProvider.BHASHINI,
                    duration_seconds=0.0,
                    is_fallback=False,
                ),
                elapsed_seconds=0.0,
                error="No audible speech detected. Please speak closer to the microphone.",
            )

        return VoicePipelineResult(
            voice_note_id=note_id or "stub_note",
            status=JobStatus.COMPLETED,
            transcript=Transcript(
                text=transcript_text.strip(),
                language_code=bhashini_language,
                provider=STTProvider.BHASHINI,
                duration_seconds=0.0,
                is_fallback=False,
            ),
            elapsed_seconds=0.0,
        )

    async def _transcribe_with_bhashini(self, audio_path: Path, language: str) -> str:
        """Call Bhashini ASR via the centralized service."""
        from backend.services.bhashini_service import BhashiniConfigError, BhashiniService

        api_key = os.environ.get("BHASHINI_ULCA_API_KEY", "")
        user_id = os.environ.get("BHASHINI_USER_ID", "")
        inference_api_key = os.environ.get("BHASHINI_INFERENCE_API_KEY", "")
        inference_api_key_name = os.environ.get("BHASHINI_INFERENCE_API_KEY_NAME", "Authorization")
        if not api_key or not user_id:
            raise BhashiniConfigError("Bhashini credentials not configured.")

        service = BhashiniService(
            user_id=user_id,
            ulca_api_key=api_key,
            inference_api_key=inference_api_key,
            inference_api_key_name=inference_api_key_name,
        )
        audio_bytes = audio_path.read_bytes()
        return await service.transcribe_audio(audio_bytes=audio_bytes, language=language)

