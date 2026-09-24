# Craftsy Android Widgets — Powerful Implementation Specification

**Version:** 1.0  
**Status:** Implementation Source of Truth  
**Scope:** Native Android home-screen widgets for the Craftsy Flutter application

---

## 1. Purpose

Craftsy widgets are a functional extension of the Craftsy artisan marketplace.

They must reduce the number of times an artisan needs to open the full app for routine information or direct navigation.

### Core principle

> Every widget must either show something the artisan genuinely needs to know or let them reach a useful action faster.

No decorative widget concepts are permitted.

The initial implementation contains exactly five widget concepts:

1. Craftsy Today
2. Orders
3. Stock Alerts
4. CraftMitra
5. Selling Channels

---

## 2. Non-Negotiable Product Principles

The implementation MUST satisfy all of the following.

### Real data only

Production widgets must use actual Craftsy state.

Never fabricate:

- orders
- products
- stock
- revenue
- sales
- channel connectivity
- ONDC publication
- GeM approval
- GeM orders
- AI responses
- Bhashini responses

Test/demo fixtures are allowed only in isolated test/demo environments.

### No fake external integration

Widgets do not directly implement:

- ONDC protocol
- GeM protocol
- Bhashini APIs

They only display state produced by Craftsy's existing integration layers.

### No second application

Widgets are an extension of Craftsy, not a separate mini-app.

### No second source of truth

Flutter/backend remains authoritative.

Widgets consume a compact, safe snapshot.

### No battery abuse

Never use continuous polling, permanent services, or second-level refresh loops merely to keep widgets current.

### No unnecessary complexity

Use the smallest architecture that is robust, testable, secure, and maintainable.

---

## 3. Technology Architecture

Craftsy is a Flutter application.

The Android widget layer MUST be native Android.

### Preferred stack

- Kotlin
- Jetpack Glance
- Android App Widget infrastructure
- Android DataStore/SharedPreferences only if appropriate after inspecting the existing project
- WorkManager only where justified
- existing Craftsy deep-link/navigation architecture

Do not render Flutter widgets directly inside Android home-screen widgets.

### High-level architecture

```text
                    CRAFTSY FLUTTER APP
                           |
             +-------------+-------------+
             |                           |
        Existing domain             Existing actions
             |                           |
             +-------------+-------------+
                           |
                    Widget Data Layer
                           |
                 Safe Widget Snapshot
                           |
                 Native Android Bridge
                           |
                    Jetpack Glance
                           |
          +----------------+----------------+
          |                |                |
      Today             Orders           Stock
          |                |                |
     CraftMitra       Channels        Future-safe
```

The exact bridge MUST be determined by inspecting the current Craftsy codebase.

Do not invent a new data architecture when an existing one can be reused.

---

## 4. Source-of-Truth Hierarchy

The implementation must respect:

```text
Backend / authoritative Craftsy state
             ↓
       Flutter domain layer
             ↓
       Widget snapshot
             ↓
      Android widget UI
```

Never reverse this hierarchy.

A widget must not independently decide:

- whether an order is paid
- whether an ONDC listing is live
- whether a GeM product is approved
- whether inventory is available
- whether an artisan is authenticated

Those states come from Craftsy's authoritative application logic.

---

## 5. Widget Snapshot Architecture

Create a minimal native-readable widget state.

Conceptual model:

```text
CraftsyWidgetSnapshot
├── schemaVersion
├── authenticated
├── lastUpdated
├── dataFreshness
├── today
│   ├── attentionCount
│   ├── orderAttentionCount
│   ├── stockAttentionCount
│   └── channelAttentionCount
├── orders
│   ├── actionableCount
│   └── items[]
├── stock
│   ├── outOfStockCount
│   ├── lowStockCount
│   └── items[]
├── channels
│   ├── craftsy
│   ├── ondc
│   └── government
└── widgetCapabilityFlags
```

This is conceptual.

The coding agent MUST inspect existing domain models before defining the final model.

Do not copy complete Product, Order, Customer, Seller, ONDC payload, GeM document, or Bhashini response objects into widget state.

---

## 6. Privacy and Security

Widgets can be visible on a device even when the user is not actively inside Craftsy.

Never store in widget state:

- passwords
- access tokens
- refresh tokens
- API keys
- ONDC signing keys
- GeM credentials
- Bhashini keys
- private document contents
- unnecessary customer PII

Use the minimum customer information needed.

Prefer:

```text
Order #1042
Ship today
```

over full customer identity/address information.

---

## 7. Authentication Lifecycle

### Logged in

Display authorized Craftsy data.

### Logged out

Clear or invalidate private widget data and show:

```text
Open Craftsy
to sign in
```

Tap → Craftsy authentication flow.

### Account switching

If multiple accounts are supported:

1. invalidate old snapshot
2. clear old private data
3. generate new snapshot
4. refresh widgets

Never show account A's information after switching to account B.

---

# 8. Widget 1 — Craftsy Today

## Purpose

Answer:

> What needs my attention right now?

This is the primary widget.

Priority:

1. Orders requiring action
2. Stock requiring action
3. Selling-channel actions
4. Other actionable Craftsy alerts

Example:

```text
CRAFTSY

3 orders need attention

Order #1042
Ship today

Order #1045
Confirm order

2 products low on stock

1 selling channel needs attention

[ Open Craftsy ]
```

Values are illustrative only.

### Empty state

```text
CRAFTSY

You're all caught up.

Nothing needs your attention.
```

### Actions

- Order → exact order
- Stock alert → exact product/inventory
- Channel alert → exact channel readiness/action screen
- Main CTA → appropriate Craftsy screen

Do not send every action to the generic home screen.

---

# 9. Widget 2 — Orders

## Purpose

Show orders requiring action.

This is NOT an order-history widget.

Priority:

1. New/action-required orders
2. Confirmation required
3. Fulfilment/shipping required
4. Delivery problem
5. Other actionable states

Example:

```text
CRAFTSY ORDERS

3 need attention

#1042
Ship today

#1045
Confirm order

#1048
Delivery issue

[ View Orders ]
```

### Empty state

```text
You're all caught up.

No orders need your attention.
```

### Interaction

Every order item must navigate to the exact order.

If exact navigation is impossible, fix the navigation architecture rather than silently opening an unrelated page.

---

# 10. Widget 3 — Stock Alerts

## Purpose

Show inventory exceptions.

Priority:

1. Out of stock
2. Low stock

Example:

```text
STOCK ALERTS

2 out of stock
3 running low

Blue Pottery Vase
2 left

Wooden Lamp
1 left

[ Manage Stock ]
```

Show approximately 3–5 actionable products.

If more exist, show a concise count such as `+ 7 more` and provide `View all`.

### Interaction

- Product → exact product/inventory screen
- Manage Stock → Craftsy inventory

The widget should NOT directly modify stock in v1.

---

# 11. Widget 4 — CraftMitra

## Purpose

Provide immediate access to CraftMitra.

This is a compact launcher, not a full chatbot.

Example:

```text
CRAFTMITRA

How can I help?

[ Speak ]

[ Type ]
```

### Primary action

Speak → real CraftMitra voice flow.

Type → real CraftMitra text flow.

If the existing app supports a route such as:

```text
/craftmitra?mode=voice
```

use the actual verified route.

### Microphone behavior

The widget MUST NOT request microphone permission.

Craftsy handles:

- permission
- ASR
- Bhashini
- AI
- confirmation
- TTS
- errors

---

# 12. Widget 5 — Selling Channels

## Purpose

Show whether selling channels require attention.

Channels:

- Craftsy
- ONDC
- Government

Example:

```text
SELLING CHANNELS

Craftsy
Active

ONDC
Ready

Government
2 actions needed

[ Sell & Grow ]
```

### State honesty

If ONDC is not configured:

```text
ONDC
Not configured
```

If Government is an assisted workflow:

```text
Government
Preparation needed
```

Never claim connected/active/approved without actual supporting state.

---

# 13. Channel State Mapping

Create one user-facing state mapping.

Potential states:

- Active
- Ready
- Needs attention
- Not configured
- Updating
- Temporarily unavailable
- Error
- Preparation needed

The exact mapping MUST come from existing Craftsy commerce states.

Do not create contradictory state definitions between Flutter, Commerce Hub, and widgets.

---

# 14. Widget Sizes

Support useful launcher sizes.

Minimum target:

- small
- medium

where appropriate.

### Small

Show one key piece of information/action.

### Medium

Show multiple useful items.

Use responsive Glance layouts rather than duplicating complete implementations.

---

# 15. Android Widget Constraints

Jetpack Glance provides a Compose-style API for App Widgets, but it does not make an App Widget an unrestricted Android/Flutter screen.

Respect App Widget limitations.

Do not assume:

- arbitrary Flutter rendering
- unrestricted background execution
- continuous animation
- continuous networking
- microphone access
- arbitrary services

Use supported Glance/App Widget capabilities.

---

# 16. Deep-Link Architecture

Widgets must open exact Craftsy destinations.

Conceptual destinations:

```text
/orders
/orders/{orderId}
/products/{productId}
/inventory
/commerce
/commerce/ondc
/commerce/government
/craftmitra
/craftmitra?mode=voice
```

These are conceptual examples.

The implementation MUST inspect the actual Craftsy router and use its real routes.

Do not create duplicate navigation infrastructure.

---

# 17. Widget Update Architecture

Avoid continuous polling.

Use a layered strategy:

### Immediate updates

When meaningful state changes occur:

- order created
- order status changed
- stock changed
- product changed
- channel state changed
- login/logout
- account switch

trigger an appropriate widget refresh.

### Scheduled refresh

Use reasonable Android-supported refresh mechanisms for stale-data recovery.

### Background work

Use WorkManager only where justified.

### Manual refresh

Opening Craftsy or a widget action may trigger refresh.

Do not create a permanent background service solely for widgets.

---

# 18. Freshness

Every snapshot should have a timestamp.

If old:

```text
Updated 2h ago
```

If fresh data cannot be obtained:

- preserve safe last-known state where appropriate
- do not claim it is current
- do not fabricate replacement data

---

# 19. Offline Behavior

If cached data exists:

- display it safely
- mark stale where appropriate

If no cached data exists:

```text
Open Craftsy to update
```

Do not fabricate offline data.

---

# 20. Accessibility

Every meaningful item needs an accessible description.

Do not rely only on color or icons.

Test with TalkBack.

Check:

- content descriptions
- readable text
- action labels
- contrast
- touch targets
- logical reading order

---

# 21. Light and Dark Mode

Widgets must work in:

- light mode
- dark mode

Use Craftsy's design system while respecting Android launcher/system appearance.

Avoid hardcoded colors that become unreadable.

Dynamic color may be used where compatible.

---

# 22. Widget Picker and Metadata

Each widget must have proper Android metadata:

- receiver
- widget metadata XML
- description
- minimum size
- resize behavior
- category
- update configuration
- preview support where appropriate

Widget picker previews must not be blank/broken.

---

# 23. Provider Architecture

Prefer one provider per widget concept unless safe sharing clearly improves maintainability.

Possible structure:

```text
widgets/
├── CraftsyTodayWidget.kt
├── OrdersWidget.kt
├── StockAlertsWidget.kt
├── CraftMitraWidget.kt
├── SellingChannelsWidget.kt
├── WidgetDataStore.kt
├── WidgetSnapshot.kt
├── WidgetUpdateManager.kt
└── WidgetDeepLinks.kt
```

This is a recommendation. Inspect existing package conventions first.

---

# 24. WidgetDataStore

Create/refine a dedicated abstraction for widget-safe state.

Responsibilities:

- read snapshot
- write snapshot
- clear snapshot
- detect stale state
- handle account changes

It must NOT:

- call ONDC directly
- call GeM directly
- call Bhashini directly
- contain authentication secrets
- become the main Craftsy database

---

# 25. WidgetUpdateManager

Centralize widget refresh behavior.

Responsibilities:

- refresh all widgets
- refresh a specific widget where appropriate
- respond to meaningful state changes
- avoid redundant updates

If Flutter already has an application event/state mechanism, integrate with it.

Do not scatter update logic across dozens of screens.

---

# 26. Idempotent Updates

Repeated refresh requests must be safe.

If multiple events occur quickly, avoid unnecessary duplicate expensive updates.

Use lightweight coalescing/debouncing only where useful.

Do not delay urgent information unnecessarily.

---

# 27. Network Policy

Widget rendering should not depend on a long-running network request.

Preferred:

```text
Network/API
    ↓
Craftsy data layer
    ↓
Widget snapshot
    ↓
Glance rendering
```

Not:

```text
Widget render
    ↓
network request
    ↓
wait
    ↓
render
```

---

# 28. Image Policy

Avoid downloading large product images merely for widget rendering.

If an image is genuinely useful:

- use a small cached representation
- handle missing images
- keep text/status useful without the image

---

# 29. No Background Service Abuse

Forbidden:

- infinite loops
- second-level polling
- permanent foreground services solely for widgets
- unnecessary wake locks
- constant network requests

Battery use is a product requirement.

---

# 30. CraftMitra Boundaries

The CraftMitra widget is a launcher.

It does NOT implement:

- ASR
- NMT
- TTS
- LLM calls
- Bhashini API
- microphone recording

Those remain in the existing CraftMitra/language architecture.

---

# 31. ONDC Boundaries

The ONDC widget only reads existing Craftsy commerce state.

It must NOT:

- store ONDC credentials
- sign requests
- call ONDC protocol APIs
- publish catalogues
- fabricate connection status
- fabricate orders

---

# 32. Government/GeM Boundaries

The Government widget only reads existing Craftsy government-selling state.

It must NOT:

- store GeM credentials
- claim government approval
- fabricate government orders
- bypass official workflows
- invent API capabilities

---

# 33. Widget Actions

Every interactive element must have one clear purpose.

### Craftsy Today

- order → exact order
- stock → exact product/inventory
- channel → relevant channel
- CTA → appropriate Craftsy screen

### Orders

- order → exact order
- view all → orders

### Stock

- product → exact product/inventory
- manage → inventory

### CraftMitra

- speak → voice mode
- type → text mode

### Selling Channels

- channel → relevant channel
- Sell & Grow → Commerce Hub

---

# 34. Widget Interaction Safety

Widgets should navigate to the app for actions that could modify important data.

Do not initially implement direct destructive actions from widgets.

Examples:

- cancel order
- delete product
- change price
- change stock
- publish external listing
- submit government workflow

The widget provides the shortcut; Craftsy performs the protected action.

---

# 35. No-Data vs Error

These are different.

### No data

```text
No orders need attention.
```

### Error

```text
Craftsy couldn't update.
Open Craftsy
```

Do not confuse backend failure with zero data.

---

# 36. Testing Matrix

Test every widget under:

### Authentication

- logged in
- logged out
- account switch where supported

### Data

- normal data
- zero data
- many items
- missing fields
- stale data

### Network

- online
- offline
- backend unavailable

### UI

- small
- medium
- resized
- light
- dark

### Accessibility

- TalkBack
- content descriptions
- readable labels

### Navigation

- exact order
- exact product
- inventory
- ONDC
- Government
- Commerce Hub
- CraftMitra

### Lifecycle

- install
- add widget
- remove widget
- reboot
- force stop
- app update

---

# 37. Testing Requirements

The implementation is not complete until:

- Flutter tests pass
- Android unit tests pass where present
- debug APK builds
- widget providers register correctly
- widgets appear in picker
- deep links work
- logged-out state is safe
- no production fake data exists

Never delete tests to make builds pass.

Never hide build failures.

---

# 38. Android Toolchain Safety

Craftsy has previously experienced Android/Gradle compatibility issues.

Before adding dependencies, inspect:

- Flutter version
- AGP
- Gradle
- Kotlin
- compileSdk
- minSdk
- Java

Choose a Jetpack Glance version compatible with the existing toolchain.

Do NOT blindly upgrade:

- Flutter
- AGP
- Gradle
- Kotlin
- Java
- compileSdk

If an upgrade is genuinely necessary:

1. explain why
2. make the smallest compatible change
3. run full verification
4. document it

---

# 39. Dependency Policy

Add only necessary dependencies.

Before adding one:

- verify need
- verify compatibility
- verify maintenance status
- check for an existing equivalent

Do not add multiple widget frameworks.

Do not add a second state-management framework.

---

# 40. Performance

Avoid:

- large database queries
- large JSON payloads
- expensive image processing
- network requests during rendering
- unnecessary recompositions
- repeated initialization

Keep snapshots compact.

---

# 41. Localization

Widget text must use Craftsy's localization architecture where practical.

Do not create a separate translation system.

The architecture must support the selected Craftsy language.

---

# 42. Voice/Language Relationship

The widget does not implement language services.

Flow:

```text
Widget
 ↓
CraftMitra
 ↓
Language Service
 ↓
Bhashini/fallback
 ↓
AI
 ↓
Action
 ↓
Localized result
 ↓
TTS
```

---

# 43. Demo/Test Mode

If an existing demo mode exists, widgets may use demo data only while explicitly enabled.

Production builds must not silently use demo data.

If demo mode is added:

- isolate it
- clearly name it
- prevent accidental production activation

---

# 44. SIH Demonstration Value

A useful demonstration:

1. Artisan receives an order.
2. Orders widget changes.
3. Artisan sees the attention state.
4. Taps the order.
5. Craftsy opens the exact order.
6. Artisan later sees low stock.
7. Taps the product.
8. Craftsy opens inventory.
9. Artisan taps CraftMitra.
10. Voice assistant opens.

This demonstrates that Craftsy remains useful between app sessions.

---

# 45. Future-Proofing

The architecture should allow future widgets such as:

- fulfilment tasks
- workshop schedule
- earnings summary
- customer messages
- product approval alerts

Do NOT implement them now.

Adding a future widget should not require rewriting the widget data layer.

---

# 46. Definition of Done

The phase is COMPLETE only when:

- [ ] Five widget concepts implemented
- [ ] All five registered correctly
- [ ] All five appear in Android widget picker
- [ ] Small/medium layouts work where applicable
- [ ] Real Craftsy data used
- [ ] No production fake data
- [ ] Empty states work
- [ ] Error states work
- [ ] Stale state works
- [ ] Offline behavior works
- [ ] Authentication behavior works
- [ ] Account switching is safe where applicable
- [ ] Deep links work
- [ ] Exact order navigation works
- [ ] Exact product navigation works
- [ ] Inventory navigation works
- [ ] Commerce navigation works
- [ ] CraftMitra voice launch works
- [ ] Light mode works
- [ ] Dark mode works
- [ ] Accessibility checked
- [ ] TalkBack checked
- [ ] No unnecessary background service
- [ ] No aggressive polling
- [ ] No secrets in widget layer
- [ ] No direct ONDC calls
- [ ] No direct GeM calls
- [ ] No direct Bhashini calls
- [ ] Flutter tests pass
- [ ] Android tests pass
- [ ] Android build passes
- [ ] Master plan updated

---

# 47. Master Plan Update

Update:

`CRAFTSY_V2_MASTER_PLAN.md`

Add a dedicated:

## Android Widgets

section containing:

- product rationale
- five widget descriptions
- architecture
- data flow
- security
- update strategy
- deep links
- authentication
- offline behavior
- accessibility
- localization
- dependencies
- testing
- limitations
- future opportunities

Use accurate labels:

- IMPLEMENTED
- PARTIAL
- BLOCKED
- EXTERNAL DEPENDENCY
- PLANNED

---

# 48. Required Agent Report

Return:

## Android Widget Status

COMPLETE / PARTIAL / BLOCKED

## Widget 1 — Craftsy Today

- implementation
- sizes
- data source
- interactions
- test status

## Widget 2 — Orders

- implementation
- sizes
- data source
- interactions
- test status

## Widget 3 — Stock Alerts

- implementation
- sizes
- data source
- interactions
- test status

## Widget 4 — CraftMitra

- implementation
- sizes
- deep link
- voice behavior
- test status

## Widget 5 — Selling Channels

- implementation
- sizes
- channel states
- interactions
- test status

## Architecture

Explain:

Flutter → widget data → native Android → Glance

## Security

Explain:

- credential handling
- authentication
- account switching
- private data handling

## Updates

Explain:

- event-triggered updates
- scheduled updates
- stale state
- offline state

## Deep Links

List actual implemented routes.

## Android Toolchain

List:

- Flutter
- AGP
- Gradle
- Kotlin
- Java
- compileSdk
- minSdk
- Glance version

## Tests

Exact commands and exact results.

## Build

Exact command and result.

## Master Plan

Sections updated.

## Known Limitations

Be explicit.

## Next Phase

Provide exactly ONE next phase.

---

# 49. Authoritative Android References

When implementation behavior is uncertain, consult current official Android documentation rather than guessing.

Jetpack Glance:

https://developer.android.com/develop/ui/compose/glance

Create an App Widget with Glance:

https://developer.android.com/develop/ui/compose/glance/create-app-widget

Glance user interaction:

https://developer.android.com/develop/ui/compose/glance/user-interaction

Glance widget updates:

https://developer.android.com/develop/ui/compose/glance/glance-app-widget

Android App Widgets:

https://developer.android.com/develop/ui/views/appwidgets

Android widget advanced/update guidance:

https://developer.android.com/develop/ui/views/appwidgets/advanced

Glance configuration:

https://developer.android.com/develop/ui/compose/glance/configuration

Glance generated previews:

https://developer.android.com/develop/ui/compose/glance/generated-previews

The coding agent must prefer current official Android documentation over memory or assumptions when dealing with Android widget APIs.

---

# 50. Final Product Rule

Craftsy widgets exist to answer:

> **What matters to me right now?**

They are not miniature versions of the Craftsy app.

They are not decorative cards.

They are not marketing.

They are not AI gimmicks.

They are not fake analytics.

They are a practical bridge:

```text
Android Home Screen
        ↓
Craftsy information/action
        ↓
Exact useful workflow
```

Every element must earn its place.

**No BS. Real data. Real actions. Honest states. Low friction.**
