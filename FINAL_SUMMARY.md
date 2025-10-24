# Community Health Centers - Final Dataset

## Overview
This project combines data from two sources to create a comprehensive database of Massachusetts community health centers and hospitals.

## Final Files

### Core Data Files
- **`community_health_centers_final.csv`** - Complete merged dataset (274 centers)
- **`community_health_centers_final.json`** - Same data in JSON format

### Parser Scripts
- **`final_document_parser.py`** - Table-aware parser for Word documents
- **`final_merge_script.py`** - Script to merge document data with existing CSV
- **`community_health_scraper.py`** - Web scraper for massleague.org
- **`run_scraper.py`** - Main script to run the web scraper

### Data Sources
- **Web Scraper**: 123 centers from massleague.org
- **Official Documents**: 151 centers from MA Health Safety Net documents
- **Total**: 274 unique health centers and hospitals

## Data Structure
Each record contains:
- **name**: Organization name
- **address**: Full address (street, city, state, zip)
- **phone**: Contact phone number
- **types**: Service types (Primary Care, Dental Care, etc.)
- **website**: Organization website
- **source**: Data source (web_scraper or official_document)

## Usage

### To re-run the web scraper:
```bash
python run_scraper.py
```

### To parse new official documents:
1. Place Word documents in `data/official_documents/`
2. Run: `python final_merge_script.py`

### To parse documents only:
```bash
python final_document_parser.py
```

## Directory Structure
```
├── community_health_centers_final.csv      # Final merged dataset
├── community_health_centers_final.json     # JSON format
├── final_document_parser.py                 # Document parser
├── final_merge_script.py                   # Merge script
├── community_health_scraper.py              # Web scraper
├── run_scraper.py                          # Main runner
└── data/
    ├── official_documents/                 # Place Word docs here
    │   ├── hsn-active-health-center-listings.docx
    │   └── hsn-active-hospital-listing.docx
    └── README.md
```

## Key Features
- ✅ **Proper Address Format**: "Street Address, City, MA Zip Code"
- ✅ **Duplicate Prevention**: Checks for existing addresses
- ✅ **Table-Aware Parsing**: Handles Word document table structure
- ✅ **Comprehensive Coverage**: 274 total health centers
- ✅ **Multiple Formats**: CSV and JSON output
- ✅ **Clean Codebase**: Only essential files remain
