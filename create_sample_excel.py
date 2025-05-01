"""
Create a sample Excel file with data in the specific ranges required by the visualization tool.

This script:
1. Reads data from sample_data.csv
2. Creates an Excel file with data in the specific ranges:
   - Loading Date (K6:K2000)
   - Truck No. (C6:C2000)
   - Driver Name (BW6:BW2000)
   - Helper Name (CA6:CA2000)
   - Destination (T6:T2000)
"""

import pandas as pd
# numpy is imported but not used
# import numpy as np
from openpyxl import Workbook
# dataframe_to_rows is imported but not used
# from openpyxl.utils.dataframe import dataframe_to_rows
import os
from datetime import datetime


def create_sample_excel():
    """Create a sample Excel file with data in specific ranges"""

    print("Creating sample Excel file...")

    # Check if sample_data.csv exists
    if not os.path.exists('sample_data.csv'):
        print("Error: sample_data.csv not found. Creating dummy data instead.")
        # Create dummy data
        data = {
            'Loading Date': pd.date_range(start='2023-01-01', periods=30),
            'Truck No': ['T001', 'T002', 'T003', 'T001', 'T002', 'T004', 'T003', 'T001', 'T005', 'T002'] * 3,
            'Acquisition Type': ['Own', 'Lease', 'Own', 'Own', 'Lease', 'Lease', 'Own', 'Own', 'Lease', 'Lease'] * 3,
            'Driver Name': ['John Smith', 'Mike Johnson', 'Sarah Davis', 'John Smith', 'Mike Johnson',
                           'Alex Thompson', 'Sarah Davis', 'John Smith', 'Lisa Garcia', 'Mike Johnson'] * 3,
            'Helper Name': ['Tom Wilson', 'Jerry Adams', 'Bob Brown', 'Tom Wilson', 'Jerry Adams',
                           'Sam Taylor', 'Bob Brown', 'Tom Wilson', 'Tim Moore', 'Jerry Adams'] * 3,
            'Destination': ['New York', 'Los Angeles', 'Chicago', 'New York', 'Los Angeles',
                           'Miami', 'Chicago', 'New York', 'Boston', 'Los Angeles'] * 3,
            'Loaded Quantity': [1250, 980, 1450, 1200, 950, 1350, 1500, 1150, 850, 920] * 3
        }
        df = pd.DataFrame(data)
    else:
        # Read the sample data
        df = pd.read_csv('sample_data.csv')

    # Create a new workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Transportation Data"

    # Add a header row
    ws['A1'] = "Aurum Data Sample"

    # Add column headers
    ws['A2'] = "Loading Date"
    ws['B2'] = "Truck No."
    ws['C2'] = "Acquisition Type"
    ws['D2'] = "Driver Name"
    ws['E2'] = "Helper Name"
    ws['F2'] = "Destination"
    ws['G2'] = "Loaded Quantity"

    # Place data in the specific ranges
    # Start from row 3 (after headers)
    start_row = 3

    # Loading Date (A3:A1000)
    for i, value in enumerate(df['Loading Date'], start=start_row):
        ws[f'A{i}'] = value

    # Truck No. (B3:B1000)
    for i, value in enumerate(df['Truck No'], start=start_row):
        ws[f'B{i}'] = value

    # Acquisition Type (C3:C1000)
    if 'Acquisition Type' in df.columns:
        for i, value in enumerate(df['Acquisition Type'], start=start_row):
            ws[f'C{i}'] = value

    # Driver Name (D3:D1000)
    for i, value in enumerate(df['Driver Name'], start=start_row):
        ws[f'D{i}'] = value

    # Helper Name (E3:E1000)
    for i, value in enumerate(df['Helper Name'], start=start_row):
        ws[f'E{i}'] = value

    # Destination (F3:F1000)
    for i, value in enumerate(df['Destination'], start=start_row):
        ws[f'F{i}'] = value

    # Loaded Quantity (G3:G1000)
    if 'Loaded Quantity' in df.columns:
        for i, value in enumerate(df['Loaded Quantity'], start=start_row):
            ws[f'G{i}'] = value

    # Save the workbook with error handling
    output_file = "sample_transportation_data.xlsx"
    try:
        wb.save(output_file)
        print(f"Sample Excel file created: {output_file}")
        print(f"Contains {len(df)} records in the specified ranges")
    except Exception as e:
        print(f"Error saving Excel file: {e}")
        # Try to save in the current directory with a different name if there's an error
        try:
            alt_output_file = f"sample_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            wb.save(alt_output_file)
            print(f"Saved alternative file: {alt_output_file}")
        except Exception as e2:
            print(f"Failed to save alternative file: {e2}")


if __name__ == "__main__":
    create_sample_excel()
