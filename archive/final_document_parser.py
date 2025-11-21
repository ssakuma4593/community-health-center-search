#!/usr/bin/env python3
"""
Table-Aware Document Parser for Official MA Health Center Documents
Parses Word documents with table structure to extract health center information
"""

import os
import json
import csv
import re
from typing import List, Dict, Optional
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TableAwareParser:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.official_docs_dir = self.data_dir / "official_documents"
        self.parsed_data_dir = self.data_dir / "parsed_data"
        self.health_centers = []
        
        # Ensure directories exist
        self.official_docs_dir.mkdir(parents=True, exist_ok=True)
        self.parsed_data_dir.mkdir(parents=True, exist_ok=True)
    
    def parse_word_document(self, file_path: str) -> List[Dict]:
        """Parse a Word document and extract health center information from tables"""
        try:
            from docx import Document
        except ImportError:
            logger.error("python-docx not installed. Install with: pip install python-docx")
            return []
        
        try:
            doc = Document(file_path)
            health_centers = []
            
            logger.info(f"Parsing document: {file_path}")
            
            # Extract from tables
            for table_idx, table in enumerate(doc.tables):
                logger.info(f"Processing table {table_idx + 1} with {len(table.rows)} rows")
                table_centers = self.parse_table(table)
                health_centers.extend(table_centers)
            
            logger.info(f"Found {len(health_centers)} health centers in document")
            return health_centers
            
        except Exception as e:
            logger.error(f"Error parsing document {file_path}: {e}")
            return []
    
    def parse_table(self, table) -> List[Dict]:
        """Parse a table to extract health center information"""
        centers = []
        
        if not table.rows:
            return centers
        
        # Get header row to understand column structure
        header_row = table.rows[0]
        headers = [cell.text.strip() for cell in header_row.cells]
        
        logger.info(f"Table headers: {headers}")
        
        # Process data rows (skip header row)
        for row_idx, row in enumerate(table.rows[1:], 1):
            if len(row.cells) < 3:  # Need at least 3 columns
                continue
            
            # Extract data from each cell
            cells = [cell.text.strip() for cell in row.cells]
            
            # Skip empty rows or header rows
            if not any(cells) or 'Organization Name' in str(cells):
                continue
            
            center_info = self.parse_table_row(cells, headers)
            if center_info:
                centers.append(center_info)
        
        logger.info(f"Extracted {len(centers)} centers from table")
        return centers
    
    def parse_table_row(self, cells: List[str], headers: List[str]) -> Optional[Dict]:
        """Parse a single table row to extract health center information"""
        center_info = {
            'name': '',
            'address': '',
            'phone': '',
            'types': [],
            'website': '',
            'source': 'official_document'
        }
        
        try:
            # Map cells to fields based on content patterns
            city_town = ''
            organization_name = ''
            street_address = ''
            zip_code = ''
            phone_number = ''
            
            # Process each cell
            for i, cell_content in enumerate(cells):
                if not cell_content:
                    continue
                
                # Identify field type based on content patterns
                if self.is_city_town(cell_content):
                    city_town = cell_content
                elif self.is_organization_name(cell_content):
                    organization_name = cell_content
                elif self.is_street_address(cell_content):
                    street_address = cell_content
                elif self.is_zip_code(cell_content):
                    zip_code = cell_content
                elif self.is_phone_number(cell_content):
                    phone_number = cell_content
            
            # If we couldn't identify fields by content, use position-based mapping
            if not organization_name and len(cells) >= 2:
                # Common pattern: [City/Town, Organization Name, Street Address, Zip Code, Phone]
                if len(cells) >= 5:
                    city_town = cells[0] if cells[0] else ''
                    organization_name = cells[1] if cells[1] else ''
                    street_address = cells[2] if cells[2] else ''
                    zip_code = cells[3] if cells[3] else ''
                    phone_number = cells[4] if cells[4] else ''
                elif len(cells) >= 4:
                    city_town = cells[0] if cells[0] else ''
                    organization_name = cells[1] if cells[1] else ''
                    street_address = cells[2] if cells[2] else ''
                    phone_number = cells[3] if cells[3] else ''
                elif len(cells) >= 3:
                    organization_name = cells[0] if cells[0] else ''
                    street_address = cells[1] if cells[1] else ''
                    phone_number = cells[2] if cells[2] else ''
            
            # Build the center info
            center_info['name'] = organization_name
            
            # Build full address
            if street_address and city_town and zip_code:
                center_info['address'] = f"{street_address}, {city_town}, MA {zip_code}"
            elif street_address and city_town:
                center_info['address'] = f"{street_address}, {city_town}, MA"
            elif street_address:
                center_info['address'] = street_address
            
            center_info['phone'] = phone_number
            
            # Extract service types from name
            name_lower = organization_name.lower()
            if 'dental' in name_lower:
                center_info['types'].append('Dental Care')
            if 'primary' in name_lower:
                center_info['types'].append('Primary Care')
            if 'eye' in name_lower or 'vision' in name_lower:
                center_info['types'].append('Eye Care')
            if 'mental' in name_lower:
                center_info['types'].append('Mental Health')
            if 'pediatric' in name_lower:
                center_info['types'].append('Pediatric Care')
            if 'hospital' in name_lower:
                center_info['types'].append('Hospital Services')
            if 'health center' in name_lower:
                center_info['types'].append('Primary Care')
            
            # Only return if we have essential info
            if center_info['name']:
                return center_info
                
        except Exception as e:
            logger.error(f"Error parsing table row: {e}")
        
        return None
    
    def is_city_town(self, text: str) -> bool:
        """Check if text is a city/town name"""
        # Common city patterns
        city_indicators = [
            'Boston', 'Cambridge', 'Somerville', 'Newton', 'Brookline', 'Quincy',
            'Worcester', 'Springfield', 'Lowell', 'Lawrence', 'New Bedford',
            'Brockton', 'Lynn', 'Fall River', 'Waltham', 'Malden', 'Medford',
            'Taunton', 'Chicopee', 'Weymouth', 'Revere', 'Peabody', 'Methuen',
            'Barnstable', 'Pittsfield', 'Attleboro', 'Salem', 'Westfield',
            'Leominster', 'Fitchburg', 'Beverly', 'Holyoke', 'Marlborough',
            'Woburn', 'West Springfield', 'Braintree', 'Chelsea', 'Haverhill',
            'Framingham', 'Burlington', 'Natick', 'Watertown', 'Franklin',
            'Gloucester', 'Northampton', 'Randolph', 'Needham', 'Wellesley'
        ]
        
        return any(city in text for city in city_indicators)
    
    def is_organization_name(self, text: str) -> bool:
        """Check if text is an organization name"""
        # Organization name indicators
        org_indicators = [
            'Hospital', 'Health Center', 'Medical Center', 'Clinic',
            'Community Health', 'Family Health', 'Neighborhood Health',
            'Health Services', 'Health Care', 'Medical Group'
        ]
        
        return any(indicator in text for indicator in org_indicators)
    
    def is_street_address(self, text: str) -> bool:
        """Check if text is a street address"""
        # Street address patterns
        address_patterns = [
            r'\d+.*?(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)',
            r'\d+.*?,\s*[A-Za-z\s]+'  # Number followed by comma and text
        ]
        
        return any(re.search(pattern, text) for pattern in address_patterns)
    
    def is_zip_code(self, text: str) -> bool:
        """Check if text is a zip code"""
        # Zip code pattern
        zip_pattern = r'^\d{5}$'
        return bool(re.match(zip_pattern, text))
    
    def is_phone_number(self, text: str) -> bool:
        """Check if text is a phone number"""
        # Phone number pattern
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        return bool(re.search(phone_pattern, text))
    
    def remove_duplicates(self, centers: List[Dict]) -> List[Dict]:
        """Remove duplicate centers based on name and address"""
        seen = set()
        unique_centers = []
        
        for center in centers:
            # Create a key based on name and address
            key = (center.get('name', '').lower().strip(), center.get('address', '').lower().strip())
            if key not in seen:
                seen.add(key)
                unique_centers.append(center)
        
        return unique_centers
    
    def save_to_json(self, filename: str = "table_parsed_health_centers.json"):
        """Save parsed data to JSON"""
        output_path = self.parsed_data_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.health_centers, f, indent=2, ensure_ascii=False)
        logger.info(f"Data saved to {output_path}")
    
    def save_to_csv(self, filename: str = "table_parsed_health_centers.csv"):
        """Save parsed data to CSV"""
        if not self.health_centers:
            logger.warning("No data to save")
            return
        
        output_path = self.parsed_data_dir / filename
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'address', 'phone', 'types', 'website', 'source'])
            writer.writeheader()
            for center in self.health_centers:
                center_copy = center.copy()
                center_copy['types'] = ', '.join(center['types'])
                writer.writerow(center_copy)
        logger.info(f"Data saved to {output_path}")
    
    def parse_all_documents(self):
        """Parse all documents in the official_documents directory"""
        documents = []
        for file_path in self.official_docs_dir.glob("*.docx"):
            documents.append(file_path.name)
        for file_path in self.official_docs_dir.glob("*.doc"):
            documents.append(file_path.name)
        
        if not documents:
            logger.warning("No documents found in official_documents directory")
            logger.info(f"Place your Word documents in: {self.official_docs_dir}")
            return []
        
        logger.info(f"Found {len(documents)} documents to parse")
        
        all_centers = []
        for doc in documents:
            doc_path = self.official_docs_dir / doc
            centers = self.parse_word_document(str(doc_path))
            all_centers.extend(centers)
        
        # Remove duplicates
        self.health_centers = self.remove_duplicates(all_centers)
        logger.info(f"Total unique health centers found: {len(self.health_centers)}")
        
        return self.health_centers
    
    def run(self):
        """Main method to parse all documents"""
        logger.info("Starting table-aware document parsing...")
        
        self.health_centers = self.parse_all_documents()
        
        if self.health_centers:
            self.save_to_json()
            self.save_to_csv()
            logger.info(f"Document parsing completed! Found {len(self.health_centers)} health centers.")
        else:
            logger.warning("No health centers found in documents.")
        
        return self.health_centers

def main():
    """Main function"""
    parser = TableAwareParser()
    centers = parser.run()
    
    print(f"\n=== TABLE-AWARE DOCUMENT PARSING SUMMARY ===")
    print(f"Total centers found: {len(centers)}")
    
    if centers:
        print(f"\n📋 Sample data with addresses:")
        for i, center in enumerate(centers[:10]):
            print(f"\n  Center {i+1}:")
            print(f"    Name: {center['name']}")
            print(f"    Address: {center['address']}")
            print(f"    Phone: {center['phone']}")
            print(f"    Types: {', '.join(center['types'])}")
            print(f"    Website: {center['website']}")
            print(f"    Source: {center['source']}")
    else:
        print("\n💡 To use this parser:")
        print("1. Place your Word document in data/official_documents/")
        print("2. Install python-docx: pip install python-docx")
        print("3. Run: python table_aware_parser.py")

if __name__ == "__main__":
    main()
