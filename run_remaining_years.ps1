param(
    [int[]]$Year,
    [string[]]$Product,
    [string[]]$Country,
    [switch]$AllYears,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) { $python = 'python' }

$arguments = @((Join-Path $projectRoot 'backend\scripts\build_daily.py'))
if ($AllYears) {
    $arguments += '--all-years'
} elseif ($Year) {
    foreach ($item in $Year) { $arguments += @('--year', "$item") }
} else {
    foreach ($item in 2020..2025) { $arguments += @('--year', "$item") }
}
foreach ($item in $Product) { $arguments += @('--product', $item) }
foreach ($item in $Country) { $arguments += @('--country', $item) }
if ($Force) { $arguments += '--force' }

Push-Location $projectRoot
try {
    & $python @arguments
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
