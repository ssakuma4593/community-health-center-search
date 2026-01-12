#!/usr/bin/env python3
"""
Interactive Vapi Setup Helper

This script helps guide you through the Vapi.ai setup process step by step.
"""

import os
import sys
import csv

def check_step(step_name, condition, success_msg, fail_msg):
    """Check if a setup step is completed."""
    print(f"\n{'='*60}")
    print(f"Step: {step_name}")
    print(f"{'='*60}")
    if condition():
        print(f"✅ {success_msg}")
        return True
    else:
        print(f"❌ {fail_msg}")
        return False

def check_api_key():
    """Check if VAPI_API_KEY is set."""
    return bool(os.getenv("VAPI_API_KEY"))

def check_csv_fields():
    """Check if CSV has call data fields."""
    csv_file = "../community_health_centers_with_coords.csv"
    if not os.path.exists(csv_file):
        return False
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames or []
            required_fields = [
                'accepting_new_patients',
                'has_waiting_list',
                'waiting_list_availability_date',
                'languages_supported'
            ]
            return all(field in fields for field in required_fields)
    except:
        return False

def check_dependencies():
    """Check if Python dependencies are installed."""
    try:
        import requests
        return True
    except ImportError:
        return False

def main():
    print("🚀 Vapi.ai Setup Helper")
    print("="*60)
    print("\nThis script will check your setup and guide you through any missing steps.")
    print("\nLet's check your setup...\n")
    
    steps_completed = 0
    total_steps = 4
    
    # Step 1: API Key
    if check_step(
        "1. VAPI_API_KEY Environment Variable",
        check_api_key,
        "API key is set!",
        "API key is not set. You need to:"
    ):
        steps_completed += 1
    else:
        print("\n   To set your API key:")
        print("   1. Sign up at https://vapi.ai")
        print("   2. Get your API key from the dashboard")
        print("   3. Run: export VAPI_API_KEY='your_key_here'")
        print("   4. (Optional) Add to ~/.zshrc to make it permanent")
    
    # Step 2: Dependencies
    if check_step(
        "2. Python Dependencies",
        check_dependencies,
        "Dependencies are installed!",
        "Dependencies are missing. Run: pip install -r vapi_requirements.txt"
    ):
        steps_completed += 1
    else:
        print("\n   To install dependencies:")
        print("   cd vapi")
        print("   pip install -r vapi_requirements.txt")
    
    # Step 3: CSV Fields
    if check_step(
        "3. CSV Call Data Fields",
        check_csv_fields,
        "CSV has call data fields!",
        "CSV fields not added. Run: python3 add_call_fields_to_csv.py ../community_health_centers_with_coords.csv"
    ):
        steps_completed += 1
    else:
        print("\n   To add call fields to CSV:")
        print("   cd vapi")
        print("   python3 add_call_fields_to_csv.py ../community_health_centers_with_coords.csv")
    
    # Step 4: Vapi Account (manual check)
    print(f"\n{'='*60}")
    print("Step: 4. Vapi.ai Account & Phone Number")
    print(f"{'='*60}")
    print("⚠️  Manual check required:")
    print("   1. Do you have a Vapi.ai account? (https://vapi.ai)")
    print("   2. Have you purchased/rented a phone number in the dashboard?")
    print("   (This is required to make outbound calls)")
    
    response = input("\n   Do you have both? (yes/no): ").lower().strip()
    if response in ['yes', 'y']:
        steps_completed += 1
        print("   ✅ Great!")
    else:
        print("   ⚠️  You'll need to:")
        print("      1. Sign up at https://vapi.ai")
        print("      2. Purchase/rent a phone number in the dashboard")
    
    # Summary
    print("\n" + "="*60)
    print("📊 Setup Summary")
    print("="*60)
    print(f"Completed: {steps_completed}/{total_steps} steps\n")
    
    if steps_completed == total_steps:
        print("🎉 All setup steps are complete!")
        print("\nNext steps:")
        print("1. (Optional) Set up webhook for local testing:")
        print("   - Start backend: cd backend && uvicorn app.main:app --reload")
        print("   - Start ngrok: ngrok http 8000")
        print("   - Set: export VAPI_WEBHOOK_URL='https://your-ngrok-url/webhooks/vapi'")
        print("\n2. Test with your phone:")
        print("   cd vapi")
        print("   python3 test_call.py 224-245-4540")
        print("\n3. Run full batch:")
        print("   python3 vapi_call_manager.py ../community_health_centers_with_coords.csv")
    else:
        print("⚠️  Please complete the missing steps above, then run this script again.")
        print("\nFor detailed instructions, see:")
        print("  - vapi/QUICK_START.md")
        print("  - vapi/VAPI_SETUP.md")

if __name__ == "__main__":
    main()
