@echo off
setlocal
cd /d "%~dp0"

echo Opening project in Jupyter...

where jupyter >nul 2>nul
if errorlevel 1 (
    echo.
    echo Jupyter was not found in PATH.
    echo Open Jupyter normally, then browse to this folder:
    echo %CD%
    echo.
    pause
    exit /b 1
)

jupyter lab --version >nul 2>nul
if not errorlevel 1 (
    jupyter lab "notebooks\01_patient_exploration.ipynb"
    exit /b
)

jupyter notebook "notebooks\01_patient_exploration.ipynb"
