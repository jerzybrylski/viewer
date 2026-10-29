@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
rem Cofniecie uzywa zapamietanej instalacji (albo ja znajduje / pyta oknem wyboru).
set "PY="
py -3 -c "import sys; assert sys.version_info >= (3,10)" >nul 2>&1
if not errorlevel 1 set "PY=py -3"
if not defined PY (
  python -c "import sys; assert sys.version_info >= (3,10)" >nul 2>&1
  if not errorlevel 1 set "PY=python"
)
if not defined PY (
  echo BLAD: wymagany Python 3.10 lub nowszy. Niczego nie zmieniono.
  pause
  exit /b 2
)
echo.
%PY% "%~dp0patcher.py" rollback %*
set "RESULT=%ERRORLEVEL%"
echo.
pause
exit /b %RESULT%
