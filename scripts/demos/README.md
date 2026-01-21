# Demo Scripts

Easy-to-run demo scripts for showcasing VAPI and OpenAI integration features.

## Quick Start

### Prerequisites

1. **For OpenAI Demo:**
   ```bash
   # Set up backend
   cd backend
   pip install -r requirements.txt
   echo "OPENAI_API_KEY=your_key_here" > .env
   uvicorn app.main:app --reload
   ```

2. **For VAPI Demo:**
   ```bash
   # Set API key
   export VAPI_API_KEY=your_vapi_api_key
   ```

## Demos

### 🤖 OpenAI Enrichment Demo

Demonstrates how OpenAI enriches health center data with verified information and new patient instructions.

**Run:**
```bash
# Make sure backend is running first
cd backend
uvicorn app.main:app --reload

# In another terminal, run the demo
python scripts/demos/demo_openai_enrichment.py
```

**What it shows:**
- Original health center data
- Enriched data from OpenAI
- Before/after comparison
- New patient instructions
- Confidence scores

**Expected output:**
- Shows original data (name, address, phone, website)
- Calls OpenAI enrichment API
- Displays enriched/verified data
- Shows new patient instructions
- Compares original vs enriched

---

### 📞 VAPI Phone Call Demo

Demonstrates how VAPI automatically calls health centers to collect information.

**Run:**
```bash
# Set API key
export VAPI_API_KEY=your_vapi_api_key

# Run demo (will prompt for phone number)
python scripts/demos/demo_vapi_call.py

# Or provide phone number directly
python scripts/demos/demo_vapi_call.py +12242454540
```

**What it shows:**
- VAPI call initiation
- Data structure that will be collected
- Call status tracking
- Where to find results

**Expected output:**
- Shows what data will be collected
- Initiates a phone call
- Tracks call status
- Provides links to view results

**Note:** You'll need to answer your phone and respond to the assistant's questions!

---

## Demo Flow for Presentations

### 1. OpenAI Enrichment Demo (5 minutes)

**Setup:**
```bash
# Terminal 1: Start backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Run demo
python scripts/demos/demo_openai_enrichment.py
```

**Talking Points:**
- "This shows how we use OpenAI to enrich health center data"
- "It verifies phone numbers and addresses"
- "Provides new patient instructions from web search"
- "Includes confidence scores for data quality"

### 2. VAPI Call Demo (5 minutes)

**Setup:**
```bash
# Set API key
export VAPI_API_KEY=your_key

# Run demo
python scripts/demos/demo_vapi_call.py +12242454540
```

**Talking Points:**
- "VAPI automatically calls health centers"
- "Collects structured data during the call"
- "Handles phone trees and navigation"
- "Provides transcripts and recordings"
- "Can scale to call all centers"

---

## Troubleshooting

### OpenAI Demo Issues

**Backend not running:**
```
❌ Backend server is not running!
```
**Solution:** Start backend with `cd backend && uvicorn app.main:app --reload`

**API Key not set:**
```
Error: OpenAI enrichment service not available
```
**Solution:** Add `OPENAI_API_KEY` to `backend/.env`

**Connection error:**
```
Could not connect to backend
```
**Solution:** Check backend is running on `http://localhost:8000`

### VAPI Demo Issues

**API Key not set:**
```
❌ Error: VAPI_API_KEY environment variable not set
```
**Solution:** `export VAPI_API_KEY=your_key`

**Import error:**
```
Could not import VapiCallManager
```
**Solution:** Run from project root directory

**Call fails:**
```
Failed to initiate call
```
**Solution:** 
- Check API key is valid
- Verify `vapi/vapi_config.json` exists
- Check VAPI dashboard for errors

---

## Files

- `demo_openai_enrichment.py` - OpenAI enrichment demo
- `demo_vapi_call.py` - VAPI phone call demo
- `README.md` - This file

---

## Tips for Presentations

1. **Run demos in separate terminals** - Keep backend running while demoing
2. **Have phone ready** - For VAPI demo, you'll need to answer your phone
3. **Show the code** - Point out key parts of the scripts
4. **Explain the flow** - Walk through what happens step by step
5. **Show results** - Display the enriched data or call transcripts

---

## Next Steps

After the demos, you can:
- Run full enrichment: `python scripts/enrich_csv.py`
- Make bulk VAPI calls: `python vapi/vapi_call_manager.py`
- View results in the CSV files
- See data displayed on the website
