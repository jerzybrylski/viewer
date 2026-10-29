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
echo Weryfikowanie hashy plikow i backupow przed przywroceniem...
%PY% "%~dp0patcher.py" rollback "%GAME%"
set "RESULT=%ERRORLEVEL%"
echo.
pause
exit /b %RESULT%
:fail
echo Operacja przerwana. Niczego nie zmieniono.
pause
exit /b 2
