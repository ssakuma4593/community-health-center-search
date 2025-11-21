#!/usr/bin/env python3
"""
Script to compare two CSV files and output statistics
"""

import csv
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple

def normalize_name(name: str) -> str:
    """Normalize health center name for comparison"""
    if not name:
        return ""
    normalized = name.lower().strip()
    normalized = re.sub(r'\s+', ' ', normalized)
    normalized = re.sub(r'[.,\-]', '', normalized)
    normalized = re.sub(r'\binc\b', '', normalized)
    normalized = re.sub(r'\bllc\b', '', normalized)
    normalized = re.sub(r'\bthe\b', '', normalized)
    return normalized.strip()

def normalize_address(address: str) -> str:
    """Normalize address for comparison"""
    if not address:
        return ""
    normalized = address.lower().strip()
    normalized = re.sub(r'\s+', ' ', normalized)
    normalized = re.sub(r'[.,]', '', normalized)
    normalized = re.sub(r'\bst\b', 'street', normalized)
    normalized = re.sub(r'\bave\b', 'avenue', normalized)
    normalized = re.sub(r'\bblvd\b', 'boulevard', normalized)
    normalized = re.sub(r'\brd\b', 'road', normalized)
    normalized = re.sub(r'\bdr\b', 'drive', normalized)
    normalized = re.sub(r'\bln\b', 'lane', normalized)
    normalized = re.sub(r'\bma\b', 'massachusetts', normalized)
    return normalized.strip()

def load_csv(csv_path: str) -> List[Dict]:
    """Load CSV file and return list of dictionaries"""
    if not Path(csv_path).exists():
        print(f"❌ Error: CSV file not found: {csv_path}")
        return []
    
    centers = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            centers.append(row)
    
    return centers

def create_normalized_set(centers: List[Dict]) -> Set[str]:
    """Create a set of normalized addresses for comparison"""
    normalized_set = set()
    for center in centers:
        address = normalize_address(center.get('address', ''))
        if address:  # Only add if we have an address
            normalized_set.add(address)
    return normalized_set

def compare_csvs(csv1_path: str, csv2_path: str, csv1_label: str = "CSV 1", csv2_label: str = "CSV 2"):
    """Compare two CSV files and output statistics"""
    
    print(f"Loading {csv1_label}...")
    centers1 = load_csv(csv1_path)
    if not centers1:
        return
    
    print(f"Loading {csv2_label}...")
    centers2 = load_csv(csv2_path)
    if not centers2:
        return
    
    # Create normalized sets for comparison
    set1 = create_normalized_set(centers1)
    set2 = create_normalized_set(centers2)
    
    # Find intersections and differences
    only_in_1 = set1 - set2
    only_in_2 = set2 - set1
    in_both = set1 & set2
    
    # Get actual center data for centers only in each set
    centers_only_in_1 = []
    centers_only_in_2 = []
    
    # Create lookup for centers based on normalized address
    lookup1 = {}
    for center in centers1:
        address_key = normalize_address(center.get('address', ''))
        if address_key and address_key not in lookup1:
            lookup1[address_key] = center
    
    lookup2 = {}
    for center in centers2:
        address_key = normalize_address(center.get('address', ''))
        if address_key and address_key not in lookup2:
            lookup2[address_key] = center
    
    # Get actual center data
    for address_key in only_in_1:
        if address_key in lookup1:
            centers_only_in_1.append(lookup1[address_key])
    
    for address_key in only_in_2:
        if address_key in lookup2:
            centers_only_in_2.append(lookup2[address_key])
    
    # Print results
    print("\n" + "="*80)
    print("CSV COMPARISON RESULTS")
    print("="*80)
    
    print(f"\n📊 SUMMARY STATISTICS")
    print(f"  Total number in {csv1_label}: {len(centers1)}")
    print(f"  Total number in {csv2_label}: {len(centers2)}")
    print(f"  Number in both: {len(in_both)}")
    print(f"  Number only in {csv1_label}: {len(only_in_1)}")
    print(f"  Number only in {csv2_label}: {len(only_in_2)}")
    
    print(f"\n📋 CENTERS ONLY IN {csv1_label.upper()} ({len(centers_only_in_1)} total):")
    if centers_only_in_1:
        # Get all fieldnames from the first center
        fieldnames = list(centers_only_in_1[0].keys()) if centers_only_in_1 else []
        for i, center in enumerate(centers_only_in_1, 1):
            print(f"\n  Row {i}:")
            for field in fieldnames:
                value = center.get(field, '')
                print(f"    {field}: {value}")
    else:
        print("  (None)")
    
    print(f"\n📋 CENTERS ONLY IN {csv2_label.upper()} ({len(centers_only_in_2)} total):")
    if centers_only_in_2:
        # Get all fieldnames from the first center
        fieldnames = list(centers_only_in_2[0].keys()) if centers_only_in_2 else []
        for i, center in enumerate(centers_only_in_2, 1):
            print(f"\n  Row {i}:")
            for field in fieldnames:
                value = center.get(field, '')
                print(f"    {field}: {value}")
    else:
        print("  (None)")
    
    print("\n" + "="*80)
    
    return {
        'total_csv1': len(centers1),
        'total_csv2': len(centers2),
        'in_both': len(in_both),
        'only_in_csv1': len(only_in_1),
        'only_in_csv2': len(only_in_2),
        'centers_only_in_csv1': centers_only_in_1,
        'centers_only_in_csv2': centers_only_in_2
    }

def main():
    csv1_path = "community_health_centers_scraped_fresh.csv"
    csv2_path = "hsn_active_health_centers_scraped.csv"
    
    compare_csvs(
        csv1_path, 
        csv2_path,
        csv1_label="community_health_centers_scraped_fresh.csv",
        csv2_label="hsn_active_health_centers_scraped.csv (DOCX scraped)"
    )

if __name__ == "__main__":
    main()

