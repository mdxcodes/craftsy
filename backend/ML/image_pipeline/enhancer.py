"""
AI Image Enhancement Pipeline for Craftsy Product Photos.

11-stage pipeline:
1. Load and validate input image
2. Auto-orient based on EXIF
3. Background removal (rembg U²-Net)
4. Smart crop to subject bounding box
5. Square canvas padding (white)
6. Resolution upscaling to 1200x1200
7. Brightness/contrast auto-correction
8. Color vibrance enhancement
9. Sharpness enhancement
10. White balance correction
11. Final quality save

Output: 1200x1200 RGB JPG with white background, studio-quality.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

# Ensure project root is in path for imports
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

logger = logging.getLogger(__name__)

# Target output dimensions (e-commerce standard square)
TARGET_SIZE = (1200, 1200)

# Subject padding ratio (subject occupies 70% of canvas)
SUBJECT_PADDING_RATIO = 0.15

# Minimum input resolution warning
MIN_INPUT_RESOLUTION = 400


def _ensure_rgb(img: Image.Image) -> Image.Image:
    """Convert image to RGB if it has an alpha channel."""
    if img.mode == "RGBA":
        # Composite onto white background
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        return bg
    elif img.mode != "RGB":
        return img.convert("RGB")
    return img


def _auto_orient(img: Image.Image) -> Image.Image:
    """Apply EXIF orientation if present."""
    try:
        exif = img.getexif()
        orientation = exif.get(274)  # 274 = Orientation tag
        if orientation:
            if orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180)
            elif orientation == 4:
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                img = img.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.rotate(90, expand=True)
            elif orientation == 7:
                img = img.rotate(270).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.rotate(270, expand=True)
    except Exception:
        pass
    return img


def _get_subject_bbox(img: Image.Image) -> Optional[tuple]:
    """
    Detect the subject bounding box from a transparent PNG.
    Returns (left, top, right, bottom) or None if detection fails.
    """
    try:
        from PIL import Image as PILImage
        # Convert to numpy array
        arr = np.array(img)

        if arr.shape[2] < 4:
            return None

        # Alpha channel
        alpha = arr[:, :, 3]

        # Find non-transparent pixels
        rows = np.any(alpha > 0, axis=1)
        cols = np.any(alpha > 0, axis=0)

        if not rows.any() or not cols.any():
            return None

        top, bottom = np.where(rows)[0][[0, -1]]
        left, right = np.where(cols)[0][[0, -1]]

        # Add small margin
        margin = 5
        h, w = alpha.shape
        left = max(0, left - margin)
        top = max(0, top - margin)
        right = min(w - 1, right + margin)
        bottom = min(h - 1, bottom + margin)

        return (left, top, right, bottom)
    except Exception as e:
        logger.warning("[Enhancer] Subject detection failed: %s", e)
        return None


def _remove_background(img: Image.Image) -> Image.Image:
    """
    Remove background using rembg.
    Returns RGBA image with transparent background.
    Falls back to original image on failure.
    """
    try:
        from rembg import remove

        # Get or create rembg session
        from ML.image_pipeline.processors.background_removal import get_rembg_session
        session = get_rembg_session()

        # Run background removal
        result = remove(
            img,
            session=session,
            alpha_matting=True,
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=10,
        )

        logger.info("[Enhancer] Background removed successfully")
        return result

    except Exception as e:
        logger.warning("[Enhancer] Background removal failed, using original: %s", e)
        return img


def _smart_crop(img: Image.Image) -> Image.Image:
    """
    Crop image to the subject bounding box, then pad to square.
    """
    # Get subject bounding box
    bbox = _get_subject_bbox(img)

    if bbox:
        left, top, right, bottom = bbox
        img = img.crop((left, top, right + 1, bottom + 1))

    # Make square by padding the shorter dimension with white
    w, h = img.size
    if w != h:
        max_dim = max(w, h)
        new_img = Image.new("RGBA" if img.mode == "RGBA" else "RGB",
                           (max_dim, max_dim), (255, 255, 255, 255))
        paste_x = (max_dim - w) // 2
        paste_y = (max_dim - h) // 2
        new_img.paste(img, (paste_x, paste_y))
        img = new_img

    return img


def _auto_enhance(img: Image.Image) -> Image.Image:
    """
    Apply automatic brightness, contrast, vibrance, and sharpness enhancements.
    """
    # Auto contrast
    img = ImageOps.autocontrast(img, cutoff=1)

    # Brightness: slightly brighter
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.05)

    # Contrast: slightly higher
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.1)

    # Color vibrance
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.15)

    # Sharpness
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.3)

    return img


def enhance_image(input_path: str, output_path: Optional[str] = None) -> str:
    """
    Run the full 11-stage AI image enhancement pipeline.

    Args:
        input_path: Path to the input image
        output_path: Optional path for the output image

    Returns:
        Path to the enhanced output image (1200x1200 RGB JPG)
    """
    input_path_obj = Path(input_path)
    if not input_path_obj.is_file():
        raise FileNotFoundError(f"Input image not found: {input_path}")

    # Determine output path
    if output_path is None:
        output_path_obj = input_path_obj.with_name(
            f"{input_path_obj.stem}_enhanced.jpg"
        )
    else:
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

    logger.info("[Enhancer] Starting image enhancement pipeline for: %s", input_path)

    # Stage 1: Load image
    img = Image.open(input_path_obj)
    logger.info("[Enhancer] Stage 1: Loaded image %s, mode=%s", img.size, img.mode)

    # Stage 2: Auto-orient
    img = _auto_orient(img)

    # Stage 3: Background removal (rembg)
    img = _remove_background(img)

    # Stage 4: Smart crop to subject
    img = _smart_crop(img)

    # Stage 5: Resize to target 1200x1200
    img = img.resize(TARGET_SIZE, Image.LANCZOS)
    logger.info("[Enhancer] Stage 5: Resized to %s", TARGET_SIZE)

    # Stage 6: Convert to RGB (white background)
    img = _ensure_rgb(img)

    # Stage 7: Auto brightness/contrast
    # Stage 8: Color vibrance
    # Stage 9: Sharpness
    img = _auto_enhance(img)
    logger.info("[Enhancer] Stages 7-9: Auto-enhancement applied")

    # Stage 10: White balance correction (simple gray world, preserve white bg)
    try:
        arr = np.array(img).astype(np.float32)
        r_mean, g_mean, b_mean = arr[:,:,0].mean(), arr[:,:,1].mean(), arr[:,:,2].mean()
        gray_mean = (r_mean + g_mean + b_mean) / 3
        # Only apply white balance if the image doesn't already have a white background
        # (avoid shifting white backgrounds to off-white)
        corner_pixels = np.concatenate([
            arr[:50, :50].reshape(-1, 3),
            arr[:50, -50:].reshape(-1, 3),
            arr[-50:, :50].reshape(-1, 3),
            arr[-50:, -50:].reshape(-1, 3),
        ])
        corner_mean = corner_pixels.mean()
        if corner_mean < 240:  # Not already white background
            arr[:,:,0] = np.clip(arr[:,:,0] * (gray_mean / max(r_mean, 1)), 0, 255)
            arr[:,:,1] = np.clip(arr[:,:,1] * (gray_mean / max(g_mean, 1)), 0, 255)
            arr[:,:,2] = np.clip(arr[:,:,2] * (gray_mean / max(b_mean, 1)), 0, 255)
            img = Image.fromarray(arr.astype(np.uint8))
            logger.info("[Enhancer] Stage 10: White balance corrected")
        else:
            logger.info("[Enhancer] Stage 10: White balance skipped (already white bg)")
    except Exception as e:
        logger.warning("[Enhancer] White balance correction skipped: %s", e)

    # Stage 11: Save with high quality
    img.save(output_path_obj, format="JPEG", quality=92, optimize=True)
    logger.info("[Enhancer] Stage 11: Saved enhanced image to: %s", output_path_obj)

    return str(output_path_obj)
