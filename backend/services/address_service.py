"""
Address Service.

Manages user address operations.
"""

from __future__ import annotations

import uuid
import logging
from typing import Optional, List
from sqlalchemy.orm import Session

from ..models.commerce_foundation_models import AddressDB

logger = logging.getLogger(__name__)


class AddressService:
    """Manages user address operations."""

    def list_addresses(self, db: Session, user_id: str) -> List[AddressDB]:
        """Get all addresses for a user."""
        return db.query(AddressDB).filter(AddressDB.user_id == user_id).all()

    def get_address(self, db: Session, address_id: str, user_id: str) -> Optional[AddressDB]:
        """Get a specific address, verifying ownership."""
        return db.query(AddressDB).filter(
            AddressDB.id == address_id,
            AddressDB.user_id == user_id,
        ).first()

    def create_address(
        self,
        db: Session,
        user_id: str,
        label: str,
        name: str,
        phone: str,
        line1: str,
        line2: str = "",
        city: str = "",
        state: str = "",
        pincode: str = "",
        is_default: bool = False,
    ) -> AddressDB:
        """Create a new address for a user."""
        address = AddressDB(
            id=f"addr_{uuid.uuid4().hex[:12]}",
            user_id=user_id,
            label=label,
            name=name,
            phone=phone,
            line1=line1,
            line2=line2,
            city=city,
            state=state,
            pincode=pincode,
            is_default=is_default,
        )
        db.add(address)
        db.commit()
        db.refresh(address)
        return address

    def update_address(
        self,
        db: Session,
        address_id: str,
        user_id: str,
        **updates,
    ) -> Optional[AddressDB]:
        """Update an address, verifying ownership."""
        address = self.get_address(db, address_id, user_id)
        if not address:
            return None

        allowed_fields = {
            "label", "name", "phone", "line1", "line2",
            "city", "state", "pincode", "is_default",
        }
        for field, value in updates.items():
            if field in allowed_fields and value is not None:
                setattr(address, field, value)

        db.commit()
        db.refresh(address)
        return address

    def delete_address(self, db: Session, address_id: str, user_id: str) -> bool:
        """Delete an address, verifying ownership."""
        address = self.get_address(db, address_id, user_id)
        if not address:
            return False

        db.delete(address)
        db.commit()
        return True


# ── Singleton ────────────────────────────────────────────────────────────────

address_service = AddressService()
