# Vapi.ai Integration

This folder contains all files related to the Vapi.ai integration for automated calling to community health centers.

## Files

- **`vapi_config.json`** - Assistant configuration with conversation prompts and settings
- **`vapi_call_manager.py`** - Main script to initiate and manage calls
- **`add_call_fields_to_csv.py`** - Script to add call data fields to CSV
- **`vapi_requirements.txt`** - Python dependencies
- **`setup_vapi.sh`** - Quick setup script (run from project root)
- **`setup_helper.py`** - Interactive setup checker
- **`test_call.py`** - Script to test call to your phone
- **`VAPI_SETUP.md`** - **Complete setup guide (start here!)**
- **`VAPI_INTEGRATION_SUMMARY.md`** - Technical summary of the integration

## Quick Start

From the project root directory:

```bash
# Run setup script
./vapi/setup_vapi.sh

# Or manually:
cd vapi
pip install -r vapi_requirements.txt
python3 add_call_fields_to_csv.py ../community_health_centers_with_coords.csv

# Set environment variables
export VAPI_API_KEY="your_key"
export VAPI_WEBHOOK_URL="https://your-url.com/webhooks/vapi"

# Run a test call
python3 vapi_call_manager.py ../community_health_centers_with_coords.csv 1
```

## Usage

All scripts should be run from the `vapi/` directory, with paths to files in the parent directory.

The CSV file (`community_health_centers_with_coords.csv`) should be in the project root.

For detailed instructions, see **VAPI_SETUP.md**.
