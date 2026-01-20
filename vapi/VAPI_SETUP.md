# Vapi.ai Setup Guide

This guide explains how to set up Vapi.ai for automated calling to community health centers to gather information about patient availability, waiting lists, and language support.

## Quick Start Checklist

- [ ] Vapi.ai account created
- [ ] API key obtained and set (VAPI_API_KEY)
- [ ] Dependencies installed
- [ ] CSV fields added
- [ ] Phone number purchased in Vapi dashboard (automatically detected - no config needed!)
- [ ] (Optional) Webhook URL configured
- [ ] Test call completed successfully
- [ ] Ready to run full batch!

## Overview

The Vapi.ai integration allows you to:
- Automatically call health centers using AI voice assistants
- Navigate phone trees (presses 0 to reach a representative)
- Ask specific questions about:
  - New patient acceptance
  - Waiting list status
  - Expected availability dates
  - Language support (Spanish, Portuguese, Haitian Creole)
- Store call results in the CSV file
- Display call information on the website

## Prerequisites

1. **Vapi.ai Account**
   - Sign up at [vapi.ai](https://vapi.ai)
   - Get your API key from the dashboard

2. **Phone Number**
   - Purchase or rent a phone number in the Vapi.ai dashboard
   - This number will be used to make outbound calls

3. **Webhook URL** (highly recommended - needed to save call data)
   - This is how Vapi.ai sends call results back to your application
   - Without it: You can make calls, but data won't automatically save to CSV
   - With it: Call data automatically updates your CSV file
   - Options:
     - Use ngrok for local testing: `ngrok http 8000`
     - Deploy the backend to a service (Heroku, Railway, etc.)
     - Use a service like Zapier or Make.com

4. **Backend Server**
   - The backend must be running to receive webhooks
   - Default port: 8000

## Setup Steps

### 1. Install Dependencies

```bash
# Install Python dependencies for Vapi integration
pip install -r vapi_requirements.txt

# Backend dependencies (if not already installed)
cd backend
pip install -r requirements.txt
```

### 2. Add Call Fields to CSV

Before making calls, add the new fields to your CSV file:

```bash
python add_call_fields_to_csv.py community_health_centers_with_coords.csv
```

This will add the following columns:
- `accepting_new_patients`
- `has_waiting_list`
- `waiting_list_availability_date`
- `languages_supported`
- `call_notes`
- `last_called_date`
- `call_status`

### 3. Configure Environment Variables

Set your API key (required):

**Important**: Use your **private key**, not the public key! The private key is used for server-side API calls.

```bash
export VAPI_API_KEY="your_private_api_key_here"
```

To make it permanent, add it to your `~/.zshrc` or `~/.bashrc`:
```bash
echo 'export VAPI_API_KEY="your_private_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

**Finding your keys in Vapi.ai dashboard:**
- **Private Key**: Used for server-side API calls (what you need)
- **Public Key**: Used for client-side calls (not what you need)
- Look for "Private Key" or "Server Key" in the API Keys section

Optional webhook URL (for local testing with ngrok or production):
```bash
export VAPI_WEBHOOK_URL="https://your-webhook-url.com/webhooks/vapi"
export VAPI_WEBHOOK_SECRET="your_webhook_secret_optional"
```

**Note about Phone Numbers**: Your phone number is automatically detected from your Vapi account - no configuration needed! When you purchase/rent a phone number in the Vapi dashboard, the script will automatically find and use it.

### 4. Start Backend Server

The backend must be running to receive webhooks:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

For production, use a process manager like `gunicorn` or deploy to a cloud service.

### 5. Create Assistant in Vapi.ai

The assistant configuration is in `vapi_config.json`. You have two options:

#### Option A: Use the Script (Recommended)

The `vapi_call_manager.py` script will automatically create the assistant:

```bash
python vapi_call_manager.py
```

#### Option B: Manual Setup in Dashboard

1. Go to Vapi.ai dashboard
2. Create a new assistant
3. Copy settings from `vapi_config.json`:
   - System prompt (handles phone trees and conversation flow)
   - First message
   - Functions (to capture call information)
   - Voice settings

### 6. Configure Webhook (Recommended)

The webhook URL tells Vapi.ai where to send call data. This is how your CSV gets automatically updated!

**Option A: Local Testing with ngrok (Recommended for first-time setup)**

1. Start your backend server:
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. In a new terminal, install and start ngrok:
   ```bash
   # Install ngrok: https://ngrok.com/download
   ngrok http 8000
   ```

3. Copy the https URL (e.g., `https://abc123.ngrok.io`)

4. Set the webhook URL environment variable:
   ```bash
   export VAPI_WEBHOOK_URL="https://abc123.ngrok.io/webhooks/vapi"
   ```

5. The script will automatically use this URL when creating the assistant

**Option B: Production Deployment**

1. Deploy your backend to a service (Heroku, Railway, Render, etc.)
2. Get your production URL (e.g., `https://your-app.herokuapp.com`)
3. Set the webhook URL:
   ```bash
   export VAPI_WEBHOOK_URL="https://your-app.herokuapp.com/webhooks/vapi"
   ```

**Note**: The webhook URL can also be set in the Vapi.ai dashboard under assistant settings, but using the environment variable is easier as the script handles it automatically.

### 7. Test Call to Your Phone

Before calling health centers, test the integration with your own phone:

```bash
cd vapi
python3 test_call.py 224-245-4540
```

Or use the default (your number is already configured):
```bash
cd vapi
python3 test_call.py
```

**What Happens:**
1. The script creates a Vapi.ai assistant
2. Calls your phone number
3. When you answer, the AI assistant will:
   - Introduce itself and explain it's calling about Connector Care Type I Coverage
   - Ask: "Are you currently taking new patients?"
   - Ask about waiting lists
   - Ask about expected availability dates
   - Ask about language support (Spanish, Portuguese, Haitian Creole)
   - Thank you and end the call

**Test Different Scenarios:**

You can practice different responses:

- **Scenario 1: Accepting New Patients**
  - Answer: "Yes, we are accepting new patients"
  - Answer: "No waiting list"
  - Answer: "Yes, we have Spanish-speaking providers"

- **Scenario 2: Waiting List**
  - Answer: "No, we're not accepting new patients right now"
  - Answer: "Yes, there is a waiting list"
  - Answer: "We expect availability in March 2025"
  - Answer: "We have providers who speak Spanish and Portuguese"

- **Scenario 3: No Language Support**
  - Answer: "No, we don't have providers speaking those languages"

**After the Test Call:**
- Check your phone's call log
- Check Vapi.ai dashboard for call recording and transcript
- Review how the assistant captured your responses
- If webhook is configured, check backend logs

### 8. Test with a Single Health Center

After testing with your phone, test with a single health center:

```bash
cd vapi
python3 vapi_call_manager.py ../community_health_centers_with_coords.csv 1
```

This will make 1 call (limit=1).

### 9. Run Batch Calls

Once tested, run calls for all health centers:

```bash
python vapi_call_manager.py community_health_centers_with_coords.csv
```

**Important Notes:**
- Calls are spaced 60 seconds apart by default (to avoid rate limiting)
- Monitor the CSV file to see results populate
- Check the backend logs for webhook events
- Review call recordings in Vapi.ai dashboard if needed

## Assistant Configuration

The assistant is configured to:

1. **Navigate Phone Trees**
   - Detects automated menus
   - Presses "0" to reach a representative
   - Waits patiently for transfers

2. **Ask Questions**
   - "Are you currently taking new patients?"
   - "If not, is there a waiting list?"
   - "When do you expect availability?"
   - "Do your providers speak Spanish, Portuguese, or Haitian Creole?"

3. **Capture Information**
   - Uses function calling to structure responses
   - Stores data in CSV via webhook

## Understanding Webhooks

### What is a Webhook?

A webhook is like a "callback URL" - when something happens in Vapi.ai (like a call completing), Vapi sends a notification to your server at the webhook URL.

### Why Do You Need It?

**Without a webhook:**
- ✅ Calls can be made
- ❌ Call data is NOT automatically saved to your CSV
- ❌ You'd have to manually check the Vapi dashboard and copy data

**With a webhook:**
- ✅ Calls are made
- ✅ Call data automatically flows back to your backend
- ✅ CSV file is automatically updated with call results
- ✅ No manual data entry needed!

### How It Works

1. **You initiate a call** → `vapi_call_manager.py` starts a call
2. **Vapi.ai makes the call** → AI assistant talks to health center
3. **Assistant captures data** → Uses function calls to structure responses
4. **Vapi sends webhook** → POST request to your `/webhooks/vapi` endpoint
5. **Backend receives data** → Webhook handler processes the information
6. **CSV gets updated** → Data is saved to `community_health_centers_with_coords.csv`

### Is It Just for Testing?

**No!** Webhooks are needed for both testing AND production:
- **Testing**: Use ngrok to expose local backend → test that data flows correctly
- **Production**: Deploy backend → use production URL → calls automatically save data

### Webhook Events

The webhook endpoint (`/webhooks/vapi`) handles:

- **function-call**: When assistant captures information → Updates CSV
- **call-end**: When call completes → Updates call status
- **status-update**: Status changes during call → Logs events

## CSV Data Structure

After calls, the CSV will include:

| Field | Description | Example Values |
|-------|-------------|----------------|
| `accepting_new_patients` | Are they accepting new patients? | `yes`, `no`, `unknown` |
| `has_waiting_list` | Is there a waiting list? | `yes`, `no`, `unknown` |
| `waiting_list_availability_date` | When will spots be available? | `January 2025`, `N/A` |
| `languages_supported` | Languages spoken by providers | `spanish, portuguese` |
| `call_notes` | Additional information | Free text |
| `last_called_date` | Timestamp of last call | `2024-01-15 14:30:00` |
| `call_status` | Status of the call | `completed`, `failed`, `no-answer`, `voicemail` |

## Displaying Call Data

The frontend automatically displays call information:
- **List View**: Shows call data in expandable sections
- **Map View**: Shows key info in info windows
- **Colors**: Green (yes), Red (no), Yellow (waiting list)

## Troubleshooting

### Calls Not Being Made

- Check API key is set: `echo $VAPI_API_KEY`
- Verify phone number is purchased in Vapi dashboard (script auto-detects it)
- Check assistant ID is set correctly
- Ensure phone number format is correct (E.164 format: +12242454540)

### Webhooks Not Receiving Events

- Verify backend is running and accessible
- Check webhook URL is publicly accessible (use ngrok for testing)
- Review backend logs for errors
- Test webhook endpoint: `curl -X POST http://localhost:8000/webhooks/vapi`

### CSV Not Updating

- Check file permissions on CSV file
- Verify webhook handler is finding health centers by phone number
- Review backend logs for CSV update errors
- Ensure CSV has the new columns (run `add_call_fields_to_csv.py`)

### Call Quality Issues

- Review call recordings in Vapi dashboard
- Adjust system prompt in `vapi_config.json` if needed
- Test with different health centers
- Consider using a different voice model

## Cost Considerations

Vapi.ai pricing:
- Pay-per-minute for calls
- Phone number rental (monthly fee)
- Check current pricing on Vapi.ai website

Tips to minimize costs:
- Test with a small batch first
- Space calls apart (already configured: 60 seconds)
- Review recordings to optimize prompt
- Consider calling during business hours only

## Best Practices

1. **Start Small**: Test with 5-10 centers first
2. **Monitor Calls**: Review recordings to improve prompts
3. **Respect Hours**: Only call during business hours
4. **Be Polite**: The assistant is configured to be respectful
5. **Update Prompt**: Refine the system prompt based on call results
6. **Backup Data**: CSV backups are created automatically
7. **Document Changes**: Keep notes on prompt improvements

## Advanced Configuration

### Custom System Prompt

Edit `vapi_config.json` to customize:
- Conversation flow
- Question wording
- Phone tree navigation logic
- Tone and style

### Multiple Assistants

You can create multiple assistants for:
- Different languages
- Different call types
- A/B testing prompts

### Scheduling

Set up a cron job or scheduled task to run calls:
- Daily during business hours
- Weekly updates
- Monthly refreshes

## Support

For issues:
1. Check Vapi.ai documentation: https://docs.vapi.ai
2. Review backend logs
3. Check CSV file for data
4. Test webhook endpoint manually
5. Review call recordings in Vapi dashboard
