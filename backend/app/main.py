from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI(title="Community Health Center Search Backend", version="1.0.0")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)