# Craftsy — Final Architecture

## System Overview

Craftsy is a full-stack application connecting rural Indian artisans to digital marketplaces.

```
Flutter Mobile App (offline-first)
    ↓ HTTP/JSON
FastAPI Backend
    ↓ SQLAlchemy 2.0
PostgreSQL (production) / SQLite (development)
    ↓
External Services
    ├── Cloudinary (permanent image storage)
    ├── StartMessaging (OTP delivery)
    ├── Groq / Gemini (LLM, embeddings, pricing)
    ├── Bhashini (ASR/translation — optional)
    ├── ChromaDB (pricing benchmark vector index)
    ├── ONDC (retail network protocol — local BPP)
    └── GeM (government marketplace — assisted handoff)
```

## Core Data Model

```
USER
└── ArtisanDB (phone-primary, role-based)
    ├── id
    ├── phone (10-digit, unique)
    ├── name (nullable)
    ├── craft_type
    ├── location_cluster
    ├── state
    ├── experience_years
    ├── pehchan_id
    ├── preferred_language
    └── role (artisan / customer)

PRODUCT
└── ProductDB
    ├── id (string primary key)
    ├── artisan_id (FK to ArtisanDB)
    ├── title / title_hi
    ├── description / description_hi
    ├── price (INR, server-authoritative)
    ├── image_url (Cloudinary HTTPS URL or remote URL)
    ├── cloudinary_public_id (nullable)
    ├── category
    ├── tags (JSON)
    ├── status (live / draft / pendingSync)
    ├── stock (unified inventory)
    ├── platforms (JSON: e.g. ["craftsy", "ondc"])
    ├── created_at / updated_at
    └── stock is the single source of truth for inventory

ORDER
└── OrderDB / OrderItemDB / PaymentDB / ShipmentDB / AddressDB
    ├── Server-authoritative pricing (never trust client price)
    ├── Atomic stock decrement with row locking
    ├── Channel tracking (craftsy / ondc)
    ├── External order ID for ONDC idempotency
    └── Status transitions with audit logging

GE M
└── ProductChannelDB (channel metadata)
    ├── gem_status
    ├── gem_prepared_at
    ├── gem_last_opened_at
    ├── gem_submission_reference
    ├── gem_listing_reference
    └── gem_last_error
```

## Authentication

- Phone + OTP via StartMessaging
- HMAC-SHA256 signed access tokens
- Token contains phone + expiry
- Verified against AUTH_SECRET_KEY
- Development/test mode uses fallback secret

## Image Lifecycle

```
Flutter (local file)
    ↓ POST /api/v1/products/upload-image (multipart)
FastAPI (temporary local storage)
    ↓ Cloudinary upload
Cloudinary (permanent HTTPS URL)
    ↓ stored in ProductDB.image_url
PostgreSQL
    ↓
Flutter display (AppImage widget)
```

ProductDB is the single source of truth for product metadata. Cloudinary is the single source of truth for permanent product images.

## AI Pipeline

```
Voice note (regional language)
    ↓
Whisper STT (or Bhashini ASR)
    ↓
Text transcription
    ↓
Groq/Gemini LLM
    ↓
Bilingual title, description, tags, price rationale
    ↓
ProductDB (with AI-generated fields)
```

Pricing:
```
ProductDB (price, cost)
    ↓
ChromaDB vector search (benchmark products)
    ↓
LLM price suggestion
    ↓
Display to artisan (never auto-set)
```

## ONDC Flow

```
BAP → BPP (Craftsyr)
    ↓ search
    Products from ProductDB (live, in stock)
    ↓ select
    Quote with server-authoritative price
    ↓ init
    Order initialized
    ↓ confirm
    Atomic: validate stock → lock rows → create order → decrement stock → commit
    ↓ status
    Order status from OrderDB
```

Idempotency: `external_order_id` + `OrderDB` query + optional database-backed idempotency table.

## GeM Flow

```
ProductDB
    ↓ readiness check
GeMReadinessService
    ↓
Missing fields → artisan fills in Craftsy
    ↓
AI listing generation (verified data only, no hallucination)
    ↓
GeM Listing Kit (copyable text + structured data)
    ↓
Open official GeM portal (https://www.gem.gov.in/)
    ↓
Artisan manually creates listing on GeM
```

## External Dependencies

| Service | Required | Failure Behavior |
|---------|----------|------------------|
| PostgreSQL | Yes | API fails to start |
| Cloudinary | No | Images stored locally, logged |
| StartMessaging | Yes (production) | OTP endpoints return 501 |
| Groq | No | Falls back to Gemini |
| Gemini | No | Falls back to Groq |
| Bhashini | No | Returns 503 |
| ChromaDB | No | Pricing returns error |
| ONDC | No | Channel metadata only |
| GeM | No | Assisted handoff only |

## Deployment

- Railway for backend hosting
- PostgreSQL via Railway marketplace
- Environment variables set in Railway dashboard
- Health endpoint: `/api/v1/health`
- CORS origins configured per environment
