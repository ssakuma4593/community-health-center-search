#!/usr/bin/env python3
"""
Script to scrape health center data from DOCX file and save as CSV
"""

import csv
import re
from pathlib import Path
from docx import Document
from typing import List, Dict, Optional

def parse_docx_to_csv(docx_path: str, output_csv_path: str):
    """Parse DOCX file and extract health center data to CSV"""
    
    print(f"Reading DOCX file: {docx_path}")
    doc = Document(docx_path)
    
    health_centers = []
    
    # Extract from tables
    for table_idx, table in enumerate(doc.tables):
        print(f"Processing table {table_idx + 1} with {len(table.rows)} rows")
        
        if not table.rows:
            continue
        
        # Get header row to understand column structure
        header_row = table.rows[0]
        headers = [cell.text.strip() for cell in header_row.cells]
        print(f"  Headers: {headers}")
        
        # Process data rows (skip header row)
        for row_idx, row in enumerate(table.rows[1:], 1):
            if len(row.cells) < 2:  # Need at least 2 columns
                continue
            
            cells = [cell.text.strip() for cell in row.cells]
            
            # Skip empty rows
            if not any(cells):
                continue
            
            # Skip header-like rows (rows that contain "Organization Name", "Street Address", etc.)
            cells_lower = ' '.join([c.lower() for c in cells])
            if any(keyword in cells_lower for keyword in ['organization name', 'street address', 'phone number', 'city/town', 'zip code']):
                continue
            
            # Parse the row
            center_info = parse_table_row(cells, headers)
            if center_info and center_info.get('name'):
                health_centers.append(center_info)
    
    # Remove duplicates based on name and address
    unique_centers = remove_duplicates(health_centers)
    
    print(f"\nExtracted {len(unique_centers)} unique health centers")
    
    # Save to CSV
    print(f"Saving to CSV: {output_csv_path}")
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'street_address_1', 'street_address_2', 'city_town', 'state', 'zipcode', 'phone', 'types', 'website', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for center in unique_centers:
            center_copy = center.copy()
            # Ensure all address fields exist
            if 'street_address_1' not in center_copy:
                center_copy['street_address_1'] = ''
            if 'street_address_2' not in center_copy:
                center_copy['street_address_2'] = ''
            if 'city_town' not in center_copy:
                center_copy['city_town'] = ''
            if 'state' not in center_copy:
                center_copy['state'] = 'MA'
            if 'zipcode' not in center_copy:
                center_copy['zipcode'] = ''
            # Convert types list to string
            if isinstance(center_copy.get('types'), list):
                center_copy['types'] = ', '.join(center_copy['types'])
            writer.writerow(center_copy)
    
    print(f"✅ Successfully saved {len(unique_centers)} centers to {output_csv_path}")
    return unique_centers

def parse_address(address_str: str) -> Dict[str, str]:
    """Parse a full address string into separate components"""
    if not address_str:
        return {
            'street_address_1': '',
            'street_address_2': '',
            'city_town': '',
            'state': 'MA',
            'zipcode': ''
        }
    
    # Try to parse address components
    # Common format: "Street Address, City, State ZIPCODE"
    parts = [p.strip() for p in address_str.split(',')]
    
    street_address_1 = ''
    street_address_2 = ''
    city_town = ''
    state = 'MA'
    zipcode = ''
    
    if len(parts) >= 3:
        # Format: "Street, City, State ZIP"
        street_address_1 = parts[0]
        city_town = parts[1]
        last_part = parts[-1].strip()
        # Extract state and zipcode from last part (e.g., "MA 01220")
        state_zip_match = re.match(r'([A-Z]{2})\s+(\d{5})', last_part)
        if state_zip_match:
            state = state_zip_match.group(1)
            zipcode = state_zip_match.group(2)
        elif last_part.isdigit() and len(last_part) == 5:
            zipcode = last_part
    elif len(parts) == 2:
        # Format: "Street, City State ZIP" or "Street, City"
        street_address_1 = parts[0]
        last_part = parts[1].strip()
        # Try to extract city, state, zip
        state_zip_match = re.match(r'(.+?)\s+([A-Z]{2})\s+(\d{5})', last_part)
        if state_zip_match:
            city_town = state_zip_match.group(1)
            state = state_zip_match.group(2)
            zipcode = state_zip_match.group(3)
        else:
            city_town = last_part
    elif len(parts) == 1:
        # Single part - could be just street or full address
        street_address_1 = parts[0]
    
    return {
        'street_address_1': street_address_1,
        'street_address_2': street_address_2,
        'city_town': city_town,
        'state': state,
        'zipcode': zipcode
    }

def parse_table_row(cells: List[str], headers: List[str]) -> Optional[Dict]:
    """Parse a single table row to extract health center information"""
    center_info = {
        'name': '',
        'street_address_1': '',
        'street_address_2': '',
        'city_town': '',
        'state': 'MA',
        'zipcode': '',
        'phone': '',
        'types': '',
        'website': '',
        'source': 'docx_scraped'
    }
    
    # Try to map based on headers first
    header_map = {}
    for i, header in enumerate(headers):
        header_lower = header.lower()
        if 'name' in header_lower or 'organization' in header_lower:
            header_map['name'] = i
        elif 'address' in header_lower or 'street' in header_lower:
            header_map['address'] = i
        elif 'phone' in header_lower or 'telephone' in header_lower:
            header_map['phone'] = i
        elif 'city' in header_lower or 'town' in header_lower:
            header_map['city'] = i
        elif 'zip' in header_lower or 'postal' in header_lower:
            header_map['zip'] = i
    
    # Extract based on header mapping
    if 'name' in header_map and header_map['name'] < len(cells):
        center_info['name'] = cells[header_map['name']]
    
    # Extract address components
    if 'address' in header_map and header_map['address'] < len(cells):
        street = cells[header_map['address']]
        if street:
            center_info['street_address_1'] = street
    
    if 'city' in header_map and header_map['city'] < len(cells):
        city = cells[header_map['city']]
        if city:
            center_info['city_town'] = city
    
    if 'zip' in header_map and header_map['zip'] < len(cells):
        zipcode = cells[header_map['zip']]
        if zipcode:
            center_info['zipcode'] = zipcode.strip()
    
    if 'phone' in header_map and header_map['phone'] < len(cells):
        center_info['phone'] = cells[header_map['phone']]
    
    # If header mapping didn't work, try position-based extraction
    if not center_info['name'] and len(cells) >= 1:
        # Common patterns: [City/Town, Organization Name, Street Address, Zip Code, Phone]
        if len(cells) >= 5:
            # Pattern: City, Name, Address, Zip, Phone
            center_info['name'] = cells[1] if not center_info['name'] else center_info['name']
            if not center_info['street_address_1']:
                center_info['street_address_1'] = cells[2]
            if not center_info['city_town']:
                center_info['city_town'] = cells[0]
            if not center_info['zipcode'] and cells[3]:
                center_info['zipcode'] = cells[3].strip()
            if not center_info['phone']:
                center_info['phone'] = cells[4]
        elif len(cells) >= 4:
            # Pattern: City, Name, Address, Phone
            center_info['name'] = cells[1] if not center_info['name'] else center_info['name']
            if not center_info['street_address_1']:
                center_info['street_address_1'] = cells[2]
            if not center_info['city_town']:
                center_info['city_town'] = cells[0]
            if not center_info['phone']:
                center_info['phone'] = cells[3]
        elif len(cells) >= 3:
            # Pattern: Name, Address, Phone
            center_info['name'] = cells[0] if not center_info['name'] else center_info['name']
            if not center_info['street_address_1']:
                # Try to parse address if it contains city/state/zip
                address_str = cells[1]
                parsed_addr = parse_address(address_str)
                if parsed_addr['street_address_1']:
                    center_info['street_address_1'] = parsed_addr['street_address_1']
                if parsed_addr['city_town']:
                    center_info['city_town'] = parsed_addr['city_town']
                if parsed_addr['zipcode']:
                    center_info['zipcode'] = parsed_addr['zipcode']
            if not center_info['phone']:
                center_info['phone'] = cells[2]
        elif len(cells) >= 2:
            # Pattern: Name, Address
            center_info['name'] = cells[0] if not center_info['name'] else center_info['name']
            if not center_info['street_address_1']:
                # Try to parse address
                address_str = cells[1]
                parsed_addr = parse_address(address_str)
                if parsed_addr['street_address_1']:
                    center_info['street_address_1'] = parsed_addr['street_address_1']
                if parsed_addr['city_town']:
                    center_info['city_town'] = parsed_addr['city_town']
                if parsed_addr['zipcode']:
                    center_info['zipcode'] = parsed_addr['zipcode']
        elif len(cells) >= 1:
            center_info['name'] = cells[0] if not center_info['name'] else center_info['name']
    
    # Clean up phone number format
    if center_info['phone']:
        center_info['phone'] = clean_phone(center_info['phone'])
    
    return center_info if center_info['name'] else None

def clean_phone(phone: str) -> str:
    """Clean and format phone number"""
    if not phone:
        return ''
    # Remove extra whitespace
    phone = ' '.join(phone.split())
    # Try to format as (XXX) XXX-XXXX
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone

def remove_duplicates(centers: List[Dict]) -> List[Dict]:
    """Remove duplicate centers based on name and address"""
    seen = set()
    unique_centers = []
    
    for center in centers:
        name = center.get('name', '').lower().strip()
        address = center.get('address', '').lower().strip()
        key = (name, address)
        
        if key not in seen:
            seen.add(key)
            unique_centers.append(center)
    
    return unique_centers

def main():
    docx_path = "data/official_documents/hsn-active-health-center-listings.docx"
    output_csv_path = "data/raw/hsn_active_health_centers_parsed.csv"
    
    if not Path(docx_path).exists():
        print(f"❌ Error: DOCX file not found at {docx_path}")
        return
    
    parse_docx_to_csv(docx_path, output_csv_path)
    print(f"\n✅ Done! CSV saved to {output_csv_path}")

if __name__ == "__main__":
    main()

