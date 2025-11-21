# Archive Directory

This directory contains archived CSV files and Python scripts that are no longer actively used in the project.

## Archived CSV Files

### `community_health_centers_final.csv`
- **Date Archived**: November 21, 2024
- **Reason**: Replaced by `community_health_centers_scraped_fresh.csv` (newer, more up-to-date data)
- **Original Date**: October 24, 2024
- **Rows**: 274

### `community_health_centers_parsed.csv`
- **Date Archived**: November 21, 2024
- **Reason**: Replaced by `community_health_centers_with_coords.csv` (production file with geocoding)
- **Original Date**: November 6, 2024
- **Rows**: 274
- **Note**: This was used as a fallback by the API, but `with_coords.csv` is the primary file now

## Archived Python Scripts

### `final_merge_script.py`
- **Date Archived**: November 21, 2024
- **Reason**: Obsolete - references non-existent files (`community_health_centers_targeted.csv`)
- **Replaced by**: Current scraper workflow

### `final_document_parser.py`
- **Date Archived**: November 21, 2024
- **Reason**: Obsolete - replaced by `scrape_docx.py` (simpler, newer)
- **Replaced by**: `scrape_docx.py`

### `parse_and_compare_new_document.py`
- **Date Archived**: November 21, 2024
- **Reason**: Obsolete - uses obsolete scripts and references archived CSV files
- **Dependencies**: `final_document_parser.py` (obsolete), `compare_health_centers.py` (obsolete)

### `compare_health_centers.py`
- **Date Archived**: November 21, 2024
- **Reason**: Obsolete - replaced by `compare_csvs.py` (simpler, address-based comparison)
- **Replaced by**: `compare_csvs.py`

## Current Active Files

The following files remain in the root directory and are actively used:

### CSV Files:
1. **`community_health_centers_scraped_fresh.csv`** - Latest scraped data (123 rows)
2. **`hsn_active_health_centers_scraped.csv`** - DOCX scraped data (111 rows)
3. **`community_health_centers_with_coords.csv`** - Production file with geocoding (273 rows)

### Python Scripts:
1. **`community_health_scraper.py`** - Main web scraper
2. **`scrape_docx.py`** - DOCX file scraper
3. **`compare_csvs.py`** - CSV comparison tool
4. **`add_geocoding.py`** - Geocoding script (generates production file)
5. **`run_scraper.py`** - Scraper wrapper

