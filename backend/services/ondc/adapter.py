"""ONDC Retail BPP protocol adapter."""

from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, Optional, List
from sqlalchemy.orm import Session

from ...models.db_models import ProductDB
from ...models.order_models import OrderDB, OrderCreate
from ...models.commerce_models import ChannelType
from ...services.order_service import order_service
from ...services.commerce_service import commerce_service
from .context import extract_context, generate_message_id
from .validators import validate_context, validate_message, ONDCValidationError
from .idempotency import idempotency_store
from .mapper import ONDCMapper

logger = logging.getLogger(__name__)


class ONDCBPPAdapter:
    """Minimal ONDC Retail B2C BPP adapter for Craftsy hackathon demo."""

    def __init__(self) -> None:
        self.mapper = ONDCMapper()

    def search(self, db: Session, request_body: Dict[str, Any]) -> Dict[str, Any]:
        """Handle BAP search request and return ONDC catalog."""
        context = validate_context(request_body.get("context", {}))
        validate_message(request_body, context.action)

        intent = request_body.get("message", {}).get("intent", {})
        query = intent.get("item", {}).get("descriptor", {}).get("name", "")

        products_query = db.query(ProductDB).filter(ProductDB.status == "live")
        if query:
            products_query = products_query.filter(
                ProductDB.title.ilike(f"%{query}%")
                | ProductDB.category.ilike(f"%{query}%")
            )

        products = products_query.limit(20).all()
        catalog = self.mapper.map_products_to_catalog(products)

        return {
            "context": self.mapper.build_context(request_body, "on_search"),
            "message": {"catalog": catalog},
        }

    def select(self, db: Session, request_body: Dict[str, Any]) -> Dict[str, Any]:
        """Handle BAP select request and return quote/order initialization."""
        context = validate_context(request_body.get("context", {}))
        validate_message(request_body, context.action)

        order_data = request_body.get("message", {}).get("order", {})
        items = order_data.get("items", [])

        validated_items, total = self._validate_items(db, items)

        return {
            "context": self.mapper.build_context(request_body, "on_select"),
            "message": {
                "order": {
                    "id": f"ord_{uuid.uuid4().hex[:12]}",
                    "state": "Initialized",
                    "items": validated_items,
                    "quote": {
                        "price": {
                            "currency": "INR",
                            "value": str(round(total, 2)),
                        },
                        "breakup": [
                            {
                                "title": item["descriptor"]["name"],
                                "price": {
                                    "currency": "INR",
                                    "value": str(
                                        round(
                                            float(item["price"]["value"])
                                            * item["quantity"],
                                            2,
                                        )
                                    ),
                                },
                            }
                            for item in validated_items
                        ],
                    },
                },
            },
        }

    def init(self, db: Session, request_body: Dict[str, Any]) -> Dict[str, Any]:
        """Handle BAP init request and return initialized order with payment/fulfillment."""
        context = validate_context(request_body.get("context", {}))
        validate_message(request_body, context.action)

        order_data = request_body.get("message", {}).get("order", {})
        items = order_data.get("items", [])

        validated_items, total = self._validate_items(db, items)

        return {
            "context": self.mapper.build_context(request_body, "on_init"),
            "message": {
                "order": {
                    "id": f"ord_{uuid.uuid4().hex[:12]}",
                    "state": "Initialized",
                    "items": validated_items,
                    "quote": {
                        "price": {
                            "currency": "INR",
                            "value": str(round(total, 2)),
                        },
                    },
                    "payment": {
                        "status": "NOT-PAID",
                        "type": "ON-ORDER",
                        "collected_by": "BAP",
                    },
                    "fulfillment": {
                        "id": "F1",
                        "type": "HOME-DELIVERY",
                        "status": "Active",
                    },
                },
            },
        }

    def confirm(self, db: Session, request_body: Dict[str, Any]) -> Dict[str, Any]:
        """Handle BAP confirm request, create Craftsy order, and return confirmation."""
        context = validate_context(request_body.get("context", {}))
        validate_message(request_body, context.action)

        transaction_id = context.transaction_id
        message_id = context.message_id
        external_order_id = f"ondc_{transaction_id}"

        existing_order_id = idempotency_store.get(transaction_id, message_id)
        if existing_order_id:
            existing_order = (
                db.query(OrderDB).filter(OrderDB.id == existing_order_id).first()
            )
            if existing_order:
                logger.info(
                    "Idempotent confirm: returning existing order %s", existing_order_id
                )
                return self._build_confirm_response(request_body, existing_order)

        existing_by_external = (
            db.query(OrderDB).filter(OrderDB.external_order_id == external_order_id).first()
        )
        if existing_by_external:
            logger.info(
                "External order id already exists: %s", external_order_id
            )
            idempotency_store.set(transaction_id, message_id, existing_by_external.id)
            return self._build_confirm_response(request_body, existing_by_external)

        order_data = request_body.get("message", {}).get("order", {})
        items = order_data.get("items", [])

        validated_items, total = self._validate_items(db, items)

        first_product = (
            db.query(ProductDB).filter(ProductDB.id == validated_items[0]["id"]).first()
            if validated_items
            else None
        )

        buyer_name = (
            order_data.get("billing", {}).get("address", {}).get("name", "ONDC Buyer")
        )
        buyer_location = (
            order_data.get("billing", {}).get("address", {}).get("city", "") or ""
        )

        order_create = OrderCreate(
            artisan_id=first_product.artisan_id if first_product else "",
            product_id=first_product.id if first_product else validated_items[0]["id"],
            product_title=first_product.title if first_product else "ONDC Order",
            product_image_url=first_product.image_url if first_product else "",
            buyer_name=buyer_name,
            buyer_location=buyer_location,
            quantity=sum(item["quantity"] for item in validated_items),
            unit_price=0.0,
            total_amount=round(total, 2),
            channel="ondc",
            external_order_id=external_order_id,
            channel_data={
                "transaction_id": transaction_id,
                "message_id": message_id,
                "bap_id": context.bap_id,
                "items": validated_items,
            },
        )

        order = order_service.create_order(db, order_create)

        product_quantities: Dict[str, int] = {}
        for item in validated_items:
            product_quantities[item["id"]] = (
                product_quantities.get(item["id"], 0) + item["quantity"]
            )

        for product_id, qty in product_quantities.items():
            product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
            if product and product.stock >= qty:
                product.stock -= qty

        db.commit()
        db.refresh(order)

        idempotency_store.set(transaction_id, message_id, order.id)

        try:
            commerce_service._log_audit(
                db,
                order.product_id,
                ChannelType.ONDC,
                "ondc_confirm",
                None,
                "confirmed",
                message=f"ONDC order confirmed: {order.id}",
                success=True,
                external_id=order.external_order_id,
            )
        except Exception:  # noqa: BLE001
            logger.debug("Audit log skipped", exc_info=True)

        return self._build_confirm_response(request_body, order)

    def status(self, db: Session, request_body: Dict[str, Any]) -> Dict[str, Any]:
        """Handle BAP status request and return current order state."""
        context = validate_context(request_body.get("context", {}))
        validate_message(request_body, context.action)

        order_id = request_body.get("message", {}).get("order_id")
        if not order_id:
            raise ONDCValidationError("MISSING_ORDER_ID", "order_id is required")

        order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
        if not order:
            order = db.query(OrderDB).filter(OrderDB.external_order_id == order_id).first()

        if not order:
            raise ONDCValidationError(
                "ORDER_NOT_FOUND", f"Order {order_id} not found"
            )

        return {
            "context": self.mapper.build_context(request_body, "on_status"),
            "message": {
                "order": {
                    "id": order.id,
                    "state": self.mapper.map_order_to_ondc_status(order),
                    "items": [
                        {
                            "id": order.product_id,
                            "quantity": order.quantity,
                            "price": {
                                "currency": "INR",
                                "value": str(round(order.total_amount, 2)),
                            },
                        }
                    ],
                },
            },
        }

    def _validate_items(
        self, db: Session, items: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], float]:
        """Validate items, check stock, and return mapped items with total."""
        if not items:
            raise ONDCValidationError("NO_ITEMS", "No items provided")

        validated_items = []
        total = 0.0

        for item in items:
            product_id = item.get("id")
            if not product_id:
                raise ONDCValidationError("MISSING_PRODUCT_ID", "Item id is required")

            quantity = int(item.get("quantity", 1))
            if quantity < 1:
                raise ONDCValidationError(
                    "INVALID_QUANTITY", "Quantity must be at least 1"
                )

            price = float(item.get("price", {}).get("value", 0))

            product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
            if not product:
                raise ONDCValidationError(
                    "PRODUCT_NOT_FOUND", f"Product {product_id} not found"
                )

            if product.stock < quantity:
                raise ONDCValidationError(
                    "INSUFFICIENT_STOCK",
                    f"Insufficient stock for {product.title}. "
                    f"Available: {product.stock}, Requested: {quantity}",
                )

            validated_items.append(
                {
                    "id": product.id,
                    "descriptor": {
                        "name": product.title,
                        "images": [product.image_url] if product.image_url else [],
                    },
                    "category_id": product.category or "General",
                    "price": {
                        "currency": "INR",
                        "value": str(round(price, 2)),
                    },
                    "quantity": quantity,
                }
            )
            total += price * quantity

        return validated_items, total

    def _build_confirm_response(
        self, request_body: Dict[str, Any], order: OrderDB
    ) -> Dict[str, Any]:
        """Build on_confirm response from an OrderDB."""
        return {
            "context": self.mapper.build_context(request_body, "on_confirm"),
            "message": {
                "order": {
                    "id": order.id,
                    "state": "Created",
                    "items": [
                        {
                            "id": order.product_id,
                            "quantity": order.quantity,
                            "price": {
                                "currency": "INR",
                                "value": str(round(order.total_amount, 2)),
                            },
                        }
                    ],
                    "quote": {
                        "price": {
                            "currency": "INR",
                            "value": str(round(order.total_amount, 2)),
                        },
                    },
                    "payment": {
                        "status": "PAID",
                        "type": "ON-ORDER",
                        "collected_by": "BAP",
                    },
                    "fulfillment": {
                        "id": "F1",
                        "type": "HOME-DELIVERY",
                        "status": "Active",
                    },
                },
            },
        }


ondc_bpp_adapter = ONDCBPPAdapter()
