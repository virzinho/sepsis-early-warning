@echo off
setlocal
cd /d "%~dp0"

echo.
echo ==========================================
echo   Sepsis Early Warning - Jupyter Launcher
echo ==========================================
echo.

set "PYTHON_CMD="

where py >nul 2>nul
if not errorlevel 1 (
    py -3.13 -c "import sys" >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=py -3.13"

    if not defined PYTHON_CMD (
        py -3.12 -c "import sys" >nul 2>nul
        if not errorlevel 1 set "PYTHON_CMD=py -3.12"
    )
)

if not defined PYTHON_CMD (
    echo.
    echo Compatible Python not found.
    echo.
    echo This project needs Python 3.13 or 3.12.
    echo Your Python 3.15 is too new for some current Jupyter dependencies.
    echo.
    echo Install Python 3.13 x64 from:
    echo https://www.python.org/downloads/
    echo.
    echo During installation, enable "Add python.exe to PATH".
    echo Then close this window and run this file again.
    echo.
    pause
    exit /b 1
)

echo Using %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

if not exist ".venv-jupyter\Scripts\python.exe" (
    echo Creating a clean project environment...
    %PYTHON_CMD% -m venv .venv-jupyter
    if errorlevel 1 (
        echo.
        echo Could not create the virtual environment.
        pause
        exit /b 1
    )

    call ".venv-jupyter\Scripts\activate.bat"

    echo Updating pip...
    python -m pip install --upgrade pip

    echo Installing project dependencies...
    pip install -r requirements.txt

    if errorlevel 1 (
        echo.
        echo Dependency installation failed.
        echo Delete the .venv-jupyter folder and try again.
        pause
        exit /b 1
    )
) else (
    call ".venv-jupyter\Scripts\activate.bat"
)

echo.
echo Environment ready.
echo Opening the first notebook directly in JupyterLab...
echo.

jupyter lab "notebooks\01_patient_exploration.ipynb"

endlocal
