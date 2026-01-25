#!/bin/bash

echo "========================================"
echo "  Financial AI Assistant"
echo "  Starting application..."
echo "========================================"
echo ""

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Warning: Virtual environment not found!"
    echo "Please run: python -m venv .venv"
    exit 1
fi

# Check if streamlit is installed
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the application
echo ""
echo "Starting Streamlit application..."
echo ""
streamlit run app.py
