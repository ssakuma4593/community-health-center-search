# Community Health Center Scraper

A production-ready web scraper for extracting community health center information from the Massachusetts League of Community Health Centers website.

## Features

- **JavaScript-aware scraping**: Uses Selenium to handle dynamically loaded content
- **Automatic pagination**: Clicks through all 9 pages automatically
- **High data quality**: Extracts ~123 community health centers with complete information
- **Targeted structure parsing**: Specifically targets the wpgb-card HTML structure
- **Multiple output formats**: Saves data in both JSON and CSV formats
- **Robust error handling**: Includes retry logic and graceful error handling

## Data Extracted

For each community health center, the scraper extracts:

- **Organization Name**: The name of the health center
- **Address**: Full street address including city, state, and ZIP code
- **Phone Number**: Contact phone number
- **Service Types**: Types of services offered (Dental Care, Primary Care, Eye Care, Administration Only)
- **Website**: Link to the health center's website

## Files

- `community_health_scraper.py` - Production-ready scraper with Selenium
- `run_scraper.py` - Simple script to run the scraper
- `scraper_requirements.txt` - Python dependencies

## Installation

1. Install Python dependencies:
```bash
pip install -r scraper_requirements.txt
```

2. For the advanced scraper (Selenium), you'll also need ChromeDriver:
```bash
# On macOS with Homebrew
brew install chromedriver

# Or download from https://chromedriver.chromium.org/
```

## Usage

### Basic Usage

Run the scraper:
```bash
python run_scraper.py
```

Or run the scraper directly:
```bash
python community_health_scraper.py
```

## Output Files

The scraper generates the following files:

- `community_health_centers_targeted.json` - JSON format with all extracted data
- `community_health_centers_targeted.csv` - CSV format for easy import into spreadsheets

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

## Scraper Features

### Production-Ready Scraper (`community_health_scraper.py`)
- **JavaScript-aware**: Uses Selenium WebDriver to handle dynamic content
- **Automatic pagination**: Clicks through all 9 pages automatically
- **Targeted parsing**: Specifically targets the wpgb-card HTML structure
- **High data quality**: Extracts ~123 community health centers with complete information
- **Comprehensive coverage**: Handles all service types and locations
- **Requires ChromeDriver**: Install with `brew install chromedriver`

## Troubleshooting

### Common Issues

1. **No data extracted**: The website structure may have changed. Try the targeted scraper or check if the site requires JavaScript.

2. **Duplicate entries**: The scraper includes deduplication logic, but some duplicates may still appear if the data is slightly different.

3. **Missing data**: Some fields may be empty if the information isn't available on the website.

4. **ChromeDriver errors**: For the advanced scraper, ensure ChromeDriver is installed and in your PATH.

### Rate Limiting

The scraper includes delays between requests to be respectful to the server. If you encounter rate limiting:

- Increase the delay between requests
- Use fewer concurrent requests
- Consider running during off-peak hours

## Legal and Ethical Considerations

- This scraper is for educational and research purposes
- Always respect the website's robots.txt file
- Don't overload the server with too many requests
- Consider reaching out to the organization for bulk data if available
- Ensure compliance with the website's terms of service

## Contributing

To improve the scraper:

1. Test with different websites
2. Add support for new data fields
3. Improve error handling
4. Add new output formats
5. Optimize performance

## License

This scraper is provided as-is for educational purposes. Please use responsibly and in accordance with the target website's terms of service.
