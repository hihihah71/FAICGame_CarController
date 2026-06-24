@echo off
setlocal
cd /d "%~dp0"

py -3.10 --version >nul 2>&1
if errorlevel 1 (
    echo Python 3.10 was not found.
    echo Please install Python 3.10 from https://www.python.org/downloads/
    echo Make sure the py launcher is installed.
    pause
    exit /b 1
)

echo Creating virtual environment...
py -3.10 -m venv .venv
if errorlevel 1 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements.
    pause
    exit /b 1
)

echo Setup complete.
pause
