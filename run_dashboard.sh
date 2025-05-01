#!/bin/bash

echo "Aurum Visualization Dashboard"
echo "============================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in the PATH."
    echo "Please install Python 3.8 or higher from https://www.python.org/downloads/"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error creating virtual environment."
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Activate virtual environment and install requirements
echo "Activating virtual environment and installing requirements..."
source venv/bin/activate

echo "Installing core requirements..."
pip install -r requirements.txt

echo "Installing additional dependencies for image export..."
pip install kaleido

# Create sample Excel file if it doesn't exist
if [ ! -f "sample_transportation_data.xlsx" ]; then
    echo "Creating sample Excel file..."
    python create_sample_excel.py
fi

# Check for warnings
echo
echo "Checking for potential warnings..."
python check_warnings.py

# Check for image export warnings
echo
echo "Checking image export functionality..."
python check_image_export_warnings.py

# Run the Streamlit app with warnings enabled
echo
echo "Starting the dashboard..."
echo
echo "The dashboard will open in your web browser."
echo "If it doesn't open automatically, go to http://localhost:8501"
echo
echo "Press Ctrl+C in this window to stop the dashboard when you're done."
echo
python -W all -m streamlit run app.py

# Deactivate virtual environment
deactivate

read -p "Press Enter to exit..."
