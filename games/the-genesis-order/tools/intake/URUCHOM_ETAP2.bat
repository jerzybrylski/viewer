@echo off
setlocal
cd /d "%~dp0"
echo The Genesis Order - targeted stage 2 sample
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0COLLECT_TGO_STAGE2.ps1"
set "RESULT=%ERRORLEVEL%"
echo.
if not "%RESULT%"=="0" echo The collection did not finish successfully. See the message above.
echo Press any key to close this window.
pause >nul
exit /b %RESULT%
