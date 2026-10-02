$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$ExampleEnv = Join-Path $ProjectRoot ".env.example"

if (-not (Test-Path $Python)) {
    Write-Host "Project virtual environment not found at .venv." -ForegroundColor Red
    Write-Host "Create it and install requirements.txt before running this script."
    exit 1
}

if (-not (Test-Path $ExampleEnv)) {
    Write-Host ".env.example was not found." -ForegroundColor Red
    exit 1
}

$env:COMICCRAFT_ENV_FILE = $ExampleEnv

Write-Host "Starting ComicCraft with .env.example in offline demo mode..." -ForegroundColor Cyan
Write-Host "Website: http://127.0.0.1:8000"
Write-Host "Press CTRL+C to stop the server."

& $Python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
