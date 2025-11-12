#!/bin/bash

# AlphaAgents Portfolio Optimizer - Run Script
# This script starts the Streamlit web application

echo "=================================="
echo "AlphaAgents Portfolio Optimizer"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo ""
    echo "Please create a .env file with your API keys:"
    echo "GOOGLE_API_KEY=your_google_api_key_here"
    echo "ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        exit 1
    fi
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
python3 -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Installing required packages..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install requirements."
        echo "Please run: pip install -r requirements.txt"
        exit 1
    fi
fi

echo "✅ Dependencies OK"
echo ""
echo "🚀 Starting AlphaAgents UI..."
echo ""
echo "================================================"
echo "Access the app from your browser at:"
echo ""
echo "  http://$(hostname -I | awk '{print $1}'):8501"
echo ""
echo "Or if you know your server's public IP/domain:"
echo "  http://YOUR_SERVER_IP:8501"
echo "================================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run Streamlit
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
