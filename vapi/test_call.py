#!/usr/bin/env python3
"""
Test Call Script for Vapi.ai

This script makes a single test call to verify the Vapi.ai integration is working.
"""

import os
import sys
import time

# Add the vapi directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vapi_call_manager import VapiCallManager

def print_data_structure():
    """Print the data structure that will be captured from the call."""
    print("📊 Data Structure to be Captured:")
    print("=" * 80)
    print("")
    print("The following information will be saved to the CSV:")
    print("")
    print("  • accepting_new_patients:")
    print("      Values: 'yes', 'no', or 'unknown'")
    print("      Question: 'Are you currently taking new patients?'")
    print("")
    print("  • has_waiting_list:")
    print("      Values: 'yes', 'no', or 'unknown'")
    print("      Question: 'Is there a waiting list?'")
    print("")
    print("  • waiting_list_availability_date:")
    print("      Values: Date string (e.g., 'March 2025') or 'N/A'")
    print("      Question: 'When do you expect availability?'")
    print("")
    print("  • languages_supported:")
    print("      Values: Comma-separated list of: 'spanish', 'portuguese', 'haitian-creole'")
    print("      Question: 'Do your providers speak Spanish, Portuguese, or Haitian Creole?'")
    print("")
    print("  • call_notes:")
    print("      Values: Free text with any additional information")
    print("")
    print("  • last_called_date:")
    print("      Values: Timestamp (e.g., '2024-01-15 14:30:00')")
    print("")
    print("  • call_status:")
    print("      Values: 'completed', 'failed', 'no-answer', 'busy', 'voicemail'")
    print("")
    print("Example captured data:")
    print("  ┌─────────────────────────────────────────────────────────┐")
    print("  │ accepting_new_patients: 'yes'                           │")
    print("  │ has_waiting_list: 'no'                                  │")
    print("  │ waiting_list_availability_date: 'N/A'                   │")
    print("  │ languages_supported: 'spanish, portuguese'              │")
    print("  │ call_notes: 'Staff was very helpful'                    │")
    print("  │ call_status: 'completed'                                │")
    print("  └─────────────────────────────────────────────────────────┘")
    print("")
    print("=" * 80)
    print("")

def format_captured_data(data_dict):
    """Format and print captured data in a readable way."""
    print("\n" + "=" * 80)
    print("📋 CAPTURED DATA FROM CALL")
    print("=" * 80)
    print("")
    
    # Format each field
    accepting = data_dict.get('accepting_new_patients', 'N/A')
    status_color = '✅' if accepting == 'yes' else '❌' if accepting == 'no' else '❓'
    print(f"{status_color} Accepting New Patients: {accepting.upper()}")
    
    waiting_list = data_dict.get('has_waiting_list', 'N/A')
    wl_color = '⚠️' if waiting_list == 'yes' else '✅' if waiting_list == 'no' else '❓'
    print(f"{wl_color} Has Waiting List: {waiting_list.upper()}")
    
    availability = data_dict.get('waiting_list_availability_date', 'N/A')
    if availability and availability != 'N/A':
        print(f"📅 Expected Availability: {availability}")
    else:
        print(f"📅 Expected Availability: {availability}")
    
    languages = data_dict.get('languages_supported', [])
    if isinstance(languages, list):
        lang_str = ', '.join(languages) if languages else 'None'
    else:
        lang_str = str(languages) if languages else 'None'
    print(f"🌐 Languages Supported: {lang_str}")
    
    notes = data_dict.get('call_notes', '')
    if notes:
        print(f"📝 Additional Notes: {notes}")
    
    call_status = data_dict.get('call_status', 'unknown')
    status_emoji = '✅' if call_status == 'completed' else '⚠️'
    print(f"{status_emoji} Call Status: {call_status.upper()}")
    
    print("")
    print("=" * 80)
    print("")

def main():
    """Make a test call to the specified phone number."""
    api_key = os.getenv("VAPI_API_KEY")
    
    if not api_key:
        print("❌ Error: VAPI_API_KEY environment variable not set")
        print("   Set it with: export VAPI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Optional webhook URL
    webhook_url = os.getenv("VAPI_WEBHOOK_URL")
    
    # Phone number to call (default to user's number, can be overridden)
    phone_number = sys.argv[1] if len(sys.argv) > 1 else "+12242454540"
    
    # Format phone number
    if not phone_number.startswith("+"):
        # Remove common formatting
        cleaned = phone_number.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        if cleaned.startswith("1") and len(cleaned) == 11:
            phone_number = f"+{cleaned}"
        elif len(cleaned) == 10:
            phone_number = f"+1{cleaned}"
    
    print("🧪 Vapi.ai Test Call")
    print("=" * 80)
    print(f"📞 Calling: {phone_number}")
    print("")
    
    # Print data structure that will be captured
    print_data_structure()
    
    manager = VapiCallManager(api_key=api_key, webhook_url=webhook_url)
    
    # Create assistant
    print("🔧 Creating assistant...")
    assistant_id = manager.create_assistant()
    
    if not assistant_id:
        print("❌ Failed to create assistant. Exiting.")
        sys.exit(1)
    
    # Get or create phone number (optional - Vapi can use default)
    print("\n📱 Checking phone number configuration...")
    phone_number_id = manager.get_or_create_phone_number()
    
    if not phone_number_id:
        print("⚠️  No phone number ID configured, but call may still work with default")
    
    # Make the test call
    print(f"\n📞 Initiating call to {phone_number}...")
    print("   This will test the assistant's ability to:")
    print("   - Navigate phone trees (press 0)")
    print("   - Ask about new patients")
    print("   - Ask about waiting lists")
    print("   - Ask about language support")
    print("")
    
    call_id = manager.initiate_call(
        phone_number=phone_number,
        health_center_name="Test Call - User's Phone",
        health_center_id="test_call"
    )
    
    if call_id:
        print(f"✅ Call initiated! Call ID: {call_id}")
        print("")
        print("📋 Next steps:")
        print("   1. Answer your phone when it rings")
        print("   2. Listen to the assistant's questions")
        print("   3. Answer as if you were a health center representative")
        print("   4. Check the Vapi.ai dashboard for call recording/transcript")
        if webhook_url:
            print("   5. Check backend logs for webhook events")
        print("")
        print("⏳ Call in progress... (press Ctrl+C to exit)")
        print("")
        
        # Wait a bit to show call status and check for results
        try:
            print("⏳ Waiting for call to complete...")
            print("   (The call may take 1-3 minutes)")
            print("")
            
            # Poll for call status
            max_wait = 180  # 3 minutes max
            wait_time = 0
            while wait_time < max_wait:
                time.sleep(5)
                wait_time += 5
                status_data = manager.get_call_status(call_id)
                if status_data:
                    call_status = status_data.get('status', 'unknown')
                    print(f"   Call status: {call_status} (waited {wait_time}s)")
                    
                    # Check if call ended
                    if call_status in ['ended', 'failed', 'no-answer', 'busy', 'voicemail']:
                        print("")
                        print("📊 Call completed!")
                        print("")
                        print("To see the captured data:")
                        print("  1. Check Vapi.ai dashboard for call transcript")
                        print("  2. Look for function call results in the dashboard")
                        if webhook_url:
                            print("  3. Check backend logs for webhook data")
                        print("")
                        break
                else:
                    print(f"   Checking call status... (waited {wait_time}s)")
                    
        except KeyboardInterrupt:
            print("\n\n👋 Exiting (call may still be in progress)")
            print("")
            print("To see captured data after the call completes:")
            print("  1. Check Vapi.ai dashboard: https://dashboard.vapi.ai")
            print("  2. Find your call by ID:", call_id)
            print("  3. Review the call transcript and function calls")
            if webhook_url:
                print("  4. Check backend logs for webhook events")
    else:
        print("❌ Failed to initiate call")
        sys.exit(1)


if __name__ == "__main__":
    main()
