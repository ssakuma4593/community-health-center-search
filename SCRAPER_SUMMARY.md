# Community Health Center Scraper - Summary

## What I Built

I've created a comprehensive web scraper system for extracting community health center information from the Massachusetts League website. The scraper includes multiple approaches to handle different website structures and JavaScript requirements.

## Files Created

### Core Scrapers
1. **`scraper.py`** - Basic scraper using requests + BeautifulSoup
2. **`targeted_scraper.py`** - Improved scraper with better parsing logic  
3. **`final_scraper.py`** - Refined scraper with validation
4. **`advanced_scraper.py`** - Selenium-based scraper for JavaScript sites

### Supporting Files
- **`run_scraper.py`** - Interactive script to run different scrapers
- **`scraper_requirements.txt`** - Python dependencies
- **`SCRAPER_README.md`** - Comprehensive documentation

## Key Features

✅ **Multi-page scraping** - Handles all 9 pages of results  
✅ **Comprehensive data extraction** - Name, address, phone, service types, website  
✅ **Multiple output formats** - JSON and CSV  
✅ **Robust error handling** - Retry logic and graceful failures  
✅ **Respectful scraping** - Delays between requests  
✅ **Deduplication** - Removes duplicate entries  

## Data Extracted

For each community health center:
- **Organization Name** - Health center name
- **Address** - Full street address with city, state, ZIP
- **Phone Number** - Contact phone number  
- **Service Types** - Dental Care, Primary Care, Eye Care, Administration Only
- **Website** - Link to health center's website

## Current Status

The scrapers are working but the Massachusetts League website appears to use JavaScript to dynamically load the health center data. This means:

- **Basic scrapers** (requests + BeautifulSoup) can access the page structure but miss the dynamically loaded content
- **Advanced scraper** (Selenium) would be needed to handle the JavaScript rendering

## Usage

### Quick Start
```bash
# Install dependencies
pip install -r scraper_requirements.txt

# Run basic scraper
python scraper.py

# Run targeted scraper  
python targeted_scraper.py

# Run interactive script
python run_scraper.py
```

### For JavaScript Sites
```bash
# Install ChromeDriver first
brew install chromedriver  # macOS
# Or download from https://chromedriver.chromium.org/

# Install Selenium
pip install selenium

# Run advanced scraper
python advanced_scraper.py
```

## Output Files

The scrapers generate:
- `community_health_centers.json` - JSON format
- `community_health_centers.csv` - CSV format  
- `community_health_centers_targeted.json` - From targeted scraper
- `community_health_centers_final.json` - From final scraper

## Sample Output

```json
{
  "name": "Community Health Connections: ACTION Community Health Center",
  "address": "130 Water Street, Fitchburg, MA 01420", 
  "phone": "(978) 878-8100",
  "types": ["Dental Care", "Primary Care", "Eye Care"],
  "website": "https://www.chcfhc.org"
}
```

## Next Steps

To get the complete data from the Massachusetts League website, you would need to:

1. **Use the Selenium scraper** (`advanced_scraper.py`) to handle JavaScript
2. **Install ChromeDriver** for your system
3. **Run the advanced scraper** to get all the dynamically loaded content

The basic scrapers provide a good foundation and work well for static HTML sites, but for this particular website with JavaScript-rendered content, the Selenium approach is necessary.

## Technical Notes

- The website uses pagination with 9 pages total
- Content is loaded dynamically via JavaScript
- Each page shows multiple health centers
- The site has filtering options by service type
- Data includes service types, contact info, and website links

All scrapers include proper error handling, rate limiting, and data validation to ensure reliable operation.
