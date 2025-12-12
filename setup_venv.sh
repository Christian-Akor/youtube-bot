#!/bin/bash
# Setup script for YouTube Viewer Bot

echo "=========================================="
echo "YouTube Viewer Bot - Setup"
echo "=========================================="

# Check if Python 3.12 is available
if ! command -v python3.12 &> /dev/null; then
    echo "Python 3.12 not found. Trying python3..."
    if ! command -v python3 &> /dev/null; then
        echo "Error: Python 3 is not installed"
        exit 1
    fi
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python3.12"
fi

echo "Using Python: $PYTHON_CMD"
$PYTHON_CMD --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "To run the bot:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo "  2. Run the bot:"
echo "     python run.py"
echo ""
echo "To deactivate the virtual environment:"
echo "  deactivate"
echo ""
