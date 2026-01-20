"""
Script to add latitude and longitude coordinates to health centers CSV using Google Maps Geocoding API.
This script reads the community_health_centers_parsed.csv file, geocodes each address,
and creates a new CSV with latitude and longitude columns.

Usage:
    python add_geocoding.py YOUR_GOOGLE_MAPS_API_KEY

Requirements:
    pip install requests pandas
"""

import sys
import csv
import time
import requests
import pandas as pd
from typing import Optional, Tuple

def is_valid_address(row) -> bool:
    """
    Check if a row has a valid address that can be geocoded.
    
    Args:
        row: DataFrame row with address fields
        
    Returns:
        True if the row has a valid address, False otherwise
    """
    # Get address components
    street = str(row.get('street_address_1', '')).strip()
    city = str(row.get('city_town', '')).strip()
    state = str(row.get('state', '')).strip()
    zipcode = str(row.get('zipcode', '')).strip()
    
    # Check for 'nan' string (from pandas)
    if street == 'nan':
        street = ''
    if city == 'nan':
        city = ''
    if state == 'nan':
        state = ''
    if zipcode == 'nan':
        zipcode = ''
    
    # Must have at least street address OR city+state to be valid
    has_street = len(street) > 0
    has_city_state = len(city) > 0 and len(state) > 0
    
    return has_street or has_city_state

def geocode_address(address: str, api_key: str) -> Optional[Tuple[float, float]]:
    """
    Geocode an address using Google Maps Geocoding API.
    
    Args:
        address: Full address string
        api_key: Google Maps API key
        
    Returns:
        Tuple of (latitude, longitude) or None if geocoding fails
    """
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] == "OK" and len(data["results"]) > 0:
            location = data["results"][0]["geometry"]["location"]
            return (location["lat"], location["lng"])
        else:
            print(f"  ⚠️  Geocoding failed for: {address[:50]}... (Status: {data['status']})")
            return None
    except Exception as e:
        print(f"  ❌ Error geocoding {address[:50]}...: {str(e)}")
        return None

def add_geocoding_to_csv(input_file: str, output_file: str, api_key: str):
    """
    Read CSV, add geocoding, and write to new CSV.
    Only geocodes entries that don't already have coordinates.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
        api_key: Google Maps API key
    """
    print(f"📖 Reading {input_file}...")
    df = pd.read_csv(input_file)
    
    # Check if output file exists and has coordinates
    try:
        existing_df = pd.read_csv(output_file)
        # Create lookup for existing coordinates
        coord_lookup = {}
        for idx, row in existing_df.iterrows():
            name = str(row.get('name', '')).lower().strip()
            street = str(row.get('street_address_1', '')).lower().strip()
            key = (name, street)
            lat = row.get('latitude')
            lng = row.get('longitude')
            if pd.notna(lat) and pd.notna(lng) and lat != '' and lng != '':
                coord_lookup[key] = {'latitude': lat, 'longitude': lng}
        
        print(f"📋 Found {len(coord_lookup)} entries with existing coordinates")
        
        # Merge existing coordinates
        for idx, row in df.iterrows():
            name = str(row.get('name', '')).lower().strip()
            street = str(row.get('street_address_1', '')).lower().strip()
            key = (name, street)
            if key in coord_lookup:
                df.at[idx, 'latitude'] = coord_lookup[key]['latitude']
                df.at[idx, 'longitude'] = coord_lookup[key]['longitude']
    except FileNotFoundError:
        print("📋 No existing coordinates file found, will geocode all entries")
        df['latitude'] = None
        df['longitude'] = None
    
    # Ensure coordinate columns exist
    if 'latitude' not in df.columns:
        df['latitude'] = None
    if 'longitude' not in df.columns:
        df['longitude'] = None
    
    total = len(df)
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    print(f"\n🌍 Starting geocoding for {total} health centers...")
    print("=" * 80)
    
    for idx, row in df.iterrows():
        # Skip if already has coordinates
        lat = row.get('latitude')
        lng = row.get('longitude')
        if pd.notna(lat) and pd.notna(lng) and lat != '' and lng != '' and lat != 0 and lng != 0:
            print(f"\n[{idx + 1}/{total}] {row.get('name', 'Unknown')}")
            print(f"  ⏭️  Skipping: Already has coordinates ({lat}, {lng})")
            continue
        
        print(f"\n[{idx + 1}/{total}] {row.get('name', 'Unknown')}")
        
        # Check if the address is valid before making API call
        if not is_valid_address(row):
            print(f"  ⏭️  Skipping: No valid address found")
            skip_count += 1
            continue
        
        # Construct full address
        address_parts = [
            str(row.get('street_address_1', '')),
            str(row.get('street_address_2', '')),
            str(row.get('city_town', '')),
            str(row.get('state', '')),
            str(row.get('zipcode', ''))
        ]
        full_address = ', '.join([part for part in address_parts if part and part != 'nan'])
        
        print(f"  📍 Address: {full_address}")
        
        # Geocode the address
        coords = geocode_address(full_address, api_key)
        
        if coords:
            df.at[idx, 'latitude'] = coords[0]
            df.at[idx, 'longitude'] = coords[1]
            success_count += 1
            print(f"  ✅ Success: {coords[0]:.6f}, {coords[1]:.6f}")
        else:
            fail_count += 1
        
        # Rate limiting: Google Maps API has usage limits
        # Free tier: 40,000 requests per month, ~1 request per second
        if idx < total - 1:  # Don't sleep after last request
            time.sleep(0.1)  # Sleep for 100ms between requests
    
    print("\n" + "=" * 80)
    print(f"\n📊 Geocoding Summary:")
    print(f"  ✅ Successful: {success_count}/{total} ({success_count/total*100:.1f}%)")
    print(f"  ❌ Failed: {fail_count}/{total} ({fail_count/total*100:.1f}%)")
    print(f"  ⏭️  Skipped (no address): {skip_count}/{total} ({skip_count/total*100:.1f}%)")
    print(f"  📞 API calls made: {success_count + fail_count} (saved {skip_count} calls)")
    
    # Save to new CSV
    print(f"\n💾 Writing results to {output_file}...")
    df.to_csv(output_file, index=False)
    print(f"✨ Done! Geocoded data saved to {output_file}")

def main():
    if len(sys.argv) < 2:
        print("❌ Error: Missing Google Maps API key")
        print("\nUsage:")
        print("  python add_geocoding.py YOUR_GOOGLE_MAPS_API_KEY")
        print("\nGet your API key from:")
        print("  https://console.cloud.google.com/google/maps-apis")
        sys.exit(1)
    
    api_key = sys.argv[1]
    input_file = "hsn_active_health_centers_parsed.csv"
    output_file = "community_health_centers_with_coords.csv"
    
    try:
        add_geocoding_to_csv(input_file, output_file, api_key)
    except FileNotFoundError:
        print(f"❌ Error: Could not find {input_file}")
        print("Make sure you're running this script from the project root directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

