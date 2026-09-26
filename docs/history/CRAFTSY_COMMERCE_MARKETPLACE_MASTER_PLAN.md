# CRAFTSY — COMMERCE & MARKETPLACE MASTER PLAN

## Post-Phase-8 Roadmap

> **Status:** New roadmap after Phases 0–8 have been completed and merged into `main`.
>
> **Goal:** Transform Craftsy into a unified artisan commerce platform: **Craftsy Marketplace + ONDC + Government/GeM workflow**, powered by the existing AI, Bhashini, accessibility, multilingual and voice-first foundations.
>
> **Critical rule:** Never claim that Craftsy is ONDC- or GeM-integrated until the corresponding real onboarding/integration has actually been completed and tested.

---

# 0. AGENT OPERATING RULES

Every AI coding agent MUST:

1. Read this file completely before changing code.
2. Read the existing `CRAFTSY_V2_MASTER_PLAN.md` and inspect the repository.
3. Treat Phases 0–8 as COMPLETE. Do not redo or regress them.
4. Reuse existing models, services, navigation, design system, accessibility, localization, Bhashini/language and AI infrastructure where appropriate.
5. Inspect existing implementation before creating abstractions.
6. Never create fake ONDC/GeM success states.
7. Keep credentials, tokens, signing keys and external secrets server-side.
8. Never let AI invent mandatory product, identity, tax, certification, inventory or procurement information.
9. Missing information must produce a clear question or guided form.
10. Preserve low-literacy, voice-first, multilingual and accessibility principles.
11. Use one canonical product, inventory and order model wherever possible.
12. Run formatter, analyzer/linter, tests and relevant builds after meaningful changes.
13. Update this roadmap with implementation notes, limitations and test results after every phase.
14. Keep each phase independently reviewable and commit-friendly.

---

# 1. PRODUCT VISION

Craftsy becomes a **digital commerce operating system for Indian artisans**.

An artisan should be able to:

- create a product once;
- sell it on the Craftsy Marketplace;
- prepare/publish it to ONDC after real ONDC onboarding;
- use a guided government-selling workflow for GeM;
- manage inventory once;
- receive orders from multiple channels in one inbox;
- use voice, regional languages, images, Bhashini and AI without understanding technical commerce systems.

Target architecture:

```text
                     CRAFTSY
                        |
              Artisan / Buyer Experience
                        |
                 Bhashini + AI
                        |
                  Commerce Engine
                        |
       +----------------+----------------+
       |                |                |
   Marketplace        ONDC          Government/GeM
     Channel         Adapter          Workflow
       |                |                |
       +----------------+----------------+
                        |
              Product / Order /
               Inventory Engine
```

---

# PHASE 9 — COMMERCE FOUNDATION

## Objective

Build the reusable commerce layer required by all three selling channels.

## Tasks

### 9.1 Existing-system audit

Inspect:
- current product/catalogue models;
- artisan/profile models;
- inventory;
- orders;
- backend/API;
- authentication;
- image/file handling;
- AI services;
- Bhashini/language services.

Produce an implementation map before changing architecture.

### 9.2 Canonical product model

Design one canonical Craftsy product using actual existing fields first. Conceptual areas may include:

- product ID;
- artisan ID;
- title/description;
- images;
- category/material;
- dimensions/weight where relevant;
- price;
- stock;
- variants;
- location;
- publication status.

Do not blindly add speculative fields.

### 9.3 Channel abstraction

Create a provider abstraction conceptually equivalent to:

```text
CommerceChannel
  - CraftsyChannel
  - ONDCChannel
  - GeMChannel
```

Expose only operations that a channel actually supports, e.g. validation, publishing, update, unpublish and status.

### 9.4 Channel state

Support states such as:

```text
Not Connected
Needs Information
Ready
Pending
Published
Syncing
Action Required
Failed
Unavailable
```

Keep technical details out of the primary artisan UI.

### Definition of Done

- Canonical product strategy documented.
- Commerce/channel abstraction implemented or clearly scaffolded.
- Existing functionality remains intact.
- Tests/build pass.

---

# PHASE 10 — CRAFTSY MARKETPLACE

## Objective

Build Craftsy's own consumer marketplace. This is a selling channel, not a replacement for ONDC.

## Features

- marketplace home;
- search;
- categories;
- filters;
- product discovery;
- product detail;
- cart;
- checkout;
- customer orders;
- artisan discovery;
- favourites/wishlist only if compatible with existing architecture;
- reviews extension points.

## UX direction

Make it feel like a **human, craft-focused marketplace**, not an AI dashboard.

Use the existing Craftsy design system. Do not create a second visual system.

## Voice discovery

Support examples such as:

```text
"Show handmade gifts under ₹2000."
"मुझे मिट्टी के दीये दिखाओ।"
"Show blue handwoven sarees."
```

Voice is an additional discovery method, not the only method.

---

# PHASE 11 — ARTISAN STOREFRONTS

Give every artisan a Craftsy storefront.

Include, where supported:

- artisan profile;
- photo;
- craft description;
- location;
- craft tradition/story;
- products;
- ratings/trust indicators.

A product page should make the artisan visible:

```text
Handwoven Maheshwari Saree
₹2,499

Made by Meera Handcrafts
Madhya Pradesh

Craft: Handloom weaving
Material: Cotton/Silk

[Buy Now]
```

Never invent provenance, authenticity or certification claims.

---

# PHASE 12 — MULTI-CHANNEL PUBLISHING

Primary interaction:

> **Where do you want to sell this?**

Example:

```text
🛍 Craftsy
✓ Ready

🌐 ONDC
⚠ Setup required
[Set up]

🏛 Government Selling
⚠ Setup/eligibility needed
[Set up]
```

Clearly distinguish planned, configured, connected, published, pending, failed and actually live.

Never show a green "live" state for an unverified integration.

---

# PHASE 13 — ONDC INTEGRATION FOUNDATION

The uploaded ONDC Developer Guide organizes the technical journey around onboarding/role determination, API understanding/development, authorization, staging, pre-production and production. It describes ONDC's protocol architecture as based on Beckn with ONDC-specific API contracts. See the uploaded guide, especially its onboarding/API and authorization sections.

## Tasks

### 13.1 Determine Craftsy's ONDC role

Investigate the appropriate seller-side participant role. Because Craftsy is intended to aggregate many independent artisans, evaluate the Marketplace Seller Node path carefully, but do not treat that assumption as final until current ONDC requirements are verified.

### 13.2 Backend-only architecture

```text
Flutter
  ↓
Craftsy Backend
  ↓
ONDC Integration Service
  ↓
ONDC Network
```

Never expose ONDC signing keys or credentials to Flutter.

### 13.3 ONDC adapter

Responsibilities may include:

- catalogue mapping;
- request/response mapping;
- authorization/signing;
- callbacks;
- status synchronization;
- error handling;
- transaction logging;
- environment configuration.

Use the current official ONDC specification for actual contracts.

### 13.4 Environments

Support separate configuration for:

```text
Development
Staging
Pre-production
Production
```

The uploaded guide explicitly identifies staging as the initial integration/testing environment and pre-production as the environment before production certification.

### 13.5 Onboarding checklist

Track:

- participant role;
- registration/onboarding;
- endpoint readiness;
- signing/authentication;
- registry requirements;
- API implementation;
- staging testing;
- pre-production certification/readiness;
- production readiness.

### Definition of Done

Either:

**A.** real ONDC staging integration is operational, or

**B.** Craftsy has an ONDC-ready adapter with clearly documented onboarding blockers.

Never simulate successful network transactions.

---

# PHASE 14 — ONDC CATALOGUE + ORDER FLOW

Only start after Phase 13 has a validated technical foundation.

Implement the current ONDC catalogue mapping and applicable transaction/callback flows using official specifications.

Normalize ONDC orders into the unified Craftsy order model.

Keep channel identity and external references on every order.

Expose understandable states such as:

```text
Order received
Confirmed
Preparing
Dispatched
Delivered
Cancelled
```

Use actual protocol states internally where required.

---

# PHASE 15 — GOVERNMENT / GeM SELLING FOUNDATION

## Objective

Create a government-selling workflow without pretending GeM is just another consumer marketplace.

GeM should be treated as a separate procurement channel with seller onboarding, catalogue requirements and government-order/bid workflows.

## Critical constraint

Do **not** invent a GeM API.

First establish what official integration mechanisms and authorization are actually available to Craftsy.

If direct integration is not available/authorized, implement:

```text
Craftsy Government Selling Assistant
             ↓
      Prepare / Validate
             ↓
      Assisted GeM workflow
```

## Tasks

- guided government seller setup;
- identify required seller information;
- identify category requirements;
- identify required documents/certifications where applicable;
- validate catalogue completeness;
- prepare government catalogue data;
- preserve a path for an official API integration if one becomes available.

Never fabricate certifications, licences, seller identity, tax information or procurement data.

Use the user-facing wording **Sell to Government** rather than exposing technical adapter terminology.

---

# PHASE 16 — UNIFIED ORDERS

Create one order inbox regardless of channel.

```text
MY ORDERS

🛍 Craftsy — Handwoven Saree — ₹2,499 — Preparing
🌐 ONDC — Bamboo Basket — ₹799 — Order received
🏛 Government — 50 Files — ₹18,500 — Fulfilment
```

Internally:

```text
UnifiedOrder
  ├── Craftsy
  ├── ONDC
  └── Government
```

Every external order retains its source channel and external reference.

---

# PHASE 17 — UNIFIED INVENTORY

Create one inventory source of truth to prevent overselling.

Example:

```text
Stock = 10
Craftsy sold = 2
ONDC sold = 3
Government reserved = 1
Available = 4
```

Implement where appropriate:

- stock quantity;
- reservations;
- deductions;
- channel synchronization;
- conflict handling;
- reconciliation;
- auditable manual corrections.

---

# PHASE 18 — AI COMMERCE AGENT

Use the existing AI/Bhashini foundation to let artisans operate commerce naturally.

Example:

> "मेरा नया टेराकोटा दिया Craftsy और ONDC पर बेच दो।"

Flow:

```text
Voice/Text
 ↓
Bhashini
 ↓
Intent detection
 ↓
Product identification
 ↓
Required-field validation
 ↓
Channel validation
 ↓
User confirmation
 ↓
Commerce action
 ↓
Verified result
```

AI must never invent:

- price;
- stock;
- weight;
- certification;
- tax information;
- seller identity;
- external publication success.

---

# PHASE 19 — BHASHINI + COMMERCE

Reuse the existing centralized Bhashini architecture. Do not create another ASR/TTS/language system inside marketplace screens.

Target:

```text
Artisan
 ↓
Speech/Text
 ↓
Bhashini
 ↓
Craftsy AI
 ↓
Commerce Agent
 ↓
Craftsy / ONDC / Government
```

Maintain consistency between selected language, recognition, translations and spoken responses.

---

# PHASE 20 — MARKETPLACE DISCOVERY + AI SEARCH

Support:

- keyword search;
- category search;
- filters;
- price range;
- material;
- location;
- craft type;
- artisan;
- availability;
- natural-language search;
- voice search.

Example:

> "Find a handmade wedding gift under ₹2,000 from Madhya Pradesh."

AI may turn this into structured filters, but results must come from actual catalogue data.

---

# PHASE 21 — TRUST, REVIEWS, RETURNS & SAFETY

Implement the minimum marketplace trust foundation:

- product reviews;
- appropriate ratings;
- order status;
- cancellation;
- returns/refunds extension points;
- dispute extension points;
- report product/seller;
- moderation hooks.

Keep the implementation proportional to the SIH scope.

---

# PHASE 22 — ARTISAN COMMERCE ANALYTICS

Provide simple, understandable numbers:

```text
This Month
Products sold       24
Orders              18
Earnings            ₹18,450
Craftsy orders      10
ONDC orders          6
Government orders    2
```

Avoid overwhelming dashboard-style analytics.

---

# PHASE 23 — END-TO-END QA

## Artisan

```text
Register
 ↓
Create product
 ↓
Add image/price/stock
 ↓
Publish on Craftsy
 ↓
Select ONDC
 ↓
Validate requirements
 ↓
Select Government Selling
 ↓
Validate requirements
 ↓
Manage inventory
 ↓
Receive orders
 ↓
Fulfil orders
```

## Buyer

```text
Marketplace
 ↓
Search
 ↓
Product
 ↓
Artisan
 ↓
Cart
 ↓
Checkout
 ↓
Order tracking
```

## Voice

```text
Speak → ASR → Intent → Commerce Agent → Validation → Confirmation → Action → TTS
```

Test each external channel only according to its actual available environment/authorization.

---

# PHASE 24 — ACCESSIBILITY + LOW-LITERACY COMMERCE AUDIT

Reuse completed accessibility foundations and audit:

- 48dp touch targets;
- screen-reader semantics;
- large text;
- high contrast;
- color-independent status;
- voice alternatives;
- icon + label consistency;
- clear errors/loading/empty states;
- offline behavior;
- multilingual UI;
- TTS;
- keyboard/accessibility navigation;
- confirmation dialogs;
- cognitive load.

Key test:

> Can an artisan with limited digital literacy create and publish a product without understanding technical e-commerce terminology?

---

# PHASE 25 — SECURITY + DATA PROTECTION AUDIT

Review:

- authentication/authorization;
- API access;
- secrets;
- ONDC credentials;
- GeM credentials if applicable;
- uploaded documents;
- personal/order data;
- logging;
- error responses.

Never log keys, tokens, passwords or unnecessary sensitive identity information.

---

# PHASE 26 — PRODUCTION READINESS + SIH DEMO

Verify:

- release build;
- backend deployment;
- database/storage;
- environment variables;
- monitoring;
- error handling;
- offline behavior;
- tests;
- integration status.

## Demo story

> **Create once. Sell everywhere.**

1. Artisan speaks in an Indian language.
2. Bhashini processes the voice.
3. Craftsy AI understands the request.
4. Artisan creates a product.
5. Product is published to Craftsy Marketplace.
6. Artisan selects ONDC.
7. Craftsy validates ONDC requirements.
8. ONDC status is shown honestly.
9. Artisan sees Government Selling/GeM workflow.
10. Buyer discovers the product.
11. Order appears in unified orders.
12. Inventory updates.
13. Artisan receives a voice notification.

If real ONDC production access is unavailable, demonstrate only the validated staging/adapter flow and clearly state production onboarding status.

---

# FINAL ARCHITECTURE

```text
                         CRAFTSY
                            |
             +--------------+--------------+
             |                             |
       ARTISAN EXPERIENCE             BUYER EXPERIENCE
             |                             |
      +------+------+                 +----+----+
      |             |                 |         |
    Voice           UI           Marketplace  Search
      |             |                 |         |
      +------+------+                 +----+----+
             |                             |
          Bhashini                         |
             |                             |
             +-------------+---------------+
                           |
                       AI Agent
                           |
                   COMMERCE ENGINE
                           |
        +------------------+------------------+
        |                  |                  |
   Product Engine      Order Engine      Inventory
        |                  |                  |
        +------------------+------------------+
                           |
                   Commerce Gateway
                           |
        +------------------+------------------+
        |                  |                  |
     Craftsy             ONDC              GeM
   Marketplace          Adapter        Gov. Workflow
```

---

# CHANNEL STATUS MODEL

Use user-friendly states:

```text
Craftsy
 ✓ Published

ONDC
 ○ Not connected
 ◐ Setup required
 ◐ Validation pending
 ✓ Published
 ! Action required
 × Failed

Government
 ○ Not configured
 ◐ Eligibility/setup
 ◐ Catalogue preparation
 ✓ Workflow ready
 ! Action required
```

Never show **Live** unless the channel is actually live.

---

# WHAT MUST NOT BE DONE

- Do not rewrite completed Phases 0–8.
- Do not replace the existing accessibility system.
- Do not create a second Bhashini implementation.
- Do not duplicate product models unnecessarily.
- Do not expose ONDC signing keys to Flutter.
- Do not invent GeM APIs.
- Do not invent ONDC API responses.
- Do not create fake production integrations.
- Do not hard-code external IDs.
- Do not claim ONDC integration without real onboarding/testing.
- Do not claim GeM integration without a verified official mechanism.
- Do not let AI fabricate required commerce information.
- Do not turn Craftsy into a generic e-commerce template that loses the artisan-first identity.

---

# DEFINITION OF DONE

## Marketplace
- [ ] Customers discover products.
- [ ] Customers view products and artisans.
- [ ] Cart/checkout/order flow works.
- [ ] Artisan storefronts work.

## Commerce Engine
- [ ] One canonical product model.
- [ ] One inventory source of truth.
- [ ] One unified order model.
- [ ] Isolated channel adapters.

## ONDC
- [ ] Correct participant role documented.
- [ ] ONDC adapter exists.
- [ ] Authorization/signing is server-side.
- [ ] Staging tested where onboarding permits.
- [ ] Pre-production requirements documented.
- [ ] Production status documented honestly.
- [ ] No fake network transactions.

## Government / GeM
- [ ] Government-selling workflow exists.
- [ ] Seller/category requirements represented.
- [ ] Missing information detected.
- [ ] Official integration mechanism documented.
- [ ] No invented GeM API.

## AI + Bhashini
- [ ] Voice product creation works.
- [ ] Voice commerce commands work where supported.
- [ ] Bhashini remains centralized.
- [ ] AI validates before acting.
- [ ] AI never fabricates required data.

## Accessibility
- [ ] Marketplace follows existing accessibility system.
- [ ] Voice alternatives exist.
- [ ] Low-literacy wording maintained.
- [ ] Multilingual support remains consistent.

## QA
- [ ] Tests pass.
- [ ] Analyzer/linter has no new unexplained issues.
- [ ] Release build succeeds.
- [ ] Critical flows manually tested.
- [ ] Integration limitations documented.

---

# AGENT REPORT FORMAT

At the end of every phase, report:

```text
PHASE: X
STATUS: COMPLETE / BLOCKED / PARTIAL

Implemented:
- ...

Files changed:
- ...

Architecture decisions:
- ...

Tests:
- ...

Build:
- ...

Integration status:
- ...

Known limitations:
- ...

Master plan updated:
- YES / NO

Recommended next phase:
- ...
```

---

# MASTER PRINCIPLE

> **The artisan makes the craft. Craftsy handles the commerce.**

The artisan should not need to understand marketplaces, ONDC protocols, government procurement systems, catalogue schemas or inventory synchronization. Craftsy should hide that complexity behind one simple, multilingual, accessible commerce experience.
