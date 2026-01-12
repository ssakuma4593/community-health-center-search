#!/usr/bin/env python3
"""
Vapi.ai Call Manager for Community Health Centers

This script:
1. Reads health center phone numbers from CSV
2. Initiates calls via Vapi.ai API
3. Tracks call status and results
"""

import csv
import json
import os
import sys
import time
import requests
from typing import Dict, List, Optional
from datetime import datetime

# Vapi.ai API configuration
VAPI_API_BASE = "https://api.vapi.ai"
VAPI_API_VERSION = "2024-06-13"


class VapiCallManager:
    def __init__(self, api_key: str, webhook_url: Optional[str] = None):
        """
        Initialize the Vapi Call Manager.
        
        Args:
            api_key: Your Vapi.ai API key
            webhook_url: Optional webhook URL to receive call events
        """
        self.api_key = api_key
        self.webhook_url = webhook_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.assistant_id = None
        self.phone_number_id = None
        
    def create_assistant(self, config_file: str = "vapi_config.json") -> Optional[str]:
        """
        Create or get an assistant using the configuration file.
        
        Args:
            config_file: Path to assistant configuration JSON file
            
        Returns:
            Assistant ID if successful, None otherwise
        """
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            assistant_config = config.get("assistant_config", {})
            
            # Add webhook if provided
            if self.webhook_url:
                assistant_config["serverUrl"] = self.webhook_url
                assistant_config["serverUrlSecret"] = os.getenv("VAPI_WEBHOOK_SECRET", "")
            
            # Create assistant via API
            response = requests.post(
                f"{VAPI_API_BASE}/assistant",
                headers=self.headers,
                json=assistant_config
            )
            
            if response.status_code == 201:
                assistant = response.json()
                self.assistant_id = assistant.get("id")
                print(f"✅ Assistant created: {self.assistant_id}")
                return self.assistant_id
            else:
                print(f"❌ Failed to create assistant: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating assistant: {str(e)}")
            return None
    
    def get_or_create_phone_number(self) -> Optional[str]:
        """
        Get an existing phone number or create a new one.
        
        Returns:
            Phone number ID if successful, None otherwise
        """
        # First, try to list existing phone numbers
        response = requests.get(
            f"{VAPI_API_BASE}/phone-number",
            headers=self.headers
        )
        
        if response.status_code == 200:
            phone_numbers = response.json()
            if phone_numbers and len(phone_numbers) > 0:
                # Use the first available phone number
                self.phone_number_id = phone_numbers[0].get("id")
                print(f"✅ Using existing phone number: {self.phone_number_id}")
                return self.phone_number_id
        
        # If no phone numbers exist, create one
        # Note: You'll need to purchase/rent a number via Vapi dashboard
        print("⚠️  No phone number found. Please create one in the Vapi.ai dashboard.")
        print("    After creating, update the phone_number_id in the config.")
        return None
    
    def initiate_call(
        self,
        phone_number: str,
        health_center_name: str,
        health_center_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Initiate a call to a health center.
        
        Args:
            phone_number: The phone number to call (format: +1234567890)
            health_center_name: Name of the health center (for metadata)
            health_center_id: Optional ID to track this health center
            
        Returns:
            Call ID if successful, None otherwise
        """
        if not self.assistant_id:
            print("❌ Assistant not created. Please create assistant first.")
            return None
        
        # Format phone number (ensure it starts with +1 for US numbers)
        if not phone_number.startswith("+"):
            # Remove common formatting
            cleaned = phone_number.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
            if cleaned.startswith("1") and len(cleaned) == 11:
                phone_number = f"+{cleaned}"
            elif len(cleaned) == 10:
                phone_number = f"+1{cleaned}"
            else:
                print(f"⚠️  Invalid phone number format: {phone_number}")
                return None
        
        call_data = {
            "assistantId": self.assistant_id,
            "customer": {
                "number": phone_number
            },
            "metadata": {
                "health_center_name": health_center_name,
                "health_center_id": health_center_id or "",
                "call_timestamp": datetime.now().isoformat()
            }
        }
        
        # Add phone number ID if available
        if self.phone_number_id:
            call_data["phoneNumberId"] = self.phone_number_id
        
        try:
            response = requests.post(
                f"{VAPI_API_BASE}/call",
                headers=self.headers,
                json=call_data
            )
            
            if response.status_code == 201:
                call = response.json()
                call_id = call.get("id")
                print(f"✅ Call initiated to {phone_number} (Call ID: {call_id})")
                return call_id
            else:
                print(f"❌ Failed to initiate call: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error initiating call: {str(e)}")
            return None
    
    def get_call_status(self, call_id: str) -> Optional[Dict]:
        """
        Get the status of a call.
        
        Args:
            call_id: The call ID to check
            
        Returns:
            Call status dictionary or None
        """
        try:
            response = requests.get(
                f"{VAPI_API_BASE}/call/{call_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error getting call status: {str(e)}")
            return None
    
    def read_health_centers_from_csv(self, csv_file: str) -> List[Dict]:
        """
        Read health centers from CSV file.
        
        Args:
            csv_file: Path to CSV file
            
        Returns:
            List of health center dictionaries
        """
        health_centers = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('phone'):
                        health_centers.append({
                            'name': row.get('name', ''),
                            'phone': row.get('phone', ''),
                            'address': row.get('street_address_1', ''),
                            'city': row.get('city_town', ''),
                            'state': row.get('state', ''),
                            'zipcode': row.get('zipcode', '')
                        })
        except Exception as e:
            print(f"❌ Error reading CSV file: {str(e)}")
        
        return health_centers
    
    def batch_call_health_centers(
        self,
        csv_file: str,
        limit: Optional[int] = None,
        delay_seconds: int = 60
    ):
        """
        Batch call health centers from CSV file.
        
        Args:
            csv_file: Path to CSV file with health centers
            limit: Optional limit on number of calls to make
            delay_seconds: Seconds to wait between calls
        """
        health_centers = self.read_health_centers_from_csv(csv_file)
        
        if limit:
            health_centers = health_centers[:limit]
        
        print(f"📞 Starting batch calls to {len(health_centers)} health centers...")
        print("=" * 80)
        
        for idx, center in enumerate(health_centers, 1):
            print(f"\n[{idx}/{len(health_centers)}] Calling {center['name']}")
            print(f"   Phone: {center['phone']}")
            
            call_id = self.initiate_call(
                phone_number=center['phone'],
                health_center_name=center['name'],
                health_center_id=f"center_{idx}"
            )
            
            if call_id:
                print(f"   ✅ Call ID: {call_id}")
            else:
                print(f"   ❌ Failed to initiate call")
            
            # Wait between calls to avoid rate limiting
            if idx < len(health_centers):
                print(f"   ⏳ Waiting {delay_seconds} seconds before next call...")
                time.sleep(delay_seconds)
        
        print("\n" + "=" * 80)
        print("✅ Batch calling complete!")


def main():
    """Main function to run the call manager."""
    api_key = os.getenv("VAPI_API_KEY")
    
    if not api_key:
        print("❌ Error: VAPI_API_KEY environment variable not set")
        print("   Set it with: export VAPI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Optional webhook URL (needs to be publicly accessible)
    webhook_url = os.getenv("VAPI_WEBHOOK_URL")
    
    manager = VapiCallManager(api_key=api_key, webhook_url=webhook_url)
    
    # Create assistant
    print("🔧 Creating assistant...")
    assistant_id = manager.create_assistant()
    
    if not assistant_id:
        print("❌ Failed to create assistant. Exiting.")
        sys.exit(1)
    
    # Get or create phone number
    print("\n📱 Getting phone number...")
    phone_number_id = manager.get_or_create_phone_number()
    
    # Read CSV file path
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "community_health_centers_with_coords.csv"
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        sys.exit(1)
    
    # Optional limit for testing
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    # Start batch calling
    print(f"\n🚀 Starting calls from {csv_file}...")
    manager.batch_call_health_centers(
        csv_file=csv_file,
        limit=limit,
        delay_seconds=60  # 1 minute between calls
    )


if __name__ == "__main__":
    main()



