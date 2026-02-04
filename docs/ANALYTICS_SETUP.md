# Analytics Setup Guide - Google Analytics 4 (GA4)

Step-by-step guide to set up analytics tracking for the Community Health Center Search app.

## Step 1: Create Google Analytics Account & Property (5 minutes)

1. **Go to Google Analytics**: https://analytics.google.com/
2. **Sign in** with your Google account
3. **Click "Start measuring"** (or "Admin" → "Create Property" if you have an account)
4. **Create Account** (if needed):
   - Account name: "Community Health Center Search" (or your choice)
   - Click "Next"
5. **Create Property**:
   - Property name: "Community Health Center Search"
   - Reporting time zone: Choose your timezone
   - Currency: USD
   - Click "Next"
6. **Fill business info** (can use "Other" if unsure)
7. **Click "Create"** and accept terms

## Step 2: Get Your Measurement ID (2 minutes)

1. In your new property, you'll see **"Data Streams"** - click it
2. Click **"Add stream"** → **"Web"**
3. Fill in:
   - **Website URL**: Your GitHub Pages URL (e.g., `https://yourusername.github.io/community-health-center-search`) or `http://localhost:5173` for testing
   - **Stream name**: "Community Health Center Search"
4. Click **"Create stream"**
5. **Copy the Measurement ID** - it looks like `G-XXXXXXXXXX` (starts with G-)

**Important:** Keep this Measurement ID handy - you'll need it in the next step!

## Step 3: Configure Local Development (1 minute)

1. **Create `.env` file** in the `frontend` directory:
   ```bash
   cd frontend
   touch .env
   ```

2. **Add your Measurement ID** to the `.env` file:
   ```bash
   VITE_GA_MEASUREMENT_ID=G-XXXXXXXXXX
   ```
   (Replace `G-XXXXXXXXXX` with your actual Measurement ID)

3. **Restart your dev server** if it's running:
   ```bash
   npm run dev
   ```

## Step 4: Test It Works (2 minutes)

1. **Open your app** in the browser (usually `http://localhost:5173`)
2. **Open browser DevTools** (F12) → Console tab
3. **Perform some actions**:
   - Search for a zip code (e.g., "02138")
   - Click "Booking Info" on a health center
4. **Check Google Analytics**:
   - Go back to Google Analytics
   - Click **"Reports"** in the left sidebar
   - Click **"Realtime"**
   - You should see events appearing within 10-30 seconds!

**Troubleshooting:** If you don't see events:
- Check the browser console for errors
- Make sure `.env` file has the correct Measurement ID
- Verify the `.env` file is in the `frontend/` directory (not root)
- Try hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

## Step 5: Configure for Production/Deployment (GitHub Pages)

For your app to track analytics when deployed to GitHub Pages:

1. **Add GitHub Secret**:
   - Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
   - Click **"New repository secret"**
   - Name: `VITE_GA_MEASUREMENT_ID`
   - Value: Your Measurement ID (e.g., `G-XXXXXXXXXX`)
   - Click **"Add secret"**

2. **The workflow file is already updated** - it will use this secret during builds!

3. **Deploy** - The next time you push to a branch that triggers deployment, analytics will work in production.

## Tracked Events

### Zip Code Search (`zipcode_search`)
Triggered when a user searches for health centers by zip code.

**Parameters:**
- `zipcode`: The searched zip code
- `zipcode_hash`: Hashed version for privacy
- `radius`: Search radius in miles
- `results_count`: Number of centers found
- `service_filters`: Comma-separated list of active filters

### Booking Info Click (`booking_info_click`)
Triggered when a user clicks the "Booking Info" button.

**Parameters:**
- `center_name`: Name of the health center
- `search_zipcode`: The zip code used in current search (if any)

### Service Filter Toggle (`service_filter_toggle`)
Triggered when a user toggles a service type filter.

**Parameters:**
- `filter_type`: Type of filter (`primary_care`, `dental_care`, `vision`, `behavioral_health`)
- `enabled`: Whether filter was enabled (`true`) or disabled (`false`)

### Center Detail View (`center_detail_view`)
Triggered when a user opens the detail modal for a health center.

**Parameters:**
- `center_name`: Name of the health center

### Contact Click (`contact_click`)
Triggered when a user clicks contact information (phone, website, or maps link).

**Parameters:**
- `contact_type`: Type of contact (`phone`, `website`, `maps`)
- `center_name`: Name of the health center

## Privacy Features

- ✅ IP anonymization enabled
- ✅ Google Signals disabled
- ✅ Ad personalization disabled
- ✅ Zip codes hashed before sending
