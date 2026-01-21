#!/usr/bin/env python3
"""
Script to enrich health center CSV data using OpenAI Responses API.

This script:
1. Creates a backup of the original CSV file
2. Reads the CSV file
3. For each center, calls the OpenAI enrichment API endpoint
4. Adds new columns with enriched data directly to the original CSV file
5. Generates a comparison report for manual review
"""
import csv
import os
import sys
import time
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
ENRICHMENT_ENDPOINT = f"{API_BASE_URL}/api/enrich-center"
CSV_FILE = "data/processed/community_health_centers_with_coords.csv"
ENRICHED_CSV = "data/processed/community_health_centers_enriched.csv"
BACKUP_CSV = "data/processed/community_health_centers_with_coords_backup_before_enrichment.csv"
COMPARISON_REPORT = "reports/enrichment_comparison_report.txt"
DELAY_BETWEEN_REQUESTS = 1.0  # seconds - be respectful to the API

# New columns to add
OPENAI_COLUMNS = [
    "openai_phone",
    "openai_address",
    "openai_website",
    "openai_types",
    "openai_new_patient_md",
    "openai_other_notes_md",
    "openai_source_urls",
    "openai_last_checked_utc",
    "openai_confidence",
]

# Resolved columns (for manual review)
RESOLVED_COLUMNS = [
    "final_phone",
    "final_address",
    "final_website",
    "final_types",
    "final_new_patient_md",
]


def read_csv(file_path: str) -> List[Dict[str, str]]:
    """Read CSV file and return list of dictionaries."""
    rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def write_csv(file_path: str, rows: List[Dict[str, str]], fieldnames: List[str]):
    """Write CSV file from list of dictionaries."""
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_address(row: Dict[str, str]) -> str:
    """Build full address from CSV row."""
    parts = []
    if row.get('street_address_1'):
        parts.append(row['street_address_1'])
    if row.get('street_address_2'):
        parts.append(row['street_address_2'])
    if row.get('city_town'):
        parts.append(row['city_town'])
    if row.get('state'):
        parts.append(row['state'])
    if row.get('zipcode'):
        parts.append(row['zipcode'])
    return ', '.join(parts)


def enrich_center(row: Dict[str, str]) -> Dict[str, str]:
    """
    Call the enrichment API endpoint for a single center.
    
    Returns enriched data dictionary.
    """
    # Prepare request data
    request_data = {
        "name": row.get('name', ''),
        "website": row.get('website', '') or None,
        "existing_address": build_address(row),
        "existing_phone": row.get('phone', '') or None,
        "existing_types": row.get('types', '') or None,
    }
    
    try:
        response = requests.post(
            ENRICHMENT_ENDPOINT,
            json=request_data,
            timeout=60  # OpenAI API can take a while
        )
        response.raise_for_status()
        enriched_data = response.json()
        
        # Add timestamp
        enriched_data['openai_last_checked_utc'] = datetime.utcnow().isoformat() + 'Z'
        
        return enriched_data
        
    except requests.exceptions.RequestException as e:
        print(f"  Error calling API: {e}")
        return {col: '' for col in OPENAI_COLUMNS}


def compare_data(row: Dict[str, str]) -> Dict[str, str]:
    """
    Compare original data with OpenAI enriched data.
    
    Returns a dictionary with comparison flags and notes.
    """
    comparison = {
        "phone_match": False,
        "address_match": False,
        "types_match": False,
        "discrepancies": [],
    }
    
    # Compare phone
    original_phone = (row.get('phone') or '').strip()
    openai_phone = (row.get('openai_phone') or '').strip()
    if original_phone and openai_phone:
        # Normalize phone numbers for comparison
        orig_normalized = ''.join(filter(str.isdigit, original_phone))
        openai_normalized = ''.join(filter(str.isdigit, openai_phone))
        comparison['phone_match'] = orig_normalized == openai_normalized
        if not comparison['phone_match']:
            comparison['discrepancies'].append(
                f"Phone mismatch: '{original_phone}' vs '{openai_phone}'"
            )
    
    # Compare address
    original_address = build_address(row).strip()
    openai_address = (row.get('openai_address') or '').strip()
    if original_address and openai_address:
        # Simple comparison - could be improved
        comparison['address_match'] = original_address.lower() == openai_address.lower()
        if not comparison['address_match']:
            comparison['discrepancies'].append(
                f"Address mismatch: '{original_address}' vs '{openai_address}'"
            )
    
    # Compare types
    original_types = (row.get('types') or '').strip()
    openai_types = (row.get('openai_types') or '').strip()
    if original_types and openai_types:
        # Simple comparison - could be improved
        comparison['types_match'] = original_types.lower() == openai_types.lower()
        if not comparison['types_match']:
            comparison['discrepancies'].append(
                f"Types mismatch: '{original_types}' vs '{openai_types}'"
            )
    
    return comparison


def generate_comparison_report(rows: List[Dict[str, str]], output_file: str):
    """Generate a comparison report for manual review."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("HEALTH CENTER ENRICHMENT COMPARISON REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"Total Centers: {len(rows)}\n\n")
        
        # Count discrepancies
        discrepancies_count = 0
        low_confidence_count = 0
        
        for i, row in enumerate(rows, 1):
            comparison = compare_data(row)
            confidence = (row.get('openai_confidence') or '').strip()
            
            has_discrepancies = len(comparison['discrepancies']) > 0
            is_low_confidence = confidence.lower() == 'low'
            
            if has_discrepancies or is_low_confidence:
                discrepancies_count += 1
                if is_low_confidence:
                    low_confidence_count += 1
                
                f.write(f"\n{'=' * 80}\n")
                f.write(f"CENTER #{i}: {row.get('name', 'Unknown')}\n")
                f.write(f"{'=' * 80}\n\n")
                
                f.write(f"Original Data:\n")
                f.write(f"  Name: {row.get('name', '')}\n")
                f.write(f"  Address: {build_address(row)}\n")
                f.write(f"  Phone: {row.get('phone', '')}\n")
                f.write(f"  Types: {row.get('types', '')}\n")
                f.write(f"  Website: {row.get('website', '')}\n\n")
                
                f.write(f"OpenAI Enriched Data:\n")
                f.write(f"  Phone: {row.get('openai_phone', '')}\n")
                f.write(f"  Address: {row.get('openai_address', '')}\n")
                f.write(f"  Website: {row.get('openai_website', '')}\n")
                f.write(f"  Types: {row.get('openai_types', '')}\n")
                f.write(f"  Confidence: {confidence}\n")
                f.write(f"  Source URLs: {row.get('openai_source_urls', '')}\n\n")
                
                if comparison['discrepancies']:
                    f.write(f"DISCREPANCIES:\n")
                    for disc in comparison['discrepancies']:
                        f.write(f"  - {disc}\n")
                    f.write("\n")
                
                if row.get('openai_new_patient_md'):
                    f.write(f"New Patient Instructions:\n")
                    f.write(f"{row.get('openai_new_patient_md', '')}\n\n")
                
                if row.get('openai_other_notes_md'):
                    f.write(f"Other Notes:\n")
                    f.write(f"{row.get('openai_other_notes_md', '')}\n\n")
        
        f.write(f"\n{'=' * 80}\n")
        f.write(f"SUMMARY\n")
        f.write(f"{'=' * 80}\n")
        f.write(f"Total centers with discrepancies: {discrepancies_count}\n")
        f.write(f"Total centers with low confidence: {low_confidence_count}\n")
        f.write(f"\nPlease review the discrepancies above and update the 'final_*' columns\n")
        f.write(f"in the enriched CSV file with the resolved values.\n")


def main():
    """Main function to enrich CSV data."""
    print("=" * 80)
    print("Health Center CSV Enrichment Script")
    print("=" * 80)
    print()
    
    # Check if input file exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file '{CSV_FILE}' not found.")
        sys.exit(1)
    
    # Create backup before enrichment
    print(f"Creating backup: {BACKUP_CSV}")
    import shutil
    shutil.copy2(CSV_FILE, BACKUP_CSV)
    print("Backup created!")
    print()
    
    # Read CSV
    print(f"Reading CSV file: {CSV_FILE}")
    rows = read_csv(CSV_FILE)
    print(f"Found {len(rows)} health centers")
    print()
    
    # Get existing fieldnames
    if rows:
        existing_fieldnames = list(rows[0].keys())
    else:
        print("Error: CSV file is empty.")
        sys.exit(1)
    
    # Add new columns if they don't exist
    all_fieldnames = existing_fieldnames.copy()
    for col in OPENAI_COLUMNS + RESOLVED_COLUMNS:
        if col not in all_fieldnames:
            all_fieldnames.append(col)
    
    # Initialize new columns for all rows
    for row in rows:
        for col in OPENAI_COLUMNS + RESOLVED_COLUMNS:
            if col not in row:
                row[col] = ''
    
    # Enrich each center
    print("Starting enrichment process...")
    print(f"API Endpoint: {ENRICHMENT_ENDPOINT}")
    print(f"Delay between requests: {DELAY_BETWEEN_REQUESTS}s")
    print()
    
    for i, row in enumerate(rows, 1):
        name = row.get('name', 'Unknown')
        print(f"[{i}/{len(rows)}] Enriching: {name}")
        
        enriched_data = enrich_center(row)
        
        # Update row with enriched data
        for col in OPENAI_COLUMNS:
            if col in enriched_data:
                row[col] = enriched_data.get(col, '')
        
        # Wait before next request
        if i < len(rows):
            time.sleep(DELAY_BETWEEN_REQUESTS)
    
    print()
    print("Enrichment complete!")
    print()
    
    # Write enriched data to a new CSV file
    print(f"Writing enriched data to: {ENRICHED_CSV}")
    write_csv(ENRICHED_CSV, rows, all_fieldnames)
    print("Done!")
    print()
    
    # Generate comparison report
    print(f"Generating comparison report: {COMPARISON_REPORT}")
    generate_comparison_report(rows, COMPARISON_REPORT)
    print("Done!")
    print()
    
    print("=" * 80)
    print("Next Steps:")
    print("1. Review the comparison report:", COMPARISON_REPORT)
    print("2. Manually resolve discrepancies in:", CSV_FILE)
    print("3. Update the 'final_*' columns with resolved values")
    print("4. Copy the CSV to frontend/public/data/centers.csv")
    print("=" * 80)
    print(f"\nNote: Original file backed up to: {BACKUP_CSV}")


if __name__ == "__main__":
    main()
