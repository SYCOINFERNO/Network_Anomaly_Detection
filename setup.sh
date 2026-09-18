#!/bin/bash

# Setup script for Network Anomaly Detection project

echo "🔒 Network Anomaly Detection System - Setup"
echo "==========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create data directory
mkdir -p data

# Generate network logs
echo ""
echo "🌐 Generating network logs..."
python3 src/log_generator.py

# Initialize database and load logs
echo ""
echo "💾 Loading logs into database..."
python3 src/database.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "📊 To run the dashboard:"
echo "   streamlit run src/dashboard.py"
echo ""
echo "Then open: http://localhost:8501"
