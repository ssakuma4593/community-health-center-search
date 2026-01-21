# OpenAI Enrichment Pipeline

This document describes the OpenAI enrichment pipeline for community health center data, including implementation details and usage instructions.

## Overview

The enrichment pipeline uses OpenAI's Responses API with web search to verify and enrich health center data. The pipeline consists of:

1. **Backend API Endpoint** - Server-side endpoint that calls OpenAI Responses API
2. **Enrichment Script** - Script that processes the CSV and calls the API
3. **Comparison Report** - Report for manual review of discrepancies
4. **Frontend Display** - Website that displays enriched data

## Architecture

```
CSV File → Enrichment Script → Backend API → OpenAI Responses API → Enriched CSV
                                                      ↓
                                            Comparison Report (for manual review)
                                                      ↓
                                            Final CSV (with resolved columns)
                                                      ↓
                                            Frontend Website
```

## What Was Implemented

### 1. New Branch Created
- Branch: `feature/openai-enrichment`
- All changes are on this branch

### 2. GitHub Pages Deployment
- Created `.github/workflows/deploy-pages.yml`
- Automatically deploys frontend to GitHub Pages on push
- Works with the existing Vite configuration

### 3. Backend API Endpoint
- **File**: `backend/app/services/openai_enrichment.py`
- **Endpoint**: `POST /api/enrich-center`
- Uses OpenAI Responses API with web search
- Returns verified phone, address, website, types, and new patient instructions

### 4. CSV Enrichment Script
- **File**: `scripts/enrich_csv.py`
- Reads `data/processed/community_health_centers_with_coords.csv`
- Calls enrichment API for each center
- Writes `data/processed/community_health_centers_enriched.csv`
- Generates `reports/enrichment_comparison_report.txt` for manual review

### 5. CSV Schema Extension
Added new columns:

**OpenAI Enrichment Columns:**
- `openai_phone` - Verified phone number
- `openai_address` - Verified address
- `openai_website` - Verified website URL
- `openai_types` - Verified service types
- `openai_new_patient_md` - Markdown instructions for new patients
- `openai_other_notes_md` - Additional helpful notes (Markdown)
- `openai_source_urls` - Source URLs (comma-separated)
- `openai_last_checked_utc` - Last check timestamp (ISO)
- `openai_confidence` - Confidence level (Low/Med/High)

**Resolved Columns (for manual review):**
- `final_phone` - Manually resolved phone number
- `final_address` - Manually resolved address
- `final_website` - Manually resolved website URL
- `final_types` - Manually resolved service types
- `final_new_patient_md` - Manually resolved new patient instructions

### 6. Frontend Updates
- Updated `frontend/src/types.ts` to include all new columns
- Updated `frontend/src/components/HealthCenterDetail.tsx` to:
  - Display enriched data with priority: `final_*` > `openai_*` > original
  - Show new patient walkthrough as Markdown
  - Display confidence level and last checked date

## Setup

### 1. Backend Setup

Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Set up environment variables:

```bash
# Create .env file in backend directory
echo "OPENAI_API_KEY=your_api_key_here" > backend/.env
```

Start the backend server:

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 2. Enrichment Script Setup

Install Python dependencies:

```bash
pip install requests
```

Set environment variable (optional, defaults to localhost):

```bash
export API_BASE_URL=http://localhost:8000
```

## Usage

### Step 1: Run Enrichment Script

```bash
python scripts/enrich_csv.py
```

This script will:
- Read `data/processed/community_health_centers_with_coords.csv`
- Call the enrichment API for each center
- Write `data/processed/community_health_centers_enriched.csv`
- Generate `reports/enrichment_comparison_report.txt`

**Note:** The script includes a 1-second delay between requests to be respectful to the API. For large datasets, this may take a while.

### Step 2: Review Comparison Report

Open `reports/enrichment_comparison_report.txt` and review:
- Centers with phone/address/type discrepancies
- Centers with low confidence scores
- New patient instructions for each center

### Step 3: Manually Resolve Discrepancies

Open `data/processed/community_health_centers_enriched.csv` and update the `final_*` columns:
- `final_phone` - Resolved phone number
- `final_address` - Resolved address
- `final_website` - Resolved website URL
- `final_types` - Resolved service types
- `final_new_patient_md` - Resolved new patient instructions

**Priority:** The frontend displays data in this order:
1. `final_*` columns (manually resolved)
2. `openai_*` columns (AI enriched)
3. Original columns (from source CSV)

### Step 4: Update Frontend Data

Copy the enriched CSV to the frontend:

```bash
cp data/processed/community_health_centers_enriched.csv frontend/public/data/centers.csv
```

## CSV Schema

### Original Columns

- `name` - Health center name
- `street_address_1` - Street address line 1
- `street_address_2` - Street address line 2 (optional)
- `city_town` - City
- `state` - State
- `zipcode` - Zipcode
- `phone` - Phone number
- `types` - Service types (comma-separated)
- `website` - Website URL
- `latitude` - Latitude coordinate
- `longitude` - Longitude coordinate

### OpenAI Enrichment Columns

- `openai_phone` - Verified phone number from OpenAI
- `openai_address` - Verified address from OpenAI
- `openai_website` - Verified website URL from OpenAI
- `openai_types` - Verified service types from OpenAI
- `openai_new_patient_md` - Markdown instructions for new patients
- `openai_other_notes_md` - Additional helpful notes (Markdown)
- `openai_source_urls` - Source URLs (comma-separated)
- `openai_last_checked_utc` - Last check timestamp (ISO format)
- `openai_confidence` - Confidence level (Low/Med/High)

### Resolved Columns (for manual review)

- `final_phone` - Manually resolved phone number
- `final_address` - Manually resolved address
- `final_website` - Manually resolved website URL
- `final_types` - Manually resolved service types
- `final_new_patient_md` - Manually resolved new patient instructions

## API Endpoint

### POST `/api/enrich-center`

Enrich a health center record using OpenAI Responses API.

**Request Body:**
```json
{
  "name": "Health Center Name",
  "website": "https://example.com",
  "raw_text": "Additional information",
  "existing_address": "123 Main St, City, State 12345",
  "existing_phone": "(555) 123-4567",
  "existing_types": "Primary Care, Dental Care"
}
```

**Response:**
```json
{
  "openai_phone": "(555) 123-4567",
  "openai_address": "123 Main Street, City, State 12345",
  "openai_website": "https://example.com",
  "openai_types": "Primary Care, Dental Care",
  "openai_new_patient_md": "## How to Become a New Patient\n\n1. Call...",
  "openai_other_notes_md": "Additional notes...",
  "openai_source_urls": "https://example.com, https://other.com",
  "openai_confidence": "High",
  "openai_last_checked_utc": "2024-01-01T00:00:00Z"
}
```

## Frontend Display

The frontend automatically:
- Prioritizes `final_*` columns over `openai_*` columns
- Falls back to original columns if enriched data is not available
- Displays new patient instructions as Markdown
- Shows confidence level and last checked date

## Files Created/Modified

### New Files
- `.github/workflows/deploy-pages.yml` - GitHub Pages deployment workflow
- `backend/app/services/openai_enrichment.py` - OpenAI enrichment service
- `scripts/enrich_csv.py` - CSV enrichment script
- `docs/OPENAI_ENRICHMENT.md` - This documentation

### Modified Files
- `backend/requirements.txt` - Added OpenAI SDK and python-dotenv
- `backend/app/main.py` - Added enrichment endpoint
- `frontend/src/types.ts` - Added new column types
- `frontend/src/components/HealthCenterDetail.tsx` - Updated to display enriched data

## Important Notes

1. **API Key Security**: Never commit `OPENAI_API_KEY` to the repository. Use environment variables.

2. **Rate Limiting**: The enrichment script includes a 1-second delay between requests. For large datasets, this may take a while.

3. **Cost Considerations**: OpenAI Responses API charges per request. Monitor usage in the OpenAI dashboard.

4. **Manual Review**: Always review the comparison report before using enriched data in production.

5. **Data Priority**: The frontend prioritizes `final_*` columns (manually resolved) over `openai_*` columns (AI enriched) over original columns.

## Testing

To test the enrichment endpoint:

```bash
curl -X POST http://localhost:8000/api/enrich-center \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Health Center",
    "website": "https://example.com",
    "existing_address": "123 Main St, Boston, MA 02115",
    "existing_phone": "(617) 555-1234",
    "existing_types": "Primary Care"
  }'
```

## Troubleshooting

### API Key Not Set

If you see "OpenAI enrichment service not available", make sure:
1. `OPENAI_API_KEY` is set in `backend/.env`
2. Backend server is running
3. API endpoint is accessible

### Enrichment Script Fails

- Check that backend server is running
- Verify `API_BASE_URL` environment variable is correct
- Check network connectivity
- Review error messages in console

### Low Quality Enrichment

- Some centers may have low confidence scores
- Review the comparison report for discrepancies
- Manually resolve discrepancies in `final_*` columns
- Re-run enrichment for specific centers if needed

## Cost Considerations

- OpenAI Responses API charges per request
- Web search tool usage may incur additional costs
- Consider batching or rate limiting for large datasets
- Monitor API usage in OpenAI dashboard

## Next Steps

After enrichment:
1. Review comparison report
2. Resolve discrepancies manually
3. Update `final_*` columns
4. Copy enriched CSV to frontend
5. Deploy updated website
