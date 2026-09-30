# GeM Demo Guide

## How to Demonstrate the GeM Workflow

### Prerequisites
- Backend running on http://localhost:8000
- Flutter app running on a device/emulator
- Artisan account with at least one product

### Step-by-Step Demo

1. **Create an artisan product**
   - Open Craftsy app
   - Add a product with title, description, price, image, and category
   - Save the product

2. **Open Product Detail**
   - Go to the artisan's product list
   - Tap on the product
   - Tap the three-dot menu (⋮)

3. **Tap "Sell on GeM"**
   - This opens the GeM registration screen

4. **Select registration state**
   - **If already registered on GeM:** Tap "Yes" → Continue on GeM
   - **If has Udyam but no GeM:** Tap "No", then "Yes" → Open Udyam
   - **If neither:** Tap "No", then "No" → Start Udyam or Visit GeM

5. **View Product Readiness**
   - Craftsy checks the product data
   - Shows missing fields (if any)
   - Shows available fields
   - Shows next actions

6. **Fill missing information**
   - If product is missing fields, tap "Add Missing Information"
   - This navigates to the listing review where the AI-generated draft is shown

7. **Generate and review listing**
   - AI generates a GeM Listing Draft from verified product data only
   - Artisan reviews product name, description, price, specifications, etc.
   - Missing fields are highlighted
   - Disclaimer clearly states this is NOT an official GeM submission

8. **Open GeM**
   - Tap "Open GeM"
   - Craftsy opens the official GeM seller portal (https://www.gem.gov.in/)
   - Artisan logs in manually

9. **Manual submission on GeM**
   - Artisan uses the Craftsy-prepared listing data
   - Completes the listing on GeM manually
   - Craftsman returns to Craftsy and marks status if needed

## Important Demo Notes

- **Do NOT claim** that Craftsy published the listing on GeM.
- **Do NOT show** a fake "Successfully listed on GeM" screen.
- **DO show** the "GeM Listing Draft" and explain it is prepared by Craftsy for artisan review.
- **DO show** the official portal handoff and explain that final submission happens on GeM.

## What is NOT Implemented

- Live GeM API publishing (requires official authorization)
- Automated GeM login
- Udyam→GeM automated onboarding
- Real GeM catalogue status updates
- Direct GeM order/payment integration
