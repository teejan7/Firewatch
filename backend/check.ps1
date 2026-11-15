$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) { $python = 'python' }
Push-Location $projectRoot
try {
    & $python -m ruff check backend\app backend\tests
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $testTemp = Join-Path $projectRoot '.tmp\pytest'
    New-Item -ItemType Directory -Force -Path $testTemp | Out-Null
    & $python -m pytest -q backend\tests --basetemp $testTemp -p no:cacheprovider
    exit $LASTEXITCODE
} finally { Pop-Location }
