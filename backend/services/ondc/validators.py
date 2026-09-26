"""ONDC request validators."""

from __future__ import annotations

import logging
from typing import Dict, Any
from pydantic import BaseModel, Field, ConfigDict, ValidationError

from .context import ONDCContext

logger = logging.getLogger(__name__)

SUPPORTED_DOMAINS = {"ONDC:RET10", "ONDC:RET12"}
SUPPORTED_VERSIONS = {"2.0.2"}
REQUIRED_CONTEXT_FIELDS = {
    "domain",
    "action",
    "version",
    "bap_id",
    "bap_uri",
    "transaction_id",
    "message_id",
    "timestamp",
}


class ONDCValidationError(Exception):
    """ONDC protocol validation error."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


def validate_context(context_data: Dict[str, Any]) -> ONDCContext:
    """Validate ONDC context fields."""
    missing = REQUIRED_CONTEXT_FIELDS - set(context_data.keys())
    if missing:
        raise ONDCValidationError(
            "MISSING_CONTEXT_FIELDS",
            f"Missing required context fields: {', '.join(sorted(missing))}",
        )

    try:
        context = ONDCContext(**context_data)
    except ValidationError as exc:
        raise ONDCValidationError("INVALID_CONTEXT", str(exc))

    if context.domain not in SUPPORTED_DOMAINS:
        raise ONDCValidationError(
            "UNSUPPORTED_DOMAIN",
            f"Domain {context.domain} is not supported. Supported: {', '.join(sorted(SUPPORTED_DOMAINS))}",
        )

    if context.version not in SUPPORTED_VERSIONS:
        raise ONDCValidationError(
            "UNSUPPORTED_VERSION",
            f"Version {context.version} is not supported. Supported: {', '.join(sorted(SUPPORTED_VERSIONS))}",
        )

    return context


def validate_message(request_body: Dict[str, Any], action: str) -> Dict[str, Any]:
    """Validate message body for a given action."""
    message = request_body.get("message")
    if not isinstance(message, dict):
        raise ONDCValidationError("INVALID_MESSAGE", "message must be an object")

    if action in {"search", "on_search"}:
        intent = message.get("intent")
        if not isinstance(intent, dict):
            raise ONDCValidationError("INVALID_INTENT", "intent is required for search")
        return message

    if action in {"select", "on_select", "init", "on_init", "confirm", "on_confirm"}:
        order = message.get("order")
        if not isinstance(order, dict):
            raise ONDCValidationError("INVALID_ORDER", "order is required")
        items = order.get("items")
        if not isinstance(items, list) or len(items) == 0:
            raise ONDCValidationError("NO_ITEMS", "order.items must be a non-empty list")
        return message

    if action in {"status", "on_status"}:
        order_id = message.get("order_id")
        if not order_id:
            raise ONDCValidationError("MISSING_ORDER_ID", "order_id is required")
        return message

    raise ONDCValidationError("UNKNOWN_ACTION", f"Unknown action: {action}")
