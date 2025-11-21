#!/usr/bin/env python3
"""
Parse New Document and Compare with Existing Data
Parses a new Word document and compares it with existing health center data.
"""

import sys
from pathlib import Path
from final_document_parser import TableAwareParser
from compare_health_centers import HealthCenterComparator
import csv

def parse_new_document(document_path: str, output_csv: str = "new_document_parsed.csv"):
    """Parse a new Word document"""
    print(f"📄 Parsing new document: {document_path}")
    
    parser = TableAwareParser()
    centers = parser.parse_word_document(document_path)
    
    if not centers:
        print("❌ No health centers found in document")
        return None
    
    # Remove duplicates
    centers = parser.remove_duplicates(centers)
    
    # Save to CSV
    output_path = Path(output_csv)
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'address', 'phone', 'types', 'website', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for center in centers:
            center_copy = center.copy()
            if isinstance(center.get('types'), list):
                center_copy['types'] = ', '.join(center['types'])
            writer.writerow(center_copy)
    
    print(f"✅ Parsed {len(centers)} health centers from document")
    print(f"💾 Saved to: {output_csv}")
    
    return output_csv

def compare_with_existing(new_document_csv: str, 
                         existing_scraped: str = "community_health_centers_final.csv",
                         existing_document: str = "community_health_centers_parsed.csv"):
    """Compare new document data with existing data"""
    print("\n🔍 Comparing new document with existing data...")
    
    # Compare with scraped data
    print("\n" + "="*80)
    print("COMPARISON 1: New Document vs Scraped Data")
    print("="*80)
    comparator1 = HealthCenterComparator()
    comparator1.load_scraped_data(existing_scraped)
    comparator1.load_document_data(new_document_csv)
    results1 = comparator1.find_matches()
    comparator1.print_comparison_report(results1)
    comparator1.save_detailed_report(results1, "new_doc_vs_scraped_report.csv")
    
    # Compare with existing document data
    print("\n" + "="*80)
    print("COMPARISON 2: New Document vs Existing Document Data")
    print("="*80)
    comparator2 = HealthCenterComparator()
    comparator2.load_document_data(existing_document)  # Treat as "scraped" for comparison
    comparator2.load_document_data(new_document_csv)
    results2 = comparator2.find_matches()
    comparator2.print_comparison_report(results2)
    comparator2.save_detailed_report(results2, "new_doc_vs_existing_doc_report.csv")
    
    return results1, results2

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python parse_and_compare_new_document.py <document_path>")
        print("\nExample:")
        print("  python parse_and_compare_new_document.py data/official_documents/new_document.docx")
        sys.exit(1)
    
    document_path = sys.argv[1]
    
    if not Path(document_path).exists():
        print(f"❌ Document not found: {document_path}")
        sys.exit(1)
    
    # Step 1: Parse the new document
    new_csv = parse_new_document(document_path)
    
    if not new_csv:
        sys.exit(1)
    
    # Step 2: Compare with existing data
    results = compare_with_existing(new_csv)
    
    if results1 and results2:
        print("\n✅ Analysis complete!")
        print("\n📊 Summary:")
        print(f"   - New document centers: {len(comparator1.document_centers)}")
        print(f"\n   vs Scraped Data:")
        print(f"     - Exact matches: {len(results1['exact_matches'])}")
        print(f"     - New centers (not in scraped): {len(results1['document_only'])}")
        print(f"     - In scraped but not in new doc: {len(results1['scraped_only'])}")
        print(f"\n   vs Existing Document Data:")
        print(f"     - Exact matches: {len(results2['exact_matches'])}")
        print(f"     - New centers (not in existing doc): {len(results2['document_only'])}")
        print(f"     - In existing doc but not in new doc: {len(results2['scraped_only'])}")

if __name__ == "__main__":
    main()

