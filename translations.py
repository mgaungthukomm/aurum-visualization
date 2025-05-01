"""
Translations Module for Aurum Visualization Dashboard

This module provides translations for the dashboard in multiple languages.
Currently supported languages:
- English (en)
- Myanmar (my)
"""

# Dictionary of translations
# Structure: translations[language_code][text_key] = translated_text
translations = {
    "en": {
        # App title and headers
        "app_title": "Visualization Dashboard",
        "welcome_title": "Welcome to the Visualization Dashboard",
        "welcome_subtitle": "This powerful tool helps you visualize and analyze transportation data with interactive charts and detailed metrics.",

        # Navigation and sections
        "upload_data": "Upload Data",
        "data_source_selection": "Data Source Selection",
        "filter_data": "Filter Data",
        "dashboard_navigation": "Dashboard Navigation",
        "about_dashboard": "About Aurum Visualization",
        "tips_tricks": "Tips & Tricks",
        "summary_stats": "Summary Statistics",
        "data_explorer": "Data Explorer",

        # Data loading
        "upload_excel": "Upload Excel file",
        "select_file_category": "Select file category:",
        "all_files": "All Files",
        "retail_files": "Retail Files",
        "nepas_files": "NEPAS Files",
        "alx_files": "ALX Files",
        "other_files": "Other Files",
        "select_excel_file": "Select Excel file:",
        "file_information": "File Information:",
        "name": "Name",
        "size": "Size",
        "type": "Type",
        "last_modified": "Last Modified",
        "load_file": "Load",
        "no_excel_files": "No Excel files found in the current directory.",
        "upload_file_tab": "Please upload a file using the 'Upload File' tab.",
        "drag_drop": "Drag and drop an Excel file here or click to browse",

        # Success and error messages
        "data_loaded": "loaded successfully!",
        "records": "records",
        "loading_data": "Loading data from",
        "could_not_read": "Could not read data from",
        "check_format": "Please check the file format.",
        "file_not_found": "not found in the current directory.",
        "error_loading": "Error loading data:",
        "error_processing": "Error processing uploaded file:",

        # Date filter
        "select_date_range": "Select date range",
        "load_data_first": "Load data first to enable date filtering.",
        "could_not_set_filter": "Could not set date filter",

        # Navigation categories
        "overview": "Overview",
        "destination_analysis": "Destination Analysis",
        "cargo_analysis": "Product Analysis",
        "fleet_analysis": "Fleet Analysis",
        "personnel_analysis": "Personnel Analysis",

        # Navigation buttons
        "summary_statistics": "Summary Statistics",
        "top_destinations": "Top Destinations",
        "loaded_quantity": "Loaded Product",
        "acquisition_types": "Acquisition Types",
        "truck_assignments": "Truck Assignments",
        "driver_assignments": "Driver Assignments",
        "helper_assignments": "Helper Assignments",

        # About section
        "about_this_dashboard": "About This Dashboard",
        "about_title": "Visualization Dashboard v2.0",
        "about_description": "A comprehensive analytics tool designed for transportation and logistics data visualization.",
        "data_requirements": "Data Requirements",
        "analysis_capabilities": "Analysis Capabilities",
        "technical_information": "Technical Information",

        # Tips section
        "getting_most": "Getting the Most from Visualization",
        "data_loading_tips": "Data Loading Tips",
        "navigation_tips": "Navigation Tips",
        "analysis_tips": "Analysis Tips",

        # Version history
        "version_history": "Version History",

        # Statistics tabs
        "overview_tab": "Overview",
        "fleet_tab": "Fleet",
        "personnel_tab": "Personnel",
        "cargo_tab": "Product",

        # Metrics
        "key_metrics": "Key Metrics",
        "total_records": "Total Records",
        "date_range": "Date Range",
        "unique_destinations": "Unique Destinations",
        "avg_trips_per_destination": "Avg Trips per Destination",
        "total_days": "Total Days",
        "avg_trips_per_day": "Avg Trips per Day",
        "fleet_metrics": "Fleet Metrics",
        "total_trucks": "Total Trucks",
        "avg_trips_per_truck": "Avg Trips per Truck",
        "own_trucks": "Own Trucks (%)",
        "leased_trucks": "Leased Trucks (%)",
        "personnel_metrics": "Personnel Metrics",
        "unique_drivers": "Unique Drivers",
        "unique_helpers": "Unique Helpers",
        "avg_trips_per_driver": "Avg Trips per Driver",
        "avg_trips_per_helper": "Avg Trips per Helper",
        "cargo_metrics": "Product Metrics",
        "total_loaded_quantity": "Total Loaded Product",
        "avg_load_per_trip": "Avg Product per Transport",
        "avg_load_per_truck": "Avg Product per Truck",
        "avg_load_per_destination": "Avg Product per Destination",

        # Data explorer
        "view_raw_data": "View Raw Data",
        "download_data": "Download Data as CSV",

        # Sample visualization
        "sample_visualization": "Sample Visualization",
        "sample_visualization_info": "This is a sample visualization. Upload your data to see actual insights.",

        # Getting started
        "getting_started": "Getting Started:",
        "select_excel": "Select an Excel file from the dropdown menu and click \"Load Selected Data\"",
        "upload_own_file": "Upload your own Excel file using the sidebar or the Upload File tab",
        "data_format_requirements": "Data Format Requirements:",
        "key_features": "Key Features:",
        "interactive_visualizations": "Interactive Visualizations: Explore data through charts and graphs",
        "detailed_analytics": "Detailed Analytics: Get insights on truck utilization, driver performance, and more",
        "export_capabilities": "Export Capabilities: Save charts as JPG files for reports and presentations",
        "filtering_options": "Filtering Options: Analyze data by date ranges and other parameters",

        # Tabs
        "excel_files_tab": "Excel Files",
        "upload_file_tab": "Upload File",

        # Export options
        "export_as_jpg": "Export as JPG",
        "download_chart": "Download Chart",

        # Advanced analysis
        "truck_destination_analysis": "Truck-Destination Analysis",
        "driver_helper_network": "Driver-Helper Network",

        # Language selection
        "language": "Language",
        "select_language": "Select Language",
        "english": "English",
        "myanmar": "Myanmar"
    },
    "my": {
        # App title and headers
        "app_title": "မြင်ကွင်း ဒက်ရှ်ဘုတ်",
        "welcome_title": "မြင်ကွင်း ဒက်ရှ်ဘုတ်မှ ကြိုဆိုပါသည်",
        "welcome_subtitle": "ဤအားကောင်းသော ကိရိယာသည် အပြန်အလှန် ဇယားများနှင့် အသေးစိတ် တိုင်းတာမှုများဖြင့် သယ်ယူပို့ဆောင်ရေး ဒေတာကို မြင်သာအောင် ပြုလုပ်ရန်နှင့် ခွဲခြမ်းစိတ်ဖြာရန် ကူညီပေးသည်။",

        # Navigation and sections
        "upload_data": "ဒေတာ တင်ရန်",
        "data_source_selection": "ဒေတာ ရင်းမြစ် ရွေးချယ်မှု",
        "filter_data": "ဒေတာ စစ်ထုတ်ရန်",
        "dashboard_navigation": "ဒက်ရှ်ဘုတ် လမ်းညွှန်",
        "about_dashboard": "မြင်ကွင်း အကြောင်း",
        "tips_tricks": "အကြံပြုချက်များနှင့် နည်းလမ်းများ",
        "summary_stats": "အနှစ်ချုပ် စာရင်းအင်းများ",
        "data_explorer": "ဒေတာ စူးစမ်းရှာဖွေရေး",

        # Data loading
        "upload_excel": "Excel ဖိုင် တင်ရန်",
        "select_file_category": "ဖိုင် အမျိုးအစား ရွေးချယ်ပါ:",
        "all_files": "ဖိုင်အားလုံး",
        "retail_files": "လက်လီ ဖိုင်များ",
        "nepas_files": "NEPAS ဖိုင်များ",
        "alx_files": "ALX ဖိုင်များ",
        "other_files": "အခြား ဖိုင်များ",
        "select_excel_file": "Excel ဖိုင် ရွေးချယ်ပါ:",
        "file_information": "ဖိုင် အချက်အလက်:",
        "name": "အမည်",
        "size": "အရွယ်အစား",
        "type": "အမျိုးအစား",
        "last_modified": "နောက်ဆုံး ပြင်ဆင်ချိန်",
        "load_file": "ဖိုင်ဖွင့်ရန်",
        "no_excel_files": "လက်ရှိ ဒါရိုက်ထရီတွင် Excel ဖိုင်များ မတွေ့ပါ။",
        "upload_file_tab": "'ဖိုင်တင်ရန်' တပ်ဗ်ကို အသုံးပြု၍ ဖိုင်တင်ပါ။",
        "drag_drop": "Excel ဖိုင်ကို ဤနေရာတွင် ဆွဲချပါ သို့မဟုတ် ရှာဖွေရန် နှိပ်ပါ",

        # Success and error messages
        "data_loaded": "အောင်မြင်စွာ ဖွင့်ပြီးပါပြီ!",
        "records": "မှတ်တမ်းများ",
        "loading_data": "ဒေတာ ဖွင့်နေသည်",
        "could_not_read": "ဒေတာကို ဖတ်၍မရပါ",
        "check_format": "ဖိုင်ပုံစံကို စစ်ဆေးပါ။",
        "file_not_found": "လက်ရှိ ဒါရိုက်ထရီတွင် မတွေ့ပါ။",
        "error_loading": "ဒေတာ ဖွင့်ရာတွင် အမှားရှိသည်:",
        "error_processing": "တင်ထားသော ဖိုင်ကို စီမံဆောင်ရွက်ရာတွင် အမှားရှိသည်:",

        # Date filter
        "select_date_range": "ရက်စွဲ အပိုင်းအခြား ရွေးချယ်ပါ",
        "load_data_first": "ရက်စွဲ စစ်ထုတ်မှုကို သုံးနိုင်ရန် ဒေတာကို ဦးစွာ ဖွင့်ပါ။",
        "could_not_set_filter": "ရက်စွဲ စစ်ထုတ်မှုကို သတ်မှတ်၍မရပါ",

        # Navigation categories
        "overview": "အနှစ်ချုပ်",
        "destination_analysis": "ဦးတည်ရာ ခွဲခြမ်းစိတ်ဖြာမှု",
        "cargo_analysis": "ဆီ ခွဲခြမ်းစိတ်ဖြာမှု",
        "fleet_analysis": "ဆီသယ်ယာဉ် ခွဲခြမ်းစိတ်ဖြာမှု",
        "personnel_analysis": "ဝန်ထမ်း ခွဲခြမ်းစိတ်ဖြာမှု",

        # Navigation buttons
        "summary_statistics": "အနှစ်ချုပ် စာရင်းအင်းများ",
        "top_destinations": "ထိပ်တန်း ဦးတည်ရာများ",
        "loaded_quantity": "တင်ဆောင်ထားသော ပမာဏ",
        "acquisition_types": "ရယူမှု အမျိုးအစားများ",
        "truck_assignments": "ဆီသယ်ယာဉ် တာဝန်ချထားမှုများ",
        "driver_assignments": "ယာဉ်မောင်း တာဝန်ချထားမှုများ",
        "helper_assignments": "အကူ တာဝန်ချထားမှုများ",

        # About section
        "about_this_dashboard": "ဤဒက်ရှ်ဘုတ်အကြောင်း",
        "about_title": "မြင်ကွင်း ဒက်ရှ်ဘုတ် v2.0",
        "about_description": "သယ်ယူပို့ဆောင်ရေးနှင့် ထောက်ပံ့ပို့ဆောင်ရေး ဒေတာ မြင်သာမှုအတွက် ဒီဇိုင်းထုတ်ထားသော ပြည့်စုံသော ခွဲခြမ်းစိတ်ဖြာရေး ကိရိယာ။",
        "data_requirements": "ဒေတာ လိုအပ်ချက်များ",
        "analysis_capabilities": "ခွဲခြမ်းစိတ်ဖြာမှု စွမ်းရည်များ",
        "technical_information": "နည်းပညာဆိုင်ရာ အချက်အလက်",

        # Tips section
        "getting_most": "မြင်ကွင်းမှ အကောင်းဆုံး ရယူခြင်း",
        "data_loading_tips": "ဒေတာ ဖွင့်ခြင်းဆိုင်ရာ အကြံပြုချက်များ",
        "navigation_tips": "လမ်းညွှန်ဆိုင်ရာ အကြံပြုချက်များ",
        "analysis_tips": "ခွဲခြမ်းစိတ်ဖြာမှုဆိုင်ရာ အကြံပြုချက်များ",

        # Version history
        "version_history": "ဗားရှင်း မှတ်တမ်း",

        # Statistics tabs
        "overview_tab": "အနှစ်ချုပ်",
        "fleet_tab": "ယာဉ်",
        "personnel_tab": "ဝန်ထမ်း",
        "cargo_tab": "ဆီ",

        # Metrics
        "key_metrics": "အဓိက တိုင်းတာချက်များ",
        "total_records": "စုစုပေါင်း မှတ်တမ်းများ",
        "date_range": "ရက်စွဲ အပိုင်းအခြား",
        "unique_destinations": "သီးခြား ဦးတည်ရာများ",
        "avg_trips_per_destination": "ဦးတည်ရာတစ်ခုလျှင် ပျမ်းမျှ ခရီးစဉ်များ",
        "total_days": "စုစုပေါင်း ရက်များ",
        "avg_trips_per_day": "တစ်ရက်လျှင် ပျမ်းမျှ ခရီးစဉ်များ",
        "fleet_metrics": "ယာဉ် တိုင်းတာချက်များ",
        "total_trucks": "စုစုပေါင်း ဆီသယ်ယာဉ်များ",
        "avg_trips_per_truck": "ဆီသယ်ယာဉ်တစ်စီးလျှင် ပျမ်းမျှ ခရီးစဉ်များ",
        "own_trucks": "ကိုယ်ပိုင် ဆီသယ်ယာဉ်များ (%)",
        "leased_trucks": "ငှားရမ်းထားသော ဆီသယ်ယာဉ်များ (%)",
        "personnel_metrics": "ဝန်ထမ်း တိုင်းတာချက်များ",
        "unique_drivers": "သီးခြား ယာဉ်မောင်းများ",
        "unique_helpers": "သီးခြား အကူများ",
        "avg_trips_per_driver": "ယာဉ်မောင်းတစ်ဦးလျှင် ပျမ်းမျှ ခရီးစဉ်များ",
        "avg_trips_per_helper": "အကူတစ်ဦးလျှင် ပျမ်းမျှ ခရီးစဉ်များ",
        "cargo_metrics": "ဆီ တိုင်းတာချက်များ",
        "total_loaded_quantity": "စုစုပေါင်း တင်ဆောင်ထားသော ဆီ",
        "avg_load_per_trip": "သယ်ယူပို့ဆောင်မှုတစ်ခုလျှင် ပျမ်းမျှ ဆီ",
        "avg_load_per_truck": "ဆီသယ်ယာဉ်တစ်စီးလျှင် ပျမ်းမျှ ဆီ",
        "avg_load_per_destination": "ဦးတည်ရာတစ်ခုလျှင် ပျမ်းမျှ ဆီ",

        # Data explorer
        "view_raw_data": "မူရင်း ဒေတာကို ကြည့်ရန်",
        "download_data": "ဒေတာကို CSV အဖြစ် ဒေါင်းလုဒ်လုပ်ရန်",

        # Sample visualization
        "sample_visualization": "နမူနာ မြင်သာမှု",
        "sample_visualization_info": "ဤသည်မှာ နမူနာ မြင်သာမှုဖြစ်သည်။ အမှန်တကယ် အမြင်များကို ကြည့်ရှုရန် သင့်ဒေတာကို တင်ပါ။",

        # Getting started
        "getting_started": "စတင်ရန်:",
        "select_excel": "ဖိုင်ရွေးချယ်ရန် မီနူးမှ Excel ဖိုင်ကို ရွေးချယ်ပြီး \"ရွေးချယ်ထားသော ဒေတာကို ဖွင့်ရန်\" ကို နှိပ်ပါ",
        "upload_own_file": "ဘေးဘားတန်း သို့မဟုတ် 'ဖိုင်တင်ရန်' တပ်ဗ်ကို အသုံးပြု၍ သင့်ကိုယ်ပိုင် Excel ဖိုင်ကို တင်ပါ",
        "data_format_requirements": "ဒေတာ ပုံစံ လိုအပ်ချက်များ:",
        "key_features": "အဓိက လုပ်ဆောင်ချက်များ:",
        "interactive_visualizations": "အပြန်အလှန် မြင်သာမှုများ: ဇယားများနှင့် ဂရပ်များမှတစ်ဆင့် ဒေတာကို စူးစမ်းပါ",
        "detailed_analytics": "အသေးစိတ် ခွဲခြမ်းစိတ်ဖြာမှု: ဆီသယ်ယာဉ် အသုံးပြုမှု၊ ယာဉ်မောင်း စွမ်းဆောင်ရည်နှင့် အခြားအရာများအပေါ် အမြင်များ ရယူပါ",
        "export_capabilities": "ထုတ်ယူနိုင်စွမ်း: ဇယားများကို JPG ဖိုင်များအဖြစ် သိမ်းဆည်းပြီး အစီရင်ခံစာများနှင့် ရှင်းလင်းတင်ပြမှုများအတွက် အသုံးပြုပါ",
        "filtering_options": "စစ်ထုတ်ရွေးချယ်မှု: ရက်စွဲ အပိုင်းအခြားများနှင့် အခြားပါရာမီတာများဖြင့် ဒေတာကို ခွဲခြမ်းစိတ်ဖြာပါ",

        # Tabs
        "excel_files_tab": "Excel ဖိုင်များ",
        "upload_file_tab": "ဖိုင်တင်ရန်",

        # Export options
        "export_as_jpg": "JPG အဖြစ် ထုတ်ယူရန်",
        "download_chart": "ဇယားကို ဒေါင်းလုဒ်လုပ်ရန်",

        # Advanced analysis
        "truck_destination_analysis": "ဆီသယ်ယာဉ်-ဦးတည်ရာ ခွဲခြမ်းစိတ်ဖြာမှု",
        "driver_helper_network": "ယာဉ်မောင်း-အကူ ကွန်ရက်",

        # Language selection
        "language": "ဘာသာစကား",
        "select_language": "ဘာသာစကား ရွေးချယ်ပါ",
        "english": "အင်္ဂလိပ်",
        "myanmar": "မြန်မာ"
    }
}


def get_text(key, language="en"):
    """
    Get translated text for a given key and language.

    Args:
        key (str): The text key to translate
        language (str): Language code (default: "en")

    Returns:
        str: Translated text or the key itself if translation not found
    """
    # If language not supported, fall back to English
    if language not in translations:
        language = "en"

    # If key not found, return the key itself
    if key not in translations[language]:
        return key

    return translations[language][key]
