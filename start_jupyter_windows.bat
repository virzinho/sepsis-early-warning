@echo off
setlocal
cd /d "%~dp0"

echo.
echo ==========================================
echo   Sepsis Early Warning - Jupyter Launcher
echo ==========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found on this computer.
    echo Install Python 3 from https://www.python.org/downloads/
    echo IMPORTANT: during installation tick "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo First launch: creating the project environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Could not create the virtual environment.
        pause
        exit /b 1
    )

    call ".venv\Scripts\activate.bat"
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Dependency installation failed.
        pause
        exit /b 1
    )
) else (
    call ".venv\Scripts\activate.bat"
)

echo.
echo Opening JupyterLab...
echo Close this black window only when you have finished working.
echo.

jupyter lab
