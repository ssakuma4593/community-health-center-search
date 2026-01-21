#!/usr/bin/env python3
"""
Demo Script: OpenAI Enrichment

This script demonstrates the OpenAI enrichment feature by:
1. Starting the backend server (if not running)
2. Testing enrichment on a single health center
3. Showing before/after comparison

Usage:
    python scripts/demos/demo_openai_enrichment.py

Requirements:
    - Backend server running (or script will try to start it)
    - OPENAI_API_KEY set in backend/.env
"""

import sys
import os
import json
import requests
import time
from pathlib import Path

# Add parent directories to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

API_BASE_URL = "http://localhost:8000"
ENRICHMENT_ENDPOINT = f"{API_BASE_URL}/api/enrich-center"

# Demo health center data
DEMO_CENTER = {
    "name": "Fenway Health - South End",
    "website": "https://fenwayhealth.org",
    "existing_address": "142 Berkley Street, Boston, MA 02116",
    "existing_phone": "(617) 247-7555",
    "existing_types": "Primary Care, LGBTQ+ Health"
}

def check_backend_running():
    """Check if backend is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def print_header():
    """Print demo header."""
    print("\n" + "="*80)
    print("🤖 OpenAI Enrichment Demo")
    print("="*80)
    print("\nThis demo shows how OpenAI enriches health center data with:")
    print("  • Verified phone numbers and addresses")
    print("  • New patient instructions")
    print("  • Additional helpful notes")
    print("  • Confidence scores")
    print("\n" + "-"*80 + "\n")

def print_original_data():
    """Print original data."""
    print("📋 ORIGINAL DATA:")
    print("-" * 80)
    print(f"Name:    {DEMO_CENTER['name']}")
    print(f"Address: {DEMO_CENTER['existing_address']}")
    print(f"Phone:   {DEMO_CENTER['existing_phone']}")
    print(f"Website: {DEMO_CENTER['website']}")
    print(f"Types:   {DEMO_CENTER['existing_types']}")
    print("\n")

def call_enrichment_api():
    """Call the enrichment API."""
    print("🔄 Calling OpenAI Enrichment API...")
    print(f"   Endpoint: {ENRICHMENT_ENDPOINT}\n")
    
    try:
        response = requests.post(
            ENRICHMENT_ENDPOINT,
            json=DEMO_CENTER,
            timeout=120  # OpenAI can take a while
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Error {response.status_code}: {response.text}"
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to backend. Make sure it's running!"
    except Exception as e:
        return False, str(e)

def print_enriched_data(enriched_data):
    """Print enriched data."""
    print("✨ ENRICHED DATA:")
    print("-" * 80)
    print(f"Phone:     {enriched_data.get('openai_phone', 'N/A')}")
    print(f"Address:   {enriched_data.get('openai_address', 'N/A')}")
    print(f"Website:   {enriched_data.get('openai_website', 'N/A')}")
    print(f"Types:     {enriched_data.get('openai_types', 'N/A')}")
    print(f"Confidence: {enriched_data.get('openai_confidence', 'N/A')}")
    
    if enriched_data.get('openai_new_patient_md'):
        print("\n📝 New Patient Instructions:")
        print("-" * 80)
        instructions = enriched_data['openai_new_patient_md']
        # Show first 300 chars
        preview = instructions[:300] + "..." if len(instructions) > 300 else instructions
        print(preview)
    
    if enriched_data.get('openai_other_notes_md'):
        print("\n💡 Additional Notes:")
        print("-" * 80)
        notes = enriched_data['openai_other_notes_md']
        preview = notes[:200] + "..." if len(notes) > 200 else notes
        print(preview)
    
    if enriched_data.get('openai_source_urls'):
        print(f"\n🔗 Sources: {enriched_data['openai_source_urls']}")
    
    print("\n")

def print_comparison(enriched_data):
    """Print before/after comparison."""
    print("📊 COMPARISON:")
    print("-" * 80)
    
    comparisons = [
        ("Phone", DEMO_CENTER['existing_phone'], enriched_data.get('openai_phone', 'N/A')),
        ("Address", DEMO_CENTER['existing_address'], enriched_data.get('openai_address', 'N/A')),
        ("Website", DEMO_CENTER['website'], enriched_data.get('openai_website', 'N/A')),
        ("Types", DEMO_CENTER['existing_types'], enriched_data.get('openai_types', 'N/A')),
    ]
    
    for field, original, enriched in comparisons:
        match = "✅" if original == enriched else "🔄"
        print(f"{match} {field:10} | Original: {original[:40]}")
        print(f"           | Enriched: {enriched[:40]}")
        print()

def main():
    """Main demo function."""
    print_header()
    
    # Check if backend is running
    print("🔍 Checking if backend is running...")
    if not check_backend_running():
        print("❌ Backend server is not running!")
        print("\nTo start the backend:")
        print("  1. cd backend")
        print("  2. Make sure OPENAI_API_KEY is set in .env")
        print("  3. uvicorn app.main:app --reload")
        print("\nThen run this demo again.")
        sys.exit(1)
    
    print("✅ Backend is running!\n")
    
    # Show original data
    print_original_data()
    
    # Call enrichment API
    success, result = call_enrichment_api()
    
    if not success:
        print(f"❌ Error: {result}")
        sys.exit(1)
    
    # Show enriched data
    print_enriched_data(result)
    
    # Show comparison
    print_comparison(result)
    
    # Summary
    print("="*80)
    print("✅ Demo Complete!")
    print("="*80)
    print("\nKey Takeaways:")
    print("  • OpenAI verifies and enriches health center data")
    print("  • Provides new patient instructions from web search")
    print("  • Includes confidence scores for data quality")
    print("  • Can be used to improve data accuracy")
    print("\n")

if __name__ == "__main__":
    main()
