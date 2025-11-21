# Community Health Center Search

**Find community health centers in Massachusetts with interactive maps**

Community Health Center Search is a comprehensive healthcare platform that helps patients locate community health centers by zipcode. The application features an interactive Google Maps integration, showing health centers with detailed information including services offered, contact details, and locations.

![Community Health Center Search Interface](https://github.com/user-attachments/assets/d9f4fe37-3eb2-4937-ae07-cec0ccafa356)

## Features

### 🗺️ Interactive Map
- **Google Maps Integration**: View health centers on an interactive map
- **Custom Markers**: Click markers to see detailed information
- **Auto-Centering**: Map automatically centers on search results
- **Info Windows**: Detailed health center information in popups

### 📋 Multiple View Modes
- **List View**: Traditional card-based list with full details
- **Map View**: Full-screen interactive map
- **Both View**: Split view showing both list and map (default)

### 🔍 Search & Filter
- **Zipcode Search**: Find health centers in specific zipcodes
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
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Maps**: @vis.gl/react-google-maps
- **UI**: React 19 with modern hooks

### Backend
- **API**: FastAPI (Python)
- **Data Source**: CSV files with geocoded addresses
- **Geocoding**: Google Maps Geocoding API

### Data Processing
- **Web Scraping**: Python with Selenium, BeautifulSoup
- **Data Parsing**: pandas for CSV processing
- **Geocoding Script**: Automated address-to-coordinate conversion

## Project Structure

```
community-health-center-search/
├── frontend/                              # Next.js application
│   ├── src/app/
│   │   ├── components/
│   │   │   ├── HealthCenterMap.tsx       # Interactive map component
│   │   │   ├── HealthCenterList.tsx      # List view component
│   │   │   └── Navigation.tsx            # Navigation bar
│   │   ├── api/health-centers/
│   │   │   └── route.ts                  # API endpoint for health centers
│   │   └── page.tsx                      # Main search page
│   ├── package.json
│   └── .env.local                         # Google Maps API key (create this)
├── backend/                               # FastAPI backend
│   └── app/main.py
├── data/                                  # Source documents and data
├── docs/                                  # All documentation
│   ├── MAPS_SETUP.md                     # Google Maps setup
│   ├── DATA_ONBOARDING.md                # Add/update health centers
│   └── ROADMAP.md                        # Development roadmap
├── community_health_centers_final.csv     # Scraped data
├── community_health_centers_with_coords.csv  # Geocoded data (used by app)
├── community_health_scraper.py            # Web scraper
├── add_geocoding.py                       # Geocoding script
└── README.md                              # This file
```

## Quick Start

### Prerequisites

- **Node.js 18+** and npm
- **Python 3.8+** and pip
- **Google Maps API Key** (see setup guide below)

### Setup (First Time)

#### 1. Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable:
   - Maps JavaScript API
   - Geocoding API
3. Create an API key under Credentials

#### 2. Configure Environment

```bash
cd frontend
echo "NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_api_key_here" > .env.local
```

Replace `your_api_key_here` with your actual API key.

#### 3. Add Geocoding (One-Time)

If `community_health_centers_with_coords.csv` doesn't exist:

```bash
# Install dependencies
pip install requests pandas

# Run geocoding script
python add_geocoding.py YOUR_GOOGLE_MAPS_API_KEY
```

This converts addresses to coordinates for map display.

### Running the Application

#### Option 1: Frontend Only (Recommended)

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

#### Option 2: Full Stack

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Usage

1. Enter a zipcode (e.g., `02138` for Cambridge, MA)
2. Click **Search Health Centers**
3. Toggle between views:
   - **📋 List** - Card-based list view
   - **🗺️ Map** - Interactive map view
   - **📍 Both** - Split view (default)
4. Click markers or list items for details

## API Endpoints

### Frontend API Routes

- `GET /api/health` - Health check endpoint
- `GET /api/health-centers?zipcode=XXXXX` - Search health centers by zipcode
  - Returns: Array of health centers with coordinates
  - Example response:
    ```json
    [
      {
        "name": "Community Health Center",
        "street_address_1": "123 Main St",
        "city_town": "Boston",
        "state": "MA",
        "zipcode": "02118",
        "phone": "(617) 555-0100",
        "types": "Primary Care, Dental Care",
        "website": "https://example.com",
        "latitude": 42.3601,
        "longitude": -71.0589
      }
    ]
    ```

### Backend (FastAPI) - Optional

- `GET /` - Health check endpoint

## Example API Usage

Search for health centers in Cambridge:

```bash
curl "http://localhost:3000/api/health-centers?zipcode=02138"
```

Search for health centers in Boston:

```bash
curl "http://localhost:3000/api/health-centers?zipcode=02118"
```

## Documentation

All documentation is in the [`docs/`](docs/) folder:

- **[docs/MAPS_SETUP.md](docs/MAPS_SETUP.md)** - Complete Google Maps setup guide
- **[docs/DATA_ONBOARDING.md](docs/DATA_ONBOARDING.md)** - How to add/update health centers (includes scraper workflow)
- **[docs/ROADMAP.md](docs/ROADMAP.md)** - Development roadmap

## Features in Detail

### Google Maps Integration

The app uses `@vis.gl/react-google-maps` for a modern, React-friendly maps experience:

- **Dynamic Loading**: Map loads only when needed (performance optimization)
- **Custom Markers**: Blue pins with white icons for health centers
- **Info Windows**: Click markers to see detailed information
- **Responsive**: Works on mobile, tablet, and desktop
- **Auto-Fit Bounds**: Map automatically adjusts to show all results

### View Modes

**List View**
- Card-based layout with hover effects
- Full address and contact information
- Clickable website links
- Shows coordinates when available

**Map View**
- Full-screen interactive Google Map
- Zoom, pan, and explore
- Marker clustering for better performance (coming soon)
- Street view integration (planned)

**Both View (Default)**
- Map displayed at the top
- List shown below
- Synchronized data between views
- Best of both worlds

### Data Processing

The project uses a simple two-step pipeline to onboard health centers:

**Pipeline:** `Scraper → Geocoding → Application`

1. **Web Scraper** (`community_health_scraper.py`)
   - Scrapes health center data from official Massachusetts sources
   - Extracts: name, address, phone, services, websites
   - Output: `community_health_centers_final.csv`

2. **Geocoding Script** (`add_geocoding.py`)
   - Converts addresses to latitude/longitude coordinates
   - Validates addresses before making API calls (saves quota!)
   - Shows progress and statistics
   - Output: `community_health_centers_with_coords.csv` (used by app)

**To add new health centers:**
```bash
# 1. Run scraper
python community_health_scraper.py

# 2. Add coordinates
python add_geocoding.py YOUR_GOOGLE_MAPS_API_KEY

# 3. Test
cd frontend && npm run dev
```

See [docs/DATA_ONBOARDING.md](docs/DATA_ONBOARDING.md) for complete details.

## Development

### Current Branch: `feature/google-maps-integration`

All Google Maps features are in this branch. Key changes:
- Added interactive map component
- Created list view component
- Implemented view mode toggle
- Added geocoding script
- Comprehensive documentation

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

Create `frontend/.env.local`:
```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_api_key_here
```

**Important**: Never commit `.env.local` to version control.

## Cost Information

### Google Maps API Pricing

- **Free Tier**: $200/month credit
- **Geocoding**: $5 per 1,000 requests (one-time: 276 requests = FREE)
- **Map Loads**: $7 per 1,000 loads
- **Break-even**: ~28,000 map loads/month

For typical usage, the app stays within the free tier.

### Monitoring Usage

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services** → **Dashboard**
3. View usage statistics
4. Set up billing alerts

## Troubleshooting

### Map Not Showing
- Verify `.env.local` exists with correct API key
- Restart dev server after adding environment variable
- Check browser console for errors

### No Markers on Map
- Run geocoding script: `python add_geocoding.py YOUR_API_KEY`
- Verify `community_health_centers_with_coords.csv` exists
- Check that CSV has latitude/longitude columns

### Geocoding Script Issues
- Install dependencies: `pip install requests pandas`
- Verify Geocoding API is enabled in Google Cloud
- Check API key permissions

See [docs/MAPS_SETUP.md](docs/MAPS_SETUP.md) for detailed troubleshooting.

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
- Google Maps Platform for mapping services
- @vis.gl/react-google-maps for React integration
- Next.js and React teams for excellent frameworks

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check documentation files for common solutions
- Review troubleshooting sections in guides

---

**Need help getting started?** See [docs/MAPS_SETUP.md](docs/MAPS_SETUP.md) for the complete setup guide!
