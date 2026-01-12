# Vapi.ai Integration Summary

This document summarizes the Vapi.ai integration that has been set up for automated calling to community health centers.

## What Was Built

### 1. Configuration Files

- **`vapi_config.json`**: Assistant configuration with:
  - System prompt for phone tree navigation (presses 0 for representative)
  - Conversation flow to ask about:
    - New patient acceptance
    - Waiting list status
    - Expected availability dates
    - Language support (Spanish, Portuguese, Haitian Creole)
  - Function definitions for capturing structured data

### 2. Call Management Script

- **`vapi_call_manager.py`**: Python script to:
  - Create/manage Vapi.ai assistants
  - Read health centers from CSV
  - Initiate outbound calls
  - Batch process multiple health centers
  - Handle phone number formatting

### 3. Backend Webhook Handler

- **`backend/app/services/vapi_webhook.py`**: Handles webhook events:
  - Processes function calls (captured information)
  - Handles call end events
  - Updates CSV file with call results
  - Matches calls to health centers by phone number

- **`backend/app/main.py`**: Added webhook endpoint:
  - `/webhooks/vapi` - Receives events from Vapi.ai
  - Updates CSV automatically when calls complete

### 4. CSV Field Management

- **`add_call_fields_to_csv.py`**: Script to add new columns:
  - `accepting_new_patients`
  - `has_waiting_list`
  - `waiting_list_availability_date`
  - `languages_supported`
  - `call_notes`
  - `last_called_date`
  - `call_status`

### 5. Frontend Updates

- **API Route** (`frontend/src/app/api/health-centers/route.ts`):
  - Returns call data fields along with health center data

- **Components**:
  - `HealthCenterList.tsx`: Displays call information in list view
  - `HealthCenterMap.tsx`: Shows call data in map info windows
  - `page.tsx`: Updated interfaces to include call data

### 6. Documentation

- **`docs/VAPI_SETUP.md`**: Complete setup guide
- **`setup_vapi.sh`**: Quick setup script

## Key Features

### Phone Tree Navigation
- Automatically detects automated menus
- Presses "0" to reach a representative
- Handles transfers gracefully

### Conversation Flow
The assistant follows this script:
1. Introduces the caller and reason for calling
2. Asks: "Are you currently taking new patients?"
3. If no: "Is there a waiting list?"
4. If yes: "When do you expect availability?"
5. Asks about language support: "Do your providers speak Spanish, Portuguese, or Haitian Creole?"
6. Thanks the representative and ends call

### Data Capture
- Structured data capture using function calling
- Automatic CSV updates via webhooks
- Status tracking (completed, failed, no-answer, voicemail)

### Display
- Call data shown in list view with color coding:
  - Green: Yes/Accepting
  - Red: No/Not accepting
  - Yellow: Waiting list
- Call information in map info windows
- Last called date displayed

## Quick Start

1. **Setup**:
   ```bash
   ./setup_vapi.sh
   ```

2. **Configure**:
   ```bash
   export VAPI_API_KEY="your_key"
   export VAPI_WEBHOOK_URL="https://your-url.com/webhooks/vapi"
   ```

3. **Start Backend**:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

4. **Test Call**:
   ```bash
   cd vapi
   python3 vapi_call_manager.py ../community_health_centers_with_coords.csv 1
   ```

5. **Run Batch**:
   ```bash
   cd vapi
   python3 vapi_call_manager.py ../community_health_centers_with_coords.csv
   ```

## File Structure

```
.
├── vapi/                               # Vapi.ai integration folder
│   ├── vapi_config.json                # Assistant configuration
│   ├── vapi_call_manager.py            # Call management script
│   ├── add_call_fields_to_csv.py       # CSV field management
│   ├── setup_vapi.sh                   # Setup script
│   ├── vapi_requirements.txt           # Python dependencies
│   ├── VAPI_SETUP.md                   # Complete setup guide
│   ├── VAPI_INTEGRATION_SUMMARY.md     # This file
│   └── README.md                       # Quick reference
├── backend/
│   └── app/
│       ├── main.py                     # Webhook endpoint added
│       └── services/
│           ├── __init__.py
│           └── vapi_webhook.py         # Webhook handler
├── frontend/
│   └── src/
│       └── app/
│           ├── api/
│           │   └── health-centers/
│           │       └── route.ts        # Updated to include call data
│           └── components/
│               ├── HealthCenterList.tsx # Updated to display call data
│               └── HealthCenterMap.tsx  # Updated to show call data
└── community_health_centers_with_coords.csv  # CSV file (in project root)
```

## Next Steps

1. **Get Vapi.ai Account**: Sign up at vapi.ai
2. **Get Phone Number**: Purchase/rent a number in Vapi dashboard
3. **Set Environment Variables**: VAPI_API_KEY, VAPI_WEBHOOK_URL
4. **Test with Small Batch**: Start with 5-10 centers
5. **Review Call Recordings**: Optimize prompts based on results
6. **Scale Up**: Run full batch when satisfied

## Important Notes

- Calls are spaced 60 seconds apart to avoid rate limiting
- Webhook URL must be publicly accessible (use ngrok for local testing)
- CSV file is automatically backed up before modifications
- All call data is stored in the CSV for website display
- Monitor costs in Vapi.ai dashboard

## Support

- See `vapi/VAPI_SETUP.md` for detailed instructions
- Check backend logs for webhook events
- Review call recordings in Vapi dashboard
- Test webhook endpoint: `curl -X POST http://localhost:8000/webhooks/vapi`
