# CRAFTSY — PHASE 1.1: DATABASE IMPLEMENTATION REPORT

**Generated:** 2026-09-24
**Status:** COMPLETE
**Repository:** `/secondary/craftsy`
**Branch:** `feature/bhavya-selective-integration`

---

## 1. Summary

Successfully implemented the database/model portion of Phase 1 Commerce Foundation. The implementation adds 6 new tables and extends 2 existing tables to support unified identity, cart, addresses, order items, payments, and shipments — while preserving all existing artisan functionality.

**Result:** 21 new tests pass, 69 total backend tests pass (3 pre-existing failures unchanged).

---

## 2. Files Changed

| File | Action | Lines |
|------|--------|-------|
| `backend/models/commerce_foundation_models.py` | **NEW** | 243 |
| `backend/models/db_models.py` | Modified | +8 |
| `backend/models/order_models.py` | Modified | +22 |
| `backend/database.py` | Modified | +30 |
| `backend/tests/test_commerce_foundation.py` | **NEW** | 483 |

**Total:** 5 files changed, 786 lines added/modified.

---

## 3. Models Added

### 3.1 CartDB (`carts` table)

| Field | Type | Constraints |
|-------|------|-------------|
| id | String(64) | PK, indexed |
| user_id | String(64) | FK→artisans.id, nullable=False, indexed, **UNIQUE** |
| created_at | DateTime | default=now |
| updated_at | DateTime | onupdate=now |

**Relationships:**
- `user` → ArtisanDB (back_populates="cart")
- `items` → CartItemDB (lazy="dynamic", cascade="all, delete-orphan")

**Design note:** One cart per user enforced by `UNIQUE(user_id)` constraint.

### 3.2 CartItemDB (`cart_items` table)

| Field | Type | Constraints |
|-------|------|-------------|
| id | String(64) | PK, indexed |
| cart_id | String(64) | FK→carts.id, nullable=False, indexed |
| product_id | String(64) | FK→products.id, nullable=False, indexed |
| quantity | Integer | nullable=False, default=1 |
| unit_price | Float | nullable=False, default=0.0 |
| created_at | DateTime | default=now |
| updated_at | DateTime | onupdate=now |

**Relationships:**
- `cart` → CartDB (back_populates="items")
- `product` → ProductDB

**Constraints:**
- `UNIQUE(cart_id, product_id)` — prevents duplicate product entries in the same cart

**Design note:** `unit_price` is a snapshot for cart display only. Checkout will re-read `ProductDB.price`.

### 3.3 AddressDB (`addresses` table)

| Field | Type | Constraints |
|-------|------|-------------|
| id | String(64) | PK, indexed |
| user_id | String(64) | FK→artisans.id, nullable=False, indexed |
| label | String(32) | default="home" |
| name | String(255) | nullable=False |
| phone | String(20) | nullable=False |
| line1 | String(512) | nullable=False |
| line2 | String(512) | default="" |
| city | String(128) | nullable=False |
| state | String(128) | nullable=False |
| pincode | String(10) | nullable=False |
| is_default | Boolean | default=False |
| created_at | DateTime | default=now |
| updated_at | DateTime | onupdate=now |

**Relationships:**
- `user` → ArtisanDB (back_populates="addresses")

### 3.4 OrderItemDB (`order_items` table)

| Field | Type | Constraints |
|-------|------|-------------|
| id | String(64) | PK, indexed |
| order_id | String(64) | FK→orders.id, nullable=False, indexed |
| product_id | String(64) | FK→products.id, nullable=True, ondelete=SET NULL |
| product_title | String(255) | nullable=False |
| product_image_url | String(512) | default="" |
| quantity | Integer | nullable=False, default=1 |
| unit_price | Float | nullable=False |
| total_price | Float | nullable=False |
| created_at | DateTime | default=now |

**Relationships:**
- `order` → OrderDB (back_populates="items")
- `product` → ProductDB

**Design note:** Prices are historical snapshots, NOT live ProductDB prices.

### 3.5 PaymentDB (`payments` table)

| Field | Type | Constraints |
|-------|------|-------------|
| id | String(64) | PK, indexed |
| order_id | String(64) | FK→orders.id, nullable=False, indexed |
| user_id | String(64) | FK→artisans.id, nullable=False, indexed |
| amount | Float | nullable=False |
| method | String(32) | default="cod" |
| status | String(32) | default="pending" |
| transaction_id | String(255) | nullable=True |
| paid_at | DateTime | nullable=True |
| created_at | DateTime | default=now |
| updated_at | DateTime | onupdate=now |

**Relationships:**
- `order` → OrderDB
- `user` → ArtisanDB (back_populates="payments")

**Supported methods:** cod, upi, card, netbanking
**Supported statuses:** pending, processing, success, failed, refunded

### 3.6 ShipmentDB (`shipments` table)

| Field | Type | Constraints |
|-------|------|-------------|
| id | String(64) | PK, indexed |
| order_id | String(64) | FK→orders.id, nullable=False, indexed |
| artisan_id | String(64) | FK→artisans.id, nullable=False, indexed |
| status | String(32) | default="pending" |
| carrier | String(128) | nullable=True |
| tracking_id | String(255) | nullable=True |
| shipped_at | DateTime | nullable=True |
| delivered_at | DateTime | nullable=True |
| created_at | DateTime | default=now |
| updated_at | DateTime | onupdate=now |

**Relationships:**
- `order` → OrderDB
- `artisan` → ArtisanDB (back_populates="shipments")

**Supported statuses:** pending, picked_up, in_transit, delivered, returned

---

## 4. Models Modified

### 4.1 ArtisanDB

**Added column:**

| Field | Type | Constraints |
|-------|------|-------------|
| role | String(32) | default="artisan", nullable=False, indexed |

**Added relationships:**
- `cart` → CartDB (uselist=False, cascade="all, delete-orphan")
- `addresses` → AddressDB (lazy="dynamic", cascade="all, delete-orphan")
- `payments` → PaymentDB (lazy="dynamic", cascade="all, delete-orphan")
- `shipments` → ShipmentDB (lazy="dynamic", cascade="all, delete-orphan")
- `customer_orders` → OrderDB (foreign_keys="OrderDB.customer_id")

**Backward compatibility:** All existing fields and relationships unchanged. The `role` column defaults to "artisan" for all existing records.

### 4.2 OrderDB

**Added columns:**

| Field | Type | Constraints |
|-------|------|-------------|
| customer_id | String(64) | FK→artisans.id, nullable=True, indexed |
| payment_id | String(64) | FK→payments.id, nullable=True, indexed |
| address_id | String(64) | FK→addresses.id, nullable=True, indexed |

**Added relationships:**
- `customer` → ArtisanDB (foreign_keys=[customer_id], back_populates="customer_orders")
- `items` → OrderItemDB (lazy="dynamic", cascade="all, delete-orphan")
- `address` → AddressDB (foreign_keys=[address_id])
- `payment` → PaymentDB (foreign_keys=[payment_id])
- `shipment` → ShipmentDB

**Modified relationships:**
- `artisan` → ArtisanDB (added `foreign_keys=[artisan_id]` for disambiguation)
- `product` → ProductDB (added `foreign_keys=[product_id]` for disambiguation)

**Backward compatibility:** All existing fields remain. New columns are nullable — existing orders have NULL for customer_id, address_id, payment_id.

---

## 5. Database/Schema Changes

### New Tables (6)

| Table | Purpose |
|-------|---------|
| carts | One cart per user |
| cart_items | Items within a cart |
| addresses | User shipping addresses |
| order_items | Line items within an order |
| payments | Payment records |
| shipments | Shipment/delivery records |

### Modified Tables (2)

| Table | Changes |
|-------|---------|
| artisans | Added `role` column |
| orders | Added `customer_id`, `payment_id`, `address_id` columns |

---

## 6. Relationships

```
ArtisanDB (unified identity)
 ├── products → ProductDB
 ├── cart → CartDB (one-to-one)
 ├── addresses → AddressDB (one-to-many)
 ├── customer_orders → OrderDB (as buyer)
 ├── payments → PaymentDB (one-to-many)
 └── shipments → ShipmentDB (as seller)

CartDB
 └── items → CartItemDB (one-to-many, cascade delete)

CartItemDB
 ├── cart → CartDB
 └── product → ProductDB

OrderDB
 ├── artisan → ArtisanDB (as seller)
 ├── customer → ArtisanDB (as buyer)
 ├── product → ProductDB (legacy single-product)
 ├── items → OrderItemDB (one-to-many, cascade delete)
 ├── address → AddressDB
 ├── payment → PaymentDB
 └── shipment → ShipmentDB

OrderItemDB
 ├── order → OrderDB
 └── product → ProductDB

PaymentDB
 ├── order → OrderDB
 └── user → ArtisanDB

ShipmentDB
 ├── order → OrderDB
 └── artisan → ArtisanDB
```

---

## 7. Constraints and Indexes

### Unique Constraints

| Table | Constraint | Purpose |
|-------|-----------|---------|
| carts | `UNIQUE(user_id)` | One cart per user |
| cart_items | `UNIQUE(cart_id, product_id)` | One product per cart |

### Indexes

| Table | Column | Purpose |
|-------|--------|---------|
| artisans | `role` | Filter by user role |
| orders | `customer_id` | Look up consumer orders |
| orders | `payment_id` | Look up payment |
| orders | `address_id` | Look up address |
| cart_items | `cart_id` | List cart items |
| cart_items | `product_id` | Find product in cart |
| addresses | `user_id` | List user addresses |
| order_items | `order_id` | List order items |
| payments | `order_id` | Look up payment |
| payments | `user_id` | List user payments |
| shipments | `order_id` | Look up shipment |
| shipments | `artisan_id` | List artisan shipments |

---

## 8. Migration/SQLite Handling

### Problem

SQLite's `Base.metadata.create_all()` only creates missing tables. It does NOT add new columns to existing tables.

### Solution

Added `_migrate_sqlite_columns(engine)` function in `backend/database.py` that:

1. Checks if the database is SQLite
2. Inspects existing tables and columns
3. Adds missing columns via `ALTER TABLE`:
   - `artisans.role` (if missing)
   - `orders.customer_id` (if missing)
   - `orders.payment_id` (if missing)
   - `orders.address_id` (if missing)
4. Uses a raw connection for DDL (no ORM session needed)
5. Commits the DDL changes

### Safety

- Does NOT delete the existing SQLite database
- Does NOT ask the developer to manually recreate the database
- All new columns are nullable or have safe defaults
- Existing data is preserved
- Idempotent — safe to run multiple times

---

## 9. Tests Added

**File:** `backend/tests/test_commerce_foundation.py`

21 tests covering:

| Test | What it validates |
|------|------------------|
| test_artisan_default_role_is_artisan | Default role is "artisan" |
| test_artisan_can_be_customer_role | Customer role can be stored |
| test_artisan_role_is_indexed | Role column works with queries |
| test_cart_can_reference_artisan | CartDB → ArtisanDB FK |
| test_cart_user_relationship | CartDB.user relationship |
| test_cart_item_can_reference_cart_and_product | CartItemDB FKs |
| test_cart_item_prevents_duplicate_product_in_same_cart | UniqueConstraint works |
| test_address_can_reference_artisan | AddressDB → ArtisanDB FK |
| test_address_user_relationship | AddressDB.user relationship |
| test_order_item_can_reference_order | OrderItemDB → OrderDB FK |
| test_order_item_order_relationship | OrderItemDB.order relationship |
| test_payment_can_reference_order_and_user | PaymentDB FKs |
| test_payment_default_values | PaymentDB defaults |
| test_shipment_can_reference_order_and_artisan | ShipmentDB FKs |
| test_shipment_default_values | ShipmentDB defaults |
| test_existing_order_fields_preserved | Backward compatibility |
| test_new_order_fields_are_nullable | New columns are nullable |
| test_order_item_relationship_to_order | OrderDB.items relationship |
| test_artisan_customer_orders_relationship | ArtisanDB.customer_orders |
| test_existing_product_order_relationships | Existing relationships still work |
| test_demo_artisan_has_artisan_role | Demo artisan has role |

---

## 10. Test Results

### Before This Implementation

| Suite | Result |
|-------|--------|
| Backend tests | 48/53 pass (3 pre-existing failures) |

### After This Implementation

| Suite | Result |
|-------|--------|
| Backend tests | **69/53 pass** (3 pre-existing failures) |
| New tests | **21/21 pass** |

### Pre-existing Failures (unchanged)

| Test | Reason |
|------|--------|
| test_chat_actions.py::test_action_update_product_status | KeyError (pre-existing) |
| test_chat_actions.py::test_action_filter_catalogue | KeyError (pre-existing) |
| test_social_channels.py::test_independent_channels_generation_and_lookup | Groq model not found (pre-existing) |

These 3 failures existed before this implementation and are unrelated to the database foundation changes.

---

## 11. Explicit Confirmations

- [x] No UserDB was introduced
- [x] ArtisanDB remains the canonical identity
- [x] Existing artisan data is preserved
- [x] Existing ProductDB was not unnecessarily changed
- [x] Existing OrderDB fields were not removed
- [x] New OrderDB fields are nullable
- [x] No payment provider was integrated
- [x] No logistics provider was integrated
- [x] No marketplace UI was added
- [x] No checkout UI was added
- [x] No ONDC/GeM code was modified
- [x] No fake integrations were added
- [x] No verified-complete features were modified
- [x] Existing tests were not deleted
- [x] No production secrets were added

---

## 12. Recommended Next Implementation Step

**Phase 1.2 — Authentication & Authorization + Commerce APIs**

After this database foundation is complete, the next step is:

1. **Authentication/Authorization middleware** — the backend currently has NO auth middleware. Any client can pass any `artistisan_id`.
2. **Consumer registration endpoint** — `POST /api/v1/auth/register-consumer` (or unified register with role parameter).
3. **Cart APIs** — cart CRUD endpoints.
4. **Address APIs** — address CRUD endpoints.
5. **Server-authoritative order creation** — validate product, use `ProductDB.price`, decrement stock atomically.

These belong to the next implementation phase and should NOT be started until this report is reviewed.

---

**END OF PHASE 1.1 DATABASE IMPLEMENTATION REPORT**
