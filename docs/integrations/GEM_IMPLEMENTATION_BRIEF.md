Craftsy GeM Integration – Implementation Brief

Purpose:
Help Craftsy artisans prepare and submit products to GeM with
minimum technical knowledge.

Verified facts:
1. GeM supports seller registration using Aadhaar/Virtual ID or
   personal PAN according to official seller prerequisites.
2. Government sources confirm API integration between Udyam MSME
   database and GeM for 2-step seller auto-registration.
3. Udyam login uses Udyam Registration Number + registered
   mobile/email + OTP.
4. GeM catalogue management is category-driven.
5. Product specifications/certifications can vary by category.
6. Craftsy currently has no verified authorized GeM seller
   catalogue publishing API.
7. Therefore current implementation must use assisted official
   GeM handoff.
8. Never store GeM/Udyam passwords or OTPs.
9. Never scrape or browser-automate GeM.
10. Never claim a product is listed without evidence.

Current Craftsy ProductDB remains the source of product data.

Current implementation:
Craftsy Product
→ GeM readiness
→ missing fields
→ category preparation
→ AI listing draft
→ artisan review
→ listing kit
→ official GeM handoff

Future:
OfficialGeMApiProvider can replace/augment AssistedGeMProvider
when authorized API access becomes available.