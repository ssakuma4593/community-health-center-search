import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const zipcode = searchParams.get('zipcode');
    
    const csvPath = path.join(process.cwd(), '..', 'community_health_centers_final.csv');
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
        
        // Extract zipcode from address
        const address = data.address || '';
        const zipcodeMatch = address.match(/\b(\d{5})\b/);
        const centerZipcode = zipcodeMatch ? zipcodeMatch[1] : '';
        
        // If no zipcode filter or if zipcode matches
        if (!zipcode || centerZipcode === zipcode) {
          results.push({
            name: data.name,
            address: data.address,
            phone: data.phone,
            types: data.types,
            website: data.website,
            zipcode: centerZipcode
          });
        }
      }
    }
    
    return NextResponse.json(results);
  } catch (error) {
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
