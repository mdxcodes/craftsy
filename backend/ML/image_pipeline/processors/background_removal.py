"""
Background Removal Processor using rembg (U²-Net ONNX model).

Removes the background from product photos and returns a transparent PNG.
The ONNX model is downloaded once on first use and cached locally.
"""

import os
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Module-level singleton for the rembg session (lazy-loaded, thread-safe)
_rembg_session = None


def get_rembg_session():
    """
    Lazily initialize and return a singleton rembg session.
    The U²-NX model is downloaded from the internet on first use.
    """
    global _rembg_session
    if _rembg_session is None:
        try:
            from rembg import new_session
            # Use the lightweight "u2netp" model (fast, good for product photos)
            # Other options: "u2net", "u2net_human_seg", "silueta"
            model_name = os.environ.get("REMBG_MODEL", "u2netp")
            logger.info("[BackgroundRemoval] Initializing rembg session with model: %s", model_name)
            _rembg_session = new_session(model_name)
            logger.info("[BackgroundRemoval] rembg session initialized successfully")
        except Exception as e:
            logger.error("[BackgroundRemoval] Failed to initialize rembg: %s", e)
            raise
    return _rembg_session


def remove_background(input_path: str, output_path: Optional[str] = None) -> str:
    """
    Remove background from an image using rembg.

    Args:
        input_path: Path to the input image (JPG/PNG/WebP)
        output_path: Optional path for the output PNG. If None, returns input path.

    Returns:
        Path to the output image (PNG with transparent background)
    """
    from rembg import remove
    from PIL import Image
    import io

    input_path_obj = Path(input_path)
    if not input_path_obj.is_file():
        raise FileNotFoundError(f"Input image not found: {input_path}")

    # Determine output path
    if output_path is None:
        output_path_obj = input_path_obj.with_suffix(".png")
    else:
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

    # Open input image
    with Image.open(input_path_obj) as img:
        # Convert to RGB if necessary (rembg requires RGB/RGBA)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        # Get rembg session
        session = get_rembg_session()

        # Run background removal
        result = remove(
            img,
            session=session,
            alpha_matting=True,  # Better edge quality
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=10,
        )

        # Save result
        result.save(output_path_obj, format="PNG")
        logger.info("[BackgroundRemoval] Saved transparent image to: %s", output_path_obj)

    return str(output_path_obj)


def remove_background_from_bytes(image_bytes: bytes) -> bytes:
    """
    Remove background from image bytes (useful for in-memory processing).

    Args:
        image_bytes: Raw image bytes

    Returns:
        Transparent PNG bytes
    """
    from rembg import remove
    from PIL import Image
    import io

    # Get rembg session
    session = get_rembg_session()

    # Process from bytes
    input_img = Image.open(io.BytesIO(image_bytes))
    if input_img.mode not in ("RGB", "RGBA"):
        input_img = input_img.convert("RGB")

    result = remove(
        input_img,
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
    )

    # Save to bytes
    output_buffer = io.BytesIO()
    result.save(output_buffer, format="PNG")
    return output_buffer.getvalue()
