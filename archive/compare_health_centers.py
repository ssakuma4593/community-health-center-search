#!/usr/bin/env python3
"""
Health Centers Comparison Tool
Compares two lists of health centers to find overlap and differences.
Can compare:
- Scraped data (from massleague website)
- Document-based data (from Word documents)
- New documents
"""

import csv
import re
from typing import List, Dict, Set, Tuple
from pathlib import Path
from collections import defaultdict
import difflib

class HealthCenterComparator:
    def __init__(self):
        self.scraped_centers = []
        self.document_centers = []
        self.normalized_scraped = {}
        self.normalized_document = {}
        
    def normalize_name(self, name: str) -> str:
        """Normalize health center name for comparison"""
        if not name:
            return ""
        
        # Convert to lowercase
        normalized = name.lower().strip()
        
        # Remove common variations
        normalized = re.sub(r'\s+', ' ', normalized)  # Multiple spaces to single
        normalized = re.sub(r'[.,\-]', '', normalized)  # Remove punctuation
        normalized = re.sub(r'\binc\b', '', normalized)  # Remove "Inc"
        normalized = re.sub(r'\bllc\b', '', normalized)  # Remove "LLC"
        normalized = re.sub(r'\bthe\b', '', normalized)  # Remove "the"
        
        return normalized.strip()
    
    def normalize_address(self, address: str) -> str:
        """Normalize address for comparison"""
        if not address:
            return ""
        
        # Convert to lowercase
        normalized = address.lower().strip()
        
        # Remove common variations
        normalized = re.sub(r'\s+', ' ', normalized)  # Multiple spaces to single
        normalized = re.sub(r'[.,]', '', normalized)  # Remove periods and commas
        normalized = re.sub(r'\bst\b', 'street', normalized)  # Standardize street
        normalized = re.sub(r'\bave\b', 'avenue', normalized)  # Standardize avenue
        normalized = re.sub(r'\bblvd\b', 'boulevard', normalized)  # Standardize boulevard
        normalized = re.sub(r'\brd\b', 'road', normalized)  # Standardize road
        normalized = re.sub(r'\bdr\b', 'drive', normalized)  # Standardize drive
        normalized = re.sub(r'\bln\b', 'lane', normalized)  # Standardize lane
        normalized = re.sub(r'\bma\b', 'massachusetts', normalized)  # Standardize state
        normalized = re.sub(r'\b\s+', ' ', normalized)  # Clean up spaces
        
        return normalized.strip()
    
    def build_address_from_parts(self, row: Dict) -> str:
        """Build full address from separate address fields"""
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
        
        return ', '.join(parts) if parts else row.get('address', '')
    
    def load_scraped_data(self, csv_path: str = "community_health_centers_final.csv") -> List[Dict]:
        """Load scraped data from CSV"""
        if not Path(csv_path).exists():
            print(f"⚠️  Scraped data file not found: {csv_path}")
            return []
        
        centers = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                centers.append(row)
        
        self.scraped_centers = centers
        
        # Create normalized lookup
        for center in centers:
            name = center.get('name', '')
            address = center.get('address', '')
            
            norm_name = self.normalize_name(name)
            norm_address = self.normalize_address(address)
            
            key = (norm_name, norm_address)
            if key not in self.normalized_scraped:
                self.normalized_scraped[key] = []
            self.normalized_scraped[key].append(center)
        
        print(f"✅ Loaded {len(centers)} centers from scraped data")
        return centers
    
    def load_document_data(self, csv_path: str = "community_health_centers_parsed.csv") -> List[Dict]:
        """Load document-based data from CSV"""
        if not Path(csv_path).exists():
            print(f"⚠️  Document data file not found: {csv_path}")
            return []
        
        centers = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Build full address if needed
                if 'address' not in row or not row['address']:
                    row['address'] = self.build_address_from_parts(row)
                centers.append(row)
        
        self.document_centers = centers
        
        # Create normalized lookup
        for center in centers:
            name = center.get('name', '')
            address = center.get('address', '')
            
            norm_name = self.normalize_name(name)
            norm_address = self.normalize_address(address)
            
            key = (norm_name, norm_address)
            if key not in self.normalized_document:
                self.normalized_document[key] = []
            self.normalized_document[key].append(center)
        
        print(f"✅ Loaded {len(centers)} centers from document data")
        return centers
    
    def find_matches(self, threshold: float = 0.8) -> Dict:
        """Find matches between scraped and document data"""
        matches = []
        scraped_only = []
        document_only = []
        similar_but_different = []
        
        # Find exact matches
        scraped_keys = set(self.normalized_scraped.keys())
        document_keys = set(self.normalized_document.keys())
        
        exact_matches = scraped_keys & document_keys
        
        for key in exact_matches:
            matches.append({
                'scraped': self.normalized_scraped[key][0],
                'document': self.normalized_document[key][0],
                'match_type': 'exact'
            })
        
        # Find centers only in scraped data
        scraped_only_keys = scraped_keys - document_keys
        for key in scraped_only_keys:
            scraped_only.extend(self.normalized_scraped[key])
        
        # Find centers only in document data
        document_only_keys = document_keys - scraped_keys
        for key in document_only_keys:
            document_only.extend(self.normalized_document[key])
        
        # Find similar matches (fuzzy matching)
        for scraped_key in scraped_only_keys:
            scraped_center = self.normalized_scraped[scraped_key][0]
            scraped_name = scraped_center.get('name', '')
            
            best_match = None
            best_score = 0
            
            for doc_key in document_only_keys:
                doc_center = self.normalized_document[doc_key][0]
                doc_name = doc_center.get('name', '')
                
                # Calculate similarity
                score = difflib.SequenceMatcher(None, 
                    self.normalize_name(scraped_name),
                    self.normalize_name(doc_name)).ratio()
                
                if score > best_score and score >= threshold:
                    best_score = score
                    best_match = doc_center
            
            if best_match:
                similar_but_different.append({
                    'scraped': scraped_center,
                    'document': best_match,
                    'similarity': best_score,
                    'match_type': 'similar'
                })
        
        return {
            'exact_matches': matches,
            'scraped_only': scraped_only,
            'document_only': document_only,
            'similar_matches': similar_but_different
        }
    
    def print_comparison_report(self, results: Dict):
        """Print a detailed comparison report"""
        print("\n" + "="*80)
        print("HEALTH CENTERS COMPARISON REPORT")
        print("="*80)
        
        exact_count = len(results['exact_matches'])
        scraped_only_count = len(results['scraped_only'])
        document_only_count = len(results['document_only'])
        similar_count = len(results['similar_matches'])
        
        total_scraped = len(self.scraped_centers)
        total_document = len(self.document_centers)
        
        print(f"\n📊 SUMMARY")
        print(f"  Scraped data: {total_scraped} centers")
        print(f"  Document data: {total_document} centers")
        print(f"  Exact matches: {exact_count}")
        print(f"  Only in scraped: {scraped_only_count}")
        print(f"  Only in document: {document_only_count}")
        print(f"  Similar (potential matches): {similar_count}")
        
        overlap_percent = (exact_count / max(total_scraped, total_document) * 100) if max(total_scraped, total_document) > 0 else 0
        print(f"\n  Overlap: {overlap_percent:.1f}%")
        
        # Show sample exact matches
        if results['exact_matches']:
            print(f"\n✅ EXACT MATCHES (showing first 5):")
            for i, match in enumerate(results['exact_matches'][:5], 1):
                print(f"\n  {i}. {match['scraped']['name']}")
                print(f"     Address: {match['scraped'].get('address', 'N/A')}")
                print(f"     Phone: {match['scraped'].get('phone', 'N/A')}")
        
        # Show sample scraped-only
        if results['scraped_only']:
            print(f"\n📋 ONLY IN SCRAPED DATA (showing first 10):")
            for i, center in enumerate(results['scraped_only'][:10], 1):
                print(f"  {i}. {center.get('name', 'N/A')}")
                print(f"     Address: {center.get('address', 'N/A')}")
        
        # Show sample document-only
        if results['document_only']:
            print(f"\n📄 ONLY IN DOCUMENT DATA (showing first 10):")
            for i, center in enumerate(results['document_only'][:10], 1):
                print(f"  {i}. {center.get('name', 'N/A')}")
                print(f"     Address: {center.get('address', 'N/A')}")
        
        # Show similar matches
        if results['similar_matches']:
            print(f"\n🔍 SIMILAR MATCHES (potential duplicates with variations):")
            for i, match in enumerate(results['similar_matches'][:5], 1):
                print(f"\n  {i}. Similarity: {match['similarity']:.2%}")
                print(f"     Scraped: {match['scraped']['name']}")
                print(f"     Document: {match['document']['name']}")
        
        print("\n" + "="*80)
    
    def save_detailed_report(self, results: Dict, output_file: str = "comparison_report.csv"):
        """Save detailed comparison to CSV"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['status', 'name', 'address', 'phone', 'source', 'match_name', 'match_address']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            # Write exact matches
            for match in results['exact_matches']:
                writer.writerow({
                    'status': 'EXACT_MATCH',
                    'name': match['scraped']['name'],
                    'address': match['scraped'].get('address', ''),
                    'phone': match['scraped'].get('phone', ''),
                    'source': 'both',
                    'match_name': match['document']['name'],
                    'match_address': match['document'].get('address', '')
                })
            
            # Write scraped-only
            for center in results['scraped_only']:
                writer.writerow({
                    'status': 'SCRAPED_ONLY',
                    'name': center.get('name', ''),
                    'address': center.get('address', ''),
                    'phone': center.get('phone', ''),
                    'source': 'scraped',
                    'match_name': '',
                    'match_address': ''
                })
            
            # Write document-only
            for center in results['document_only']:
                writer.writerow({
                    'status': 'DOCUMENT_ONLY',
                    'name': center.get('name', ''),
                    'address': center.get('address', ''),
                    'phone': center.get('phone', ''),
                    'source': 'document',
                    'match_name': '',
                    'match_address': ''
                })
            
            # Write similar matches
            for match in results['similar_matches']:
                writer.writerow({
                    'status': f'SIMILAR_{match["similarity"]:.0%}',
                    'name': match['scraped']['name'],
                    'address': match['scraped'].get('address', ''),
                    'phone': match['scraped'].get('phone', ''),
                    'source': 'scraped',
                    'match_name': match['document']['name'],
                    'match_address': match['document'].get('address', '')
                })
        
        print(f"\n💾 Detailed report saved to: {output_file}")
    
    def compare(self, scraped_csv: str = "community_health_centers_final.csv",
                document_csv: str = "community_health_centers_parsed.csv",
                similarity_threshold: float = 0.8):
        """Main comparison method"""
        print("🔍 Starting health centers comparison...")
        
        # Load data
        self.load_scraped_data(scraped_csv)
        self.load_document_data(document_csv)
        
        if not self.scraped_centers or not self.document_centers:
            print("❌ Cannot compare: missing data files")
            return None
        
        # Find matches
        print("\n🔎 Finding matches...")
        results = self.find_matches(threshold=similarity_threshold)
        
        # Print report
        self.print_comparison_report(results)
        
        # Save detailed report
        self.save_detailed_report(results)
        
        return results

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Compare health centers from different sources')
    parser.add_argument('--scraped', default='community_health_centers_final.csv',
                        help='Path to scraped data CSV')
    parser.add_argument('--document', default='community_health_centers_parsed.csv',
                        help='Path to document data CSV')
    parser.add_argument('--threshold', type=float, default=0.8,
                        help='Similarity threshold for fuzzy matching (0.0-1.0)')
    
    args = parser.parse_args()
    
    comparator = HealthCenterComparator()
    results = comparator.compare(
        scraped_csv=args.scraped,
        document_csv=args.document,
        similarity_threshold=args.threshold
    )
    
    if results:
        print("\n✅ Comparison complete!")
        print("\n💡 Next steps:")
        print("   1. Review the comparison_report.csv for detailed results")
        print("   2. Check 'EXACT_MATCH' entries to verify they're the same")
        print("   3. Review 'SIMILAR' entries - they might be duplicates with variations")
        print("   4. Decide which centers to keep from each source")

if __name__ == "__main__":
    main()

