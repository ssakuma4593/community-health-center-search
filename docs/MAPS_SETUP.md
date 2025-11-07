# Google Maps Setup Guide

Complete guide to set up and use the Google Maps integration for the Community Health Centers finder.

## 🚀 Quick Setup (5 Minutes)

### 1. Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable these APIs:
   - **Maps JavaScript API**
   - **Geocoding API**
4. Go to **Credentials** → **Create Credentials** → **API Key**
5. Copy your API key

### 2. Add API Key to Frontend

```bash
cd frontend
echo "NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_api_key_here" > .env.local
```

Replace `your_api_key_here` with your actual API key.

### 3. Run Geocoding (One-Time)

```bash
# Install Python dependencies
pip install requests pandas

# Run geocoding script
python add_geocoding.py YOUR_API_KEY
```

This creates `community_health_centers_with_coords.csv` with coordinates.

### 4. Start the App

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 and search by zipcode!

---

## 📋 Features

### Interactive Map
- Custom markers for each health center
- Click markers to see details
- Auto-centers on search results
- Zoom, pan, and explore

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

### API Key Security (Recommended)

1. In Google Cloud Console, click your API key to edit
2. Under **Application restrictions**, select **HTTP referrers**
3. Add your domains:
   ```
   localhost:3000/*
   yourdomain.com/*
   ```
4. Under **API restrictions**, select **Restrict key**
5. Choose only:
   - Maps JavaScript API
   - Geocoding API
6. Click **Save**

### Environment Variables

Create `frontend/.env.local`:
```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_api_key_here
```

**Important:**
- Must start with `NEXT_PUBLIC_` for client-side access
- Never commit `.env.local` to version control
- Restart dev server after creating this file

### Geocoding Script Details

The `add_geocoding.py` script:
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

---

## 💰 Cost Information

### Google Maps Pricing

- **Free Tier**: $200/month credit (automatically applied)
- **Geocoding**: $5 per 1,000 requests
  - One-time: 276 requests = **$0.00**
- **Map Loads**: $7 per 1,000 loads
  - Typical usage: **$0.00** (within free tier)
  - Break-even: ~28,000 map loads/month

### Monitoring Usage

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services** → **Dashboard**
3. View usage statistics
4. Set up billing alerts to avoid surprises

---

## 🐛 Troubleshooting

### Map Not Showing

**Problem**: Gray box or "API Key Required" message

**Solutions:**
- Check that `frontend/.env.local` exists
- Verify API key is correct (no extra spaces)
- Ensure key starts with `NEXT_PUBLIC_`
- Restart dev server: `Ctrl+C` then `npm run dev`
- Check browser console for errors

### No Markers on Map

**Problem**: Map displays but no markers

**Solutions:**
- Run geocoding script: `python add_geocoding.py YOUR_API_KEY`
- Verify `community_health_centers_with_coords.csv` exists
- Check CSV has `latitude` and `longitude` columns
- Try a different zipcode with known health centers

### Geocoding Script Fails

**Problem**: Script errors or API failures

**Solutions:**
- Install dependencies: `pip install requests pandas`
- Verify Geocoding API is enabled in Google Cloud Console
- Check API key has correct permissions
- Verify you're in project root directory
- Check API quota hasn't been exceeded

### Build Errors

**Problem**: TypeScript or Next.js errors

**Solutions:**
- Delete `node_modules`: `rm -rf node_modules && npm install`
- Clear Next.js cache: `rm -rf .next`
- Check TypeScript version: `npm list typescript`
- Restart dev server

---

## 📁 File Structure

```
frontend/src/app/
├── components/
│   ├── HealthCenterMap.tsx      # Map with markers
│   ├── HealthCenterList.tsx     # List view
│   └── Navigation.tsx
├── api/health-centers/
│   └── route.ts                 # Data endpoint
└── page.tsx                     # Main search page
```

### Component Details

**HealthCenterMap.tsx**
- Uses @vis.gl/react-google-maps
- Custom blue markers
- Info windows on click
- Auto-centering
- Responsive design

**HealthCenterList.tsx**
- Card-based layout
- Full address and contact info
- Clickable website links
- Shows coordinates

**page.tsx**
- Search form
- View mode toggle
- State management
- Integrates map and list

---

## 🎯 Usage

### Basic Search

1. Enter a zipcode (e.g., `02138`)
2. Click **Search Health Centers**
3. Results appear in your selected view

### View Modes

Click the buttons to toggle:
- **📋 List** - Shows list only
- **🗺️ Map** - Shows map only
- **📍 Both** - Shows both (default)

### Interacting with Results

**Map View:**
- Click markers to see info windows
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

### Environment Variables

Set in your hosting platform (Vercel, Netlify, etc.):
```
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_production_api_key
```

### API Key Configuration

1. Update API key restrictions in Google Cloud Console
2. Add production domain to HTTP referrers
3. Keep API restrictions (Maps JavaScript API, Geocoding API)

### Build & Deploy

```bash
cd frontend
npm run build
npm start  # or deploy to your platform
```

### Checklist

- [ ] Add API key to hosting platform
- [ ] Update API key domain restrictions
- [ ] Upload `community_health_centers_with_coords.csv`
- [ ] Test in production
- [ ] Set up error monitoring
- [ ] Configure billing alerts

---

## 🔌 API Endpoint

### GET /api/health-centers

**Query Parameters:**
- `zipcode` (optional): Filter by zipcode

**Example:**
```bash
curl "http://localhost:3000/api/health-centers?zipcode=02138"
```

**Response:**
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

---

## 📝 Additional Resources

- [Google Maps Platform Documentation](https://developers.google.com/maps/documentation)
- [@vis.gl/react-google-maps Docs](https://visgl.github.io/react-google-maps/)
- [Next.js Environment Variables](https://nextjs.org/docs/basic-features/environment-variables)
- [Google Cloud Console](https://console.cloud.google.com/)

---

## ✨ Summary

You now have:
- ✅ Interactive Google Maps with health center markers
- ✅ Multiple view modes (List/Map/Both)
- ✅ Zipcode search functionality
- ✅ 276+ health centers with geocoded addresses
- ✅ Mobile-responsive design
- ✅ Cost-effective (free tier)

**Need help?** Check the troubleshooting section above or open an issue on GitHub.

