#!/usr/bin/env python3
"""
Community Health Center Scraper Runner
Uses the production-ready targeted structure scraper
"""

import sys
import os

def main():
    print("Community Health Center Scraper")
    print("==============================")
    print("Using the production-ready scraper that:")
    print("  ✓ Targets the specific wpgb-card structure")
    print("  ✓ Handles JavaScript-rendered content")
    print("  ✓ Clicks through pagination automatically")
    print("  ✓ Extracts ~15 centers per page across 9 pages")
    print("  ✓ Finds ~123 total community health centers")
    print("  ✓ Exports to JSON and CSV")
    
    print("\n⚠️  Requirements:")
    print("   - ChromeDriver installed: brew install chromedriver")
    print("   - Selenium installed: pip install selenium")
    
    print("\n🚀 Starting scraper...")
    
    try:
        from community_health_scraper import TargetedStructureScraper
        scraper = TargetedStructureScraper(headless=True)
        centers = scraper.run()
        
        print(f"\n✅ Scraping completed!")
        print(f"📊 Found {len(centers)} community health centers")
        print(f"📁 Data saved to:")
        print(f"   - community_health_centers_targeted.json")
        print(f"   - community_health_centers_targeted.csv")
        
        if centers:
            print(f"\n📋 Sample data:")
            for i, center in enumerate(centers[:5]):
                print(f"\n  Center {i+1}:")
                print(f"    Name: {center['name']}")
                print(f"    Address: {center['address']}")
                print(f"    Phone: {center['phone']}")
                print(f"    Types: {', '.join(center['types'])}")
                print(f"    Website: {center['website']}")
        else:
            print("\n⚠️  No centers found. Check ChromeDriver installation.")
            
    except ImportError as e:
        print(f"\n❌ Error: {e}")
        print("   Install Selenium: pip install selenium")
        print("   Install ChromeDriver: brew install chromedriver")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Check ChromeDriver installation and try again.")

if __name__ == "__main__":
    main()
