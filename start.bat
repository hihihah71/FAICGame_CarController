@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\activate.bat" (
    echo Virtual environment not found. Running setup...
    call setup.bat
    if errorlevel 1 (
        echo Setup failed.
        pause
        exit /b 1
    )
)

call .venv\Scripts\activate.bat
python -c "import customtkinter, PIL" >nul 2>&1
if errorlevel 1 (
    echo Required UI packages are missing. Installing requirements...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install requirements.
        pause
        exit /b 1
    )
)

python main.py
if errorlevel 1 (
    echo App exited with an error.
    pause
    exit /b 1
)
