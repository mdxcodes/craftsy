"""
Vector store and Chroma configuration tests.

Covers:
- Cloud mode missing credentials
- Local mode initialization
- Collection name consistency
- No secrets in logs
"""

from __future__ import annotations

import logging
from unittest.mock import MagicMock, patch

import pytest

from ML.pricing.config import Settings, get_settings
from ML.pricing.embeddings.vector_store import VectorStore


def _set_chroma_env(monkeypatch, mode="cloud", **overrides):
    """Helper to set Chroma-related env vars for tests."""
    env = {
        "CHROMA_MODE": mode,
        "CHROMA_API_KEY": overrides.get("api_key", ""),
        "CHROMA_TENANT": overrides.get("tenant", ""),
        "CHROMA_DATABASE": overrides.get("database", ""),
        "CHROMADB_PATH": overrides.get("path", "/tmp/test_chroma"),
        "CHROMADB_COLLECTION": overrides.get("collection", "benchmark_products"),
    }
    for key, value in env.items():
        monkeypatch.setenv(key, value)


def test_cloud_mode_missing_api_key_raises(monkeypatch):
    """Cloud mode without CHROMA_API_KEY should fail clearly."""
    _set_chroma_env(monkeypatch, mode="cloud", api_key="", tenant="t", database="d")
    with pytest.raises(ValueError, match="CHROMA_API_KEY"):
        VectorStore()


def test_cloud_mode_missing_tenant_raises(monkeypatch):
    """Cloud mode without CHROMA_TENANT should fail clearly."""
    _set_chroma_env(monkeypatch, mode="cloud", api_key="key", tenant="", database="d")
    with pytest.raises(ValueError, match="CHROMA_TENANT"):
        VectorStore()


def test_cloud_mode_missing_database_raises(monkeypatch):
    """Cloud mode without CHROMA_DATABASE should fail clearly."""
    _set_chroma_env(monkeypatch, mode="cloud", api_key="key", tenant="t", database="")
    with pytest.raises(ValueError, match="CHROMA_DATABASE"):
        VectorStore()


def test_cloud_mode_with_credentials_creates_client(monkeypatch):
    """Cloud mode with all credentials should initialize."""
    _set_chroma_env(
        monkeypatch,
        mode="cloud",
        api_key="test-api-key",
        tenant="test-tenant",
        database="test-db",
    )
    with patch("chromadb.CloudClient") as MockCloud:
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_collection.count.return_value = 0
        mock_client.get_or_create_collection.return_value = mock_collection
        MockCloud.return_value = mock_client

        store = VectorStore()
        assert store._mode == "cloud"
        MockCloud.assert_called_once_with(
            tenant="test-tenant",
            database="test-db",
            api_key="test-api-key",
        )


def test_local_mode_uses_persistent_client(monkeypatch, tmp_path):
    """Local mode should use PersistentClient."""
    _set_chroma_env(
        monkeypatch,
        mode="local",
        api_key="",
        tenant="",
        database="",
        path=str(tmp_path),
    )
    with patch("chromadb.PersistentClient") as MockLocal:
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_collection.count.return_value = 0
        mock_client.get_or_create_collection.return_value = mock_collection
        MockLocal.return_value = mock_client

        store = VectorStore()
        assert store._mode == "local"
        MockLocal.assert_called_once()


def test_collection_name_is_consistent(monkeypatch):
    """Collection name should be 'benchmark_products' from settings."""
    _set_chroma_env(
        monkeypatch,
        mode="cloud",
        api_key="test-key",
        tenant="test-tenant",
        database="test-db",
        collection="benchmark_products",
    )
    with patch("chromadb.CloudClient") as MockCloud:
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_collection.count.return_value = 0
        mock_client.get_or_create_collection.return_value = mock_collection
        MockCloud.return_value = mock_client

        store = VectorStore()
        assert store._collection_name == "benchmark_products"
        mock_client.get_or_create_collection.assert_called_once_with(
            name="benchmark_products",
            metadata={"hnsw:space": "cosine"},
        )


def test_no_secrets_in_logs(monkeypatch, caplog):
    """Logging should not expose API keys or credentials."""
    _set_chroma_env(
        monkeypatch,
        mode="cloud",
        api_key="super-secret-key-12345",
        tenant="secret-tenant",
        database="secret-db",
    )
    with patch("chromadb.CloudClient") as MockCloud:
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_collection.count.return_value = 0
        mock_client.get_or_create_collection.return_value = mock_collection
        MockCloud.return_value = mock_client

        with caplog.at_level(logging.INFO):
            VectorStore()

    log_text = caplog.text
    assert "super-secret-key-12345" not in log_text
    assert "secret-tenant" not in log_text
    assert "secret-db" not in log_text
    assert "mode=cloud" in log_text
    assert "collection=benchmark_products" in log_text
