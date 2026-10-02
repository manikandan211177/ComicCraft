#!/usr/bin/env bash

# =========================================================
# ComicCraft - Demo Launcher
# Linux / macOS / Git Bash / WSL
# =========================================================

set -e


echo ""
echo "============================================="
echo "        ComicCraft - Demo Mode"
echo "============================================="
echo ""


# ---------------------------------------------------------
# Find project root
# ---------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"


echo "Project directory:"
echo "$PROJECT_ROOT"
echo ""


# ---------------------------------------------------------
# Check Python
# ---------------------------------------------------------

echo "Checking Python..."


if command -v python3 >/dev/null 2>&1; then

    PYTHON="python3"

elif command -v python >/dev/null 2>&1; then

    PYTHON="python"

else

    echo ""
    echo "Python was not found."
    echo "Please install Python 3 and add it to PATH."
    exit 1

fi


$PYTHON --version

echo ""


# ---------------------------------------------------------
# Check virtual environment
# ---------------------------------------------------------

VENV_PATH="$PROJECT_ROOT/.venv"


if [ ! -d "$VENV_PATH" ]; then

    echo "Virtual environment not found."

    echo "Creating .venv..."

    "$PYTHON" -m venv .venv

    echo ".venv created successfully."

fi


# ---------------------------------------------------------
# Activate virtual environment
# ---------------------------------------------------------

echo ""

echo "Activating virtual environment..."


if [ -f "$VENV_PATH/bin/activate" ]; then

    source "$VENV_PATH/bin/activate"

else

    echo "Virtual environment activation script not found."

    exit 1

fi


# ---------------------------------------------------------
# Install requirements
# ---------------------------------------------------------

if [ -f "requirements.txt" ]; then

    echo ""

    echo "Installing/checking Python dependencies..."

    python -m pip install --upgrade pip

    python -m pip install -r requirements.txt

else

    echo ""

    echo "requirements.txt was not found."

    exit 1

fi


# ---------------------------------------------------------
# Demo environment
# ---------------------------------------------------------

export DEMO_MODE="true"

export IMAGE_PROVIDER="demo"


echo ""

echo "Demo configuration:"

echo "DEMO_MODE=true"

echo "IMAGE_PROVIDER=demo"

echo ""


# ---------------------------------------------------------
# Create runtime directories
# ---------------------------------------------------------

mkdir -p "$PROJECT_ROOT/static/panels"

mkdir -p "$PROJECT_ROOT/static/exports"


echo "Runtime directories ready."


# ---------------------------------------------------------
# Start FastAPI
# ---------------------------------------------------------

echo ""

echo "============================================="

echo "Starting ComicCraft..."

echo "============================================="

echo ""

echo "Website:"

echo "http://127.0.0.1:8000"

echo ""

echo "API documentation:"

echo "http://127.0.0.1:8000/docs"

echo ""

echo "Health check:"

echo "http://127.0.0.1:8000/health"

echo ""

echo "Press CTRL+C to stop the server."

echo ""


python -m uvicorn app.main:app \
    --host 127.0.0.1 \
    --port 8000 \
    --reload