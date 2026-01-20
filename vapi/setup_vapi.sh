#!/bin/bash
# Quick setup script for Vapi.ai integration

set -e

echo "🚀 Setting up Vapi.ai integration for Community Health Center Search"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Check if CSV file exists (in project root)
CSV_FILE="$PROJECT_ROOT/community_health_centers_with_coords.csv"
if [ ! -f "$CSV_FILE" ]; then
    echo "❌ Error: community_health_centers_with_coords.csv not found in project root"
    echo "   Please ensure the CSV file exists in: $PROJECT_ROOT"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found"
    exit 1
fi

# Install requirements
echo "📦 Installing Python requirements..."
cd "$SCRIPT_DIR"
pip install -q -r vapi_requirements.txt

# Add call fields to CSV
echo "📝 Adding call data fields to CSV..."
python3 add_call_fields_to_csv.py "$CSV_FILE"

# Check environment variables
echo ""
echo "🔑 Environment Variables Check:"
if [ -z "$VAPI_API_KEY" ]; then
    echo "   ⚠️  VAPI_API_KEY not set"
    echo "   Set it with: export VAPI_API_KEY=your_key_here"
else
    echo "   ✅ VAPI_API_KEY is set"
fi

if [ -z "$VAPI_WEBHOOK_URL" ]; then
    echo "   ⚠️  VAPI_WEBHOOK_URL not set (optional but recommended)"
    echo "   Set it with: export VAPI_WEBHOOK_URL=https://your-webhook-url.com/webhooks/vapi"
else
    echo "   ✅ VAPI_WEBHOOK_URL is set"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Set VAPI_API_KEY environment variable"
echo "2. (Optional) Set VAPI_WEBHOOK_URL for webhook callbacks"
echo "3. Start the backend server: cd backend && uvicorn app.main:app --reload"
echo "4. Run a test call: cd vapi && python3 vapi_call_manager.py ../community_health_centers_with_coords.csv 1"
echo ""
echo "For detailed instructions, see: vapi/VAPI_SETUP.md"
echo ""
echo "Note: This script should be run from the project root directory."
