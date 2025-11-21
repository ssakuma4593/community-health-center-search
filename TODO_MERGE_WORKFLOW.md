# TODO: Merge Workflow Implementation

This document outlines the desired workflow for merging data from multiple sources and generating the final production CSV file.

## 🎯 Desired Workflow

```
1. Scrape Mass League Website
   ↓
   community_health_centers_scraped_fresh.csv
   
2. Scrape DOCX File
   ↓
   hsn_active_health_centers_scraped.csv
   
3. Merge Script (TO BE CREATED)
   ↓
   community_health_centers_merged.csv
   
4. Add Geocoding
   ↓
   community_health_centers_with_coords.csv (PRODUCTION FILE)
```

## 📋 Step-by-Step Workflow

### Step 1: Scrape Mass League Website ✅ **DONE**
- **Script**: `community_health_scraper.py` or `run_scraper.py`
- **Output**: `community_health_centers_scraped_fresh.csv`
- **Status**: ✅ Working - generates 123 rows
- **Command**: `python3 run_scraper.py` or `python3 community_health_scraper.py`

### Step 2: Scrape DOCX File ✅ **DONE**
- **Script**: `scrape_docx.py`
- **Input**: `data/official_documents/hsn-active-health-center-listings.docx`
- **Output**: `hsn_active_health_centers_scraped.csv`
- **Status**: ✅ Working - generates 111 rows
- **Command**: `python3 scrape_docx.py`

### Step 3: Merge Script ⚠️ **TO BE CREATED**
- **Script Name**: `merge_health_centers.py` (or similar)
- **Input Files**:
  - `community_health_centers_scraped_fresh.csv` (123 rows)
  - `hsn_active_health_centers_scraped.csv` (111 rows)
- **Output**: `community_health_centers_merged.csv`
- **Status**: ❌ **NOT IMPLEMENTED YET**

#### Merge Script Requirements:
1. **Load both CSV files**
2. **Deduplicate by address** (same logic as `compare_csvs.py` uses)
   - Normalize addresses (same normalization function)
   - If same address exists in both, keep the one with more complete data
3. **Merge unique entries**
   - Centers only in scraped_fresh.csv → add to merged
   - Centers only in DOCX scraped.csv → add to merged
   - Centers in both → merge data (prefer non-empty fields)
4. **Output format**: **MUST match the format expected by `add_geocoding.py`**
   - **Required fields**: `street_address_1`, `street_address_2`, `city_town`, `state`, `zipcode`
   - Current CSVs have full `address` field - need to parse/split it
   - Also need: `name`, `phone`, `types`, `website`, `source`
   - See `add_geocoding.py` lines 118-125 for expected format
5. **Handle data quality**:
   - Prefer data from source with more complete fields
   - Merge types/services if different
   - Keep best phone number/website if different
6. **Address Parsing**: 
   - Both input CSVs have full address strings (e.g., "123 Main St, Boston, MA 02101")
   - Need to parse into: `street_address_1`, `city_town`, `state`, `zipcode`
   - Can use regex or address parsing library

#### Reference:
- Look at `archive/final_merge_script.py` for inspiration (but it's obsolete)
- Use address normalization from `compare_csvs.py` (already working)
- Check `add_geocoding.py` to see what input format it expects

### Step 4: Add Geocoding ✅ **DONE**
- **Script**: `add_geocoding.py`
- **Input**: `community_health_centers_merged.csv` (from Step 3)
- **Output**: `community_health_centers_with_coords.csv` (PRODUCTION FILE)
- **Status**: ✅ Working - but needs to be updated to use merged CSV
- **Command**: `python3 add_geocoding.py YOUR_GOOGLE_MAPS_API_KEY`

## 🔧 Implementation Notes

### Current State:
- ✅ Step 1: Working (`community_health_scraper.py`)
- ✅ Step 2: Working (`scrape_docx.py`)
- ❌ Step 3: **NEEDS TO BE CREATED**
- ✅ Step 4: Working (`add_geocoding.py`) but needs to be updated to use merged CSV

### What Needs to Be Done:

1. **Create `merge_health_centers.py` script**:
   - [ ] Load `community_health_centers_scraped_fresh.csv`
   - [ ] Load `hsn_active_health_centers_scraped.csv`
   - [ ] Implement address-based deduplication (reuse logic from `compare_csvs.py`)
   - [ ] Merge entries intelligently (prefer complete data)
   - [ ] Output in format compatible with `add_geocoding.py`
   - [ ] Handle edge cases (missing fields, different formats)

2. **Update `add_geocoding.py`**:
   - [ ] Change default input from `community_health_centers_parsed.csv` to `community_health_centers_merged.csv`
   - [ ] Or make it configurable via command-line argument

3. **Create master script (optional)**:
   - [ ] `run_full_pipeline.py` that runs all 4 steps in sequence
   - [ ] Or document the manual workflow clearly

## 📊 Expected Results

### Before Merge:
- `community_health_centers_scraped_fresh.csv`: 123 rows
- `hsn_active_health_centers_scraped.csv`: 111 rows
- Overlap: ~42 addresses (from comparison results)

### After Merge:
- `community_health_centers_merged.csv`: ~150-190 rows (estimated)
  - 123 from scraped_fresh
  - ~27-67 unique from DOCX (111 - 42 overlap = 69, but some may be duplicates)

### After Geocoding:
- `community_health_centers_with_coords.csv`: Same count as merged, with lat/lng added

## 🔍 Key Considerations

1. **Address Normalization**: Use the same normalization logic as `compare_csvs.py` to ensure proper deduplication
2. **Data Quality**: When merging duplicate addresses, prefer:
   - More complete data (more fields filled)
   - More recent source (scraped_fresh might be more up-to-date)
   - Combine types/services if they differ
3. **Format Compatibility**: **CRITICAL** - Ensure merged CSV format matches what `add_geocoding.py` expects
   - **Required format**: Split address fields (`street_address_1`, `street_address_2`, `city_town`, `state`, `zipcode`)
   - **Current format**: Both input CSVs have full `address` string (e.g., "123 Main St, Boston, MA 02101")
   - **Solution**: Parse full address into components using regex or address parsing library
   - See `archive/community_health_centers_parsed.csv` for example of split format
4. **Source Tracking**: Consider adding a `source` field that indicates which source(s) contributed to each entry
5. **Address Parsing Challenge**: 
   - Input: `"130 Water Street, Fitchburg, MA 01420"`
   - Output needed: 
     - `street_address_1`: "130 Water Street"
     - `city_town`: "Fitchburg"
     - `state`: "MA"
     - `zipcode`: "01420"
   - May need regex pattern: `^(.+?),\s*(.+?),\s*([A-Z]{2})\s+(\d{5})$`

## 📝 Example Merge Logic

```python
# Pseudo-code for merge logic
for center in scraped_fresh:
    normalized_addr = normalize_address(center['address'])
    if normalized_addr in merged_set:
        # Merge with existing entry
        existing = merged_set[normalized_addr]
        merged = merge_entries(existing, center)  # Prefer complete data
    else:
        # New entry
        merged_set[normalized_addr] = center

for center in docx_scraped:
    normalized_addr = normalize_address(center['address'])
    if normalized_addr in merged_set:
        # Merge with existing entry
        existing = merged_set[normalized_addr]
        merged = merge_entries(existing, center)  # Prefer complete data
    else:
        # New entry
        merged_set[normalized_addr] = center
```

## 🚀 When Ready to Implement

1. **Review existing code**:
   - Use address normalization from `compare_csvs.py` (already working)
   - Review `archive/final_merge_script.py` for merge logic inspiration (but it's obsolete)
   - Check `archive/community_health_centers_parsed.csv` for split address format example
   - Review `add_geocoding.py` to understand expected input format (lines 118-125)

2. **Create merge script** (`merge_health_centers.py`):
   - Load both CSV files
   - Implement address parsing (full address → split components)
   - Implement address normalization for deduplication
   - Merge entries intelligently
   - Output in format: `name, street_address_1, street_address_2, city_town, state, zipcode, phone, types, website, source`

3. **Update geocoding script**:
   - Change default input in `add_geocoding.py` from `community_health_centers_parsed.csv` to `community_health_centers_merged.csv`
   - Or add command-line argument for input file

4. **Test pipeline**:
   - Test merge script with current CSV files
   - Verify output format matches `add_geocoding.py` expectations
   - Test full pipeline end-to-end
   - Verify final `with_coords.csv` works with frontend

## 📚 Related Files

- **Comparison Script**: `compare_csvs.py` - Shows how to normalize addresses and compare
- **Geocoding Script**: `add_geocoding.py` - Shows expected input format
- **Archived Reference**: `archive/final_merge_script.py` - Old merge logic (for reference only)
- **Input CSVs**: 
  - `community_health_centers_scraped_fresh.csv`
  - `hsn_active_health_centers_scraped.csv`
- **Output CSV**: `community_health_centers_merged.csv` (to be created)
- **Final Output**: `community_health_centers_with_coords.csv` (production file)

