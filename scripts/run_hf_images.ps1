$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$EnvFile = Join-Path $ProjectRoot ".env"

if (-not (Test-Path $Python)) {
    Write-Host "Project virtual environment not found at .venv." -ForegroundColor Red
    Write-Host "Create it and install requirements.txt before running this script."
    exit 1
}

if (-not (Test-Path $EnvFile)) {
    Write-Host "Local .env file was not found." -ForegroundColor Red
    Write-Host "Copy .env.example to .env, then add your Hugging Face token to .env."
    exit 1
}

$env:COMICCRAFT_ENV_FILE = $EnvFile
$env:DEMO_MODE = "true"
$env:IMAGE_PROVIDER = "hf"

& $Python -c "from app.config import get_settings; raise SystemExit(0 if get_settings().hf_api_key.strip() else 1)"

$tokenProvidedAtPrompt = $false

if ($LASTEXITCODE -ne 0) {
    if ([Console]::IsInputRedirected) {
        Write-Host "HF_API_KEY is not configured in .env." -ForegroundColor Red
        Write-Host "Run this script from an interactive PowerShell terminal to enter the token securely."
        exit 1
    }

    $secureToken = Read-Host "Enter your Hugging Face token (input is hidden; it will not be saved)" -AsSecureString

    if ($secureToken.Length -eq 0) {
        Write-Host "No Hugging Face token was entered. Image generation cannot start." -ForegroundColor Red
        exit 1
    }

    $tokenPointer = [IntPtr]::Zero

    try {
        $tokenPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureToken)
        $env:HF_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($tokenPointer)
        $tokenProvidedAtPrompt = $true
    }
    finally {
        if ($tokenPointer -ne [IntPtr]::Zero) {
            [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($tokenPointer)
        }

        $secureToken.Dispose()
    }
}

& $Python -c "from app.config import get_settings; print('Using Hugging Face model: ' + get_settings().image_model)"

Write-Host "Starting ComicCraft with demo stories and Hugging Face images..." -ForegroundColor Cyan
Write-Host "Each of the five panels will request its own generated image."
Write-Host "Website: http://127.0.0.1:8000"
Write-Host "Press CTRL+C to stop the server."

try {
    & $Python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
}
finally {
    if ($tokenProvidedAtPrompt) {
        $env:HF_API_KEY = ""
    }
}
