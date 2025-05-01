@echo off
echo Aurum Visualization Dashboard
echo ===========================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in the PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo.
    pause
    exit /b
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error creating virtual environment.
        pause
        exit /b
    )
)

REM Activate virtual environment and install requirements
echo Activating virtual environment and installing requirements...
call venv\Scripts\activate

echo Installing core requirements...
pip install -r requirements.txt

echo Installing additional dependencies for image export...
pip install kaleido

REM Create sample Excel file if it doesn't exist
if not exist sample_transportation_data.xlsx (
    echo Creating sample Excel file...
    python create_sample_excel.py
)

REM Check for warnings
echo.
echo Checking for potential warnings...
python check_warnings.py

REM Check for image export warnings
echo.
echo Checking image export functionality...
python check_image_export_warnings.py

REM Run the Streamlit app with warnings enabled
echo.
echo Starting the dashboard...
echo.
echo The dashboard will open in your web browser.
echo If it doesn't open automatically, go to http://localhost:8501
echo.
echo Press Ctrl+C in this window to stop the dashboard when you're done.
echo.
python -W all -m streamlit run app.py

REM Deactivate virtual environment
call venv\Scripts\deactivate

pause
