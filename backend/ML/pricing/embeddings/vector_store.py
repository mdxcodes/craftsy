"""
Vector Store for Product Embeddings.

Uses ChromaDB for similarity search across benchmark products.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class VectorStore:
    """ChromaDB-based vector store for product similarity search."""

    def __init__(self):
        self._client = None
        self._collection = None

    def _get_client(self):
        """Lazy-initialize ChromaDB client."""
        if self._client is None:
            try:
                import chromadb
                self._client = chromadb.Client()
                self._collection = self._client.get_or_create_collection(
                    name="craftsy_benchmarks",
                    metadata={"description": "Craftsy benchmark product embeddings"},
                )
            except Exception as e:
                logger.warning("[VectorStore] ChromaDB initialization failed: %s", e)
                self._client = None
        return self._client

    def get_count(self) -> int:
        """Return the number of indexed benchmark products."""
        client = self._get_client()
        if client is None:
            return 0
        try:
            return self._collection.count()
        except Exception:
            return 0

    def search_similar(
        self,
        query_embedding: list,
        n_results: int = 5,
    ) -> list:
        """Search for similar products by embedding."""
        client = self._get_client()
        if client is None:
            return []
        try:
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
            )
            return results.get("metadatas", [])
        except Exception:
            return []
