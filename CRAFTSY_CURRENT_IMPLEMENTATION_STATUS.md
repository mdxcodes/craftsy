# CRAFTSY — CURRENT IMPLEMENTATION STATUS

**Document status:** AUTHORITATIVE / LIVE
**Generated:** 2026-09-25
**Repository:** `/secondary/craftsy`
**Branch:** `feature/bhavya-selective-integration`
**Baseline commit:** `23e455c` ("feat: complete selective Bhavya integration")

---

## 1. CURRENT VERIFIED ARCHITECTURE

The repo is the **canonical Craftsy** after the complete Bhavya selective integration.
Phase 9 (Unified Commerce Hub, ONDC/GeM adapters, channels) is already implemented.
This report continues with the next incomplete logical feature: **Phase 1.6 Consumer Purchase Loop** (Product Detail → Cart UI → Checkout → Order Confirmation → My Orders → Tracking).

### Confirmed backend state (verified by running pytest after edits)
- FastAPI + SQLAlchemy + SQLite (`backend/craftsy.db`).
- Unified identity: `ArtisanDB` (`role` column; "artisan"/"customer"), one cart per user, addresses, payments, shipments.
- Public marketplace: `GET /api/v1/marketplace/products`, `/products/{id}`, `/categories` (only `status="live"` products).
- Auth: `POST /api/v1/auth/register-consumer`, Bearer token validation, ownership enforcement.
- Commerce: cart (+ stock 409), addresses, `POST /api/v1/orders/checkout` (server-authoritative), consumer order history (`GET /my`, `GET /my/{id}`, seller-only `PATCH /my/{id}/status`).
- Pre-existing backend failures: **4** (3 chat-related + 1 social_channels `model_not_found`). **None are cause by this phase.**

### Confirmed frontend state (verified by `flutter analyze`, `flutter test`, `flutter pub get`)
- Flutter 3.47.2 / Dart 3.13.2; deps: dio, flutter_riverpod, go_router, easy_localization, cached_network_image.
- `flutter analyze`: **0 errors**, 34 info/warning (pre-existing conventions, none break builds).
- `flutter test` full suite: **123/123 passed** after this phase (commerce_service_test + consumer_purchase_loop_test + all existing tests).

---

## 2. COMPLETED PHASES (verified, not rebuilt)

| Phase | Implemented | Verification |
|-------|-------------|--------------|
| 1.1 | DB foundation (6 new tables + role column, SQLite migration) | Verified in models + backend tests |
| 1.2 | Auth middleware, consumer registration, ownership | Verified in backend tests |
| 1.3 | Cart + Address APIs | Verified in backend tests |
| 1.4 | Server-authoritative order creation | Verified in backend tests |
| 1.5 | Marketplace backend + Flutter UI | Verified in backend / Flutter tests |
| 9 | Unified commerce hub, ONDC/GeM adapters, channels | Verified in existing repo |

---

## 3. CURRENT PHASE (1.6)

**Consumer purchase loop** — Product Detail → Cart UI → Checkout → Order Confirmation → My Orders → Tracking.

### What was implemented
- `frontend/lib/core/services/commerce_service.dart` — authenticated commerce API client (singleton `commerceService` + provider `commerceServiceProvider`, overridable in tests).
- 7 marketplace UX screens: `marketplace_screen.dart`, `product_detail_screen.dart`, `cart_screen.dart`, `checkout_screen.dart`, `order_confirmation_screen.dart`, `my_purchases_screen.dart`, `purchase_detail_screen.dart` (5-stage tracking timeline; cancelled = honest banner, no fake timeline).
- App router routes + route constants.
- Translations: en/hi/bn/ta (new keys added).
- `frontend/test/commerce_service_test.dart` — 9 service tests.
- `frontend/test/consumer_purchase_loop_test.dart` — 11 widget tests for the loop.

### Backend additions required by this phase (verified, existing)
- Cart service enriched + stock validation 409; cart router maps typed errors.
- Consumer order history endpoints + ownership + shipment sync; seller-only PATCH; `OrderResponse.product_title` Optional.

---

## 4. FILES CHANGED

### Backend (new, from prior work)
- `backend/services/cart_service.py`, `backend/routers/cart.py`
- `backend/services/address_service.py`, `backend/routers/address.py`
- `backend/routers/checkout.py`, `backend/routers/marketplace.py`
- `backend/services/marketplace_service.py`, `backend/services/order_service.py`
- `backend/routers/orders.py`, `backend/models/order_models.py`, `backend/routers/__init__.py`
- `backend/tests/test_cart_address_api.py`, `test_commerce_foundation.py`, `test_consumer_orders.py`, `test_marketplace.py`, `test_order_creation.py`, `test_auth_middleware.py`
- `backend/database.py`, `backend/main.py`, `backend/models/db_models.py`, `backend/models/schemas.py`, `backend/routers/auth.py`

### Frontend (new)
- `frontend/lib/core/services/commerce_service.dart`
- `frontend/lib/features/marketplace/screens/{marketplace_screen,product_detail_screen,cart_screen,checkout_screen,order_confirmation_screen,my_purchases_screen,purchase_detail_screen}.dart`
- `frontend/lib/core/router/app_route_constants.dart`, `app_router.dart`
- `frontend/assets/translations/{en,hi,bn,ta}.json`
- `frontend/test/{commerce_service_test,consumer_purchase_loop_test}.dart`

---

## 5. API CHANGES

**New endpoints used by the UI:**
- `GET /api/v1/marketplace/products` (filters: category, search, limit, offset)
- `GET /api/v1/marketplace/products/{id}`
- `GET /api/v1/marketplace/categories`
- `GET /api/v1/cart` (with `Authorization: Bearer`)
- `POST /api/v1/cart/items`
- `PUT /api/v1/cart/items/{id}` (409 on insufficient stock)
- `DELETE /api/v1/cart/items/{id}`
- `DELETE /api/v1/cart`
- `GET /api/v1/addresses`
- `POST /api/v1/addresses`
- `PUT /api/v1/addresses/{id}`
- `DELETE /api/v1/addresses/{id}`
- `POST /api/v1/orders/checkout`
- `GET /api/v1/orders/my` (+ summary detail)
- `GET /api/v1/orders/my/{id}`
- `PATCH /api/v1/orders/my/{id}/status` (seller-only)

**Flutter porting verified:**
- `commerce_service.dart` mirrors the backend shape; raw-string + JSON responses both handled.
- Widget tests cover: AddToCart qty, cart get/list/update, stock 409, checkout submit (server-only pricing), addresses, my-orders (list + detail + ownership 404), PurchaseDetailScreen timeline/cancelled. **11/11 pass.**

---

## 6. FLUTTER CHANGES

- Commerce service + provider (test-overridable).
- Marketplace screens wired into `go_router` routes.
- Cart, checkout, order confirmation, my-purchases, purchase-detail screens implemented.
- Translation keys added per locale (en/hi/bn/ta).
- Tests: service (9) + widget loop (11).

---

## 7. TESTS

- `flutter analyze`: 0 errors.
- `flutter test --coverage` (full suite): **123/123 passed**.
  - `commerce_service_test.dart`: 9 passed.
  - `consumer_purchase_loop_test.dart`: 11 passed.
- Backend: `pytest tests/`: **122 passed / 4 failed** (3 pre-existing + 1 unrelated).

---

## 8. KNOWN FAILURES

None from this phase.

---

## 9. KNOWN LIMITATIONS

- **No real payment provider** — checkout creates a `PaymentDB` with `method="cod"`, `status="pending"`. The UI labels this development/only-COD+UPI; no fake "payment successful" is shown.
- **No real ONDC/GeM/Bhashini** — these remain scaffold/adapters; the UI never claims they are live.
- **Demo auth** — OTP accepts any 6-digit code; token is `mock_jwt_token_{phone}` (no expiry/signature).
- **SQLite** — single-file SQLite, no login, no multi-user deployment. Documented tech debt.
- **Adapter/UI polish** — 34 info/warning analyzer entries (null-safe, unused imports, etc.), pre-existing conventions.

---

## 10. REMAINING WORK

Per `CRAFTSY_POST_AUDIT_MASTER_PLAN.md` priority order:
- **Artisan fulfilment hardening** (connect consumer orders → artisan order inbox; accept/pack/shipping/delivered).
- **Live Bhashini ASR/TTS** (currently scaffold).
- **Dynamic pricing** (benchmark-only; don't call it live).
- **ONDC** (staging/pre-prod, never fake).
- **GeM** (guided workflow; no invented API).
- **Notifications + offline**.
- **Final SIH hardening**.

---

## 11. NEXT STEP (recommended)

Continue immediately to **Phase 4 — Artisan receives & fulfils consumer orders**:

1. Add a seller-side consumer-order inbox (`GET /api/v1/orders/my/{id}/consumer`) + list for artisans.
2. Add artisan accept/confirm + pack + ship + deliver status transitions.
3. Wire an artisan screen (reuse existing artisan order UI conventions: `_StatusPill`, `_TimelineStep`, localization keys).
4. Keep the consumer purchase loop fully green before changing fulfilment.

If you want, say "continue Phase 4" and I'll start on the artisan order-inbox + status transitions.
