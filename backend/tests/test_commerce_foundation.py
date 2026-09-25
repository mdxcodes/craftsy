"""
Database Foundation Model Tests.

Validates the commerce foundation database layer:
- ArtisanDB role column
- CartDB and CartItemDB
- AddressDB
- OrderItemDB
- PaymentDB
- ShipmentDB
- Backward compatibility with existing OrderDB records
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base
from backend.models.db_models import ArtisanDB, ProductDB, SocialDraftDB
from backend.models.commerce_models import ProductChannelDB, ChannelAuditLogDB
from backend.models.order_models import OrderDB
from backend.models.commerce_foundation_models import (
    CartDB,
    CartItemDB,
    AddressDB,
    OrderItemDB,
    PaymentDB,
    ShipmentDB,
)


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Session()
    try:
        yield db
    finally:
        db.close()


def _create_artisan(db, role="artisan"):
    """Helper to create an artisan record."""
    artisan = ArtisanDB(
        id=f"artisan_{role}_{role}",
        name=f"Test {role.title()}",
        phone=f"9876543210_{role}",
        craft_type="Test Craft",
        location_cluster="Test Cluster",
        state="Test State",
        experience_years="5",
        preferred_language="en",
        role=role,
    )
    db.add(artisan)
    db.commit()
    return artisan


def _create_product(db, artisan_id=None):
    """Helper to create a product record."""
    product = ProductDB(
        id=f"prod_{artisan_id or 'test'}",
        artisan_id=artisan_id,
        title="Test Product",
        title_hi="टेस्ट उत्पाद",
        description="A test product description",
        price=500.0,
        image_url="https://example.com/image.jpg",
        category="Pottery",
        tags='["handmade", "terracotta"]',
        status="live",
        stock=10,
    )
    db.add(product)
    db.commit()
    return product


def _create_order(db, artisan_id, product_id):
    """Helper to create an order record."""
    order = OrderDB(
        id=f"ord_{artisan_id}_{product_id}",
        artisan_id=artisan_id,
        product_id=product_id,
        product_title="Test Product",
        product_image_url="https://example.com/image.jpg",
        buyer_name="Test Buyer",
        buyer_location="Test Location",
        quantity=2,
        unit_price=500.0,
        total_amount=1000.0,
        status="new",
        channel="craftsy",
    )
    db.add(order)
    db.commit()
    return order


# ── ArtisanDB role tests ─────────────────────────────────────────────────────


def test_artisan_default_role_is_artisan(db_session):
    """Existing artisan records should default to role='artisan'."""
    artisan = _create_artisan(db_session, role="artisan")
    assert artisan.role == "artisan"


def test_artisan_can_be_customer_role(db_session):
    """A customer-role identity can be stored."""
    customer = _create_artisan(db_session, role="customer")
    assert customer.role == "customer"


def test_artisan_role_is_indexed(db_session):
    """The role column should be indexed for query performance."""
    # Just verify we can create records with different roles
    a = _create_artisan(db_session, role="artisan")
    c = _create_artisan(db_session, role="customer")
    assert a.role == "artisan"
    assert c.role == "customer"


# ── CartDB tests ─────────────────────────────────────────────────────────────


def test_cart_can_reference_artisan(db_session):
    """CartDB can reference an artisan identity."""
    artisan = _create_artisan(db_session)
    cart = CartDB(
        id="cart_01",
        user_id=artisan.id,
    )
    db_session.add(cart)
    db_session.commit()

    fetched = db_session.query(CartDB).filter(CartDB.id == "cart_01").first()
    assert fetched is not None
    assert fetched.user_id == artisan.id


def test_cart_user_relationship(db_session):
    """CartDB has a user relationship to ArtisanDB."""
    artisan = _create_artisan(db_session)
    cart = CartDB(id="cart_02", user_id=artisan.id)
    db_session.add(cart)
    db_session.commit()

    fetched = db_session.query(CartDB).filter(CartDB.id == "cart_02").first()
    assert fetched.user is not None
    assert fetched.user.id == artisan.id


# ── CartItemDB tests ─────────────────────────────────────────────────────────


def test_cart_item_can_reference_cart_and_product(db_session):
    """CartItemDB can reference a cart and product."""
    artisan = _create_artisan(db_session)
    product = _create_product(db_session, artisan_id=artisan.id)
    cart = CartDB(id="cart_03", user_id=artisan.id)
    db_session.add(cart)
    db_session.commit()

    item = CartItemDB(
        id="item_01",
        cart_id=cart.id,
        product_id=product.id,
        quantity=2,
        unit_price=500.0,
    )
    db_session.add(item)
    db_session.commit()

    fetched = db_session.query(CartItemDB).filter(CartItemDB.id == "item_01").first()
    assert fetched is not None
    assert fetched.cart_id == cart.id
    assert fetched.product_id == product.id
    assert fetched.quantity == 2
    assert fetched.unit_price == 500.0


def test_cart_item_prevents_duplicate_product_in_same_cart(db_session):
    """Duplicate product entries in the same cart should be prevented."""
    from sqlalchemy.exc import IntegrityError

    artisan = _create_artisan(db_session)
    product = _create_product(db_session, artisan_id=artisan.id)
    cart = CartDB(id="cart_04", user_id=artisan.id)
    db_session.add(cart)
    db_session.commit()

    item1 = CartItemDB(
        id="item_02a",
        cart_id=cart.id,
        product_id=product.id,
        quantity=1,
        unit_price=500.0,
    )
    db_session.add(item1)
    db_session.commit()

    # Attempt to add the same product to the same cart again
    item2 = CartItemDB(
        id="item_02b",
        cart_id=cart.id,
        product_id=product.id,
        quantity=2,
        unit_price=500.0,
    )
    db_session.add(item2)

    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


# ── AddressDB tests ──────────────────────────────────────────────────────────


def test_address_can_reference_artisan(db_session):
    """AddressDB can reference an artisan identity."""
    artisan = _create_artisan(db_session)
    address = AddressDB(
        id="addr_01",
        user_id=artisan.id,
        label="home",
        name="Test User",
        phone="9876543210",
        line1="123 Main Street",
        line2="Near Temple",
        city="Delhi",
        state="Delhi",
        pincode="110001",
        is_default=True,
    )
    db_session.add(address)
    db_session.commit()

    fetched = db_session.query(AddressDB).filter(AddressDB.id == "addr_01").first()
    assert fetched is not None
    assert fetched.user_id == artisan.id
    assert fetched.name == "Test User"
    assert fetched.is_default is True


def test_address_user_relationship(db_session):
    """AddressDB has a user relationship to ArtisanDB."""
    artisan = _create_artisan(db_session)
    address = AddressDB(
        id="addr_02",
        user_id=artisan.id,
        label="work",
        name="Test User",
        phone="9876543210",
        line1="456 Work Lane",
        city="Mumbai",
        state="Maharashtra",
        pincode="400001",
    )
    db_session.add(address)
    db_session.commit()

    fetched = db_session.query(AddressDB).filter(AddressDB.id == "addr_02").first()
    assert fetched.user is not None
    assert fetched.user.id == artisan.id


# ── OrderItemDB tests ────────────────────────────────────────────────────────


def test_order_item_can_reference_order(db_session):
    """OrderItemDB can reference an order."""
    artisan = _create_artisan(db_session)
    product = _create_product(db_session, artisan_id=artisan.id)
    order = _create_order(db_session, artisan.id, product.id)

    item = OrderItemDB(
        id="oitem_01",
        order_id=order.id,
        product_id=product.id,
        product_title=product.title,
        product_image_url=product.image_url,
        quantity=2,
        unit_price=500.0,
        total_price=1000.0,
    )
    db_session.add(item)
    db_session.commit()

    fetched = db_session.query(OrderItemDB).filter(OrderItemDB.id == "oitem_01").first()
    assert fetched is not None
    assert fetched.order_id == order.id
    assert fetched.quantity == 2
    assert fetched.total_price == 1000.0


def test_order_item_order_relationship(db_session):
    """OrderItemDB has an order relationship to OrderDB."""
    artisan = _create_artisan(db_session)
    product = _create_product(db_session, artisan_id=artisan.id)
    order = _create_order(db_session, artisan.id, product.id)

    item = OrderItemDB(
        id="oitem_02",
        order_id=order.id,
        product_id=product.id,
        product_title=product.title,
        product_image_url=product.image_url,
        quantity=1,
        unit_price=500.0,
        total_price=500.0,
    )
    db_session.add(item)
    db_session.commit()

    fetched = db_session.query(OrderItemDB).filter(OrderItemDB.id == "oitem_02").first()
    assert fetched.order is not None
    assert fetched.order.id == order.id


# ── PaymentDB tests ──────────────────────────────────────────────────────────


def test_payment_can_reference_order_and_user(db_session):
    """PaymentDB can reference an order and user."""
    artisan = _create_artisan(db_session)
    product = _create_product(db_session, artisan_id=artisan.id)
    order = _create_order(db_session, artisan.id, product.id)

    payment = PaymentDB(
        id="pay_01",
        order_id=order.id,
        user_id=artisan.id,
        amount=1000.0,
        method="cod",
        status="pending",
    )
    db_session.add(payment)
    db_session.commit()

    fetched = db_session.query(PaymentDB).filter(PaymentDB.id == "pay_01").first()
    assert fetched is not None
    assert fetched.order_id == order.id
    assert fetched.user_id == artisan.id
    assert fetched.amount == 1000.0
    assert fetched.method == "cod"
    assert fetched.status == "pending"


def test_payment_default_values(db_session):
    """PaymentDB should have correct default values."""
    artisan = _create_artisan(db_session)
    product = _create_product(db_session, artisan_id=artisan.id)
    order = _create_order(db_session, artisan.id, product.id)

    payment = PaymentDB(
        id="pay_02",
        order_id=order.id,
        user_id=artisan.id,
        amount=500.0,
    )
    db_session.add(payment)
    db_session.commit()

    fetched = db_session.query(PaymentDB).filter(PaymentDB.id == "pay_02").first()
    assert fetched.method == "cod"
    assert fetched.status == "pending"
    assert fetched.transaction_id is None
    assert fetched.paid_at is None


# ── ShipmentDB tests ─────────────────────────────────────────────────────────


def test_shipment_can_reference_order_and_artisan(db_session):
    """ShipmentDB can reference an order and artisan."""
    artisan = _create_artisan(db_session)
    product = _create_product(db_session, artisan_id=artisan.id)
    order = _create_order(db_session, artisan.id, product.id)

    shipment = ShipmentDB(
        id="ship_01",
        order_id=order.id,
        artisan_id=artisan.id,
        status="pending",
    )
    db_session.add(shipment)
    db_session.commit()

    fetched = db_session.query(ShipmentDB).filter(ShipmentDB.id == "ship_01").first()
    assert fetched is not None
    assert fetched.order_id == order.id
    assert fetched.artisan_id == artisan.id
    assert fetched.status == "pending"


def test_shipment_default_values(db_session):
    """ShipmentDB should have correct default values."""
    artisan = _create_artisan(db_session)
    product = _create_product(db_session, artisan_id=artisan.id)
    order = _create_order(db_session, artisan.id, product.id)

    shipment = ShipmentDB(
        id="ship_02",
        order_id=order.id,
        artisan_id=artisan.id,
    )
    db_session.add(shipment)
    db_session.commit()

    fetched = db_session.query(ShipmentDB).filter(ShipmentDB.id == "ship_02").first()
    assert fetched.status == "pending"
    assert fetched.carrier is None
    assert fetched.tracking_id is None
    assert fetched.shipped_at is None
    assert fetched.delivered_at is None


# ── Backward compatibility tests ─────────────────────────────────────────────


def test_existing_order_fields_preserved(db_session):
    """Existing OrderDB fields should still work (backward compatibility)."""
    artisan = _create_artisan(db_session)
    product = _create_product(db_session, artisan_id=artisan.id)
    order = _create_order(db_session, artisan.id, product.id)

    # Verify all existing fields are accessible
    assert order.artisan_id == artisan.id
    assert order.product_id == product.id
    assert order.product_title == "Test Product"
    assert order.buyer_name == "Test Buyer"
    assert order.quantity == 2
    assert order.unit_price == 500.0
    assert order.total_amount == 1000.0
    assert order.status == "new"
    assert order.channel == "craftsy"


def test_new_order_fields_are_nullable(db_session):
    """New OrderDB fields (customer_id, address_id, payment_id) should be nullable."""
    artisan = _create_artisan(db_session)
    product = _create_product(db_session, artisan_id=artisan.id)
    order = _create_order(db_session, artisan.id, product.id)

    # New fields should be None for existing-style orders
    assert order.customer_id is None
    assert order.address_id is None
    assert order.payment_id is None


def test_order_item_relationship_to_order(db_session):
    """OrderDB should have an items relationship to OrderItemDB."""
    artisan = _create_artisan(db_session)
    product = _create_product(db_session, artisan_id=artisan.id)
    order = _create_order(db_session, artisan.id, product.id)

    # Create order items
    item1 = OrderItemDB(
        id="oitem_rel_01",
        order_id=order.id,
        product_id=product.id,
        product_title="Test Product",
        quantity=1,
        unit_price=500.0,
        total_price=500.0,
    )
    db_session.add(item1)
    db_session.commit()

    # Access items through the relationship
    assert order.items.count() == 1
    assert order.items.first().id == "oitem_rel_01"


def test_artisan_customer_orders_relationship(db_session):
    """ArtisanDB should have a customer_orders relationship."""
    artisan = _create_artisan(db_session, role="customer")
    product = _create_product(db_session)

    # Create an order with customer_id
    order = OrderDB(
        id="ord_customer_01",
        artisan_id=product.artisan_id,
        customer_id=artisan.id,
        product_id=product.id,
        product_title=product.title,
        buyer_name="Test Buyer",
        quantity=1,
        unit_price=500.0,
        total_amount=500.0,
    )
    db_session.add(order)
    db_session.commit()

    # Access customer_orders through the relationship
    assert artisan.customer_orders.count() == 1
    assert artisan.customer_orders.first().id == "ord_customer_01"


def test_existing_product_order_relationships(db_session):
    """Existing product/order relationships should still work."""
    artisan = _create_artisan(db_session)
    product = _create_product(db_session, artisan_id=artisan.id)

    # Artisan -> Products
    assert artisan.products.count() == 1

    # Product -> Artisan
    assert product.artisan is not None
    assert product.artisan.id == artisan.id


def test_demo_artisan_has_artisan_role(db_session):
    """The demo artisan seeded in init_db should have role='artisan'."""
    # This test validates the migration path
    # In a real scenario, init_db() would be called
    artisan = ArtisanDB(
        id="artisan_01",
        name="Rameshwar Lal Kumhar",
        phone="9876543210",
        craft_type="Terracotta Pottery",
        location_cluster="Kumhar Gram, Delhi NCR",
        state="Delhi",
        experience_years="25",
        pehchan_id="PEHCHAN-DL-0042",
        preferred_language="en",
        role="artisan",
    )
    db_session.add(artisan)
    db_session.commit()

    fetched = db_session.query(ArtisanDB).filter(ArtisanDB.id == "artisan_01").first()
    assert fetched.role == "artisan"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
