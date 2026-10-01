from typing import Optional

from fastapi import Request
from sqlalchemy.orm import Session

from backend.models.db_models import ArtisanDB, ProductDB


def get_artisan_from_x_user_id(request: Request, db: Session) -> Optional[ArtisanDB]:
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        return None
    return db.query(ArtisanDB).filter(ArtisanDB.id == user_id).first()


def verify_product_owner(artisan: ArtisanDB, product: ProductDB) -> None:
    if product.artisan_id != artisan.id:
        raise PermissionError("Not authorized to modify this product")
