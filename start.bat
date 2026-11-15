@echo off
setlocal
cd /d "%~dp0"
if not exist "node_modules" (
  echo Installing JavaScript dependencies...
  call npm install
  if errorlevel 1 goto failed
)
if not exist ".venv\Scripts\python.exe" (
  echo Creating Python environment...
  py -3 -m venv .venv
  if errorlevel 1 goto failed
)
".venv\Scripts\python.exe" -c "import fastapi, uvicorn" >nul 2>nul
if errorlevel 1 (
  echo Installing Python dependencies...
  ".venv\Scripts\python.exe" -m pip install -r backend\requirements.txt
  if errorlevel 1 goto failed
)
call npm run dev
goto done
:failed
echo FIREWATCH setup failed. Read the message above and retry after fixing the reported dependency issue.
pause
:done
endlocal
