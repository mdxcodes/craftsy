"""
Vector Store — ChromaDB wrapper for benchmark product embeddings.

Provides add/query operations over the benchmark product collection
using cosine similarity search.

Supports two backend modes:
- cloud: Chroma Cloud via CloudClient (production)
- local: ChromaDB PersistentClient (development)
"""

from __future__ import annotations

import logging
from typing import Optional

import chromadb

from ..config import get_settings
from ..models import BenchmarkProduct, SimilarProduct

logger = logging.getLogger(__name__)


class VectorStore:
    """
    ChromaDB-backed vector store for benchmark product embeddings.

    Uses either Chroma Cloud or local persistent storage depending on
    the configured chroma_mode. Cosine similarity is the default metric.
    """

    def __init__(self) -> None:
        settings = get_settings()
        self._mode = settings.chroma_mode
        self._collection_name = settings.chromadb_collection

        self.client = self._create_client(settings)
        self.collection = self.client.get_or_create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": "cosine"},
        )

        logger.info(
            "VectorStore initialized: mode=%s, collection=%s, items=%d",
            self._mode,
            self._collection_name,
            self.collection.count(),
        )

    def _create_client(self, settings) -> chromadb.ClientAPI:
        """Create the appropriate Chroma client based on chroma_mode."""
        mode = getattr(settings, "chroma_mode", "cloud")

        if mode == "local":
            db_path = settings.chromadb_path
            return chromadb.PersistentClient(
                path=db_path,
                settings=chromadb.config.Settings(anonymized_telemetry=False),
            )

        # Cloud mode (default production)
        api_key = getattr(settings, "chroma_api_key", "") or ""
        tenant = getattr(settings, "chroma_tenant", "") or ""
        database = getattr(settings, "chroma_database", "") or ""

        missing = []
        if not api_key:
            missing.append("CHROMA_API_KEY")
        if not tenant:
            missing.append("CHROMA_TENANT")
        if not database:
            missing.append("CHROMA_DATABASE")

        if missing:
            raise ValueError(
                f"Chroma Cloud is configured but missing required environment variables: "
                f"{', '.join(missing)}. "
                f"Set them in .env or Railway Variables."
            )

        return chromadb.CloudClient(
            tenant=tenant,
            database=database,
            api_key=api_key,
        )

    def _safe_client_operation(self, operation_name: str, operation):
        """Execute a client operation with mode-aware error handling."""
        try:
            return operation()
        except Exception as exc:
            logger.error("Chroma %s operation failed [mode=%s]: %s", operation_name, self._mode, exc)
            raise

    def add_products(
        self,
        products: list[BenchmarkProduct],
        vectors: list[list[float]],
    ) -> int:
        """
        Upsert benchmark products with their embedding vectors.

        Args:
            products: List of benchmark products to index.
            vectors: Corresponding embedding vectors (same order).

        Returns:
            Number of products successfully indexed.
        """
        if len(products) != len(vectors):
            raise ValueError(
                f"Products ({len(products)}) and vectors ({len(vectors)}) "
                f"count mismatch"
            )

        if not products:
            return 0

        ids = [p.id for p in products]
        documents = [p.embedding_text() for p in products]
        metadatas = [
            {
                "title": p.title,
                "description": p.description[:500] if p.description else "",
                "category": p.category,
                "selling_price": p.selling_price,
                "source_platform": p.source_platform.value,
                "product_url": p.product_url or "",
                "image_url": p.image_url,
            }
            for p in products
        ]

        batch_size = 100
        total_added = 0

        for i in range(0, len(ids), batch_size):
            batch_end = min(i + batch_size, len(ids))
            try:
                self._safe_client_operation(
                    f"upsert batch {i}-{batch_end}",
                    lambda: self.collection.upsert(
                        ids=ids[i:batch_end],
                        embeddings=vectors[i:batch_end],
                        documents=documents[i:batch_end],
                        metadatas=metadatas[i:batch_end],
                    ),
                )
                total_added += batch_end - i
                logger.info(
                    "Indexed batch %d–%d (%d items)",
                    i,
                    batch_end - 1,
                    batch_end - i,
                )
            except Exception as exc:
                logger.error("Failed to index batch %d–%d: %s", i, batch_end - 1, exc)

        logger.info(
            "VectorStore now contains %d items (added %d)",
            self.collection.count(),
            total_added,
        )
        return total_added

    def query_similar(
        self,
        query_vector: list[float],
        top_k: int = 5,
        category_filter: Optional[str] = None,
        similarity_threshold: float = 0.55,
    ) -> list[SimilarProduct]:
        """
        Find the most similar benchmark products using cosine similarity.

        Args:
            query_vector: The query embedding vector (from artisan's product).
            top_k: Number of results to return (after threshold filtering).
            category_filter: Optional category to restrict search to.
            similarity_threshold: Minimum cosine similarity (0–1).

        Returns:
            List of SimilarProduct instances sorted by similarity (highest first).
        """
        where_filter = None
        if category_filter:
            where_filter = {"category": category_filter}

        fetch_k = max(top_k * 2, top_k + 5)

        try:
            results = self._safe_client_operation(
                "query",
                lambda: self.collection.query(
                    query_embeddings=[query_vector],
                    n_results=fetch_k,
                    where=where_filter,
                    include=["metadatas", "distances", "documents"],
                ),
            )
        except Exception as exc:
            logger.error("Vector query failed [mode=%s]: %s", self._mode, exc)
            return []

        similar_products: list[SimilarProduct] = []

        if not results.get("ids") or not results["ids"][0]:
            logger.info("No similar products found")
            return []

        for i, product_id in enumerate(results["ids"][0]):
            metadata = results["metadatas"][0][i]
            distance = results["distances"][0][i]
            similarity = 1.0 - distance

            if similarity < similarity_threshold:
                logger.debug(
                    "Dropping comparable '%s' — similarity %.4f below threshold %.2f",
                    metadata.get("title", "?"),
                    similarity,
                    similarity_threshold,
                )
                continue

            similar_products.append(
                SimilarProduct(
                    id=product_id,
                    title=metadata.get("title", ""),
                    description=metadata.get("description", ""),
                    category=metadata.get("category", ""),
                    selling_price=float(metadata.get("selling_price", 0)),
                    source_platform=metadata.get("source_platform", ""),
                    similarity_score=round(max(0.0, similarity), 4),
                    product_url=metadata.get("product_url"),
                )
            )

            if len(similar_products) >= top_k:
                break

        logger.info(
            "Found %d similar products above threshold %.2f (top similarity: %.4f)",
            len(similar_products),
            similarity_threshold,
            similar_products[0].similarity_score if similar_products else 0,
        )
        return similar_products

    def get_count(self) -> int:
        """Return the number of items in the collection."""
        return self.collection.count()

    def clear(self) -> None:
        """Delete all items from the collection."""
        settings = get_settings()
        self._safe_client_operation(
            "delete_collection",
            lambda: self.client.delete_collection(settings.chromadb_collection),
        )
        self.collection = self.client.get_or_create_collection(
            name=settings.chromadb_collection,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info("VectorStore cleared")
