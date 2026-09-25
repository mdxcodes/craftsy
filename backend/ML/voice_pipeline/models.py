"""Voice Pipeline Models."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class STTProvider(str, Enum):
    WHISPER = "whisper"
    GOOGLE = "google"
    GROQ = "groq"
    BHASHINI = "bhashini"


@dataclass
class Transcript:
    text: str = ""
    language_code: str = "en"
    provider: STTProvider = STTProvider.WHISPER
    duration_seconds: float = 0.0
    is_fallback: bool = False

    def is_usable(self) -> bool:
        return bool(self.text and self.text.strip())


@dataclass
class VoicePipelineResult:
    voice_note_id: str = ""
    status: JobStatus = JobStatus.PENDING
    transcript: Transcript = field(default_factory=Transcript)
    elapsed_seconds: float = 0.0
    error: Optional[str] = None
