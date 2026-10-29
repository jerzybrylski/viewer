@echo off
setlocal
title The Genesis Order - inventory

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-ChildItem -LiteralPath '%~dp0' -File | Unblock-File -ErrorAction SilentlyContinue" >nul 2>&1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0COLLECT_TGO.ps1"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" (
  echo.
  echo The inventory did not finish. Read the error above.
) else (
  echo.
  echo Inventory complete. Upload the TGO_DIAGNOSTIC ZIP from your Desktop to Google Drive.
)
echo.
pause
exit /b %RC%
