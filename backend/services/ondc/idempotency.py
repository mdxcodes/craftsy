"""Idempotency store for ONDC confirm requests."""

from __future__ import annotations

import threading
import logging
from typing import Optional, Dict, Tuple

logger = logging.getLogger(__name__)


class IdempotencyStore:
    """In-memory idempotency store keyed by (transaction_id, message_id)."""

    def __init__(self) -> None:
        self._store: Dict[Tuple[str, str], str] = {}
        self._lock = threading.Lock()

    def get(self, transaction_id: str, message_id: str) -> Optional[str]:
        """Return existing order_id if this confirm was already processed."""
        key = (transaction_id, message_id)
        with self._lock:
            return self._store.get(key)

    def set(self, transaction_id: str, message_id: str, order_id: str) -> None:
        """Record a processed confirm."""
        key = (transaction_id, message_id)
        with self._lock:
            self._store[key] = order_id

    def clear(self) -> None:
        """Clear all entries (testing only)."""
        with self._lock:
            self._store.clear()


idempotency_store = IdempotencyStore()
