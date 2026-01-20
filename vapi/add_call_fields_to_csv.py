#!/usr/bin/env python3
"""
Add Call Data Fields to CSV

This script adds new columns to the existing CSV file for storing call data:
- accepting_new_patients
- has_waiting_list
- waiting_list_availability_date
- languages_supported
- call_notes
- last_called_date
- call_status
"""

import csv
import sys
import os
from pathlib import Path


def add_call_fields_to_csv(csv_file: str, backup: bool = True):
    """
    Add new call data fields to existing CSV file.
    
    Args:
        csv_file: Path to CSV file
        backup: Whether to create a backup before modifying
    """
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return False
    
    # New fields to add
    new_fields = [
        'accepting_new_patients',
        'has_waiting_list',
        'waiting_list_availability_date',
        'languages_supported',
        'call_notes',
        'last_called_date',
        'call_status'
    ]
    
    # Create backup if requested
    if backup:
        backup_file = csv_file.replace('.csv', '_backup.csv')
        import shutil
        shutil.copy2(csv_file, backup_file)
        print(f"✅ Backup created: {backup_file}")
    
    # Read existing CSV
    rows = []
    existing_fieldnames = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_fieldnames = reader.fieldnames or []
            rows = list(reader)
    except Exception as e:
        print(f"❌ Error reading CSV: {str(e)}")
        return False
    
    # Check which fields need to be added
    fields_to_add = [field for field in new_fields if field not in existing_fieldnames]
    
    if not fields_to_add:
        print("✅ All call data fields already exist in CSV")
        return True
    
    print(f"📝 Adding {len(fields_to_add)} new fields: {', '.join(fields_to_add)}")
    
    # Add new fields to fieldnames
    new_fieldnames = existing_fieldnames + fields_to_add
    
    # Add empty values for new fields in existing rows
    for row in rows:
        for field in fields_to_add:
            row[field] = ''
    
    # Write updated CSV
    try:
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=new_fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"✅ Successfully added fields to {csv_file}")
        print(f"   Total rows: {len(rows)}")
        return True
        
    except Exception as e:
        print(f"❌ Error writing CSV: {str(e)}")
        return False


def main():
    """Main function."""
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "community_health_centers_with_coords.csv"
    
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        print("   Usage: python add_call_fields_to_csv.py [csv_file_path]")
        sys.exit(1)
    
    print(f"📄 Processing: {csv_file}")
    success = add_call_fields_to_csv(csv_file)
    
    if success:
        print("✅ Done!")
    else:
        print("❌ Failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()



