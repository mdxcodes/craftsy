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


class BhashiniAuthenticationError(Exception):
    """Raised when Bhashini rejects Pipeline Config credentials."""


class BhashiniUnsupportedLanguageError(Exception):
    """Raised when the requested language is not supported by the pipeline."""


class BhashiniUnsupportedServiceError(Exception):
    """Raised when no service is available for the requested task/language."""


class BhashiniAudioFormatError(Exception):
    """Raised when audio format/sampling rate is invalid."""


class BhashiniAPIError(Exception):
    """Raised when Bhashini API returns an error response."""


class BhashiniService:
    """Centralized client for Bhashini ULCA pipeline APIs.

    Usage:
        service = BhashiniService(
            user_id="...",
            ulca_api_key="...",         # for Pipeline Config
            inference_api_key="...",    # fallback for compute auth
            inference_api_key_name="Authorization",
        )
        transcript = await service.transcribe_audio(audio_bytes, language="hi")
        translated = await service.translate_text(text, source="hi", target="en")
        audio_bytes = await service.synthesize_speech(text, language="hi")
    """

    def __init__(
        self,
        user_id: str,
        ulca_api_key: str,
        inference_api_key: str = "",
        inference_api_key_name: str = "Authorization",
        pipeline_id: str = DEFAULT_PIPELINE_ID,
        timeout: float = 60.0,
    ) -> None:
        if not user_id or not ulca_api_key:
            raise BhashiniConfigError(
                "Bhashini User ID and ULCA API key are required. "
                "Set BHASHINI_USER_ID and BHASHINI_ULCA_API_KEY environment variables."
            )
        self._user_id = user_id
        self._ulca_api_key = ulca_api_key
        self._inference_api_key = inference_api_key
        self._inference_api_key_name = inference_api_key_name
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
            "ulcaApiKey": self._ulca_api_key,
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

            if response.status_code == 400:
                body = response.text
                logger.warning(
                    "Bhashini Pipeline Config 400: status=%s, body=%s",
                    response.status_code,
                    body[:500],
                )
                try:
                    error_data = response.json()
                except Exception:
                    error_data = {"message": body[:500]}

                message = error_data.get("message", "")
                if message == "Sequence of languages not supported" and language_configs:
                    logger.info(
                        "Retrying Pipeline Config without language configs "
                        "to discover supported languages."
                    )
                    return await self._get_pipeline_config(
                        task_types=task_types,
                        language_configs=None,
                    )

                raise BhashiniUnsupportedLanguageError(
                    f"Bhashini Pipeline Config failed with unsupported language/sequence. "
                    f"status=400 message={message}"
                )

            if response.status_code == 401:
                raise BhashiniAuthenticationError(
                    "Bhashini Pipeline Config authentication failed. "
                    "Verify BHASHINI_USER_ID and BHASHINI_ULCA_API_KEY."
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
        """Extract auth headers for Pipeline Compute Call from config response.

        Prefers the dynamically returned inferenceApiKey from the Pipeline Config
        response. Falls back to environment-provided values if the response does
        not supply them.
        """
        endpoint = config.get("pipelineInferenceAPIEndPoint", {})
        inference_api_key = endpoint.get("inferenceApiKey", {})
        auth_name = inference_api_key.get("name") or self._inference_api_key_name
        auth_value = inference_api_key.get("value") or self._inference_api_key
        return {
            auth_name: auth_value,
            "Content-Type": "application/json",
        }

    async def _post_compute(
        self,
        config: Dict[str, Any],
        payload: Dict[str, Any],
        task_label: str,
    ) -> Dict[str, Any]:
        """Send a Pipeline Compute request and return parsed JSON.

        Raises structured Bhashini errors with safe logging.
        """
        headers = self._get_compute_headers(config)
        compute_url = self._get_compute_url(config)

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            logger.info(
                "Bhashini %s compute request: url=%s",
                task_label,
                compute_url,
            )
            response = await client.post(
                compute_url,
                headers=headers,
                json=payload,
            )
            logger.info(
                "Bhashini %s compute response: status=%s, content_type=%s",
                task_label,
                response.status_code,
                response.headers.get("content-type"),
            )

            if response.status_code == 400:
                raise BhashiniAPIError(
                    f"Bhashini {task_label} compute failed with 400. "
                    f"body={response.text[:500]}"
                )
            if response.status_code == 401:
                raise BhashiniAuthenticationError(
                    f"Bhashini {task_label} compute authentication failed. "
                    f"Verify inference API key."
                )
            response.raise_for_status()
            return response.json()

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
        if not self._ulca_api_key or not self._user_id:
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
                "input": [{"source": None}],
                "audio": [
                    {"audioContent": self._encode_audio(audio_bytes)}
                ],
            },
        }

        # Step 3: Call compute endpoint.
        result = await self._post_compute(
            config=config,
            payload=compute_payload,
            task_label="ASR",
        )

        # Parse ASR result.
        pipeline_response = result.get("pipelineResponse", [])
        for step in pipeline_response:
            if step.get("taskType") == TASK_ASR:
                output = step.get("output", [])
                if output:
                    transcript = output[0].get("source", "")
                    logger.info(
                        "Bhashini ASR transcript extracted: len=%d",
                        len(transcript),
                    )
                    return transcript
                break

        logger.error(
            "Bhashini ASR response missing output. Response keys: %s",
            list(result.keys()) if isinstance(result, dict) else type(result).__name__,
        )
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
        if not self._ulca_api_key or not self._user_id:
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
        result = await self._post_compute(
            config=config,
            payload=compute_payload,
            task_label="Translation",
        )

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
        if not self._ulca_api_key or not self._user_id:
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
        result = await self._post_compute(
            config=config,
            payload=compute_payload,
            task_label="TTS",
        )

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
