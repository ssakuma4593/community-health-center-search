from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os
import sys
import logging

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.vapi_webhook import VapiWebhookHandler, parse_vapi_webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Community Health Center Search Backend", version="1.0.0")

# Initialize webhook handler
CSV_FILE_PATH = os.path.join(
    os.path.dirname(__file__), 
    "..", 
    "..", 
    "community_health_centers_with_coords.csv"
)
webhook_handler = VapiWebhookHandler(CSV_FILE_PATH)

class ProviderSearchRequest(BaseModel):
    language: str
    specialty: str
    location: str

class Provider(BaseModel):
    id: int
    name: str
    specialty: str
    location: str
    languages: List[str]
    phone: str

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "backend"}

@app.post("/providers/search")
async def search_providers(request: ProviderSearchRequest):
    """Search for healthcare providers based on language, specialty, and location"""
    # Load providers data
    providers_file = os.path.join(os.path.dirname(__file__), "..", "..", "data", "providers.json")
    
    try:
        with open(providers_file, 'r') as f:
            providers_data = json.load(f)
    except FileNotFoundError:
        return {"error": "Providers data not found", "providers": []}
    
    # Filter providers based on search criteria
    matching_providers = []
    
    for provider in providers_data:
        # Check if the requested language is supported
        language_match = request.language.lower() in [lang.lower() for lang in provider.get("languages", [])]
        
        # Check if specialty matches (case-insensitive partial match)
        specialty_match = request.specialty.lower() in provider.get("specialty", "").lower()
        
        # Check if location matches (case-insensitive partial match)
        location_match = request.location.lower() in provider.get("location", "").lower()
        
        if language_match and specialty_match and location_match:
            matching_providers.append(provider)
    
    return {"providers": matching_providers}


@app.post("/webhooks/vapi")
async def vapi_webhook(request: Request):
    """
    Webhook endpoint to receive events from Vapi.ai calls.
    
    Handles:
    - function-call: When assistant captures information
    - call-end: When call completes
    - status-update: Status updates during call
    """
    try:
        payload = await request.json()
        logger.info(f"Received Vapi webhook: {payload.get('type', 'unknown')}")
        
        event_type = payload.get('type', '')
        call_data = payload.get('call', {})
        message = payload.get('message', {})
        
        if event_type == 'function-call':
            function_call = message.get('functionCall', {})
            metadata = call_data.get('metadata', {})
            
            # Handle the function call (capture information)
            response = webhook_handler.handle_function_call(function_call, call_data)
            return response
            
        elif event_type == 'call-end':
            # Handle call end
            webhook_handler.handle_call_end(call_data)
            return {"status": "ok", "message": "Call end processed"}
            
        elif event_type == 'status-update':
            # Log status updates
            status = call_data.get('status', '')
            logger.info(f"Call status update: {status}")
            return {"status": "ok"}
        
        else:
            logger.warning(f"Unknown webhook event type: {event_type}")
            return {"status": "ok", "message": "Event logged"}
            
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {"error": str(e)}, 500


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)