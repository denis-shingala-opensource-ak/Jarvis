#!/bin/bash
# Jarvis Smart Voice Assistant - Setup Script

set -e

echo "========================================="
echo "  Jarvis Smart Voice Assistant - Setup"
echo "========================================="
echo ""

# Install system dependencies
echo "[1/4] Installing system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y -qq ffmpeg > /dev/null 2>&1
echo "  -> ffmpeg installed"

# Create virtual environment
echo "[2/4] Creating virtual environment..."
python3 -m venv venv
echo "  -> venv created"

# Activate and install Python dependencies
echo "[3/4] Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "  -> Dependencies installed"

# Copy .env if it doesn't exist
echo "[4/4] Setting up configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "  -> Created .env from .env.example"
    echo "  -> IMPORTANT: Edit .env and add your API keys!"
else
    echo "  -> .env already exists, skipping"
fi

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your OpenAI/Anthropic API key"
echo "  2. Activate venv:  source venv/bin/activate"
echo "  3. Run Jarvis:     python run.py"
echo "  4. Open browser:   http://localhost:8000"
echo ""
