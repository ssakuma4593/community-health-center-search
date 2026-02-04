#!/usr/bin/env python3
"""
Utility function for parsing service types into boolean fields and normalized string.

This function is used by:
1. CSV transformation script (one-time data migration)
2. OpenAI enrichment process (when enriching new centers)
"""

import re
from typing import Dict, Optional


def parse_service_types(types_string: Optional[str]) -> Dict[str, any]:
    """
    Parse a comma-separated service types string into boolean fields and normalized string.
    
    Args:
        types_string: Comma-separated string of service types (e.g., "Primary Care, Dental, Vision")
    
    Returns:
        Dictionary with:
        - has_primary_care: bool
        - has_dental_care: bool
        - has_vision: bool
        - has_behavioral_health: bool
        - all_services: str (normalized, comma-separated)
    """
    if not types_string or not types_string.strip():
        return {
            'has_primary_care': False,
            'has_dental_care': False,
            'has_vision': False,
            'has_behavioral_health': False,
            'all_services': ''
        }
    
    # Normalize: lowercase, strip whitespace
    normalized = types_string.strip()
    
    # Split by comma or semicolon
    service_list = [s.strip() for s in re.split(r'[,;]', normalized) if s.strip()]
    
    # Normalize each service name for matching
    normalized_services = [s.lower() for s in service_list]
    
    # Define matching patterns for each service type
    primary_care_patterns = [
        'primary care',
        'internal medicine',
        'family medicine',
        'general practice',
        'family practice',
        'primary healthcare'
    ]
    
    dental_care_patterns = [
        'dental',
        'dentistry',
        'dental care',
        'oral health',
        'dental services'
    ]
    
    vision_patterns = [
        'vision',
        'eye care',
        'optometry',
        'ophthalmology',
        'eye services',
        'vision care',
        'visual'
    ]
    
    behavioral_health_patterns = [
        'behavioral health',
        'mental health',
        'psychiatry',
        'counseling',
        'therapy',
        'psychological',
        'psychology',
        'behavioral',
        'mental',
        'counseling services',
        'therapy services'
    ]
    
    # Check for matches
    has_primary_care = any(
        any(pattern in service for pattern in primary_care_patterns)
        for service in normalized_services
    )
    
    has_dental_care = any(
        any(pattern in service for pattern in dental_care_patterns)
        for service in normalized_services
    )
    
    has_vision = any(
        any(pattern in service for pattern in vision_patterns)
        for service in normalized_services
    )
    
    has_behavioral_health = any(
        any(pattern in service for pattern in behavioral_health_patterns)
        for service in normalized_services
    )
    
    # Create normalized all_services string (preserve original capitalization where reasonable)
    # Use original service names but ensure consistent formatting
    all_services = ', '.join(service_list)
    
    return {
        'has_primary_care': has_primary_care,
        'has_dental_care': has_dental_care,
        'has_vision': has_vision,
        'has_behavioral_health': has_behavioral_health,
        'all_services': all_services
    }


if __name__ == '__main__':
    # Test the function
    test_cases = [
        "Primary Care, Dental, Behavioral Health, Vision, Pharmacy",
        "Primary Care, Internal Medicine, Nurse Practitioner services",
        "Dental Care, Eye Care, Behavioral Health",
        "Vision",
        "",
        None,
        "Primary Care, Mental Health, Optometry, Dentistry"
    ]
    
    print("Testing parse_service_types function:\n")
    for test in test_cases:
        result = parse_service_types(test)
        print(f"Input: {test}")
        print(f"  Primary Care: {result['has_primary_care']}")
        print(f"  Dental Care: {result['has_dental_care']}")
        print(f"  Vision: {result['has_vision']}")
        print(f"  Behavioral Health: {result['has_behavioral_health']}")
        print(f"  All Services: {result['all_services']}")
        print()
