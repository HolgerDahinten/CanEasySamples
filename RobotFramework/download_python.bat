@echo off
cls
echo **** Python Portable for CanEasy installer ***
echo : This batchfile will download portable python from sourceforge.net
echo : to be used with CanEasy
echo.

if exist "%~dp0python\" (
  echo ": A python directory already exists."
  echo ": Please remove (or rename) this directory before running this batch file."
  goto :eof
)
set /P continue=": Do you want to continue? (Y/N) "

if /I "%continue%"=="y" goto make_python
if /I "%continue%"=="yes" goto make_python

goto :eof

:make_python
@powershell.exe -noprofile -executionpolicy bypass -file download_python.ps1

setlocal

set INSTALLER=PortablePython.exe

echo ": Installing Python"
%INSTALLER% -o".\" -y
if errorlevel 1 goto ERROR

FOR /F " usebackq delims==" %%i IN (`dir /ad /b portable*`) DO set PORTABLE=%%i
echo : Found Python in "%~dp0%PORTABLE%"

echo ": Renaming python directory"
ren "%PORTABLE%" python
if errorlevel 1 goto ERROR

echo ": Upgrading pip"
.\python\App\Python\python.exe -m pip install -U pip --no-warn-script-location
if errorlevel 1 goto ERROR

echo ": Installing robotframework"
.\python\App\Python\python.exe -m pip install robotframework --no-warn-script-location
if errorlevel 1 goto ERROR

echo ": Installing pywin32"
.\python\App\Python\python.exe -m pip install pywin32 --no-warn-script-location
if errorlevel 1 goto ERROR

echo ": Installing Pillow"
.\python\App\Python\python.exe -m pip install Pillow --no-warn-script-location
if errorlevel 1 goto ERROR

echo.
echo python created in "%~dp0python"
echo You can delete the installer %INSTALLER% now
echo.
goto FINISH

:ERROR
echo ": ERROR"
goto FINISH

:FINISH
pause
