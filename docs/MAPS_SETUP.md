# Maps Setup Guide

Complete guide to set up and use the Leaflet/OpenStreetMap integration for the Community Health Centers finder.

## 🚀 Quick Setup (5 Minutes)

### 1. Install Dependencies

```bash
cd frontend
npm install
```

**No API keys required!** The app uses free services:
- OpenStreetMap tiles for maps (no API key)
- Nominatim for zipcode geocoding (free, no API key, max 1 request/second)

### 2. Run Geocoding (One-Time, Optional)

If you need to geocode health center addresses, you can use the Google Maps Geocoding API script (one-time data processing):

```bash
# Install Python dependencies
pip install requests pandas

# Run geocoding script (requires Google Maps API key for one-time geocoding)
python scripts/add_geocoding.py YOUR_GOOGLE_MAPS_API_KEY
```

This creates `data/processed/community_health_centers_with_coords.csv` with coordinates.

**Note:** This is only needed if you're adding new health centers. The app itself doesn't require Google Maps API.

### 3. Start the App

```bash
cd frontend
npm run dev
```

Open http://localhost:5173 and search by zipcode!

---

## 📋 Features

### Interactive Map
- **Leaflet/OpenStreetMap Integration**: Free, open-source mapping solution
- **Custom Markers**: Click markers to see detailed information
- **Auto-Centering**: Map automatically centers on search results
- **Zoom & Pan**: Interactive map controls
- **Responsive Design**: Works on mobile, tablet, and desktop

### View Modes
- **📋 List** - Card-based list view
- **🗺️ Map** - Full interactive map
- **📍 Both** - Split view (default)

### Search
- Search by zipcode
- View services offered (Primary Care, Dental, Eye Care)
- Get contact info and directions
- 276+ health centers in Massachusetts

---

## 🔧 Detailed Setup

### Map Library: Leaflet

The app uses **Leaflet** with **react-leaflet** for React integration:

- **Leaflet**: Open-source JavaScript library for mobile-friendly interactive maps
- **react-leaflet**: React components for Leaflet
- **OpenStreetMap Tiles**: Free map tiles (no API key required)

### Geocoding: Nominatim

Zipcode geocoding uses **Nominatim** (OpenStreetMap's free geocoding service):

- **No API Key Required**: Completely free
- **Rate Limiting**: Max 1 request per second (please use responsibly)
- **User-Agent Required**: The app includes a proper User-Agent header

### Environment Variables

**None required for map display!** The app uses free services:
- OpenStreetMap tiles (no API key)
- Nominatim geocoding (no API key)

### Geocoding Script Details

The `scripts/add_geocoding.py` script (optional, for one-time data processing):
- Uses Google Maps Geocoding API to geocode health center addresses
- Validates addresses before making API calls
- Shows progress for each health center
- Skips entries without valid addresses
- Includes rate limiting (100ms between requests)
- Displays summary statistics

**Example output:**
```
🌍 Starting geocoding for 276 health centers...

[1/276] Community Health Center
  📍 Address: 130 Water Street, Fitchburg, MA, 01420
  ✅ Success: 42.583542, -71.802345

[2/276] Hospital
  ⏭️  Skipping: No valid address found

...

📊 Geocoding Summary:
  ✅ Successful: 260/276 (94.2%)
  ❌ Failed: 8/276 (2.9%)
  ⏭️  Skipped (no address): 8/276 (2.9%)
  📞 API calls made: 268 (saved 8 calls)
```

**Note:** This script is only needed when adding new health centers. The frontend app uses Nominatim for zipcode geocoding, not Google Maps.

---

## 💰 Cost Information

### Free Services

- **OpenStreetMap**: Completely free, no API key required
- **Nominatim Geocoding**: Free, no API key (please use responsibly - max 1 request/second)
- **GitHub Pages**: Free hosting for public repositories

### Optional: Google Maps Geocoding (One-Time)

If you use the `scripts/add_geocoding.py` script for one-time geocoding:
- **Free Tier**: $200/month credit (automatically applied)
- **Geocoding**: $5 per 1,000 requests
  - One-time: 276 requests = **$0.00** (within free tier)

**Note:** The frontend app itself doesn't use Google Maps, so there are no ongoing costs for map display.

---

## 🐛 Troubleshooting

### Map Not Showing

**Problem**: Gray box or map not loading

**Solutions:**
- Check browser console for errors
- Verify Leaflet CSS is loading (should be automatic)
- Check that `centers.csv` has valid latitude/longitude values
- Ensure you're running from the correct port (http://localhost:5173)
- Try clearing browser cache

### No Markers on Map

**Problem**: Map displays but no markers

**Solutions:**
- Verify `frontend/public/data/centers.csv` exists
- Check CSV has `latitude` and `longitude` columns
- Try a different zipcode with known health centers
- Check browser console for data loading errors

### Geocoding Fails (Zipcode Search)

**Problem**: Zipcode search doesn't work

**Solutions:**
- Check browser console for errors
- Verify zipcode is valid (5 digits)
- Nominatim may be rate-limited (max 1 request/second)
- Check network connectivity
- The app includes a fallback for common MA zipcodes

### Geocoding Script Fails (One-Time Processing)

**Problem**: `scripts/add_geocoding.py` errors or API failures

**Solutions:**
- Install dependencies: `pip install requests pandas`
- Verify Geocoding API is enabled in Google Cloud Console
- Check API key has correct permissions
- Verify you're in project root directory
- Check API quota hasn't been exceeded

### Build Errors

**Problem**: TypeScript or Vite errors

**Solutions:**
- Delete `node_modules`: `rm -rf node_modules && npm install`
- Clear Vite cache: `rm -rf node_modules/.vite`
- Check TypeScript version: `npm list typescript`
- Restart dev server

---

## 📁 File Structure

```
frontend/src/
├── components/
│   ├── HealthCenterMap.tsx      # Leaflet map component
│   ├── HealthCenterList.tsx     # List view component
│   └── HealthCenterDetail.tsx   # Detail modal
├── utils/
│   ├── csvLoader.ts             # CSV parsing
│   ├── geocoding.ts             # Zipcode geocoding (Nominatim)
│   └── distance.ts              # Haversine distance calculation
├── types.ts                      # TypeScript types
├── App.tsx                       # Main app component
└── main.tsx                      # Entry point
```

### Component Details

**HealthCenterMap.tsx**
- Uses `react-leaflet` with Leaflet
- OpenStreetMap tiles
- Custom markers with popups
- Auto-centering on results
- Responsive design

**geocoding.ts**
- Uses Nominatim (OpenStreetMap's geocoding service)
- Includes fallback for common MA zipcodes
- No API key required
- Rate-limited to 1 request/second

---

## 🎯 Usage

### Basic Search

1. Enter a zipcode (e.g., `02138`)
2. Select a search radius (10/25/50/100 miles)
3. Click **Search**
4. Results appear in your selected view

### View Modes

Click the buttons to toggle:
- **📋 List** - Shows list only
- **🗺️ Map** - Shows map only
- **📍 Both** - Shows both (default)

### Interacting with Results

**Map View:**
- Click markers to see popups with center information
- Zoom with mouse wheel or +/- buttons
- Pan by dragging
- Click website links to visit health centers

**List View:**
- Scroll through results
- Click website links
- View full addresses and coordinates
- See all services offered

---

## 🚀 Deployment

### No Configuration Needed!

Since the app uses free services (OpenStreetMap and Nominatim), no environment variables or API keys are needed for deployment.

### Build & Deploy

```bash
cd frontend
npm run build
```

The build output will be in `frontend/dist/` directory.

### GitHub Pages Deployment

The app is configured for GitHub Pages deployment:
- Base path is set in `vite.config.ts`
- GitHub Actions workflow handles deployment automatically
- See [docs/DEPLOYMENT.md](DEPLOYMENT.md) for details

### Checklist

- [ ] Verify `frontend/public/data/centers.csv` exists
- [ ] Test locally: `npm run dev`
- [ ] Build for production: `npm run build`
- [ ] Deploy to GitHub Pages (automatic via GitHub Actions)
- [ ] Test in production

---

## 📝 Additional Resources

- [Leaflet Documentation](https://leafletjs.com/)
- [react-leaflet Documentation](https://react-leaflet.js.org/)
- [OpenStreetMap](https://www.openstreetmap.org/)
- [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/)
- [Vite Documentation](https://vitejs.dev/)

---

## ✨ Summary

You now have:
- ✅ Interactive Leaflet maps with OpenStreetMap tiles (free, no API key)
- ✅ Multiple view modes (List/Map/Both)
- ✅ Zipcode search functionality with Nominatim geocoding (free)
- ✅ 276+ health centers with geocoded addresses
- ✅ Mobile-responsive design
- ✅ **Zero ongoing costs** for map display

**Key Benefits:**
- No API keys required for map display
- Completely free mapping solution
- Open-source and community-driven
- No usage limits (except Nominatim rate limiting: 1 req/sec)

**Need help?** Check the troubleshooting section above or open an issue on GitHub.
