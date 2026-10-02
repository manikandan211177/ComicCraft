# =========================================================
# ComicCraft - Demo Launcher
# Windows PowerShell
# =========================================================

$ErrorActionPreference = "Stop"


Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "        ComicCraft - Demo Mode" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""


# ---------------------------------------------------------
# Find project root
# ---------------------------------------------------------

$ProjectRoot = Split-Path -Parent $PSScriptRoot

Set-Location $ProjectRoot

Write-Host "Project directory:" -ForegroundColor Yellow
Write-Host $ProjectRoot
Write-Host ""


# ---------------------------------------------------------
# Check Python
# ---------------------------------------------------------

Write-Host "Checking Python..." -ForegroundColor Yellow

try {

    $pythonVersion = python --version 2>&1

    Write-Host $pythonVersion -ForegroundColor Green

}
catch {

    Write-Host ""
    Write-Host "Python was not found." -ForegroundColor Red
    Write-Host "Please install Python and add it to PATH."
    exit 1

}


# ---------------------------------------------------------
# Check virtual environment
# ---------------------------------------------------------

$VenvPath = Join-Path $ProjectRoot ".venv"


if (-Not (Test-Path $VenvPath)) {

    Write-Host ""
    Write-Host "Virtual environment not found." -ForegroundColor Yellow

    Write-Host "Creating .venv..." -ForegroundColor Yellow

    python -m venv .venv

    if ($LASTEXITCODE -ne 0) {

        Write-Host ""
        Write-Host "Failed to create virtual environment." -ForegroundColor Red
        exit 1

    }

    Write-Host ".venv created successfully." -ForegroundColor Green

}


# ---------------------------------------------------------
# Activate virtual environment
# ---------------------------------------------------------

$ActivateScript =
    Join-Path $VenvPath "Scripts\Activate.ps1"


if (-Not (Test-Path $ActivateScript)) {

    Write-Host ""
    Write-Host "Virtual environment activation script not found." -ForegroundColor Red
    exit 1

}


Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow

& $ActivateScript


# ---------------------------------------------------------
# Install requirements
# ---------------------------------------------------------

if (Test-Path "requirements.txt") {

    Write-Host ""
    Write-Host "Installing/checking Python dependencies..." -ForegroundColor Yellow

    python -m pip install --upgrade pip

    python -m pip install -r requirements.txt

    if ($LASTEXITCODE -ne 0) {

        Write-Host ""
        Write-Host "Failed to install dependencies." -ForegroundColor Red
        exit 1

    }

}
else {

    Write-Host ""
    Write-Host "requirements.txt was not found." -ForegroundColor Red
    exit 1

}


# ---------------------------------------------------------
# Demo environment
# ---------------------------------------------------------

$env:DEMO_MODE = "true"
$env:IMAGE_PROVIDER = "demo"


Write-Host ""
Write-Host "Demo configuration:" -ForegroundColor Yellow

Write-Host "DEMO_MODE=true" -ForegroundColor Green
Write-Host "IMAGE_PROVIDER=demo" -ForegroundColor Green

Write-Host ""


# ---------------------------------------------------------
# Create runtime directories
# ---------------------------------------------------------

$PanelsDirectory =
    Join-Path $ProjectRoot "static\panels"


$ExportsDirectory =
    Join-Path $ProjectRoot "static\exports"


if (-Not (Test-Path $PanelsDirectory)) {

    New-Item `
        -ItemType Directory `
        -Path $PanelsDirectory `
        -Force | Out-Null

}


if (-Not (Test-Path $ExportsDirectory)) {

    New-Item `
        -ItemType Directory `
        -Path $ExportsDirectory `
        -Force | Out-Null

}


Write-Host "Runtime directories ready." -ForegroundColor Green


# ---------------------------------------------------------
# Start FastAPI
# ---------------------------------------------------------

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Starting ComicCraft..." -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Website:" -ForegroundColor Yellow
Write-Host "http://127.0.0.1:8000" -ForegroundColor Green

Write-Host ""

Write-Host "API documentation:" -ForegroundColor Yellow
Write-Host "http://127.0.0.1:8000/docs" -ForegroundColor Green

Write-Host ""

Write-Host "Health check:" -ForegroundColor Yellow
Write-Host "http://127.0.0.1:8000/health" -ForegroundColor Green

Write-Host ""

Write-Host "Press CTRL+C to stop the server." -ForegroundColor DarkGray

Write-Host ""


python -m uvicorn app.main:app `
    --host 127.0.0.1 `
    --port 8000 `
    --reload