# CRAFTSY_BHAVYA_MERGE_PLAN.md

## 1. Purpose

Authoritative execution plan for selectively integrating useful work from:

- Canonical: `/secondary/craftsy`
- Feature source: `/secondary/craftsy_bhavya/Craftsy`

This is **not** a wholesale repository merge. The canonical repository remains the source of truth for Craftsy branding/theme, accessibility, Bhashini/LanguageService architecture, CraftMitra, marketplace/commerce, ONDC, GeM, orders/seller workflows, Android widgets, routing, offline architecture, and existing tests.

The friend repository is a feature source. Only independently verified, compatible capabilities are to be ported.

---

## 2. Read Before Any Changes

Inside `/secondary/craftsy`, read:

1. `CRAFTSY_V2_MASTER_PLAN.md`
2. `CRAFTSY_ANDROID_WIDGETS_IMPLEMENTATION.md`

Also read:

3. `/secondary/CRAFTSY_BHAVYA_COMPARISON_REPORT.md`

Do not redo completed phases.

The comparison report identifies potentially useful friend capabilities including Whisper/Groq voice input, social-media AI, pricing ML, chat quick topics, additional seller fields, SocialDraftDB, and several UI/services. It also states that voice, pricing ML, social AI, and runtime behavior have not been fully verified. Verify them before treating them as production-ready. fileciteturn1file0L536-L543

---

# 3. Non-Negotiable Rules

## 3.1 No wholesale Git merge

Do **not**:

- run `git merge` between the repositories;
- replace `/secondary/craftsy` with the friend repository;
- copy entire `backend/`, `frontend/`, or `android/` directories;
- replace the canonical theme;
- replace canonical routing;
- replace accessibility work;
- replace Bhashini/LanguageService;
- replace CraftMitra;
- replace ONDC/GeM;
- replace canonical widgets;
- replace canonical tests.

The repositories have no common Git ancestor according to the comparison report, so this is selective feature integration, not a conventional branch merge. fileciteturn1file0L11-L22

## 3.2 Canonical architecture wins conflicts

If a friend implementation conflicts with Craftsy:

**Keep the canonical architecture and adapt the useful feature into it.**

## 3.3 Verify before accepting

Every candidate feature requires:

1. source inspection;
2. dependency/configuration inspection;
3. runtime verification where possible;
4. tests;
5. regression testing;
6. documentation.

## 3.4 Never copy secrets

Do not copy `.env`, API keys, tokens, credentials, certificates, or production secrets. Port only safe variable names into `.env.example`.

---

# 4. Feature Decision Matrix

| Friend feature | Decision | Strategy |
|---|---|---|
| Whisper/Groq ASR | ADAPT / VERIFY | Provider/adapter only if verified and compatible |
| Social-media AI | PORT | Additive backend capability |
| Pricing ML | PORT AFTER VERIFICATION | Keep canonical pricing boundary |
| Chat quick topics | PORT | Feed existing CraftMitra intents/actions |
| Cost extraction | CONSIDER | Add if useful to pricing workflow |
| SocialDraftDB | ADAPT | Explicit migration required |
| Additional artisan fields | CONSIDER | Add only if compatible |
| Business Advisor | REVIEW → PORT | Reuse canonical UX/services |
| Update Price | REVIEW → PORT | Use canonical product/inventory source |
| Update Stock | REVIEW → PORT | Use canonical inventory source |
| Social sharing service | REVIEW → PORT | Add without replacing canonical behavior |
| Speech service | ADAPT | Must use LanguageService |
| Sync service | REVIEW CAREFULLY | Do not duplicate WorkManager/offline sync |
| Image enhancer | REVIEW CAREFULLY | Compare with canonical image pipeline |
| Old branding/theme | REJECT | Preserve canonical Craftsy identity |
| Friend Android widgets | REJECT | Preserve canonical widget system |
| Friend missing accessibility | REJECT | Adopted UI must meet Craftsy standard |
| Friend test structure | DO NOT REPLACE | Keep canonical tests and add new tests |

The report classifies Whisper/Groq, social media, pricing ML, and chat quick topics as the main candidates, while flagging speech/sync/image-enhancer work for careful review. fileciteturn1file0L448-L482

---

# 5. Phase 0 — Safety Checkpoint

Inside `/secondary/craftsy`:

1. Confirm clean working tree.
2. Record branch, commit, and `git status`.
3. Create branch:
   `feature/bhavya-selective-integration`
4. Create rollback tag:
   `pre-bhavya-integration`
5. Do not modify the friend repository.
6. Record baseline:
   - Flutter tests
   - backend tests
   - analyzer
   - Android/widget tests
   - build status where practical

### Exit criteria

A clean rollback point exists and the baseline is recorded.

---

# 6. Phase 1 — Verify Friend Features

Inspect the actual friend source before porting.

### Backend

- `backend/services/groq_client.py`
- `backend/routers/voice.py`
- `backend/services/social_media_service.py`
- `backend/routers/social.py`
- `backend/services/pricing_service.py`
- `backend/routers/pricing.py`
- `backend/services/chat_service.py`
- `backend/routers/chat.py`
- `backend/utils/cost_extraction.py`
- `backend/models/db_models.py`
- `backend/models/schemas.py`

### Flutter

- `frontend/lib/data/services/speech_service.dart`
- `frontend/lib/data/services/image_enhancer_service.dart`
- `frontend/lib/data/services/sync_service.dart`
- `frontend/lib/core/services/social_sharing_service.dart`
- `frontend/lib/features/home/screens/business_advisor_screen.dart`
- `frontend/lib/features/home/screens/update_price_screen.dart`
- `frontend/lib/features/home/screens/update_stock_screen.dart`

### ML

- `ML/pricing/`
- `ML/voice_pipeline/`

For every candidate determine:

- real implementation vs scaffold;
- required model files;
- required external APIs;
- required environment variables;
- dependency requirements;
- tests;
- runtime status;
- old KalaSetu assumptions;
- canonical conflicts;
- schema changes;
- Android changes;
- offline/network behavior;
- accessibility/localization compatibility.

Create an internal table:

| Feature | Source verified | Runtime verified | Dependencies verified | Migration | Canonical conflict | Decision |
|---|---:|---:|---:|---:|---:|---|
| Whisper/Groq | | | | | | |
| Social AI | | | | | | |
| Pricing ML | | | | | | |
| Quick topics | | | | | | |
| SocialDraftDB | | | | | | |
| Artisan fields | | | | | | |
| Business Advisor | | | | | | |
| Update Price | | | | | | |
| Update Stock | | | | | | |

Do not continue with an unverified feature merely because it appears in the report.

---

# 7. Phase 2 — Backend Foundation and Schema

The report identifies `backend/main.py`, `backend/config.py`, `backend/database.py`, and especially `backend/models/db_models.py` as conflict areas. It also identifies ProductDB differences, SocialDraftDB, and additional artisan fields as migration risks. fileciteturn1file0L194-L207 fileciteturn1file0L249-L258

### `backend/main.py`

Keep canonical router registration. Add friend routers individually after checking:
- prefixes;
- auth;
- dependencies;
- errors;
- naming conflicts.

Do not replace the whole file.

### `backend/config.py`

Merge only required configuration fields. Keep canonical defaults.

### `backend/database.py`

Keep canonical initialization. Do not replace it with the friend's version.

### `backend/models/db_models.py`

Potential changes:
- `SocialDraftDB`;
- `experience_years`;
- `pehchan_id`;
- `preferred_language`.

Do not blindly copy model definitions.

### ProductDB

The report contains differing descriptions of ProductDB stock handling. Verify both actual schemas before changing anything.

### Migration requirements

For every accepted schema change:

1. document old schema;
2. document new schema;
3. define migration;
4. preserve existing rows;
5. test fresh DB;
6. test existing DB;
7. test rollback;
8. test API serialization compatibility.

### Exit criteria

Existing canonical backend tests pass and schema changes are intentional and documented.

---

# 8. Phase 3 — Voice / ASR

The canonical project has Bhashini/LanguageService architecture; the friend project has Whisper/Groq. The report describes canonical ASR as a Bhashini scaffold and friend ASR as Whisper/Groq. fileciteturn1file0L346-L354

## Architecture rule

Do **not** replace:

`LanguageService`

with:

`Whisper service`

Use:

`UI → LanguageService → provider abstraction → ASR provider`

If Whisper/Groq is verified, adapt it as a provider.

Bhashini remains the canonical language architecture.

Verify:
- audio formats;
- request size;
- timeouts;
- authentication;
- language support;
- errors;
- retries;
- rate limits;
- cost;
- privacy;
- secret handling.

Do not blindly copy `speech_service.dart` if it bypasses LanguageService.

### Acceptance tests

- successful transcription;
- empty speech;
- unsupported audio;
- network failure;
- API failure;
- Hindi;
- another supported language;
- fallback behavior;
- no key leakage;
- accessibility.

---

# 9. Phase 4 — Social Media AI

Candidate sources:

- `backend/services/social_media_service.py`
- `backend/routers/social.py`
- social schemas;
- `frontend/lib/core/services/social_sharing_service.dart`

The report identifies social-media AI as a unique friend capability. fileciteturn1file0L158-L190

Add it as an optional Craftsy capability.

Do not make social media required for catalogue, orders, ONDC, GeM, or CraftMitra.

Never claim a social platform is connected unless the integration actually exists.

Keep social credentials backend-side.

Add:
- service tests;
- schema tests;
- endpoint tests;
- failure tests;
- auth tests;
- no-credential tests;
- UI tests where UI is added.

---

# 10. Phase 5 — Pricing ML

Candidate sources:

- `ML/pricing/`
- `backend/services/pricing_service.py`
- `backend/routers/pricing.py`
- `backend/utils/cost_extraction.py`

The report identifies pricing ML as a potentially useful friend capability. fileciteturn1file0L68-L118

Do not replace canonical pricing architecture without comparing:
- inputs;
- outputs;
- training/model assumptions;
- model availability;
- inference requirements;
- latency;
- accuracy evidence;
- explainability;
- deployment dependencies.

Pricing remains a **seller suggestion**, not an automatic price change.

Seller must explicitly confirm before saving.

Test:
- valid product;
- missing/invalid cost;
- missing category/history;
- extreme values;
- unavailable model/API;
- seller override.

Do not invent confidence scores.

---

# 11. Phase 6 — CraftMitra Quick Topics

The report identifies eight curated Hindi quick topics. fileciteturn1file0L172-L186

Keep canonical intent-based CraftMitra.

Use:

`Quick Topic → canonical intent/action → existing screen/service`

Do not create a second assistant architecture.

Every topic must map to a known intent/action or documented informational response.

Add localization, accessibility, and voice-compatible behavior.

---

# 12. Phase 7 — Seller Tools

Potential friend screens:

- Business Advisor
- Update Price
- Update Stock

Review them against canonical seller workflows before porting.

Reuse canonical:
- theme;
- buttons;
- cards;
- dialogs;
- typography;
- accessibility;
- localization;
- routing;
- state management;
- repositories/services.

### Update Price

Use canonical product/inventory source of truth.

### Update Stock

Use canonical inventory synchronization. Do not create a parallel stock database.

### Business Advisor

Port only real, useful logic. Do not port placeholder/fake analytics.

---

# 13. Phase 8 — Flutter Services

The report flags speech, sync, and image-enhancer services for careful review. fileciteturn1file0L448-L482

### `speech_service.dart`

Adapt only if it integrates through `LanguageService`.

### `sync_service.dart`

Do not introduce a second synchronization system. Compare against canonical Hive/Drift/WorkManager/offline queue/conflict handling and port only missing capability.

### `image_enhancer_service.dart`

Compare with the canonical image pipeline before adoption. Avoid two competing image-processing pipelines.

---

# 14. Phase 9 — Android

Keep canonical package:

`com.craftsy.app`

The report identifies the friend package as old KalaSetu identity and canonical package as `com.craftsy.app`. fileciteturn1file0L488-L531

## Widgets

Keep all five canonical widgets:

1. Craftsy Today
2. Orders
3. Stock Alerts
4. CraftMitra
5. Selling Channels

Keep:
- Glance;
- widget data bridge;
- SharedPreferences/widget snapshots;
- account isolation;
- deep links;
- WidgetUpdateManager.

The report says the friend repository has no Android widget implementation. fileciteturn1file0L409-L420

If the friend Android code has useful WhatsApp/TTS behavior, port it only if compatible. Never replace `MainActivity` wholesale.

---

# 15. Phase 10 — Accessibility and Localization Gate

Every adopted feature must meet Craftsy standards:

- minimum touch targets;
- semantics;
- meaningful image descriptions;
- focus/keyboard behavior where applicable;
- text scaling;
- contrast;
- voice guidance;
- localized strings;
- Hindi and other supported locales;
- low-literacy-friendly errors;
- no critical color-only information.

Canonical accessibility must not be regressed. fileciteturn1file0L448-L482

---

# 16. Phase 11 — Testing

The report states the canonical repository has 24 Flutter test files/102 Flutter tests and 130 Android widget tests, while the friend repository has no Flutter test files and no Android widget tests. fileciteturn1file0L424-L430

Never replace canonical tests.

Add tests for every accepted feature.

### Backend
- unit;
- service;
- route;
- schema;
- failure paths.

### Flutter
- services;
- widgets;
- navigation;
- localization;
- accessibility.

### Android
- widgets;
- deep links;
- MethodChannels if changed;
- package/build.

### Integration

Verify:

`Voice → LanguageService → intent → action`

`Product → pricing suggestion → seller confirmation`

`Product → social content → sharing`

`Quick topic → CraftMitra intent → destination`

`Inventory → stock UI → canonical inventory`

`Canonical state → widget snapshot → Android widget`

---

# 17. Phase 12 — Security and Reliability

Check:

### Secrets
- no API keys committed;
- no tokens in source;
- no credentials in Flutter;
- safe `.env.example`.

### Authorization
New endpoints must use canonical auth/authorization.

### Validation
Validate audio, text, prices, quantities, social content, product IDs, and artisan IDs.

### External services
Every external service needs timeout, failure handling, graceful fallback, and logging without secrets.

### Cost
Review request sizes, rate limits, repeated calls, and expensive model usage.

---

# 18. Phase 13 — Final UX Integration

The final app must feel like one Craftsy application.

Check:
- navigation;
- typography;
- colors;
- buttons/cards/dialogs;
- loading/error/empty states;
- voice affordances;
- translations;
- accessibility;
- offline behavior.

Reject old KalaSetu visual/interaction patterns that make the product feel inconsistent.

---

# 19. Phase 14 — Documentation

Update:

`/secondary/craftsy/CRAFTSY_V2_MASTER_PLAN.md`

Document:
- accepted features;
- rejected features;
- migrations;
- environment variables;
- external services;
- tests;
- limitations;
- source commit for each imported feature.

Never call a feature production-ready without runtime verification.

---

# 20. Final Acceptance Checklist

## Architecture
- [ ] Canonical `/secondary/craftsy` remains source of truth.
- [ ] No wholesale Git merge.
- [ ] No unnecessary subsystem replacement.
- [ ] No duplicate business logic.
- [ ] No duplicate sync architecture.
- [ ] No duplicate language architecture.

## Voice
- [ ] Whisper/Groq independently verified.
- [ ] If adopted, integrated through LanguageService.
- [ ] Bhashini architecture retained.
- [ ] Failure handling works.
- [ ] Secrets remain backend-only.

## Social
- [ ] Source verified.
- [ ] Endpoints authenticated.
- [ ] Social feature is additive.
- [ ] No fake connected-channel state.

## Pricing
- [ ] ML source verified.
- [ ] Model/dependencies available.
- [ ] Suggestions do not silently change prices.
- [ ] Seller confirmation exists.

## CraftMitra
- [ ] Quick topics map to canonical intents/actions.
- [ ] No second assistant architecture.
- [ ] Localization/accessibility complete.

## Data
- [ ] Schema changes documented.
- [ ] SocialDraftDB migration handled if adopted.
- [ ] Artisan-field changes handled if adopted.
- [ ] ProductDB differences verified against actual source.
- [ ] Existing records remain compatible.

## Android
- [ ] `com.craftsy.app` retained.
- [ ] Five canonical widgets retained.
- [ ] Widget bridge retained.
- [ ] Account isolation retained.
- [ ] No wholesale MainActivity replacement.

## Accessibility
- [ ] Touch targets pass.
- [ ] Semantics pass.
- [ ] Screen-reader labels pass.
- [ ] Localization pass.
- [ ] Text scaling pass.
- [ ] Low-literacy UX remains intact.

## Tests
- [ ] Existing canonical tests pass.
- [ ] New backend tests pass.
- [ ] New Flutter tests pass.
- [ ] Android tests pass.
- [ ] Integration tests pass.
- [ ] Analyzer/build checks pass.

## Documentation
- [ ] Master plan updated.
- [ ] Environment variables documented.
- [ ] Migrations documented.
- [ ] Accepted/rejected features documented.
- [ ] Known limitations documented.

---

# 21. Rollback Strategy

If a phase causes regression:

1. Stop.
2. Do not stack further changes.
3. Identify the first failing phase.
4. Revert only that phase where practical.
5. Run the baseline suite.
6. Compare changes against `pre-bhavya-integration`.
7. Resolve the architectural conflict before retrying.

If the repository becomes unstable, return to the pre-integration checkpoint.

Never delete canonical functionality merely to make the build pass.

---

# 22. Required Final Report

Create:

`/secondary/CRAFTSY_BHAVYA_MERGE_FINAL_REPORT.md`

Include:

### Imported
- feature;
- source files;
- destination files;
- source commit;
- tests;
- runtime verification.

### Adapted
- original feature;
- canonical architecture used;
- modifications;
- reason for adaptation.

### Rejected
- feature;
- reason;
- possible future reconsideration.

### Schema
- migrations;
- fields;
- compatibility notes.

### Dependencies
- package;
- reason;
- version;
- compatibility.

### Verification
- backend tests;
- Flutter tests;
- Android tests;
- analyzer;
- build;
- integration tests.

### Known limitations

Be explicit.

---

# 23. Definition of Done

The integration is complete only when:

1. Canonical Craftsy architecture remains intact.
2. Useful friend capabilities are independently verified.
3. Accepted features are integrated rather than blindly copied.
4. No duplicate architecture is introduced.
5. Database changes are migrated safely.
6. Bhashini/LanguageService remains authoritative.
7. CraftMitra remains canonical.
8. ONDC/GeM remain intact.
9. Canonical Android widgets remain intact.
10. Accessibility remains intact.
11. Existing tests remain green.
12. New features have dedicated tests.
13. No secrets are committed.
14. Master documentation is updated.
15. Known limitations are documented.

**Final outcome: one coherent Craftsy application, not two partially merged codebases.**
