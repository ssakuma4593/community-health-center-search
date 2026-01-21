# Repository Organization

This document describes the organization of files and directories in this repository.

## Directory Structure

```
community-health-center-search/
├── backend/                    # FastAPI backend application
│   ├── app/                   # Application code
│   └── requirements.txt        # Python dependencies
├── data/                      # Data files
│   ├── official_documents/   # Original source documents (Word files)
│   ├── raw/                   # Raw/scraped CSV files
│   │   └── hsn_active_health_centers_parsed.csv
│   └── processed/             # Processed CSV files with coordinates
│       ├── community_health_centers_with_coords.csv
│       └── community_health_centers_with_coords_backup_before_merge.csv
├── docs/                      # Documentation
│   ├── DATA_ONBOARDING.md    # How to add/update health centers
│   ├── DEPLOYMENT.md         # Deployment guide (merged from DEPLOYMENT.md + README_GITHUB_PAGES.md)
│   ├── MAPS_SETUP.md         # Maps setup guide
│   ├── OPENAI_ENRICHMENT.md  # OpenAI enrichment pipeline (merged from IMPLEMENTATION_SUMMARY.md + OPENAI_ENRICHMENT.md)
│   ├── REPO_ORGANIZATION.md  # This file
│   └── ROADMAP.md            # Development roadmap
├── frontend/                  # Vite + React frontend application
│   ├── src/                  # Source code
│   ├── public/               # Public assets
│   └── package.json          # Node.js dependencies
├── reports/                   # Reports and test results
│   ├── enrichment_comparison_report.txt
│   └── test_enrichment_results.json
├── scripts/                   # Data processing scripts
│   ├── add_geocoding.py      # Geocoding script
│   ├── enrich_csv.py         # OpenAI enrichment script
│   ├── merge_enriched_data.py # Merge enriched data
│   ├── scrape_docx.py        # Document parser
│   ├── test_enrichment.py    # Test enrichment script
│   └── scraper_requirements.txt # Python dependencies for scripts
└── README.md                  # Main project README
```

## File Organization Principles

### Scripts (`scripts/`)
All Python scripts for data processing are located in the `scripts/` directory:
- **Document parsing**: `scrape_docx.py` - Parses official Word documents
- **Geocoding**: `add_geocoding.py` - Adds coordinates to addresses
- **Enrichment**: `enrich_csv.py` - Enriches data using OpenAI API
- **Merging**: `merge_enriched_data.py` - Merges enriched data back
- **Testing**: `test_enrichment.py` - Tests enrichment functionality

### Data Files (`data/`)
Data files are organized by processing stage:
- **`data/official_documents/`**: Original source documents (Word files, etc.)
- **`data/raw/`**: Raw/scraped CSV files before processing
- **`data/processed/`**: Processed CSV files with coordinates and enrichment

### Documentation (`docs/`)
All documentation is centralized in the `docs/` directory:
- Setup and configuration guides
- Deployment instructions
- Data onboarding procedures
- API documentation

### Reports (`reports/`)
Generated reports and test results:
- Comparison reports from enrichment processes
- Test results in JSON format

## Migration Notes

### Moved Files

**Scripts:**
- `add_geocoding.py` → `scripts/add_geocoding.py`
- `enrich_csv.py` → `scripts/enrich_csv.py`
- `merge_enriched_data.py` → `scripts/merge_enriched_data.py`
- `scrape_docx.py` → `scripts/scrape_docx.py`
- `test_enrichment.py` → `scripts/test_enrichment.py`
- `scraper_requirements.txt` → `scripts/scraper_requirements.txt`

**Data Files:**
- `community_health_centers_with_coords.csv` → `data/processed/community_health_centers_with_coords.csv`
- `community_health_centers_with_coords_backup_before_merge.csv` → `data/processed/community_health_centers_with_coords_backup_before_merge.csv`
- `hsn_active_health_centers_parsed.csv` → `data/raw/hsn_active_health_centers_parsed.csv`

**Reports:**
- `enrichment_comparison_report.txt` → `reports/enrichment_comparison_report.txt`
- `test_enrichment_results.json` → `reports/test_enrichment_results.json`

**Documentation:**
- `DEPLOYMENT.md` + `README_GITHUB_PAGES.md` → `docs/DEPLOYMENT.md` (merged)
- `IMPLEMENTATION_SUMMARY.md` + `OPENAI_ENRICHMENT.md` → `docs/OPENAI_ENRICHMENT.md` (merged)

### Updated References

All scripts have been updated to use the new file paths:
- Scripts now reference `data/processed/` and `data/raw/` directories
- Reports are written to `reports/` directory
- Documentation references have been updated throughout

## Usage

When running scripts, make sure to:
1. Run from the project root directory
2. Use the new paths: `python scripts/script_name.py`
3. Reference data files using the new directory structure

Example:
```bash
# Parse document
python scripts/scrape_docx.py

# Add geocoding
python scripts/add_geocoding.py YOUR_API_KEY

# Enrich data
python scripts/enrich_csv.py
```

## Benefits

This organization provides:
- **Clear separation** of concerns (scripts, data, docs, reports)
- **Easier navigation** with logical grouping
- **Better maintainability** with centralized documentation
- **Scalability** for adding new scripts and data files
- **Consistency** across the project structure
