@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
set "GAME=%~1"
if not defined GAME set /p "GAME=Podaj folder The Genesis Order (zawierający www\index.html): "
if not defined GAME goto fail
set "PY="
py -3 -c "import sys; assert sys.version_info >= (3,10)" >nul 2>&1
if not errorlevel 1 set "PY=py -3"
if not defined PY (
  python -c "import sys; assert sys.version_info >= (3,10)" >nul 2>&1
  if not errorlevel 1 set "PY=python"
)
if not defined PY (
  echo BLAD: wymagany Python 3.10 lub nowszy. Niczego nie zmieniono.
  goto fail
)
echo.
echo Sprawdzanie fingerprintow i tworzenie kopii zapasowych...
%PY% "%~dp0patcher.py" apply "%GAME%"
set "RESULT=%ERRORLEVEL%"
echo.
if "%RESULT%"=="0" echo Operacja zakonczona. Raport stanu jest w folderze gry.
pause
exit /b %RESULT%
:fail
echo Operacja przerwana. Nie modyfikowano plikow gry.
pause
exit /b 2
