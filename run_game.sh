#!/bin/bash
# Quick start script for Unix-like systems (Linux/macOS)
# Retro Platform Fighter - Diamond Quest

echo ""
echo "========================================"
echo " Retro Platform Fighter - Diamond Quest"
echo "========================================"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python is not installed"
    echo "   Please install Python 3.8+ from your package manager or https://python.org"
    exit 1
fi

echo "Checking Python version..."
$PYTHON_CMD --version

# Check Python version (requires 3.8+)
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Error: Python 3.8 or higher is required"
    echo "   Current version: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python version check passed"
echo ""

# Check if pip is available
if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
    echo "❌ Error: pip is not available"
    echo "   Please install pip for your Python installation"
    exit 1
fi

echo "Installing/updating dependencies..."
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error: Failed to install dependencies"
    echo "   Please check your internet connection and try again"
    echo "   You may need to install system dependencies first:"
    echo "   Ubuntu/Debian: sudo apt install python3-dev libsdl2-dev"
    echo "   CentOS/RHEL: sudo dnf install python3-devel SDL2-devel"
    exit 1
fi

echo ""
echo "🎮 Starting game..."
$PYTHON_CMD retro_platform_game.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error: Failed to start game"
    echo "   Check the error messages above"
    exit 1
fi

echo ""
echo "👋 Thanks for playing!"
