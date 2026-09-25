"""
Database Configuration and Session Management.

Database-agnostic by design:
    - Local development : SQLite (`DATABASE_URL=sqlite:///...` or the default).
    - Production        : PostgreSQL (`DATABASE_URL=postgresql://...`).

The engine is always built from `DATABASE_URL`, so the application is never
hard-wired to a single database implementation. SQLite-only upgrade helpers
run *only* when the active dialect is SQLite.
"""

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


def _migrate_sqlite_columns(engine: Engine) -> None:
    """Add new columns to existing SQLite tables if they are missing.

    SQLite's Base.metadata.create_all() only creates missing tables.
    It does NOT add new columns to existing tables. This function
    manually checks for and adds columns that may be missing from
    a pre-existing craftsy.db file.

    This runs ONLY for SQLite. PostgreSQL never executes these statements.
    """
    if not str(engine.url).startswith("sqlite"):
        return

    inspector = inspect(engine)
    existing_tables = {t for t in inspector.get_table_names()}

    # Use a raw connection for DDL (ALTER TABLE) — no ORM session needed
    with engine.connect() as conn:
        # ── ArtisanDB.role ───────────────────────────────────────────────────
        if "artisans" in existing_tables:
            existing_cols = {c["name"] for c in inspector.get_columns("artisans")}
            if "role" not in existing_cols:
                conn.execute(
                    text("ALTER TABLE artisans ADD COLUMN role VARCHAR(32) DEFAULT 'artisan' NOT NULL")
                )

        # ── OrderDB new columns ───────────────────────────────────────────────
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

    # ── SQLite migrations for existing databases ──────────────────────────────
    # SQLite's create_all only creates missing tables; it does NOT add new
    # columns to existing tables. We manually add columns that may be missing
    # from a pre-existing craftsy.db file. Guarded to SQLite only.
    _migrate_sqlite_columns(engine)

    # Ensure demo artisan exists so demo login and FK constraints always succeed
    db = SessionLocal()
    try:
        demo_phone = "9876543210"
        existing = db.query(ArtisanDB).filter(ArtisanDB.phone == demo_phone).first()
        if not existing:
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
    except Exception as e:
        db.rollback()
        logger.warning("Could not seed demo artisan: %s", e)
    finally:
        db.close()
