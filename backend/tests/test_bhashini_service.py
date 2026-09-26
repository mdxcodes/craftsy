"""
BhashiniService unit and integration tests.

Covers:
- Configuration validation
- Pipeline Config 400 retry
- Compute request structure
- Response parsing
- Error classes
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys_path = str(PROJECT_ROOT)
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from importlib.util import spec_from_file_location, module_from_spec

_spec = spec_from_file_location(
    "bhashini_service",
    str(PROJECT_ROOT / "backend" / "services" / "bhashini_service.py"),
)
_bhashini_service = module_from_spec(_spec)
_spec.loader.exec_module(_bhashini_service)

BhashiniAPIError = _bhashini_service.BhashiniAPIError
BhashiniAuthenticationError = _bhashini_service.BhashiniAuthenticationError
BhashiniConfigError = _bhashini_service.BhashiniConfigError
BhashiniService = _bhashini_service.BhashiniService
BhashiniUnsupportedLanguageError = _bhashini_service.BhashiniUnsupportedLanguageError
DEFAULT_PIPELINE_ID = _bhashini_service.DEFAULT_PIPELINE_ID
ULCA_CONFIG_URL = _bhashini_service.ULCA_CONFIG_URL


def make_service() -> BhashiniService:
    return BhashiniService(
        user_id="test-user",
        ulca_api_key="test-ulca-key",
        inference_api_key="test-inference-key",
        inference_api_key_name="Authorization",
    )


def test_missing_user_id_raises():
    with pytest.raises(BhashiniConfigError):
        BhashiniService(user_id="", ulca_api_key="key")


def test_missing_ulca_key_raises():
    with pytest.raises(BhashiniConfigError):
        BhashiniService(user_id="user", ulca_api_key="")


def test_config_headers():
    service = make_service()
    headers = service._get_config_headers()
    assert headers["userID"] == "test-user"
    assert headers["ulcaApiKey"] == "test-ulca-key"
    assert headers["Content-Type"] == "application/json"


def test_pipeline_config_400_retry():
    service = make_service()

    bad_response = MagicMock()
    bad_response.status_code = 400
    bad_response.text = json.dumps({"message": "Sequence of languages not supported"})
    bad_response.json.return_value = {"message": "Sequence of languages not supported"}

    good_response = MagicMock()
    good_response.status_code = 200
    good_response.text = json.dumps({
        "pipelineInferenceAPIEndPoint": {
            "callbackUrl": "https://example.com",
            "inferenceApiKey": {"name": "Authorization", "value": "xyz"},
        },
        "pipelineResponseConfig": [],
    })
    good_response.json.return_value = {
        "pipelineInferenceAPIEndPoint": {
            "callbackUrl": "https://example.com",
            "inferenceApiKey": {"name": "Authorization", "value": "xyz"},
        },
        "pipelineResponseConfig": [],
    }

    call_count = 0

    async def fake_post(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        return bad_response if call_count == 1 else good_response

    mock_client = MagicMock()
    mock_client.post = fake_post
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch.object(_bhashini_service.httpx, "AsyncClient", return_value=mock_client):
        result = asyncio.run(
            service._get_pipeline_config(
                task_types=["asr"],
                language_configs=[{"language": {"sourceLanguage": "hi"}}],
            )
        )

    assert call_count == 2
    assert result["pipelineInferenceAPIEndPoint"]["callbackUrl"] == "https://example.com"


def test_pipeline_config_400_no_retry_when_no_language_configs():
    service = make_service()

    response = MagicMock()
    response.status_code = 400
    response.text = json.dumps({"message": "Sequence of languages not supported"})
    response.json.return_value = {"message": "Sequence of languages not supported"}

    async def fake_post(*args, **kwargs):
        return response

    mock_client = MagicMock()
    mock_client.post = fake_post
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch.object(_bhashini_service.httpx, "AsyncClient", return_value=mock_client):
        with pytest.raises(BhashiniUnsupportedLanguageError):
            asyncio.run(
                service._get_pipeline_config(
                    task_types=["asr"],
                    language_configs=None,
                )
            )


def test_pipeline_config_401_raises_auth_error():
    service = make_service()

    response = MagicMock()
    response.status_code = 401
    response.text = "Unauthorized"

    async def fake_post(*args, **kwargs):
        return response

    mock_client = MagicMock()
    mock_client.post = fake_post
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch.object(_bhashini_service.httpx, "AsyncClient", return_value=mock_client):
        with pytest.raises(BhashiniAuthenticationError):
            asyncio.run(
                service._get_pipeline_config(
                    task_types=["asr"],
                    language_configs=None,
                )
            )


def test_compute_headers_prefers_dynamic():
    config = {
        "pipelineInferenceAPIEndPoint": {
            "callbackUrl": "https://example.com",
            "inferenceApiKey": {"name": "X-Auth", "value": "dynamic-key"},
        }
    }
    service = make_service()
    headers = service._get_compute_headers(config)
    assert headers["X-Auth"] == "dynamic-key"
    assert headers["Content-Type"] == "application/json"


def test_compute_headers_fallback():
    config = {"pipelineInferenceAPIEndPoint": {}}
    service = make_service()
    headers = service._get_compute_headers(config)
    assert headers["Authorization"] == "test-inference-key"


def test_encode_audio():
    import base64
    service = make_service()
    encoded = service._encode_audio(b"hello")
    assert encoded == base64.b64encode(b"hello").decode("utf-8")


def test_transcribe_audio_payload_structure():
    service = make_service()

    config = {
        "pipelineInferenceAPIEndPoint": {
            "callbackUrl": "https://compute.example.com",
            "inferenceApiKey": {"name": "Authorization", "value": "inf-key"},
        },
        "pipelineResponseConfig": [
            {
                "taskType": "asr",
                "config": [
                    {
                        "serviceId": "test-service",
                        "language": {"sourceLanguage": "hi"},
                    }
                ],
            }
        ],
    }

    compute_response = MagicMock()
    compute_response.status_code = 200
    compute_response.json.return_value = {
        "pipelineResponse": [
            {
                "taskType": "asr",
                "output": [{"source": "नमस्ते"}],
            }
        ]
    }

    mock_post = AsyncMock(return_value=compute_response)
    mock_client = MagicMock()
    mock_client.post = mock_post
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch.object(service, "_get_pipeline_config", new_callable=AsyncMock, return_value=config):
        with patch.object(_bhashini_service.httpx, "AsyncClient", return_value=mock_client):
            transcript = asyncio.run(
                service.transcribe_audio(
                    audio_bytes=b"fake-audio-bytes",
                    language="hi",
                )
            )

    assert transcript == "नमस्ते"
    sent_payload = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1].get("json")
    assert sent_payload["pipelineTasks"][0]["taskType"] == "asr"
    assert sent_payload["inputData"]["input"][0]["source"] is None


def test_transcribe_empty_output_returns_empty():
    service = make_service()

    config = {
        "pipelineInferenceAPIEndPoint": {
            "callbackUrl": "https://compute.example.com",
            "inferenceApiKey": {"name": "Authorization", "value": "inf-key"},
        },
        "pipelineResponseConfig": [
            {
                "taskType": "asr",
                "config": [{"serviceId": "svc", "language": {"sourceLanguage": "hi"}}],
            }
        ],
    }

    compute_response = MagicMock()
    compute_response.status_code = 200
    compute_response.json.return_value = {
        "pipelineResponse": [
            {
                "taskType": "asr",
                "output": [{"source": "   "}],
            }
        ]
    }

    mock_post = AsyncMock(return_value=compute_response)
    mock_client = MagicMock()
    mock_client.post = mock_post
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch.object(service, "_get_pipeline_config", new_callable=AsyncMock, return_value=config):
        with patch.object(_bhashini_service.httpx, "AsyncClient", return_value=mock_client):
            transcript = asyncio.run(
                service.transcribe_audio(audio_bytes=b"fake", language="hi")
            )

    assert transcript == "   "


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
