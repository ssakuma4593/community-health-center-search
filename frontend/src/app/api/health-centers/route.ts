import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const zipcode = searchParams.get('zipcode');
    
    // Try to use the geocoded CSV first, fall back to parsed CSV
    let csvPath = path.join(process.cwd(), '..', 'community_health_centers_with_coords.csv');
    if (!fs.existsSync(csvPath)) {
      csvPath = path.join(process.cwd(), '..', 'community_health_centers_parsed.csv');
    }
    
    const csvContent = fs.readFileSync(csvPath, 'utf-8');
    const lines = csvContent.split('\n');
    const headers = lines[0].split(',');
    const results: any[] = [];
    
    for (let i = 1; i < lines.length; i++) {
      if (lines[i].trim()) {
        const values = lines[i].split(',');
        const data: any = {};
        
        headers.forEach((header, index) => {
          data[header.trim()] = values[index]?.trim() || '';
        });
        
        // Get zipcode from the dedicated zipcode column
        const centerZipcode = data.zipcode || '';
        
        // Normalize zipcodes for comparison (remove .0 and pad with leading zeros)
        const normalizeZip = (zip: string) => {
          if (!zip) return '';
          // Remove .0 if present and convert to number, then pad to 5 digits
          const numZip = parseInt(zip.replace('.0', ''));
          return isNaN(numZip) ? '' : numZip.toString().padStart(5, '0');
        };
        
        const normalizedCenterZip = normalizeZip(centerZipcode);
        const normalizedSearchZip = zipcode ? normalizeZip(zipcode) : '';
        
        // If no zipcode filter or if zipcode matches
        if (!zipcode || normalizedCenterZip === normalizedSearchZip) {
          // Reconstruct full address from components
          const fullAddress = [
            data.street_address_1,
            data.street_address_2,
            data.city_town,
            data.state,
            data.zipcode
          ].filter(Boolean).join(', ');
          
          results.push({
            name: data.name,
            address: fullAddress,
            phone: data.phone,
            types: data.types,
            website: data.website,
            zipcode: normalizedCenterZip, // Use normalized zipcode with leading zeros
            street_address_1: data.street_address_1,
            street_address_2: data.street_address_2,
            city_town: data.city_town,
            state: data.state,
            latitude: data.latitude ? parseFloat(data.latitude) : undefined,
            longitude: data.longitude ? parseFloat(data.longitude) : undefined
          });
        }
      }
    }
    
    return NextResponse.json(results);
  } catch (error) {
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
