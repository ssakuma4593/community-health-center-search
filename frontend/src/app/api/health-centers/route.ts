import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const zipcode = searchParams.get('zipcode');
    
    const csvPath = path.join(process.cwd(), '..', 'community_health_centers_parsed.csv');
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
            state: data.state
          });
        }
      }
    }
    
    return NextResponse.json(results);
  } catch (error) {
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
