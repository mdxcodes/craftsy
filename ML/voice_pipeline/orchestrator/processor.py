"""
Artisan Voice Processor.

The main entry point for processing an artisan's voice note:
1. Validates the recording
2. Transcribes it in its source language using Bhashini ASR

The pipeline stops at the transcript. Listing generation is owned by the
backend catalog service, which consumes the transcript this module produces —
see the README for the handoff contract.

This is triggered when the mobile app drains its offline queue and uploads a
recording. The artisan is never blocked waiting on it — the recording is saved
locally first and processed whenever connectivity allows.
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional

from ..config import get_settings
from ..models import JobStatus, PipelineStage, VoiceNote, VoicePipelineResult, STTProvider

logger = logging.getLogger(__name__)


class ArtisanVoiceProcessor:
    """
    Processes an artisan's voice note through the pipeline:
    transcribe → return text ready for the catalog service.
    """

    def __init__(self):
        self.settings = get_settings()

    def process_voice_note(
        self,
        audio_path: str,
        language_code: str = "hi",
        category_hint: Optional[str] = None,
        note_id: Optional[str] = None,
        product_draft_id: Optional[str] = None,
    ) -> VoicePipelineResult:
        """
        Process a single voice note and return a transcript ready for cataloging.

        Args:
            audio_path: Path to the recorded audio file (.m4a, .wav, .mp3).
            language_code: Language the artisan selected before recording.
            category_hint: Craft category, used to prioritise glossary terms.
            note_id: Idempotency key from the client. Generated if absent.
            product_draft_id: Draft this recording belongs to.

        Returns:
            VoicePipelineResult carrying the transcript. Failures are reported
            in the result rather than raised, so a queued job can be retried
            without losing context.
        """
        path = Path(audio_path)
        if not path.exists():
            return VoicePipelineResult(
                voice_note_id=note_id or "error",
                status=JobStatus.FAILED,
                failed_stage=PipelineStage.INGESTION,
                error=f"Audio file not found: {audio_path}",
            )

        note = VoiceNote(
            id=note_id or f"voice-{int(time.time() * 1000)}",
            audio_path=audio_path,
            language_code=language_code,
            product_draft_id=product_draft_id,
        )
        logger.info("Processing voice note %s (lang=%s)", note.id, language_code)

        # ── Step 1: Transcribe via Bhashini ASR ───────────────────────────
        logger.info("Step 1: Transcribing audio with Bhashini ASR...")
        transcript = self._transcribe_with_bhashini(path, language_code)

        if not transcript.is_usable():
            logger.error("Transcription unusable for %s — aborting.", note.id)
            return VoicePipelineResult(
                voice_note_id=note.id,
                status=JobStatus.FAILED,
                transcript=transcript,
                failed_stage=PipelineStage.TRANSCRIPTION,
                error="Transcription failed or returned empty text.",
            )

        result = VoicePipelineResult(
            voice_note_id=note.id,
            status=JobStatus.COMPLETED,
            transcript=transcript,
            elapsed_seconds=0.0,
        )

        logger.info(
            "Pipeline complete for %s: %d characters ready for cataloging",
            note.id,
            len(result.text_for_listing),
        )

        return result

    def process_batch(self, notes: list[dict]) -> list[VoicePipelineResult]:
        """
        Process multiple voice notes.

        Args:
            notes: List of dicts, each with keys:
                   audio_path, language_code (optional), category_hint (optional).

        Returns:
            List of VoicePipelineResult instances, one per input.
        """
        results = []
        for i, note in enumerate(notes):
            logger.info("Processing voice note %d/%d...", i + 1, len(notes))
            results.append(
                self.process_voice_note(
                    audio_path=note["audio_path"],
                    language_code=note.get("language_code", self.settings.default_language),
                    category_hint=note.get("category_hint"),
                    note_id=note.get("id"),
                    product_draft_id=note.get("product_draft_id"),
                )
            )
        return results

    # ── Internals ────────────────────────────────────────────────────────

    def _transcribe_with_bhashini(self, audio_path: Path, language_code: str):
        """
        Transcribe audio using Bhashini ASR via the backend service client.

        Returns a Transcript instance. On failure, returns a non-usable fallback
        transcript so the caller can decide whether to abort.
        """
        from backend.config import get_settings
        from backend.services.bhashini_service import BhashiniConfigError, BhashiniService

        settings = get_settings()
        if not settings.bhashini_api_key or not settings.bhashini_user_id:
            logger.error("Bhashini credentials not configured.")
            return self._failed_transcript(
                language_code=language_code,
                error="Bhashini credentials not configured.",
            )

        try:
            service = BhashiniService(
                api_key=settings.bhashini_api_key,
                user_id=settings.bhashini_user_id,
            )
            audio_bytes = audio_path.read_bytes()
            text = asyncio.run(
                service.transcribe_audio(audio_bytes=audio_bytes, language=language_code)
            )
        except Exception as exc:
            logger.error("Bhashini ASR failed: %s", exc)
            return self._failed_transcript(
                language_code=language_code,
                error=f"Bhashini ASR failed: {exc}",
            )

        if not text or not text.strip():
            return self._failed_transcript(
                language_code=language_code,
                error="No audible speech detected. Please speak closer to the microphone.",
            )

        from ..models import Transcript
        return Transcript(
            text=text.strip(),
            language_code=language_code,
            provider=STTProvider.BHASHINI,
            is_fallback=False,
        )

    def _failed_transcript(self, language_code: str, error: str):
        """Build a non-usable fallback transcript."""
        from ..models import Transcript
        return Transcript(
            text="",
            language_code=language_code,
            provider=STTProvider.BHASHINI,
            is_fallback=True,
        )
