# CRAFTSY — POST-AUDIT MASTER IMPLEMENTATION PLAN

**Document status:** AUTHORITATIVE  
**Created:** 2026-09-24  
**Baseline audit:** `CRAFTSY — COMPLETE IMPLEMENTATION STATE AUDIT` generated 2026-09-24  
**Repository:** `/secondary/craftsy`  
**Baseline branch:** `feature/bhavya-selective-integration`  
**Baseline commit:** `23e455c`

---

# 0. PURPOSE OF THIS DOCUMENT

This document is the authoritative implementation roadmap for Craftsy **after the verified 2026-09-24 implementation audit**.

It exists to answer one question:

> **Given what Craftsy actually has today, what should we build next to solve the official problem statement strongly, honestly, and end-to-end?**

This is NOT a greenfield plan.

Do not rebuild functionality already verified as complete.

Do not treat previous plans as proof of implementation.

The repository and the latest verified audit remain the source of truth.

---

# 1. OFFICIAL PROBLEM TO SOLVE

The official problem statement describes marginalized micro-entrepreneurs, artisans, and weavers who receive temporary physical-market exposure through exhibitions, fairs, cluster programs, and trade events, but lack continuous year-round access to broader digital markets.

The stated barriers include:

- low digital literacy
- language barriers
- lack of technical e-commerce skills
- difficulty taking professional product photographs
- difficulty creating professional product descriptions/catalogues
- difficulty understanding market pricing
- difficulty connecting to larger B2B buyers or government e-marketplaces

The expected solution is an:

> **AI-powered, cross-platform mobile application acting as a "virtual business manager" for artisans.**

The explicitly required capabilities are:

1. AI Image Enhancer & Studio
2. Multilingual Auto-Cataloger
3. Dynamic Pricing Assistant

The impact goal is continuous digital commerce and reduced dependence on periodic physical exhibitions.

---

# 2. THE CORE PRODUCT DEFINITION

Craftsy must NOT be positioned primarily as:

> "another Amazon/Etsy for handicrafts."

Craftsy's core product is:

> **An AI-powered virtual business manager that transforms an artisan's physical craft into a professional, commerce-ready digital business and helps that business reach multiple sales channels.**

The consumer marketplace is a **sales channel and proof of the complete commerce loop**, not the entire product identity.

The product hierarchy is:

```text
                           CRAFTSY
                              |
                 VIRTUAL BUSINESS MANAGER
                              |
        +---------------------+---------------------+
        |                     |                     |
        v                     v                     v
   CREATE & MANAGE       SELL & DISTRIBUTE     BUSINESS HELP
        |                     |                     |
   AI Image Studio        Craftsy Market       CraftMitra
   Voice Catalogue        ONDC                  Business Advisor
   AI Description         Government/B2B
   Pricing
   Inventory
   Orders
```

The central promise is:

> **Create once. Sell across channels.**

---

# 3. CURRENT VERIFIED BASELINE — DO NOT REDO

The 2026-09-24 audit verified these as implemented:

## 3.1 Working

- Artisan registration + OTP authentication
- Artisan profile
- Product CRUD
- AI image enhancement
- Background removal using rembg/U²-Net
- Lighting correction
- E-commerce image formatting
- AI catalogue/product description generation
- Inventory tracking
- Artisan order management
- Order status updates
- Social media content generation
- CraftMitra chatbot
- Business Advisor
- Four-language localization
- Accessibility/Semantics/touch targets/text scaling
- Five Android Glance widgets with real data
- Debug APK build

## 3.2 Do not rebuild these

Do not replace or unnecessarily rewrite:

- AI image enhancement pipeline
- Artisan registration
- Product CRUD
- Android widget architecture
- Localization architecture
- Accessibility implementation
- CraftMitra
- Social media integration

Any future work must integrate with these existing systems.

---

# 4. CURRENT VERIFIED GAPS

The audit verified the following gaps:

## P0/P1 product gaps

- Bhashini live ASR is missing
- Bhashini live TTS is missing
- Bhashini translation is missing
- Dynamic pricing lacks live market data
- Consumer marketplace does not exist
- Consumer/customer model does not exist
- Cart does not exist
- Address model does not exist
- Checkout does not exist
- Payment does not exist
- Consumer order tracking does not exist
- Public artisan storefront does not exist
- Inventory is not decremented/reserved during order creation
- Order price is not server-authoritatively validated
- Logistics/delivery integration does not exist

## Channel gaps

- ONDC is scaffold only
- GeM is scaffold only
- No real ONDC API calls
- No real GeM API calls
- No ONDC credentials/signing
- No ONDC webhooks
- No GeM authentication/publishing integration

## Technical gaps

- Offline sync is partial
- Notifications are partially mocked
- Backend has documented test failures
- Camera currently opens gallery instead of native camera on device
- Root `ML/` duplicates `backend/ML/`
- Production deployment is not implemented

---

# 5. STRATEGIC PRINCIPLE

Do NOT build all channels equally.

The implementation should prove this complete value chain:

```text
ARTISAN
   |
   | speaks / photographs
   v
CRAFTSY AI BUSINESS MANAGER
   |
   +--> professional image
   +--> catalogue
   +--> price
   +--> inventory
   |
   v
COMMERCE-READY PRODUCT
   |
   +-------------------+-------------------+
   |                   |                   |
   v                   v                   v
CRAFTSY MARKET       ONDC             GOVERNMENT/B2B
   |
   v
CONSUMER
   |
   v
ORDER
   |
   v
ARTISAN
   |
   v
FULFILMENT
   |
   v
INCOME
```

This is the primary end-to-end demo and product architecture.

---

# 6. IMPLEMENTATION PRIORITY

The remaining work should be executed in this order:

```text
PHASE 0  Architecture + safety baseline
   ↓
PHASE 1  Fix commerce foundation
   ↓
PHASE 2  Consumer identity + marketplace
   ↓
PHASE 3  Consumer purchase + order lifecycle
   ↓
PHASE 4  Artisan receives and fulfils consumer orders
   ↓
PHASE 5  Live Bhashini voice pipeline
   ↓
PHASE 6  Dynamic pricing improvement
   ↓
PHASE 7  ONDC technical integration/readiness
   ↓
PHASE 8  Government/GeM guided selling
   ↓
PHASE 9  Notifications + offline reliability
   ↓
PHASE 10 End-to-end hardening + SIH demo
```

This order is deliberate.

Do NOT begin by building a large consumer marketplace disconnected from the existing commerce engine.

---

# 7. PHASE 0 — PRE-IMPLEMENTATION SAFETY CHECK

Before modifying code:

1. Verify current branch and commit.
2. Run existing tests.
3. Record analyzer state.
4. Confirm backend starts.
5. Confirm current routes.
6. Confirm current database schema.
7. Confirm existing artisan flows still work.
8. Create a clean checkpoint commit/branch before commerce work.

Do not fix unrelated legacy issues during this phase unless they block the upcoming implementation.

---

# 8. PHASE 1 — COMMERCE FOUNDATION

## Goal

Make the existing commerce/order system safe enough to support both artisans and consumers.

The current order implementation is artisan-oriented and has known weaknesses:

- no consumer model
- no inventory-aware order creation
- requested price is not authoritative
- no payment model
- no address model
- no shipment model

Before adding a marketplace, establish canonical commerce primitives.

## Required models

Add only what is needed:

```text
User
SellerProfile / ArtisanProfile
CustomerProfile (if architecture requires)
Product
Cart
CartItem
Address
Order
OrderItem
Payment
Shipment / Delivery
ProductChannel
ChannelAuditLog
```

Do not duplicate existing `ArtisanDB`, `ProductDB`, `OrderDB`, or channel models without first determining whether they can be evolved safely.

## User identity

The intended conceptual model is:

```text
User
 |
 +-- can shop
 |
 +-- can become artisan
       |
       +-- SellerProfile
```

A user should NOT need two accounts to shop and sell.

The artisan status should be represented by seller onboarding/profile state rather than a mutually exclusive consumer-vs-artisan account.

However, adapt this to the existing authentication architecture rather than blindly replacing it.

## Order authority

The server must determine:

- product existence
- active product state
- current price
- available stock
- quantity
- seller
- totals

The client must not be trusted to provide authoritative price or total.

Order creation should:

1. authenticate user
2. validate cart
3. validate products
4. validate current prices
5. validate stock
6. calculate totals server-side
7. create order/items
8. reserve or decrement inventory safely
9. associate seller
10. persist order
11. create initial status
12. trigger notification/event

Use a transaction.

---

# 9. PHASE 2 — CONSUMER IDENTITY + MARKETPLACE

## Goal

Introduce the second side of Craftsy:

> **Shopping Mode**

The existing artisan application remains intact.

A user can enter Craftsy and:

```text
SHOP CRAFTS
```

or:

```text
SELL MY CRAFTS
```

The two modes use the same underlying account.

## Entry concept

Preferred conceptual experience:

```text
CRAFTSY

India's digital home for handmade crafts.

[ SHOP CRAFTS ]

[ SELL MY CRAFTS ]
```

Do not force a permanent consumer/artisan choice during initial registration.

## Marketplace

Implement a real consumer marketplace backed by the existing database.

Required:

- marketplace home
- search
- categories
- product cards
- filters
- product detail
- public artisan/storefront page
- product availability
- artisan/craft information

Do not use hardcoded product cards for the actual marketplace.

Development seed data may be used for controlled testing, but production marketplace data must come from the backend.

---

# 10. PHASE 3 — CONSUMER PURCHASE LOOP

## Goal

Complete:

```text
Discover
→ Product
→ Cart
→ Address
→ Checkout
→ Payment state
→ Order
→ Confirmation
→ My Orders
→ Tracking
```

## Cart

Implement:

- add item
- remove item
- change quantity
- stock validation
- price refresh
- seller association
- cart persistence

## Address

Implement:

- add address
- edit address
- delete/select address
- validation

Keep the UX simple.

## Checkout

Show:

- products
- quantities
- subtotal
- delivery charge if applicable
- total
- delivery address
- payment method/state

Totals must come from the server-authoritative commerce calculation.

## Payment

The audit confirms there is currently NO payment provider.

Therefore:

- do not pretend payment exists
- create a payment abstraction
- support a clearly labelled development/mock payment state if required for the SIH demo
- integrate a real payment provider only if credentials and a suitable integration are actually available

Never display a fake "payment successful" as though money was actually transferred.

---

# 11. PHASE 4 — ARTISAN ORDER LOOP

This phase connects the consumer marketplace back to the core PS.

After a consumer places a valid order:

```text
Consumer
   ↓
Order created
   ↓
Seller receives order
   ↓
Artisan sees:
"New order received"
   ↓
Accept
   ↓
Preparing
   ↓
Ready/Shipped
   ↓
Delivered
```

The existing artisan order screen should be extended rather than duplicated.

The artisan should not need to understand consumer technical details.

For a low-literacy UX, use:

- clear icons
- simple status labels
- voice/read-aloud affordances
- large actions
- minimal text
- local language support

---

# 12. PHASE 5 — BHASHINI LIVE VOICE

## Goal

Turn the current Bhashini abstraction from scaffold into a working provider.

Current architecture already contains:

```text
CraftsyLanguageService
        ↓
BhashiniLanguageProvider
        ↓
FallbackLanguageProvider
```

Preserve this architecture.

Do not scatter Bhashini API calls through UI widgets.

## Required flow

```text
Artisan speaks
      ↓
Bhashini ASR
      ↓
recognized text
      ↓
catalogue generation
      ↓
English/Hindi/regional output
      ↓
Bhashini TTS
```

## Required validation

Test:

- microphone permission
- supported languages
- ASR success
- ASR failure
- network failure
- translation
- TTS
- retry
- fallback behavior

Do not claim Bhashini is live until real API calls have been tested with valid credentials.

---

# 13. PHASE 6 — DYNAMIC PRICING

Current pricing is NOT a fully dynamic market-pricing system.

It already has:

- image input
- description input
- material-cost extraction
- embeddings
- ChromaDB similarity
- benchmark data

The next step is to improve it honestly.

## Pricing architecture

```text
Product
 +
Material cost
 +
Labour estimate
 +
Product category
 +
Comparable products
 +
Verified market observations
        ↓
Pricing Engine
        ↓
Suggested range
        +
Explanation
```

Do not scrape websites simply because they are available.

Market-data sources must be:

- legally usable
- stable enough for the demo
- attributable
- structured enough for reproducible results

If live market data cannot be reliably obtained, present the feature honestly as:

> AI-assisted competitive pricing based on available benchmark/comparable data.

Do not call benchmark-only pricing "live dynamic pricing."

---

# 14. PHASE 7 — ONDC

## Goal

Make ONDC technically credible without faking integration.

Current status:

> Scaffold only.

The UI, state machine, validation, and audit logging can be retained.

Next work:

1. determine the correct seller-side participant architecture
2. determine onboarding requirements
3. obtain authorized credentials
4. implement required authentication/signing
5. configure staging/pre-production
6. implement catalogue publishing
7. implement callbacks/webhooks
8. implement order synchronization
9. implement error/retry handling
10. verify with an actual ONDC environment

## Important architecture rule

ONDC is a network/channel.

Do not build:

```text
Craftsy
  └── ONDC Marketplace
```

Build:

```text
Craftsy Master Catalogue
        ↓
ONDC Adapter
        ↓
ONDC network
```

Craftsy remains the artisan's business manager.

---

# 15. PHASE 8 — GOVERNMENT / GeM

## Goal

Provide an honest government-selling pathway.

Current status:

> Scaffold only.

Do not create a fake GeM marketplace inside Craftsy.

Instead:

```text
SELL TO GOVERNMENT
        ↓
Seller readiness
        ↓
Documents
        ↓
Business information
        ↓
Product/category requirements
        ↓
Catalogue preparation
        ↓
Official GeM pathway
```

If an authorized technical integration becomes available, add it behind an adapter.

Otherwise the product should clearly show:

- readiness
- missing requirements
- catalogue preparation
- next official step

Do not claim automatic GeM registration or publishing unless technically verified.

---

# 16. PHASE 9 — NOTIFICATIONS + OFFLINE RELIABILITY

After the commerce loop works:

## Notifications

Replace current mock notification behavior with real persisted events.

Important events:

- new order
- order accepted
- order status changed
- low stock
- payment state changed
- delivery state changed
- seller/channel status

Use push notifications only when a real provider is configured.

## Offline

Complete the existing Drift/offline architecture where useful.

Prioritize:

- viewing existing products
- drafting product information
- viewing cached inventory
- viewing cached orders
- queued sync

Do not make complex offline checkout unless the business rules can safely support it.

---

# 17. PHASE 10 — FINAL SIH HARDENING

The final product should demonstrate one coherent story.

## Primary demo

```text
1. Artisan logs in
2. Artisan taps "Add My Craft"
3. Takes product photo
4. Craftsy improves the image
5. Artisan speaks in a regional language
6. Craftsy converts speech into product information
7. Craftsy generates professional catalogue content
8. Craftsy suggests a price
9. Artisan confirms product
10. Product becomes available on Craftsy Marketplace
11. Consumer enters Shopping Mode
12. Consumer discovers product
13. Consumer opens artisan/product page
14. Consumer adds to cart
15. Consumer checks out
16. Order is created
17. Artisan receives the order
18. Artisan accepts it
19. Artisan prepares/ships it
20. Consumer tracks order
21. Product/order data remains available to the artisan
22. Same product can be prepared for ONDC/Government selling
```

This is the strongest demonstration because it proves the complete bridge:

> **traditional craft → digital business → market → sale → artisan**

---

# 18. UI/UX PRINCIPLES

Do not let the consumer marketplace turn Craftsy into a generic e-commerce clone.

## Artisan mode

Prioritize:

- voice
- icons
- large actions
- short instructions
- local language
- visual status
- guided workflows
- minimal typing

Examples:

```text
📷 Add Craft
🎙️ Tell Craftsy
💰 Check Price
📦 My Orders
🌐 Sell Everywhere
```

## Consumer mode

It can behave like a normal modern marketplace:

- search
- discovery
- categories
- product images
- artisan stories
- cart
- checkout
- order tracking

But maintain Craftsy's handmade/artisan identity.

---

# 19. ROLE MODEL

The conceptual identity model is:

```text
User
 |
 +--------------------+
 |                    |
Shop               Sell
 |                    |
Consumer         SellerProfile
                      |
                  Artisan Shop
```

A person can be both.

Do NOT create separate consumer and artisan accounts unless technical constraints make it unavoidable.

The important distinction is:

```text
Everyone can shop.

A user becomes a seller after seller onboarding.
```

---

# 20. WHAT NOT TO BUILD

Do not spend major implementation time on:

- coupons
- loyalty points
- complex advertising
- flash sales
- consumer social feeds
- advanced recommendations
- unnecessary AI features
- decorative dashboards
- fake ONDC transactions
- fake GeM transactions
- fake payment success
- fake delivery tracking
- hardcoded marketplace listings presented as real
- duplicate AI/image/catalogue systems

The product must optimize for the official problem statement.

---

# 21. DATA AUTHORITY RULES

## Product

Backend/database is authoritative.

## Price

Server/database + pricing engine are authoritative.

## Stock

Server/database is authoritative.

## Order total

Server-calculated.

## Order status

Server-controlled.

## Payment

Payment provider/backend state is authoritative.

## Delivery

Delivery integration/backend state is authoritative.

## ONDC

ONDC adapter/network state is authoritative when actually connected.

## GeM

Official/authorized GeM state is authoritative when actually connected.

Never let UI state imply a successful external transaction.

---

# 22. TESTING STRATEGY

Every phase must preserve previously passing tests.

Required levels:

## Unit

- pricing
- order calculations
- inventory
- catalogue transformation
- role logic
- channel state

## Widget/UI

- marketplace
- cart
- checkout
- artisan order flow
- seller onboarding

## Integration

At minimum:

```text
register/login
→ create product
→ publish
→ discover
→ cart
→ checkout
→ order
→ artisan order inbox
→ status update
```

## External integration

Only mark ONDC/GeM/Bhashini tests as integration-complete when they actually call the configured service/environment.

---

# 23. DEFINITION OF DONE

Craftsy's post-audit implementation is considered successful when:

## Artisan

- can register
- can create a product
- can photograph it
- can improve the image
- can describe it through voice
- can generate catalogue content
- can receive pricing assistance
- can publish the product
- can manage stock
- can receive orders
- can process orders

## Consumer

- can enter without being an artisan
- can browse products
- can search
- can filter
- can view artisan/product details
- can cart products
- can provide address
- can checkout
- can receive an order confirmation
- can view orders
- can track order state

## Commerce

- inventory is authoritative
- prices are authoritative
- orders are persistent
- sellers are associated correctly
- order lifecycle is consistent

## AI

- image enhancement works
- catalogue generation works
- voice pipeline works with configured Bhashini
- pricing assistance works honestly according to available data

## Channels

- Craftsy marketplace works as an actual consumer channel
- ONDC status is accurately represented
- GeM status is accurately represented
- no external integration is falsely claimed

---

# 24. SIH DEMO PRIORITY

If time becomes limited, prioritize this exact chain:

```text
P0
AI Image Studio
+
AI Catalogue
+
Voice
+
Pricing
        ↓
P0
Craftsy Marketplace
        ↓
P0
Consumer → Cart → Order
        ↓
P0
Artisan receives order
        ↓
P1
Order fulfilment/tracking
        ↓
P1
ONDC
        ↓
P1
Government/GeM
```

Do not sacrifice the core end-to-end story to build superficial integrations with every channel.

---

# 25. FINAL PRODUCT STORY

The final narrative should be:

> An artisan should not have to become an e-commerce expert to participate in the digital economy.

Craftsy handles the difficult parts:

```text
Photo
   ↓
AI enhancement

Voice
   ↓
Catalogue

Costs + market information
   ↓
Pricing assistance

Catalogue
   ↓
Commerce channels

Consumer order
   ↓
Artisan fulfilment

Sales
   ↓
Continuous digital income opportunity
```

The marketplace proves that the digitized product can actually reach consumers.

ONDC and Government/GeM extend the same commerce-ready product into additional channels.

Therefore:

> **Craftsy is not primarily a marketplace. Craftsy is the business layer that makes an artisan commerce-ready.**

---

# 26. IMPLEMENTATION RULE FOR FUTURE AI CODING AGENTS

Every future coding-agent task MUST begin from this document and the latest verified implementation audit.

The agent must:

1. inspect existing implementation before changing it
2. identify reusable components
3. avoid duplicate models/services/routes
4. avoid rebuilding completed features
5. preserve canonical architecture
6. preserve accessibility
7. preserve localization
8. preserve the existing Indigo Loom theme
9. avoid fake integrations
10. avoid hardcoded production data
11. run relevant tests after implementation
12. report exactly what changed
13. report what remains incomplete
14. never claim an external integration is live without verification

If the repository differs from this document, the repository must be audited before proceeding.

A newer verified audit supersedes this document where the two conflict.

---

# 27. IMMEDIATE NEXT TASK

Do NOT implement all phases at once.

The next coding task should be:

> **Phase 1 — Commerce Foundation Audit & Design**

Before writing the consumer marketplace UI, inspect the existing `ArtisanDB`, `ProductDB`, `OrderDB`, authentication flow, commerce models, routers, services, and database migrations/schema.

Produce a concrete implementation plan for:

- unified user identity
- artisan/seller profile
- customer/consumer identity
- cart
- address
- order
- order item
- payment abstraction
- shipment/delivery abstraction
- inventory reservation/decrement
- server-authoritative price
- order status lifecycle

Only after this design is verified should marketplace screens be implemented.

---

# 28. CANONICAL STATUS

At the beginning of this document:

```text
Craftsy = Artisan Business Manager
Marketplace = NOT IMPLEMENTED
ONDC = SCAFFOLD
GeM = SCAFFOLD
Bhashini = SCAFFOLD
Pricing = PARTIAL
AI Image = COMPLETE
AI Catalogue = COMPLETE
Artisan Orders = COMPLETE/PARTIAL COMMERCE FOUNDATION
Consumer Commerce = NOT IMPLEMENTED
```

The target is:

```text
Craftsy
  ↓
Virtual Business Manager
  ↓
Commerce-ready artisan
  ↓
Craftsy Marketplace + ONDC + Government/B2B
  ↓
Real commerce loop
```

---

# END OF CRAFTSY POST-AUDIT MASTER IMPLEMENTATION PLAN
