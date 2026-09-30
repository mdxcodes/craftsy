# GeM Integration — Architecture & Implementation

## 1. Overview

Craftsy's GeM integration uses an **assisted official-handoff model**.
The artisan prepares the listing on Craftsy, then manually submits it on the
official GeM seller portal.

**Craftsy does NOT:**
- publish directly to GeM
- scrape or reverse-engineer GeM APIs
- store GeM credentials or OTPs
- automate GeM browser login
- claim a product is "listed on GeM" without evidence

## 2. Architecture

```
Flutter App
    ↓
Craftsy Backend
    ↓
GeM Integration Service (assisted)
    ↓
Artisan → Official GeM Portal (manual submission)
```

### Provider Abstraction

```
GeMIntegrationProvider (interface)
    │
    ├── AssistedGeMProvider  ← current implementation
    │
    └── OfficialGeMApiProvider  ← future stub (requires official authorization)
```

## 3. Backend Services

`backend/services/gem/`
- `readiness_service.py` — examines ProductDB for GeM readiness
- `category_service.py` — Craftsy's preparation schema for GeM categories
- `listing_service.py` — AI listing generation with strict hallucination prevention
- `registration_service.py` — registration guidance and official link handoff
- `provider.py` — `GeMIntegrationProvider` abstract interface
- `assisted_provider.py` — current production implementation
- `schemas.py` — Pydantic request/response models
- `prompts.py` — LLM prompts with hallucination guards

## 4. Database Changes

`ProductChannelDB` gains nullable GeM metadata columns:
- `gem_status`
- `gem_prepared_at`
- `gem_last_opened_at`
- `gem_submission_reference`
- `gem_listing_reference`
- `gem_last_error`

Migration handled in `backend/database.py::_run_schema_migrations`.

## 5. API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/v1/gem/products/{id}/readiness` | Check product readiness |
| POST | `/api/v1/gem/products/{id}/prepare` | Prepare listing draft |
| POST | `/api/v1/gem/products/{id}/listing-draft` | Generate listing draft |
| GET | `/api/v1/gem/products/{id}/listing-kit` | Get human-readable kit |
| GET | `/api/v1/gem/registration-options` | Get registration paths |
| GET | `/api/v1/gem/registration-guidance?path=` | Get step-by-step guidance |
| POST | `/api/v1/gem/products/{id}/open` | Open official GeM portal |

## 6. Seller Journeys

### Path A — Already Registered on GeM
1. Artisan taps "Sell on GeM"
2. Confirms they have a GeM account
3. Craftsy checks product readiness
4. Artisan fills missing information
5. AI generates listing draft
6. Artisan reviews
7. Taps "Open GeM"
8. Artisan logs in on GeM and submits manually

### Path B — Udyam/MSME but No GeM
1. Artisan taps "Sell on GeM"
2. Confirms no GeM account, but has Udyam
3. Craftsy shows Udyam→GeM guidance
4. Artisan opens official Udyam portal, authenticates
5. Completes GeM onboarding on official portal
6. Returns to Craftsy, prepares listing, opens GeM

### Path C — Neither Udyam nor GeM
1. Artisan taps "Sell on GeM"
2. Confirms neither Udyam nor GeM
3. Craftsy explains both options with official links
4. Artisan registers on Udyam and GeM via official portals
5. Returns to Craftsy to prepare listing

## 7. AI Listing Generation

- Uses ONLY verified ProductDB fields
- May improve wording and organization
- MUST NOT invent specifications, certifications, warranty, dimensions, material, origin, compliance, etc.
- Unknown values remain as "Information not provided"
- Provenance tracking included where practical

## 8. Status Model

| Status | Meaning |
|--------|---------|
| `NOT_STARTED` | No GeM action taken |
| `REGISTRATION_REQUIRED` | Seller needs GeM account |
| `NEEDS_INFORMATION` | Product data incomplete |
| `READY_TO_EXPORT` | Listing draft ready |
| `OPENED_ON_GEM` | Artisan opened GeM portal |
| `SUBMITTED_BY_SELLER` | Artisan confirmed submission (assisted workflow terminal state) |
| `LISTED` | Only set with actual verified evidence (future official API) |

## 9. Security

- GeM passwords are NEVER requested or stored
- Udyam OTPs are NEVER collected
- Aadhaar/PAN are directed to official portals only
- All external links use official government domains:
  - https://www.gem.gov.in/
  - https://www.gem.gov.in/seller-learning
  - https://udyamregistration.gov.in/

## 10. Future Official API

When official GeM seller catalogue API authorization exists:
1. Implement `OfficialGeMApiProvider`
2. Replace assisted handoff with authenticated API calls
3. Update status transitions with verified API responses
4. Document API access requirements

## 11. Current Limitations

- No direct GeM catalogue publishing
- No automated GeM login
- No Udyam→GeM automated onboarding
- GeM category rules are Craftsy's preparation layer, not official GeM taxonomy
- Listing kit is a draft, not an official GeM upload payload
