#!/usr/bin/env python3
"""
Demo Script: VAPI Phone Call Integration

This script demonstrates the VAPI integration by:
1. Making a test call to a phone number
2. Showing what data is collected during the call
3. Displaying the captured information

Usage:
    python scripts/demos/demo_vapi_call.py [phone_number]

Example:
    python scripts/demos/demo_vapi_call.py +12242454540

Requirements:
    - VAPI_API_KEY environment variable set
    - VAPI account configured
"""

import sys
import os
import time
from pathlib import Path

# Add vapi directory to path
project_root = Path(__file__).parent.parent.parent
vapi_dir = project_root / "vapi"
sys.path.insert(0, str(vapi_dir))

try:
    from vapi_call_manager import VapiCallManager
except ImportError:
    print("❌ Error: Could not import VapiCallManager")
    print("   Make sure you're running from the project root directory")
    sys.exit(1)

def print_header():
    """Print demo header."""
    print("\n" + "="*80)
    print("📞 VAPI Phone Call Integration Demo")
    print("="*80)
    print("\nThis demo shows how VAPI automatically calls health centers to:")
    print("  • Check if they're accepting new patients")
    print("  • Ask about waiting lists")
    print("  • Collect language support information")
    print("  • Gather additional notes")
    print("\n" + "-"*80 + "\n")

def print_data_structure():
    """Print what data will be collected."""
    print("📊 Data Structure to be Collected:")
    print("-" * 80)
    print("""
  • accepting_new_patients: 'yes', 'no', or 'unknown'
    Question: "Are you currently taking new patients?"

  • has_waiting_list: 'yes', 'no', or 'unknown'
    Question: "Is there a waiting list?"

  • waiting_list_availability_date: Date string or 'N/A'
    Question: "When do you expect availability?"

  • languages_supported: Comma-separated list
    Question: "Do your providers speak Spanish, Portuguese, or Haitian Creole?"

  • call_notes: Free text with additional information

  • call_status: 'completed', 'failed', 'no-answer', 'busy', 'voicemail'
    """)
    print("-" * 80 + "\n")

def format_phone_number(phone):
    """Format phone number to E.164 format."""
    if phone.startswith("+"):
        return phone
    
    # Remove common formatting
    cleaned = phone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    
    if cleaned.startswith("1") and len(cleaned) == 11:
        return f"+{cleaned}"
    elif len(cleaned) == 10:
        return f"+1{cleaned}"
    
    return phone

def main():
    """Main demo function."""
    print_header()
    
    # Check for API key
    api_key = os.getenv("VAPI_API_KEY")
    if not api_key:
        print("❌ Error: VAPI_API_KEY environment variable not set")
        print("\nTo set it:")
        print("  export VAPI_API_KEY=your_api_key_here")
        print("\nOr add it to your shell profile (~/.zshrc or ~/.bashrc)")
        sys.exit(1)
    
    print("✅ VAPI_API_KEY found\n")
    
    # Get phone number
    if len(sys.argv) > 1:
        phone_number = format_phone_number(sys.argv[1])
    else:
        print("📞 Enter phone number to call (E.164 format, e.g., +12242454540):")
        phone_input = input("   Phone: ").strip()
        if not phone_input:
            print("❌ No phone number provided")
            sys.exit(1)
        phone_number = format_phone_number(phone_input)
    
    print(f"📞 Calling: {phone_number}\n")
    
    # Show data structure
    print_data_structure()
    
    # Initialize VAPI manager
    print("🔧 Initializing VAPI Call Manager...")
    webhook_url = os.getenv("VAPI_WEBHOOK_URL")  # Optional
    manager = VapiCallManager(api_key=api_key, webhook_url=webhook_url)
    
    # Create assistant
    print("🤖 Creating assistant...")
    assistant_id = manager.create_assistant()
    
    if not assistant_id:
        print("❌ Failed to create assistant")
        print("   Check your VAPI_API_KEY and vapi/vapi_config.json")
        sys.exit(1)
    
    print(f"✅ Assistant created: {assistant_id}\n")
    
    # Get or create phone number
    print("📱 Checking phone number configuration...")
    phone_number_id = manager.get_or_create_phone_number()
    
    if phone_number_id:
        print(f"✅ Phone number ID: {phone_number_id}\n")
    else:
        print("⚠️  No phone number ID configured (using default)\n")
    
    # Make the call
    print("📞 Initiating call...")
    print("   The assistant will:")
    print("   • Navigate phone trees (press 0)")
    print("   • Ask about new patients")
    print("   • Ask about waiting lists")
    print("   • Ask about language support")
    print("   • Collect any additional information\n")
    
    call_id = manager.initiate_call(
        phone_number=phone_number,
        health_center_name="Demo Test Call",
        health_center_id="demo_call"
    )
    
    if not call_id:
        print("❌ Failed to initiate call")
        sys.exit(1)
    
    print(f"✅ Call initiated!")
    print(f"   Call ID: {call_id}\n")
    
    print("="*80)
    print("📋 Next Steps:")
    print("="*80)
    print("1. Answer your phone when it rings")
    print("2. Listen to the assistant's questions")
    print("3. Answer as if you were a health center representative")
    print("4. The call will be recorded and transcribed")
    print("\nTo view results:")
    print(f"  • VAPI Dashboard: https://dashboard.vapi.ai")
    print(f"  • Look for call ID: {call_id}")
    print("  • Review transcript and function calls")
    if webhook_url:
        print(f"  • Check webhook logs at: {webhook_url}")
    print("\n⏳ Waiting for call to complete...")
    print("   (Press Ctrl+C to exit early)\n")
    
    # Poll for call status
    try:
        max_wait = 180  # 3 minutes
        wait_time = 0
        
        while wait_time < max_wait:
            time.sleep(5)
            wait_time += 5
            
            status_data = manager.get_call_status(call_id)
            if status_data:
                call_status = status_data.get('status', 'unknown')
                print(f"   Status: {call_status} ({wait_time}s elapsed)")
                
                if call_status in ['ended', 'failed', 'no-answer', 'busy', 'voicemail']:
                    print("\n✅ Call completed!")
                    print("\nTo see captured data:")
                    print("  1. Check VAPI dashboard for call transcript")
                    print("  2. Look for function call results")
                    if webhook_url:
                        print("  3. Check backend logs for webhook data")
                    break
    except KeyboardInterrupt:
        print("\n\n👋 Exiting (call may still be in progress)")
        print(f"\nTo see results later, check VAPI dashboard for call ID: {call_id}")
    
    print("\n" + "="*80)
    print("✅ Demo Complete!")
    print("="*80)
    print("\nKey Takeaways:")
    print("  • VAPI can automatically call health centers")
    print("  • Collects structured data during the call")
    print("  • Handles phone trees and navigation")
    print("  • Provides transcripts and call recordings")
    print("\n")

if __name__ == "__main__":
    main()
