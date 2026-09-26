# CRAFTSY ONDC HACKATHON DEMO

## Architecture

```
ONDC Mock Buyer / Test Harness
           ↓
Craftsy ONDC BPP Adapter (FastAPI)
           ↓
Craftsy Business Services
   - ProductDB
   - ArtisanDB
   - OrderDB
   - OrderService
   - CommerceService
```

## Official Repositories Used

- `ONDC-Official/ONDC-RET-Specifications` (release-2.0.2)
- `ONDC-Official/ondc-mock-server` (inspected, see below)
- `ONDC-Official/developer-docs`

## Official Mock Server

**Status:** BLOCKED

**Repository:** `ONDC-Official/ondc-mock-server`

**Commit inspected:** `dev` branch (`694089e449449a73dac51567b7ef6294c380f79b`)

**Attempted:** Yes

**Blocker:** Server startup hangs after Redis connection. The retail specification submodules (`apps/backend/domain-repos/@retail-b2b/release-2.0.2` and `b2c_exports_2.0`) did not finish initializing. The backend process stays alive but does not bind to the port.

**Workaround:** Implemented a minimal local Retail BPP test harness inside Craftsy that follows the official ONDC Retail B2C contract structure and uses real Craftsy business data.

## Retail Domain

`ONDC:RET10`

## Retail API Version

`2.0.2`

## Protocol Version

Beckn Protocol Core `release=1.x`, ONDC Specifications `2.0.2`

## Supported Flows (Hackathon)

- search → on_search
- select → on_select
- init → on_init
- confirm → on_confirm
- status → on_status

## How to Start Craftsy

```bash
cd /secondary/craftsy/backend
.venv/bin/python -m uvicorn main:app --reload --port 8000
```

## Required Environment Variables

See `.env.example` for ONDC-related placeholders:

```bash
ONDC_ENABLED=true
ONDC_MODE=mock
ONDC_DOMAIN=ONDC:RET10
ONDC_VERSION=2.0.2
ONDC_BPP_ID=craftsy.bpp.hackathon
ONDC_BPP_URI=http://localhost:8000/api/v1/ondc
```

## Example Search Flow

```bash
curl -X POST http://localhost:8000/api/v1/ondc/search \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "action": "search",
      "version": "2.0.2",
      "bap_id": "test-buyer",
      "bap_uri": "http://localhost:9000",
      "transaction_id": "txn-001",
      "message_id": "msg-001",
      "timestamp": "2026-09-26T18:00:00Z",
      "ttl": "PT30S",
      "location": {
        "country": {"code": "IND"},
        "city": {"code": "*"}
      }
    },
    "message": {
      "intent": {
        "item": {
          "descriptor": {"name": "terracotta"}
        }
      }
    }
  }'
```

## Example Confirm Flow

```bash
curl -X POST http://localhost:8000/api/v1/ondc/confirm \
  -H "Content-Type: application/json" \
  -d '{
    "context": { ... },
    "message": {
      "order": {
        "items": [
          {
            "id": "<craftsy-product-id>",
            "quantity": 1,
            "price": {"currency": "INR", "value": "500"}
          }
        ]
      }
    }
  }'
```

## Stock Behavior

- Stock is read from `ProductDB.stock`
- `select` and `confirm` validate requested quantity <= available stock
- Successful `confirm` decrements stock via `OrderService.create_order()`
- Repeated `confirm` with the same `transaction_id`/`message_id` does not decrement stock again

## Idempotency Behavior

- Confirm requests are keyed by `transaction_id` + `message_id`
- Duplicate confirms return the existing order result
- No duplicate Craftsy orders are created

## Test Commands

```bash
cd /secondary/craftsy/backend
.venv/bin/python -m pytest tests/test_ondc_bpp.py -v
.venv/bin/python -m pytest tests/ -q
```

## Test Results

All 18 ONDC BPP tests pass:

```text
tests/test_ondc_bpp.py::test_search_returns_catalog PASSED
tests/test_ondc_bpp.py::test_on_search_alias_works PASSED
tests/test_ondc_bpp.py::test_search_without_query_returns_all_live_products PASSED
tests/test_ondc_bpp.py::test_select_validates_stock_and_returns_quote PASSED
tests/test_ondc_bpp.py::test_select_rejects_insufficient_stock PASSED
tests/test_ondc_bpp.py::test_init_returns_payment_and_fulfillment PASSED
tests/test_ondc_bpp.py::test_confirm_creates_order_and_decrements_stock PASSED
tests/test_ondc_bpp.py::test_confirm_is_idempotent PASSED
tests/test_ondc_bpp.py::test_confirm_rejects_duplicate_external_order_id PASSED
tests/test_ondc_bpp.py::test_confirm_rejects_insufficient_stock PASSED
tests/test_ondc_bpp.py::test_status_returns_existing_order PASSED
tests/test_ondc_bpp.py::test_status_lookup_by_external_order_id PASSED
tests/test_ondc_bpp.py::test_missing_context_fields_returns_400 PASSED
tests/test_ondc_bpp.py::test_unsupported_domain_returns_400 PASSED
tests/test_ondc_bpp.py::test_unsupported_version_returns_400 PASSED
tests/test_ondc_bpp.py::test_confirm_missing_items_returns_400 PASSED
tests/test_ondc_bpp.py::test_status_missing_order_id_returns_400 PASSED
tests/test_ondc_bpp.py::test_full_ondc_flow PASSED
```

Existing Craftsy tests: `155 passed, 1 failed` — the single failure is the pre-existing `test_social_channels.py::test_independent_channels_generation_and_lookup` failure unrelated to ONDC changes.

## E2E Evidence

See `tests/test_ondc_bpp.py::test_full_ondc_flow` for the full search → select → init → confirm → status sequence using real seeded Craftsy data.

Idempotency evidence:
- `test_confirm_is_idempotent` — repeated confirm with the same `transaction_id`/`message_id` returns the existing order, no second `OrderDB` row, stock unchanged after the first decrement.
- `test_confirm_rejects_duplicate_external_order_id` — confirms the idempotency key includes the external order reference.

## Known Limitations

- This is a local/mock hackathon integration, NOT production ONDC onboarding
- No real ONDC network participant registration
- No production signing/authentication
- Mock mode only; production auth is abstracted but not implemented
- Official `ondc-mock-server` could not be started in this environment due to submodule/spec initialization issues
