@echo off
setlocal
cd /d "%~dp0"

echo.
echo ========================================
echo        FitBuddy AI - One Click Run
echo ========================================
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py"
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set "PY=python"
    ) else (
        echo Python was not found.
        echo Please install Python 3.10+ from https://www.python.org/downloads/
        echo Make sure "Add Python to PATH" is checked.
        pause
        exit /b 1
    )
)

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creating virtual environment...
    %PY% -m venv .venv
    if errorlevel 1 goto :error
)

set "VPY=%~dp0.venv\Scripts\python.exe"

echo [2/3] Installing/updating dependencies...
"%VPY%" -m pip install --disable-pip-version-check -q -r requirements.txt
if errorlevel 1 goto :error

echo [3/3] Starting FitBuddy...
start "FitBuddy Server" /min "%VPY%" launcher.py

timeout /t 2 /nobreak >nul
echo.
echo FitBuddy is running at http://127.0.0.1:8000
echo Keep this window open while using the website.
echo Close the "FitBuddy Server" window to stop the server.
echo.
pause
exit /b 0

:error
echo.
echo Something went wrong while setting up FitBuddy.
echo Read the message above, fix the issue, and run run.bat again.
echo.
pause
exit /b 1
