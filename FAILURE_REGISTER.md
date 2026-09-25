# Failure Register
**Project:** Craftsy  
**Date:** 2026-09-25  
**Scope:** Pre-deployment forensic audit and remediation  
**Status:** ACTIVE / ENVIRONMENT BLOCKER noted

---

## Fixed Failures

### F-01: Deterministic Chat Action Bypass
- **File:** `backend/services/chat_service.py`
- **Issue:** Deterministic actions (update product status, filter catalogue, sync pending, Hindi sold count) were parsed only after an LLM call, causing test flakiness and unnecessary LLM usage.
- **Fix:** Added `_try_deterministic_action()` and invoked it before the Groq LLM call.
- **Tests:** `flutter test test/chatbot_direct_actions_test.dart` — 5/5 passed.

### F-02: Bhashini Language Code Lookup Bug
- **File:** `backend/routers/bhashini.py`
- **Issue:** Language code mapping returned wrong codes for Hindi/English inputs due to incorrect `BHASHINI_LANGUAGES.get(...)` usage.
- **Fix:** Corrected lookup to use exact key matching for `"hi"` and `"en"`.
- **Note:** Bhashini endpoint paths (`/asr/transcribe`, `/nmt/translate`, `/tts/synthesize`, `/ald/detect`) still require external verification against live Bhashini API documentation.

### F-03: Unreachable Dead Code in Social Router
- **File:** `backend/routers/social.py`
- **Issue:** Code following `raise HTTPException(...)` was unreachable.
- **Fix:** Removed unreachable block after `raise HTTPException(status_code=404, detail="Social draft not found.")`.

---

## Environment Blockers

### E-01: Python Test Execution Blocked (pytest)
- **Issue:** `pytest` is not installed in the managed system Python environment.
- **Impact:** Backend unit/integration tests cannot be executed to validate Phase 11–Phase 18 fixes.
- **Resolution Required:** Install `pytest` in a virtual environment or enable system Python package installation.
- **Workaround Attempted:** None (PEP 668 managed Python blocks `pip install pytest`).
- **Status:** BLOCKED — do not proceed to production without resolving or confirming test results in CI.

---

## Items Requiring External Verification

### V-01: Bhashini API Endpoint Paths
- **File:** `backend/routers/bhashini.py`
- **Endpoints:**
  - ASR: `/asr/transcribe`
  - NMT: `/nmt/translate`
  - TTS: `/tts/synthesize`
  - ALD: `/ald/detect`
- **Action Required:** Cross-reference with current Bhashini API docs to confirm paths and required headers/payload structure.

---

## Dead Code / Low-Value Modules Not Removed

### D-01: `backend/ML/` Directory
- **Issue:** The `backend/ML/` directory and its modules are not imported anywhere in the backend application.
- **Action Taken:** Left untouched per instructions.
- **Recommendation:** Remove or clearly document as experimental/unused in a future cleanup phase.

---

## Recurring Pattern Scan Results

- **TODO / FIXME / HACK / DEPRECATED:** None found.
- **Bare `except:`:** None found.
- **Empty exception handlers (`pass`):** None found.
- **Generic `except Exception as e` → `raise HTTPException(500, detail=str(e))`:** Present in many routers as standard FastAPI error wrapping. This is acceptable for pre-production but should be replaced with typed exceptions and structured error responses before launch.

---

## Overall Health Status

| Category | Status |
|---|---|
| Modified files compile | PASS |
| Flutter chat action tests | PASS (5/5) |
| Python backend tests | BLOCKED (pytest unavailable) |
| Railway deployment config | PASS |
| Hardcoded secrets | NONE FOUND |
| Dead code removal | DEFERRED (backend/ML/) |

---

## Next Steps

1. Resolve E-01 (pytest installation) and run full backend test suite.
2. Complete V-01 (Bhashini endpoint verification).
3. Replace generic `except Exception` with typed exceptions where feasible.
4. Decide fate of `backend/ML/` dead code.
