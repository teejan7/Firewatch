@echo off
setlocal
cd /d "%~dp0"
if not exist "node_modules" (
  echo Installing JavaScript dependencies...
  call npm ci
  if errorlevel 1 goto failed
)
call npm run start
goto done
:failed
echo FIREWATCH setup failed. Read the message above and retry after fixing the reported dependency issue.
pause
:done
endlocal
