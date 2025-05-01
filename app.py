"""
Aurum Visualization Dashboard

A comprehensive Streamlit dashboard for visualizing and analyzing transportation data from Excel.
Features include data loading from multiple sources, interactive visualizations, and export capabilities.

Data is read from these specific ranges:
- Loading Date (A2:A1000)
- Truck No. (B2:B1000)
- Acquisition Type (C2:C1000)
- Loaded Quantity (D2:D1000)
- Destination (E2:E1000)
- Driver Name (F2:F1000)
- Helper Name (G2:G1000)

Author: Augment Code
Version: 2.0
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import streamlit.components.v1 as components

# Import custom modules
import data_processor as dp
import visualizations as viz

# Set page configuration
st.set_page_config(
    page_title="Aurum Visualization",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for enhanced UI
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1rem;
        border-bottom: 2px solid #1E88E5;
        font-weight: 600;
    }

    /* Section header styling */
    .sub-header {
        font-size: 1.8rem;
        color: #333;
        padding: 0.5rem 0;
        margin: 2rem 0 1rem 0;
        border-bottom: 1px solid #ddd;
        font-weight: 500;
    }

    /* Card styling for welcome message */
    .card {
        padding: 1.8rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        border-left: 4px solid #1E88E5;
    }

    /* Make buttons full width and improve appearance */
    .stButton>button {
        width: 100%;
        font-weight: 500;
        border-radius: 4px;
        background-color: #1E88E5;
        color: white;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #1565C0;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Improve sidebar appearance */
    .css-1d391kg {
        padding-top: 2rem;
    }

    /* Improve metric styling */
    .css-1xarl3l {
        font-size: 1.1rem;
        font-weight: 500;
    }

    /* Info text styling */
    .info-text {
        font-size: 1rem;
        color: #555;
        line-height: 1.5;
    }

    /* Improve table appearance */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
        border: none;
    }

    .dataframe th {
        background-color: #f2f2f2;
        padding: 8px;
        text-align: left;
        border-bottom: 2px solid #ddd;
    }

    .dataframe td {
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }

    /* Improve expander styling */
    .streamlit-expanderHeader {
        font-weight: 500;
        color: #333;
    }

    /* Improve tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1E88E5;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False
if 'date_filter' not in st.session_state:
    st.session_state.date_filter = None
if 'scroll_to' not in st.session_state:
    st.session_state.scroll_to = None


def main():
    """Main function to run the Streamlit app"""

    # Header
    st.markdown('<div class="main-header">Aurum Visualization Dashboard</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/gold-medal--v1.png", width=80)
        st.markdown("## Upload Data")

        # File uploader in sidebar
        uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"], key="sidebar_uploader")

        if uploaded_file is not None:
            # Process the uploaded file
            try:
                # Save the uploaded file to a temporary location
                temp_file = "temp_excel_file.xlsx"
                try:
                    with open(temp_file, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Read the data
                    df = dp.read_excel_data(temp_file)

                    # Clean up the temporary file
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except Exception as e:
                    st.error(f"Error handling file: {e}")
                    return

                if df is not None and not df.empty:
                    st.session_state.data = df
                    st.session_state.file_uploaded = True
                    st.success("Data loaded successfully!")

                    # Show data info
                    st.markdown("### Data Summary")
                    st.write(f"Total records: {len(df)}")
                    st.write(f"Date range: {df['Loading Date'].min().strftime('%Y-%m-%d')} to {df['Loading Date'].max().strftime('%Y-%m-%d')}")

                    # Date filter
                    st.markdown("### Filter Data")
                    date_range = st.date_input(
                        "Select date range",
                        value=(df['Loading Date'].min().date(), df['Loading Date'].max().date()),
                        min_value=df['Loading Date'].min().date(),
                        max_value=df['Loading Date'].max().date()
                    )

                    if len(date_range) == 2:
                        start_date, end_date = date_range
                        st.session_state.date_filter = (start_date, end_date)
                else:
                    st.error("Error: Could not read data from the Excel file. Please check the format.")
            except Exception as e:
                st.error(f"Error processing file: {e}")

        # Enhanced data loading interface
        st.markdown("### 📂 Data Source Selection")

        # Create tabs for different data loading methods
        data_tabs = st.tabs(["📊 Excel Files", "📤 Upload File"])

        with data_tabs[0]:
            # Check for available Excel files in the directory
            excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and os.path.isfile(f)]

            if excel_files:
                # Group files by type if possible
                retail_files = [f for f in excel_files if "retail" in f.lower()]
                nepas_files = [f for f in excel_files if "nepas" in f.lower()]
                alx_files = [f for f in excel_files if "alx" in f.lower()]
                other_files = [f for f in excel_files if f not in retail_files + nepas_files + alx_files]

                # Create a more organized selection interface
                file_category = st.radio(
                    "Select file category:",
                    options=["All Files"] +
                            (["Retail Files"] if retail_files else []) +
                            (["NEPAS Files"] if nepas_files else []) +
                            (["ALX Files"] if alx_files else []) +
                            (["Other Files"] if other_files else []),
                    horizontal=True
                )

                # Filter files based on selected category
                if file_category == "Retail Files":
                    display_files = retail_files
                elif file_category == "NEPAS Files":
                    display_files = nepas_files
                elif file_category == "ALX Files":
                    display_files = alx_files
                elif file_category == "Other Files":
                    display_files = other_files
                else:
                    display_files = excel_files

                # Add a dropdown to select which file to load
                selected_file = st.selectbox(
                    "Select Excel file:",
                    options=display_files,
                    index=0,
                    format_func=lambda x: f"{x} ({os.path.getsize(x) // 1024} KB)"
                )

                # Add file info
                if selected_file:
                    file_stats = os.stat(selected_file)
                    st.info(f"""
                    **File Information:**
                    - Size: {file_stats.st_size // 1024} KB
                    - Last Modified: {datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
                    """)

                # Load button with improved styling
                if st.button(f"📥 Load {selected_file}", key="load_selected", use_container_width=True):
                    try:
                        # Try to load the selected file
                        if os.path.exists(selected_file):
                            # Show loading spinner
                            with st.spinner(f"Loading data from {selected_file}..."):
                                # Read the data using our data processor
                                df = dp.read_excel_data(selected_file)

                                if df is not None and not df.empty:
                                    st.session_state.data = df
                                    st.session_state.file_uploaded = True
                                    st.success(f"✅ {selected_file} loaded successfully! ({len(df)} records)")
                                else:
                                    st.error(f"❌ Could not read data from {selected_file}. Please check the file format.")
                        else:
                            st.error(f"❌ {selected_file} not found in the current directory.")
                    except Exception as e:
                        st.error(f"❌ Error loading data: {e}")
            else:
                st.warning("📝 No Excel files found in the current directory.")
                st.info("Please upload a file using the 'Upload File' tab.")

        with data_tabs[1]:
            # File uploader in tab
            uploaded_file_tab = st.file_uploader("Upload Excel file", type=["xlsx", "xls"], key="tab_uploader")

            if uploaded_file_tab is not None:
                try:
                    # Show file info
                    st.info(f"""
                    **File Information:**
                    - Name: {uploaded_file_tab.name}
                    - Size: {uploaded_file_tab.size // 1024} KB
                    - Type: {uploaded_file_tab.type}
                    """)

                    # Save button
                    if st.button("📥 Load Uploaded File", key="load_uploaded", use_container_width=True):
                        with st.spinner("Processing uploaded file..."):
                            # Save the uploaded file temporarily
                            temp_file_path = os.path.join(".", uploaded_file_tab.name)
                            with open(temp_file_path, "wb") as f:
                                f.write(uploaded_file_tab.getbuffer())

                            # Read the data using our data processor
                            df = dp.read_excel_data(temp_file_path)

                            if df is not None and not df.empty:
                                st.session_state.data = df
                                st.session_state.file_uploaded = True
                                st.success(f"✅ {uploaded_file_tab.name} loaded successfully! ({len(df)} records)")
                            else:
                                st.error(f"❌ Could not read data from {uploaded_file_tab.name}. Please check the file format.")
                except Exception as e:
                    st.error(f"❌ Error processing uploaded file: {e}")
            else:
                st.info("📤 Drag and drop an Excel file here or click to browse")

        # Date filter
        st.markdown("### Filter Data")
        # Only show date filter if data is loaded
        if st.session_state.file_uploaded and st.session_state.data is not None:
            temp_df = st.session_state.data
            try:
                date_range = st.date_input(
                    "Select date range",
                    value=(temp_df['Loading Date'].min().date(), temp_df['Loading Date'].max().date()),
                    min_value=temp_df['Loading Date'].min().date(),
                    max_value=temp_df['Loading Date'].max().date()
                )

                if len(date_range) == 2:
                    start_date, end_date = date_range
                    st.session_state.date_filter = (start_date, end_date)
            except Exception as e:
                st.warning(f"Could not set date filter: {e}")
        else:
            st.info("Load data first to enable date filtering.")

        # Enhanced Navigation
        st.markdown("---")
        st.markdown("### 🧭 Dashboard Navigation")

        # Group navigation buttons by category
        st.markdown("#### Overview")
        if st.button("📊 Summary Statistics", key="nav_summary"):
            st.session_state.scroll_to = "summary_stats"

        st.markdown("#### Destination Analysis")
        if st.button("🌎 Top Destinations", key="nav_destinations"):
            st.session_state.scroll_to = "top_destinations"

        st.markdown("#### Cargo Analysis")
        if st.button("📦 Loaded Quantity", key="nav_quantity"):
            st.session_state.scroll_to = "loaded_quantity"

        st.markdown("#### Fleet Analysis")
        if st.button("🏷️ Acquisition Types", key="nav_acquisition"):
            st.session_state.scroll_to = "acquisition_analysis"

        if st.button("🚚 Truck Assignments", key="nav_trucks"):
            st.session_state.scroll_to = "truck_assignments"

        st.markdown("#### Personnel Analysis")
        if st.button("👨‍✈️ Driver Assignments", key="nav_drivers"):
            st.session_state.scroll_to = "driver_assignments"

        if st.button("👨‍🔧 Helper Assignments", key="nav_helpers"):
            st.session_state.scroll_to = "helper_assignments"

        # Enhanced About section
        st.markdown("---")
        st.markdown("### ℹ️ About Aurum Visualization")

        with st.expander("About This Dashboard", expanded=False):
            st.markdown("""
            ### Aurum Visualization Dashboard v2.0

            A comprehensive analytics tool designed for transportation and logistics data visualization.

            #### Data Requirements

            This dashboard reads data from Excel files with the following structure:

            | Column | Range | Description |
            |--------|-------|-------------|
            | Loading Date | A2:A1000 | Date of loading |
            | Truck No. | B2:B1000 | Truck identifier |
            | Acquisition Type | C2:C1000 | Own or Lease |
            | Loaded Quantity | D2:D1000 | Numeric quantity values |
            | Destination | E2:E1000 | Delivery location |
            | Driver Name | F2:F1000 | Name of driver |
            | Helper Name | G2:G1000 | Name of helper |

            #### Analysis Capabilities

            The dashboard provides detailed analysis across multiple dimensions:

            - **Operational Metrics**: Track shipment volumes, destinations, and trends over time
            - **Fleet Management**: Analyze truck utilization, acquisition types, and assignment patterns
            - **Personnel Management**: Evaluate driver and helper performance and relationships
            - **Cargo Analysis**: Examine loaded quantities by truck, destination, and time period

            #### Technical Information

            Built with:
            - Streamlit for the web interface
            - Plotly for interactive visualizations
            - Pandas for data processing

            For support or feature requests, please contact the development team.
            """)

        with st.expander("Tips & Tricks", expanded=False):
            st.markdown("""
            ### Getting the Most from Aurum Visualization

            #### Data Loading Tips
            - Use consistent data formats in your Excel files
            - Ensure dates are properly formatted
            - Fill in acquisition types as either "Own" or "Lease"

            #### Navigation Tips
            - Use the sidebar navigation to jump between sections
            - Filter data by date range to focus on specific time periods
            - Export charts as JPG files for reports and presentations

            #### Analysis Tips
            - Look for patterns in the truck assignments chart
            - Compare driver performance metrics
            - Analyze destination patterns over time
            - Track loaded quantities to identify efficiency opportunities
            """)

        with st.expander("Version History", expanded=False):
            st.markdown("""
            ### Version History

            #### v2.0 (Current)
            - Added support for Loaded Quantity analysis
            - Added Acquisition Type analysis
            - Improved UI and navigation
            - Enhanced data loading capabilities
            - Added multi-file support

            #### v1.0
            - Initial release
            - Basic transportation data visualization
            - Support for Excel data import
            """)


    # Main content
    if st.session_state.file_uploaded and st.session_state.data is not None:
        df = st.session_state.data

        # Add JavaScript for scrolling to anchors
        if st.session_state.scroll_to:
            section = st.session_state.scroll_to
            js = f"""
            <script>
                function scroll_to(id) {{
                    var element = document.getElementById(id);
                    if (element) {{
                        element.scrollIntoView();
                    }}
                }}
                scroll_to("{section}");
            </script>
            """
            components.html(js, height=0)
            # Reset scroll_to after use
            st.session_state.scroll_to = None

        # Apply date filter if set
        if st.session_state.date_filter is not None:
            start_date, end_date = st.session_state.date_filter
            df = df[(df['Loading Date'].dt.date >= start_date) &
                   (df['Loading Date'].dt.date <= end_date)]

        # Calculate statistics and prepare data for visualization
        stats = dp.get_summary_stats(df)
        destination_data = dp.get_destination_data(df)
        truck_driver_data = dp.get_truck_driver_data(df)
        date_data = dp.get_date_based_data(df)
        helper_data = dp.get_helper_analysis(df)
        truck_destination_data = dp.get_truck_destination_data(df)

        # New data analyses
        truck_assignments = dp.get_truck_assignments(df)
        driver_assignments = dp.get_driver_assignments(df)
        helper_assignments = dp.get_helper_assignments(df)
        top_routes = dp.get_top_routes(df)
        acquisition_counts, acquisition_metrics = dp.get_acquisition_analysis(df)

        # Loaded quantity analysis
        quantity_by_destination, quantity_by_truck, quantity_over_time = dp.get_loaded_quantity_analysis(df)

        # Create dashboard layout
        # Row 1: Enhanced Summary Statistics
        st.markdown('<div id="summary_stats" class="sub-header">📊 Summary Statistics</div>', unsafe_allow_html=True)

        # Create tabs for different categories of statistics
        stat_tabs = st.tabs(["📈 Overview", "🚚 Fleet", "👨‍✈️ Personnel", "📦 Cargo"])

        with stat_tabs[0]:
            # Overview statistics
            st.markdown("### Key Metrics")

            # Display summary statistics in a grid with icons and better formatting
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📝 Total Records", f"{stats['Total Records']:,}")
                st.metric("📅 Date Range", stats['Date Range'])
            with col2:
                st.metric("🌎 Unique Destinations", stats['Unique Destinations'])
                # Calculate average trips per destination
                avg_trips_per_dest = stats['Total Records'] / stats['Unique Destinations'] if stats['Unique Destinations'] > 0 else 0
                st.metric("🔄 Avg Trips per Destination", f"{avg_trips_per_dest:.1f}")
            with col3:
                # Calculate total days in date range
                try:
                    start_date, end_date = stats['Date Range'].split(" to ")
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")
                    total_days = (end_date - start_date).days + 1
                    st.metric("📆 Total Days", total_days)
                    # Calculate average trips per day
                    avg_trips_per_day = stats['Total Records'] / total_days if total_days > 0 else 0
                    st.metric("📊 Avg Trips per Day", f"{avg_trips_per_day:.1f}")
                except:
                    st.metric("📆 Total Days", "N/A")
                    st.metric("📊 Avg Trips per Day", "N/A")

        with stat_tabs[1]:
            # Fleet statistics
            st.markdown("### Fleet Metrics")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("🚚 Total Trucks", stats['Unique Trucks'])
                # Calculate average trips per truck
                avg_trips_per_truck = stats['Total Records'] / stats['Unique Trucks'] if stats['Unique Trucks'] > 0 else 0
                st.metric("🔄 Avg Trips per Truck", f"{avg_trips_per_truck:.1f}")
            with col2:
                # Get acquisition type counts if available
                if 'Acquisition Type' in df.columns:
                    own_count = len(df[df['Acquisition Type'] == 'Own'])
                    lease_count = len(df[df['Acquisition Type'] == 'Lease'])
                    own_pct = own_count / len(df) * 100 if len(df) > 0 else 0
                    lease_pct = lease_count / len(df) * 100 if len(df) > 0 else 0
                    st.metric("🏠 Own Trucks (%)", f"{own_pct:.1f}%")
                    st.metric("📋 Leased Trucks (%)", f"{lease_pct:.1f}%")
                else:
                    st.info("Acquisition type data not available")

        with stat_tabs[2]:
            # Personnel statistics
            st.markdown("### Personnel Metrics")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("👨‍✈️ Total Drivers", stats['Unique Drivers'])
                # Calculate average trips per driver
                avg_trips_per_driver = stats['Total Records'] / stats['Unique Drivers'] if stats['Unique Drivers'] > 0 else 0
                st.metric("🔄 Avg Trips per Driver", f"{avg_trips_per_driver:.1f}")
            with col2:
                st.metric("👨‍🔧 Total Helpers", stats['Unique Helpers'])
                # Calculate average trips per helper
                avg_trips_per_helper = stats['Total Records'] / stats['Unique Helpers'] if stats['Unique Helpers'] > 0 else 0
                st.metric("🔄 Avg Trips per Helper", f"{avg_trips_per_helper:.1f}")

            # Calculate driver-truck ratio
            driver_truck_ratio = stats['Unique Drivers'] / stats['Unique Trucks'] if stats['Unique Trucks'] > 0 else 0
            st.metric("📊 Driver-to-Truck Ratio", f"{driver_truck_ratio:.2f}")

        with stat_tabs[3]:
            # Cargo statistics
            st.markdown("### Cargo Metrics")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("📦 Total Loaded Quantity", f"{stats['Total Loaded Quantity']:,}")
                st.metric("📊 Avg Load per Trip", f"{stats['Average Load per Trip']:.2f}")
            with col2:
                # Calculate average load per truck
                avg_load_per_truck = stats['Total Loaded Quantity'] / stats['Unique Trucks'] if stats['Unique Trucks'] > 0 else 0
                st.metric("🚚 Avg Load per Truck", f"{avg_load_per_truck:.2f}")

                # Calculate average load per destination
                avg_load_per_dest = stats['Total Loaded Quantity'] / stats['Unique Destinations'] if stats['Unique Destinations'] > 0 else 0
                st.metric("🌎 Avg Load per Destination", f"{avg_load_per_dest:.2f}")

            # If we have date information, calculate daily metrics
            try:
                start_date, end_date = stats['Date Range'].split(" to ")
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                total_days = (end_date - start_date).days + 1

                # Calculate average quantity per day
                avg_quantity_per_day = stats['Total Loaded Quantity'] / total_days if total_days > 0 else 0
                st.metric("📅 Avg Quantity per Day", f"{avg_quantity_per_day:.2f}")
            except:
                st.info("Date range information not available for daily metrics")

        # Row 2: Destination and Date charts
        st.markdown('<div class="sub-header">Destination and Time Analysis</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            # Create the destination chart
            dest_chart = viz.create_destination_chart(destination_data)
            st.plotly_chart(dest_chart, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button("Export Destination Chart as JPG", key="export_dest_jpg"):
                    export_path = viz.export_figure_as_image(dest_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(dest_chart, format='jpg', link_text="Download Destination Chart"), unsafe_allow_html=True)

        with col2:
            # Create the date chart
            date_chart = viz.create_date_chart(date_data)
            st.plotly_chart(date_chart, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button("Export Date Chart as JPG", key="export_date_jpg"):
                    export_path = viz.export_figure_as_image(date_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(date_chart, format='jpg', link_text="Download Date Chart"), unsafe_allow_html=True)

        # Row 3: Truck-Driver and Helper charts
        st.markdown('<div class="sub-header">Personnel Analysis</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            # Create the truck-driver chart
            truck_driver_chart = viz.create_truck_driver_chart(truck_driver_data)
            st.plotly_chart(truck_driver_chart, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button("Export Truck-Driver Chart as JPG", key="export_truck_driver_jpg"):
                    export_path = viz.export_figure_as_image(truck_driver_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(truck_driver_chart, format='jpg', link_text="Download Truck-Driver Chart"), unsafe_allow_html=True)

        with col2:
            # Create the helper chart
            helper_chart = viz.create_helper_chart(helper_data)
            st.plotly_chart(helper_chart, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button("Export Helper Chart as JPG", key="export_helper_jpg"):
                    export_path = viz.export_figure_as_image(helper_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(helper_chart, format='jpg', link_text="Download Helper Chart"), unsafe_allow_html=True)

        # Row 4: Advanced visualizations
        st.markdown('<div class="sub-header">Advanced Analysis</div>', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Truck-Destination Analysis", "Driver-Helper Network"])

        with tab1:
            # Create the truck-destination chart
            truck_dest_chart = viz.create_truck_destination_chart(truck_destination_data)
            st.plotly_chart(truck_dest_chart, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button("Export Truck-Destination Chart as JPG", key="export_truck_dest_jpg"):
                    export_path = viz.export_figure_as_image(truck_dest_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(truck_dest_chart, format='jpg', link_text="Download Truck-Destination Chart"), unsafe_allow_html=True)

        with tab2:
            # Create the driver-helper network chart
            network_chart = viz.create_driver_helper_network(df)
            st.plotly_chart(network_chart, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button("Export Network Chart as JPG", key="export_network_jpg"):
                    export_path = viz.export_figure_as_image(network_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(network_chart, format='jpg', link_text="Download Network Chart"), unsafe_allow_html=True)

        # Row 5: Top Destinations Analysis
        st.markdown('<div id="top_destinations" class="sub-header">Top Destinations Analysis</div>', unsafe_allow_html=True)

        # Create the top routes charts
        top_routes_chart, top_routes_table = viz.create_top_routes_chart(top_routes)

        # Display the charts
        st.plotly_chart(top_routes_chart, use_container_width=True)
        st.plotly_chart(top_routes_table, use_container_width=True)

        # Add export options
        export_col1, export_col2 = st.columns(2)
        with export_col1:
            if st.button("Export Top Destinations Chart as JPG", key="export_top_routes_jpg"):
                export_path = viz.export_figure_as_image(top_routes_chart, format='jpg')
                if export_path:
                    st.success(f"Chart exported to {export_path}")
        with export_col2:
            st.markdown(viz.get_image_download_link(top_routes_chart, format='jpg', link_text="Download Top Destinations Chart"), unsafe_allow_html=True)

        # Row 6: Loaded Quantity Analysis
        st.markdown('<div id="loaded_quantity" class="sub-header">Loaded Quantity Analysis</div>', unsafe_allow_html=True)

        # Create the loaded quantity charts
        dest_quantity_chart, truck_quantity_chart, time_quantity_chart = viz.create_loaded_quantity_charts(
            quantity_by_destination, quantity_by_truck, quantity_over_time
        )

        # Display the destination quantity chart
        st.plotly_chart(dest_quantity_chart, use_container_width=True)

        # Add export options
        export_col1, export_col2 = st.columns(2)
        with export_col1:
            if st.button("Export Destination Quantity Chart as JPG", key="export_dest_quantity_jpg"):
                export_path = viz.export_figure_as_image(dest_quantity_chart, format='jpg')
                if export_path:
                    st.success(f"Chart exported to {export_path}")
        with export_col2:
            st.markdown(viz.get_image_download_link(dest_quantity_chart, format='jpg', link_text="Download Destination Quantity Chart"), unsafe_allow_html=True)

        # Display the truck quantity and time quantity charts side by side
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(truck_quantity_chart, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button("Export Truck Quantity Chart as JPG", key="export_truck_quantity_jpg"):
                    export_path = viz.export_figure_as_image(truck_quantity_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(truck_quantity_chart, format='jpg', link_text="Download Truck Quantity Chart"), unsafe_allow_html=True)

        with col2:
            st.plotly_chart(time_quantity_chart, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button("Export Time Quantity Chart as JPG", key="export_time_quantity_jpg"):
                    export_path = viz.export_figure_as_image(time_quantity_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(time_quantity_chart, format='jpg', link_text="Download Time Quantity Chart"), unsafe_allow_html=True)

        # Row 7: Acquisition Type Analysis
        st.markdown('<div id="acquisition_analysis" class="sub-header">Acquisition Type Analysis</div>', unsafe_allow_html=True)

        # Create the acquisition type charts
        acquisition_pie, acquisition_bar = viz.create_acquisition_charts(acquisition_counts, acquisition_metrics)

        # Display the charts
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(acquisition_pie, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button("Export Acquisition Pie Chart as JPG", key="export_acquisition_pie_jpg"):
                    export_path = viz.export_figure_as_image(acquisition_pie, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(acquisition_pie, format='jpg', link_text="Download Acquisition Pie Chart"), unsafe_allow_html=True)

        with col2:
            st.plotly_chart(acquisition_bar, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button("Export Acquisition Bar Chart as JPG", key="export_acquisition_bar_jpg"):
                    export_path = viz.export_figure_as_image(acquisition_bar, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(acquisition_bar, format='jpg', link_text="Download Acquisition Bar Chart"), unsafe_allow_html=True)

        # Row 7: Truck Assignments Analysis
        st.markdown('<div id="truck_assignments" class="sub-header">Truck Assignments Analysis</div>', unsafe_allow_html=True)

        # Create the truck assignments chart
        truck_assignments_chart = viz.create_truck_assignments_chart(truck_assignments)

        # Display the chart
        st.plotly_chart(truck_assignments_chart, use_container_width=True)

        # Add export options
        export_col1, export_col2 = st.columns(2)
        with export_col1:
            if st.button("Export Truck Assignments Chart as JPG", key="export_truck_assignments_jpg"):
                export_path = viz.export_figure_as_image(truck_assignments_chart, format='jpg')
                if export_path:
                    st.success(f"Chart exported to {export_path}")
        with export_col2:
            st.markdown(viz.get_image_download_link(truck_assignments_chart, format='jpg', link_text="Download Truck Assignments Chart"), unsafe_allow_html=True)

        # Row 7: Driver Assignments Analysis
        st.markdown('<div id="driver_assignments" class="sub-header">Driver Assignments Analysis</div>', unsafe_allow_html=True)

        # Create the driver assignments charts
        driver_assignments_chart, driver_assignments_table = viz.create_driver_assignments_chart(driver_assignments)

        # Display the charts
        st.plotly_chart(driver_assignments_chart, use_container_width=True)
        st.plotly_chart(driver_assignments_table, use_container_width=True)

        # Add export options
        export_col1, export_col2 = st.columns(2)
        with export_col1:
            if st.button("Export Driver Assignments Chart as JPG", key="export_driver_assignments_jpg"):
                export_path = viz.export_figure_as_image(driver_assignments_chart, format='jpg')
                if export_path:
                    st.success(f"Chart exported to {export_path}")
        with export_col2:
            st.markdown(viz.get_image_download_link(driver_assignments_chart, format='jpg', link_text="Download Driver Assignments Chart"), unsafe_allow_html=True)

        # Row 8: Helper Assignments Analysis
        st.markdown('<div id="helper_assignments" class="sub-header">Helper Assignments Analysis</div>', unsafe_allow_html=True)

        # Create the helper assignments charts
        helper_assignments_chart, helper_assignments_table = viz.create_helper_assignments_chart(helper_assignments)

        # Display the charts
        st.plotly_chart(helper_assignments_chart, use_container_width=True)
        st.plotly_chart(helper_assignments_table, use_container_width=True)

        # Add export options
        export_col1, export_col2 = st.columns(2)
        with export_col1:
            if st.button("Export Helper Assignments Chart as JPG", key="export_helper_assignments_jpg"):
                export_path = viz.export_figure_as_image(helper_assignments_chart, format='jpg')
                if export_path:
                    st.success(f"Chart exported to {export_path}")
        with export_col2:
            st.markdown(viz.get_image_download_link(helper_assignments_chart, format='jpg', link_text="Download Helper Assignments Chart"), unsafe_allow_html=True)

        # Data explorer
        st.markdown('<div class="sub-header">Data Explorer</div>', unsafe_allow_html=True)

        with st.expander("View Raw Data"):
            st.dataframe(df)

            # Download option
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Data as CSV",
                data=csv,
                file_name=f"transportation_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

    else:
        # Show enhanced welcome message when no data is loaded
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        ## 🏆 Welcome to the Aurum Visualization Dashboard

        This powerful tool helps you visualize and analyze transportation data with interactive charts and detailed metrics.

        ### Getting Started:

        1. **Select an Excel file** from the dropdown menu and click "Load Selected Data"
        2. **Upload your own Excel file** using the sidebar or the Upload File tab

        ### Data Format Requirements:

        Your Excel file should contain data in these specific columns:

        | Column | Range | Description |
        |--------|-------|-------------|
        | Loading Date | A2:A1000 | Date of loading |
        | Truck No. | B2:B1000 | Truck identifier |
        | Acquisition Type | C2:C1000 | Own or Lease |
        | Loaded Quantity | D2:D1000 | Numeric quantity values |
        | Destination | E2:E1000 | Delivery location |
        | Driver Name | F2:F1000 | Name of driver |
        | Helper Name | G2:G1000 | Name of helper |

        ### Key Features:

        - **Interactive Visualizations**: Explore data through charts and graphs
        - **Detailed Analytics**: Get insights on truck utilization, driver performance, and more
        - **Export Capabilities**: Save charts as JPG files for reports and presentations
        - **Filtering Options**: Analyze data by date ranges and other parameters

        Click any of the navigation buttons in the sidebar to jump to specific sections after loading data.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        # Show sample visualization
        st.markdown('<div class="sub-header">Sample Visualization</div>', unsafe_allow_html=True)

        # Create sample data for preview
        sample_destinations = pd.DataFrame({
            'Destination': ['New York', 'Los Angeles', 'Chicago', 'Miami', 'Dallas'],
            'Count': [42, 38, 29, 25, 18]
        })

        # Show sample chart
        st.plotly_chart(viz.create_destination_chart(sample_destinations), use_container_width=True)

        st.info("👆 This is a sample visualization. Upload your data to see actual insights.")


if __name__ == "__main__":
    main()
