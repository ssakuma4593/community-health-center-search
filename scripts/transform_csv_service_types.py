#!/usr/bin/env python3
"""
Transform CSV to add service type boolean fields and all_services column.

This script:
1. Reads the processed CSV file
2. Parses types column (prioritizing openai_types, then types, then final_types)
3. Adds boolean columns for filtering
4. Adds all_services column for display
5. Creates backup before transformation
6. Updates the CSV file
"""
import csv
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from utils.parse_service_types import parse_service_types

# Configuration
CSV_FILE = "data/processed/community_health_centers_with_coords.csv"
BACKUP_CSV = f"data/processed/community_health_centers_with_coords_backup_before_service_types_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
FRONTEND_CSV = "frontend/public/data/centers.csv"

# New columns to add
NEW_COLUMNS = [
    "has_primary_care",
    "has_dental_care",
    "has_vision",
    "has_behavioral_health",
    "has_pharmacy",
    "all_services"
]


def get_types_string(row: dict) -> str:
    """
    Get the types string from a row, using priority order:
    1. final_types (manually resolved)
    2. openai_types (AI enriched)
    3. types (original)
    """
    return (
        row.get('final_types', '').strip() or
        row.get('openai_types', '').strip() or
        row.get('types', '').strip() or
        ''
    )


def read_csv(file_path: str) -> list:
    """Read CSV file and return list of dictionaries."""
    rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def write_csv(file_path: str, rows: list, fieldnames: list):
    """Write CSV file from list of dictionaries."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def transform_row(row: dict) -> dict:
    """Transform a single row by parsing service types."""
    # Get types string using priority order
    types_string = get_types_string(row)
    
    # Parse service types
    parsed = parse_service_types(types_string)
    
    # Add new fields to row
    row['has_primary_care'] = 'true' if parsed['has_primary_care'] else 'false'
    row['has_dental_care'] = 'true' if parsed['has_dental_care'] else 'false'
    row['has_vision'] = 'true' if parsed['has_vision'] else 'false'
    row['has_behavioral_health'] = 'true' if parsed['has_behavioral_health'] else 'false'
    row['has_pharmacy'] = 'true' if parsed['has_pharmacy'] else 'false'
    row['all_services'] = parsed['all_services']
    
    return row


def main():
    """Main function to transform CSV."""
    print("=" * 80)
    print("Service Types CSV Transformation Script")
    print("=" * 80)
    print()
    
    # Check if input file exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file '{CSV_FILE}' not found.")
        sys.exit(1)
    
    # Create backup
    print(f"Creating backup: {BACKUP_CSV}")
    shutil.copy2(CSV_FILE, BACKUP_CSV)
    print("Backup created!")
    print()
    
    # Read CSV
    print(f"Reading CSV file: {CSV_FILE}")
    rows = read_csv(CSV_FILE)
    print(f"Found {len(rows)} health centers")
    print()
    
    if not rows:
        print("Error: CSV file is empty.")
        sys.exit(1)
    
    # Get existing fieldnames
    existing_fieldnames = list(rows[0].keys())
    
    # Add new columns if they don't exist
    all_fieldnames = existing_fieldnames.copy()
    for col in NEW_COLUMNS:
        if col not in all_fieldnames:
            all_fieldnames.append(col)
    
    # Initialize new columns for all rows (in case some already exist)
    for row in rows:
        for col in NEW_COLUMNS:
            if col not in row:
                row[col] = ''
    
    # Transform each row
    print("Transforming service types...")
    stats = {
        'has_primary_care': 0,
        'has_dental_care': 0,
        'has_vision': 0,
        'has_behavioral_health': 0,
        'has_pharmacy': 0,
        'has_all_services': 0
    }
    
    for i, row in enumerate(rows, 1):
        if i % 100 == 0:
            print(f"  Processing row {i}/{len(rows)}...")
        
        row = transform_row(row)
        
        # Update stats
        if row.get('has_primary_care') == 'true':
            stats['has_primary_care'] += 1
        if row.get('has_dental_care') == 'true':
            stats['has_dental_care'] += 1
        if row.get('has_vision') == 'true':
            stats['has_vision'] += 1
        if row.get('has_behavioral_health') == 'true':
            stats['has_behavioral_health'] += 1
        if row.get('has_pharmacy') == 'true':
            stats['has_pharmacy'] += 1
        if row.get('all_services'):
            stats['has_all_services'] += 1
    
    print("Transformation complete!")
    print()
    
    # Print statistics
    print("Statistics:")
    print(f"  Centers with Primary Care: {stats['has_primary_care']}")
    print(f"  Centers with Dental Care: {stats['has_dental_care']}")
    print(f"  Centers with Vision: {stats['has_vision']}")
    print(f"  Centers with Behavioral Health: {stats['has_behavioral_health']}")
    print(f"  Centers with Pharmacy: {stats['has_pharmacy']}")
    print(f"  Centers with any services listed: {stats['has_all_services']}")
    print()
    
    # Write transformed CSV
    print(f"Writing transformed CSV to: {CSV_FILE}")
    write_csv(CSV_FILE, rows, all_fieldnames)
    print("Done!")
    print()
    
    # Copy to frontend
    print(f"Copying to frontend: {FRONTEND_CSV}")
    os.makedirs(os.path.dirname(FRONTEND_CSV), exist_ok=True)
    write_csv(FRONTEND_CSV, rows, all_fieldnames)
    print("Done!")
    print()
    
    print("=" * 80)
    print("Transformation Complete!")
    print("=" * 80)
    print(f"Backup saved to: {BACKUP_CSV}")
    print(f"Updated CSV: {CSV_FILE}")
    print(f"Frontend CSV: {FRONTEND_CSV}")
    print()


if __name__ == "__main__":
    main()
