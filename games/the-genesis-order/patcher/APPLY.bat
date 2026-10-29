@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
rem Patch sam znajdzie instalacje (pamiec, Steam/GOG, typowe foldery) i w razie
rem watpliwosci otworzy okno wyboru folderu. Sciezke mozna tez podac argumentem
rem albo przeciagnac folder na ten plik.
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
echo Szukanie instalacji The Genesis Order...
%PY% "%~dp0patcher.py" apply %*
set "RESULT=%ERRORLEVEL%"
echo.
if "%RESULT%"=="0" echo Operacja zakonczona. Folder gry zostal zapamietany dla kolejnych uruchomien.
pause
exit /b %RESULT%
