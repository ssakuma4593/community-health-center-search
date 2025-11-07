# Community Health Centers Map Feature

This feature adds a map interface to search for community health centers by zipcode using the data from `community_health_centers_final.csv`.

## Features

- **Zipcode Search**: Enter a 5-digit zipcode to find health centers in that area
- **Health Center Details**: View name, address, phone, services, and website for each center
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Search**: Instant results as you search

## How to Use

1. Navigate to the main page and click "View Health Centers Map"
2. Enter a 5-digit zipcode (e.g., 02138, 02139)
3. Click "Search Health Centers" to see results
4. View detailed information for each health center

## Technical Implementation

- **Frontend**: Next.js with TypeScript and Tailwind CSS
- **API**: RESTful endpoint at `/api/health-centers` with zipcode filtering
- **Data Source**: CSV file parsing without external dependencies
- **Navigation**: Simple navigation component for easy page switching

## API Endpoint

```
GET /api/health-centers?zipcode=02138
```

Returns JSON array of health centers matching the zipcode filter.

## File Structure

- `/frontend/src/app/map/page.tsx` - Map page component
- `/frontend/src/app/api/health-centers/route.ts` - API endpoint
- `/frontend/src/app/components/Navigation.tsx` - Navigation component
- `/frontend/src/app/layout.tsx` - Updated with navigation

## Data Format

Each health center includes:
- `name`: Health center name
- `address`: Full address with zipcode
- `phone`: Contact phone number
- `types`: Services offered (Primary Care, Dental Care, etc.)
- `website`: Website URL
- `zipcode`: Extracted 5-digit zipcode
