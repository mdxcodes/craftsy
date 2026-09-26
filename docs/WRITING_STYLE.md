# Craftsy Writing Style Guide

## Purpose

Keep documentation and comments readable, specific, and honest. This guide prevents generic AI-generated prose from accumulating in the repository.

## Terminology

Use these exact terms:

- `ArtisanDB`, `ProductDB`, `OrderDB` — database models
- `OrderService`, `CommerceService`, `CatalogService` — service classes
- `ProductDB.stock` — inventory source of truth
- `ONDC BPP adapter` — the local Retail B2C hackathon integration
- `Bhashini ASR` — REST speech-to-text integration
- `ChromaDB` — vector store for pricing benchmarks
- `CraftMitra` — in-app chat assistant

Do not alternate between:
- artisan / seller / creator / vendor / merchant
- product / item / listing
- order / purchase

Pick one and stick with it.

## Documentation Style

- Start with what the file/component does.
- Explain why it exists.
- Note constraints or non-obvious behavior.
- Do not narrate obvious syntax.

Good:
```python
# Product IDs from ONDC requests are mapped back to Craftsy IDs
# before querying ProductDB.
```

Bad:
```python
# This function is responsible for creating an order.
# It takes the order details and creates an order in the database.
# Finally, it returns the created order.
```

## README / Markdown

- Prefer short sentences.
- Use concrete nouns and specific file/module names.
- Avoid: "seamless", "robust", "comprehensive", "cutting-edge", "leveraging", "harnessing", "empowering", "revolutionary", "innovative solution", "state-of-the-art", "end-to-end ecosystem", "holistic", "streamlined", "transformative", "next-generation".
- Do not add fake "future scope" lists. Only document work that is actually planned.

## Code Comments

- Keep comments for public services, complex algorithms, protocol behavior, security decisions, and compatibility workarounds.
- Remove comments that repeat the code.
- Do not use comments as a narrative of what the next line does.

## API Descriptions

Describe actual behavior.

Good:
```
Returns products matching the supplied category and search query.
```

Bad:
```
This endpoint provides a comprehensive mechanism for...
```

## Status Terminology

Use exactly one of:
- `Implemented` — works end-to-end in the current codebase
- `Partially implemented` — some paths work, others are stubbed
- `Scaffold` — structure exists but no real behavior
- `Mock` — fake behavior for demo/testing
- `Blocked` — known blocker prevents completion
- `Unknown` — not yet inspected

Do not invent statuses.

## ONDC Language

Always qualify ONDC work honestly:
- Use "ONDC Retail hackathon/mock integration" or "local Retail BPP harness".
- Never claim production ONDC integration unless actual participant onboarding has occurred.
- Document blockers explicitly rather than hiding them.

## Test Names

Describe behavior, not implementation order.

Good:
```python
def test_confirm_is_idempotent():
def test_select_rejects_quantity_above_stock():
```

Bad:
```python
def test1():
def test_order():
```

## UI Text

Use clear interface language:
- "Add product"
- "View orders"
- "Enhance image"
- "Try again"
- "No products found"
- "Order confirmed"

Avoid marketing copy like "Unlock your creative potential" or "Discover extraordinary craftsmanship".

## Limitations

Document real limitations directly. Specific limitations are more credible than vague hedges.

Good:
```
ONDC is currently a local Retail BPP harness. The official
ondc-mock-server could not be started because its retail spec
submodules did not initialize correctly.
```

Bad:
```
While Craftsy represents a highly comprehensive solution, some
advanced functionality remains subject to future enhancement.
```
