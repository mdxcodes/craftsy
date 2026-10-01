"""
Product Management Router.

Provides product CRUD endpoints and batch sync for Flutter offline queue.
"""

import json
import logging
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile, Form, Request
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from ..database import get_db
from ..models.db_models import ArtisanDB, ProductDB
from ..models.schemas import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductSyncBatch,
    ProductSyncResponse,
)
from ..services.cloudinary_service import cloudinary_service
from ..utils.authorization import get_artisan_from_x_user_id, verify_product_owner

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


def _handle_permission_error(exc: PermissionError) -> None:
    raise HTTPException(status_code=403, detail=str(exc))


def _get_current_artisan(request: Request, db: Session) -> ArtisanDB:
    artisan = get_artisan_from_x_user_id(request, db)
    if not artisan:
        raise HTTPException(status_code=401, detail="Authentication required")
    return artisan


@router.get("", response_model=List[ProductResponse])
async def list_products(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    List the authenticated artisan's own catalog products.
    """
    artisan = _get_current_artisan(request, db)

    query = db.query(ProductDB).filter(ProductDB.artisan_id == artisan.id)

    items = query.order_by(ProductDB.created_at.desc()).all()

    return [
        ProductResponse(
            id=item.id,
            artisan_id=item.artisan_id,
            title=item.title,
            title_hi=item.title_hi or "",
            description=item.description or "",
            description_hi=item.description_hi or "",
            price=item.price,
            image_url=item.image_url,
            category=item.category,
            tags=item.tags_list,
            status=item.status,
            created_at=item.created_at,
            updated_at=item.updated_at,
            cloudinary_public_id=item.cloudinary_public_id,
        )
        for item in items
    ]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, db: Session = Depends(get_db)):
    """Fetch a single product by ID."""
    item = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")

    return ProductResponse(
        id=item.id,
        artisan_id=item.artisan_id,
        title=item.title,
        title_hi=item.title_hi or "",
        description=item.description or "",
        description_hi=item.description_hi or "",
        price=item.price,
        image_url=item.image_url,
        category=item.category,
        tags=item.tags_list,
        status=item.status,
        created_at=item.created_at,
        updated_at=item.updated_at,
        cloudinary_public_id=item.cloudinary_public_id,
    )


@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(
    request: Request,
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    """Create a new artisan product listing."""
    artisan = _get_current_artisan(request, db)

    prod_id = product.id if product.id else f"prod_{uuid.uuid4().hex[:10]}"

    existing = db.query(ProductDB).filter(ProductDB.id == prod_id).first()
    if existing:
        existing.title = product.title
        existing.title_hi = product.title_hi or ""
        existing.description = product.description
        existing.description_hi = product.description_hi or ""
        existing.price = product.price
        existing.image_url = product.image_url
        existing.category = product.category
        existing.tags = json.dumps(product.tags)
        existing.status = product.status
        if product.stock is not None:
            existing.stock = product.stock
        existing.updated_at = datetime.now()
        db.commit()
        db.refresh(existing)
        db_item = existing
    else:
        db_item = ProductDB(
            id=prod_id,
            artisan_id=artisan.id,
            title=product.title,
            title_hi=product.title_hi or "",
            description=product.description,
            description_hi=product.description_hi or "",
            price=product.price,
            image_url=product.image_url,
            category=product.category,
            tags=json.dumps(product.tags),
            status=product.status,
            stock=product.stock if product.stock is not None else 0,
            platforms=json.dumps(product.platforms),
            created_at=product.created_at or datetime.now(),
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

    return ProductResponse(
        id=db_item.id,
        artisan_id=db_item.artisan_id,
        title=db_item.title,
        title_hi=db_item.title_hi or "",
        description=db_item.description or "",
        description_hi=db_item.description_hi or "",
        price=db_item.price,
        image_url=db_item.image_url,
        category=db_item.category,
        tags=db_item.tags_list,
        status=db_item.status,
        stock=db_item.stock,
        created_at=db_item.created_at,
        updated_at=db_item.updated_at,
        cloudinary_public_id=db_item.cloudinary_public_id,
    )


@router.post("/upload-image", response_model=dict)
async def upload_product_image(
    request: Request,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload a product image to Cloudinary and return the permanent URL."""
    _get_current_artisan(request, db)

    try:
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image.filename)[1]) as tmp:
            content = await image.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            if cloudinary_service.enabled:
                upload_result = cloudinary_service.upload_image(
                    file_path=tmp_path,
                    folder="craftsy/products",
                    public_id=f"product_{uuid.uuid4().hex[:8]}",
                )
                cloudinary_url = upload_result.get("secure_url")
                if cloudinary_url:
                    return {"image_url": cloudinary_url, "public_id": upload_result.get("public_id")}

            return {"image_url": tmp_path, "public_id": None}
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    request: Request,
    product_id: str,
    update_data: ProductUpdate,
    db: Session = Depends(get_db),
):
    """Update product fields."""
    artisan = _get_current_artisan(request, db)

    db_item = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        verify_product_owner(artisan, db_item)
    except PermissionError as exc:
        _handle_permission_error(exc)

    if update_data.title is not None:
        db_item.title = update_data.title
    if update_data.title_hi is not None:
        db_item.title_hi = update_data.title_hi
    if update_data.description is not None:
        db_item.description = update_data.description
    if update_data.description_hi is not None:
        db_item.description_hi = update_data.description_hi
    if update_data.price is not None:
        db_item.price = update_data.price
    if update_data.image_url is not None:
        old_image_url = db_item.image_url
        old_cloudinary_public_id = db_item.cloudinary_public_id

        db_item.image_url = update_data.image_url

        # Update cloudinary_public_id if the new URL is a Cloudinary URL
        new_cloudinary_public_id = None
        if update_data.image_url.startswith("https://") and "res.cloudinary.com" in update_data.image_url:
            from ..services.cloudinary_service import cloudinary_service
            new_cloudinary_public_id = cloudinary_service.extract_public_id_from_url(update_data.image_url)

        if new_cloudinary_public_id:
            db_item.cloudinary_public_id = new_cloudinary_public_id
            # Delete old Cloudinary image if it was a different asset
            if old_cloudinary_public_id and old_cloudinary_public_id != new_cloudinary_public_id:
                try:
                    from ..services.cloudinary_service import cloudinary_service
                    if cloudinary_service.enabled:
                        cloudinary_service.delete_image(old_cloudinary_public_id)
                except Exception as cloud_exc:  # noqa: BLE001
                    logger.warning(
                        "Failed to delete old Cloudinary image for product %s (old_public_id=%s): %s",
                        product_id,
                        old_cloudinary_public_id,
                        cloud_exc,
                    )
        else:
            # New image is not from Cloudinary, clear the public_id
            db_item.cloudinary_public_id = None
            # Delete old Cloudinary image if it existed
            if old_cloudinary_public_id:
                try:
                    from ..services.cloudinary_service import cloudinary_service
                    if cloudinary_service.enabled:
                        cloudinary_service.delete_image(old_cloudinary_public_id)
                except Exception as cloud_exc:  # noqa: BLE001
                    logger.warning(
                        "Failed to delete old Cloudinary image for product %s (old_public_id=%s): %s",
                        product_id,
                        old_cloudinary_public_id,
                        cloud_exc,
                    )
    if update_data.category is not None:
        db_item.category = update_data.category
    if update_data.tags is not None:
        db_item.tags = json.dumps(update_data.tags)
    if update_data.status is not None:
        db_item.status = update_data.status
    if update_data.stock is not None:
        db_item.stock = update_data.stock
    if update_data.platforms is not None:
        db_item.platforms = json.dumps(update_data.platforms)

    db_item.updated_at = datetime.now()
    db.commit()
    db.refresh(db_item)

    return ProductResponse(
        id=db_item.id,
        artisan_id=db_item.artisan_id,
        title=db_item.title,
        title_hi=db_item.title_hi or "",
        description=db_item.description or "",
        description_hi=db_item.description_hi or "",
        price=db_item.price,
        image_url=db_item.image_url,
        category=db_item.category,
        tags=db_item.tags_list,
        status=db_item.status,
        stock=db_item.stock,
        created_at=db_item.created_at,
        updated_at=db_item.updated_at,
        cloudinary_public_id=db_item.cloudinary_public_id,
    )


@router.delete("/{product_id}")
async def delete_product(request: Request, product_id: str, db: Session = Depends(get_db)):
    """Delete product from database and remove associated Cloudinary image if present."""
    artisan = _get_current_artisan(request, db)

    db_item = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        verify_product_owner(artisan, db_item)
    except PermissionError as exc:
        _handle_permission_error(exc)

    # Delete Cloudinary image before removing the database record
    cloudinary_public_id = db_item.cloudinary_public_id
    if cloudinary_public_id:
        try:
            from ..services.cloudinary_service import cloudinary_service
            if cloudinary_service.enabled:
                cloudinary_service.delete_image(cloudinary_public_id)
        except Exception as cloud_exc:  # noqa: BLE001
            logger.warning(
                "Cloudinary image deletion failed for product %s (public_id=%s): %s",
                product_id,
                cloudinary_public_id,
                cloud_exc,
            )

    db.delete(db_item)
    db.commit()
    return {"success": True, "deleted_id": product_id}


@router.post("/sync", response_model=ProductSyncResponse)
async def sync_offline_products(
    request: Request,
    batch: ProductSyncBatch,
    db: Session = Depends(get_db),
):
    """
    Batch drain endpoint for Flutter's offline queue.
    Accepts products captured while offline and persists them.
    """
    artisan = _get_current_artisan(request, db)

    synced_items = []
    for item in batch.products:
        prod_id = item.id if item.id else f"prod_{uuid.uuid4().hex[:10]}"
        existing = db.query(ProductDB).filter(ProductDB.id == prod_id).first()
        if existing:
            existing.title = item.title
            existing.title_hi = item.title_hi or ""
            existing.description = item.description
            existing.description_hi = item.description_hi or ""
            existing.price = item.price
            existing.image_url = item.image_url
            existing.category = item.category
            existing.tags = json.dumps(item.tags)
            existing.status = "live"
            existing.updated_at = datetime.now()
            db_item = existing
        else:
            db_item = ProductDB(
                id=prod_id,
                artisan_id=artisan.id,
                title=item.title,
                title_hi=item.title_hi or "",
                description=item.description,
                description_hi=item.description_hi or "",
                price=item.price,
                image_url=item.image_url,
                category=item.category,
                tags=json.dumps(item.tags),
                status="live",
                created_at=item.created_at or datetime.now(),
            )
            db.add(db_item)
        synced_items.append(db_item)

    db.commit()
    for s in synced_items:
        db.refresh(s)

    responses = [
        ProductResponse(
            id=s.id,
            artisan_id=s.artisan_id,
            title=s.title,
            title_hi=s.title_hi or "",
            description=s.description or "",
            description_hi=s.description_hi or "",
            price=s.price,
            image_url=s.image_url,
            category=s.category,
            tags=s.tags_list,
            status=s.status,
            created_at=s.created_at,
            updated_at=s.updated_at,
            cloudinary_public_id=s.cloudinary_public_id,
        )
        for s in synced_items
    ]

    return ProductSyncResponse(synced_count=len(responses), products=responses)
