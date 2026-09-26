"""
Bhashini language capability registry.

Maps ISO-639 language codes to available Bhashini services for:
- ASR
- Translation (to/from English and other major languages)
- TTS
- Transliteration
- Language Detection

Data sourced from the official Bhashini GitBook documentation and
verified against live Pipeline Config responses.

Status:
    documented: listed in official Bhashini documentation
    configured: present in Craftsy's Bhashini service
    tested: verified with real audio/API calls
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BhashiniCapability:
    """Capability information for a single language."""
    code: str
    name: str
    native_name: str
    asr: bool = False
    asr_service: Optional[str] = None
    translation_to_en: bool = False
    translation_from_en: bool = False
    tts: bool = False
    tts_service: Optional[str] = None
    transliteration: bool = False
    language_detection: bool = False
    documented: bool = False
    configured: bool = False
    tested: bool = False


# Registry of Bhashini-supported languages.
# Service IDs are from the official Bhashini GitBook documentation.
BHASHINI_LANGUAGE_REGISTRY: dict[str, BhashiniCapability] = {
    # ---- Indo-Aryan languages ----
    "hi": BhashiniCapability(
        code="hi",
        name="Hindi",
        native_name="हिन्दी",
        asr=True,
        asr_service="ai4bharat/conformer-hi-gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        tts_service="ai4bharat/tts-hi-gpu--t4",
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=True,
        tested=True,
    ),
    "en": BhashiniCapability(
        code="en",
        name="English",
        native_name="English",
        asr=True,
        asr_service="ai4bharat/whisper-medium-en--gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        tts_service="ai4bharat/tts-en-gpu--t4",
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=True,
        tested=False,
    ),
    "mr": BhashiniCapability(
        code="mr",
        name="Marathi",
        native_name="मराठी",
        asr=True,
        asr_service="ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "gu": BhashiniCapability(
        code="gu",
        name="Gujarati",
        native_name="ગુજરાતી",
        asr=True,
        asr_service="ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "pa": BhashiniCapability(
        code="pa",
        name="Punjabi",
        native_name="ਪੰਜਾਬੀ",
        asr=True,
        asr_service="ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "or": BhashiniCapability(
        code="or",
        name="Odia",
        native_name="ଓଡ଼ିଆ",
        asr=True,
        asr_service="ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "bn": BhashiniCapability(
        code="bn",
        name="Bengali",
        native_name="বাংলা",
        asr=True,
        asr_service="ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=True,
        tested=False,
    ),
    "as": BhashiniCapability(
        code="as",
        name="Assamese",
        native_name="অসমীয়া",
        asr=True,
        asr_service="ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "ur": BhashiniCapability(
        code="ur",
        name="Urdu",
        native_name="اردو",
        asr=True,
        asr_service="ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "ne": BhashiniCapability(
        code="ne",
        name="Nepali",
        native_name="नेपाली",
        asr=True,
        asr_service="ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "sa": BhashiniCapability(
        code="sa",
        name="Sanskrit",
        native_name="संस्कृतम्",
        asr=True,
        asr_service="ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    # ---- Dravidian languages ----
    "ta": BhashiniCapability(
        code="ta",
        name="Tamil",
        native_name="தமிழ்",
        asr=True,
        asr_service="ai4bharat/conformer-multilingual-dravidian-gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=True,
        tested=False,
    ),
    "te": BhashiniCapability(
        code="te",
        name="Telugu",
        native_name="తెలుగు",
        asr=True,
        asr_service="ai4bharat/conformer-multilingual-dravidian-gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "kn": BhashiniCapability(
        code="kn",
        name="Kannada",
        native_name="ಕನ್ನಡ",
        asr=True,
        asr_service="ai4bharat/conformer-multilingual-dravidian-gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "ml": BhashiniCapability(
        code="ml",
        name="Malayalam",
        native_name="മലയാളം",
        asr=True,
        asr_service="ai4bharat/conformer-multilingual-dravidian-gpu--t4",
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    # ---- Other documented languages ----
    "mai": BhashiniCapability(
        code="mai",
        name="Maithili",
        native_name="मैथिली",
        asr=True,
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "mni": BhashiniCapability(
        code="mni",
        name="Manipuri",
        native_name="ꯃꯤꯇꯩꯂꯣꯟ",
        asr=True,
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "brx": BhashiniCapability(
        code="brx",
        name="Bodo",
        native_name="बड़ो",
        asr=True,
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "doi": BhashiniCapability(
        code="doi",
        name="Dogri",
        native_name="डोगरी",
        asr=True,
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "sat": BhashiniCapability(
        code="sat",
        name="Santali",
        native_name="ᱥᱟᱱᱛᱟᱲᱤ",
        asr=True,
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "ks": BhashiniCapability(
        code="ks",
        name="Kashmiri",
        native_name="कॉशुर",
        asr=True,
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "gom": BhashiniCapability(
        code="gom",
        name="Konkani",
        native_name="कोंकणी",
        asr=True,
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "bho": BhashiniCapability(
        code="bho",
        name="Bhojpuri",
        native_name="भोजपुरी",
        asr=True,
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
    "sd": BhashiniCapability(
        code="sd",
        name="Sindhi",
        native_name="सिन्धी",
        asr=True,
        translation_to_en=True,
        translation_from_en=True,
        tts=True,
        transliteration=True,
        language_detection=True,
        documented=True,
        configured=False,
        tested=False,
    ),
}


def get_capability(language_code: str) -> Optional[BhashiniCapability]:
    """Get capability information for a language."""
    return BHASHINI_LANGUAGE_REGISTRY.get(language_code.lower())


def get_supported_languages(task: str = "asr") -> list[BhashiniCapability]:
    """Get all languages that support a specific task."""
    task_map = {
        "asr": "asr",
        "translation": "translation_to_en",
        "tts": "tts",
        "transliteration": "transliteration",
        "language_detection": "language_detection",
    }
    attr = task_map.get(task, "asr")
    return [
        cap for cap in BHASHINI_LANGUAGE_REGISTRY.values()
        if getattr(cap, attr, False)
    ]


def get_tested_languages() -> list[BhashiniCapability]:
    """Get all languages that have been tested with real audio."""
    return [cap for cap in BHASHINI_LANGUAGE_REGISTRY.values() if cap.tested]


def get_configured_languages() -> list[BhashiniCapability]:
    """Get all languages that are configured in Craftsy's Bhashini service."""
    return [cap for cap in BHASHINI_LANGUAGE_REGISTRY.values() if cap.configured]
