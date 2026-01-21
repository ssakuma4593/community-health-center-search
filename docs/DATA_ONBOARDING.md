# Data Onboarding Guide

How to add or update community health centers in the application.

## 🔄 Data Pipeline Overview

```
1. Parse Official Document        2. Geocoding                    3. Application
   ↓                                ↓                               ↓
scripts/scrape_docx.py      →  scripts/add_geocoding.py  →  frontend/api reads
   ↓                                ↓                               ↓
data/raw/hsn_active_health_  →  data/processed/community_  →  Displays on map
centers_parsed.csv                health_centers_with_          and list
                                 coords.csv
```

---

## 📥 Adding New Health Centers

### Step 1: Parse Official Document

The parser extracts health center data from official Massachusetts health center documents.

```bash
# Install dependencies (first time only)
pip install python-docx

# Run the parser
python scripts/scrape_docx.py
```

**What it does:**
- Parses health center listings from official Word documents
- Extracts: name, address, phone, services, website
- Outputs: `data/raw/hsn_active_health_centers_parsed.csv` (with separate address columns)

**Expected output:**
```
Reading DOCX file: data/official_documents/hsn-active-health-center-listings.docx
Processing table 1 with 112 rows
Extracted 111 unique health centers
✅ Successfully saved 111 centers to data/raw/hsn_active_health_centers_parsed.csv
```

**Output file:** `data/raw/hsn_active_health_centers_parsed.csv`

### Step 2: Add Geocoding

Convert addresses to latitude/longitude coordinates for map display.

```bash
# Install dependencies (if not already installed)
pip install requests pandas

# Run geocoding
python scripts/add_geocoding.py YOUR_GOOGLE_MAPS_API_KEY
```

**What it does:**
- Reads parsed CSV file: `data/raw/hsn_active_health_centers_parsed.csv`
- Validates each address
- Calls Google Maps Geocoding API (one-time data processing)
- Adds latitude/longitude columns
- Outputs: `data/processed/community_health_centers_with_coords.csv`

**Note:** This script uses Google Maps API for one-time geocoding. The frontend app uses free Leaflet/OpenStreetMap and doesn't require any API keys.

**Expected output:**
```
🌍 Starting geocoding for 276 health centers...
[1/276] Community Health Center
  📍 Address: 130 Water Street, Fitchburg, MA, 01420
  ✅ Success: 42.583542, -71.802345
...
📊 Geocoding Summary:
  ✅ Successful: 260/276 (94.2%)
  ❌ Failed: 8/276 (2.9%)
  ⏭️  Skipped (no address): 8/276 (2.9%)
  📞 API calls made: 268 (saved 8 calls)
```

**Output file:** `data/processed/community_health_centers_with_coords.csv`

### Step 3: Verify & Deploy

```bash
# Test locally
cd frontend
npm run dev

# Search for a zipcode to verify new data appears
# e.g., search for 02138
```

The application automatically reads `data/processed/community_health_centers_with_coords.csv` (or the CSV copied to `frontend/public/data/centers.csv`).

---

## 🔧 Manual Data Entry

If you need to add health centers manually:

### 1. Edit the CSV

Open the parsed CSV file (`data/raw/hsn_active_health_centers_parsed.csv`) and add a new row:

```csv
name,street_address_1,street_address_2,city_town,state,zipcode,phone,types,website,source
"New Health Center","123 Main St","Suite 100","Boston","MA","02118","(617) 555-0100","Primary Care, Dental Care","https://example.com","manual"
```

### 2. Run Geocoding

```bash
python scripts/add_geocoding.py YOUR_GOOGLE_MAPS_API_KEY
```

This will add coordinates for the new entry.

---

## 📝 CSV Format

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Health center name | `"Community Health Center"` |
| `street_address_1` | Primary street address | `"123 Main St"` |
| `city_town` | City or town | `"Boston"` |
| `state` | State (MA) | `"MA"` |
| `zipcode` | 5-digit zipcode | `"02118"` |
| `phone` | Phone number | `"(617) 555-0100"` |
| `types` | Services offered | `"Primary Care, Dental Care"` |

### Optional Fields

| Field | Description | Example |
|-------|-------------|---------|
| `street_address_2` | Suite, floor, etc. | `"Suite 100"` |
| `website` | Website URL | `"https://example.com"` |
| `source` | Data source | `"official_document"` or `"web_scraper"` |

### Geocoded Fields (Added Automatically)

| Field | Description | Example |
|-------|-------------|---------|
| `latitude` | Latitude coordinate | `42.3601` |
| `longitude` | Longitude coordinate | `-71.0589` |

---

## 🔄 Updating Existing Data

### Option 1: Re-run the Parser

```bash
# This will parse the latest data from official documents
python scripts/scrape_docx.py

# Then re-geocode
python scripts/add_geocoding.py YOUR_GOOGLE_MAPS_API_KEY
```

### Option 2: Manual Edit

1. Open the parsed CSV file (`data/raw/hsn_active_health_centers_parsed.csv`)
2. Edit the specific row(s)
3. Save the file
4. Re-run geocoding: `python scripts/add_geocoding.py YOUR_API_KEY`

---

## 🗑️ Deprecated Scripts

These scripts are **no longer needed** with the current workflow:

- ❌ `final_merge_script.py` - Was used to merge multiple data sources
- ❌ `final_document_parser.py` - Was replaced by `scripts/scrape_docx.py`
- ❌ `community_health_scraper.py` - Web scraper (removed, using official documents only)
- ❌ `run_scraper.py` - Web scraper runner (removed, using official documents only)

You can safely ignore these files. The current workflow is:
1. **Document Parser** (`scripts/scrape_docx.py`) → extracts data from official documents, outputs parsed format
2. **Geocoding** (`scripts/add_geocoding.py`) → adds coordinates

---

## 🧪 Testing Your Changes

### 1. Check CSV Format

```bash
# View the first few lines
head -n 5 data/processed/community_health_centers_with_coords.csv

# Count total entries
wc -l data/processed/community_health_centers_with_coords.csv
```

### 2. Test Locally

```bash
cd frontend
npm run dev
```

Open http://localhost:3000 and:
- Search for zipcodes with new/updated centers
- Verify they appear on the map
- Click markers to check details
- Ensure contact info is correct

### 3. Verify Geocoding

Check that new entries have coordinates:
```bash
# Look for entries with coordinates
grep "42\." data/processed/community_health_centers_with_coords.csv | head -n 3
```

---

## 📊 Data Quality Checks

### Before Deploying

- [ ] All required fields are populated
- [ ] Phone numbers are formatted consistently
- [ ] Zipcodes are 5 digits
- [ ] Addresses are valid
- [ ] Coordinates exist for entries with addresses
- [ ] Website URLs are valid (if provided)
- [ ] Service types are consistent

### Common Issues

**Missing Coordinates:**
- Cause: Invalid or incomplete address
- Fix: Update address in CSV and re-run geocoding

**Duplicate Entries:**
- Cause: Center listed multiple times
- Fix: Remove duplicates from CSV

**Wrong Location on Map:**
- Cause: Incorrect address or geocoding error
- Fix: Verify address, re-run geocoding, or manually correct coordinates

---

## 🚀 Deployment

### After Updating Data

1. **Commit changes:**
   ```bash
   git add data/processed/community_health_centers_with_coords.csv
   git commit -m "Update health center data"
   ```

2. **Deploy to production:**
   - Your hosting platform will automatically use the updated CSV
   - No code changes needed
   - Data updates are instant

3. **Verify in production:**
   - Test searches with updated zipcodes
   - Check that new centers appear
   - Verify map markers are in correct locations

---

## 🔑 API Key Management

### Google Maps API Key (Optional - One-Time Geocoding Only)

The Google Maps API key is **only needed** for the one-time geocoding script (`scripts/add_geocoding.py`) when adding new health centers. The frontend app itself uses free services (Leaflet/OpenStreetMap) and doesn't require any API keys.

### For One-Time Geocoding Script

If you need to geocode new health center addresses:

1. Get a Google Maps Geocoding API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Run the geocoding script:
   ```bash
   python scripts/add_geocoding.py YOUR_GOOGLE_MAPS_API_KEY
   ```

### API Usage

- **Geocoding Script**: Only needed when adding/updating data (one-time process)
- **Frontend App**: Uses free Leaflet/OpenStreetMap (no API key needed)
- **Free Tier**: Google Maps $200/month credit covers typical geocoding usage

---

## 📞 Troubleshooting

### Parser Issues

**Problem:** Parser fails or returns no data

**Solutions:**
- Verify the DOCX file exists in `data/official_documents/`
- Check that `python-docx` is installed: `pip install python-docx`
- Verify the document structure matches expected format
- Check file permissions

### Geocoding Issues

**Problem:** Geocoding fails for some addresses

**Solutions:**
- Check address format (should include street, city, state)
- Verify API key has Geocoding API enabled
- Check API quota hasn't been exceeded
- Try geocoding individual problematic addresses

### Data Not Showing

**Problem:** New data doesn't appear in the app

**Solutions:**
- Verify `data/processed/community_health_centers_with_coords.csv` exists
- Check file has latitude/longitude columns
- Copy CSV to `frontend/public/data/centers.csv` if needed
- Restart dev server
- Clear browser cache
- Check API endpoint: `http://localhost:3000/api/health-centers`

---

## 📅 Recommended Update Schedule

### Frequency

- **Monthly**: Run scraper to check for new health centers
- **Quarterly**: Verify existing data is still accurate
- **As Needed**: When notified of new centers or closures

### Process

1. Run scraper on first of the month
2. Compare with previous data
3. If changes detected, run geocoding
4. Test locally
5. Deploy to production
6. Notify users of updates (if significant)

---

## 🤝 Contributing Data

If you have information about health centers not in our database:

1. **Submit an issue** on GitHub with details
2. **Or** fork the repo, add to CSV, and submit a pull request
3. **Or** email details to maintainers

Include:
- Health center name
- Full address
- Phone number
- Services offered
- Website (if available)
- Source of information

---

## 📝 Summary

**Quick Workflow:**
```bash
# 1. Parse official document
python scripts/scrape_docx.py

# 2. Add coordinates
python scripts/add_geocoding.py YOUR_API_KEY

# 3. Test
cd frontend && npm run dev

# 4. Deploy
git add data/processed/community_health_centers_with_coords.csv
git commit -m "Update health center data"
git push
```

**That's it!** The application will automatically use the updated data.

