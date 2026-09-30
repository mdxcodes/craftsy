"""
Shared Groq Client Utility.

Provides asynchronous, resilient chat completions via Groq Cloud REST API
(OpenAI-compatible) using httpx.
Includes regex-based reasoning tag removal (<think>...</think>), markdown fence
stripping, and automatic JSON extraction.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, List, Optional
import httpx

from ..config import get_settings

logger = logging.getLogger(__name__)

# Pattern to strip out thinking/reasoning blocks (e.g., from deepseek/qwen reasoning models)
THINKING_PATTERN = re.compile(r"<think>.*?</think>", re.DOTALL)


class GroqClient:
    """Lightweight async client for Groq Cloud chat completions."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.settings = get_settings()
        self.api_key = api_key or self.settings.get_active_groq_key()
        self.base_url = (base_url or self.settings.groq_base_url).rstrip("/")
        self.default_model = self.settings.groq_chat_model

    def is_available(self) -> bool:
        """Check whether an active Groq API key is present."""
        return bool(self.api_key and self.api_key.startswith("gsk_"))

    @staticmethod
    def clean_response_text(raw_text: str) -> str:
        """Strip reasoning tags, extra whitespace, and markdown formatting."""
        if not raw_text:
            return ""
        # 1. Remove <think>...</think> blocks
        cleaned = THINKING_PATTERN.sub("", raw_text).strip()
        return cleaned

    @staticmethod
    def normalize_ai_error(exc: Exception) -> str:
        """Map provider exceptions to normalized error codes."""
        error_str = str(exc).lower()
        if "429" in error_str or "resource_exhausted" in error_str or "rate limit" in error_str:
            return "AI_RATE_LIMITED"
        if "404" in error_str or "model_not_found" in error_str:
            return "AI_MODEL_UNAVAILABLE"
        if "503" in error_str or "unavailable" in error_str or "service_unavailable" in error_str:
            return "AI_PROVIDER_UNAVAILABLE"
        if "400" in error_str or "invalid" in error_str or "validation" in error_str:
            return "AI_INVALID_RESPONSE"
        return "AI_GENERATION_FAILED"

    @staticmethod
    def extract_json_payload(text: str) -> Dict[str, Any]:
        """Extract and parse a JSON dictionary from LLM response text."""
        cleaned = GroqClient.clean_response_text(text)
        
        # 1. Check for markdown code fence ```json ... ```
        fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
        if fence_match:
            candidate = fence_match.group(1).strip()
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass

        # 2. Check for outermost { ... }
        brace_match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
        if brace_match:
            candidate = brace_match.group(1).strip()
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass

        # 3. Direct parse
        return json.loads(cleaned)

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1024,
        response_format_json: bool = False,
        timeout: float = 20.0,
    ) -> str:
        """
        Send a chat completion request to Groq Cloud.
        Returns the raw string output from the model.
        """
        if not self.is_available():
            raise RuntimeError("Groq API key is not configured. Set GROQ_API_KEY in .env.")

        active_model = model or self.settings.groq_model_primary or self.settings.groq_chat_model
        fallback_models = [
            m for m in [
                self.settings.groq_model_fallback,
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
            ]
            if m and m != active_model
        ]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload: Dict[str, Any] = {
            "model": active_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if response_format_json:
            payload["response_format"] = {"type": "json_object"}

        models_to_try = [active_model] + fallback_models

        async with httpx.AsyncClient(timeout=timeout) as client:
            last_error: Optional[Exception] = None

            for attempt_model in models_to_try:
                payload["model"] = attempt_model
                try:
                    url = f"{self.base_url}/chat/completions"
                    resp = await client.post(url, headers=headers, json=payload)
                    
                    if resp.status_code == 200:
                        data = resp.json()
                        choices = data.get("choices", [])
                        if choices:
                            raw_content = choices[0].get("message", {}).get("content", "")
                            return self.clean_response_text(raw_content)
                        raise RuntimeError("Groq returned empty choices list.")

                    error_data = resp.text
                    error_code = self.normalize_ai_error(
                        RuntimeError(f"Groq API error ({resp.status_code}): {error_data}")
                    )
                    logger.warning(
                        "[GroqClient] Model '%s' returned status %s (%s): %s",
                        attempt_model,
                        resp.status_code,
                        error_code,
                        error_data[:200],
                    )
                    last_error = RuntimeError(f"Groq API error ({resp.status_code}): {error_data}")
                    
                    # Do NOT retry non-retryable errors
                    if error_code in ("AI_MODEL_UNAVAILABLE", "AI_RATE_LIMITED"):
                        break
                    # For transient server errors, retry with next fallback
                    if resp.status_code in (500, 502, 503) and attempt_model != models_to_try[-1]:
                        continue
                    # For 400/404 on non-primary, try next; on primary, break
                    if resp.status_code in (400, 404) and attempt_model != models_to_try[-1]:
                        continue
                    break

                except Exception as e:
                    error_code = self.normalize_ai_error(e)
                    logger.warning("[GroqClient] Request to '%s' failed (%s): %s", attempt_model, error_code, e)
                    last_error = e
                    if error_code in ("AI_MODEL_UNAVAILABLE", "AI_RATE_LIMITED"):
                        break

            raise last_error or RuntimeError("All Groq model attempts failed.")

    async def chat_json(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> Dict[str, Any]:
        """
        Send a chat completion and parse the output directly as a JSON dict.
        """
        raw_text = await self.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format_json=True,
        )
        try:
            return self.extract_json_payload(raw_text)
        except Exception as e:
            logger.error("[GroqClient] Failed to parse JSON from text: %r (error: %s)", raw_text, e)
            raise RuntimeError(f"Failed to parse structured JSON from Groq output: {e}") from e

    def chat_completion_sync(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 800,
        response_format_json: bool = False,
        timeout: float = 20.0,
    ) -> str:
        """Synchronous chat completion for non-async ML pipeline modules."""
        if not self.is_available():
            raise RuntimeError("Groq API key is not configured.")

        active_model = model or self.settings.groq_model_primary or self.settings.groq_chat_model
        fallback_models = [
            m for m in [
                self.settings.groq_model_fallback,
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
            ]
            if m and m != active_model
        ]
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": active_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if response_format_json:
            payload["response_format"] = {"type": "json_object"}

        models_to_try = [active_model] + fallback_models

        with httpx.Client(timeout=timeout) as client:
            last_error: Optional[Exception] = None
            for attempt_model in models_to_try:
                payload["model"] = attempt_model
                try:
                    url = f"{self.base_url}/chat/completions"
                    resp = client.post(url, headers=headers, json=payload)
                    if resp.status_code == 200:
                        choices = resp.json().get("choices", [])
                        if choices:
                            raw_content = choices[0].get("message", {}).get("content", "")
                            return self.clean_response_text(raw_content)
                    error_code = self.normalize_ai_error(
                        RuntimeError(f"Groq API error ({resp.status_code}): {resp.text}")
                    )
                    logger.warning(
                        "[GroqClient] Sync model '%s' returned status %s (%s): %s",
                        attempt_model,
                        resp.status_code,
                        error_code,
                        resp.text[:200],
                    )
                    last_error = RuntimeError(f"Groq API error ({resp.status_code}): {resp.text}")
                    if error_code in ("AI_MODEL_UNAVAILABLE", "AI_RATE_LIMITED"):
                        break
                    if resp.status_code in (500, 502, 503) and attempt_model != models_to_try[-1]:
                        continue
                    if resp.status_code in (400, 404) and attempt_model != models_to_try[-1]:
                        continue
                    break
                except Exception as e:
                    error_code = self.normalize_ai_error(e)
                    logger.warning("[GroqClient] Sync request to '%s' failed (%s): %s", attempt_model, error_code, e)
                    last_error = e
                    if error_code in ("AI_MODEL_UNAVAILABLE", "AI_RATE_LIMITED"):
                        break
            raise last_error or RuntimeError("All Groq sync model attempts failed.")

    def chat_json_sync(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> Dict[str, Any]:
        """Synchronous JSON chat completion for ML pricer."""
        raw_text = self.chat_completion_sync(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format_json=True,
        )
        return self.extract_json_payload(raw_text)
