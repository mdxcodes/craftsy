# Cloudinary Integration

## 1. Why Cloudinary Is Used

Craftsy's Railway container filesystem is ephemeral. Images stored under
`/app/backend/uploads` are lost on every redeployment or container restart.
Cloudinary provides permanent, redundant image storage with CDN delivery,
ensuring product images persist across Railway deploys.

Railway remains the backend hosting platform. Cloudinary is the permanent
image storage and delivery service.

## 2. Architecture

```
Flutter
   |
   v
Railway FastAPI
   |
   +--> temporary local file (/app/backend/uploads)
   |       |
   |       v
   |   rembg/Pillow AI enhancement
   |       |
   |       v
   +--> Cloudinary (permanent image)
   |       |
   |       v
   |   HTTPS URL
   |
   +--> PostgreSQL
           |
           +--> ProductDB.image_url = Cloudinary HTTPS URL
           +--> ProductDB.cloudinary_public_id = Cloudinary public ID
```

## 3. Local Development vs Production

- **Local development**: Cloudinary is optional. If `CLOUDINARY_*` env vars
  are not set, the backend falls back to local `/uploads` URLs.
- **Production (Railway)**: Set `CLOUDINARY_CLOUD_NAME`,
  `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET` in the Railway
  dashboard. All enhanced product images are uploaded to Cloudinary.

## 4. Required Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | Yes (for Cloudinary) |
| `CLOUDINARY_API_KEY` | Cloudinary API key | Yes (for Cloudinary) |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | Yes (for Cloudinary) |

Never commit real values to Git. Put empty placeholders in `.env.example`.
Railway supplies the real values via dashboard or CLI.

## 5. Cloudinary Account Setup

1. Sign up at https://cloudinary.com/
2. Create a new "cloud" (or use the default one)
3. Copy the **Cloud name**, **API Key**, and **API Secret** from the
   dashboard
4. Add them to your Railway backend service environment variables

## 6. Upload Lifecycle

1. Flutter sends image via multipart POST to `/api/v1/catalog/enhance-image`
2. Backend saves raw upload to `/app/backend/uploads/raw/` (temporary)
3. Backend runs AI enhancement (rembg + Pillow) and saves to
   `/app/backend/uploads/enhanced/` (temporary)
4. Backend uploads enhanced image to Cloudinary folder
   `craftsy/products/{product_id}/`
5. Cloudinary returns `public_id` and `secure_url`
6. Backend stores `secure_url` in `ProductDB.image_url` and
   `public_id` in `ProductDB.cloudinary_public_id`
7. API response returns the Cloudinary HTTPS URL
8. Flutter displays the image via `CachedNetworkImage`

## 7. Product Image Lifecycle

### Creation
- Artisan captures/selects photo in Flutter
- Flutter sends to `/api/v1/catalog/enhance-image` for AI enhancement
- Backend returns Cloudinary HTTPS URL (or local fallback)
- Flutter includes `image_url` in product creation payload
- Backend stores Cloudinary URL in `ProductDB.image_url`

### Update
- When `image_url` is updated with a new Cloudinary URL:
  - Backend extracts `cloudinary_public_id` from the new URL
  - Deletes the old Cloudinary image (if different)
  - Saves new `image_url` and `cloudinary_public_id`
- When `image_url` is updated with a non-Cloudinary URL:
  - Backend clears `cloudinary_public_id`
  - Deletes the old Cloudinary image (if any)

### Deletion
- When a product is deleted:
  - Backend checks `cloudinary_public_id`
  - If present, deletes the image from Cloudinary
  - Then deletes the database record
  - Cloudinary deletion failure is logged but does not block DB deletion

## 8. Existing Image Migration

Products created before Cloudinary migration have local `/uploads/...` URLs
in `image_url` and `cloudinary_public_id = NULL`.

A migration script can be created at `scripts/migrate_images_to_cloudinary.py`
to:

1. Query products with local `image_url` values
2. Verify the local file exists
3. Upload to Cloudinary
4. Update `image_url` to Cloudinary HTTPS URL
5. Update `cloudinary_public_id`
6. Commit the database update

**Do not run migration automatically at startup.**

## 9. Cloudinary Folder Structure

```
craftsy/
  products/
    {product_id}/
      original      # Enhanced product photo
  social/
    {filename}      # Social media helper images
  profiles/
    {artisan_id}/
      profile        # (Future) artisan profile photos
```

Public IDs are stable and collision-resistant. Raw user filenames are
never used as the sole Cloudinary public ID.

## 10. Local Development Setup

1. Install the Cloudinary Python SDK:
   ```bash
   pip install cloudinary
   ```
2. Optional: Add to `.env`:
   ```
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```
3. Without these variables, the backend uses local `/uploads` URLs.

## 11. Railway Configuration

Add the following environment variables to your Railway backend service:

```
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

Do **not** create a Railway Volume for permanent product images.
Cloudinary handles persistent storage.

## 12. Security Considerations

- Cloudinary credentials are **backend-only**. They never appear in Flutter,
  frontend code, or API responses.
- `CLOUDINARY_API_SECRET` is never logged. Startup logs only indicate
  whether Cloudinary is configured (`Cloudinary configured: yes/no`).
- `.env.example` contains empty placeholders only.
- All Cloudinary public IDs are sanitized to prevent path traversal.
- The `extract_public_id_from_url` method only processes URLs from
  `res.cloudinary.com`.

## 13. Troubleshooting

### Images not persisting across Railway deploys
- Verify `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and
  `CLOUDINARY_API_SECRET` are set in Railway.
- Check Railway logs for "Cloudinary configured: yes" at startup.
- Verify `image_url` in the database response is a `https://res.cloudinary.com`
  URL, not a `/uploads/...` path.

### Social media helper fails with "Invalid or unavailable product image"
- The social media service downloads Cloudinary images to a temporary
  local path before sending to Gemini vision.
- Check that the Railway container can reach `res.cloudinary.com`.

### Enhanced image upload fails but enhancement succeeds
- The `/api/v1/catalog/enhance-image` endpoint returns the local
  `/uploads/enhanced/...` URL as a fallback when Cloudinary upload fails.
- Check Railway logs for the warning: `Cloudinary upload failed, falling
  back to local URL`.
