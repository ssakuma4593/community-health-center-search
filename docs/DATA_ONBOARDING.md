# Data Onboarding Guide

How to add or update community health centers in the application.

## 🔄 Data Pipeline Overview

```
1. Web Scraper          2. DOCX Scraper          3. Geocoding          4. Application
   ↓                        ↓                       ↓                      ↓
community_health_    →  scrape_docx.py    →  add_geocoding.py  →  frontend/api reads
scraper.py                                       ↓                      ↓
   ↓                        ↓                   community_health_  →  Displays on map
community_health_          hsn_active_         centers_with_         and list
centers_scraped_           health_centers_     coords.csv
fresh.csv                  scraped.csv
```

---

## 📍 Data Sources

The official list of community health centers comes from the Massachusetts state government:

**Official Source:** [Mass.gov - Information for Patients](https://www.mass.gov/info-details/information-for-patients)

This page provides links to Health Safety Net (HSN) provider listings, including community health centers and acute care hospitals in Massachusetts. It includes a downloadable DOCX file (`hsn-active-health-center-listings.docx`) that contains the official list.

**Data Collection Methods:**

1. **Mass League Website Scraper** (`community_health_scraper.py`)
   - Source: [Mass League of Community Health Centers - Find a Community Health Center](https://www.massleague.org/public-resources/about-community-health-centers/find-a-community-health-center/)
   - Output: `community_health_centers_scraped_fresh.csv`
   - The Mass League website is linked from the official Mass.gov page and provides a searchable directory.

2. **Official DOCX Scraper** (`scrape_docx.py`)
   - Source: Official DOCX file from Mass.gov (`data/official_documents/hsn-active-health-center-listings.docx`)
   - Output: `hsn_active_health_centers_scraped.csv`
   - This pulls directly from the authoritative government document.

---

## 📥 Adding New Health Centers

### Step 1: Run the Web Scraper

The scraper pulls health center data from the [Mass League of Community Health Centers website](https://www.massleague.org/public-resources/about-community-health-centers/find-a-community-health-center/), which is the searchable directory of community health centers. 

```bash
# Install dependencies (first time only)
pip install -r scraper_requirements.txt

# Run the scraper
python community_health_scraper.py
```

**What it does:**
- Scrapes health center listings from official websites
- Extracts: name, address, phone, services, website
- Outputs: `community_health_centers_scraped_fresh.csv`

**Expected output:**
```
🌐 Starting scraper...
[1/123] Scraping Community Health Center...
  ✅ Success
...
✨ Done! Saved 123 health centers to community_health_centers_scraped_fresh.csv
```

**Output file:** `community_health_centers_scraped_fresh.csv`

### Step 2: Scrape Official DOCX File

The official Mass.gov page provides a DOCX file listing all Health Safety Net (HSN) community health centers. This script extracts data from that official document.

```bash
# Install dependencies (first time only)
pip install python-docx

# Run the DOCX scraper
python scrape_docx.py
```

**What it does:**
- Reads the official DOCX file from `data/official_documents/hsn-active-health-center-listings.docx`
- Extracts: name, address, phone, services
- Outputs: `hsn_active_health_centers_scraped.csv`

**Expected output:**
```
Reading DOCX file: data/official_documents/hsn-active-health-center-listings.docx
Processing table 1 with 112 rows
  Headers: [...]
...
Extracted 111 unique health centers
✅ Successfully saved 111 centers to hsn_active_health_centers_scraped.csv
✅ Done! CSV saved to hsn_active_health_centers_scraped.csv
```

**Output file:** `hsn_active_health_centers_scraped.csv`

**Note:** This pulls from the official Mass.gov source file, which provides authoritative Health Safety Net provider listings.

### Step 3: Add Geocoding

Convert addresses to latitude/longitude coordinates for map display.

```bash
# Install dependencies (if not already installed)
pip install requests pandas

# Run geocoding
python add_geocoding.py YOUR_GOOGLE_MAPS_API_KEY
```

**What it does:**
- Reads `community_health_centers_parsed.csv` (or you can modify the script to read other CSV files)
- Validates each address
- Calls Google Maps Geocoding API
- Adds latitude/longitude columns
- Outputs: `community_health_centers_with_coords.csv`

**Note:** The `add_geocoding.py` script currently reads from `community_health_centers_parsed.csv` by default. If you have a different CSV file, you can modify the script or ensure your CSV matches the expected format with columns: `name`, `street_address_1`, `street_address_2`, `city_town`, `state`, `zipcode`, `phone`, `types`, `website`.

**Expected output:**
```
🌍 Starting geocoding for 273 health centers...
[1/273] Community Health Center
  📍 Address: 130 Water Street, Fitchburg, MA, 01420
  ✅ Success: 42.583542, -71.802345
...
📊 Geocoding Summary:
  ✅ Successful: 260/273 (95.2%)
  ❌ Failed: 5/273 (1.8%)
  ⏭️  Skipped (no address): 8/273 (2.9%)
  📞 API calls made: 265 (saved 8 calls)
```

**Output file:** `community_health_centers_with_coords.csv`

### Step 4: Verify & Deploy

```bash
# Test locally
cd frontend
npm run dev

# Search for a zipcode to verify new data appears
# e.g., search for 02138
```

The application automatically reads `community_health_centers_with_coords.csv`.

---

## 🔧 Manual Data Entry

If you need to add health centers manually:

### 1. Edit the CSV

Open `community_health_centers_with_coords.csv` (production file) or create a new CSV with the correct format. Add a new row:

```csv
name,street_address_1,street_address_2,city_town,state,zipcode,phone,types,website,source
"New Health Center","123 Main St","Suite 100","Boston","MA","02118","(617) 555-0100","Primary Care, Dental Care","https://example.com","manual"
```

### 2. Run Geocoding

```bash
python add_geocoding.py YOUR_GOOGLE_MAPS_API_KEY
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

### Option 1: Re-run Both Scrapers

```bash
# This will fetch the latest data from official sources

# Step 1: Scrape Mass League website
python community_health_scraper.py
# or
python run_scraper.py
# This generates: community_health_centers_scraped_fresh.csv

# Step 2: Scrape official DOCX file
python scrape_docx.py
# This generates: hsn_active_health_centers_scraped.csv

# Step 3: Then re-geocode (make sure add_geocoding.py is configured to read the correct input file)
python add_geocoding.py YOUR_GOOGLE_MAPS_API_KEY
```

### Option 2: Manual Edit

1. Open `community_health_centers_with_coords.csv` (production file) or the source CSV file you're working with
2. Edit the specific row(s)
3. Save the file
4. Re-run geocoding: `python add_geocoding.py YOUR_API_KEY`

---

## 🗑️ Deprecated Scripts

These scripts are **archived** and no longer used in the current workflow:

- ❌ `archive/final_merge_script.py` - Was used to merge multiple data sources
- ❌ `archive/final_document_parser.py` - Was used to parse Word documents
- ❌ `archive/community_health_centers_final.csv` - Old scraped data (replaced by `community_health_centers_scraped_fresh.csv`)
- ❌ `archive/community_health_centers_parsed.csv` - Old parsed data

You can safely ignore these archived files. The current workflow is:
1. **Scraper** (`community_health_scraper.py` or `run_scraper.py`) → generates `community_health_centers_scraped_fresh.csv`
2. **Geocoding** (`add_geocoding.py`) → adds coordinates → generates `community_health_centers_with_coords.csv` (production file)

---

## 🧪 Testing Your Changes

### 1. Check CSV Format

```bash
# View the first few lines
head -n 5 community_health_centers_with_coords.csv

# Count total entries
wc -l community_health_centers_with_coords.csv
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
grep "42\." community_health_centers_with_coords.csv | head -n 3
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
   git add community_health_centers_with_coords.csv
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

### Development

Store in `frontend/.env.local`:
```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_dev_api_key
```

### Production

Add to your hosting platform (Vercel, Netlify, etc.):
```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_production_api_key
```

### API Usage

- **Geocoding**: Only needed when adding/updating data (not on every deployment)
- **Maps Display**: Used by users viewing the map
- **Free Tier**: $200/month credit covers typical usage

---

## 📞 Troubleshooting

### Scraper Issues

**Problem:** Scraper fails or returns no data

**Solutions:**
- Check internet connection
- Verify source website is accessible
- Update scraper if website structure changed
- Check Chrome/ChromeDriver compatibility

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
- Verify `community_health_centers_with_coords.csv` exists
- Check file has latitude/longitude columns
- Restart dev server
- Clear browser cache
- Check API endpoint: `http://localhost:3000/api/health-centers`

---

## 📅 Recommended Update Schedule

### Frequency

- **Monthly**: Run both scrapers (Mass League website and official DOCX) to check for new health centers
- **Quarterly**: Verify existing data is still accurate
- **As Needed**: When notified of new centers or closures

### Process

1. Run both scrapers on first of the month (Mass League and DOCX)
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
# 1. Scrape Mass League website
python community_health_scraper.py
# or
python run_scraper.py
# Generates: community_health_centers_scraped_fresh.csv

# 2. Scrape official DOCX file
python scrape_docx.py
# Generates: hsn_active_health_centers_scraped.csv

# 3. Add coordinates
# Note: Make sure add_geocoding.py is configured to read your source CSV file
python add_geocoding.py YOUR_API_KEY
# Generates: community_health_centers_with_coords.csv (production file)

# 4. Test
cd frontend && npm run dev

# 5. Deploy
git add community_health_centers_with_coords.csv
git commit -m "Update health center data"
git push
```

**That's it!** The application will automatically use the updated data.

