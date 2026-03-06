#!/usr/bin/env python3
"""Analyze the types column in the CSV to understand service type patterns."""
import csv
import re
from collections import Counter

csv_path = 'data/processed/community_health_centers_with_coords.csv'

types_set = set()
types_list = []

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        types_str = row.get('types', '').strip()
        if types_str:
            types_set.add(types_str)
            # Split by comma or semicolon
            split_types = [t.strip() for t in re.split(r'[,;]', types_str) if t.strip()]
            types_list.extend(split_types)

print("=== Sample types values (first 20) ===")
for t in sorted(list(types_set))[:20]:
    print(f"  - {t[:150]}")

print("\n=== Most common individual service types ===")
counter = Counter([t.lower() for t in types_list])
for k, v in counter.most_common(30):
    print(f"  {k}: {v}")

print("\n=== Checking for key service types ===")
key_types = ['primary care', 'dental', 'vision', 'eye care', 'behavioral health', 'mental health']
for key in key_types:
    matches = [t for t in types_list if key in t.lower()]
    print(f"  {key}: {len(matches)} matches")
    if matches:
        print(f"    Examples: {set(matches[:5])}")
