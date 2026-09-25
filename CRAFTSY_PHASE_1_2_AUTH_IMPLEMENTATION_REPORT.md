# CRAFTSY — PHASE 1.2: AUTH & AUTHORIZATION IMPLEMENTATION REPORT

**Generated:** 2026-09-24
**Status:** COMPLETE
**Repository:** `/secondary/craftsy`
**Branch:** `feature/bhavya-selective-integration`

---

## 1. Summary

Implemented authentication middleware and consumer registration for the commerce foundation. The backend now validates Bearer tokens, restricts order access to owning artisans, and supports consumer account registration.

**Result:** 8 new tests pass, 77 total backend tests pass (3 pre-existing failures unchanged).

---

## 2. Files Changed

| File | Action | Lines |
|------|--------|-------|
| `backend/middleware/__init__.py` | **NEW** | 1 |
| `backend/middleware/auth.py` | **NEW** | 73 |
| `backend/routers/auth.py` | Modified | +42 |
| `backend/routers/orders.py` | Modified | +8 |
| `backend/models/schemas.py` | Modified | +1 |
| `backend/tests/test_auth_middleware.py` | **NEW** | 178 |

**Total:** 6 files changed, 303 lines added/modified.

---

## 3. What Was Implemented

### 3.1 Auth Middleware (`backend/middleware/auth.py`)

**`get_current_artisan(request, db)`** — FastAPI dependency that:
1. Extracts `Authorization` header
2. Validates `Bearer` format
3. Parses token (`mock_jwt_token_{phone}`)
4. Looks up artisan by phone
5. Returns `ArtisanDB` or raises 401

**`get_current_artisan_optional(request, db)`** — Same but returns `None` instead of raising 401.

### 3.2 Consumer Registration (`backend/routers/auth.py`)

**`POST /api/v1/auth/register-consumer`** — New endpoint that:
- Accepts `name`, `phone`, `preferred_language`
- Creates `ArtisanDB` with `role="customer"`
- Returns `ArtisanProfileResponse` (201)
- Duplicate phone returns 409

### 3.3 Order Authorization (`backend/routers/orders.py`)

**`GET /api/v1/orders/artisan/{artisan_id}`** — Now requires:
- Valid Bearer token (401 if missing/invalid)
- Artisan ID must match token (403 if mismatch)

### 3.4 Schema Update (`backend/models/schemas.py`)

**`ArtisanProfileResponse`** — Added `role: str = "artisan"` field to expose the role in API responses.

---

## 4. API Endpoints

### New Endpoint

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register-consumer` | POST | Register a new consumer/buyer |

### Modified Endpoints

| Endpoint | Method | Change |
|----------|--------|--------|
| `/api/v1/orders/artisan/{artisan_id}` | GET | Now requires auth + ownership |

### Auth Flow

```
Client
  → POST /api/v1/auth/register-consumer
  → { name, phone }
  → Server creates ArtisanDB with role="customer"
  → Returns { id, name, phone, role, ... }

Client
  → POST /api/v1/auth/login { phone }
  → Server returns { demo_otp: "123456" }

Client
  → POST /api/v1/auth/verify-otp { phone, otp }
  → Server returns { access_token: "mock_jwt_token_{phone}" }

Client
  → GET /api/v1/orders/artisan/{id}
  → Headers: Authorization: Bearer mock_jwt_token_{phone}
  → Server validates token + ownership
  → Returns orders (200) or 401/403
```

---

## 5. Tests Added

**File:** `backend/tests/test_auth_middleware.py`

| Test | What it validates |
|------|------------------|
| test_register_consumer_returns_customer_role | Consumer registration creates role="customer" |
| test_register_consumer_duplicate_phone_returns_409 | Duplicate phone returns 409 |
| test_current_artisan_dep_returns_401_without_token | No token → 401 |
| test_current_artisan_dep_returns_401_with_invalid_token | Invalid token → 401 |
| test_current_artisan_dep_returns_artisan_with_valid_token | Valid token → returns artisan |
| test_orders_endpoint_rejects_missing_token | Orders without token → 401 |
| test_orders_endpoint_rejects_invalid_token | Orders with invalid token → 401 |
| test_orders_endpoint_accepts_valid_token | Orders with valid token → 200 |

---

## 6. Test Results

### Before This Implementation

| Suite | Result |
|-------|--------|
| Backend tests | 69/72 pass (3 pre-existing failures) |

### After This Implementation

| Suite | Result |
|-------|--------|
| Backend tests | **77/80 pass** (3 pre-existing failures) |
| New tests | **8/8 pass** |

### Pre-existing Failures (unchanged)

| Test | Reason |
|------|--------|
| test_chat_actions.py::test_action_update_product_status | KeyError (pre-existing) |
| test_chat_actions.py::test_action_filter_catalogue | KeyError (pre-existing) |
| test_social_channels.py::test_independent_channels_generation_and_lookup | Groq model not found (pre-existing) |

---

## 7. Security Notes

### Current State
- Token format: `mock_jwt_token_{phone}` (not a real JWT)
- No token expiry
- No token signature
- OTP is demo-mode (accepts any 6-digit code)
- No password storage

### What This Means
- **Auth middleware validates token format and artisan existence** — prevents anonymous access
- **Order authorization checks ownership** — prevents artisans from viewing each other's orders
- **Consumer registration creates separate identity** — enables role-based access control

### Limitations (documented, not fixed)
- Token is not cryptographically secure
- No session expiry
- No rate limiting on OTP
- These are acceptable for SIH demo but must be hardened for production

---

## 8. Backward Compatibility

- All existing artisan endpoints continue to work
- `ArtisanProfileResponse` now includes `role` field (default="artisan")
- `POST /api/v1/auth/register` unchanged (still creates artisans with default role)
- `POST /api/v1/auth/login` and `POST /api/v1/auth/verify-otp` unchanged
- Only `GET /api/v1/orders/artisan/{id}` now requires auth (previously unauthenticated)

---

## 9. Recommended Next Implementation Step

**Phase 1.3 — Cart & Address APIs**

After this auth foundation is complete, the next step is:

1. **Cart Service** — cart CRUD operations
2. **Cart Router** — `/api/v1/cart` endpoints
3. **Address Service** — address CRUD operations
4. **Address Router** — `/api/v1/addresses` endpoints
5. **Server-Authoritative Order Creation** — validate product, use `ProductDB.price`, decrement stock

---

**END OF PHASE 1.2 AUTH & AUTHORIZATION IMPLEMENTATION REPORT**
