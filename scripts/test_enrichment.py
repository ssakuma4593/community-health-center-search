#!/usr/bin/env python3
"""
Quick test script to test OpenAI enrichment with a few CSV entries.
Saves results to a JSON file for review.
"""
import csv
import requests
import json
import os
from pathlib import Path
from datetime import datetime

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
ENRICHMENT_ENDPOINT = "{}/api/enrich-center".format(API_BASE_URL)
INPUT_CSV = "data/processed/community_health_centers_with_coords.csv"
OUTPUT_JSON = "reports/test_enrichment_results.json"
NUM_TO_TEST = 3

def build_address(row):
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

def test_enrichment(row):
    """Test enrichment for a single row."""
    name = row.get('name', 'Unknown')
    print("\n" + "="*80)
    print("Testing: {}".format(name))
    print("="*80)
    
    # Prepare request data
    request_data = {
        "name": name,
        "website": row.get('website', '') or None,
        "existing_address": build_address(row),
        "existing_phone": row.get('phone', '') or None,
        "existing_types": row.get('types', '') or None,
    }
    
    print("\nRequest Data:")
    print(json.dumps(request_data, indent=2))
    
    try:
        print("\nCalling API: {}".format(ENRICHMENT_ENDPOINT))
        response = requests.post(
            ENRICHMENT_ENDPOINT,
            json=request_data,
            timeout=120  # OpenAI API can take a while
        )
        
        print("Response Status: {}".format(response.status_code))
        
        if response.status_code == 200:
            enriched_data = response.json()
            print("\n✅ Enrichment Successful!")
            print("\nEnriched Data:")
            print(json.dumps(enriched_data, indent=2))
            
            # Show comparison
            print("\n" + "─"*80)
            print("COMPARISON:")
            print("─"*80)
            print("Phone:     '{}' → '{}'".format(row.get('phone', ''), enriched_data.get('openai_phone', '')))
            print("Address:   '{}' → '{}'".format(build_address(row), enriched_data.get('openai_address', '')))
            print("Website:   '{}' → '{}'".format(row.get('website', ''), enriched_data.get('openai_website', '')))
            print("Types:     '{}' → '{}'".format(row.get('types', ''), enriched_data.get('openai_types', '')))
            print("Confidence: {}".format(enriched_data.get('openai_confidence', 'N/A')))
            
            if enriched_data.get('openai_new_patient_md'):
                print("\nNew Patient Instructions (first 200 chars):")
                print(enriched_data.get('openai_new_patient_md', '')[:200] + "...")
            
            # Return both success status and enriched data
            return True, enriched_data
        else:
            print("❌ Error: {}".format(response.status_code))
            print("Response: {}".format(response.text))
            return False, None
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API at {}".format(ENRICHMENT_ENDPOINT))
        print("Make sure the backend server is running:")
        print("  cd backend && uvicorn app.main:app --reload")
        return False, None
    except Exception as e:
        print("❌ Error: {}".format(e))
        return False, None

def main():
    """Main function."""
    print("="*80)
    print("OpenAI Enrichment Test Script")
    print("="*80)
    
    # Check if CSV exists
    if not os.path.exists(INPUT_CSV):
        print("Error: Input file '{}' not found.".format(INPUT_CSV))
        return
    
    # Read CSV
    print("\nReading CSV: {}".format(INPUT_CSV))
    rows = []
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Filter rows that have at least name and some contact info
    valid_rows = [
        row for row in rows 
        if row.get('name') and (row.get('phone') or row.get('website') or build_address(row))
    ]
    
    if not valid_rows:
        print("No valid rows found in CSV.")
        return
    
    # Take first N valid rows
    test_rows = valid_rows[:NUM_TO_TEST]
    print("Found {} valid rows. Testing {} entries.\n".format(len(valid_rows), len(test_rows)))
    
    # Test each row
    results = []
    enriched_results = []
    
    for i, row in enumerate(test_rows, 1):
        print("\n[{}]".format(i))
        success, enriched_data = test_enrichment(row)
        results.append((row.get('name', 'Unknown'), success))
        
        if success and enriched_data:
            # Combine original row with enriched data
            result_entry = {
                "original": {
                    "name": row.get('name', ''),
                    "address": build_address(row),
                    "phone": row.get('phone', ''),
                    "website": row.get('website', ''),
                    "types": row.get('types', ''),
                },
                "enriched": enriched_data,
                "timestamp": datetime.utcnow().isoformat() + 'Z'
            }
            enriched_results.append(result_entry)
    
    # Save results to JSON file
    output_data = {
        "test_date": datetime.now().isoformat(),
        "total_tested": len(test_rows),
        "successful": sum(1 for _, s in results if s),
        "results": enriched_results
    }
    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    for name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print("{}: {}".format(status, name))
    
    print("\nTotal: {}/{} successful".format(sum(1 for _, s in results if s), len(results)))
    print("\n✅ Results saved to: {}".format(OUTPUT_JSON))

if __name__ == "__main__":
    main()
