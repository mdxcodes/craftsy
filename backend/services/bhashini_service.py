"""
Bhashini Language API Client (ULCA Pipeline).

Implements the real Bhashini ULCA pipeline flow:
  1. Pipeline Config Call  → obtain service IDs + callback URL + auth headers
  2. Pipeline Compute Call → send audio/text and receive inference results

Reference:
    https://dibd-bhashini.gitbook.io/bhashini-apis

Architecture:
    Flutter App → Craftsy Backend (this module) → Bhashini ULCA API
"""

from __future__ import annotations

import base64
import logging
from typing import Any, Dict, List, Optional

import httpx

logger = logging.getLogger(__name__)

# Default pipeline IDs that support ASR, NMT, TTS.
# Source: https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-search-call
DEFAULT_PIPELINE_ID = "64392f96daac500b55c543cd"

# Bhashini ULCA config endpoint (Pipeline Config Call).
ULCA_CONFIG_URL = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

# Task type constants.
TASK_ASR = "asr"
TASK_TRANSLATION = "translation"
TASK_TTS = "tts"


class BhashiniConfigError(Exception):
    """Raised when Bhashini credentials are missing or invalid."""


class BhashiniAPIError(Exception):
    """Raised when Bhashini API returns an error response."""


class BhashiniService:
    """Centralized client for Bhashini ULCA pipeline APIs.

    Usage:
        service = BhashiniService(api_key="...", user_id="...")
        transcript = await service.transcribe_audio(audio_bytes, language="hi")
        translated = await service.translate_text(text, source="hi", target="en")
        audio_bytes = await service.synthesize_speech(text, language="hi")
    """

    def __init__(
        self,
        api_key: str,
        user_id: str,
        pipeline_id: str = DEFAULT_PIPELINE_ID,
        timeout: float = 60.0,
    ) -> None:
        if not api_key or not user_id:
            raise BhashiniConfigError(
                "Bhashini API key and user ID are required. "
                "Set BHASHINI_API_KEY and BHASHINI_USER_ID environment variables."
            )
        self._api_key = api_key
        self._user_id = user_id
        self._pipeline_id = pipeline_id
        self._timeout = timeout
        self._config_cache: Optional[Dict[str, Any]] = None

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _get_config_headers(self) -> Dict[str, str]:
        """Headers for Pipeline Config Call."""
        headers = {
            "userID": self._user_id,
            "ulcaApiKey": "***REDACTED***",
            "Content-Type": "application/json",
        }
        logger.info(
            "Bhashini config request headers: userID=%s, ulcaApiKey=%s",
            self._user_id[:8] + "..." if self._user_id else "",
            "***REDACTED***",
        )
        return {
            "userID": self._user_id,
            "ulcaApiKey": self._api_key,
            "Content-Type": "application/json",
        }

    async def _get_pipeline_config(
        self,
        task_types: List[str],
        language_configs: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Call Pipeline Config API and return parsed config.

        Args:
            task_types: List of task types, e.g. ["asr"], ["translation"], ["tts"],
                        or ["asr", "translation"], etc.
            language_configs: Optional per-task language configs. If provided,
                        must match the length of task_types.

        Returns:
            Parsed config dict containing:
                - pipelineResponseConfig: service IDs per task
                - pipelineInferenceAPIEndPoint: callback URL + auth key
                - languages: supported languages
        """
        pipeline_tasks: List[Dict[str, Any]] = []
        for idx, task_type in enumerate(task_types):
            task: Dict[str, Any] = {"taskType": task_type}
            if language_configs and idx < len(language_configs):
                task["config"] = language_configs[idx]
            pipeline_tasks.append(task)

        payload: Dict[str, Any] = {
            "pipelineTasks": pipeline_tasks,
            "pipelineRequestConfig": {"pipelineId": self._pipeline_id},
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            logger.debug(
                "Bhashini config request: url=%s, task_types=%s, language=%s",
                ULCA_CONFIG_URL,
                task_types,
                language_configs,
            )
            response = await client.post(
                ULCA_CONFIG_URL,
                headers=self._get_config_headers(),
                json=payload,
            )
            logger.debug(
                "Bhashini config response: status=%s, body=%s",
                response.status_code,
                response.text[:500],
            )
            response.raise_for_status()
            data = response.json()

        # Validate response structure.
        if "pipelineInferenceAPIEndPoint" not in data:
            raise BhashiniAPIError(
                f"Unexpected Bhashini config response: missing pipelineInferenceAPIEndPoint. "
                f"Response keys: {list(data.keys())}"
            )

        self._config_cache = data
        return data

    def _get_compute_headers(self, config: Dict[str, Any]) -> Dict[str, str]:
        """Extract auth headers for Pipeline Compute Call from config response."""
        endpoint = config.get("pipelineInferenceAPIEndPoint", {})
        inference_api_key = endpoint.get("inferenceApiKey", {})
        auth_name = inference_api_key.get("name", "Authorization")
        auth_value = inference_api_key.get("value", "")
        return {
            auth_name: auth_value,
            "Content-Type": "application/json",
        }

    def _get_compute_url(self, config: Dict[str, Any]) -> str:
        """Extract callback URL for Pipeline Compute Call from config response."""
        endpoint = config.get("pipelineInferenceAPIEndPoint", {})
        callback_url = endpoint.get("callbackUrl", "")
        if not callback_url:
            raise BhashiniAPIError(
                "Bhashini config response missing callbackUrl. "
                "Cannot determine compute endpoint."
            )
        return callback_url

    @staticmethod
    def _encode_audio(audio_bytes: bytes) -> str:
        """Encode raw audio bytes to base64 string for Bhashini API."""
        return base64.b64encode(audio_bytes).decode("utf-8")

    # ── Public API ───────────────────────────────────────────────────────────

    async def transcribe_audio(
        self,
        audio_bytes: bytes,
        language: str = "hi",
        audio_format: str = "wav",
        sampling_rate: int = 16000,
    ) -> str:
        """Transcribe audio using Bhashini ASR.

        Args:
            audio_bytes: Raw audio file bytes.
            language: ISO-639 language code (e.g. "hi", "en", "bn").
            audio_format: Audio format string (e.g. "wav", "mp3", "flac").
            sampling_rate: Audio sampling rate in Hz (minimum 8000).

        Returns:
            Transcribed text string.

        Raises:
            BhashiniConfigError: If credentials are missing.
            BhashiniAPIError: If Bhashini returns an error response.
        """
        if not self._api_key or not self._user_id:
            raise BhashiniConfigError("Bhashini credentials not configured.")

        # Step 1: Get pipeline config for ASR.
        config = await self._get_pipeline_config(
            task_types=[TASK_ASR],
            language_configs=[
                {"language": {"sourceLanguage": language}}
            ],
        )

        # Find ASR service config.
        response_configs = config.get("pipelineResponseConfig", [])
        asr_config = None
        for rc in response_configs:
            if rc.get("taskType") == TASK_ASR:
                asr_configs = rc.get("config", [])
                # Find matching language.
                for ac in asr_configs:
                    lang_info = ac.get("language", {})
                    if lang_info.get("sourceLanguage") == language:
                        asr_config = ac
                        break
                if asr_config is None and asr_configs:
                    # Fallback to first available ASR config.
                    asr_config = asr_configs[0]
                break

        if not asr_config:
            raise BhashiniAPIError(
                f"No ASR service configured for language '{language}'. "
                f"Available languages: {config.get('languages', [])}"
            )

        # Step 2: Build compute payload.
        service_id = asr_config.get("serviceId", "")
        compute_payload = {
            "pipelineTasks": [
                {
                    "taskType": TASK_ASR,
                    "config": {
                        "language": {"sourceLanguage": language},
                        "serviceId": service_id,
                        "audioFormat": audio_format,
                        "samplingRate": sampling_rate,
                    },
                }
            ],
            "inputData": {
                "input": [{"source": ""}],
                "audio": [
                    {"audioContent": self._encode_audio(audio_bytes)}
                ],
            },
        }

        # Step 3: Call compute endpoint.
        headers = self._get_compute_headers(config)
        compute_url = self._get_compute_url(config)

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                compute_url,
                headers=headers,
                json=compute_payload,
            )
            response.raise_for_status()
            result = response.json()

        # Parse ASR result.
        pipeline_response = result.get("pipelineResponse", [])
        for step in pipeline_response:
            if step.get("taskType") == TASK_ASR:
                output = step.get("output", [])
                if output:
                    return output[0].get("source", "")
                break

        raise BhashiniAPIError(
            f"Bhashini ASR response missing output. Response: {result}"
        )

    async def translate_text(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:
        """Translate text using Bhashini NMT.

        Args:
            text: Source text to translate.
            source_language: ISO-639 source language code.
            target_language: ISO-639 target language code.

        Returns:
            Translated text string.

        Raises:
            BhashiniConfigError: If credentials are missing.
            BhashiniAPIError: If Bhashini returns an error response.
        """
        if not self._api_key or not self._user_id:
            raise BhashiniConfigError("Bhashini credentials not configured.")

        # Step 1: Get pipeline config for translation.
        config = await self._get_pipeline_config(
            task_types=[TASK_TRANSLATION],
            language_configs=[
                {
                    "language": {
                        "sourceLanguage": source_language,
                        "targetLanguage": target_language,
                    }
                }
            ],
        )

        # Find translation service config.
        response_configs = config.get("pipelineResponseConfig", [])
        translation_config = None
        for rc in response_configs:
            if rc.get("taskType") == TASK_TRANSLATION:
                configs = rc.get("config", [])
                for tc in configs:
                    lang_info = tc.get("language", {})
                    if (lang_info.get("sourceLanguage") == source_language and
                            lang_info.get("targetLanguage") == target_language):
                        translation_config = tc
                        break
                if translation_config is None and configs:
                    translation_config = configs[0]
                break

        if not translation_config:
            raise BhashiniAPIError(
                f"No translation service configured for "
                f"'{source_language}' → '{target_language}'. "
                f"Available languages: {config.get('languages', [])}"
            )

        # Step 2: Build compute payload.
        service_id = translation_config.get("serviceId", "")
        compute_payload = {
            "pipelineTasks": [
                {
                    "taskType": TASK_TRANSLATION,
                    "config": {
                        "language": {
                            "sourceLanguage": source_language,
                            "targetLanguage": target_language,
                        },
                        "serviceId": service_id,
                    },
                }
            ],
            "inputData": {
                "input": [{"source": text}],
                "audio": [{"audioContent": None}],
            },
        }

        # Step 3: Call compute endpoint.
        headers = self._get_compute_headers(config)
        compute_url = self._get_compute_url(config)

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                compute_url,
                headers=headers,
                json=compute_payload,
            )
            response.raise_for_status()
            result = response.json()

        # Parse translation result.
        pipeline_response = result.get("pipelineResponse", [])
        for step in pipeline_response:
            if step.get("taskType") == TASK_TRANSLATION:
                output = step.get("output", [])
                if output:
                    # Translation returns both source and target.
                    return output[0].get("target", "")
                break

        raise BhashiniAPIError(
            f"Bhashini translation response missing output. Response: {result}"
        )

    async def synthesize_speech(
        self,
        text: str,
        language: str = "hi",
        gender: str = "female",
        speed: float = 1.0,
        sampling_rate: int = 22050,
    ) -> bytes:
        """Synthesize speech using Bhashini TTS.

        Args:
            text: Text to synthesize.
            language: ISO-639 language code.
            gender: Voice gender ("male" or "female").
            speed: Speech speed (0.1 to 1.99).
            sampling_rate: Output audio sampling rate in Hz.

        Returns:
            Raw audio bytes (WAV format).

        Raises:
            BhashiniConfigError: If credentials are missing.
            BhashiniAPIError: If Bhashini returns an error response.
        """
        if not self._api_key or not self._user_id:
            raise BhashiniConfigError("Bhashini credentials not configured.")

        # Step 1: Get pipeline config for TTS.
        config = await self._get_pipeline_config(
            task_types=[TASK_TTS],
            language_configs=[
                {"language": {"sourceLanguage": language}}
            ],
        )

        # Find TTS service config.
        response_configs = config.get("pipelineResponseConfig", [])
        tts_config = None
        for rc in response_configs:
            if rc.get("taskType") == TASK_TTS:
                configs = rc.get("config", [])
                for tc in configs:
                    lang_info = tc.get("language", {})
                    if lang_info.get("sourceLanguage") == language:
                        tts_config = tc
                        break
                if tts_config is None and configs:
                    tts_config = configs[0]
                break

        if not tts_config:
            raise BhashiniAPIError(
                f"No TTS service configured for language '{language}'. "
                f"Available languages: {config.get('languages', [])}"
            )

        # Step 2: Build compute payload.
        service_id = tts_config.get("serviceId", "")
        compute_payload = {
            "pipelineTasks": [
                {
                    "taskType": TASK_TTS,
                    "config": {
                        "language": {"sourceLanguage": language},
                        "serviceId": service_id,
                        "gender": gender,
                        "speed": speed,
                        "samplingRate": sampling_rate,
                    },
                }
            ],
            "inputData": {
                "input": [{"source": text}],
                "audio": [{"audioContent": None}],
            },
        }

        # Step 3: Call compute endpoint.
        headers = self._get_compute_headers(config)
        compute_url = self._get_compute_url(config)

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                compute_url,
                headers=headers,
                json=compute_payload,
            )
            response.raise_for_status()
            result = response.json()

        # Parse TTS result - audio is base64 encoded.
        pipeline_response = result.get("pipelineResponse", [])
        for step in pipeline_response:
            if step.get("taskType") == TASK_TTS:
                audio_list = step.get("audio", [])
                if audio_list:
                    audio_content = audio_list[0].get("audioContent", "")
                    if audio_content:
                        return base64.b64decode(audio_content)
                break

        raise BhashiniAPIError(
            f"Bhashini TTS response missing audio. Response: {result}"
        )
