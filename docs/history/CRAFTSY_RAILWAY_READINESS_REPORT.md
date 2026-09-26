# Craftsy Railway Readiness Report

## Repository

- **Path:** `/secondary/craftsy`
- **Branch:** `feature/bhavya-selective-integration`
- **Base commit:** `23e455c` (feat: complete selective Bhavya integration)
- **Companion document:** `CRAFTSY_RAILWAY_READINESS_AUDIT.md`
- **Local Python:** 3.14.7 (`backend/.venv`)

No previously completed phase was redone. Database foundation, auth, cart/address,
server-authoritative checkout, marketplace backend, marketplace Flutter UI, and the
verified AI features were preserved. No new product features were added.

---

## Database

| Item | Status |
|------|--------|
| SQLite (local) | **Working** — default `sqlite:///<backend>/craftsy.db`; `init_db()` creates all 12 tables and seeds the demo artisan. Verified in-process (`conn: (True, 'ok')`). |
| PostgreSQL (production) | **Prepared** — driver added, engine uses pooled/pinged connections, DDL verified against the PostgreSQL dialect. Actual execution **Requires Railway verification**. |
| URL selection | Application always builds the engine from `DATABASE_URL`. `postgres://` is normalised to `postgresql://`. No database is hardcoded. |
| Schema | All models registered and created via `Base.metadata.create_all()`: `artisans`, `products`, `social_drafts`, `product_channels`, `channel_audit_logs`, `orders`, `carts`, `cart_items`, `addresses`, `order_items`, `payments`, `shipments`. |
| Migration/init | Kept the existing create-all + SQLite column-upgrade approach. `_migrate_sqlite_columns()` is **guarded to SQLite only** — it never runs against PostgreSQL. No Alembic introduced (out of scope for SIH). |
| Circular FK (`orders` ↔ `payments`) | Verified safe: `create_all` emits `CREATE TABLE` for both and adds the FK constraints via `ALTER TABLE` afterwards (valid PostgreSQL). |
| Production guard | Logs a loud warning if `ENVIRONMENT=production` while SQLite is in use. |

Changes made:
- `backend/config.py` — `resolved_database_url`, `uses_sqlite`, `is_production`.
- `backend/database.py` — dialect-aware engine (`pool_pre_ping`, `pool_recycle` for Postgres; `check_same_thread` only for SQLite), `describe_database()`, `check_database_connection()`.
- `requirements.txt`, `backend/requirements.txt` — added `psycopg2-binary>=2.9.9`.

Verification performed:
- All 12 tables compile to PostgreSQL DDL with **0 errors** using the PostgreSQL dialect.
- `SELECT … FOR UPDATE` renders for PostgreSQL and is correctly omitted for SQLite.
- SQLite `init_db()` creates 12 tables and the demo seed succeeds.

> Money fields (`price`, `unit_price`, `total_price`, `total_amount`, `amount`) remain
> `Float`, which PostgreSQL stores as `double precision`. Server-side checkout now rounds
> every monetary value to 2 decimal places. Moving to `Numeric(10,2)` would change API
> response types and is deliberately deferred (see WARNINGS).

---

## ChromaDB

- **Current purpose:** price-suggestion RAG — retrieves comparable benchmark handicraft products to feed the LLM pricer.
- **Storage location:** `ML/pricing/chroma_db/` (`chromadb.PersistentClient`), collection `benchmark_products`, cosine space.
- **Data origin:** scraped/seeded competitor catalogue built by `ML/pricing/embeddings/build_index.py`; no user-generated content.
- **Persistence requirement:** **none** — it is a disposable/rebuildable cache.
- **Railway compatibility:** acceptable as-is. An ephemeral filesystem just means the index is empty until rebuilt; pricing degrades to cost-floor-only without crashing.
- **Recommended production approach (documented, not implemented):** treat it as a warm cache — mount a Railway volume at `ML/pricing/chroma_db`, or rebuild the index once after deploy, or accept cost-floor-only pricing. **No migration to pgvector / hosted vector DB performed** (unnecessary for disposable data).

## Embeddings

- **Model/library:** `google-genai` → `gemini-embedding-001` (multimodal), 3072-d; deterministic SHA-256 fallback (768-d) when no key.
- **Runtime requirements:** remote API call; **no local model download**; no torch / HF cache.
- **Cache/model behaviour:** none — nothing to persist. Works on Railway; optional (no key ⇒ fallback).

---

## AI Providers

| Provider | Configured? | Required for startup? | Env vars | Railway concern |
|----------|-------------|-----------------------|----------|-----------------|
| **Groq** | Optional | **No** — gated by `is_available()` + offline fallback | `GROQ_API_KEY` (falls back to `WHISPER_API_KEY`), `GROQ_BASE_URL`, `GROQ_CHAT_MODEL` | None (outbound HTTPS) |
| **Gemini** | Optional | **No** — client is `None` without a key | `GEMINI_API_KEY`, `LLM_MODEL`, `EMBEDDING_MODEL` | None (outbound HTTPS) |
| **Bhashini** | Optional | **No** — per-request, returns 503 unconfigured | `BHASHINI_API_KEY`, `BHASHINI_USER_ID`, `BHASHINI_BASE_URL` | None; centralised into Settings; latent `NameError`/bad-kwarg bugs fixed |

All secrets come from environment variables. `.env.example` documents names only.

---

## Image Processing

- **Pillow:** used for resize/format conversion. Portable; ready.
- **rembg:** ONNX session (`u2netp`, fallback `u2net`) created lazily. Model downloads at first use into the container's `~/.u2net/`; on Railway it is re-downloaded per cold start.
- **Storage:** uploads live under `backend/uploads/` (`raw/`, `enhanced/`, `products/`, `social/`, `audio/`, `chat_audio/`). Product images referenced by `ProductDB.image_url` are **business data**; everything else is temporary.
- **Model behaviour:** startup pre-warm is now **disabled by default** (`WARMUP_MODELS_ENABLED=false`) so containers do not download models on boot.
- **Status:** Pillow ready; rembg functional but its model cache is ephemeral; **external object storage is required before production** for uploaded images (documented, not introduced in this phase).

---

## Filesystem

Every persistent local filesystem dependency:

| Path | Purpose | Persistent? | Action |
|------|---------|-------------|--------|
| `backend/craftsy.db` | Local SQLite DB | Dev only | Keep local; production uses PostgreSQL |
| `backend/uploads/products/` | Product images referenced by DB | **Business data** | Object storage before production |
| `backend/uploads/raw/`, `enhanced/`, `social/` | Photo uploads/enhancements | User data | Object storage before production |
| `backend/uploads/audio/`, `chat_audio/` | Voice notes | Temporary | Safe to lose |
| `ML/pricing/chroma_db/` | Vector cache | Rebuildable | Volume or rebuild |
| `ML/pricing/data/`, `ML/voice_pipeline/data/` | Scrape data, audit logs | Rebuildable | Acceptable |
| `~/.u2net/` | rembg model cache | Cache | Re-download or bake into image |

`.gitignore` already excludes `.env`, `*.db`/SQLite files, `uploads/`, `chroma_db/`,
model caches, keystores, and Flutter build output. `.dockerignore` additionally keeps
all of the above out of the image.

---

## External Integrations

| Integration | Classification | Notes |
|-------------|----------------|-------|
| ONDC | **SCAFFOLD** | Validation/status/audit only; no network calls; no credentials required. |
| GeM | **SCAFFOLD** | Guided-workflow data only; no network calls; no credentials required. |
| Payments | **MOCK** | `PaymentDB` records only; no gateway. |
| Delivery / shipments | **MOCK** | `ShipmentDB` rows only; no carrier API. |
| Notifications | **NOT IMPLEMENTED** | No SMS/email/push provider. |
| Bhashini voice services | **REAL (optional)** | Live httpx proxy; 503 when unconfigured. |
| Groq / Gemini / Whisper | **REAL (optional)** | Live APIs; graceful offline fallback. |

No optional integration can block startup, and none were faked into production behaviour.

---

## Railway

- **Startup command:** `uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}`
  (in `Procfile`, `railway.toml`, and the Dockerfile `CMD`).
- **Python version:** Docker image pins **`python:3.12-slim`** — all runtime wheels
  (chromadb, onnxruntime, rembg, opencv-python-headless, psycopg2-binary) are published
  for 3.12. The project also resolves successfully on Python **3.14.7** locally, so 3.14
  is viable if preferred. **Requires Railway verification** of wheel availability for the
  chosen runtime.
- **Environment variables:** `DATABASE_URL`, `ENVIRONMENT`, `CORS_ORIGINS`, optional provider keys (see `.env.example`). `PORT` is injected by Railway and already bound by `Settings.port`.
- **Health endpoint:** `GET /api/v1/health` (fast, no AI). Added `GET /api/v1/health/live` (liveness) and `GET /api/v1/health/ready` (database readiness, 503 when unreachable). Railway health check points at `/api/v1/health`.
- **PostgreSQL:** engine uses `pool_pre_ping` + `pool_recycle=1800`; schema creates from empty via `create_all`.
- **Docker:** new `Dockerfile` (ffmpeg + libgomp1 + libglib2.0-0, non-root user, no secrets baked in) and `.dockerignore`.
- **Config-as-code:** new minimal `railway.toml` (Dockerfile builder, start command, health check, restart policy).

CORS: `allow_origins=["*"]` with `allow_credentials=True` was the unsafe default. Now
`cors_allow_credentials` defaults to **false**, a model validator forces credentials off
whenever a wildcard origin is present, and origins/methods/headers are configurable via
`CORS_ORIGINS` / `CORS_ALLOW_METHODS` / `CORS_ALLOW_HEADERS` (comma-separated or JSON).
Native Android clients are unaffected (they do not send browser `Origin` preflights).

---

## Flutter

- **Development API URL:** `ApiConfig.baseUrl` — Android defaults to the LAN IP (`192.168.1.5:8000`), desktop/web to `127.0.0.1:8000`, with runtime discovery across `127.0.0.1`, LAN IP, `10.0.2.2`, and `localhost`.
- **Production configuration:** already supported — `--dart-define=API_BASE_URL=https://<railway-domain>`; when set, discovery is skipped and the value is used verbatim.
- **Change made:** the LAN fallback IP is now also overridable via `--dart-define=API_HOST_LAN_IP=…`; production usage documented in the file header. No Railway URL is hardcoded (it is not yet known).
- **Remaining localhost references:** intentional dev-only entries in the discovery candidate list and `app_image.dart` host detection.

---

## Tests

Exact numbers from this session (no fabrication):

| Suite | Command | Result |
|-------|---------|--------|
| Backend (before changes) | `backend/.venv/bin/python -m pytest backend/tests -q` | **124 passed, 2 failed** in 183.78 s |
| Backend (after changes) | `backend/.venv/bin/python -m pytest backend/tests -q` | **124 passed, 2 failed** in 135.94 s |
| Flutter | `flutter test` | **123 passed** ("All tests passed!") |
| Flutter static analysis | `flutter analyze` | **34 pre-existing issues** (warnings/info), none in changed files |
| Config/DB smoke | TestClient lifespan + health/root | `/api/v1/health` 200, `/live` 200, `/ready` 200, `/` 200 |

The 2 backend failures (`test_chat_actions.py::test_action_update_product_status`,
`test_action_filter_catalogue`) are **pre-existing and unchanged** by this work; they
depend on non-deterministic LLM output shape. They are not infrastructure regressions.

PostgreSQL-specific verification performed offline: all 12 tables compiled against the
PostgreSQL dialect with zero errors; `FOR UPDATE` renders on PostgreSQL and not on SQLite.
Actual PostgreSQL execution and Railway wheel resolution remain **Requires Railway
verification**.

---

## Remaining Blockers

### BLOCKER (must fix before Railway)
1. ~~No PostgreSQL driver~~ — **FIXED** (`psycopg2-binary` added).
2. ~~`Procfile` hardcodes port 8000~~ — **FIXED** (`${PORT:-8000}` in Procfile, railway.toml, Dockerfile).
3. ~~CORS wildcard + credentials~~ — **FIXED** (credentials forced off with `*`; origins configurable).
4. ~~No container/system definition for `ffmpeg`~~ — **FIXED** (Dockerfile installs ffmpeg, libgomp1, libglib2.0-0).
5. ~~Silent SQLite fallback in production~~ — **MITIGATED** (loud warning when `ENVIRONMENT=production` + SQLite; set `DATABASE_URL` to PostgreSQL).
6. ~~Checkout oversell race~~ — **MITIGATED** (`SELECT … FOR UPDATE` on product rows; SQLite ignored, PostgreSQL locks; explicit rollback on failure).
7. **Railway PostgreSQL execution is unverified locally** — DDL compiles cleanly and the driver is present, but a real Postgres run must confirm `create_all`, the circular FK, checkout, and stock concurrency. **Requires Railway verification.**

### WARNING (deployable, address later)
- Money stored as `Float`; server rounds to 2 dp but `Numeric(10,2)` is the durable fix (would change API response types — deferred deliberately).
- Uploaded/business images live only on the ephemeral filesystem — **external object storage required before production**.
- rembg model re-downloads per cold start; bake into the image or mount a volume if it hurts.
- Unpinned `>=` dependency ranges; no lock file.
- `backend/ML/` is an unreferenced stale duplicate of `ML/` — cleanup candidate.
- Bhashini endpoints are real but use unverified URL paths; `Response` import and an invalid kwarg were fixed, but the integration itself remains optional/untested.
- `test_chat_actions.py` has 2 pre-existing LLM-dependent failures.

### FUTURE (not required for SIH deployment)
- Hosted/persistent vector store or `pgvector` (only if the benchmark index becomes valuable data).
- Alembic migration framework.
- Real payment gateway, delivery/carrier, and notification integrations.
- Dedicated object storage (S3-compatible or similar).
- Dependency lock file and CI.

---

## Success condition

- Local `Flutter → FastAPI → SQLite` still works: backend suite unchanged, Flutter suite fully green, SQLite init verified, no API contract changes.
- Backend is architecturally prepared for `Android → Railway FastAPI → Railway PostgreSQL`: database selected entirely from `DATABASE_URL`, driver present, schema verified portable, checkout transactional with row locking, health/readiness endpoints, safe CORS, Railway-native start command, and a reproducible Docker build.
- All AI infrastructure (Groq, Gemini, ChromaDB, embeddings, rembg, Pillow, Bhashini, ONDC, GeM) and filesystem storage is understood, classified, and **never required to boot**.
