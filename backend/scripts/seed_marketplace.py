"""
Seed script: upsert 20 marketplace products for the test artisan
(phone 9876543210 / id artisan_01).

Usage:
    # Local SQLite (default)
    python scripts/seed_marketplace.py

    # Railway / PostgreSQL
    DATABASE_URL=postgresql://user:pass@host:5432/dbname python scripts/seed_marketplace.py

The script reuses the app's existing database configuration so it works
with both SQLite and PostgreSQL without code changes.
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Ensure backend package is importable when running from repo root
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from backend.database import SessionLocal, IS_SQLITE, IS_POSTGRES  # noqa: E402

# Import all model modules so SQLAlchemy registers every table/relationship
# before we query ArtisanDB / ProductDB. Order matters for circular deps.
from backend.models.db_models import ArtisanDB, ProductDB, SocialDraftDB  # noqa: E402
from backend.models.commerce_models import ProductChannelDB, ChannelAuditLogDB  # noqa: E402
from backend.models.order_models import OrderDB  # noqa: E402
from backend.models.commerce_foundation_models import (  # noqa: E402
    CartDB,
    CartItemDB,
    AddressDB,
    OrderItemDB,
    PaymentDB,
    ShipmentDB,
)


DEMO_PHONE = "9876543210"
DEMO_ARTISAN_ID = "artisan_01"
DEMO_ARTISAN_NAME = "Rameshwar Lal Kumhar"

BASE_TIME = datetime.now(timezone.utc)


PRODUCTS = [
    ("prod_dupatta_01", "Handwoven Cotton Dupatta", "A beautifully handwoven cotton dupatta featuring traditional geometric patterns. Lightweight and breathable, perfect for everyday wear.", "Textiles", 899, 25, ["craftsy"]),
    ("prod_vase_02", "Terracotta Decorative Vase", "Handcrafted terracotta vase with intricate tribal motifs. Each piece is unique, shaped on the potter's wheel and fired in a traditional kiln.", "Pottery", 1450, 12, ["craftsy"]),
    ("prod_tray_03", "Hand-Painted Wooden Tray", "A sturdy wooden tray hand-painted with vibrant Madhubani art patterns. Perfect for serving snacks or as a decorative wall piece.", "Woodwork", 650, 18, ["craftsy"]),
    ("prod_panel_04", "Madhubani Art Panel", "Traditional Madhubani painting on handmade paper. Features nature-inspired motifs including fish, birds, and floral patterns. Ready to frame.", "Paintings", 2200, 8, ["craftsy"]),
    ("prod_basket_05", "Bamboo Storage Basket", "Eco-friendly bamboo storage basket with sturdy weave. Ideal for storing clothes, toys, or kitchen essentials. Natural and chemical-free.", "Bamboo & Cane", 450, 30, ["craftsy"]),
    ("prod_bag_06", "Handloom Jute Shopping Bag", "Durable handloom jute bag with traditional Assamese motifs. Strong handles, spacious interior, and a sturdy base for daily use.", "Textiles", 450, 25, ["craftsy"]),
    ("prod_clay_07", "Blue Pottery Dinner Plate Set", "Set of 6 hand-painted blue pottery plates. Food-safe glaze, dishwasher friendly, and each piece has subtle variations that prove it's handmade.", "Pottery", 1200, 15, ["craftsy"]),
    ("prod_scarf_08", "Handblock Print Cotton Scarf", "Soft cotton scarf with natural dye block prints inspired by rural Rajasthan. Light enough for summer, warm enough for winter evenings.", "Textiles", 650, 30, ["craftsy"]),
    ("prod_earring_09", "Silver Terracotta Earrings", "Lightweight terracotta stud earrings with silver plating. Hypoallergenic and comfortable for all-day wear.", "Jewelry", 380, 40, ["craftsy"]),
    ("prod_box_10", "Carved Teakwood Jewelry Box", "Hand-carved teakwood box with brass inlay. Multiple compartments for rings, earrings, and necklaces. A timeless gift.", "Woodwork", 2200, 10, ["craftsy"]),
    ("prod_mat_11", "Handwoven Coir Door Mat", "Eco-friendly coir mat with geometric border design. Naturally water-resistant and tough enough for daily foot traffic.", "Textiles", 520, 35, ["craftsy"]),
    ("prod_lamp_12", "Brass Diya Table Lamp", "Traditional brass diya-shaped lamp with fabric shade. Warm ambient light perfect for pooja rooms, bedrooms, or living rooms.", "Metalwork", 1800, 12, ["craftsy"]),
    ("prod_quilt_13", "Handstitched Cotton Quilt", "Queen-size quilt with hand-stitched kantha embroidery. Soft cotton fill, reversible design, and gets softer with every wash.", "Textiles", 3500, 8, ["craftsy"]),
    ("prod_bowl_14", "Terracotta Serving Bowl Set", "Set of 4 nested terracotta bowls, food-safe and microwave friendly. Perfect for serving snacks, salads, or desserts.", "Pottery", 890, 20, ["craftsy"]),
    ("prod_wallet_15", "Handtooled Leather Wallet", "Full-grain leather wallet with handtooled floral pattern. Multiple card slots, RFID-blocking liner, and a slim profile.", "Leather", 950, 18, ["craftsy"]),
    ("prod_incense_16", "Natural Incense Stick Pack", "Hand-rolled incense with sandalwood and jasmine. Bamboo-free, charcoal-free, and packaged in a reusable glass jar.", "Wellness", 280, 50, ["craftsy"]),
    ("prod_statue_17", "Brass Dancing Nataraja", "Classic brass statue with antique finish. Handcrafted using the lost-wax method in Thanjavur. A statement piece for any shelf.", "Metalwork", 4500, 5, ["craftsy"]),
    ("prod_cushion_18", "Embroidered Cushion Cover", "Cotton cushion cover with zari embroidery. Hidden zipper closure, fits standard 16x16 inserts. Sold as a set of 2.", "Textiles", 420, 28, ["craftsy"]),
    ("prod_plate_19", "Kalamkari Wall Plate", "Hand-painted kalamkari art on a decorative plate. Mounted on a wooden stand. Each design is drawn with a bamboo stylus and natural dyes.", "Art", 1600, 10, ["craftsy"]),
    ("prod_stand_20", "Bamboo Plant Stand", "Foldable bamboo stand for indoor plants. Tool-free assembly, adjustable height, and a natural finish that suits any decor.", "Woodwork", 750, 22, ["craftsy"]),
]


def ensure_artisan(db: Session) -> str:
    artisan = db.query(ArtisanDB).filter(ArtisanDB.phone == DEMO_PHONE).first()
    if artisan:
        return artisan.id

    artisan = ArtisanDB(
        id=DEMO_ARTISAN_ID,
        name=DEMO_ARTISAN_NAME,
        phone=DEMO_PHONE,
        craft_type="Terracotta Pottery",
        location_cluster="Kumhar Gram, Delhi NCR",
        state="Delhi",
        experience_years="25",
        pehchan_id="PEHCHAN-DL-0042",
        preferred_language="en",
        role="artisan",
        created_at=datetime.now(timezone.utc),
    )
    db.add(artisan)
    db.flush()
    return artisan.id


def upsert_products(db: Session, artisan_id: str) -> int:
    upserted = 0
    for idx, (pid, title, description, category, price, stock, platforms) in enumerate(PRODUCTS, start=1):
        created_at = BASE_TIME - timedelta(days=idx)
        existing = db.get(ProductDB, pid)
        if existing:
            existing.artisan_id = artisan_id
            existing.title = title
            existing.description = description
            existing.price = float(price)
            existing.image_url = f"/uploads/images/{pid}.jpg"
            existing.category = category
            existing.tags = json.dumps([category.lower().replace(" ", "_"), "handmade", "artisan"])
            existing.status = "live"
            existing.stock = int(stock)
            existing.platforms = json.dumps(platforms)
            existing.updated_at = datetime.now(timezone.utc)
        else:
            product = ProductDB(
                id=pid,
                artisan_id=artisan_id,
                title=title,
                title_hi="",
                description=description,
                description_hi="",
                price=float(price),
                image_url=f"/uploads/images/{pid}.jpg",
                cloudinary_public_id=None,
                category=category,
                tags=json.dumps([category.lower().replace(" ", "_"), "handmade", "artisan"]),
                status="live",
                stock=int(stock),
                platforms=json.dumps(platforms),
                created_at=created_at,
                updated_at=created_at,
            )
            db.add(product)
        upserted += 1
    return upserted


def main() -> int:
    print(f"Database: {'SQLite' if IS_SQLITE else 'PostgreSQL' if IS_POSTGRES else 'unknown'}")
    db = SessionLocal()
    try:
        artisan_id = ensure_artisan(db)
        db.commit()
        print(f"Artisan ready: {artisan_id}")

        count = upsert_products(db, artisan_id)
        db.commit()
        print(f"Upserted {count} products for artisan {artisan_id}.")

        total = db.query(ProductDB).filter(ProductDB.status == "live").count()
        artisan_count = db.query(ProductDB).filter(ProductDB.artisan_id == artisan_id, ProductDB.status == "live").count()
        print(f"Total live products: {total}")
        print(f"Artisan live products: {artisan_count}")
        return 0
    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
