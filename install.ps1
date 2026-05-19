#Requires -Version 7.0

param(
    [string]$Branch = ""
)

$ErrorActionPreference = "Stop"

$OHClone = "$env:USERPROFILE\.agents\skill-hub\openharness"
$OHRepo  = "https://github.com/Krual-T/OpenHarness.git"

# --- helpers ---

function Write-Step { Write-Host "==> $args" -ForegroundColor Cyan }
function Write-Info  { Write-Host "    $args" }
function Write-Err   { Write-Host "ERROR: $args" -ForegroundColor Red }

# --- prerequisite checks ---

foreach ($cmd in @("git", "uv")) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Err "$cmd is required but not found"
        exit 1
    }
}

# --- clone or update ---

if (Test-Path "$OHClone\.git") {
    Write-Step "Updating OpenHarness at $OHClone ..."
    Push-Location $OHClone
    try {
        git pull
    } finally {
        Pop-Location
    }
} else {
    if (Test-Path $OHClone) {
        Write-Err "$OHClone exists but is not a git repository"
        Write-Err "Remove it manually and retry."
        exit 1
    }
    Write-Step "Cloning OpenHarness to $OHClone ..."
    $parent = Split-Path $OHClone -Parent
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    if ($Branch) {
        git clone --branch $Branch $OHRepo $OHClone
    } else {
        git clone $OHRepo $OHClone
    }
}

# --- checkout branch if specified and repo already existed ---

if ($Branch) {
    Push-Location $OHClone
    try {
        git checkout $Branch
    } finally {
        Pop-Location
    }
}

# --- install CLI ---

Write-Step "Installing openharness CLI ..."
uv tool install --editable $OHClone

Write-Host ""
Write-Host "OpenHarness installed. Next, run this in each project:"
Write-Host "  openharness init --agent <claude|codex|all>"
