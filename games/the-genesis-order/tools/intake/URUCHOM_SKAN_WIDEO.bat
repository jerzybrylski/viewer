@echo off
setlocal
title The Genesis Order - skan wstawek wideo

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-ChildItem -LiteralPath '%~dp0' -File | Unblock-File -ErrorAction SilentlyContinue" >nul 2>&1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0SCAN_MOVIES_TGO.ps1"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" (
  echo.
  echo Skan nie zakonczyl sie. Przeczytaj komunikat powyzej.
) else (
  echo.
  echo Gotowe. Przeslij plik TGO_movie_calls_....json z Pulpitu.
)
echo.
pause
exit /b %RC%
