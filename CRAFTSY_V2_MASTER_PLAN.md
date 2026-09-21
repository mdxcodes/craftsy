# Craftsy V2 — Master Product, UX, Accessibility & Engineering Plan

**Status:** Living document — source of truth for all Craftsy V2 work  
**Project:** Craftsy — SIH 2026 / PS-90 / Heritage & Culture  
**Primary client:** Flutter mobile app  
**Backend:** FastAPI + SQLAlchemy  
**AI/ML:** Voice, image enhancement, fair pricing, AI assistant  
**Target user:** Indian artisan with low digital literacy and potentially low/no reading ability  
**Primary product goal:** Enable an artisan to create, understand, manage, and sell products with minimal typing and minimal reading.

---

## 0. IMPORTANT: HOW AI CODING AGENTS MUST USE THIS FILE

This document is the **single source of truth** for Craftsy V2.

Every AI coding agent working on this repository must:

1. Read this file before making changes.
2. Treat the current repository as the implementation baseline described below.
3. Follow the current phase in `## 13. Implementation Roadmap`.
4. Never invent a new architecture when an existing architecture already satisfies the requirement.
5. Preserve working backend/ML behavior unless a task explicitly requires a backend/ML change.
6. Prefer incremental refactors over rewrites.
7. Never delete an existing feature simply because it is not part of the new home screen. Move it to a secondary/advanced location when appropriate.
8. After each completed task, update the `## 14. Execution Status` section.
9. After each meaningful UI change, run the most relevant Flutter tests/analyzer available in the environment.
10. Before changing APIs or database behavior, inspect the existing client/service/route/model implementation and document the impact in `## 15. Decision Log`.
11. Do not use the old HTML redesign as the visual source of truth. It is historical reference only.
12. Do not introduce fake AI features. A feature may be visually represented as AI only when the implementation actually exists or the task explicitly creates the implementation.
13. Do not claim that mock/demo functionality is production functionality.
14. Keep user-facing language simple, short, culturally respectful, and suitable for the selected Indian language.
15. For low-literacy UX, favor **show + speak + confirm** over **read + type + submit**.

### Agent task protocol

When receiving a task, the agent should silently apply this sequence:

```text
READ MASTER PLAN
      ↓
LOCATE CURRENT FILES / SERVICES
      ↓
CHECK CURRENT PHASE
      ↓
MAKE SMALLEST SAFE CHANGE
      ↓
RUN RELEVANT TESTS / ANALYSIS
      ↓
CHECK ACCESSIBILITY REQUIREMENTS
      ↓
UPDATE EXECUTION STATUS
      ↓
UPDATE DECISION LOG IF ARCHITECTURE CHANGED
```

If a task conflicts with this file, the agent must identify the conflict before coding and choose the option that preserves the product principles in this document.

---

# 1. PRODUCT NORTH STAR

## 1.1 Core problem

Craftsy is intended for artisans who may face:

- low digital literacy
- limited ability/desire to type
- limited English proficiency
- regional-language preferences
- inconsistent internet connectivity
- difficulty producing professional product photographs
- difficulty writing product descriptions
- difficulty understanding digital-market pricing

The product must not assume that the artisan understands e-commerce concepts.

## 1.2 Product philosophy

### Current mental model

```text
USER LEARNS THE APP
        ↓
USER NAVIGATES MENUS
        ↓
USER FILLS FORMS
        ↓
AI HELPS
```

### Craftsy V2 mental model

```text
ARTISAN EXPRESSES INTENT
        ↓
CRAFTSY UNDERSTANDS
        ↓
CRAFTSY DOES THE COMPLEX WORK
        ↓
CRAFTSY SHOWS / SPEAKS RESULT
        ↓
ARTISAN CONFIRMS
```

### North-star statement

> **Craftsy should let an artisan sell online without first having to learn how to use an e-commerce application.**

## 1.3 Primary interaction model

Every major action must be possible through three equivalent modes where technically appropriate:

```text
           ACTION
             │
     ┌───────┼───────┐
     ↓       ↓       ↓
    🎤      👆      📸
   SPEAK     TAP     SHOW
```

Voice is not an optional accessibility add-on. It is a primary interaction surface.

---

# 2. TARGET USER EXPERIENCE

## 2.1 Primary persona

**Artisan / maker**

The artisan may:

- primarily speak rather than type
- understand spoken instructions better than written instructions
- be more comfortable with photos/icons than dense menus
- use a budget Android phone
- have intermittent connectivity
- be unfamiliar with terms such as catalogue, listing, SEO, SKU, analytics, draft, or checkout

## 2.2 Secondary personas

### Customer

Wants to:

- discover authentic products
- understand the artisan/story
- purchase simply
- trust the product and seller

### Helper / NGO / trusted coordinator

May assist an artisan with:

- product photography
- listing setup
- order management
- account help

The helper must not replace artisan ownership.

## 2.3 Accessibility goals

Craftsy V2 should support users with:

- low/no literacy
- limited English ability
- low digital familiarity
- reduced confidence with forms
- visual accessibility needs
- hearing accessibility needs where possible
- motor limitations through large touch targets and simple gestures

---

# 3. REPOSITORY BASELINE — ACTUAL CURRENT IMPLEMENTATION

The uploaded repository contains approximately 370 tracked/source files across the main application, backend, and ML subsystems.

## 3.1 Top-level structure

```text
craftsy-main/
├── frontend/                  # Flutter application
├── backend/                   # FastAPI backend
├── ML/
│   ├── image_pipeline/       # Image enhancement
│   ├── voice_pipeline/       # Speech processing
│   └── pricing/              # Fair-price engine
├── docs/
├── submission/
├── assets/
├── README.md
└── craftsy-redesign-v3.html   # Historical visual prototype
```

## 3.2 Frontend architecture

Flutter dependencies include:

- Flutter / Dart
- Riverpod
- go_router
- Hive
- Drift / SQLite
- WorkManager
- Dio
- connectivity_plus
- camera
- image_picker
- record
- just_audio
- flutter_tts
- cached_network_image
- easy_localization
- google_fonts
- phosphor_flutter
- lottie
- permission_handler
- share_plus
- gal
- URL launcher
- PDF / printing / QR packages

Important frontend folders:

```text
frontend/lib/
├── app.dart
├── main.dart
├── core/
│   ├── config/
│   ├── offline_sync/
│   ├── providers/
│   ├── router/
│   ├── services/
│   ├── theme/
│   ├── utils/
│   └── widgets/
├── data/
│   ├── models/
│   ├── repositories/
│   └── services/
└── features/
    ├── add_product/
    ├── auth/
    ├── catalogue/
    ├── chatbot/
    ├── home/
    ├── notifications/
    ├── orders/
    ├── profile/
    ├── social_media/
    └── tutorial/
```

## 3.3 Current major routes

```text
/splash
/language
/sign-in
/register
/ngo-auth
/otp
/home
/catalogue
/add-product
/social-media-helper
/profile
/product/:id
/language-settings
/my-stats
/listing-tutorial
/assistant
/notifications
/my-orders
/orders/:orderId
```

## 3.4 Current home structure

`HomeShell` currently exposes four primary tabs:

```text
Add Product
Catalogue
My Orders
Profile
```

and exposes CraftMitra as a floating action button.

This is the main interaction structure to redesign.

## 3.5 Current add-product structure

The current product flow contains five stages:

```text
1. Capture
2. Describe
3. AI Review
4. Pricing
5. Confirm
```

Relevant files:

```text
frontend/lib/features/add_product/
├── screens/add_product_flow_screen.dart
└── widgets/
    ├── step1_capture_widget.dart
    ├── step2_describe_widget.dart
    ├── step3_ai_review_widget.dart
    ├── step4_pricing_widget.dart
    ├── step5_confirm_widget.dart
    └── step_progress_bar.dart
```

This flow is the primary candidate for the V2 flagship UX.

---

# 4. EXISTING PRODUCT CAPABILITIES TO PRESERVE

Do not rewrite these simply to make the UI look different.

## 4.1 AI product/listing workflow

Existing flow supports the concept:

```text
PHOTO + SPOKEN DESCRIPTION
        ↓
AI LISTING GENERATION
        ↓
TITLE / DESCRIPTION / CATEGORY / TAGS
        ↓
ARTISAN REVIEW
        ↓
PUBLISH
```

## 4.2 Image enhancement pipeline

Current ML image pipeline contains stages for:

1. input validation
2. AI background removal
3. subject detection / auto-cropping
4. lighting / white balance / sharpening
5. clean background/canvas placement
6. output resize / compression

Important implementation files:

```text
ML/image_pipeline/enhancer.py
ML/image_pipeline/processors/
```

Do not remove this capability during UI redesign.

## 4.3 Voice pipeline

Current voice pipeline includes:

```text
ML/voice_pipeline/
├── transcription/
├── orchestrator/
├── glossary/
└── models.py
```

There is already a craft terminology glossary.

Existing mobile voice services include recording, transcription, and TTS.

## 4.4 Fair pricing engine

Current pricing architecture combines:

```text
COST FLOOR
  ├── materials
  ├── labour
  ├── transport
  └── overhead

        +

MARKET COMPARABLES
  ├── embeddings/vector retrieval
  ├── marketplace data
  └── category filtering

        ↓

LLM PRICE RECOMMENDATION
```

The system already has pricing code under:

```text
ML/pricing/
├── artisan/
├── embeddings/
├── llm/
└── scrapers/
```

The UI should make the reasoning understandable without requiring the artisan to read a technical explanation.

## 4.5 CraftMitra assistant

Existing assistant architecture includes:

```text
frontend/lib/features/chatbot/
backend/routers/chat.py
backend/services/chat_service.py
```

There are text and voice interaction paths plus action/navigation concepts.

For V2, CraftMitra should evolve from a floating chatbot into the primary AI companion / task interface.

## 4.6 Offline-first architecture

The app already contains:

```text
Drift / SQLite
Hive
Connectivity detection
Offline queue
Sync manager
WorkManager background sync
```

The offline architecture is a product feature, not merely an engineering detail.

## 4.7 Accessibility infrastructure

Existing pieces include:

```text
app_tts_service.dart
speaker_affordance.dart
tts_page_guides.dart
Semantics usage
cycling guidance cues
language picker
large/safe buttons and controls
```

V2 should unify these into a coherent accessibility system instead of scattering them across screens.

---

# 5. IMPORTANT IMPLEMENTATION REALITY / KNOWN GAPS

These items were found during static repo analysis. They must not be presented as production-ready functionality unless they are actually implemented later.

## 5.1 Documentation vs backend database mismatch

The README describes Supabase/Postgres, but the inspected backend implementation currently uses SQLAlchemy with SQLite (`backend/craftsy.db`).

**Rule:** Do not migrate databases during the UI redesign unless explicitly requested. Keep this as a documented technical debt item.

## 5.2 Orders are currently mock/demo-oriented

The frontend has order screens and an order provider, but the inspected backend does not currently have a full persistent order subsystem equivalent to the product system.

**Rule:** During V2 UI work, maintain clear demo labels/data boundaries and do not imply a fully persistent production order backend until implemented.

## 5.3 Analytics depends on limited order data

Statistics/revenue views should be redesigned with this limitation in mind.

## 5.4 Authentication is demo-grade

The repository includes login/OTP flows, but parts of authentication are clearly demo-oriented.

**Rule:** Do not fabricate security claims in UI copy.

## 5.5 NGO verification is currently limited/demo-oriented

Treat helper/NGO concepts as a future trust-support mechanism unless the underlying verification system is implemented.

## 5.6 Notifications are not equivalent to a production push system

Do not build critical UX around guaranteed push delivery.

## 5.7 Localization scope is not the same at every layer

The frontend currently has packaged translation files for:

```text
en
hi
ta
bn
```

The backend/documentation discusses broader Indian-language support.

**Rule:** Do not expose a language as “fully supported” unless the relevant UI/voice behavior exists.

---

# 6. CRAFTSY V2 UX PRINCIPLES

These principles override aesthetic preferences.

## P1 — No-reading path

A core task must be completable without reading long paragraphs.

## P2 — Voice-first, not voice-only

Voice is primary but must have visual fallback for noisy environments, speech recognition errors, hearing limitations, and user preference.

## P3 — Photo-first

Use images and icons to communicate product concepts wherever possible.

## P4 — One decision per screen/state

Avoid presenting five form fields and six competing buttons at once.

## P5 — Show, speak, confirm

Preferred pattern:

```text
INPUT
  ↓
AI PROCESSING
  ↓
SHOW RESULT
  ↓
🔊 READ RESULT
  ↓
👍 CONFIRM / 👎 CHANGE
```

## P6 — Never expose technical vocabulary to the artisan

Avoid terms such as:

- SKU
- SEO
- vector
- embedding
- confidence score
- cost floor
- RAG
- metadata
- draft payload
- sync queue

Translate internal concepts into everyday language.

## P7 — Large touch targets

Primary actions should be comfortably finger-operable. Avoid dense navigation and tiny icon-only buttons.

## P8 — Strong visual hierarchy

The artisan should know the primary action within 1–2 seconds without reading a paragraph.

## P9 — Confirm before irreversible or public actions

Publishing, deleting, changing important price information, and final actions require clear confirmation.

## P10 — Recover gracefully

Every failure should offer a simple next action:

```text
Try again
Speak again
Take another photo
Do this later
```

rather than exposing raw exceptions.

## P11 — Offline is visible, not alarming

Show a simple state such as:

```text
🟢 Connected
🟠 Will upload when internet returns
```

Do not show infrastructure terminology.

## P12 — Artisan remains the final decision maker

AI recommends; artisan confirms.

## P13 — Dignity over charity aesthetics

Avoid making the artisan UI look like a “welfare app”. It should feel premium, capable, and empowering.

## P14 — Indian craft identity without visual overload

Retain the craft-inspired personality but reduce decorative elements that compete with core actions.

---

# 7. NEW INFORMATION ARCHITECTURE

## 7.1 Proposed artisan home

The new home should reduce the primary interaction set to approximately five things:

```text
                🎤
          ASK / SPEAK TO CRAFTSY

     📸             📦              💰
   SELL         MY ORDERS        MY MONEY

                  🤝
             ASK CRAFTMITRA
```

The exact visual layout may change during implementation, but the information architecture must remain simple.

## 7.2 Navigation model

Preferred primary nav:

```text
🏠 Home
📦 Orders
➕ Sell
💰 Money
👤 Me
```

Voice should be available from Home and from major contextual screens.

## 7.3 Advanced features

Do not put every capability in the primary navigation.

Secondary/advanced actions can include:

- social media helper
- product statistics
- packaging suggestions
- labels/QR
- language settings
- helper/NGO mode
- advanced catalogue management

The home screen should not become a feature directory.

---

# 8. FLAGSHIP FLOW — “SELL SOMETHING”

This is the most important V2 flow.

## 8.1 Entry points

Artisan may initiate from:

```text
🎤 “मुझे अपना सामान बेचना है”

OR

👆 Sell something

OR

📸 directly take a product photo
```

All three should converge into the same underlying product workflow.

## 8.2 Step A — Capture

Screen should visually ask for one thing:

```text
📸
अपने सामान की फोटो लें

[ CAMERA ]

🔊 “सामान को साफ जगह पर रखें और फोटो लें।”
```

No dense instructions.

## 8.3 Step B — Describe

Primary input:

```text
🎤
इस सामान के बारे में बोलें

[ HOLD / TAP TO SPEAK ]
```

Optional text input remains available but secondary.

Example spoken input:

> “ये नीले रंग की हाथ से बनी मिट्टी की सुराही है, इसे बनाने में दो दिन लगे।”

## 8.4 Step C — AI result

Show one clean product card:

```text
[IMAGE]

🏺 मिट्टी की सुराही
₹250

🔊 सुनें

👍 सही है
✏️ कुछ बदलना है
```

AI-generated title/description/category/tags can exist behind an expandable “details” section.

## 8.5 Step D — Fair price

The pricing UI must feel like guidance, not a financial spreadsheet.

Preferred presentation:

```text
💰 आपकी सुझाई कीमत

      ₹250

इस कीमत में आपकी मेहनत
और सामान दोनों शामिल हैं.

🔊 सुनें

[ ₹200 ]   [ ₹250 ]   [ ₹300 ]

        👍 ठीक है
```

Advanced details may expose:

- material cost
- labour
- transport
- market references
- suggested range

but only after the primary answer is understood.

## 8.6 Step E — Publish

Final confirmation:

```text
✨ सामान तैयार है

[IMAGE]

🏺 मिट्टी की सुराही
₹250

🔊 सुनें

[ 🟢 बेचने के लिए डालें ]
```

After publishing:

```text
🎉 आपका सामान अब बिक्री के लिए तैयार है.
```

---

# 9. AI SAATHI / CRAFTMITRA V2

## 9.1 Strategic role

CraftMitra should become the **action layer** of the application, not merely a chat screen.

## 9.2 Supported natural intents

Initial intent vocabulary:

```text
ADD_PRODUCT
VIEW_PRODUCTS
VIEW_ORDERS
CHECK_ORDER
VIEW_EARNINGS
CHANGE_PRICE
EDIT_PRODUCT
SHARE_PRODUCT
ASK_PRICE
ASK_CRAFT_ADVICE
CHANGE_LANGUAGE
GET_HELP
```

## 9.3 Intent architecture

Preferred model:

```text
Voice / Text / Tap
       ↓
CraftMitra understanding
       ↓
CraftsyIntent
       ↓
Existing repository/service/API
       ↓
Result
       ↓
Visual response + TTS
```

Do not create separate implementations for the same action merely because the entry method is different.

## 9.4 Response style

Responses must be short and action-oriented.

Bad:

> “Your request has been successfully processed and your current product inventory is available through the catalogue section.”

Better:

> “आपके 8 सामान बिक रहे हैं।”

Then offer:

```text
📦 सामान देखें
```

---

# 10. LOW-LITERACY DESIGN SYSTEM

## 10.1 Typography

Use the existing font system where appropriate, but redesign hierarchy around readability rather than decoration.

Rules:

- body text must remain comfortable at large accessibility settings
- do not depend on very small captions
- avoid long uppercase labels
- avoid putting critical meaning only in typography weight/color

## 10.2 Buttons

Primary actions should:

- be large
- contain icon + short label when text is used
- support Semantics
- have clear pressed/disabled states
- be understandable without context

## 10.3 Icons

Use recognizable metaphors:

```text
📸 photo
🎤 voice
📦 orders
💰 earnings
👤 profile
🏠 home
🔊 listen
👍 confirm
👎 change/retry
➕ add
🗑 delete
```

Do not use abstract icons when a concrete metaphor is available.

## 10.4 Color

Current theme uses an “Indigo Loom” visual identity. Preserve the brand personality but prioritize:

- high contrast
- obvious active/inactive states
- color + icon + text rather than color alone

## 10.5 Decorative motifs

Existing craft motifs may remain as subtle brand language:

- Warli-inspired pattern
- tanka stitch
- petal ring
- mehrab
- dotted border

But decorative elements must never make the primary action less obvious.

---

# 11. VOICE & AUDIO UX SPECIFICATION

## 11.1 Voice should always have visible state

```text
READY
🎤 बोलें

LISTENING
🔴 सुन रहा हूँ...

PROCESSING
✨ समझ रहा हूँ...

RESULT
🔊 सुनें

ERROR
⚠️ फिर से बोलें
```

## 11.2 Never hide recording state

Users must know whether the phone is:

- waiting
- listening
- processing
- finished

## 11.3 TTS

For user-critical actions:

- use concise sentences
- speak the main result
- avoid reading long UI trees
- allow replay

## 11.4 Voice confirmation

Where supported:

```text
AI: “कीमत 250 रुपये रखें?”

USER: “हाँ”

→ confirm
```

But visual confirmation remains available.

## 11.5 Speech recognition failure

Never say only:

> “ASR failed.”

Instead:

> “मैं ठीक से सुन नहीं पाया। फिर से बोलें।”

with:

```text
🎤 फिर से बोलें
✍️ लिखें
```

---

# 12. SCREEN-BY-SCREEN V2 TARGET

## 12.1 Splash

Goal: fast, calm brand introduction.

Must not contain long marketing text.

## 12.2 Language selection

Language choice should be visual and audio-assisted.

Preferred pattern:

```text
🌐
आप कौन-सी भाषा में बात करना चाहते हैं?

हिन्दी
தமிழ்
বাংলা
English
```

Add speaker support so the user can hear language names/instructions.

## 12.3 Authentication

Keep the auth flow simple.

Avoid exposing technical account concepts.

Example:

```text
📱 अपना मोबाइल नंबर डालें
```

Then voice/read-back where appropriate.

## 12.4 Home

This is the highest-priority redesign screen.

Primary goal: make the next action obvious without a menu-learning period.

## 12.5 Add Product

Use the flagship five-stage workflow but make it feel like one guided conversation rather than five form pages.

## 12.6 Catalogue

Rename concepts into familiar language.

Potential framing:

```text
🛍️ मेरा सामान
```

Each product card should prioritize:

- image
- product name
- price
- availability/status
- listen button

## 12.7 Product detail

Keep the artisan story and product authenticity visible.

## 12.8 Orders

Use visual order states rather than dense tables.

Example:

```text
🟡 नया
🔵 तैयार करें
🚚 रास्ते में
🏠 पहुंच गया
```

## 12.9 Earnings

Use simple language:

```text
💰 इस महीने
₹12,450
```

Then optionally:

```text
📦 38 सामान बिके
```

Do not lead with charts.

## 12.10 Profile / Me

Organize secondary controls:

- language
- accessibility
- helper
- account
- help

## 12.11 CraftMitra

Should open as an immersive assistant/action surface rather than a conventional developer-looking chatbot.

## 12.12 Social media

Frame as an action:

> “अपने सामान का प्रचार करें”

not as a technical “social media helper”.

---

# 13. IMPLEMENTATION ROADMAP

Work in phases. Do not jump directly to Phase 7 before Phase 1 is stable.

## PHASE 0 — Baseline freeze / safety

### Goals

- ensure repository builds/analyses in the available environment
- document current behavior
- establish V2 branch/working state
- avoid accidental backend changes

### Tasks

- run Flutter analyze if Flutter is available
- run relevant Flutter tests
- run backend tests if Python dependencies are installed
- record failures that are environment/tooling issues vs code defects
- confirm API base URL/config
- confirm current feature flags / demo behavior

### Acceptance

There is a written baseline and no unexplained destructive changes.

---

## PHASE 1 — V2 design foundation

### Goals

Create a reusable accessibility-first design system.

### Tasks

Refactor/create reusable components for:

```text
VoiceActionButton
SpeakButton
LargeActionCard
PrimaryActionButton
SecondaryActionButton
ConfirmRejectRow
VisualStatusChip
GuidedStepShell
ListeningState
ProcessingState
EmptyState
OfflineState
AccessibilityToggle
```

Create central tokens for:

- spacing
- minimum touch target sizes
- corner radii
- typography scale
- semantic colors
- elevation

### Acceptance

No core V2 screen needs to hand-build the same accessibility behavior repeatedly.

---

## PHASE 2 — Navigation / Home redesign

### Goals

Replace conventional dashboard navigation with the new artisan-centered information architecture.

### Tasks

- redesign `HomeShell`
- introduce simplified home actions
- integrate CraftMitra/AI Saathi as primary action surface
- preserve access to advanced features via secondary navigation
- preserve existing providers/services

### Acceptance

A new user can identify how to sell, view orders, and ask for help without learning a complex menu.

---

## PHASE 3 — Sell Something / Add Product redesign

### Goals

Turn the existing five-step flow into a guided, multimodal experience.

### Tasks

- redesign Step 1 camera
- redesign Step 2 voice
- redesign Step 3 AI review
- redesign Step 4 price
- redesign Step 5 confirmation
- connect TTS to the important states
- maintain draft/resume behavior
- maintain offline behavior

### Acceptance

A user can complete a product listing with:

```text
photo + voice + confirmation
```

without needing to type a long form.

---

## PHASE 4 — AI Saathi / intent-driven actions

### Goals

Make CraftMitra capable of performing common app actions through natural language.

### Tasks

- formalize intent model
- map intents to existing services/repositories
- support voice + text input
- implement concise responses
- preserve TTS
- add contextual quick actions

### Acceptance

Example requests should work through the shared action architecture:

```text
“मेरा ऑर्डर दिखाओ”
“मेरी कमाई बताओ”
“नया सामान जोड़ना है”
“इस सामान की कीमत बताओ”
```

---

## PHASE 5 — Catalogue / Orders / Earnings redesign

### Goals

Make existing secondary workflows visually simple and honest about backend capability.

### Tasks

- redesign catalogue cards
- redesign product detail
- redesign orders
- redesign order detail
- redesign earnings/statistics
- add listen affordances where useful

### Acceptance

Critical information can be understood visually and through TTS without dense tables.

---

## PHASE 6 — Accessibility & localization hardening

### Tasks

- audit Semantics
- audit text scaling
- audit contrast
- audit minimum touch targets
- verify all primary actions have understandable labels
- verify TTS wording
- verify Hindi and currently shipped locales
- verify fallback behavior
- remove hard-coded English strings from redesigned paths

### Acceptance

A screen-by-screen accessibility checklist passes.

---

## PHASE 7 — Offline / failure-state UX

### Tasks

- redesign offline banner/state
- redesign queued upload states
- redesign sync errors
- preserve draft recovery
- ensure users can continue when cloud services are unavailable

### Acceptance

Users are told what is happening in human language and are never exposed to infrastructure errors.

---

## PHASE 8 — Advanced capabilities

Only after core UX is stable:

- social media promotion
- packaging suggestions
- labels / QR
- helper / NGO flows
- richer analytics
- additional languages

---

## PHASE 9 — Polish / SIH demo mode

### Goals

Prepare the app for a clean live demonstration.

### Priority demo flow

```text
LOGIN
 ↓
SELECT LANGUAGE
 ↓
HOME
 ↓
“मैं नया सामान बेचना चाहता हूँ”
 ↓
CAMERA
 ↓
PHOTO
 ↓
VOICE DESCRIPTION
 ↓
AI LISTING
 ↓
FAIR PRICE
 ↓
TTS READBACK
 ↓
ARTISAN CONFIRMS
 ↓
PRODUCT PUBLISHED
```

The demo must show the differentiated product behavior, not merely visual polish.

---

# 14. EXECUTION STATUS

This section must be updated after work.

## Current phase

**PHASE 0 — Baseline freeze / safety**

## Completed baseline audit

- [x] Repository extracted and statically inspected
- [x] Frontend structure inspected
- [x] Backend structure inspected
- [x] ML image pipeline inspected
- [x] ML voice pipeline inspected
- [x] ML pricing architecture inspected
- [x] Existing routes inspected
- [x] Add Product flow inspected
- [x] CraftMitra architecture inspected
- [x] Offline architecture identified
- [x] Accessibility infrastructure identified
- [x] Documentation/implementation mismatches recorded

## Phase 1

- [ ] Accessibility design tokens
- [ ] Reusable voice action component
- [ ] Reusable speak/listen component
- [ ] Large action card
- [ ] Visual status component
- [ ] Guided screen shell
- [ ] Common confirmation component

## Phase 2

- [ ] New HomeShell architecture
- [ ] Simplified artisan home
- [ ] New primary navigation
- [ ] AI Saathi integration point

## Phase 3

- [ ] New Capture UX
- [ ] New Voice UX
- [ ] New AI Review UX
- [ ] New Pricing UX
- [ ] New Publish UX

## Phase 4

- [ ] Intent model
- [ ] Voice action routing
- [ ] Text action routing
- [ ] Contextual assistant actions

## Phase 5

- [ ] Catalogue redesign
- [ ] Product detail redesign
- [ ] Orders redesign
- [ ] Earnings redesign

## Phase 6

- [ ] Semantics audit
- [ ] Touch-target audit
- [ ] Text scaling audit
- [ ] Contrast audit
- [ ] Localization audit
- [ ] TTS audit

## Phase 7

- [ ] Offline-state redesign
- [ ] Queue/sync UX
- [ ] Failure recovery UX

## Phase 8

- [ ] Social media
- [ ] Packaging
- [ ] Labels/QR
- [ ] Helper mode
- [ ] Additional languages

## Phase 9

- [ ] SIH demo path
- [ ] Demo data cleanup
- [ ] Performance pass
- [ ] Final accessibility pass
- [ ] Final visual polish

---

# 15. DECISION LOG

Use this section whenever architecture/product decisions are made.

## D-001 — Keep existing backend/ML and redesign experience first

**Decision:** Preserve existing AI/ML and service architecture where functional; focus V2 effort on the interaction layer.

**Reason:** Craftsy already contains substantial voice, image, pricing, offline, TTS, and assistant infrastructure. A rewrite would create unnecessary risk and lose working functionality.

## D-002 — CraftMitra becomes an action interface

**Decision:** Evolve CraftMitra from a floating chat feature into the action/intent layer for the artisan experience.

**Reason:** Voice/text/tap interactions should converge on the same actions instead of creating duplicate implementations.

## D-003 — Simple home information architecture

**Decision:** Reduce primary artisan navigation to a small set of understandable tasks rather than exposing every feature.

**Reason:** Low-literacy users should not have to learn the app's internal information architecture.

## D-004 — Old HTML redesign is historical reference

**Decision:** Do not use `craftsy-redesign-v3.html` as V2's visual source of truth.

**Reason:** It represents a prior design iteration and a more conventional dashboard model.

## D-005 — Do not migrate database during UI redesign

**Decision:** The Supabase-vs-SQLite mismatch is tracked as technical debt, but database migration is outside the initial V2 UX scope.

**Reason:** Mixing major infrastructure migration with a full UX redesign increases risk and makes AI-agent work harder to control.

---

# 16. DEFINITION OF DONE — EVERY USER-FACING V2 FEATURE

A feature is not done because it compiles.

It is done only when all applicable criteria are true:

### UX

- [ ] Primary action is obvious
- [ ] User does not face unnecessary choices
- [ ] Text is short and simple
- [ ] Visual feedback is immediate
- [ ] Important result can be heard

### Accessibility

- [ ] Semantics label exists where appropriate
- [ ] Touch target is comfortably large
- [ ] Contrast is sufficient
- [ ] Meaning does not rely on color alone
- [ ] Text scaling does not break the layout
- [ ] Voice fallback exists for core actions where appropriate

### Localization

- [ ] No unnecessary hard-coded UI English
- [ ] Translation key exists for supported locales
- [ ] TTS wording is localized where available
- [ ] The UI does not overflow with longer translated strings

### Error handling

- [ ] Network failure handled
- [ ] AI failure handled
- [ ] Voice failure handled
- [ ] User has a clear recovery action
- [ ] Technical exception text is never presented directly

### Technical

- [ ] Existing service/repository reused when possible
- [ ] No duplicate implementation introduced
- [ ] State management remains consistent with Riverpod
- [ ] Routing remains coherent
- [ ] Relevant tests added/updated
- [ ] No secret/API key committed

---

# 17. DO / DON'T FOR AI AGENTS

## DO

- inspect existing code before editing
- reuse existing providers, repositories, services, and ML endpoints
- create reusable UI primitives
- keep the artisan flow short
- add TTS to important decisions
- make voice state obvious
- design for one-handed phone use
- use local language strings
- preserve offline behavior
- test the exact changed feature
- keep changes incremental
- document architectural decisions

## DON'T

- rewrite the whole Flutter app
- replace Riverpod without a compelling reason
- replace FastAPI/ML architecture during UX work
- invent Supabase behavior that doesn't exist in the current implementation
- represent mock orders as real persistent orders
- add fake analytics
- add decorative animations everywhere
- put every feature on the home screen
- require typing for essential artisan tasks
- make AI outputs automatically public without human confirmation
- expose raw API/exception errors to artisans
- create duplicate service layers just for the new UI
- remove offline capability
- remove TTS or Semantics because they complicate styling

---

# 18. RECOMMENDED CODE ORGANIZATION FOR V2

Refactor toward reusable interaction primitives without forcing a total directory rewrite.

Suggested additions:

```text
frontend/lib/
├── core/
│   ├── accessibility/
│   │   ├── accessibility_tokens.dart
│   │   ├── accessibility_service.dart
│   │   └── accessibility_settings.dart
│   └── widgets/
│       ├── voice_action_button.dart
│       ├── speak_button.dart
│       ├── large_action_card.dart
│       ├── guided_state.dart
│       ├── confirm_reject_row.dart
│       └── visual_status.dart
│
└── features/
    ├── artisan_home/
    │   ├── screens/
    │   ├── widgets/
    │   └── providers/
    │
    └── assistant/
        ├── models/
        │   └── craftsy_intent.dart
        ├── services/
        │   └── intent_action_service.dart
        ├── providers/
        └── widgets/
```

This is a direction, not a license to perform a giant file move in one task.

---

# 19. ACCEPTANCE SCENARIOS

These are product-level tests that should guide development.

## Scenario A — New artisan, no typing

```text
User opens Craftsy
→ chooses Hindi
→ hears/understands onboarding
→ taps or speaks “मुझे सामान बेचना है”
→ takes photo
→ speaks description
→ hears AI result
→ hears price
→ confirms
→ listing is created
```

No long-form typing should be required.

## Scenario B — User cannot remember navigation

```text
User: “मेरा ऑर्डर कहाँ है?”
→ CraftMitra understands intent
→ opens relevant order state
→ reads the important status aloud
```

## Scenario C — Poor internet

```text
User captures a product
→ app stores work locally
→ user continues
→ app clearly says it will upload later
→ network returns
→ background sync occurs
```

## Scenario D — Voice recognition error

```text
User speaks
→ recognition is unclear
→ app says it did not understand
→ user can speak again or use visual fallback
```

## Scenario E — AI wrong result

```text
AI suggests wrong title/category/price
→ artisan can reject/change
→ AI does not silently publish it
```

---

# 20. SIH DEMO PRINCIPLES

The demo should prove four things quickly:

```text
ACCESSIBILITY
   +
AI AUTOMATION
   +
FAIR PRICING
   +
OFFLINE RESILIENCE
```

Do not spend the entire demo on:

- login screens
- profile editing
- static dashboards
- decorative animations

The hero moment is:

```text
ONE PHOTO
+
ONE SPOKEN SENTENCE
+
ONE CONFIRMATION
=
SELLABLE PRODUCT
```

Then show that the system can explain the result back to the artisan in their language.

---

# 21. FINAL PRODUCT CHECKLIST

Craftsy V2 should eventually satisfy:

- [ ] An artisan can understand the home screen mostly from icons, images, short labels, and audio.
- [ ] The primary selling flow does not require typing.
- [ ] Voice and visual interactions use the same underlying actions.
- [ ] AI outputs are understandable and confirmable.
- [ ] Product photography is improved automatically.
- [ ] Product listing content is generated automatically.
- [ ] Pricing is presented in a human-understandable way.
- [ ] The app remains usable with intermittent connectivity.
- [ ] Errors are actionable and non-technical.
- [ ] The app does not bury essential actions behind menus.
- [ ] Current working AI/ML/backend capabilities are preserved.
- [ ] Mock/demo limitations remain clearly separated from production claims.
- [ ] Localization is honest about what is actually supported.
- [ ] The artisan remains in control of publishing and pricing decisions.
- [ ] The application feels premium and empowering rather than charity-oriented.

---

# 22. OPERATING RULE FOR FUTURE PROMPTS

When using an AI coding agent, start prompts with something equivalent to:

> Read `CRAFTSY_V2_MASTER_PLAN.md` before making any changes. Treat it as the source of truth. Work only on the requested phase/task. Preserve existing working services and ML pipelines. Do not redesign unrelated features. After implementation, test the changed area and update the execution status and decision log in the master plan.

Then give the agent **one concrete task at a time**.

Example:

> Read `CRAFTSY_V2_MASTER_PLAN.md`. Implement Phase 1: create the reusable `VoiceActionButton` and `SpeakButton` components. Do not redesign HomeShell yet. Reuse the existing TTS service. Add/update tests and update the master plan status when complete.

This keeps AI-agent changes bounded and prevents the model from trying to rebuild the entire application at once.

---

# 23. ONE-SENTENCE NORTH STAR

> **Craftsy V2 should feel less like an e-commerce app that an artisan has to learn, and more like a trusted digital companion that understands what the artisan wants to do.**

