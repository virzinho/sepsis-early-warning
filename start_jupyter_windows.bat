@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_CMD="
set "ENV_DIR=%LOCALAPPDATA%\sepsis-early-warning-venv"
set "REQ_COPY=%ENV_DIR%\requirements.txt"

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
    echo Python 3.13 or 3.12 is required for this project.
    echo Your Python 3.15 can stay installed.
    pause
    exit /b 1
)

if not exist "%ENV_DIR%\Scripts\python.exe" (
    echo First setup only: creating Jupyter environment...
    %PYTHON_CMD% -m venv "%ENV_DIR%"
    call "%ENV_DIR%\Scripts\activate.bat"
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Installation failed.
        pause
        exit /b 1
    )
    copy /Y requirements.txt "%REQ_COPY%" >nul
) else (
    call "%ENV_DIR%\Scripts\activate.bat"

    if not exist "%REQ_COPY%" (
        pip install -r requirements.txt
        copy /Y requirements.txt "%REQ_COPY%" >nul
    ) else (
        fc /b requirements.txt "%REQ_COPY%" >nul
        if errorlevel 1 (
            echo Project dependencies changed. Updating once...
            pip install -r requirements.txt
            copy /Y requirements.txt "%REQ_COPY%" >nul
        )
    )
)

echo Opening Jupyter...
jupyter lab "notebooks\01_patient_exploration.ipynb"

endlocal
