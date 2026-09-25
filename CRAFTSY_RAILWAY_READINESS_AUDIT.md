# Craftsy — Railway Backend + Database Readiness Audit

**Phase:** Infrastructure Readiness (no new product features)
**Repository:** `/secondary/craftsy`
**Branch:** `feature/bhavya-selective-integration`
**Commit at audit time:** `23e455c` (feat: complete selective Bhavya integration)
**Local Python:** 3.14.7 (backend/.venv)

> This audit was produced by inspecting the actual code in the repository, not by
> trusting prior phase reports. Where behaviour could not be verified locally it is
> marked **Requires Railway verification**.

---

## 1. Scope and method

Inspected:

- `backend/` — `main.py`, `config.py`, `database.py`, `models/`, `routers/`, `services/`, `middleware/`, `utils/`, `tests/`
- `ML/` — `pricing/`, `voice_pipeline/`, `image_pipeline/`
- `backend/ML/` — a partial duplicate of `ML/`
- Flutter networking — `frontend/lib/core/config/api_config.dart` and callers
- Root config — `requirements.txt`, `backend/requirements.txt`, `Procfile`, `.railwayignore`, `.env.example`, `.gitignore`, `pytest.ini`
- Existing status/report documents (`CRAFTSY_*.md`)

Baseline test run (before any change): **124 passed, 2 failed** (pre-existing failures in
`backend/tests/test_chat_actions.py`; unrelated to infrastructure).

---

## 2. Classification key

| Code | Meaning |
|------|---------|
| **A** | PostgreSQL-compatible / ready |
| **B** | SQLite-specific, needs adaptation |
| **C** | Local filesystem dependent |
| **D** | Persistent external service required |
| **E** | Environment-variable configured |
| **F** | Secret / API-key dependent |
| **G** | Works on Railway without changes |
| **H** | Needs Railway configuration |
| **I** | Scaffold / mock only |
| **J** | Potentially problematic on Railway |

---

## 3. Database

### 3.1 Current architecture

- SQLAlchemy 2.0 ORM, `declarative_base()`, `sessionmaker`.
- Engine is created once in `backend/database.py` from `settings.database_url`.
- `init_db()` (called from the FastAPI lifespan) does `Base.metadata.create_all()`
  then runs SQLite-only column migrations, then seeds a demo artisan.
- Two ML config modules also read `.env` independently (`ML/pricing/config.py`,
  `ML/voice_pipeline/config.py`).

### 3.2 Findings

| Area | Finding | Class |
|------|---------|-------|
| Driver selection | `database_url` is already read from the `DATABASE_URL` env var (pydantic-settings maps the field automatically). SQLite is only *one* possible value. | **A/E** |
| PostgreSQL driver | **No PostgreSQL driver is declared** in either `requirements.txt`. Railway injects `postgresql://…`; SQLAlchemy resolves that to `psycopg2`, which is absent. | **J (BLOCKER)** |
| Engine args | `connect_args={"check_same_thread": False}` is already guarded by `if "sqlite" in settings.database_url`. No pooling options for Postgres (`pool_pre_ping`, `pool_recycle`). | **A (needs minor change)** |
| `Base.metadata.create_all()` | Table-per-model DDL. `String` PKs, `Float`, `DateTime`, `Text`, `Integer`, `Boolean`, FKs with `ondelete`, `index=True`, `UniqueConstraint`. All portable to PostgreSQL. | **A** |
| Circular FK | `orders.payment_id → payments.id` and `payments.order_id → orders.id` form a cycle. SQLAlchemy emits `ALTER TABLE … ADD CONSTRAINT` for cycles; PostgreSQL supports this. | **A (Requires Railway verification)** |
| SQLite-only migrations | `_migrate_sqlite_columns()` uses `inspect()` + `ALTER TABLE`, and is already short-circuited when the URL does **not** contain `sqlite`. | **B (already correctly guarded)** |
| `sqlite_master` / PRAGMA / `sqlite3` import | **None found.** | — |
| `Float` money columns | `products.price`, `cart_items.unit_price`, `order_items.unit_price/total_price`, `orders.unit_price/total_amount`, `payments.amount` are `Float`. Works on PostgreSQL as `double precision`; precision is a correctness (not compatibility) concern. | **A/J (WARNING)** |
| Indexes / unique constraints | `CartDB.user_id unique=True`, `UniqueConstraint("cart_id","product_id")`, plus numerous `index=True`. Portable. | **A** |
| Concurrency / oversell | `create_order_from_cart()` validates stock, creates order + items + payment + shipment, decrements stock, then a single `commit()`. It re-queries the product for the decrement, but **does not lock rows**. Two concurrent buyers can oversell the last unit. | **J (BLOCKER for correctness)** |
| Transaction rollback | If an exception is raised after `db.flush()`, the session is not explicitly rolled back. | **A (needs minor change)** |
| Database init from empty DB | `create_all()` creates every table. All models are imported inside `init_db()` (including `commerce_models`, `order_models`, `commerce_foundation_models`). | **A (Requires Railway verification)** |
| SQLite as production DB | If `DATABASE_URL` is unset on Railway, the app silently falls back to a local SQLite file on an ephemeral filesystem. Must be prevented/flagged in production. | **J (BLOCKER)** |

### 3.3 Models present

`artisans`, `products`, `social_drafts`, `product_channels`, `channel_audit_logs`,
`orders`, `carts`, `cart_items`, `addresses`, `order_items`, `payments`, `shipments`.

---

## 4. ChromaDB / vector database

| Question | Answer |
|----------|--------|
| Where initialised | `ML/pricing/embeddings/vector_store.py` → `chromadb.PersistentClient(path=settings.chromadb_path)` |
| Client type | `PersistentClient` (durable local directory) |
| Storage path | `ML/pricing/chroma_db/` (default `CHROMADB_DIR`), currently contains `chroma.sqlite3` |
| Collections | `benchmark_products` (metadata `hnsw:space = cosine`) |
| Embeddings | Google Gemini `gemini-embedding-001`, multimodal, generated **remotely via API** (no local model). A SHA-256 pseudo-vector fallback is used when no API key is present. |
| Consumers | `ML/pricing/artisan/processor.py` (`ArtisanProductProcessor`), `backend/services/pricing_service.py`, `ML/pricing/run_pipeline.py`, `ML/pricing/embeddings/build_index.py` |
| Purpose | Price-suggestion RAG: retrieve comparable benchmark handicraft products, then feed them to an LLM pricer. |
| Data origin | Scraped/seeded competitor catalogue, built by `build_index.py` from `ML/pricing/data/benchmark_products.json` (gitignored). |
| User-generated? | **No.** Benchmark data is derived from public product pages; results are logged to `ML/pricing/data/pricing_results.jsonl`. |
| Rebuildable? | **Yes.** `python -m ML.pricing.run_pipeline --build-index` re-creates it from scraper seed data / scraped data. |
| Empty-store behaviour | `query_similar()` returns `[]`; the LLM pricer then prices from the cost floor + description alone. Degraded but functional. |

**Classification: disposable / rebuildable cache (option A in the brief), NOT persistent
business data and NOT production-required.**

Consequences:

- An ephemeral Railway filesystem is acceptable: the directory is recreated on boot and
  the index is empty until rebuilt/populated.
- Do **not** migrate to pgvector/hosted vector DB in this phase — out of scope and not
  required, because the data is disposable.
- The pricing endpoint must never crash when the store is missing/empty. It already
  degrades gracefully (verified by reading the call chain).
- **Recommended production approach:** treat ChromaDB as a warm cache. Either (a) ship a
  pre-built index via a Railway volume mounted at `ML/pricing/chroma_db`, or (b) run the
  index build once after deploy, or (c) accept cost-floor-only pricing. Documented only —
  no migration performed.

> Note: a second, unused stub `backend/ML/pricing/embeddings/vector_store.py` uses an
> in-memory `chromadb.Client()` (no persistence). It is not imported anywhere; see §13.

---

## 5. Embeddings

| Property | Value |
|----------|-------|
| Library | `google-genai` (`google.genai`) |
| Model | `gemini-embedding-001` (`EMBEDDING_MODEL`) |
| Dimensions | 3072 (reported by `/api/v1/pricing/status`); fallback vector is 768-d |
| Runtime model download | **None.** Embeddings are computed by a remote API. |
| Internet required | Yes — for real embeddings. Without a key the deterministic SHA-256 fallback is used. |
| Cache location | None (no local model cache) |
| Startup cost | None on startup; only per-call API latency |
| Deterministic | Fallback is deterministic; API embeddings are model-version dependent |

**Classification: E/F (env-configured, secret-dependent). Railway-safe.** The one caveat
is embedding **dimension mismatch** if the store was built with one model and queried with
another — operational, not a deployment blocker.

---

## 6. AI providers

### 6.1 Groq

| Item | Value |
|------|-------|
| Client | `backend/services/groq_client.py` (httpx, OpenAI-compatible) |
| Base URL | `GROQ_BASE_URL` (default `https://api.groq.com/openai/v1`) |
| Key | `GROQ_API_KEY` (falls back to `WHISPER_API_KEY` via `get_active_groq_key()`) |
| Models | `openai/gpt-oss-120b` + fallbacks `groq/compound-mini`, `qwen/qwen3.6-27b` |
| Used for | Listing generation, cost extraction, chat (CraftMitra) |
| Required for startup | **No** — `is_available()` gates all use; offline fallbacks exist |
| Timeout/retry | httpx timeout 20 s; per-model fallback loop |
| Classification | **E/F, OPTIONAL** |

### 6.2 Gemini

| Item | Value |
|------|-------|
| Client | `google-genai` in `catalog_service.py`, `pricing_service.py`, `embedding_engine.py` |
| Key | `GEMINI_API_KEY` |
| Models | `gemini-3.6-flash` (`LLM_MODEL`), `gemini-embedding-001` |
| Used for | Listing generation fallback, Hindi reasoning, embeddings, LLM pricer |
| Required for startup | **No** — clients are `None` without a key; fallbacks engage |
| Classification | **E/F, OPTIONAL** |

### 6.3 Bhashini

| Item | Value |
|------|-------|
| Location | `backend/routers/bhashini.py` |
| Credentials | `BHASHINI_API_KEY`, `BHASHINI_USER_ID`, `BHASHINI_BASE_URL` read via `os.getenv` |
| Behaviour | **REAL API proxy** (httpx) for ASR/NMT/TTS/ALD — not a mock. Returns `503` when unconfigured. |
| Required for startup | **No** — lazy, per-request, guarded by `_is_configured()` |
| Caveats | `/synthesize` references `Response` without importing it (would raise `NameError` if called); endpoints use plausible-but-unverified URL paths; `tts` uses an undefined `response_type` kwarg. | 
| Classification | **E/F, OPTIONAL, partially real, latent bugs** |

The Bhashini integration is **not** implemented fully in this phase, only made
deployment-safe (it already fails gracefully to 503).

---

## 7. Image processing

| Item | Finding | Class |
|------|---------|-------|
| Pillow | Used for resize/format conversion. Pure-runtime, portable. | **A/G** |
| rembg | `ML/image_pipeline/processors/background_removal.py`; lazily creates an ONNX session (`u2netp`, fallback `u2net`). | **J** |
| rembg model download | Downloads the ONNX model at first use into `~/.u2net/` (rembg default). On an ephemeral Railway filesystem it is re-downloaded on each cold start. | **C/J** |
| rembg startup warm-up | `backend/main.py` spawns a daemon thread that calls `get_rembg_session()` at startup — i.e. it downloads a model on boot unconditionally. | **J (should be gated)** |
| OpenCV / scikit-image | `opencv-python-headless`, `scikit-image`; CPU-only, needs `libgomp1` for onnxruntime. | **H** |
| Input files | `backend/uploads/raw/…`, `backend/uploads/social/…`, `backend/uploads/products/…` | **C** |
| Enhanced files | `backend/uploads/enhanced/…`, URL `/uploads/enhanced/…` stored indirectly via `image_url` on products | **C** |
| Persistence expectation | If a product's `image_url` points at an upload and the filesystem is wiped, the image 404s. Product images are therefore **user/business data**. | **C/J** |
| Classification | Pillow ready; rembg needs Railway config/pinning; uploads need external object storage before production (documented, not implemented). | |

---

## 8. Voice pipeline

| Item | Finding | Class |
|------|---------|-------|
| Transcription | `ML/voice_pipeline/transcription/whisper_transcriber.py` posts to an OpenAI-compatible endpoint (`WHISPER_BASE_URL`, `WHISPER_MODEL`, `WHISPER_API_KEY`). | **E/F/G** |
| Local model | **None** — no local Whisper weights. | **G** |
| External binary | `ffmpeg` is invoked via `subprocess` for silence detection (both `catalog_service.py` and `whisper_transcriber.py`). Must exist in the container. | **H (BLOCKER)** |
| Audio temp files | `backend/uploads/audio/…` and `backend/uploads/chat_audio/…` (gitignored). Not cleaned up automatically. | **C** |
| Fallback voice | `WhisperTranscriber` returns a flagged fallback `Transcript` on failure; callers raise a friendly `ValueError`. | **G** |
| Classification | Real API integration, optional, workspace-safe; needs `ffmpeg`. | |

---

## 9. External integrations

| Integration | Status | Detail |
|-------------|--------|--------|
| ONDC | **SCAFFOLD** (`backend/services/ondc_adapter.py`) — no network calls; validation, status model, audit helpers only. | No credentials required. |
| GeM | **SCAFFOLD** (`backend/services/gem_adapter.py`) — no network calls; guided-workflow data only. | No credentials required. |
| Payments | **MOCK** — `PaymentDB` records with `method`/`status`; no gateway.
| Delivery / shipments | **MOCK** — `ShipmentDB` rows only; no carrier API. |
| Notifications | **Not implemented.** No SMS/email/push provider. |
| Social posting | `backend/services/social_media_service.py` builds drafts; no outbound posting. |

None of these are required at startup. Missing credentials do not crash the app.

---

## 10. Backend runtime

| Area | Finding | Class |
|------|---------|-------|
| Framework | FastAPI + Uvicorn. Entrypoint `backend.main:app`. | **G** |
| CORS | `cors_origins = ["*"]` **with** `cors_allow_credentials = True` — the exact anti-pattern the brief forbids. | **J (BLOCKER config)** |
| Health | `GET /api/v1/health` exists, returns fast, calls no AI. | **G** |
| Startup | `init_db()` + unconditional rembg model warm-up thread. | **J** |
| `Procfile` | `uvicorn backend.main:app --host 0.0.0.0 --port 8000` — hardcodes `8000`, ignores Railway's `$PORT`. | **J (BLOCKER)** |
| `PORT` setting | `Settings.port` already binds to the `PORT` env var. | **E** |
| Logging | No centralized logging config; startup prints localhost URLs; several services log via `print`. | **J (minor)** |
| Dockerfile | **None.** No `railway.toml`, no `runtime.txt`, no `.python-version`. | **H** |
| `.railwayignore` | Excludes `frontend/`, `assets/`, `docs/`, `submission/`, venvs, logs. | **G** |

---

## 11. Filesystem audit

| Path | Purpose | Persistent? | Railway-safe? | Action |
|------|---------|-------------|---------------|--------|
| `backend/craftsy.db` | Local SQLite DB | Dev only | **No** (ephemeral) | Keep for local; production uses Postgres |
| `backend/uploads/` | Parent upload dir | User data | No | Document: external object storage required |
| `backend/uploads/raw/` | Original photo uploads | User data | No | Document |
| `backend/uploads/enhanced/` | Enhanced photos | Derived user data | No | Document |
| `backend/uploads/products/` | Product images referenced by `ProductDB.image_url` | **Business data** | No | Document (object storage) |
| `backend/uploads/social/` | Social image uploads | User data | No | Document |
| `backend/uploads/audio/` | Voice notes for cataloging | Temporary | No | Safe to lose; cleanup recommended |
| `backend/uploads/chat_audio/` | Chat voice notes | Temporary | No | Safe to lose |
| `ML/pricing/chroma_db/` | ChromaDB persistent dir | Rebuildable | Acceptable (empty) | Rebuild or mount volume |
| `ML/pricing/data/` | Benchmark JSON, pricing audit `jsonl` | Rebuildable | No | Rebuild |
| `ML/voice_pipeline/data/` | `transcripts.jsonl`, `pipeline_runs.log` | Non-critical | No | Acceptable |
| `ML/image_pipeline/output/` | Pipeline output images | Temporary | No | Gitignored |
| `~/.u2net/` (or `U2NET_HOME`) | rembg ONNX model cache | Cache | Ephemeral | Accept re-download or bake model into image |
| `~/.cache/huggingface/`, `~/.cache/torch/` | Not used (no torch / HF) | — | — | None |
| `.pytest_cache/`, `__pycache__/` | Build caches | No | No | Ignored |

No hidden runtime directories beyond these were found.

---

## 12. Flutter networking

| Item | Finding |
|------|---------|
| Centralised config | `frontend/lib/core/config/api_config.dart` |
| Compile-time override | `String.fromEnvironment('API_BASE_URL')` — already supported and respected before any discovery. |
| Default (Android) | `http://192.168.1.5:8000` (hardcoded LAN IP constant `hostLanIp`) |
| Default (desktop/web) | `http://127.0.0.1:8000` |
| Discovery | `discoverWorkingUrl()` probes `127.0.0.1`, LAN IP, `10.0.2.2`, `localhost` against `/api/v1/health`. |
| Hardcoded localhost | Only in the discovery candidate list and `app_image.dart` host detection — both intentional for local dev. |
| Production mechanism | Already available via `--dart-define=API_BASE_URL=https://…`; the LAN IP is not yet overridable. |

**Verdict:** production configuration mechanism already exists. Minor improvement
planned: make the LAN IP also a `dart-define` and document the production build command.
No Railway URL is hardcoded (correct, since it is not yet known).

---

## 13. Duplicate ML tree

`backend/ML/` (17 tracked files) is a partial, stale duplicate of root `ML/` (65 files).
Root `ML/` is the tree actually imported by the backend (`from ML.pricing…`, etc.). The
`backend/ML` copy is **not referenced** by any import (verified: all imports use
`ML.*`). It contains a non-persistent in-memory ChromaDB stub (`backend/ML/pricing/embeddings/vector_store.py`)
and a divergent image enhancer that imports `ML.*` anyway.

**Recommendation:** leave in place this phase (deleting is out of scope and could surprise
other tooling); flag as a WARNING/cleanup item. It does not affect deployment because
root `ML/` wins on `sys.path`.

---

## 14. Dependencies

Root `requirements.txt` and `backend/requirements.txt` differ slightly. Railway will
most likely install the root file (Nixpacks default). Observed locally installed versions
(Python 3.14.7):

`chromadb 1.5.9`, `onnxruntime 1.30.0`, `rembg 2.0.85`, `numpy 2.5.3`,
`opencv-python-headless 5.0.0.93`, `scikit-image 0.26.0`, `pillow 12.3.0`,
`SQLAlchemy 2.0.54`, `pydantic 2.13.5`, `fastapi 0.141.1`, `google-genai 2.24.0`,
`uvicorn 0.53.0`, `mutagen 1.48.1`, `httpx 0.28.1`, `requests 2.34.2`.

| Concern | Finding | Class |
|---------|---------|-------|
| PostgreSQL driver | Missing in both requirement files. | **J (BLOCKER)** |
| `torch` / `torchvision` | **Not a dependency** anywhere. Good — no multi-GB download. | **G** |
| `torch` via rembg | `rembg` (non-`cli`) only needs `onnxruntime`; no torch pulled. | **G** |
| Native/system packages | onnxruntime needs `libgomp1`; `ffmpeg` binary needed for voice; headless OpenCV avoids libGL. | **H** |
| Python version | All pinned libs resolved on 3.14 **locally**. Railway's runtime must also have wheels for the chosen version. | **H (Requires Railway verification)** |
| Version ranges | All `>=`, no lock file. Acceptable for SIH; reproduce via Docker pin of Python. | **J (WARNING)** |

---

## 15. Environment variables

Currently consumed (source of truth = code + `.env.example`):

| Variable | Used by | Required locally | Required on Railway |
|----------|---------|------------------|---------------------|
| `DATABASE_URL` | `backend/config.py` | No (SQLite default) | **Yes (Postgres)** |
| `PORT` | `Settings.port` | No | Provided by Railway |
| `ENVIRONMENT` | (planned) | No | Recommended |
| `DEBUG` | `Settings.debug` | No | No |
| `GROQ_API_KEY` | Groq client | No | No (optional) |
| `GEMINI_API_KEY` | Gemini + embeddings | No | No (optional) |
| `WHISPER_API_KEY` / `WHISPER_BASE_URL` / `WHISPER_MODEL` | Voice pipeline | No | No (optional) |
| `LLM_PROVIDER` | catalog service | No | No |
| `BHASHINI_API_KEY` / `BHASHINI_USER_ID` / `BHASHINI_BASE_URL` | Bhashini router | No | No (optional) |
| `CHROMADB_PATH` | ML pricing config | No | No |
| `CORS_ORIGINS` | (planned) | No | Recommended |
| `MODEL_WARMUP_ENABLED` | (planned) | No | Recommended false |

`.env.example` currently documents only `WHISPER_*`, `GROQ_API_KEY`, `GEMINI_API_KEY`.
It omits `DATABASE_URL`, Bhashini, CORS, `PORT`, and Chroma. Must be extended.

---

## 16. Secret handling

- `.env` is gitignored and (in this environment) read-protected; **no secrets were
  printed** during this audit.
- `.gitignore` already excludes `.env`, `.env.*`, `*.pem`, `*.key`, `*.db`, SQLite files,
  `chroma_db/`, `uploads/`, model caches, keystores, and Flutter build output.
- No API keys were found embedded in source.
- `backend/craftsy.db` and `backend/uploads/` are present on disk but ignored by git.
- **Action:** keep `.env.example` placeholder-only; never log keys.

---

## 17. Summary of blockers

### BLOCKER (must fix before Railway)
1. No PostgreSQL driver declared (`psycopg2-binary`).
2. `Procfile` hardcodes port `8000` instead of `$PORT`.
3. CORS uses `allow_origins=["*"]` **with** `allow_credentials=True`.
4. `ffmpeg` is required by the voice pipeline but no container/system definition exists
   (no Dockerfile).
5. Risk of silently running SQLite on Railway when `DATABASE_URL` is unset.
6. Checkout stock decrement has no row locking → concurrent oversell.

### WARNING (deployable, address later)
- `Float` money columns (precision) — server-authoritative pricing rounds to 2 dp.
- rembg model downloaded at each cold start (and warmed at startup unconditionally).
- Uploaded/business images live only on the ephemeral filesystem → object storage needed
  before real production.
- Unpinned `>=` dependency ranges; no lock file.
- `backend/ML/` duplicate tree.
- Bhashini router latent bugs (`Response` not imported, unknown kwargs).

### FUTURE (not required for SIH deployment)
- Hosted/persistent vector store or pgvector.
- Real payment gateway, delivery, and notification integrations.
- Alembic migration framework.
- Dedicated object storage (S3-compatible / Supabase Storage).

---

## 18. Target architecture (after this phase)

```
LOCAL DEV                     RAILWAY
Flutter                       Flutter (Android)
   │                             │ HTTPS
   ▼                             ▼
FastAPI (localhost:8000)      FastAPI (Railway, $PORT)
   │                             │ DATABASE_URL
   ▼                             ▼
SQLite (backend/craftsy.db)   PostgreSQL (Railway)
```

AI/voice/image/vector services remain optional external APIs, initialized lazily and
never required to boot.
