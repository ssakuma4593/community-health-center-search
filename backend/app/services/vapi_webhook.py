"""
Vapi.ai Webhook Handler

This module handles webhook events from Vapi.ai calls and updates the CSV
with the collected information.
"""

import csv
import json
import os
import logging
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class VapiWebhookHandler:
    def __init__(self, csv_file_path: str):
        """
        Initialize the webhook handler.
        
        Args:
            csv_file_path: Path to the CSV file to update
        """
        self.csv_file_path = csv_file_path
        self.field_names = [
            'name', 'street_address_1', 'street_address_2', 'city_town', 'state',
            'zipcode', 'phone', 'types', 'website', 'source', 'latitude', 'longitude',
            # New fields for call data
            'accepting_new_patients', 'has_waiting_list', 'waiting_list_availability_date',
            'languages_supported', 'call_notes', 'last_called_date', 'call_status'
        ]
    
    def parse_phone_number(self, phone: str) -> str:
        """Normalize phone number for matching."""
        # Remove formatting
        cleaned = phone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        # Remove leading +1 if present
        if cleaned.startswith("+1"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("1") and len(cleaned) == 11:
            cleaned = cleaned[1:]
        return cleaned
    
    def find_health_center_by_phone(self, phone_number: str) -> Optional[Dict]:
        """
        Find health center in CSV by phone number.
        
        Args:
            phone_number: Phone number to search for
            
        Returns:
            Dictionary with row data and index, or None
        """
        if not os.path.exists(self.csv_file_path):
            logger.warning(f"CSV file not found: {self.csv_file_path}")
            return None
        
        normalized_search_phone = self.parse_phone_number(phone_number)
        
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
                for idx, row in enumerate(rows):
                    row_phone = row.get('phone', '')
                    if row_phone:
                        normalized_row_phone = self.parse_phone_number(row_phone)
                        if normalized_row_phone == normalized_search_phone:
                            return {'row': row, 'index': idx + 1}  # +1 for header
                
                return None
                
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            return None
    
    def update_csv_row(self, phone_number: str, call_data: Dict) -> bool:
        """
        Update a row in the CSV with call data.
        
        Args:
            phone_number: Phone number to identify the row
            call_data: Dictionary with call results
            
        Returns:
            True if successful, False otherwise
        """
        center_match = self.find_health_center_by_phone(phone_number)
        
        if not center_match:
            logger.warning(f"Health center not found for phone: {phone_number}")
            return False
        
        # Read all rows
        rows = []
        with open(self.csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []
            rows = list(reader)
        
        # Ensure new fields exist in fieldnames
        new_fields = [
            'accepting_new_patients', 'has_waiting_list', 'waiting_list_availability_date',
            'languages_supported', 'call_notes', 'last_called_date', 'call_status'
        ]
        
        for field in new_fields:
            if field not in fieldnames:
                fieldnames.append(field)
        
        # Update the matching row
        row_idx = center_match['index'] - 1  # Convert to 0-based
        if row_idx < len(rows):
            row = rows[row_idx]
            
            # Update fields from call data
            row['accepting_new_patients'] = call_data.get('accepting_new_patients', '')
            row['has_waiting_list'] = call_data.get('has_waiting_list', '')
            row['waiting_list_availability_date'] = call_data.get('waiting_list_availability_date', '')
            
            # Join languages array
            languages = call_data.get('languages_supported', [])
            if isinstance(languages, list):
                row['languages_supported'] = ', '.join([lang for lang in languages if lang != 'none'])
            else:
                row['languages_supported'] = str(languages) if languages else ''
            
            row['call_notes'] = call_data.get('additional_notes', '')
            row['last_called_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            row['call_status'] = call_data.get('call_status', 'completed')
            
            # Ensure all fields exist
            for field in fieldnames:
                if field not in row:
                    row[field] = ''
        
        # Write updated rows back to CSV
        try:
            with open(self.csv_file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            
            logger.info(f"✅ Updated CSV for phone: {phone_number}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error writing CSV: {str(e)}")
            return False
    
    def handle_function_call(self, function_call: Dict, call_metadata: Dict) -> Dict:
        """
        Handle function call from Vapi (when assistant captures information).
        
        Args:
            function_call: The function call data from Vapi
            call_metadata: Metadata from the call
            
        Returns:
            Response dictionary
        """
        function_name = function_call.get('name')
        
        if function_name == 'capture_call_information':
            parameters = function_call.get('parameters', {})
            
            # Extract phone number from call metadata
            customer_number = call_metadata.get('customer', {}).get('number', '')
            health_center_name = call_metadata.get('metadata', {}).get('health_center_name', 'Unknown')
            
            # Prepare call data
            call_data = {
                'accepting_new_patients': parameters.get('accepting_new_patients', 'unknown'),
                'has_waiting_list': parameters.get('has_waiting_list', 'unknown'),
                'waiting_list_availability_date': parameters.get('waiting_list_availability_date', 'N/A'),
                'languages_supported': parameters.get('languages_supported', []),
                'additional_notes': parameters.get('additional_notes', ''),
                'call_status': 'completed'
            }
            
            # Update CSV
            if customer_number:
                success = self.update_csv_row(customer_number, call_data)
                if success:
                    logger.info(f"✅ Updated {health_center_name} with call data")
                else:
                    logger.warning(f"⚠️  Could not update {health_center_name}")
            
            return {
                'result': 'Information captured successfully',
                'toolCallId': function_call.get('id')
            }
        
        return {'result': 'Unknown function', 'toolCallId': function_call.get('id')}
    
    def handle_call_end(self, call_data: Dict) -> bool:
        """
        Handle call end event.
        
        Args:
            call_data: Call end event data
            
        Returns:
            True if handled successfully
        """
        customer_number = call_data.get('customer', {}).get('number', '')
        status = call_data.get('status', 'unknown')
        metadata = call_data.get('metadata', {})
        health_center_name = metadata.get('health_center_name', 'Unknown')
        
        logger.info(f"📞 Call ended for {health_center_name}: {status}")
        
        # If call failed or ended without function call, update status
        if status in ['failed', 'no-answer', 'busy', 'voicemail']:
            call_data_update = {
                'call_status': status,
                'accepting_new_patients': '',
                'has_waiting_list': '',
                'waiting_list_availability_date': '',
                'languages_supported': [],
                'additional_notes': f'Call status: {status}',
                'last_called_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            if customer_number:
                return self.update_csv_row(customer_number, call_data_update)
        
        return True


def parse_vapi_webhook(payload: Dict) -> Dict:
    """
    Parse Vapi webhook payload and extract relevant information.
    
    Args:
        payload: Webhook payload from Vapi
        
    Returns:
        Parsed event dictionary
    """
    event_type = payload.get('type', '')
    message = payload.get('message', {})
    
    result = {
        'event_type': event_type,
        'call_id': payload.get('call', {}).get('id', ''),
        'status': payload.get('call', {}).get('status', ''),
        'customer_number': payload.get('call', {}).get('customer', {}).get('number', ''),
        'metadata': payload.get('call', {}).get('metadata', {})
    }
    
    if event_type == 'function-call':
        result['function_call'] = message.get('functionCall', {})
    
    return result



