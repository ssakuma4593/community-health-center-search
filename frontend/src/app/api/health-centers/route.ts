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
    
    // Helper function to parse CSV line properly (handles quoted fields)
    const parseCSVLine = (line: string): string[] => {
      const result: string[] = [];
      let current = '';
      let inQuotes = false;
      
      for (let i = 0; i < line.length; i++) {
        const char = line[i];
        
        if (char === '"') {
          inQuotes = !inQuotes;
        } else if (char === ',' && !inQuotes) {
          result.push(current.trim());
          current = '';
        } else {
          current += char;
        }
      }
      result.push(current.trim());
      return result;
    };
    
    const lines = csvContent.split('\n');
    const headers = parseCSVLine(lines[0]);
    const results: any[] = [];
    
    for (let i = 1; i < lines.length; i++) {
      if (lines[i].trim()) {
        const values = parseCSVLine(lines[i]);
        const data: any = {};
        
        headers.forEach((header, index) => {
          data[header.trim()] = values[index]?.trim() || '';
        });
        
        // Get zipcode from the dedicated zipcode column
        const centerZipcode = data.zipcode || '';
        
        // If no zipcode filter or if zipcode matches
        if (!zipcode || centerZipcode === zipcode) {
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
            zipcode: centerZipcode,
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
