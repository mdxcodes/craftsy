"""
Database Configuration and Session Management.

Database-agnostic by design:
    - Local development : SQLite (`DATABASE_URL=sqlite:///...` or the default).
    - Production        : PostgreSQL (`DATABASE_URL=postgresql://...`).

The engine is always built from `DATABASE_URL`, so the application is never
hard-wired to a single database implementation. SQLite-only upgrade helpers
run *only* when the active dialect is SQLite.
"""

import json
import logging
from typing import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from .config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

DATABASE_URL = settings.resolved_database_url
IS_SQLITE = DATABASE_URL.startswith("sqlite")
IS_POSTGRES = DATABASE_URL.startswith("postgresql")


def _build_engine() -> Engine:
    """Create the SQLAlchemy engine with dialect-appropriate options."""
    common_kwargs: dict = {
        "echo": bool(settings.database_echo or settings.debug),
        "future": True,
    }

    if IS_SQLITE:
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            **common_kwargs,
        )
    elif IS_POSTGRES:
        # pool_pre_ping recovers stale connections after Railway idle/restart;
        # pool_recycle keeps connections below managed-Postgres idle limits.
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=1800,
            **common_kwargs,
        )
    else:
        engine = create_engine(DATABASE_URL, **common_kwargs)

    return engine


try:
    engine = _build_engine()
except ModuleNotFoundError as exc:
    # Most likely the PostgreSQL driver is missing.
    raise ModuleNotFoundError(
        f"Could not create the database engine for '{DATABASE_URL.split('://')[0]}://...'. "
        "If you are deploying to Railway with PostgreSQL, install the driver "
        "(`pip install psycopg2-binary`). Original error: "
        f"{exc}"
    ) from exc

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """FastAPI Dependency for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def describe_database() -> str:
    """Human-readable description of the active database backend."""
    if IS_SQLITE:
        return "SQLite (local development)"
    if IS_POSTGRES:
        return "PostgreSQL"
    return engine.dialect.name


def check_database_connection() -> tuple[bool, str]:
    """Lightweight readiness probe.

    Executes `SELECT 1` and returns (ok, detail). Never raises, never touches
    external AI services. Used by the readiness health endpoint.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "ok"
    except Exception as exc:  # noqa: BLE001 - report, do not crash
        logger.error("Database connection check failed: %s", exc)
        return False, str(exc)


def _run_schema_migrations(engine: Engine) -> None:
    """Run dialect-appropriate schema migrations for existing tables.

    SQLite: add missing columns via ALTER TABLE.
    PostgreSQL: adjust column nullability via ALTER TABLE.
    """
    dialect = engine.dialect.name
    if dialect not in {"sqlite", "postgresql"}:
        return

    inspector = inspect(engine)
    existing_tables = {t for t in inspector.get_table_names()}

    with engine.connect() as conn:
        # ── ArtisanDB.name nullable ─────────────────────────────────────────────
        if "artisans" in existing_tables:
            existing_cols = {c["name"] for c in inspector.get_columns("artisans")}
            if dialect == "sqlite" and "name" not in existing_cols:
                conn.execute(text("ALTER TABLE artisans ADD COLUMN name VARCHAR(255)"))
            elif dialect == "postgresql":
                conn.execute(text("ALTER TABLE artisans ALTER COLUMN name DROP NOT NULL"))

        # ── ArtisanDB.role (SQLite only) ────────────────────────────────────────
        if "artisans" in existing_tables:
            existing_cols = {c["name"] for c in inspector.get_columns("artisans")}
            if dialect == "sqlite" and "role" not in existing_cols:
                conn.execute(
                    text("ALTER TABLE artisans ADD COLUMN role VARCHAR(32) DEFAULT 'artisan' NOT NULL")
                )

        # ── OrderDB new columns ─────────────────────────────────────────────────
        if "orders" in existing_tables:
            order_cols = {c["name"] for c in inspector.get_columns("orders")}
            migrations = [
                ("customer_id", "VARCHAR(64)"),
                ("payment_id", "VARCHAR(64)"),
                ("address_id", "VARCHAR(64)"),
            ]
            for col_name, col_type in migrations:
                if col_name not in order_cols:
                    conn.execute(text(f"ALTER TABLE orders ADD COLUMN {col_name} {col_type}"))

        # ── ProductDB Cloudinary columns ────────────────────────────────────────
        if "products" in existing_tables:
            product_cols = {c["name"] for c in inspector.get_columns("products")}
            if "cloudinary_public_id" not in product_cols:
                conn.execute(
                    text("ALTER TABLE products ADD COLUMN cloudinary_public_id VARCHAR(255)")
                )

        conn.commit()


def init_db() -> None:
    """Create all tables and ensure the demo artisan exists.

    Safe to run against SQLite and PostgreSQL. All model modules are imported
    here so SQLAlchemy registers every table with `Base.metadata` before DDL.
    """
    # Import models so SQLAlchemy registers them with Base.metadata
    from .models.db_models import ArtisanDB, ProductDB, SocialDraftDB  # noqa: F401
    from .models.commerce_models import ProductChannelDB, ChannelAuditLogDB  # noqa: F401
    from .models.order_models import OrderDB  # noqa: F401
    from .models.commerce_foundation_models import (  # noqa: F401
        CartDB,
        CartItemDB,
        AddressDB,
        OrderItemDB,
        PaymentDB,
        ShipmentDB,
    )
    from datetime import datetime

    if settings.is_production and IS_SQLITE:
        logger.warning(
            "PRODUCTION is running on SQLite (%s). Railway's filesystem is ephemeral — "
            "set DATABASE_URL to the PostgreSQL connection string before going live.",
            DATABASE_URL,
        )
    elif not IS_SQLITE and not IS_POSTGRES:
        logger.warning("Unrecognised database dialect for URL scheme: %s", DATABASE_URL.split("://")[0])

    Base.metadata.create_all(bind=engine)

    _run_schema_migrations(engine)

    # Ensure demo artisan exists so demo login and FK constraints always succeed
    db = SessionLocal()
    try:
        demo_phone = "9876543210"
        existing = db.query(ArtisanDB).filter(ArtisanDB.phone == demo_phone).first()
        if existing:
            demo_artisan = existing
        else:
            demo_artisan = ArtisanDB(
                id="artisan_01",
                name="Rameshwar Lal Kumhar",
                phone=demo_phone,
                craft_type="Terracotta Pottery",
                location_cluster="Kumhar Gram, Delhi NCR",
                state="Delhi",
                experience_years="25",
                pehchan_id="PEHCHAN-DL-0042",
                preferred_language="en",
                role="artisan",
                created_at=datetime.now(),
            )
            db.add(demo_artisan)
            db.commit()

        seed_demo_products(db, demo_artisan.id)
    except Exception as e:
        db.rollback()
        logger.warning("Could not seed demo data: %s", e)
    finally:
        db.close()


def seed_demo_products(db: Session, artisan_id: str) -> None:
    """Seed initial marketplace catalog products for demo/testing."""
    from .models.db_models import ProductDB

    existing_count = db.query(ProductDB).filter(ProductDB.artisan_id == artisan_id).count()
    if existing_count > 0:
        return

    demo_products = [
        {
            "id": "prod_dupatta_01",
            "artisan_id": artisan_id,
            "title": "Handwoven Cotton Dupatta",
            "title_hi": "हाथ से बुना हुआ कॉटन दुपट्टा",
            "description": "A beautifully handwoven cotton dupatta featuring traditional geometric patterns. Lightweight and breathable, perfect for everyday wear.",
            "description_hi": "पारंपरिक ज्यामितीय पैटर्न वाला सुंदर हाथ से बुना हुआ कॉटन दुपट्टा। हल्का और श्वसन योग्य, रोजमर्रा के लिए उपयुक्त।",
            "price": 899.0,
            "image_url": "/uploads/images/dupatta_demo.jpg",
            "category": "Textiles",
            "tags": ["handwoven", "cotton", "dupatta", "traditional"],
            "status": "live",
            "stock": 25,
        },
        {
            "id": "prod_vase_02",
            "artisan_id": artisan_id,
            "title": "Terracotta Decorative Vase",
            "title_hi": "टेराकोटा सजावटी फूलदान",
            "description": "Handcrafted terracotta vase with intricate tribal motifs. Each piece is unique, shaped on the potter's wheel and fired in a traditional kiln.",
            "description_hi": "जटिल जनजातीय अलंकारों वाली हाथ से बनी टेराकोटा फूलदान। प्रत्येक टुकड़ा अद्वितीय है, कुम्हार के चाकी पर आकार दिया गया है और पारंपरिक भट्ठी में पकाया गया है।",
            "price": 1450.0,
            "image_url": "/uploads/images/vase_demo.jpg",
            "category": "Pottery",
            "tags": ["terracotta", "vase", "handcrafted", "pottery"],
            "status": "live",
            "stock": 12,
        },
        {
            "id": "prod_tray_03",
            "artisan_id": artisan_id,
            "title": "Hand-Painted Wooden Tray",
            "title_hi": "हाथ से पेंट किया हुआ लकड़ी का ट्रे",
            "description": "A sturdy wooden tray hand-painted with vibrant Madhubani art patterns. Perfect for serving snacks or as a decorative wall piece.",
            "description_hi": "जीवंत मधुबनी कला पैटर्न से हाथ से पेंट किया हुआ मजबूत लकड़ी का ट्रे। स्नैक्स परोसने या सजावटी दीवार के टुकड़े के रूप में उपयुक्त।",
            "price": 650.0,
            "image_url": "/uploads/images/tray_demo.jpg",
            "category": "Woodwork",
            "tags": ["wooden", "tray", "madhubani", "hand-painted"],
            "status": "live",
            "stock": 18,
        },
        {
            "id": "prod_panel_04",
            "artisan_id": artisan_id,
            "title": "Madhubani Art Panel",
            "title_hi": "मधुबनी कला पैनल",
            "description": "Traditional Madhubani painting on handmade paper. Features nature-inspired motifs including fish, birds, and floral patterns. Ready to frame.",
            "description_hi": "हाथ से बनے कागज पर पारंपरिक मधुबनी चित्रकला। मछली, पक्षी और फूलों के पैटर्न सहित प्रकृति से प्रेरित अलंकार शामिल हैं। फ्रेम करने के लिए तैयार।",
            "price": 2200.0,
            "image_url": "/uploads/images/panel_demo.jpg",
            "category": "Paintings",
            "tags": ["madhubani", "painting", "handmade", "art"],
            "status": "live",
            "stock": 8,
        },
        {
            "id": "prod_basket_05",
            "artisan_id": artisan_id,
            "title": "Bamboo Storage Basket",
            "title_hi": "बांस का भंडारण टोकरी",
            "description": "Eco-friendly bamboo storage basket with sturdy weave. Ideal for storing clothes, toys, or kitchen essentials. Natural and chemical-free.",
            "description_hi": "मजबूत बुनाई वाली पर्यावरण के अनुकूल बांस की भंडारण टोकरी। कपड़े, खिलौने या किचन सामान स्टोर करने के लिए आदर्श। प्राकृतिक और रसायन मुक्त।",
            "price": 450.0,
            "image_url": "/uploads/images/basket_demo.jpg",
            "category": "Bamboo & Cane",
            "tags": ["bamboo", "basket", "storage", "eco-friendly"],
            "status": "live",
            "stock": 30,
        },
    ]

    for product_data in demo_products:
        product = ProductDB(
            id=product_data["id"],
            artisan_id=product_data["artisan_id"],
            title=product_data["title"],
            title_hi=product_data["title_hi"],
            description=product_data["description"],
            description_hi=product_data["description_hi"],
            price=product_data["price"],
            image_url=product_data["image_url"],
            category=product_data["category"],
            tags=json.dumps(product_data["tags"]),
            status=product_data["status"],
            stock=product_data["stock"],
            created_at=datetime.now(),
        )
        db.add(product)

    db.commit()
