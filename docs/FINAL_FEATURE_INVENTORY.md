# Craftsy — Final Feature Inventory

## Feature: Artisan Authentication

Frontend entry: `lib/features/auth/screens/`
Flutter route: `/otp`, `/signIn`
API endpoint: `POST /api/v1/auth/login`, `POST /api/v1/auth/verify-otp`, `POST /api/v1/auth/resend-otp`
Backend service: `backend/routers/auth.py`, `backend/middleware/auth.py`
Database tables: `ArtisanDB`
External service: StartMessaging OTP
Configuration required: `STARTMESSAGING_API_KEY`, `STARTMESSAGING_TEMPLATE_ID`, `AUTH_SECRET_KEY`
Current state: IMPLEMENTED
Test coverage: `tests/test_auth_middleware.py`, `tests/test_startmessaging.py`
Known problem: None
Action required: None

## Feature: Product CRUD

Frontend entry: `lib/features/add_product/`, `lib/features/catalogue/screens/`
Flutter route: `/addProduct`, `/product/:productId`
API endpoint: `POST /api/v1/products`, `GET /api/v1/products`, `GET /api/v1/products/{id}`, `PATCH /api/v1/products/{id}`, `DELETE /api/v1/products/{id}`
Backend service: `backend/routers/products.py`, `backend/services/catalog_service.py`
Database tables: `ProductDB`
External service: Cloudinary (optional)
Configuration required: `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
Current state: IMPLEMENTED
Test coverage: `tests/test_api.py`, `tests/test_listing_rules.py`
Known problem: Image upload requires explicit Cloudinary upload step
Action required: None (image upload endpoint available)

## Feature: Image Upload

Frontend entry: `lib/features/add_product/widgets/`
API endpoint: `POST /api/v1/products/upload-image`, `POST /api/v1/catalog/upload-image`
Backend service: `backend/routers/products.py`, `backend/routers/catalog.py`, `backend/services/cloudinary_service.py`
Database tables: `ProductDB.cloudinary_public_id`
External service: Cloudinary
Configuration required: `CLOUDINARY_*`
Current state: IMPLEMENTED
Test coverage: Manual
Known problem: Flutter app does not automatically upload before product creation
Action required: Update Flutter to upload images before product creation

## Feature: AI Image Enhancement

Frontend entry: `lib/features/add_product/widgets/step3_enhance_widget.dart`
API endpoint: `POST /api/v1/catalog/enhance-image`
Backend service: `backend/services/catalog_service.py`, `ML/image_pipeline/`
Database tables: `ProductDB`
External service: None (local ML)
Configuration required: `REMBG_MODEL`, `WARMUP_MODELS_ENABLED`
Current state: IMPLEMENTED
Test coverage: Manual
Known problem: None
Action required: None

## Feature: Voice Listing / Speech-to-Text

Frontend entry: `lib/features/add_product/widgets/step1_capture_widget.dart`
API endpoint: `POST /api/v1/catalog/transcribe`
Backend service: `backend/services/catalog_service.py`, `backend/services/voice_service.py`
Database tables: `ProductDB`
External service: Whisper or Bhashini ASR
Configuration required: `WHISPER_API_KEY`, `BHASHINI_*`
Current state: IMPLEMENTED
Test coverage: Manual
Known problem: None
Action required: None

## Feature: AI Catalog Generation

Frontend entry: `lib/features/add_product/widgets/`
API endpoint: `POST /api/v1/catalog/generate`
Backend service: `backend/services/catalog_service.py`
Database tables: `ProductDB`
External service: Groq / Gemini
Configuration required: `GROQ_API_KEY`, `GEMINI_API_KEY`
Current state: IMPLEMENTED
Test coverage: Manual
Known problem: None
Action required: None

## Feature: Pricing

Frontend entry: `lib/features/pricing/`
API endpoint: `POST /api/v1/pricing/suggest`
Backend service: `backend/services/pricing_service.py`, `ML/pricing/`
Database tables: `ProductDB`
External service: ChromaDB, LLM
Configuration required: `CHROMA_*`, `GROQ_API_KEY`, `GEMINI_API_KEY`
Current state: IMPLEMENTED
Test coverage: Manual
Known problem: Chroma failure returns error (not crash)
Action required: None

## Feature: Marketplace

Frontend entry: `lib/features/marketplace/`
Flutter route: `/marketplace`, `/product-detail/:productId`
API endpoint: `GET /api/v1/products`
Backend service: `backend/routers/products.py`
Database tables: `ProductDB`
External service: None
Configuration required: None
Current state: IMPLEMENTED
Test coverage: Manual
Known problem: None
Action required: None

## Feature: Cart & Checkout

Frontend entry: `lib/features/marketplace/screens/cart_screen.dart`
Flutter route: `/myCart`, `/checkout`
API endpoint: `POST /api/v1/cart`, `POST /api/v1/orders/checkout`
Backend service: `backend/services/cart_service.py`, `backend/services/order_service.py`
Database tables: `CartDB`, `CartItemDB`, `OrderDB`, `OrderItemDB`, `PaymentDB`, `ShipmentDB`
External service: None
Configuration required: None
Current state: IMPLEMENTED
Test coverage: `tests/test_cart_address_api.py`, `tests/test_order_creation.py`
Known problem: None
Action required: None

## Feature: Order History

Frontend entry: `lib/features/orders/screens/`
Flutter route: `/myOrders`, `/orderDetail`
API endpoint: `GET /api/v1/orders/my`, `GET /api/v1/orders/my/{id}`, `PATCH /api/v1/orders/{id}/status`
Backend service: `backend/routers/orders.py`, `backend/services/order_service.py`
Database tables: `OrderDB`, `ShipmentDB`
External service: None
Configuration required: None
Current state: IMPLEMENTED
Test coverage: `tests/test_consumer_orders.py`
Known problem: None
Action required: None

## Feature: ONDC Integration

Frontend entry: `lib/features/commerce/screens/government_selling_screen.dart`
API endpoint: `POST /api/v1/ondc/search`, `POST /api/v1/ondc/select`, `POST /api/v1/ondc/init`, `POST /api/v1/ondc/confirm`, `POST /api/v1/ondc/status`
Backend service: `backend/services/ondc/adapter.py`
Database tables: `OrderDB`, `ProductDB`
External service: ONDC network (optional)
Configuration required: None
Current state: IMPLEMENTED (local BPP)
Test coverage: Manual
Known problem: None
Action required: None

## Feature: GeM Integration

Frontend entry: `lib/features/gem/screens/`, `lib/features/catalogue/screens/product_detail_screen.dart`
Flutter route: `/gem/registration/:productId`, `/gem/readiness/:productId`, `/gem/listing-review/:productId`
API endpoint: `GET /api/v1/gem/products/{id}/readiness`, `POST /api/v1/gem/products/{id}/listing-draft`, `GET /api/v1/gem/products/{id}/listing-kit`, `GET /api/v1/gem/registration-options`, `GET /api/v1/gem/registration-guidance`, `POST /api/v1/gem/products/{id}/open`
Backend service: `backend/services/gem/`
Database tables: `ProductChannelDB`
External service: GeM portal (manual), Udyam portal (manual)
Configuration required: None
Current state: IMPLEMENTED (assisted handoff)
Test coverage: `tests/test_gem_integration.py`
Known problem: None
Action required: None

## Feature: Bhashini Integration

Frontend entry: `lib/features/add_product/widgets/step1_capture_widget.dart`
API endpoint: `POST /api/v1/catalog/transcribe`
Backend service: `backend/services/bhashini_service.py`
Database tables: None
External service: Bhashini ULCA (optional)
Configuration required: `BHASHINI_*`
Current state: IMPLEMENTED
Test coverage: Manual
Known problem: None
Action required: None

## Feature: Business Advisor

Frontend entry: `lib/features/business_advisor/`
Flutter route: `/businessAdvisor`
API endpoint: `GET /api/v1/advisor/insights`
Backend service: `backend/routers/advisor.py`
Database tables: `ProductDB`, `OrderDB`
External service: LLM
Configuration required: `GROQ_API_KEY`, `GEMINI_API_KEY`
Current state: IMPLEMENTED
Test coverage: Manual
Known problem: None
Action required: None

## Feature: Offline Sync

Frontend entry: `lib/core/offline_sync/`
API endpoint: Multiple (with queue drain)
Backend service: `backend/routers/products.py` (batch sync)
Database tables: `ProductDB`
External service: None
Configuration required: None
Current state: IMPLEMENTED
Test coverage: Manual
Known problem: None
Action required: None

## Feature: Localization

Frontend entry: `assets/translations/`
API: None
Backend: None
Configuration required: None
Current state: IMPLEMENTED
Test coverage: Manual
Known problem: Some missing translation keys
Action required: None

## Feature: Accessibility (TTS, large text, haptics)

Frontend entry: `lib/core/services/app_tts_service.dart`, `lib/core/theme/`
API: None
Backend: None
Configuration required: None
Current state: IMPLEMENTED
Test coverage: Manual
Known problem: None
Action required: None
