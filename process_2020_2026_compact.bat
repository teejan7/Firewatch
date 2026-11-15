@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo FIREWATCH Python environment was not found. Run start.bat once, then retry.
  pause
  exit /b 1
)
echo Processing 2020-2026 FIRMS records into compact cell summaries.
echo Raw source CSV files will not be changed.
".venv\Scripts\python.exe" backend\scripts\build_processed.py --year 2020 --year 2021 --year 2022 --year 2023 --year 2024 --year 2025 --year 2026 --compact-cells --build-daily-cells
if errorlevel 1 (
  echo Processing stopped. Read the preflight or per-file error above. Raw files are preserved.
  pause
  exit /b 1
)
echo Compact daily-cell data is ready. Verify the dashboard before removing any derived files.
pause
endlocal
