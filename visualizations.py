"""
Visualization Module for Transportation Data

This module creates visualizations from processed transportation data.
"""

# Core visualization libraries
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# System libraries
import os
import base64
from datetime import datetime

# Image export functionality
# Note: kaleido package must be installed for image export to work
# pip install kaleido
try:
    # Import is used indirectly through fig.write_image and fig.to_image
    import plotly.io as pio
    # Set renderer for better compatibility
    pio.renderers.default = "browser"
    HAS_KALEIDO = True
except ImportError:
    print("Warning: kaleido package not found. Image export functionality will be limited.")
    HAS_KALEIDO = False


def create_summary_card(stats):
    """
    Create a summary card with key statistics.

    Args:
        stats (dict): Dictionary of summary statistics

    Returns:
        go.Figure: Plotly figure object
    """
    # Create a table figure
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['Metric', 'Value'],
            fill_color='#2c3e50',
            align='left',
            font=dict(color='white', size=14)
        ),
        cells=dict(
            values=[
                list(stats.keys()),
                list(stats.values())
            ],
            fill_color='#f9f9f9',
            align='left',
            font=dict(color='#333', size=12)
        )
    )])

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=300
    )

    return fig


def create_destination_chart(destination_data):
    """
    Create a bar chart showing top destinations.

    Args:
        destination_data (pd.DataFrame): DataFrame with destination counts

    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.bar(
        destination_data,
        x='Destination',
        y='Count',
        title='Top Destinations',
        color='Count',
        color_continuous_scale='Viridis'
    )

    fig.update_layout(
        xaxis_title='Destination',
        yaxis_title='Number of Shipments',
        xaxis={'categoryorder':'total descending'},
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor="white", font_size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig


def create_truck_driver_chart(truck_driver_data):
    """
    Create a heatmap showing truck-driver relationships.

    Args:
        truck_driver_data (pd.DataFrame): DataFrame with truck-driver relationships

    Returns:
        go.Figure: Plotly figure object
    """
    # Create a pivot table for the heatmap
    pivot_data = truck_driver_data.pivot(
        index='Truck No',
        columns='Driver Name',
        values='Count'
    ).fillna(0)

    # Create the heatmap
    fig = px.imshow(
        pivot_data,
        labels=dict(x="Driver Name", y="Truck No", color="Count"),
        x=pivot_data.columns,
        y=pivot_data.index,
        color_continuous_scale='Viridis',
        title='Truck-Driver Relationship'
    )

    fig.update_layout(
        xaxis={'side': 'top'},
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor="white", font_size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig


def create_date_chart(date_data):
    """
    Create a line chart showing shipments by date.

    Args:
        date_data (pd.DataFrame): DataFrame with date-based counts

    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.line(
        date_data,
        x='Loading Date',
        y='Count',
        title='Shipments by Loading Date',
        markers=True
    )

    fig.update_layout(
        xaxis_title='Loading Date',
        yaxis_title='Number of Shipments',
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor="white", font_size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig


def create_acquisition_charts(acquisition_counts, acquisition_metrics):
    """
    Create charts for acquisition type analysis.

    Args:
        acquisition_counts (pd.DataFrame): DataFrame with acquisition type counts
        acquisition_metrics (pd.DataFrame): DataFrame with acquisition metrics

    Returns:
        tuple: (pie_fig, metrics_fig) Plotly figure objects
    """
    # Create a pie chart for acquisition types
    pie_fig = px.pie(
        acquisition_counts,
        names='Acquisition Type',
        values='Count',
        title='Truck Acquisition Types',
        color='Acquisition Type',
        color_discrete_map={
            'Own': '#3498db',
            'Lease': '#e74c3c',
            'Unknown': '#95a5a6'
        },
        hole=0.4
    )

    pie_fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hoverinfo='label+percent+value',
        marker=dict(line=dict(color='white', width=2))
    )

    pie_fig.update_layout(
        legend_title='Acquisition Type',
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor="white", font_size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    # Create a bar chart for acquisition metrics
    metrics_fig = px.bar(
        acquisition_metrics,
        x='Metric',
        y='Value',
        title='Acquisition Type Percentages',
        color='Metric',
        color_discrete_map={
            'Own Percentage': '#3498db',
            'Lease Percentage': '#e74c3c',
            'Unknown Percentage': '#95a5a6'
        },
        text_auto='.1f'
    )

    metrics_fig.update_traces(
        texttemplate='%{text}%',
        textposition='outside'
    )

    metrics_fig.update_layout(
        xaxis_title='',
        yaxis_title='Percentage (%)',
        yaxis=dict(range=[0, 100]),
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor="white", font_size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return pie_fig, metrics_fig


def create_helper_chart(helper_data):
    """
    Create a bar chart showing top helpers.

    Args:
        helper_data (pd.DataFrame): DataFrame with helper counts

    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.bar(
        helper_data,
        x='Helper Name',
        y='Count',
        title='Top Helpers',
        color='Count',
        color_continuous_scale='Viridis'
    )

    fig.update_layout(
        xaxis_title='Helper Name',
        yaxis_title='Number of Shipments',
        xaxis={'categoryorder':'total descending'},
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor="white", font_size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig


def create_truck_assignments_chart(truck_assignments):
    """
    Create a visualization for truck assignments.

    Args:
        truck_assignments (pd.DataFrame): DataFrame with truck assignment data

    Returns:
        go.Figure: Plotly figure object
    """
    # Create a parallel coordinates plot for truck assignments
    dimensions = [
        dict(range=[0, truck_assignments['Trip Count'].max() * 1.1],
             label='Trip Count', values=truck_assignments['Trip Count']),
        dict(range=[0, truck_assignments['Unique Destinations'].max() * 1.1],
             label='Unique Destinations', values=truck_assignments['Unique Destinations']),
        dict(range=[0, truck_assignments['Unique Drivers'].max() * 1.1],
             label='Unique Drivers', values=truck_assignments['Unique Drivers']),
        dict(range=[0, truck_assignments['Utilization'].max() * 1.1],
             label='Utilization', values=truck_assignments['Utilization'])
    ]

    # Add acquisition type as a dimension if available
    if 'Acquisition Type' in truck_assignments.columns:
        # Create a numeric mapping for acquisition types
        acquisition_map = {'Own': 0, 'Lease': 1, 'Unknown': 2}
        truck_assignments['Acquisition_Numeric'] = truck_assignments['Acquisition Type'].map(
            lambda x: acquisition_map.get(x, 2)
        )

        # Add the dimension
        dimensions.append(
            dict(range=[-0.5, 2.5],
                 label='Acquisition Type',
                 values=truck_assignments['Acquisition_Numeric'],
                 tickvals=[0, 1, 2],
                 ticktext=['Own', 'Lease', 'Unknown'])
        )

    fig = go.Figure(data=
        go.Parcoords(
            line=dict(color=truck_assignments['Trip Count'],
                     colorscale='Viridis',
                     showscale=True,
                     cmin=0,
                     cmax=truck_assignments['Trip Count'].max()),
            dimensions=dimensions,
            labelfont=dict(size=12),
            tickfont=dict(size=10)
        )
    )

    # Add a table below the parallel coordinates
    table_data = truck_assignments.head(10).copy()  # Top 10 trucks

    # Format the utilization column
    table_data['Utilization'] = table_data['Utilization'].round(2)

    fig.add_trace(go.Table(
        header=dict(
            values=list(table_data.columns),
            fill_color='#2c3e50',
            align='left',
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[table_data[col] for col in table_data.columns],
            fill_color='#f9f9f9',
            align='left',
            font=dict(color='#333', size=11)
        ),
        columnwidth=[2, 1, 1, 1, 1]
    ))

    fig.update_layout(
        title='Truck Assignments Analysis',
        height=800,
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig


def create_driver_assignments_chart(driver_assignments):
    """
    Create a visualization for driver assignments.

    Args:
        driver_assignments (pd.DataFrame): DataFrame with driver assignment data

    Returns:
        go.Figure: Plotly figure object
    """
    # Create a scatter plot matrix for driver assignments
    fig = px.scatter_matrix(
        driver_assignments,
        dimensions=['Trip Count', 'Unique Trucks', 'Unique Destinations', 'Unique Helpers'],
        color='Trip Count',
        color_continuous_scale='Viridis',
        title='Driver Assignments Analysis',
        labels={
            'Trip Count': 'Trip Count',
            'Unique Trucks': 'Unique Trucks',
            'Unique Destinations': 'Unique Destinations',
            'Unique Helpers': 'Unique Helpers'
        },
        hover_data=['Driver Name'] + (['Truck_Consistency'] if 'Truck_Consistency' in driver_assignments.columns else [])
    )

    # Add a table below the scatter matrix
    table_data = driver_assignments.head(10).copy()  # Top 10 drivers

    # Format the truck consistency column
    if 'Truck_Consistency' in table_data.columns:
        table_data['Truck_Consistency'] = table_data['Truck_Consistency'].round(2)

    # Create a separate figure for the table
    table_fig = go.Figure(go.Table(
        header=dict(
            values=list(table_data.columns),
            fill_color='#2c3e50',
            align='left',
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[table_data[col] for col in table_data.columns],
            fill_color='#f9f9f9',
            align='left',
            font=dict(color='#333', size=11)
        ),
        columnwidth=[2, 1, 1, 1, 1, 1]
    ))

    table_fig.update_layout(
        title='Top 10 Drivers by Trip Count',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # Update the scatter matrix layout
    fig.update_layout(
        height=600,
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig, table_fig


def create_helper_assignments_chart(helper_assignments):
    """
    Create a visualization for helper assignments.

    Args:
        helper_assignments (pd.DataFrame): DataFrame with helper assignment data

    Returns:
        go.Figure: Plotly figure object
    """
    # Create a sunburst chart for helper assignments
    fig = px.sunburst(
        helper_assignments,
        path=['Helper Name'],
        values='Trip Count',
        color='Unique Drivers',
        color_continuous_scale='Viridis',
        title='Helper Assignments Analysis',
        hover_data=['Unique Trucks', 'Unique Destinations'] +
                 (['Driver_Consistency'] if 'Driver_Consistency' in helper_assignments.columns else [])
    )

    # Add a table below the sunburst chart
    table_data = helper_assignments.head(10).copy()  # Top 10 helpers

    # Format the driver consistency column
    if 'Driver_Consistency' in table_data.columns:
        table_data['Driver_Consistency'] = table_data['Driver_Consistency'].round(2)

    # Create a separate figure for the table
    table_fig = go.Figure(go.Table(
        header=dict(
            values=list(table_data.columns),
            fill_color='#2c3e50',
            align='left',
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[table_data[col] for col in table_data.columns],
            fill_color='#f9f9f9',
            align='left',
            font=dict(color='#333', size=11)
        ),
        columnwidth=[2, 1, 1, 1, 1, 1]
    ))

    table_fig.update_layout(
        title='Top 10 Helpers by Trip Count',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # Update the sunburst layout
    fig.update_layout(
        height=600,
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig, table_fig


def create_loaded_quantity_charts(quantity_by_destination, quantity_by_truck, quantity_over_time):
    """
    Create charts for loaded quantity analysis.

    Args:
        quantity_by_destination (pd.DataFrame): DataFrame with quantity by destination
        quantity_by_truck (pd.DataFrame): DataFrame with quantity by truck
        quantity_over_time (pd.DataFrame): DataFrame with quantity over time

    Returns:
        tuple: (dest_fig, truck_fig, time_fig) Plotly figure objects
    """
    # Create a bar chart for quantity by destination
    dest_fig = px.bar(
        quantity_by_destination.head(10),  # Top 10 destinations by quantity
        x='Destination',
        y='Total Quantity',
        color='Average Quantity',
        color_continuous_scale='Viridis',
        title='Top Destinations by Loaded Quantity',
        hover_data=['Trip Count', 'Average Quantity']
    )

    dest_fig.update_layout(
        xaxis_title='Destination',
        yaxis_title='Total Loaded Quantity',
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor="white", font_size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    # Create a bar chart for quantity by truck
    truck_fig = px.bar(
        quantity_by_truck.head(10),  # Top 10 trucks by quantity
        x='Truck No',
        y='Total Quantity',
        color='Average Quantity',
        color_continuous_scale='Viridis',
        title='Top Trucks by Loaded Quantity',
        hover_data=['Trip Count', 'Average Quantity']
    )

    truck_fig.update_layout(
        xaxis_title='Truck Number',
        yaxis_title='Total Loaded Quantity',
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor="white", font_size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    # Create a line chart for quantity over time
    time_fig = px.line(
        quantity_over_time,
        x='Loading Date',
        y='Loaded Quantity',
        title='Loaded Quantity Over Time',
        markers=True
    )

    time_fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Total Loaded Quantity',
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor="white", font_size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return dest_fig, truck_fig, time_fig


def create_top_routes_chart(top_routes):
    """
    Create a visualization for top routes.

    Args:
        top_routes (pd.DataFrame): DataFrame with top routes data

    Returns:
        go.Figure: Plotly figure object
    """
    # Create a horizontal bar chart for top routes
    hover_data = ['Most Common Truck', 'Most Common Driver']

    # Add loaded quantity to hover data if available
    if 'Total Quantity' in top_routes.columns:
        hover_data.extend(['Total Quantity', 'Avg Quantity per Trip'])

    fig = px.bar(
        top_routes.head(15),  # Top 15 destinations
        y='Destination',
        x='Trip Count',
        color='Total Quantity' if 'Total Quantity' in top_routes.columns else
              ('Trips_per_Day' if 'Trips_per_Day' in top_routes.columns else 'Trip Count'),
        color_continuous_scale='Viridis',
        title='Top Destinations Analysis',
        orientation='h',
        hover_data=hover_data
    )

    # Add a table below the bar chart
    table_data = top_routes.head(10).copy()  # Top 10 destinations

    # Format the trips per day column
    if 'Trips_per_Day' in table_data.columns:
        table_data['Trips_per_Day'] = table_data['Trips_per_Day'].round(2)

    # Create a separate figure for the table
    table_fig = go.Figure(go.Table(
        header=dict(
            values=list(table_data.columns),
            fill_color='#2c3e50',
            align='left',
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[table_data[col] for col in table_data.columns],
            fill_color='#f9f9f9',
            align='left',
            font=dict(color='#333', size=11)
        ),
        columnwidth=[2, 1, 1, 2, 2]
    ))

    table_fig.update_layout(
        title='Top 10 Destinations by Trip Count',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # Update the bar chart layout
    fig.update_layout(
        xaxis_title='Number of Trips',
        yaxis_title='Destination',
        yaxis={'categoryorder':'total ascending'},
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor="white", font_size=12),
        height=600,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig, table_fig


def create_truck_destination_chart(truck_destination_data):
    """
    Create a sunburst chart showing truck-destination relationships.

    Args:
        truck_destination_data (pd.DataFrame): DataFrame with truck-destination relationships

    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.sunburst(
        truck_destination_data,
        path=['Truck No', 'Destination'],
        values='Count',
        title='Truck-Destination Relationships'
    )

    fig.update_layout(
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor="white", font_size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig


def create_driver_helper_network(df):
    """
    Create a network graph showing driver-helper relationships.

    Args:
        df (pd.DataFrame): Processed DataFrame

    Returns:
        go.Figure: Plotly figure object
    """
    # Create a dataframe of driver-helper pairs and their counts
    driver_helper = df.groupby(['Driver Name', 'Helper Name']).size().reset_index()
    driver_helper.columns = ['Driver', 'Helper', 'Count']

    # Filter to include only pairs that occur more than once
    driver_helper = driver_helper[driver_helper['Count'] > 1]

    # Create a list of nodes (drivers and helpers)
    drivers = list(driver_helper['Driver'].unique())
    helpers = list(driver_helper['Helper'].unique())

    # Create node dataframe
    nodes = pd.DataFrame({
        'name': drivers + helpers,
        'group': ['Driver'] * len(drivers) + ['Helper'] * len(helpers)
    })

    # Create edge dataframe
    edges = driver_helper.copy()

    # Create the network graph
    fig = go.Figure()

    # Add edges (links)
    for _, edge in edges.iterrows():
        # Convert values to strings to avoid numpy.int64 error
        driver = str(edge['Driver'])
        helper = str(edge['Helper'])
        count = int(edge['Count']) if isinstance(edge['Count'], (int, float, np.integer, np.floating)) else 1

        fig.add_trace(
            go.Scatter(
                x=[driver, helper],
                y=[0, 0],
                mode='lines',
                line=dict(width=count / 2, color='rgba(150, 150, 150, 0.5)'),
                hoverinfo='text',
                text=f"{driver} - {helper}: {count} trips",
                showlegend=False
            )
        )

    # Add nodes
    for _, node in nodes.iterrows():
        color = 'blue' if node['group'] == 'Driver' else 'red'
        # Convert node name to string to avoid numpy.int64 error
        node_name = str(node['name'])
        fig.add_trace(
            go.Scatter(
                x=[node_name],
                y=[0],
                mode='markers',
                marker=dict(size=10, color=color),
                name=node['group'],
                hoverinfo='text',
                text=node_name,
                showlegend=True
            )
        )

    fig.update_layout(
        title='Driver-Helper Relationships',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor="white", font_size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig


def export_figure_as_image(fig, filename=None, format='jpg', width=1200, height=800):
    """
    Export a Plotly figure as an image file.

    Args:
        fig (go.Figure): Plotly figure to export
        filename (str, optional): Output filename. If None, a default name is generated.
        format (str, optional): Image format ('jpg', 'png', 'svg', 'pdf'). Defaults to 'jpg'.
        width (int, optional): Image width in pixels. Defaults to 1200.
        height (int, optional): Image height in pixels. Defaults to 800.

    Returns:
        str: Path to the saved image file or None if export fails
    """
    # Validate parameters
    if fig is None:
        print("Error: No figure provided for export")
        return None

    # Validate and normalize format
    valid_formats = ['jpg', 'jpeg', 'png', 'svg', 'pdf', 'webp']
    format = format.lower()
    if format == 'jpeg':
        format = 'jpg'  # Normalize jpeg to jpg
    if format not in valid_formats:
        print(f"Warning: Unsupported format '{format}'. Using 'jpg' instead.")
        format = 'jpg'

    # Create exports directory if it doesn't exist
    export_dir = 'exports'
    try:
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
    except Exception as e:
        print(f"Error creating exports directory: {e}")
        export_dir = '.'  # Fallback to current directory

    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Get title from figure or use default
        try:
            title = fig.layout.title.text if hasattr(fig.layout, 'title') and fig.layout.title.text else 'chart'
            # Clean title for filename (remove special characters)
            title = ''.join(c if c.isalnum() else '_' for c in title)
            # Limit length to avoid overly long filenames
            title = title[:50]
        except Exception:
            title = 'chart'

        filename = f"{title}_{timestamp}.{format}"
    elif not filename.endswith(f'.{format}'):
        filename = f"{filename}.{format}"

    # Full path to the output file
    output_path = os.path.join(export_dir, filename)

    # Check if kaleido is available for image export
    if not HAS_KALEIDO:
        print("Warning: kaleido package is required for image export. Please install it with 'pip install kaleido'")
        return None

    try:
        # Export the figure
        fig.write_image(output_path, width=width, height=height, scale=2)
        print(f"Image saved to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error exporting image: {e}")
        # Try alternative method
        try:
            # For JPG/PNG, try using to_image method
            img_bytes = fig.to_image(format=format, width=width, height=height, scale=2)
            with open(output_path, 'wb') as f:
                f.write(img_bytes)
            print(f"Image saved to {output_path} using alternative method")
            return output_path
        except Exception as e2:
            print(f"Error with alternative export method: {e2}")
            # Create a simple fallback image with a message
            try:
                from PIL import Image, ImageDraw
                # Create a blank image
                img = Image.new('RGB', (width, height), color=(255, 255, 255))
                draw = ImageDraw.Draw(img)
                # Add error message
                draw.text((width//2-150, height//2),
                          f"Error exporting chart: {str(e)[:50]}...",
                          fill=(0, 0, 0))
                # Save the image
                img.save(output_path)
                print(f"Created fallback image at {output_path}")
                return output_path
            except Exception:
                return None


def get_image_download_link(fig, filename=None, format='jpg', width=1200, height=800, link_text="Download Image"):
    """
    Generate a download link for a Plotly figure as an image.

    Args:
        fig (go.Figure): Plotly figure to export
        filename (str, optional): Output filename. If None, a default name is generated.
        format (str, optional): Image format ('jpg', 'png', 'svg', 'pdf'). Defaults to 'jpg'.
        width (int, optional): Image width in pixels. Defaults to 1200.
        height (int, optional): Image height in pixels. Defaults to 800.
        link_text (str, optional): Text to display for the download link. Defaults to "Download Image".

    Returns:
        str: HTML string containing the download link or error message
    """
    # Validate parameters
    if fig is None:
        return "Error: No figure provided for download link"

    # Validate and normalize format
    valid_formats = ['jpg', 'jpeg', 'png', 'svg', 'pdf', 'webp']
    format = format.lower()
    if format == 'jpeg':
        format = 'jpg'  # Normalize jpeg to jpg
    if format not in valid_formats:
        format = 'jpg'  # Default to jpg for unsupported formats

    # Set correct MIME type
    mime_types = {
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'svg': 'image/svg+xml',
        'pdf': 'application/pdf',
        'webp': 'image/webp'
    }
    mime_type = mime_types.get(format, 'image/jpeg')

    # Generate filename if not provided
    if filename is None:
        try:
            title = fig.layout.title.text if hasattr(fig.layout, 'title') and fig.layout.title.text else 'chart'
            # Clean title for filename
            title = ''.join(c if c.isalnum() else '_' for c in title)
            # Limit length
            title = title[:50]
            filename = f"{title}.{format}"
        except Exception:
            filename = f"chart.{format}"
    elif not filename.endswith(f'.{format}'):
        filename = f"{filename}.{format}"

    # Check if kaleido is available for image export
    if not HAS_KALEIDO:
        return f'<span style="color: #999; cursor: not-allowed;">{link_text} (Error: kaleido package not installed)</span>'

    try:
        # Convert figure to image bytes
        img_bytes = fig.to_image(format=format, width=width, height=height, scale=2)

        # Encode image bytes to base64
        b64 = base64.b64encode(img_bytes).decode()

        # Create HTML download link with proper styling
        href = f'data:{mime_type};base64,{b64}'
        download_link = f'''
        <a href="{href}"
           download="{filename}"
           style="display: inline-block;
                  padding: 0.5em 1em;
                  color: white;
                  background-color: #4CAF50;
                  text-decoration: none;
                  border-radius: 4px;
                  text-align: center;">
            {link_text}
        </a>
        '''

        return download_link
    except Exception as e:
        print(f"Error generating download link: {e}")
        # Return a disabled link with error message
        return f'<span style="color: #999; cursor: not-allowed;">{link_text} (Error: Unable to generate)</span>'
