# Deployment Guide

This document describes the deployment setup for the Community Health Center Search application, including GitHub Pages deployment.

## Quick Start

### Local Development

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

### Build for Production

```bash
cd frontend
npm run build
```

### Deploy to GitHub Pages

The app automatically deploys to GitHub Pages when you push to the `feature/github-pages-deployment` or `main` branch.

**Deployment URL:** `https://<org>.github.io/community-health-center-search/`

## Features

- ✅ **Zipcode Search** - Search health centers by zipcode
- ✅ **Interactive Map** - Leaflet map with OpenStreetMap tiles (free, no API key)
- ✅ **Distance Calculation** - Haversine formula for accurate distances
- ✅ **Results List** - Sorted by distance, filterable by radius
- ✅ **Detail View** - Markdown rendering for patient instructions
- ✅ **GitHub Pages Ready** - Configured base path for subpath deployment
- ✅ **GitHub Actions** - Automated deployment workflow

## Tech Stack

- **Vite** - Fast build tool
- **React 19** - UI framework
- **TypeScript** - Type safety
- **Leaflet** - Interactive maps (free, open source)
- **react-leaflet** - React bindings
- **react-markdown** - Markdown rendering
- **PapaParse** - CSV parsing

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── HealthCenterMap.tsx      # Leaflet map component
│   │   ├── HealthCenterList.tsx      # Results list component
│   │   └── HealthCenterDetail.tsx    # Detail modal with markdown
│   ├── utils/
│   │   ├── csvLoader.ts              # CSV parsing
│   │   ├── geocoding.ts              # Zipcode geocoding (free API)
│   │   └── distance.ts               # Haversine distance calculation
│   ├── types.ts                       # TypeScript types
│   ├── App.tsx                        # Main app component
│   └── main.tsx                       # Entry point
├── public/
│   └── data/
│       └── centers.csv                # Health center data
├── vite.config.ts                     # Vite config with base path
└── package.json

.github/
└── workflows/
    └── deploy-pages.yml               # GitHub Actions deployment
```

## How It Works

### Zipcode Geocoding

The app uses **Nominatim** (OpenStreetMap's free geocoding service) to convert zipcodes to coordinates. No API key required, but please use responsibly (max 1 request per second).

### Distance Calculation

Uses the **Haversine formula** to calculate distances between zipcode and health centers. Results are sorted by distance and filtered by radius (default 25 miles).

### Data Loading

Health center data is loaded client-side from `/public/data/centers.csv` using PapaParse. The CSV includes:
- Basic info: name, address, phone, website
- Coordinates: latitude, longitude
- Services: types of care offered
- OpenAI enrichment fields (optional): `openai_phone`, `openai_address`, `openai_new_patient_md`, etc.

## GitHub Pages Configuration

### Base Path

The app is configured to work under a subpath: `/community-health-center-search/`

This is set in `vite.config.ts`:
```typescript
base: process.env.NODE_ENV === 'production' ? '/community-health-center-search/' : '/',
```

### GitHub Actions Workflow

The workflow (`.github/workflows/deploy-pages.yml`) automatically:
1. Builds the Vite app
2. Uploads the dist folder as a Pages artifact
3. Deploys to GitHub Pages

**To enable GitHub Pages:**
1. Go to repository Settings → Pages
2. Source: GitHub Actions
3. The workflow will deploy automatically on push

## Step-by-Step Deployment Instructions

### Step 1: Commit and Push Your Changes

```bash
# Make sure you're on the right branch
git checkout feature/github-pages-deployment

# Add all changes
git add -A

# Commit
git commit -m "Add Vite frontend with GitHub Pages deployment support"

# Push to GitHub
git push origin feature/github-pages-deployment
```

### Step 2: Enable GitHub Pages

1. Go to your GitHub repository: `https://github.com/<your-org>/community-health-center-search`
2. Click on **Settings** (top menu)
3. Scroll down to **Pages** (left sidebar)
4. Under **Source**, select **GitHub Actions**
5. Save the changes

### Step 3: Wait for Deployment

1. Go to the **Actions** tab in your repository
2. You should see a workflow run called "Deploy to GitHub Pages"
3. Wait for it to complete (usually 2-3 minutes)
4. Once it's done, you'll see a green checkmark

### Step 4: Access Your Site

Your site will be available at:
```
https://<your-org>.github.io/community-health-center-search/
```

**Note:** Replace `<your-org>` with your GitHub username or organization name.

## Environment Variables

**None required!** The app uses free services:
- OpenStreetMap/Nominatim for geocoding (no API key)
- OpenStreetMap tiles for maps (no API key)

## CSV Schema

The CSV file (`public/data/centers.csv`) should have these columns:

**Required:**
- `name` - Health center name
- `street_address_1` - Street address
- `city_town` - City
- `state` - State (e.g., MA)
- `zipcode` - Zipcode
- `phone` - Phone number
- `latitude` - Latitude coordinate
- `longitude` - Longitude coordinate

**Optional:**
- `street_address_2` - Additional address line
- `types` - Services offered (comma-separated)
- `website` - Website URL
- `source` - Data source

**OpenAI Enrichment (optional):**
- `openai_phone` - Verified phone number
- `openai_address` - Verified address
- `openai_new_patient_md` - Markdown instructions for new patients
- `openai_other_notes_md` - Additional notes (Markdown)
- `openai_source_urls` - Source URLs (comma-separated)
- `openai_last_checked_utc` - Last check timestamp (ISO)
- `openai_confidence` - Confidence level (Low/Med/High or 0-1)

## Troubleshooting

### Map Not Showing

- Check browser console for errors
- Verify Leaflet CSS is imported (should be automatic)
- Check that centers.csv has valid latitude/longitude values

### No Results Found

- Verify zipcode is valid (5 digits)
- Try expanding the radius
- Check browser console for geocoding errors

### Build Fails

- Run `npm install` in `frontend/`
- Check TypeScript errors: `npm run build`
- Verify all dependencies are installed

### GitHub Pages Not Updating

- Check GitHub Actions tab for workflow status
- Verify Pages is enabled in repository Settings
- Check that workflow file is in `.github/workflows/`
- Ensure you're pushing to `main` or `feature/github-pages-deployment` branch

### Workflow Not Running

- Make sure you pushed to `feature/github-pages-deployment` or `main` branch
- Check the Actions tab for any errors

### Pages Not Showing

- Wait a few minutes after the workflow completes (GitHub Pages can take 1-5 minutes to update)
- Check that Pages source is set to "GitHub Actions" in Settings → Pages
- Verify the workflow completed successfully (green checkmark)

### 404 Error

- Make sure the base path in `vite.config.ts` matches your repository name
- The base path should be `/community-health-center-search/` (with trailing slash)

## Updating Your Site

Every time you push to `main` or `feature/github-pages-deployment`, the site will automatically rebuild and deploy. Just push your changes and wait for the workflow to complete!

## Next Steps

Once GitHub Pages is deployed and working, the next phase includes:
- OpenAI enrichment pipeline for patient instructions
- Backend API endpoint for enrichment
- Script to enrich CSV data
- Display enriched data in the detail view

See [docs/OPENAI_ENRICHMENT.md](OPENAI_ENRICHMENT.md) for OpenAI enrichment setup instructions.
