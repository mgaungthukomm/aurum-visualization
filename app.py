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
import translations as tr

# Page configuration is set below

# Set page configuration with favicon
st.set_page_config(
    page_title="Visualization Dashboard",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for Material Design 3 Expressive styling
st.markdown("""
<style>
    /* Material Design 3 Expressive color palette - more vibrant and dynamic */
    :root {
        /* Primary color - more vibrant purple */
        --md-primary: #8B5CF6;
        --md-primary-container: #F3E8FF;
        --md-on-primary: #FFFFFF;
        --md-on-primary-container: #4C1D95;

        /* Secondary color - teal for contrast */
        --md-secondary: #0EA5E9;
        --md-secondary-container: #E0F2FE;
        --md-on-secondary: #FFFFFF;
        --md-on-secondary-container: #0C4A6E;

        /* Tertiary color - coral for accent */
        --md-tertiary: #F97316;
        --md-tertiary-container: #FFEDD5;
        --md-on-tertiary: #FFFFFF;
        --md-on-tertiary-container: #7C2D12;

        /* Error color - more vibrant red */
        --md-error: #EF4444;
        --md-error-container: #FEE2E2;
        --md-on-error: #FFFFFF;
        --md-on-error-container: #7F1D1D;

        /* Background and surface colors - slightly warmer */
        --md-background: #FEFBFF;
        --md-on-background: #1A1523;
        --md-surface: #FEFBFF;
        --md-on-surface: #1A1523;
        --md-surface-variant: #F1EAFF;
        --md-on-surface-variant: #4A4458;

        /* Other colors */
        --md-outline: #7C7991;
        --md-outline-variant: #D8D5E0;
        --md-shadow: rgba(79, 70, 229, 0.15);
        --md-scrim: rgba(79, 70, 229, 0.3);
        --md-inverse-surface: #2E1065;
        --md-inverse-on-surface: #F5F3FF;
        --md-inverse-primary: #C4B5FD;

        /* Additional expressive colors */
        --md-accent-1: #EC4899;
        --md-accent-2: #10B981;
        --md-accent-3: #F59E0B;
        --md-accent-4: #3B82F6;

        /* Gradient backgrounds */
        --md-gradient-1: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%);
        --md-gradient-2: linear-gradient(135deg, #0EA5E9 0%, #3B82F6 100%);
        --md-gradient-3: linear-gradient(135deg, #F97316 0%, #F59E0B 100%);
    }

    /* Main header styling - more expressive with gradient */
    .main-header {
        font-size: 2.8rem;
        background: var(--md-gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.2rem;
        border-bottom: 3px solid var(--md-primary-container);
        font-weight: 700;
        letter-spacing: -0.02em;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }

    /* Section header styling - more dynamic */
    .sub-header {
        font-size: 2rem;
        color: var(--md-primary);
        padding: 0.7rem 0;
        margin: 2.5rem 0 1.5rem 0;
        border-bottom: 2px solid var(--md-primary-container);
        font-weight: 600;
        letter-spacing: -0.01em;
        position: relative;
    }

    .sub-header::after {
        content: "";
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 60px;
        height: 2px;
        background: var(--md-primary);
    }

    /* Card styling - more expressive with subtle gradient and enhanced shadow */
    .card {
        padding: 2rem;
        border-radius: 24px;
        background: linear-gradient(145deg, var(--md-surface) 0%, var(--md-surface-variant) 100%);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
        border-left: 6px solid var(--md-primary);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }

    /* Make buttons more expressive with gradient and enhanced hover effects */
    .stButton>button {
        width: 100%;
        font-weight: 600;
        border-radius: 12px;
        background: var(--md-gradient-1);
        color: var(--md-on-primary);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.9rem;
        padding: 0.7rem 1.2rem;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        opacity: 0.95;
    }

    .stButton>button:active {
        transform: translateY(0);
    }

    /* Improve sidebar appearance with subtle gradient */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--md-surface) 0%, var(--md-surface-variant) 100%);
        padding-top: 2rem;
        box-shadow: inset -5px 0 15px -5px rgba(0, 0, 0, 0.05);
    }

    /* Improve metric styling with more expressive colors */
    .css-1xarl3l, [data-testid="stMetricValue"] {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--md-primary);
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }

    [data-testid="stMetricLabel"] {
        font-weight: 500;
        color: var(--md-on-surface-variant);
    }

    [data-testid="stMetricDelta"] {
        font-weight: 600;
    }

    /* Info text styling */
    .info-text {
        font-size: 1.05rem;
        color: var(--md-on-surface-variant);
        line-height: 1.6;
        letter-spacing: 0.01em;
    }

    /* Improve table appearance with more expressive styling */
    .dataframe {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        border: none;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    .dataframe th {
        background: var(--md-gradient-2);
        color: var(--md-on-secondary);
        padding: 14px;
        text-align: left;
        font-weight: 600;
        letter-spacing: 0.02em;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    }

    .dataframe td {
        padding: 14px;
        border-bottom: 1px solid var(--md-outline-variant);
        color: var(--md-on-surface);
        transition: background-color 0.2s ease;
    }

    .dataframe tr:hover td {
        background-color: var(--md-surface-variant);
    }

    .dataframe tr:last-child td {
        border-bottom: none;
    }

    /* Improve expander styling with more expressive design */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: var(--md-on-surface);
        background-color: var(--md-surface-variant);
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    .streamlit-expanderHeader:hover {
        background-color: var(--md-primary-container);
        color: var(--md-on-primary-container);
    }

    .streamlit-expanderContent {
        border-radius: 0 0 12px 12px;
        padding-top: 1rem;
    }

    /* Improve tabs styling with more expressive design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
        border-bottom: 2px solid var(--md-outline-variant);
        padding-bottom: 2px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 54px;
        white-space: pre-wrap;
        background-color: var(--md-surface);
        border-radius: 12px 12px 0 0;
        gap: 1px;
        padding: 12px 20px;
        color: var(--md-on-surface-variant);
        font-weight: 500;
        transition: all 0.2s ease;
        border: 1px solid var(--md-outline-variant);
        border-bottom: none;
    }

    .stTabs [aria-selected="true"] {
        background: var(--md-gradient-1);
        color: var(--md-on-primary);
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
        background-color: var(--md-surface-variant);
        transform: translateY(-2px);
    }

    /* Radio buttons styling - more expressive */
    .stRadio [data-testid="stMarkdownContainer"] > p {
        font-size: 1.05rem;
        font-weight: 500;
        color: var(--md-on-surface);
    }

    .stRadio label {
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .stRadio label:hover {
        color: var(--md-primary);
    }

    /* Selectbox styling - more expressive */
    .stSelectbox label {
        color: var(--md-on-surface);
        font-weight: 500;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
    }

    .stSelectbox > div[data-baseweb="select"] {
        border-radius: 12px;
        transition: all 0.2s ease;
        border: 2px solid var(--md-outline-variant);
    }

    .stSelectbox > div[data-baseweb="select"]:focus-within {
        border-color: var(--md-primary);
        box-shadow: 0 0 0 2px var(--md-primary-container);
    }

    /* Date input styling - more expressive */
    .stDateInput label {
        color: var(--md-on-surface);
        font-weight: 500;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
    }

    .stDateInput > div[data-baseweb="input"] {
        border-radius: 12px;
        transition: all 0.2s ease;
        border: 2px solid var(--md-outline-variant);
    }

    .stDateInput > div[data-baseweb="input"]:focus-within {
        border-color: var(--md-primary);
        box-shadow: 0 0 0 2px var(--md-primary-container);
    }

    /* File uploader styling - more expressive */
    .stFileUploader label {
        color: var(--md-on-surface);
        font-weight: 500;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
    }

    .stFileUploader > div[data-testid="stFileUploader"] {
        border-radius: 12px;
        border: 2px dashed var(--md-outline-variant);
        transition: all 0.2s ease;
    }

    .stFileUploader > div[data-testid="stFileUploader"]:hover {
        border-color: var(--md-primary);
        background-color: var(--md-primary-container);
    }

    /* Success message styling - more expressive */
    .element-container div[data-testid="stAlert"] {
        background: linear-gradient(135deg, #84cc16 0%, #22c55e 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.8rem 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    /* Error message styling - more expressive */
    .element-container div[data-testid="stAlert"][data-baseweb="notification"] {
        background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.8rem 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    /* Info message styling - more expressive */
    .element-container div[data-testid="stAlert"][data-baseweb="notification"][kind="info"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        color: white;
    }

    /* Warning message styling - more expressive */
    .element-container div[data-testid="stAlert"][data-baseweb="notification"][kind="warning"] {
        background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%);
        color: white;
    }

    /* Markdown styling - more expressive */
    .element-container [data-testid="stMarkdownContainer"] h1,
    .element-container [data-testid="stMarkdownContainer"] h2,
    .element-container [data-testid="stMarkdownContainer"] h3 {
        color: var(--md-primary);
        font-weight: 700;
        letter-spacing: -0.01em;
    }

    .element-container [data-testid="stMarkdownContainer"] a {
        color: var(--md-accent-4);
        text-decoration: none;
        font-weight: 500;
        border-bottom: 1px solid transparent;
        transition: all 0.2s ease;
    }

    .element-container [data-testid="stMarkdownContainer"] a:hover {
        border-bottom-color: var(--md-accent-4);
    }

    /* Add animations for page load */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .main-header, .card, .sub-header {
        animation: fadeIn 0.5s ease-out forwards;
    }

    .card {
        animation-delay: 0.1s;
    }

    .sub-header {
        animation-delay: 0.2s;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--md-surface-variant);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--md-primary);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--md-primary);
        opacity: 0.8;
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
if 'language' not in st.session_state:
    st.session_state.language = "my"  # Default language is Myanmar
if 'auto_load_done' not in st.session_state:
    st.session_state.auto_load_done = False  # Flag to track if we've already tried to auto-load


def main():
    """Main function to run the Streamlit app"""

    # Header
    st.markdown(f'<div class="main-header">{tr.get_text("app_title", st.session_state.language)}</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("logo.png", width=80)

        # Language selector
        st.markdown(f"### {tr.get_text('language', st.session_state.language)}")
        language_options = {
            "en": tr.get_text("english", st.session_state.language),
            "my": tr.get_text("myanmar", st.session_state.language)
        }
        selected_language = st.radio(
            label=tr.get_text("select_language", st.session_state.language),
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            horizontal=True,
            key="language_selector",
            index=0 if st.session_state.language == "en" else 1,
            label_visibility="hidden"  # Hide the label but provide it for accessibility
        )

        # Update language in session state if changed
        if selected_language != st.session_state.language:
            st.session_state.language = selected_language
            st.rerun()

        st.markdown(f"## {tr.get_text('upload_data', st.session_state.language)}")

        # File uploader in sidebar
        uploaded_file = st.file_uploader(tr.get_text("upload_excel", st.session_state.language), type=["xlsx", "xls"], key="sidebar_uploader")

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
                    st.success(f"{tr.get_text('data_loaded', st.session_state.language)}")

                    # Show data info
                    st.markdown(f"### {tr.get_text('data_summary', st.session_state.language)}")
                    st.write(f"{tr.get_text('total_records', st.session_state.language)}: {len(df)}")
                    st.write(f"{tr.get_text('date_range', st.session_state.language)}: {df['Loading Date'].min().strftime('%Y-%m-%d')} to {df['Loading Date'].max().strftime('%Y-%m-%d')}")

                    # Date filter
                    st.markdown(f"### {tr.get_text('filter_data', st.session_state.language)}")
                    date_range = st.date_input(
                        tr.get_text("select_date_range", st.session_state.language),
                        value=(df['Loading Date'].min().date(), df['Loading Date'].max().date()),
                        min_value=df['Loading Date'].min().date(),
                        max_value=df['Loading Date'].max().date()
                    )

                    if len(date_range) == 2:
                        start_date, end_date = date_range
                        st.session_state.date_filter = (start_date, end_date)
                else:
                    st.error(f"{tr.get_text('could_not_read', st.session_state.language)} {tr.get_text('check_format', st.session_state.language)}")
            except Exception as e:
                st.error(f"Error processing file: {e}")

        # Enhanced data loading interface
        st.markdown(f"### 📂 {tr.get_text('data_source_selection', st.session_state.language)}")

        # Create tabs for different data loading methods
        data_tabs = st.tabs([
            f"📊 {tr.get_text('excel_files_tab', st.session_state.language)}",
            f"📤 {tr.get_text('upload_file_tab', st.session_state.language)}"
        ])

        with data_tabs[0]:
            # Check for available Excel files in the directory
            excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and os.path.isfile(f)]

            if excel_files:
                # Group files by type if possible
                retail_files = [f for f in excel_files if "retail" in f.lower()]
                nepas_files = [f for f in excel_files if "nepas" in f.lower()]
                alx_files = [f for f in excel_files if "alx" in f.lower()]
                other_files = [f for f in excel_files if f not in retail_files + nepas_files + alx_files]

                # Only show Retail Files and Other Files
                display_files = retail_files if retail_files else other_files

                # Auto-load the first retail file if available and not already loaded
                if not st.session_state.auto_load_done and retail_files:
                    st.session_state.auto_load_done = True
                    selected_file = retail_files[0]

                    try:
                        # Try to load the selected file
                        if os.path.exists(selected_file):
                            # Read the data using our data processor
                            df = dp.read_excel_data(selected_file)

                            if df is not None and not df.empty:
                                st.session_state.data = df
                                st.session_state.file_uploaded = True
                                st.success(f"✅ {selected_file} {tr.get_text('data_loaded', st.session_state.language)} ({len(df)} {tr.get_text('records', st.session_state.language)})")
                    except Exception as e:
                        # If auto-loading fails, we'll just continue with manual selection
                        pass

                # Add a dropdown to select which file to load
                selected_file = st.selectbox(
                    tr.get_text("select_excel_file", st.session_state.language),
                    options=display_files,
                    index=0,
                    format_func=lambda x: f"{x} ({os.path.getsize(x) // 1024} KB)"
                )

                # Add file info
                if selected_file:
                    file_stats = os.stat(selected_file)
                    st.info(f"""
                    **{tr.get_text("file_information", st.session_state.language)}**
                    - {tr.get_text("size", st.session_state.language)}: {file_stats.st_size // 1024} KB
                    - {tr.get_text("last_modified", st.session_state.language)}: {datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d')}
                    """)

                # Load button with improved styling
                if st.button(
                    label=f"📥 {tr.get_text('load_file', st.session_state.language)} {selected_file}",
                    key="load_selected",
                    use_container_width=True
                ):
                    try:
                        # Try to load the selected file
                        if os.path.exists(selected_file):
                            # Show loading spinner
                            with st.spinner(f"{tr.get_text('loading_data', st.session_state.language)} {selected_file}..."):
                                # Read the data using our data processor
                                df = dp.read_excel_data(selected_file)

                                if df is not None and not df.empty:
                                    st.session_state.data = df
                                    st.session_state.file_uploaded = True
                                    st.success(f"✅ {selected_file} {tr.get_text('data_loaded', st.session_state.language)} ({len(df)} {tr.get_text('records', st.session_state.language)})")
                                else:
                                    st.error(f"❌ {tr.get_text('could_not_read', st.session_state.language)} {selected_file}. {tr.get_text('check_format', st.session_state.language)}")
                        else:
                            st.error(f"❌ {selected_file} {tr.get_text('file_not_found', st.session_state.language)}")
                    except Exception as e:
                        st.error(f"❌ {tr.get_text('error_loading', st.session_state.language)} {e}")
            else:
                st.warning(f"📝 {tr.get_text('no_excel_files', st.session_state.language)}")
                st.info(f"{tr.get_text('upload_file_tab', st.session_state.language)}")

        with data_tabs[1]:
            # File uploader in tab
            uploaded_file_tab = st.file_uploader(tr.get_text("upload_excel", st.session_state.language), type=["xlsx", "xls"], key="tab_uploader")

            if uploaded_file_tab is not None:
                try:
                    # Show file info
                    st.info(f"""
                    **{tr.get_text("file_information", st.session_state.language)}**
                    - {tr.get_text("name", st.session_state.language)}: {uploaded_file_tab.name}
                    - {tr.get_text("size", st.session_state.language)}: {uploaded_file_tab.size // 1024} KB
                    - {tr.get_text("type", st.session_state.language)}: {uploaded_file_tab.type}
                    """)

                    # Save button
                    if st.button(
                        label=f"📥 {tr.get_text('load_file', st.session_state.language)} {uploaded_file_tab.name}",
                        key="load_uploaded",
                        use_container_width=True
                    ):
                        with st.spinner(f"{tr.get_text('loading_data', st.session_state.language)} {uploaded_file_tab.name}..."):
                            # Save the uploaded file temporarily
                            temp_file_path = os.path.join(".", uploaded_file_tab.name)
                            with open(temp_file_path, "wb") as f:
                                f.write(uploaded_file_tab.getbuffer())

                            # Read the data using our data processor
                            df = dp.read_excel_data(temp_file_path)

                            if df is not None and not df.empty:
                                st.session_state.data = df
                                st.session_state.file_uploaded = True
                                st.success(f"✅ {uploaded_file_tab.name} {tr.get_text('data_loaded', st.session_state.language)} ({len(df)} {tr.get_text('records', st.session_state.language)})")
                            else:
                                st.error(f"❌ {tr.get_text('could_not_read', st.session_state.language)} {uploaded_file_tab.name}. {tr.get_text('check_format', st.session_state.language)}")
                except Exception as e:
                    st.error(f"❌ {tr.get_text('error_processing', st.session_state.language)} {e}")
            else:
                st.info(f"📤 {tr.get_text('drag_drop', st.session_state.language)}")

        # Date filter
        st.markdown(f"### {tr.get_text('filter_data', st.session_state.language)}")
        # Only show date filter if data is loaded
        if st.session_state.file_uploaded and st.session_state.data is not None:
            temp_df = st.session_state.data
            try:
                date_range = st.date_input(
                    tr.get_text("select_date_range", st.session_state.language),
                    value=(temp_df['Loading Date'].min().date(), temp_df['Loading Date'].max().date()),
                    min_value=temp_df['Loading Date'].min().date(),
                    max_value=temp_df['Loading Date'].max().date()
                )

                if len(date_range) == 2:
                    start_date, end_date = date_range
                    st.session_state.date_filter = (start_date, end_date)
            except Exception as e:
                st.warning(f"{tr.get_text('could_not_set_filter', st.session_state.language)}: {e}")
        else:
            st.info(f"{tr.get_text('load_data_first', st.session_state.language)}")

        # Enhanced Navigation
        st.markdown("---")
        st.markdown(f"### 🧭 {tr.get_text('dashboard_navigation', st.session_state.language)}")

        # Group navigation buttons by category
        st.markdown(f"#### {tr.get_text('overview', st.session_state.language)}")
        if st.button(
            label=f"📊 {tr.get_text('summary_statistics', st.session_state.language)}",
            key="nav_summary"
        ):
            st.session_state.scroll_to = "summary_stats"

        st.markdown(f"#### {tr.get_text('destination_analysis', st.session_state.language)}")
        if st.button(
            label=f"🌎 {tr.get_text('top_destinations', st.session_state.language)}",
            key="nav_destinations"
        ):
            st.session_state.scroll_to = "top_destinations"

        st.markdown(f"#### {tr.get_text('cargo_analysis', st.session_state.language)}")
        if st.button(
            label=f"📦 {tr.get_text('loaded_quantity', st.session_state.language)}",
            key="nav_quantity"
        ):
            st.session_state.scroll_to = "loaded_quantity"

        st.markdown(f"#### {tr.get_text('fleet_analysis', st.session_state.language)}")
        if st.button(
            label=f"🏷️ {tr.get_text('acquisition_types', st.session_state.language)}",
            key="nav_acquisition"
        ):
            st.session_state.scroll_to = "acquisition_analysis"

        if st.button(
            label=f"🚚 {tr.get_text('truck_assignments', st.session_state.language)}",
            key="nav_trucks"
        ):
            st.session_state.scroll_to = "truck_assignments"

        st.markdown(f"#### {tr.get_text('personnel_analysis', st.session_state.language)}")
        if st.button(
            label=f"👨‍✈️ {tr.get_text('driver_assignments', st.session_state.language)}",
            key="nav_drivers"
        ):
            st.session_state.scroll_to = "driver_assignments"

        if st.button(
            label=f"👨‍🔧 {tr.get_text('helper_assignments', st.session_state.language)}",
            key="nav_helpers"
        ):
            st.session_state.scroll_to = "helper_assignments"

        # Enhanced About section
        st.markdown("---")
        st.markdown(f"### ℹ️ {tr.get_text('about_dashboard', st.session_state.language)}")

        with st.expander(tr.get_text("about_this_dashboard", st.session_state.language), expanded=False):
            st.markdown(f"""
            ### {tr.get_text("about_title", st.session_state.language)}

            {tr.get_text("about_description", st.session_state.language)}

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

        with st.expander(tr.get_text("tips_tricks", st.session_state.language), expanded=False):
            st.markdown(f"""
            ### {tr.get_text("getting_most", st.session_state.language)}

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

        with st.expander(tr.get_text("version_history", st.session_state.language), expanded=False):
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
        st.markdown(f'<div id="summary_stats" class="sub-header">📊 {tr.get_text("summary_stats", st.session_state.language)}</div>', unsafe_allow_html=True)

        # Create tabs for different categories of statistics
        stat_tabs = st.tabs([
            f"📈 {tr.get_text('overview_tab', st.session_state.language)}",
            f"🚚 {tr.get_text('fleet_tab', st.session_state.language)}",
            f"👨‍✈️ {tr.get_text('personnel_tab', st.session_state.language)}",
            f"📦 {tr.get_text('cargo_tab', st.session_state.language)}"
        ])

        with stat_tabs[0]:
            # Overview statistics
            st.markdown(f"### {tr.get_text('key_metrics', st.session_state.language)}")

            # Display summary statistics in a grid with icons and better formatting
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"📝 {tr.get_text('total_records', st.session_state.language)}", f"{stats['Total Records']:,}")
                st.metric(f"📅 {tr.get_text('date_range', st.session_state.language)}", stats['Date Range'])
            with col2:
                st.metric(f"🌎 {tr.get_text('unique_destinations', st.session_state.language)}", stats['Unique Destinations'])
                # Calculate average trips per destination
                avg_trips_per_dest = stats['Total Records'] / stats['Unique Destinations'] if stats['Unique Destinations'] > 0 else 0
                st.metric(f"🔄 {tr.get_text('avg_trips_per_destination', st.session_state.language)}", f"{avg_trips_per_dest:.1f}")
            with col3:
                # Calculate total days in date range
                try:
                    start_date, end_date = stats['Date Range'].split(" to ")
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")
                    total_days = (end_date - start_date).days + 1
                    st.metric(label="📆 Total Days", value=total_days)
                    # Calculate average trips per day
                    avg_trips_per_day = stats['Total Records'] / total_days if total_days > 0 else 0
                    st.metric(label="📊 Avg Trips per Day", value=f"{avg_trips_per_day:.1f}")
                except:
                    st.metric(label="📆 Total Days", value="N/A")
                    st.metric(label="📊 Avg Trips per Day", value="N/A")

        with stat_tabs[1]:
            # Fleet statistics
            st.markdown("### Fleet Metrics")

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="🚚 Total Trucks", value=stats['Unique Trucks'])
                # Calculate average trips per truck
                avg_trips_per_truck = stats['Total Records'] / stats['Unique Trucks'] if stats['Unique Trucks'] > 0 else 0
                st.metric(label="🔄 Avg Trips per Truck", value=f"{avg_trips_per_truck:.1f}")
            with col2:
                # Get acquisition type counts if available
                if 'Acquisition Type' in df.columns:
                    own_count = len(df[df['Acquisition Type'] == 'Own'])
                    lease_count = len(df[df['Acquisition Type'] == 'Lease'])
                    own_pct = own_count / len(df) * 100 if len(df) > 0 else 0
                    lease_pct = lease_count / len(df) * 100 if len(df) > 0 else 0
                    st.metric(label="🏠 Own Trucks (%)", value=f"{own_pct:.1f}%")
                    st.metric(label="📋 Leased Trucks (%)", value=f"{lease_pct:.1f}%")
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
                if st.button(
                    label=tr.get_text("export_as_jpg", st.session_state.language),
                    key="export_dest_jpg"
                ):
                    export_path = viz.export_figure_as_image(dest_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(dest_chart, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

        with col2:
            # Create the date chart
            date_chart = viz.create_date_chart(date_data)
            st.plotly_chart(date_chart, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button(
                    label=tr.get_text("export_as_jpg", st.session_state.language),
                    key="export_date_jpg"
                ):
                    export_path = viz.export_figure_as_image(date_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(date_chart, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

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
                if st.button(
                    label=tr.get_text("export_as_jpg", st.session_state.language),
                    key="export_truck_driver_jpg"
                ):
                    export_path = viz.export_figure_as_image(truck_driver_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(truck_driver_chart, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

        with col2:
            # Create the helper chart
            helper_chart = viz.create_helper_chart(helper_data)
            st.plotly_chart(helper_chart, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button(
                    label=tr.get_text("export_as_jpg", st.session_state.language),
                    key="export_helper_jpg"
                ):
                    export_path = viz.export_figure_as_image(helper_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(helper_chart, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

        # Row 4: Advanced visualizations
        st.markdown('<div class="sub-header">Advanced Analysis</div>', unsafe_allow_html=True)

        tab1, tab2 = st.tabs([
            f"{tr.get_text('truck_destination_analysis', st.session_state.language)}",
            f"{tr.get_text('driver_helper_network', st.session_state.language)}"
        ])

        with tab1:
            # Create the truck-destination chart
            truck_dest_chart = viz.create_truck_destination_chart(truck_destination_data)
            st.plotly_chart(truck_dest_chart, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button(
                    label=tr.get_text("export_as_jpg", st.session_state.language),
                    key="export_truck_dest_jpg"
                ):
                    export_path = viz.export_figure_as_image(truck_dest_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(truck_dest_chart, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

        with tab2:
            # Create the driver-helper network chart
            network_chart = viz.create_driver_helper_network(df)
            st.plotly_chart(network_chart, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button(
                    label=tr.get_text("export_as_jpg", st.session_state.language),
                    key="export_network_jpg"
                ):
                    export_path = viz.export_figure_as_image(network_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(network_chart, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

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
            if st.button(
                label=tr.get_text("export_as_jpg", st.session_state.language),
                key="export_top_routes_jpg"
            ):
                export_path = viz.export_figure_as_image(top_routes_chart, format='jpg')
                if export_path:
                    st.success(f"Chart exported to {export_path}")
        with export_col2:
            st.markdown(viz.get_image_download_link(top_routes_chart, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

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
            if st.button(
                label=tr.get_text("export_as_jpg", st.session_state.language),
                key="export_dest_quantity_jpg"
            ):
                export_path = viz.export_figure_as_image(dest_quantity_chart, format='jpg')
                if export_path:
                    st.success(f"Chart exported to {export_path}")
        with export_col2:
            st.markdown(viz.get_image_download_link(dest_quantity_chart, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

        # Display the truck quantity and time quantity charts side by side
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(truck_quantity_chart, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button(
                    label=tr.get_text("export_as_jpg", st.session_state.language),
                    key="export_truck_quantity_jpg"
                ):
                    export_path = viz.export_figure_as_image(truck_quantity_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(truck_quantity_chart, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

        with col2:
            st.plotly_chart(time_quantity_chart, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button(
                    label=tr.get_text("export_as_jpg", st.session_state.language),
                    key="export_time_quantity_jpg"
                ):
                    export_path = viz.export_figure_as_image(time_quantity_chart, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(time_quantity_chart, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

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
                if st.button(
                    label=tr.get_text("export_as_jpg", st.session_state.language),
                    key="export_acquisition_pie_jpg"
                ):
                    export_path = viz.export_figure_as_image(acquisition_pie, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(acquisition_pie, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

        with col2:
            st.plotly_chart(acquisition_bar, use_container_width=True)

            # Add export options
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                if st.button(
                    label=tr.get_text("export_as_jpg", st.session_state.language),
                    key="export_acquisition_bar_jpg"
                ):
                    export_path = viz.export_figure_as_image(acquisition_bar, format='jpg')
                    if export_path:
                        st.success(f"Chart exported to {export_path}")
            with export_col2:
                st.markdown(viz.get_image_download_link(acquisition_bar, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

        # Row 7: Truck Assignments Analysis
        st.markdown('<div id="truck_assignments" class="sub-header">Truck Assignments Analysis</div>', unsafe_allow_html=True)

        # Create the truck assignments chart
        truck_assignments_chart = viz.create_truck_assignments_chart(truck_assignments)

        # Display the chart
        st.plotly_chart(truck_assignments_chart, use_container_width=True)

        # Add export options
        export_col1, export_col2 = st.columns(2)
        with export_col1:
            if st.button(
                label=tr.get_text("export_as_jpg", st.session_state.language),
                key="export_truck_assignments_jpg"
            ):
                export_path = viz.export_figure_as_image(truck_assignments_chart, format='jpg')
                if export_path:
                    st.success(f"Chart exported to {export_path}")
        with export_col2:
            st.markdown(viz.get_image_download_link(truck_assignments_chart, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

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
            if st.button(
                label=tr.get_text("export_as_jpg", st.session_state.language),
                key="export_driver_assignments_jpg"
            ):
                export_path = viz.export_figure_as_image(driver_assignments_chart, format='jpg')
                if export_path:
                    st.success(f"Chart exported to {export_path}")
        with export_col2:
            st.markdown(viz.get_image_download_link(driver_assignments_chart, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

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
            if st.button(
                label=tr.get_text("export_as_jpg", st.session_state.language),
                key="export_helper_assignments_jpg"
            ):
                export_path = viz.export_figure_as_image(helper_assignments_chart, format='jpg')
                if export_path:
                    st.success(f"Chart exported to {export_path}")
        with export_col2:
            st.markdown(viz.get_image_download_link(helper_assignments_chart, format='jpg', link_text=tr.get_text("download_chart", st.session_state.language)), unsafe_allow_html=True)

        # Data explorer
        st.markdown(f'<div class="sub-header">{tr.get_text("data_explorer", st.session_state.language)}</div>', unsafe_allow_html=True)

        with st.expander(tr.get_text("view_raw_data", st.session_state.language)):
            st.dataframe(df)

            # Download option
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=tr.get_text("download_data", st.session_state.language),
                data=csv,
                file_name=f"transportation_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

    else:
        # Show enhanced welcome message when no data is loaded
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"""
        ## 🏆 {tr.get_text('welcome_title', st.session_state.language)}

        {tr.get_text('welcome_subtitle', st.session_state.language)}

        ### {tr.get_text('getting_started', st.session_state.language)}

        1. **{tr.get_text('select_excel', st.session_state.language)}**
        2. **{tr.get_text('upload_own_file', st.session_state.language)}**

        ### {tr.get_text('data_format_requirements', st.session_state.language)}

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

        ### {tr.get_text('key_features', st.session_state.language)}

        - **{tr.get_text('interactive_visualizations', st.session_state.language)}**
        - **{tr.get_text('detailed_analytics', st.session_state.language)}**
        - **{tr.get_text('export_capabilities', st.session_state.language)}**
        - **{tr.get_text('filtering_options', st.session_state.language)}**
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        # Show sample visualization
        st.markdown(f'<div class="sub-header">{tr.get_text("sample_visualization", st.session_state.language)}</div>', unsafe_allow_html=True)

        # Create sample data for preview
        sample_destinations = pd.DataFrame({
            'Destination': ['New York', 'Los Angeles', 'Chicago', 'Miami', 'Dallas'],
            'Count': [42, 38, 29, 25, 18]
        })

        # Show sample chart
        st.plotly_chart(viz.create_destination_chart(sample_destinations), use_container_width=True)

        st.info(f"👆 {tr.get_text('sample_visualization_info', st.session_state.language)}")


if __name__ == "__main__":
    main()
