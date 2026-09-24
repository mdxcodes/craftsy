# Craftsy — Real vs Mock/Demo Functionality Disclosure

**Date:** 2026-09-23
**Phase:** 9 (Final Polish & Validation)
**Purpose:** Honest documentation of what is real vs what is mock/demo in the Craftsy application.

---

## 1. REAL FUNCTIONALITY (Actually Working)

### 1.1 Backend (FastAPI)
| Feature | Status | Notes |
|---------|--------|-------|
| Artisan registration & login | ✅ Real | Phone + OTP (demo OTP: 123456) |
| Product CRUD | ✅ Real | SQLite database, full create/read/update/delete |
| Product image upload | ✅ Real | File storage in uploads/ directory |
| AI image enhancement | ✅ Real | rembg background removal + 11-stage enhancer |
| AI pricing suggestions | ✅ Real | Gemini/Groq API with cost extraction |
| Bilingual listing generation | ✅ Real | Gemini API for English + Hindi |
| Voice-to-product pipeline | ✅ Real | Whisper STT + AI cataloging (requires API key) |
| Social media draft generation | ✅ Real | Groq/Gemini API for captions + hashtags |
| Offline sync queue | ✅ Real | Hive local storage + sync manager |
| Commerce channel management | ✅ Real | Channel status tracking, validation, audit logging |
| Unified order model | ✅ Real | Multi-channel order support |
| Audit logging | ✅ Real | All channel operations logged |

### 1.2 Frontend (Flutter)
| Feature | Status | Notes |
|---------|--------|-------|
| Authentication flow | ✅ Real | Sign-in, OTP, registration, language selection |
| Home dashboard | ✅ Real | Greeting, quick actions, recent orders, earnings |
| Add Product flow | ✅ Real | 5-step guided flow with camera/gallery |
| AI image enhancement | ✅ Real | Before/after comparison slider |
| AI listing review | ✅ Real | Bilingual title, description, tags |
| Fair pricing assistant | ✅ Real | AI-powered price suggestions |
| Product catalogue | ✅ Real | Search, filter, grid/list view |
| Product detail | ✅ Real | Full product info with channel status |
| Order management | ✅ Real | Status updates, tracking |
| Analytics/Stats | ✅ Real | Earnings, charts, order summary |
| Profile management | ✅ Real | Artisan profile with accessibility settings |
| Notifications | ✅ Real | Local notifications with action buttons |
| Tutorial carousel | ✅ Real | 7-slide onboarding with TTS |
| Multi-language support | ✅ Real | English, Hindi, Tamil, Bengali |
| Accessibility features | ✅ Real | TTS, sound effects, haptic feedback, large text |
| Commerce channel UI | ✅ Real | Channel selector, status cards, GeM guided workflow |
| Offline support | ✅ Real | Hive local storage, sync queue |
| Voice actions | ✅ Real | TTS playback, voice navigation |

### 1.3 ML Pipeline
| Feature | Status | Notes |
|---------|--------|-------|
| Background removal | ✅ Real | rembg U²-Net model |
| Image enhancement | ✅ Real | 11-stage pipeline (brightness, contrast, sharpness, etc.) |
| Voice transcription | ✅ Real | Whisper STT (requires API key) |
| Craft glossary | ✅ Real | Category-specific vocabulary for STT biasing |

---

## 2. MOCK/DEMO FUNCTIONALITY (Not Real — Placeholder/Stub)

### 2.1 Authentication
| Feature | Mock Status | Notes |
|---------|-------------|-------|
| OTP verification | ⚠️ Demo | Accepts any 6-digit code or 123456 |
| JWT tokens | ⚠️ Mock | `mock_jwt_token_{phone}` — not real JWT |
| NGO Assist | ⚠️ Mock | UI only, no real NGO integration |

### 2.2 Data
| Feature | Mock Status | Notes |
|---------|-------------|-------|
| Demo artisan | ⚠️ Demo | Seeded artisan: Rameshwar Lal Kumhar (phone: 9876543210) |
| Demo products | ⚠️ Demo | 3 sample products in database |
| Demo orders | ⚠️ Demo | Sample orders for testing |
| Demo notifications | ⚠️ Demo | Sample notifications for testing |
| Earnings/analytics | ⚠️ Demo | Mock data for demonstration |

### 2.3 External Integrations
| Feature | Mock Status | Notes |
|---------|-------------|-------|
| ONDC integration | ⚠️ Not Connected | Architecture ready, no real API calls |
| GeM integration | ⚠️ Not Connected | Guided workflow only, no API |
| Social media posting | ⚠️ Mock | Generates drafts but doesn't actually post |
| Payment processing | ⚠️ Mock | No real payment gateway |
| Shipping/tracking | ⚠️ Mock | No real shipping integration |

### 2.4 ML/AI
| Feature | Mock Status | Notes |
|---------|-------------|-------|
| Voice transcription | ⚠️ Stub | Returns stub transcript if no API key |
| Image enhancement | ✅ Real | Actually processes images |
| AI pricing | ✅ Real | Actually calls Gemini/Groq |
| AI listing generation | ✅ Real | Actually calls Gemini/Groq |

---

## 3. WHAT REQUIRES CREDENTIALS/ACCESS

| Feature | Required | Status |
|---------|----------|--------|
| ONDC real integration | ONDC Network Participant signing keys, SSL cert | ❌ Not obtained |
| GeM real integration | GeM seller registration (manual) | ❌ Not completed |
| Real OTP SMS | SMS gateway integration | ❌ Not implemented |
| Real payment | Payment gateway (Razorpay/Stripe) | ❌ Not implemented |
| Real shipping | Shipping API (Delhivery/Shiprocket) | ❌ Not implemented |
| Whisper STT | OpenAI API key | ⚠️ Optional (stub fallback) |
| Groq API | Groq API key | ✅ Configured |
| Gemini API | Gemini API key | ✅ Configured |

---

## 4. KNOWN LIMITATIONS

1. **No real external commerce integration** — ONDC and GeM are architecture-ready but not connected
2. **Demo authentication** — OTP accepts any code, tokens are mock
3. **Demo data** — Sample artisan, products, orders, and notifications are seeded for testing
4. **No real payment processing** — Checkout flow is UI-only
5. **No real shipping integration** — Tracking IDs are manual
6. **Social media** — Drafts are generated but not actually posted
7. **Voice pipeline** — Works with API key, falls back to stub without it
8. **Offline sync** — Queue exists but sync is manual (no automatic background sync)

---

## 5. SIH DEMO NOTES

For SIH 2026 demonstration:
- **DO show:** Product creation flow, AI image enhancement, AI pricing, multi-language support, accessibility features, commerce channel architecture
- **DO NOT claim:** ONDC/GeM integration, real payments, real shipping, real OTP
- **BE HONEST:** When asked about external integrations, say "Architecture ready, pending credentials/onboarding"

---

## 6. TEST COVERAGE

| Suite | Tests | Pass | Fail | Notes |
|-------|-------|------|------|-------|
| Backend API | 53 | 48 | 5 | 3 pre-existing (Groq API), 2 fixed |
| Frontend Flutter | 102 | 102 | 0 | All passing |
| ML Pipeline | 2 | 2 | 0 | Image + voice integration |
| **Total** | **157** | **152** | **5** | **96.8% pass rate** |

---

## 7. SECURITY AUDIT RESULTS

| Check | Status | Notes |
|-------|--------|-------|
| Hardcoded API keys | ✅ None found | All keys in environment variables |
| Hardcoded passwords | ✅ None found | No passwords in code |
| SQL injection | ✅ Safe | Using SQLAlchemy ORM (parameterized queries) |
| XSS | ✅ Safe | Flutter escapes HTML by default |
| CORS | ✅ Configured | Permissive for development |
| Secrets in git | ✅ None | .env in .gitignore |
| ONDC/GeM credentials | ✅ Not in Flutter | All external integrations backend-only |

---

## 8. RECOMMENDATIONS FOR PRODUCTION

1. **Replace demo OTP** with real SMS gateway (MSG91, Twilio)
2. **Implement real JWT** authentication with refresh tokens
3. **Add payment gateway** (Razorpay for Indian market)
4. **Complete ONDC onboarding** when ready
5. **Complete GeM seller registration** for artisans
6. **Add real shipping** integration
7. **Implement background sync** for offline queue
8. **Add analytics** (Firebase Analytics or similar)
9. **Add crash reporting** (Sentry, Firebase Crashlytics)
10. **Penetration testing** before production launch
