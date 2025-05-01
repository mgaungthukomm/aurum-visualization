"""
Data Processor Module for Transportation Data Visualization

This module handles reading and processing Excel data for visualization.
It extracts data from specific ranges:
- Loading Date (K6:K2000)
- Truck No. (C6:C2000)
- Driver Name (BW6:BW2000)
- Helper Name (CA6:CA2000)
- Destination (T6:T2000)
"""

import pandas as pd
from datetime import datetime  # Used in get_summary_stats and export functions
# numpy is imported but not used, removing to avoid warning
# import numpy as np


def read_excel_data(file_path):
    """
    Read data from specific Excel ranges.

    Args:
        file_path (str): Path to the Excel file

    Returns:
        pd.DataFrame: Processed DataFrame with combined data
    """
    try:
        # Read the Excel file
        xl = pd.ExcelFile(file_path)

        # Get the first sheet name
        sheet_name = xl.sheet_names[0]

        # Read data from the new ranges (A2:G1000) with updated column order
        try:
            # Try to read all columns at once
            df = pd.read_excel(file_path, sheet_name=sheet_name,
                              usecols="A:G", skiprows=1, nrows=999)

            # Check if we have enough columns
            if len(df.columns) >= 6:
                # Rename columns to match the actual structure:
                # A: Loading Date, B: Truck, C: Acquisition, D: Quantity, E: Destination, F: Driver, G: Helper
                column_names = ['Loading Date', 'Truck No', 'Acquisition Type', 'Loaded Quantity',
                               'Destination', 'Driver Name', 'Helper Name']
                df.columns = column_names[:len(df.columns)]

                # If any columns are missing, add them with default values
                for i, col in enumerate(column_names):
                    if i >= len(df.columns):
                        df[col] = 'Unknown'
            else:
                # Not enough columns, try individual approach
                raise Exception("Not enough columns found")

        except Exception as e:
            print(f"Error reading all columns at once: {e}")
            print("Trying to read individual columns...")

            # Read specific ranges individually based on the actual column order
            # A: Loading Date, B: Truck, C: Acquisition, D: Quantity, E: Destination, F: Driver, G: Helper
            loading_dates = pd.read_excel(file_path, sheet_name=sheet_name,
                                         usecols="A", skiprows=1, nrows=999)
            truck_nos = pd.read_excel(file_path, sheet_name=sheet_name,
                                     usecols="B", skiprows=1, nrows=999)
            acquisition_types = pd.read_excel(file_path, sheet_name=sheet_name,
                                             usecols="C", skiprows=1, nrows=999)

            # Read loaded quantity from column D
            try:
                loaded_quantities = pd.read_excel(file_path, sheet_name=sheet_name,
                                                usecols="D", skiprows=1, nrows=999)
                loaded_quantities.columns = ['Loaded Quantity']
            except Exception:
                # If column doesn't exist, create a default one with zeros
                loaded_quantities = pd.DataFrame({'Loaded Quantity': [0] * len(loading_dates)})

            destinations = pd.read_excel(file_path, sheet_name=sheet_name,
                                        usecols="E", skiprows=1, nrows=999)
            driver_names = pd.read_excel(file_path, sheet_name=sheet_name,
                                        usecols="F", skiprows=1, nrows=999)
            helper_names = pd.read_excel(file_path, sheet_name=sheet_name,
                                        usecols="G", skiprows=1, nrows=999)

            # Rename columns to more descriptive names
            loading_dates.columns = ['Loading Date']
            truck_nos.columns = ['Truck No']
            acquisition_types.columns = ['Acquisition Type']
            destinations.columns = ['Destination']
            driver_names.columns = ['Driver Name']
            helper_names.columns = ['Helper Name']

            # Combine all dataframes in the correct order
            df = pd.concat([loading_dates, truck_nos, acquisition_types, loaded_quantities,
                           destinations, driver_names, helper_names], axis=1)

        # Clean the data
        df = clean_data(df)

        return df

    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None


def clean_data(df):
    """
    Clean and prepare the data for visualization.

    Args:
        df (pd.DataFrame): Raw DataFrame

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    # Remove rows where all values are NaN
    df = df.dropna(how='all')

    # Convert loading date to datetime if it's not already
    if df['Loading Date'].dtype != 'datetime64[ns]':
        df['Loading Date'] = pd.to_datetime(df['Loading Date'], errors='coerce')

    # Fill NaN values with appropriate placeholders
    df['Truck No'] = df['Truck No'].fillna('Unknown')
    df['Driver Name'] = df['Driver Name'].fillna('Unknown')
    df['Helper Name'] = df['Helper Name'].fillna('Unknown')
    df['Destination'] = df['Destination'].fillna('Unknown')

    # Clean and standardize acquisition type
    if 'Acquisition Type' in df.columns:
        # Convert to string and standardize values
        df['Acquisition Type'] = df['Acquisition Type'].astype(str).str.lower()
        # Map variations to standard values
        acquisition_map = {
            'own': 'Own',
            'owned': 'Own',
            'o': 'Own',
            'lease': 'Lease',
            'leased': 'Lease',
            'l': 'Lease',
            'rental': 'Lease',
            'rent': 'Lease',
            'r': 'Lease',
            'nan': 'Unknown',
            'unknown': 'Unknown',
            'none': 'Unknown'
        }
        # Apply mapping with a default of 'Unknown'
        df['Acquisition Type'] = df['Acquisition Type'].map(
            lambda x: acquisition_map.get(x.strip(), 'Unknown') if isinstance(x, str) else 'Unknown'
        )

    # Handle Loaded Quantity
    if 'Loaded Quantity' in df.columns:
        # Convert to numeric, coerce errors to NaN
        df['Loaded Quantity'] = pd.to_numeric(df['Loaded Quantity'], errors='coerce')
        # Replace NaN with 0
        df['Loaded Quantity'] = df['Loaded Quantity'].fillna(0)
        # Ensure it's an integer (or float if there are decimal values)
        if (df['Loaded Quantity'] % 1 == 0).all():
            df['Loaded Quantity'] = df['Loaded Quantity'].astype(int)
    else:
        # Add the column if it doesn't exist
        df['Loaded Quantity'] = 0

    # Remove rows with invalid dates
    df = df.dropna(subset=['Loading Date'])

    return df


def get_summary_stats(df):
    """
    Calculate summary statistics from the data.

    Args:
        df (pd.DataFrame): Processed DataFrame

    Returns:
        dict: Dictionary of summary statistics
    """
    stats = {
        'Total Records': len(df),
        'Unique Trucks': df['Truck No'].nunique(),
        'Unique Drivers': df['Driver Name'].nunique(),
        'Unique Helpers': df['Helper Name'].nunique(),
        'Unique Destinations': df['Destination'].nunique(),
        'Total Loaded Quantity': int(df['Loaded Quantity'].sum()),
        'Average Load per Trip': round(df['Loaded Quantity'].mean(), 2),
        'Date Range': f"{df['Loading Date'].min().strftime('%Y-%m-%d')} to {df['Loading Date'].max().strftime('%Y-%m-%d')}"
    }

    return stats


def get_destination_data(df):
    """
    Process data for destination analysis.

    Args:
        df (pd.DataFrame): Processed DataFrame

    Returns:
        pd.DataFrame: DataFrame with destination counts
    """
    destination_counts = df['Destination'].value_counts().reset_index()
    destination_counts.columns = ['Destination', 'Count']

    # Sort by count and take top 10
    destination_counts = destination_counts.sort_values('Count', ascending=False).head(10)

    return destination_counts


def get_truck_driver_data(df):
    """
    Process data for truck-driver relationship analysis.

    Args:
        df (pd.DataFrame): Processed DataFrame

    Returns:
        pd.DataFrame: DataFrame with truck-driver relationships
    """
    # Create a pivot table of truck-driver relationships
    truck_driver = pd.crosstab(df['Truck No'], df['Driver Name'])

    # Convert to long format for visualization
    truck_driver_long = truck_driver.reset_index().melt(
        id_vars='Truck No',
        var_name='Driver Name',
        value_name='Count'
    )

    # Filter out zero counts
    truck_driver_long = truck_driver_long[truck_driver_long['Count'] > 0]

    return truck_driver_long


def get_date_based_data(df):
    """
    Process data for date-based analysis.

    Args:
        df (pd.DataFrame): Processed DataFrame

    Returns:
        pd.DataFrame: DataFrame with date-based counts
    """
    # Create a copy of the dataframe to avoid SettingWithCopyWarning
    df_copy = df.copy()

    # Group by loading date and count
    df_copy['Loading Date'] = pd.to_datetime(df_copy['Loading Date']).dt.date
    date_counts = df_copy.groupby('Loading Date').size().reset_index()
    date_counts.columns = ['Loading Date', 'Count']

    # Sort by date
    date_counts = date_counts.sort_values('Loading Date')

    return date_counts


def get_helper_analysis(df):
    """
    Process data for helper analysis.

    Args:
        df (pd.DataFrame): Processed DataFrame

    Returns:
        pd.DataFrame: DataFrame with helper counts
    """
    helper_counts = df['Helper Name'].value_counts().reset_index()
    helper_counts.columns = ['Helper Name', 'Count']

    # Sort by count and take top 10
    helper_counts = helper_counts.sort_values('Count', ascending=False).head(10)

    return helper_counts


def get_truck_destination_data(df):
    """
    Process data for truck-destination analysis.

    Args:
        df (pd.DataFrame): Processed DataFrame

    Returns:
        pd.DataFrame: DataFrame with truck-destination relationships
    """
    # Create a pivot table of truck-destination relationships
    truck_destination = pd.crosstab(df['Truck No'], df['Destination'])

    # Convert to long format for visualization
    truck_destination_long = truck_destination.reset_index().melt(
        id_vars='Truck No',
        var_name='Destination',
        value_name='Count'
    )

    # Filter out zero counts
    truck_destination_long = truck_destination_long[truck_destination_long['Count'] > 0]

    return truck_destination_long


def get_acquisition_analysis(df):
    """
    Process data for acquisition type analysis.

    Args:
        df (pd.DataFrame): Processed DataFrame

    Returns:
        tuple: (acquisition_counts, acquisition_metrics) DataFrames with acquisition analysis
    """
    # Check if acquisition type column exists
    if 'Acquisition Type' not in df.columns:
        # Create a dummy DataFrame if the column doesn't exist
        acquisition_counts = pd.DataFrame({
            'Acquisition Type': ['Unknown'],
            'Count': [len(df)]
        })
        acquisition_metrics = pd.DataFrame({
            'Metric': ['Own Percentage', 'Lease Percentage', 'Unknown Percentage'],
            'Value': [0, 0, 100]
        })
        return acquisition_counts, acquisition_metrics

    # Count by acquisition type
    acquisition_counts = df['Acquisition Type'].value_counts().reset_index()
    acquisition_counts.columns = ['Acquisition Type', 'Count']

    # Calculate percentages
    total = acquisition_counts['Count'].sum()
    own_count = acquisition_counts[acquisition_counts['Acquisition Type'] == 'Own']['Count'].sum() if 'Own' in acquisition_counts['Acquisition Type'].values else 0
    lease_count = acquisition_counts[acquisition_counts['Acquisition Type'] == 'Lease']['Count'].sum() if 'Lease' in acquisition_counts['Acquisition Type'].values else 0
    unknown_count = acquisition_counts[acquisition_counts['Acquisition Type'] == 'Unknown']['Count'].sum() if 'Unknown' in acquisition_counts['Acquisition Type'].values else 0

    own_pct = (own_count / total * 100) if total > 0 else 0
    lease_pct = (lease_count / total * 100) if total > 0 else 0
    unknown_pct = (unknown_count / total * 100) if total > 0 else 0

    # Create metrics DataFrame
    acquisition_metrics = pd.DataFrame({
        'Metric': ['Own Percentage', 'Lease Percentage', 'Unknown Percentage'],
        'Value': [own_pct, lease_pct, unknown_pct]
    })

    return acquisition_counts, acquisition_metrics


def get_truck_assignments(df):
    """
    Process data for truck assignments analysis.

    Args:
        df (pd.DataFrame): Processed DataFrame

    Returns:
        pd.DataFrame: DataFrame with truck assignments and frequency
    """
    # Count trips by truck
    truck_counts = df['Truck No'].value_counts().reset_index()
    truck_counts.columns = ['Truck No', 'Trip Count']

    # Get unique destinations per truck
    truck_destinations = df.groupby('Truck No')['Destination'].nunique().reset_index()
    truck_destinations.columns = ['Truck No', 'Unique Destinations']

    # Get unique drivers per truck
    truck_drivers = df.groupby('Truck No')['Driver Name'].nunique().reset_index()
    truck_drivers.columns = ['Truck No', 'Unique Drivers']

    # Get acquisition type for each truck if available
    if 'Acquisition Type' in df.columns:
        # Get the most common acquisition type for each truck
        truck_acquisition = df.groupby('Truck No')['Acquisition Type'].agg(
            lambda x: x.value_counts().index[0] if len(x) > 0 else 'Unknown'
        ).reset_index()
        truck_acquisition.columns = ['Truck No', 'Acquisition Type']
    else:
        # Create a default acquisition type
        truck_acquisition = pd.DataFrame({
            'Truck No': truck_counts['Truck No'],
            'Acquisition Type': ['Unknown'] * len(truck_counts)
        })

    # Merge all data
    truck_assignments = pd.merge(truck_counts, truck_destinations, on='Truck No')
    truck_assignments = pd.merge(truck_assignments, truck_drivers, on='Truck No')
    truck_assignments = pd.merge(truck_assignments, truck_acquisition, on='Truck No')

    # Calculate utilization (trips per unique destination)
    truck_assignments = truck_assignments.assign(
        Utilization=truck_assignments['Trip Count'] / truck_assignments['Unique Destinations']
    )

    # Sort by trip count
    truck_assignments = truck_assignments.sort_values('Trip Count', ascending=False)

    return truck_assignments


def get_driver_assignments(df):
    """
    Process data for driver assignments analysis.

    Args:
        df (pd.DataFrame): Processed DataFrame

    Returns:
        pd.DataFrame: DataFrame with driver assignments and metrics
    """
    # Count trips by driver
    driver_counts = df['Driver Name'].value_counts().reset_index()
    driver_counts.columns = ['Driver Name', 'Trip Count']

    # Get unique trucks per driver
    driver_trucks = df.groupby('Driver Name')['Truck No'].nunique().reset_index()
    driver_trucks.columns = ['Driver Name', 'Unique Trucks']

    # Get unique destinations per driver
    driver_destinations = df.groupby('Driver Name')['Destination'].nunique().reset_index()
    driver_destinations.columns = ['Driver Name', 'Unique Destinations']

    # Get unique helpers per driver
    driver_helpers = df.groupby('Driver Name')['Helper Name'].nunique().reset_index()
    driver_helpers.columns = ['Driver Name', 'Unique Helpers']

    # Merge all data
    driver_assignments = pd.merge(driver_counts, driver_trucks, on='Driver Name')
    driver_assignments = pd.merge(driver_assignments, driver_destinations, on='Driver Name')
    driver_assignments = pd.merge(driver_assignments, driver_helpers, on='Driver Name')

    # Calculate truck consistency (lower number means driver uses fewer trucks)
    driver_assignments = driver_assignments.assign(
        Truck_Consistency=driver_assignments['Unique Trucks'] / driver_assignments['Trip Count']
    )

    # Sort by trip count
    driver_assignments = driver_assignments.sort_values('Trip Count', ascending=False)

    return driver_assignments


def get_helper_assignments(df):
    """
    Process data for helper assignments analysis.

    Args:
        df (pd.DataFrame): Processed DataFrame

    Returns:
        pd.DataFrame: DataFrame with helper assignments and metrics
    """
    # Count trips by helper
    helper_counts = df['Helper Name'].value_counts().reset_index()
    helper_counts.columns = ['Helper Name', 'Trip Count']

    # Get unique drivers per helper
    helper_drivers = df.groupby('Helper Name')['Driver Name'].nunique().reset_index()
    helper_drivers.columns = ['Helper Name', 'Unique Drivers']

    # Get unique trucks per helper
    helper_trucks = df.groupby('Helper Name')['Truck No'].nunique().reset_index()
    helper_trucks.columns = ['Helper Name', 'Unique Trucks']

    # Get unique destinations per helper
    helper_destinations = df.groupby('Helper Name')['Destination'].nunique().reset_index()
    helper_destinations.columns = ['Helper Name', 'Unique Destinations']

    # Merge all data
    helper_assignments = pd.merge(helper_counts, helper_drivers, on='Helper Name')
    helper_assignments = pd.merge(helper_assignments, helper_trucks, on='Helper Name')
    helper_assignments = pd.merge(helper_assignments, helper_destinations, on='Helper Name')

    # Calculate driver consistency (lower number means helper works with fewer drivers)
    helper_assignments = helper_assignments.assign(
        Driver_Consistency=helper_assignments['Unique Drivers'] / helper_assignments['Trip Count']
    )

    # Sort by trip count
    helper_assignments = helper_assignments.sort_values('Trip Count', ascending=False)

    return helper_assignments


def get_loaded_quantity_analysis(df):
    """
    Process data for loaded quantity analysis.

    Args:
        df (pd.DataFrame): Processed DataFrame

    Returns:
        tuple: (quantity_by_destination, quantity_by_truck, quantity_over_time) DataFrames with loaded quantity analysis
    """
    # Ensure we have the Loaded Quantity column
    if 'Loaded Quantity' not in df.columns:
        df['Loaded Quantity'] = 0

    # Quantity by destination
    quantity_by_destination = df.groupby('Destination')['Loaded Quantity'].agg(['sum', 'mean', 'count']).reset_index()
    quantity_by_destination.columns = ['Destination', 'Total Quantity', 'Average Quantity', 'Trip Count']
    quantity_by_destination = quantity_by_destination.sort_values('Total Quantity', ascending=False)

    # Quantity by truck
    quantity_by_truck = df.groupby('Truck No')['Loaded Quantity'].agg(['sum', 'mean', 'count']).reset_index()
    quantity_by_truck.columns = ['Truck No', 'Total Quantity', 'Average Quantity', 'Trip Count']
    quantity_by_truck = quantity_by_truck.sort_values('Total Quantity', ascending=False)

    # Quantity over time
    df_copy = df.copy()
    df_copy['Loading Date'] = pd.to_datetime(df_copy['Loading Date']).dt.date
    quantity_over_time = df_copy.groupby('Loading Date')['Loaded Quantity'].sum().reset_index()
    quantity_over_time = quantity_over_time.sort_values('Loading Date')

    return quantity_by_destination, quantity_by_truck, quantity_over_time


def get_top_routes(df):
    """
    Process data to identify top routes (origin-destination pairs).

    Args:
        df (pd.DataFrame): Processed DataFrame

    Returns:
        pd.DataFrame: DataFrame with top routes
    """
    # Group by destination and count
    route_counts = df['Destination'].value_counts().reset_index()
    route_counts.columns = ['Destination', 'Trip Count']

    # Add loaded quantity information if available
    if 'Loaded Quantity' in df.columns:
        # Calculate total quantity by destination
        quantity_by_dest = df.groupby('Destination')['Loaded Quantity'].sum().reset_index()
        quantity_by_dest.columns = ['Destination', 'Total Quantity']

        # Merge with route counts
        route_counts = pd.merge(route_counts, quantity_by_dest, on='Destination', how='left')

        # Fill NaN values with 0
        route_counts['Total Quantity'] = route_counts['Total Quantity'].fillna(0)

        # Calculate average quantity per trip
        route_counts['Avg Quantity per Trip'] = route_counts['Total Quantity'] / route_counts['Trip Count']
    else:
        # Add placeholder columns if loaded quantity is not available
        route_counts['Total Quantity'] = 0
        route_counts['Avg Quantity per Trip'] = 0

    # Get average trips per day for each destination
    df_copy = df.copy()
    df_copy['Loading Date'] = pd.to_datetime(df_copy['Loading Date']).dt.date

    # Count unique dates
    unique_dates = df_copy['Loading Date'].nunique()

    # Calculate trips per day
    if unique_dates > 0:
        route_counts = route_counts.assign(
            Trips_per_Day=route_counts['Trip Count'] / unique_dates
        )
    else:
        route_counts = route_counts.assign(Trips_per_Day=0)

    # Get most common truck for each destination
    destination_trucks = df.groupby('Destination')['Truck No'].agg(
        lambda x: x.value_counts().index[0] if len(x) > 0 else 'None'
    ).reset_index()
    destination_trucks.columns = ['Destination', 'Most Common Truck']

    # Get most common driver for each destination
    destination_drivers = df.groupby('Destination')['Driver Name'].agg(
        lambda x: x.value_counts().index[0] if len(x) > 0 else 'None'
    ).reset_index()
    destination_drivers.columns = ['Destination', 'Most Common Driver']

    # Merge all data
    top_routes = pd.merge(route_counts, destination_trucks, on='Destination')
    top_routes = pd.merge(top_routes, destination_drivers, on='Destination')

    # Sort by trip count
    top_routes = top_routes.sort_values('Trip Count', ascending=False)

    return top_routes


# For testing
if __name__ == "__main__":
    # Sample data for testing
    sample_data = {
        'Loading Date': pd.date_range(start='2023-01-01', periods=10),
        'Truck No': ['T001', 'T002', 'T003', 'T001', 'T002', 'T004', 'T003', 'T001', 'T005', 'T002'],
        'Driver Name': ['John', 'Mike', 'Sarah', 'John', 'Mike', 'Alex', 'Sarah', 'John', 'Lisa', 'Mike'],
        'Helper Name': ['Tom', 'Jerry', 'Bob', 'Tom', 'Jerry', 'Sam', 'Bob', 'Tom', 'Tim', 'Jerry'],
        'Destination': ['NYC', 'LA', 'CHI', 'NYC', 'LA', 'MIA', 'CHI', 'NYC', 'BOS', 'LA']
    }

    df = pd.DataFrame(sample_data)

    # Test functions
    print("Summary Stats:")
    print(get_summary_stats(df))

    print("\nDestination Data:")
    print(get_destination_data(df))

    print("\nTruck-Driver Data:")
    print(get_truck_driver_data(df))

    print("\nDate-Based Data:")
    print(get_date_based_data(df))

    print("\nTruck Assignments:")
    print(get_truck_assignments(df))

    print("\nDriver Assignments:")
    print(get_driver_assignments(df))

    print("\nHelper Assignments:")
    print(get_helper_assignments(df))

    print("\nTop Routes:")
    print(get_top_routes(df))
