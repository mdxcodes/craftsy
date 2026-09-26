"""ONDC Retail BPP protocol endpoints."""

from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.commerce_service import commerce_service
from backend.services.ondc.adapter import ondc_bpp_adapter
from backend.services.ondc.validators import ONDCValidationError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ondc", tags=["ONDC BPP"])


def _handle_ondc_error(exc: ONDCValidationError) -> Dict[str, Any]:
    return {"error": {"code": exc.code, "message": exc.message}}


@router.post("/search")
async def ondc_search(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    try:
        return ondc_bpp_adapter.search(db, payload)
    except ONDCValidationError as exc:
        raise HTTPException(status_code=400, detail=_handle_ondc_error(exc))
    except Exception as exc:  # noqa: BLE001
        logger.error("ONDC search failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": {"code": "INTERNAL_ERROR", "message": str(exc)}})


@router.post("/on_search")
async def ondc_on_search(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    try:
        return ondc_bpp_adapter.search(db, payload)
    except ONDCValidationError as exc:
        raise HTTPException(status_code=400, detail=_handle_ondc_error(exc))
    except Exception as exc:  # noqa: BLE001
        logger.error("ONDC on_search failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": {"code": "INTERNAL_ERROR", "message": str(exc)}})


@router.post("/select")
async def ondc_select(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    try:
        return ondc_bpp_adapter.select(db, payload)
    except ONDCValidationError as exc:
        raise HTTPException(status_code=400, detail=_handle_ondc_error(exc))
    except Exception as exc:  # noqa: BLE001
        logger.error("ONDC select failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": {"code": "INTERNAL_ERROR", "message": str(exc)}})


@router.post("/on_select")
async def ondc_on_select(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    try:
        return ondc_bpp_adapter.select(db, payload)
    except ONDCValidationError as exc:
        raise HTTPException(status_code=400, detail=_handle_ondc_error(exc))
    except Exception as exc:  # noqa: BLE001
        logger.error("ONDC on_select failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": {"code": "INTERNAL_ERROR", "message": str(exc)}})


@router.post("/init")
async def ondc_init(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    try:
        return ondc_bpp_adapter.init(db, payload)
    except ONDCValidationError as exc:
        raise HTTPException(status_code=400, detail=_handle_ondc_error(exc))
    except Exception as exc:  # noqa: BLE001
        logger.error("ONDC init failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": {"code": "INTERNAL_ERROR", "message": str(exc)}})


@router.post("/on_init")
async def ondc_on_init(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    try:
        return ondc_bpp_adapter.init(db, payload)
    except ONDCValidationError as exc:
        raise HTTPException(status_code=400, detail=_handle_ondc_error(exc))
    except Exception as exc:  # noqa: BLE001
        logger.error("ONDC on_init failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": {"code": "INTERNAL_ERROR", "message": str(exc)}})


@router.post("/confirm")
async def ondc_confirm(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    try:
        return ondc_bpp_adapter.confirm(db, payload)
    except ONDCValidationError as exc:
        raise HTTPException(status_code=400, detail=_handle_ondc_error(exc))
    except Exception as exc:  # noqa: BLE001
        logger.error("ONDC confirm failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": {"code": "INTERNAL_ERROR", "message": str(exc)}})


@router.post("/on_confirm")
async def ondc_on_confirm(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    try:
        return ondc_bpp_adapter.confirm(db, payload)
    except ONDCValidationError as exc:
        raise HTTPException(status_code=400, detail=_handle_ondc_error(exc))
    except Exception as exc:  # noqa: BLE001
        logger.error("ONDC on_confirm failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": {"code": "INTERNAL_ERROR", "message": str(exc)}})


@router.post("/status")
async def ondc_status(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    try:
        return ondc_bpp_adapter.status(db, payload)
    except ONDCValidationError as exc:
        raise HTTPException(status_code=400, detail=_handle_ondc_error(exc))
    except Exception as exc:  # noqa: BLE001
        logger.error("ONDC status failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": {"code": "INTERNAL_ERROR", "message": str(exc)}})


@router.post("/on_status")
async def ondc_on_status(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    try:
        return ondc_bpp_adapter.status(db, payload)
    except ONDCValidationError as exc:
        raise HTTPException(status_code=400, detail=_handle_ondc_error(exc))
    except Exception as exc:  # noqa: BLE001
        logger.error("ONDC on_status failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": {"code": "INTERNAL_ERROR", "message": str(exc)}})
