"""
Catalog & AI Multimodal Router.

Handles photo enhancement, speech-to-text audio transcription via ML voice pipeline,
bilingual listing generation, and complete voice-to-product draft creation.
"""

import logging
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.schemas import (
    AudioTranscribeResponse,
    ListingGenerateRequest,
    ListingGenerateResponse,
    ImageEnhanceResponse,
    VoiceToProductResponse,
    CostInputsSchema,
)
from ..services.catalog_service import CatalogService
from ..services.storage_service import StorageService
from ..services.cloudinary_service import cloudinary_service

import asyncio

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/catalog", tags=["Cataloger AI"])
catalog_service = CatalogService()
storage_service = StorageService()
_image_semaphore = asyncio.Semaphore(1)


@router.post("/enhance-image", response_model=ImageEnhanceResponse)
async def enhance_image(
    image: UploadFile = File(...),
):
    """
    Upload and optimize product photos for studio quality e-commerce listings.
    Non-blocking: offloads CPU-bound rembg/CV processing to background threadpool.
    Serialized with Semaphore(1) to avoid concurrent memory spikes on cloud containers.
    """
    try:
        # 1. Save original raw upload (temporary local processing storage)
        raw_url = await storage_service.save_upload(image, subfolder="raw")
        raw_path = storage_service.get_local_path_from_url(raw_url)
        if not raw_path:
            raise HTTPException(status_code=500, detail="Failed to locate stored raw image")

        # 2. Prepare destination path for enhanced image (temporary local processing storage)
        enhanced_dir = storage_service.upload_dir / "enhanced"
        enhanced_dir.mkdir(parents=True, exist_ok=True)
        enhanced_filename = f"{raw_path.stem}_enhanced.jpg"
        enhanced_path = enhanced_dir / enhanced_filename

        # 3. Execute non-blocking AI image enhancement (serialized)
        async with _image_semaphore:
            result_path = await catalog_service.enhance_product_photo(
                input_path=str(raw_path),
                output_path=str(enhanced_path),
            )
            if Path(result_path) != enhanced_path or not enhanced_path.is_file():
                import shutil
                shutil.copy2(str(result_path), str(enhanced_path))

        # 4. Upload enhanced image to Cloudinary (permanent storage)
        enhanced_cloudinary_url = None
        enhanced_public_id = None
        if cloudinary_service.enabled:
            try:
                product_hint = raw_path.stem
                folder = f"craftsy/products/{product_hint}"
                upload_result = cloudinary_service.upload_image(
                    file_path=str(enhanced_path),
                    folder=folder,
                    public_id="original",
                )
                enhanced_public_id = upload_result.get("public_id")
                enhanced_cloudinary_url = upload_result.get("secure_url")
                logger.info(
                    "Enhanced image uploaded to Cloudinary: public_id=%s, url=%s",
                    enhanced_public_id,
                    enhanced_cloudinary_url,
                )
            except Exception as cloud_exc:  # noqa: BLE001
                logger.warning(
                    "Cloudinary upload failed, falling back to local URL: %s",
                    cloud_exc,
                )

        # 5. Determine the enhanced image URL to return
        if enhanced_cloudinary_url:
            enhanced_url = enhanced_cloudinary_url
        else:
            enhanced_url = f"{storage_service.settings.static_url_prefix}/enhanced/{enhanced_filename}" if hasattr(storage_service, 'settings') else f"/uploads/enhanced/{enhanced_filename}"

        return ImageEnhanceResponse(
            original_url=raw_url,
            enhanced_url=enhanced_url,
            status="success",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image enhancement failed: {str(e)}")


@router.post("/upload-image", response_model=dict)
async def upload_image(image: UploadFile = File(...)):
    """Store a client-local image, upload to Cloudinary, and return the Cloudinary HTTPS URL."""
    try:
        # Save to temporary local processing storage
        local_url = await storage_service.save_upload(image, subfolder="social")
        local_path = storage_service.get_local_path_from_url(local_url)
        if not local_path:
            raise HTTPException(status_code=500, detail="Failed to locate stored image")

        # Upload to Cloudinary for permanent storage
        if cloudinary_service.enabled:
            try:
                upload_result = cloudinary_service.upload_image(
                    file_path=str(local_path),
                    folder="craftsy/social",
                    public_id=local_path.stem,
                )
                cloudinary_url = upload_result.get("secure_url")
                if cloudinary_url:
                    return {"image_url": cloudinary_url}
            except Exception as cloud_exc:  # noqa: BLE001
                logger.warning(
                    "Cloudinary upload failed for social image, returning local URL: %s",
                    cloud_exc,
                )

        return {"image_url": local_url}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")


@router.post("/transcribe", response_model=AudioTranscribeResponse)
async def transcribe_voice_note(
    audio: UploadFile = File(...),
    language_code: str = Form("hi"),
    category_hint: Optional[str] = Form(None),
):
    """
    Transcribe an artisan's regional voice note to text using the ML voice pipeline (Whisper STT).
    """
    try:
        audio_url = await storage_service.save_upload(audio, subfolder="audio")
        local_path = storage_service.get_local_path_from_url(audio_url)
        if not local_path:
            raise HTTPException(status_code=500, detail="Failed to locate saved audio")

        response = await catalog_service.transcribe_audio(
            audio_file_path=str(local_path),
            language_code=language_code,
            category_hint=category_hint,
        )
        if response.status == "failed" and response.error_code:
            raise HTTPException(status_code=400, detail={
                "error_code": response.error_code,
                "message": _get_error_message(response.error_code),
            })
        return response
    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail={"error_code": "invalid_audio", "message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio transcription failed: {str(e)}")


def _get_error_message(error_code: str) -> str:
    """Map error codes to user-friendly messages."""
    messages = {
        "silent_audio": "No audible speech detected. Please speak closer to the microphone.",
        "invalid_audio": "Invalid or empty audio file. Please try recording again.",
        "missing_transcription_config": "Speech transcription is not configured. Please contact support.",
        "transcription_failed": "Transcription failed. Please try again.",
        "empty_transcript": "No speech was detected in the recording. Please try again.",
    }
    return messages.get(error_code, "Voice transcription failed.")


@router.post("/generate-listing", response_model=ListingGenerateResponse)
async def generate_bilingual_listing(
    request: ListingGenerateRequest,
):
    """
    Generate professional bilingual (English + Hindi) titles, descriptions,
    category classification, and SEO tags from a transcript.
    """
    try:
        return await catalog_service.generate_listing(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Listing generation failed: {str(e)}")


@router.post("/voice-to-listing", response_model=ListingGenerateResponse)
async def voice_to_listing(
    audio: UploadFile = File(...),
    language_code: str = Form("hi"),
    category_hint: Optional[str] = Form(None),
):
    """
    Direct voice-to-listing pipeline:
    Transcribes artisan voice note and directly generates bilingual title, description, category, and tags.
    """
    try:
        audio_url = await storage_service.save_upload(audio, subfolder="audio")
        local_path = storage_service.get_local_path_from_url(audio_url)
        if not local_path:
            raise HTTPException(status_code=500, detail="Failed to locate saved audio")

        transcribe_res = await catalog_service.transcribe_audio(
            audio_file_path=str(local_path),
            language_code=language_code,
            category_hint=category_hint,
        )
        if transcribe_res.status == "failed" and transcribe_res.error_code:
            raise HTTPException(status_code=400, detail={
                "error_code": transcribe_res.error_code,
                "message": _get_error_message(transcribe_res.error_code),
            })

        return await catalog_service.generate_listing(
            ListingGenerateRequest(
                transcript=transcribe_res.transcript,
                language_code=language_code,
                category_hint=category_hint,
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice to listing failed: {str(e)}")


@router.post("/voice-to-product", response_model=VoiceToProductResponse)
async def voice_to_product(
    audio: UploadFile = File(...),
    image: Optional[UploadFile] = File(None),
    language_code: str = Form("hi"),
    category_hint: Optional[str] = Form(None),
    raw_material_cost: Optional[float] = Form(None),
    labor_hours: Optional[float] = Form(None),
    hourly_wage: Optional[float] = Form(None),
    transport: Optional[float] = Form(0.0),
    overhead: Optional[float] = Form(0.0),
    db: Session = Depends(get_db),
):
    """
    One-click voice-to-product endpoint:
    Processes artisan voice audio, generates description & tags, calculates base prices and
    pricing suggestions, and returns a pre-populated product draft.
    """
    try:
        audio_url = await storage_service.save_upload(audio, subfolder="audio")
        audio_path = storage_service.get_local_path_from_url(audio_url)
        if not audio_path:
            raise HTTPException(status_code=500, detail="Failed to store audio file")

        image_url = None
        if image:
            local_image_url = await storage_service.save_upload(image, subfolder="products")
            local_image_path = storage_service.get_local_path_from_url(local_image_url)

            # Upload to Cloudinary for permanent storage
            if cloudinary_service.enabled and local_image_path:
                try:
                    upload_result = cloudinary_service.upload_image(
                        file_path=str(local_image_path),
                        folder="craftsy/products",
                        public_id=local_image_path.stem,
                    )
                    image_url = upload_result.get("secure_url")
                except Exception as cloud_exc:  # noqa: BLE001
                    logger.warning(
                        "Cloudinary upload failed for voice-to-product image, using local URL: %s",
                        cloud_exc,
                    )
                    image_url = local_image_url
            else:
                image_url = local_image_url

        cost_override = None
        if raw_material_cost is not None or labor_hours is not None or hourly_wage is not None:
            cost_override = CostInputsSchema(
                materials=raw_material_cost or 0.0,
                labor_hours=labor_hours or 0.0,
                hourly_rate=hourly_wage or 50.0,
                transport=transport or 0.0,
                overhead=overhead or 0.0,
            )

        return await catalog_service.process_voice_to_product(
            audio_file_path=str(audio_path),
            language_code=language_code,
            category_hint=category_hint,
            image_url=image_url,
            audio_url=audio_url,
            cost_inputs_override=cost_override,
            db=db,
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice to product failed: {str(e)}")
