"""
Cloudinary Image Storage Service.

Provides persistent image upload, deletion, and URL generation for Craftsy.
The Railway filesystem (/app/backend/uploads) remains as temporary processing
storage only; Cloudinary is the permanent image store.
"""

import logging
import os
from pathlib import Path
from typing import Optional

import cloudinary
import cloudinary.uploader
import cloudinary.utils

from ..config import get_settings

logger = logging.getLogger(__name__)


class CloudinaryService:
    """Manages Cloudinary image storage for product and profile images."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._enabled = self._configure()

    @property
    def enabled(self) -> bool:
        """Whether Cloudinary is configured and available."""
        return self._enabled

    def _configure(self) -> bool:
        """Configure Cloudinary from environment variables."""
        cloud_name = (self.settings.cloudinary_cloud_name or "").strip()
        api_key = (self.settings.cloudinary_api_key or "").strip()
        api_secret = (self.settings.cloudinary_api_secret or "").strip()

        if not cloud_name or not api_key or not api_secret:
            logger.warning(
                "Cloudinary not configured: missing CLOUDINARY_CLOUD_NAME, "
                "CLOUDINARY_API_KEY, or CLOUDINARY_API_SECRET."
            )
            return False

        try:
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret,
                secure=True,
            )
            logger.info("Cloudinary configured successfully.")
            return True
        except Exception as exc:  # noqa: BLE001
            logger.warning("Cloudinary configuration failed: %s", exc)
            return False

    def upload_image(
        self,
        file_path: str | Path,
        folder: str = "craftsy/products",
        public_id: Optional[str] = None,
        overwrite: bool = True,
    ) -> dict:
        """Upload an image to Cloudinary.

        Args:
            file_path: Local path to the image file.
            folder: Cloudinary folder path (e.g. 'craftsy/products/prod_123').
            public_id: Optional stable public ID. If omitted, Cloudinary
                       generates one from the filename.
            overwrite: Whether to overwrite existing assets with the same ID.

        Returns:
            Cloudinary upload response dict containing public_id, secure_url,
            resource_type, format, width, height, bytes, etc.

        Raises:
            RuntimeError: If Cloudinary is not configured or upload fails.
        """
        if not self._enabled:
            raise RuntimeError("Cloudinary is not configured.")

        file_path = Path(file_path)
        if not file_path.is_file():
            raise FileNotFoundError(f"Image file not found: {file_path}")

        # Sanitize public_id — prevent path traversal and empty values
        safe_public_id = None
        if public_id:
            safe_public_id = public_id.replace("\\", "/").strip("/")
            if not safe_public_id:
                safe_public_id = None

        # Build absolute folder path
        abs_folder = folder.replace("\\", "/").strip("/")
        if not abs_folder:
            abs_folder = "craftsy"

        try:
            result = cloudinary.uploader.upload(
                str(file_path),
                folder=abs_folder,
                overwrite=overwrite,
                resource_type="image",
                use_filename=False,
                unique_filename=False,
                public_id=safe_public_id,
            )
            logger.info(
                "Cloudinary upload OK: public_id=%s, url=%s",
                result.get("public_id"),
                result.get("secure_url"),
            )
            return result
        except Exception as exc:  # noqa: BLE001
            logger.error("Cloudinary upload failed for %s: %s", file_path, exc)
            raise RuntimeError(f"Cloudinary upload failed: {exc}") from exc

    def delete_image(self, public_id: str) -> dict:
        """Delete an image from Cloudinary by public ID.

        Args:
            public_id: Cloudinary public ID (with or without folder prefix).

        Returns:
            Cloudinary deletion response dict.

        Raises:
            RuntimeError: If Cloudinary is not configured or deletion fails.
        """
        if not self._enabled:
            raise RuntimeError("Cloudinary is not configured.")

        safe_id = public_id.replace("\\", "/").strip("/")
        if not safe_id:
            raise ValueError("public_id must not be empty.")

        try:
            result = cloudinary.uploader.destroy(safe_id, resource_type="image")
            logger.info("Cloudinary delete OK: public_id=%s, result=%s", safe_id, result)
            return result
        except Exception as exc:  # noqa: BLE001
            logger.error("Cloudinary delete failed for %s: %s", safe_id, exc)
            raise RuntimeError(f"Cloudinary delete failed: {exc}") from exc

    def build_url(
        self,
        public_id: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        crop: Optional[str] = None,
        quality: Optional[str] = None,
        fetch_format: Optional[str] = None,
    ) -> str:
        """Build a Cloudinary delivery URL for a known public ID.

        This does not verify the asset exists in Cloudinary; it simply
        constructs the URL so the API can return it immediately after
        a successful upload.

        Args:
            public_id: Cloudinary public ID.
            width: Optional target width.
            height: Optional target height.
            crop: Optional crop mode (e.g. 'limit', 'fill', 'thumb').
            quality: Optional quality preset (e.g. 'auto:good').
            fetch_format: Optional delivery format (e.g. 'auto', 'webp').

        Returns:
            HTTPS URL to the Cloudinary asset.
        """
        if not public_id:
            return ""

        safe_id = public_id.replace("\\", "/").strip("/")
        options = {}

        if width:
            options["w"] = width
        if height:
            options["h"] = height
        if crop:
            options["c"] = crop
        if quality:
            options["q"] = quality
        if fetch_format:
            options["f"] = fetch_format

        try:
            url = cloudinary.utils.cloudinary_url(safe_id, **options)
            return url
        except Exception as exc:  # noqa: BLE001
            logger.warning("Cloudinary URL build failed for %s: %s", safe_id, exc)
            return ""

    def extract_public_id_from_url(self, url: str) -> Optional[str]:
        """Extract the Cloudinary public ID from a full secure URL.

        Args:
            url: Full Cloudinary HTTPS URL.

        Returns:
            Public ID string, or None if the URL is not a Cloudinary URL.
        """
        if not url or "res.cloudinary.com" not in url:
            return None

        try:
            # Cloudinary URLs follow the pattern:
            # https://res.cloudinary.com/<cloud>/image/upload/v<ver>/<public_id>.<ext>
            # or:
            # https://res.cloudinary.com/<cloud>/image/upload/<public_id>
            parts = url.split("/image/upload/")
            if len(parts) < 2:
                return None

            public_id_with_ext = parts[-1]
            # Strip version prefix if present (v1234567890/)
            if public_id_with_ext.startswith("v"):
                slash_idx = public_id_with_ext.find("/")
                if slash_idx != -1 and public_id_with_ext[1:slash_idx].isdigit():
                    public_id_with_ext = public_id_with_ext[slash_idx + 1:]

            # Strip extension
            dot_idx = public_id_with_ext.rfind(".")
            if dot_idx != -1:
                public_id = public_id_with_ext[:dot_idx]
            else:
                public_id = public_id_with_ext

            return public_id.strip("/") or None
        except Exception:  # noqa: BLE001
            return None


# Singleton instance
cloudinary_service = CloudinaryService()

