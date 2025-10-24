#!/usr/bin/env python3
"""
Final Table-Aware Merge Script
Uses table-aware document parser to extract data and merge with existing CSV,
checking for duplicates by address.
"""

import os
import json
import csv
import re
from typing import List, Dict, Optional, Set
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinalTableMergeScript:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.official_docs_dir = self.data_dir / "official_documents"
        self.existing_csv = "community_health_centers_targeted.csv"
        self.output_csv = "community_health_centers_final_with_addresses.csv"
        self.existing_centers = []
        self.document_centers = []
        self.merged_centers = []
        
    def load_existing_csv(self) -> List[Dict]:
        """Load existing centers from CSV"""
        if not os.path.exists(self.existing_csv):
            logger.warning(f"Existing CSV not found: {self.existing_csv}")
            return []
        
        centers = []
        with open(self.existing_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                centers.append(row)
        
        logger.info(f"Loaded {len(centers)} existing centers from CSV")
        return centers
    
    def parse_word_document_table_aware(self, file_path: str) -> List[Dict]:
        """Parse a Word document using table-aware extraction"""
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
    
    def normalize_address(self, address: str) -> str:
        """Normalize address for comparison"""
        if not address:
            return ""
        
        # Convert to lowercase and remove extra spaces
        normalized = address.lower().strip()
        
        # Remove common variations
        normalized = re.sub(r'\s+', ' ', normalized)  # Multiple spaces to single
        normalized = re.sub(r'[.,]', '', normalized)  # Remove periods and commas
        normalized = re.sub(r'\bst\b', 'street', normalized)  # Standardize street
        normalized = re.sub(r'\bave\b', 'avenue', normalized)  # Standardize avenue
        normalized = re.sub(r'\bblvd\b', 'boulevard', normalized)  # Standardize boulevard
        
        return normalized
    
    def is_duplicate_address(self, new_address: str, existing_addresses: Set[str]) -> bool:
        """Check if address already exists (case-insensitive)"""
        if not new_address:
            return False
        
        normalized_new = self.normalize_address(new_address)
        return normalized_new in existing_addresses
    
    def merge_data(self) -> List[Dict]:
        """Merge document data with existing CSV data"""
        # Load existing data
        self.existing_centers = self.load_existing_csv()
        
        # Parse all documents
        all_document_centers = []
        for doc_path in self.official_docs_dir.glob("*.docx"):
            centers = self.parse_word_document_table_aware(str(doc_path))
            all_document_centers.extend(centers)
        
        # Remove duplicates within document data
        self.document_centers = self.remove_duplicates(all_document_centers)
        
        # Create set of existing addresses for quick lookup
        existing_addresses = set()
        for center in self.existing_centers:
            if center.get('address'):
                normalized = self.normalize_address(center['address'])
                existing_addresses.add(normalized)
        
        # Start with existing centers
        merged_centers = self.existing_centers.copy()
        new_centers_count = 0
        
        # Add new centers from document
        for doc_center in self.document_centers:
            doc_address = doc_center.get('address', '')
            
            if not self.is_duplicate_address(doc_address, existing_addresses):
                # Convert types list to string for CSV compatibility
                if isinstance(doc_center.get('types'), list):
                    doc_center['types'] = ', '.join(doc_center['types'])
                
                merged_centers.append(doc_center)
                new_centers_count += 1
                
                # Add to existing addresses set to avoid duplicates within document
                if doc_address:
                    normalized = self.normalize_address(doc_address)
                    existing_addresses.add(normalized)
                
                logger.info(f"Added new center: {doc_center['name']} - {doc_address}")
            else:
                logger.info(f"Skipped duplicate address: {doc_center['name']} - {doc_address}")
        
        self.merged_centers = merged_centers
        logger.info(f"Merge complete: {len(merged_centers)} total centers ({new_centers_count} new from document)")
        
        return merged_centers
    
    def save_merged_csv(self):
        """Save merged data to CSV"""
        if not self.merged_centers:
            logger.warning("No merged data to save")
            return
        
        with open(self.output_csv, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['name', 'address', 'phone', 'types', 'website', 'source']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for center in self.merged_centers:
                # Ensure all fields are present
                row = {field: center.get(field, '') for field in fieldnames}
                writer.writerow(row)
        
        logger.info(f"Merged data saved to {self.output_csv}")
    
    def run(self):
        """Main method to merge document data with existing CSV"""
        logger.info("Starting final table-aware merge process...")
        
        # Merge data
        merged_centers = self.merge_data()
        
        if merged_centers:
            # Save merged data
            self.save_merged_csv()
            
            # Show summary
            existing_count = len(self.existing_centers)
            document_count = len(self.document_centers)
            merged_count = len(merged_centers)
            new_count = merged_count - existing_count
            
            print(f"\n=== FINAL TABLE-AWARE MERGE SUMMARY ===")
            print(f"Existing centers: {existing_count}")
            print(f"Document centers: {document_count}")
            print(f"New centers added: {new_count}")
            print(f"Total merged centers: {merged_count}")
            print(f"Output file: {self.output_csv}")
            
            if new_count > 0:
                print(f"\n📋 Sample new centers with addresses:")
                for center in self.merged_centers[-min(new_count, 10):]:
                    print(f"  - {center['name']} ({center.get('address', 'No address')})")
        else:
            logger.warning("No data to merge")
        
        return merged_centers

def main():
    """Main function"""
    merger = FinalTableMergeScript()
    centers = merger.run()
    
    if centers:
        print(f"\n✅ Final table-aware merge completed successfully!")
        print(f"📊 Total centers: {len(centers)}")
        print(f"📁 Output file: community_health_centers_final_with_addresses.csv")
    else:
        print("\n❌ Final merge failed. Check the logs for details.")

if __name__ == "__main__":
    main()
