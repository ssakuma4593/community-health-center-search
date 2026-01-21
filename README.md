# Community Health Center Search

**Find community health centers in Massachusetts with interactive maps**

Community Health Center Search is a comprehensive healthcare platform that helps patients locate community health centers by zipcode. The application features an interactive map with Leaflet/OpenStreetMap, showing health centers with detailed information including services offered, contact details, and locations.

## Features

### 🗺️ Interactive Map
- **Leaflet/OpenStreetMap Integration**: View health centers on an interactive map (free, no API key required)
- **Custom Markers**: Click markers to see detailed information
- **Auto-Centering**: Map automatically centers on search results
- **Distance Calculation**: Haversine formula for accurate distance calculations

### 📋 Search & Results
- **Zipcode Search**: Find health centers by zipcode with radius filtering (10/25/50/100 miles)
- **Results List**: Sorted by distance, displayed in cards
- **Detail View**: Modal with markdown rendering for patient instructions
- **Service Types**: View available services (Primary Care, Dental, Eye Care)
- **Contact Information**: Phone numbers and website links
- **Address Details**: Complete address with coordinates

### 📊 Data Coverage
- **276+ Health Centers** in Massachusetts
- **Geocoded Addresses**: Latitude/longitude for accurate mapping
- **Service Categories**: Primary Care, Dental Care, Eye Care, and more
- **Regular Updates**: Data sourced from official health center listings

## Tech Stack

### Frontend
- **Framework**: Vite + React 19
- **Language**: TypeScript
- **Maps**: Leaflet + react-leaflet (OpenStreetMap tiles)
- **Markdown**: react-markdown for patient instructions
- **CSV Parsing**: PapaParse
- **Geocoding**: Nominatim (OpenStreetMap, free, no API key)
- **Deployment**: GitHub Pages via GitHub Actions

### Data Processing
- **Document Parsing**: Python with python-docx for parsing official Word documents
- **Data Parsing**: pandas for CSV processing
- **Geocoding Script**: Automated address-to-coordinate conversion

## Project Structure

```
community-health-center-search/
├── frontend/                              # Vite + React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── HealthCenterMap.tsx       # Leaflet map component
│   │   │   ├── HealthCenterList.tsx      # Results list component
│   │   │   └── HealthCenterDetail.tsx    # Detail modal with markdown
│   │   ├── utils/
│   │   │   ├── csvLoader.ts              # CSV parsing
│   │   │   ├── geocoding.ts              # Zipcode geocoding
│   │   │   └── distance.ts               # Haversine distance
│   │   ├── types.ts                       # TypeScript types
│   │   ├── App.tsx                        # Main app component
│   │   └── main.tsx                       # Entry point
│   ├── public/
│   │   └── data/
│   │       └── centers.csv                # Health center data
│   ├── vite.config.ts                     # Vite config with base path
│   └── package.json
├── backend/                               # FastAPI backend (optional)
│   └── app/main.py
├── data/                                  # Source documents and data
│   ├── official_documents/               # Original source documents
│   ├── raw/                              # Raw/scraped CSV files
│   └── processed/                        # Processed CSV files with coordinates
├── docs/                                  # All documentation
│   ├── MAPS_SETUP.md                     # Maps setup (legacy)
│   ├── DATA_ONBOARDING.md                # Add/update health centers
│   ├── DEPLOYMENT.md                     # Deployment guide
│   ├── OPENAI_ENRICHMENT.md              # OpenAI enrichment pipeline
│   └── ROADMAP.md                        # Development roadmap
├── scripts/                               # Data processing scripts
│   ├── scrape_docx.py                    # Document parser
│   ├── add_geocoding.py                  # Geocoding script
│   ├── enrich_csv.py                     # OpenAI enrichment script
│   └── merge_enriched_data.py            # Merge enriched data
├── reports/                               # Reports and test results
│   ├── enrichment_comparison_report.txt  # Enrichment comparison report
│   └── test_enrichment_results.json      # Test enrichment results
├── .github/
│   └── workflows/
│       └── deploy-pages.yml               # GitHub Pages deployment
└── README.md                              # This file
```

## Quick Start

### Prerequisites

- **Node.js 18+** and npm
- **Python 3.8+** and pip (for data processing scripts)

### Setup (First Time)

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

**No API keys required!** The app uses free services:
- OpenStreetMap/Nominatim for geocoding (no API key)
- OpenStreetMap tiles for maps (no API key)

#### 2. Data Setup

The health center data is already included in `frontend/public/data/centers.csv`. If you need to update it:

```bash
# Copy the geocoded CSV to the frontend public directory
cp community_health_centers_with_coords.csv frontend/public/data/centers.csv
```

### Running the Application

#### Local Development

```bash
cd frontend
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

#### Build for Production

```bash
cd frontend
npm run build
```

Output will be in `frontend/dist/` directory.

#### Preview Production Build

```bash
cd frontend
npm run preview
```

### GitHub Pages Deployment

The app automatically deploys to GitHub Pages when you push to `main` or `feature/github-pages-deployment` branch.

**Deployment URL:** `https://<org>.github.io/community-health-center-search/`

**To enable:**
1. Go to repository Settings → Pages
2. Source: GitHub Actions
3. The workflow (`.github/workflows/deploy-pages.yml`) will deploy automatically

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

### Usage

1. Enter a zipcode (e.g., `02138` for Cambridge, MA)
2. Select a search radius (10/25/50/100 miles)
3. Click **Search**
4. View results:
   - **🗺️ Map** - Interactive map with markers
   - **📋 List** - Results sorted by distance
5. Click a center to see detailed information including "How to become a new patient" instructions

## Data Source

Health center data is loaded client-side from `/public/data/centers.csv`. The CSV includes:

**Required fields:**
- `name`, `street_address_1`, `city_town`, `state`, `zipcode`, `phone`
- `latitude`, `longitude` (for mapping)

**Optional fields:**
- `street_address_2`, `types`, `website`, `source`

**OpenAI enrichment fields (optional):**
- `openai_phone`, `openai_address`, `openai_new_patient_md`, `openai_other_notes_md`
- `openai_source_urls`, `openai_last_checked_utc`, `openai_confidence`

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for CSV schema details.

## Documentation

All documentation is in the [`docs/`](docs/) folder:

- **[docs/MAPS_SETUP.md](docs/MAPS_SETUP.md)** - Complete Leaflet/OpenStreetMap setup guide
- **[docs/DATA_ONBOARDING.md](docs/DATA_ONBOARDING.md)** - How to add/update health centers (includes scraper workflow)
- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Deployment guide for GitHub Pages
- **[docs/OPENAI_ENRICHMENT.md](docs/OPENAI_ENRICHMENT.md)** - OpenAI enrichment pipeline documentation
- **[docs/REPO_ORGANIZATION.md](docs/REPO_ORGANIZATION.md)** - Repository structure and organization
- **[docs/ROADMAP.md](docs/ROADMAP.md)** - Development roadmap

## 🎬 Demo Scripts

Easy-to-run demo scripts for showcasing features:

- **[scripts/demos/README.md](scripts/demos/README.md)** - Demo scripts guide
- **OpenAI Enrichment Demo:** `python scripts/demos/demo_openai_enrichment.py`
- **VAPI Call Demo:** `python scripts/demos/demo_vapi_call.py`

Perfect for presentations and testing individual features!

## Features in Detail

### Map Integration

The app uses **Leaflet** with **OpenStreetMap** tiles for a free, open-source mapping solution:

- **No API Key Required**: Uses free OpenStreetMap services
- **Interactive Map**: Zoom, pan, and explore
- **Custom Markers**: Click markers to see detailed information
- **Auto-Fit Bounds**: Map automatically adjusts to show all results
- **Responsive**: Works on mobile, tablet, and desktop

### Search & Results

**Zipcode Search**
- Enter a 5-digit zipcode
- Select search radius (10/25/50/100 miles)
- Results sorted by distance using Haversine formula

**Results List**
- Card-based layout with hover effects
- Full address and contact information
- Clickable website links
- Distance displayed for each center

**Detail View**
- Modal popup with full center information
- Markdown rendering for patient instructions
- Contact details and services offered

### Data Processing

The project uses a simple two-step pipeline to onboard health centers:

**Pipeline:** `Document Parser → Geocoding → Application`

1. **Document Parser** (`scrape_docx.py`)
   - Parses health center data from official Massachusetts Word documents
   - Extracts: name, address, phone, services, websites
   - Output: `data/raw/hsn_active_health_centers_parsed.csv` (with separate address columns)

2. **Geocoding Script** (`scripts/add_geocoding.py`)
   - Converts addresses to latitude/longitude coordinates (one-time data processing)
   - Uses Google Maps Geocoding API for batch geocoding
   - Validates addresses before making API calls (saves quota!)
   - Shows progress and statistics
   - Output: `data/processed/community_health_centers_with_coords.csv` (used by app)
   
   **Note:** The frontend app uses free Leaflet/OpenStreetMap for maps and Nominatim for zipcode geocoding (no API keys needed).

**To add new health centers:**
```bash
# 1. Parse official document
python scripts/scrape_docx.py

# 2. Add coordinates
python scripts/add_geocoding.py YOUR_GOOGLE_MAPS_API_KEY

# 3. Test
cd frontend && npm run dev
```

See [docs/DATA_ONBOARDING.md](docs/DATA_ONBOARDING.md) for complete details.

## Development

### Current Branch: `organize-repo-structure`

Repository organization improvements. Key changes:
- Organized scripts, data, and documentation into logical directories
- Merged related documentation files
- Updated all file paths and references

### Local Development

```bash
# Install dependencies
cd frontend
npm install

# Run in development mode
npm run dev

# Build for production
npm run build

# Run linting
npm run lint
```

### Environment Variables

**None required!** The app uses free services:
- OpenStreetMap/Nominatim for geocoding (no API key, max 1 request/second)
- OpenStreetMap tiles for maps (no API key)

## Cost Information

### Free Services

- **OpenStreetMap**: Completely free, no API key required
- **Nominatim Geocoding**: Free, no API key (please use responsibly - max 1 request/second)
- **GitHub Pages**: Free hosting for public repositories

No costs associated with running this application!

## Troubleshooting

### Map Not Showing
- Check browser console for errors
- Verify Leaflet CSS is loading (should be automatic)
- Check that `centers.csv` has valid latitude/longitude values

### No Results Found
- Verify zipcode is valid (5 digits)
- Try expanding the radius
- Check browser console for geocoding errors
- Verify CSV file exists at `frontend/public/data/centers.csv`

### Build Fails
- Run `npm install` in `frontend/`
- Check TypeScript errors: `npm run build`
- Verify all dependencies are installed

### GitHub Pages Not Updating
- Check GitHub Actions tab for workflow status
- Verify Pages is enabled in repository Settings → Pages
- Ensure workflow file is in `.github/workflows/deploy-pages.yml`
- Check that you're pushing to `main` or `feature/github-pages-deployment` branch

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed troubleshooting.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly (both desktop and mobile)
5. Update documentation if needed
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Guidelines

- Write TypeScript for type safety
- Use Tailwind CSS for styling
- Follow React best practices
- Add tests for new features
- Update documentation
- Keep commits focused and descriptive

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Health center data sourced from official Massachusetts health department listings
- OpenStreetMap for free mapping tiles and geocoding services
- Leaflet and react-leaflet for excellent mapping libraries
- Vite and React teams for excellent frameworks

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check documentation files for common solutions
- Review troubleshooting sections in guides

---

**Need help getting started?** See [docs/MAPS_SETUP.md](docs/MAPS_SETUP.md) for the complete setup guide!
