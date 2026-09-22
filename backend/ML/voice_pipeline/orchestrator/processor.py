"""
Artisan Voice Processor.

Processes voice notes through speech-to-text (Whisper) with craft glossary biasing.
"""

import logging
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
        Transcribe a voice note using Whisper STT.

        Args:
            audio_path: Path to the audio file
            language_code: Language code (hi, en, bn, ta, or auto)
            category_hint: Optional craft category for glossary biasing
            note_id: Optional note identifier
            product_draft_id: Optional product draft identifier

        Returns:
            VoicePipelineResult with transcript
        """
        # This is a stub implementation.
        # The actual Whisper model integration would be here.
        logger.warning("[ArtisanVoiceProcessor] Using stub implementation")

        return VoicePipelineResult(
            voice_note_id=note_id or "stub_note",
            status=JobStatus.COMPLETED,
            transcript=Transcript(
                text="",
                language_code=language_code if language_code != "auto" else "en",
                provider=STTProvider.WHISPER,
                duration_seconds=0.0,
                is_fallback=True,
            ),
            elapsed_seconds=0.0,
        )
