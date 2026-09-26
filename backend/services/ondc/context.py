"""ONDC request context extraction and correlation."""

from __future__ import annotations

import uuid
import logging
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, ValidationError

logger = logging.getLogger(__name__)


class ONDCContext(BaseModel):
    """ONDC protocol context."""
    model_config = ConfigDict(extra="ignore")

    domain: str
    action: str
    version: str
    bap_id: str
    bap_uri: str
    transaction_id: str
    message_id: str
    timestamp: str
    ttl: Optional[str] = "PT30S"
    location: Optional[Dict[str, Any]] = None
    bpp_id: Optional[str] = None
    bpp_uri: Optional[str] = None


def extract_context(request_body: Dict[str, Any]) -> ONDCContext:
    """Extract and validate ONDC context from request body."""
    context_data = request_body.get("context", {})
    try:
        return ONDCContext(**context_data)
    except ValidationError as exc:
        raise ValueError(f"Invalid ONDC context: {exc}")


def generate_message_id() -> str:
    """Generate a new ONDC message ID."""
    return f"msg_{uuid.uuid4().hex[:12]}"
