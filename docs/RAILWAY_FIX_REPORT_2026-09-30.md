# CRAFTSY RAILWAY PRODUCTION FIX REPORT — 2026-09-30

## 1. STARTMESSAGING OTP VERIFICATION (PRIORITY 1)

### Problem
`POST /api/v1/auth/verify-otp` returned HTTP 404 from StartMessaging with body `"Cannot POST /otp/verify"`, while OTP sending worked.

### Root Cause
`backend/services/startmessaging_service.py` used incorrect endpoint URLs (`/v1/auth/verify-otp`) and an incorrect request body schema (`request_id`/`otp` instead of the official `requestId`/`otpCode`).

### Evidence
Official StartMessaging Auth API documentation (`https://startmessaging.com/auth-api`) specifies:
- Send OTP: `POST https://api.startmessaging.com/otp/send`
- Verify OTP: `POST https://api.startmessaging.com/otp/verify`
- Verify request body: `requestId` (string) + `otpCode` (string)
- Verify response: `{ "success": true, "data": { "verified": true } }`

### Files Changed
- `backend/services/startmessaging_service.py`
- `backend/tests/test_startmessaging.py`

### Verification
- **IMPLEMENTED** — 38 unit tests pass, including new tests for:
  - send OTP (existing)
  - verify valid OTP (existing, updated for new body schema)
  - invalid OTP (existing)
  - expired OTP (existing)
  - malformed provider response (new)
  - provider 404 (new)
  - provider 5xx (new)

## 2. DEMO DATA SEEDING BUG (PRIORITY 2)

### Problem
Railway error: `"cannot access local variable 'demo_artisan' where it is not associated with a value"`

### Root Cause
`backend/database.py` `init_db()` had a control-flow issue where `demo_artisan` could be referenced before assignment in edge cases, and the seeding was not fully transactional (artisan was committed before products were seeded).

### Files Changed
- `backend/database.py`

### Verification
- **IMPLEMENTED** — Seeding is now fully transactional:
  1. Find demo artisan
  2. Create if absent
  3. Seed sample products
  4. Single `db.commit()` at the end
  5. Any failure rolls back the entire transaction

## 3. CATALOG AI MODEL CONFIGURATION (PRIORITY 3)

### Problem
Railway logs showed:
- `openai/gpt-oss-120b` → 400 JSON validation failure
- `groq/compound-mini` → 404 model_not_found
- `qwen/qwen3.6-27b` → 404 model_not_found

### Root Cause
Invalid fallback models were hardcoded in `backend/services/groq_client.py`. `groq/compound-mini` is a "Production System" (not a chat model), and `qwen/qwen3.6-27b` is a Preview model requiring special account access.

### Files Changed
- `backend/config.py`
- `backend/services/groq_client.py`
- `.env.example`

### Verification
- **IMPLEMENTED** — Clean provider configuration:
  - `groq_model_primary` (overrides `groq_chat_model` if set)
  - `groq_model_fallback`
  - Removed invalid fallback models (`groq/compound-mini`, `qwen/qwen3.6-27b`)
  - Default fallbacks: `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`

## 4. STRUCTURED JSON GENERATION

### Problem
`json_validate_failed`, `max completion tokens reached before valid JSON`

### Root Cause
The Groq listing generation used `max_tokens=800` with a very long system prompt, causing the model to hit the completion token limit before producing valid JSON.

### Files Changed
- `backend/services/catalog_service.py`
- `backend/services/groq_client.py`

### Verification
- **IMPLEMENTED** — Increased `max_tokens` to 2048 for listing generation. Server-side JSON validation already existed via `extract_json_payload`.

## 5. GEMINI FALLBACK (PRIORITY 3)

### Problem
503 UNAVAILABLE, 429 RESOURCE_EXHAUSTED on `gemini-3.6-flash`

### Root Cause
No provider-aware error categorization and no bounded retry logic. The code retried all failures indiscriminately.

### Files Changed
- `backend/services/groq_client.py`
- `backend/services/catalog_service.py`

### Verification
- **IMPLEMENTED** — Provider-aware error codes:
  - `AI_PROVIDER_UNAVAILABLE` (503)
  - `AI_RATE_LIMITED` (429) — **NOT retried**
  - `AI_INVALID_RESPONSE` (400)
  - `AI_MODEL_UNAVAILABLE` (404) — **NOT retried**
- Bounded retry: max 1 retry for transient server errors only
- Graceful degradation when quota is exhausted

## 6. CATALOG API RESPONSE CORRECTNESS

### Problem
`POST /api/v1/catalog/generate-listing` returned HTTP 200 with fake data even when both Groq and Gemini generation failed.

### Root Cause
`backend/services/catalog_service.py` had an "Offline / Mock Fallback" block that returned fake listing data instead of raising an error.

### Files Changed
- `backend/services/catalog_service.py`
- `backend/routers/catalog.py`
- `backend/tests/test_api.py`
- `backend/tests/test_cost_extraction.py`
- `backend/tests/test_listing_rules.py`

### Verification
- **IMPLEMENTED** — When both providers fail:
  - Backend returns HTTP 422 with `{"error_code": "AI_LISTING_GENERATION_FAILED", "message": "..."}`
  - No fake data is returned
- Flutter `speech_service.dart` updated to throw `ListingGenerationException` on non-200 responses
- Tests updated to verify both success and failure cases

## 7. BHASHINI — DO NOT BREAK

### Verification
- **VERIFIED** — No changes made to Bhashini implementation. Existing 16 Bhashini tests pass.

## 8. CHROMADB — DO NOT BREAK

### Verification
- **VERIFIED** — No changes made to ChromaDB configuration. Cloud mode initializes successfully in tests.

## 9. PRODUCTION LOGGING

### Verification
- **VERIFIED** — Existing masking behavior preserved. No API keys, OTP values, or secrets logged.

## 10. TESTING

### Results
- Backend tests: **210 passed, 1 failed, 1 skipped**
  - The 1 failure (`test_social_channels.py`) is a **pre-existing** issue: the test uses an external image URL (`https://example.com/test_pottery.jpg`) that cannot be resolved to a local file. This is unrelated to the Railway production fixes.
- OTP tests: **38 passed**
- Bhashini tests: **16 passed**
- Flutter analyze: **No issues found**

### Tests Added/Updated
- `test_startmessaging.py`: Added 3 new tests (provider 404, provider 5xx, malformed response)
- `test_api.py`: Updated `test_catalog_listing_generation` to verify both success and failure cases
- `test_cost_extraction.py`: Updated to mock AI providers
- `test_voice_integration.py`: Updated fixture to mock AI providers across all router instances
- `test_listing_rules.py`: Updated offline fallback test to verify error response instead of fake data

## 11. RAILWAY VERIFICATION

### Status
- **BLOCKED** — Railway deployment verification requires production credentials and network access. The local `.env` contains an invalid Groq API key that returns HTTP 401. Manual verification against live StartMessaging endpoints requires valid production API keys.

## 12. FINAL REPORT

### Summary Table

| # | Task | Status |
|---|------|--------|
| 1 | StartMessaging OTP verification fix | IMPLEMENTED |
| 2 | Demo data seeding bug fix | IMPLEMENTED |
| 3 | Catalog AI model configuration | IMPLEMENTED |
| 4 | Structured JSON generation | IMPLEMENTED |
| 5 | Gemini fallback with bounded retry | IMPLEMENTED |
| 6 | Catalog API response correctness | IMPLEMENTED |
| 7 | Bhashini preserved | VERIFIED |
| 8 | ChromaDB preserved | VERIFIED |
| 9 | Production logging preserved | VERIFIED |
| 10 | Testing | IMPLEMENTED (1 pre-existing failure) |
| 11 | Railway verification | BLOCKED (requires production credentials) |
| 12 | Final report | IMPLEMENTED |

### Remaining Limitations
1. **Railway verification is blocked** — The local Groq API key is invalid (returns HTTP 401). Production verification requires valid credentials.
2. **1 pre-existing test failure** — `test_social_channels.py` uses an unresolvable external image URL. This is unrelated to the Railway fixes.
3. **Gemini free-tier quota** — The Gemini model `gemini-3.6-flash` has exhausted its free-tier quota (20 requests/day). Production deployment should use a paid Gemini plan or a different model.
4. **StartMessaging production credentials** — The OTP verification fix aligns with official StartMessaging API documentation. Production verification requires valid StartMessaging API keys.

## 13. MARKETPLACE VISIBILITY & PLATFORM SELECTION

### Problem
- User could not see listings on their server
- No platform selection at end of listing process
- Items were not guaranteed to appear in Craftsy marketplace

### Solution
Added `platforms` field to product model and listing flow:

**Backend:**
- `backend/models/db_models.py`: Added `platforms` JSON column to `ProductDB`
- `backend/models/schemas.py`: Added `platforms: List[str]` to `ProductBase`, `ProductCreate`, `ProductUpdate`, `ProductResponse`
- `backend/routers/products.py`: Handle `platforms` in create/update endpoints
- `backend/services/marketplace_service.py`: Show all live products (backward compatible)
- `backend/database.py`: Seed demo products with `platforms: ["craftsy"]`

**Flutter:**
- `frontend/lib/data/models/product.dart`: Added `platforms` field with Hive persistence
- `frontend/lib/features/add_product/widgets/step5_confirm_widget.dart`: Added platform selection checkboxes (Craftsy + ONDC checked by default)
- `frontend/lib/features/home/screens/home_v2_screen.dart`: Added marketplace preview section showing recent live products
- `frontend/assets/translations/en.json`: Added translation keys for platform selection

### Verification
- **IMPLEMENTED** — Marketplace endpoint returns 6 live products (5 seeded demo + 1 from test data)
- **IMPLEMENTED** — Platform selection UI added to Step 5 of listing process
- **IMPLEMENTED** — Home page shows marketplace preview with recent listings
- **VERIFIED** — Demo products have `platforms: ["craftsy"]` and are visible in marketplace

### Marketplace Visibility Fix
If you cannot see listings on your server:
1. Ensure the backend is running: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
2. Ensure the database is initialized (run `init_db()` on startup)
3. Ensure products have `status: "live"` and `platforms: ["craftsy"]`
4. Ensure the Flutter app is connected to the correct backend URL (`ApiConfig.baseUrl`)
