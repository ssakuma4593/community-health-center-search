#!/usr/bin/env python
"""
CSV Parser to split address into separate columns
"""

import csv
import re
import sys

def parse_address(address):
    """
    Parse address string into components
    """
    if not address:
        return "", "", "", "", ""
    
    # Remove quotes if present
    address = address.strip('"')
    
    # Pattern to match: "Street Address, City, State ZIP"
    # This handles most US address formats
    pattern = r'^(.+?),\s*([^,]+),\s*([A-Z]{2})\s+(\d{5}(?:-\d{4})?)$'
    match = re.match(pattern, address)
    
    if match:
        street = match.group(1).strip()
        city = match.group(2).strip()
        state = match.group(3).strip()
        zipcode = match.group(4).strip()
        return street, "", city, state, zipcode
    
    # Fallback: try to extract zipcode and work backwards
    zipcode_match = re.search(r'\b(\d{5}(?:-\d{4})?)\b', address)
    if zipcode_match:
        zipcode = zipcode_match.group(1)
        # Remove zipcode from address to get the rest
        remaining = address.replace(zipcode, '').strip()
        # Split by comma
        parts = [p.strip() for p in remaining.split(',')]
        if len(parts) >= 2:
            street = parts[0]
            city = parts[1]
            state = parts[2] if len(parts) > 2 else ""
        else:
            street = remaining
            city = ""
            state = ""
        return street, "", city, state, zipcode
    
    # If no zipcode found, return as street address
    return address, "", "", "", ""

def process_csv(input_file, output_file):
    """
    Process CSV file and create new one with separate address columns
    """
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        
        # New fieldnames with separate address columns
        fieldnames = [
            'name',
            'street_address_1',
            'street_address_2', 
            'city_town',
            'state',
            'zipcode',
            'phone',
            'types',
            'website',
            'source'
        ]
        
        with open(output_file, 'w') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                # Parse the address
                street1, street2, city, state, zipcode = parse_address(row.get('address', ''))
                
                # Create new row with separated address components
                new_row = {
                    'name': row.get('name', ''),
                    'street_address_1': street1,
                    'street_address_2': street2,
                    'city_town': city,
                    'state': state,
                    'zipcode': zipcode,
                    'phone': row.get('phone', ''),
                    'types': row.get('types', ''),
                    'website': row.get('website', ''),
                    'source': row.get('source', '')
                }
                
                writer.writerow(new_row)

if __name__ == "__main__":
    input_file = "community_health_centers_final.csv"
    output_file = "community_health_centers_parsed.csv"
    
    try:
        process_csv(input_file, output_file)
        print("Successfully processed {} -> {}".format(input_file, output_file))
        print("New columns: street_address_1, street_address_2, city_town, state, zipcode")
    except Exception as e:
        print("Error processing CSV: {}".format(e))
        sys.exit(1)
