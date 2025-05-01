# Aurum Visualization Dashboard

An interactive dashboard for visualizing transportation data built with Streamlit and Plotly.

## Features

- Interactive data visualization
- Support for multiple Excel file formats
- Detailed analytics for transportation metrics
- Export capabilities for charts and data

## Data Format

The dashboard expects Excel files with the following columns:
- Loading Date (A2:A1000)
- Truck No. (B2:B1000)
- Acquisition Type (C2:C1000)
- Loaded Quantity (D2:D1000)
- Destination (E2:E1000)
- Driver Name (F2:F1000)
- Helper Name (G2:G1000)

## Installation

```bash
pip install -r requirements.txt
streamlit run app.py