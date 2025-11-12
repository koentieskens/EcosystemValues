import streamlit as st
import folium
from streamlit_folium import st_folium
from shapely.geometry import Polygon

import ee
import sys
import os

# Add the project root to the path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.app_utils.utils import St_Utils
from src.models.benefit_models import (
    TropicalForest, TemparateForest, IntensiveLandUse,
    Mangroves, Grassland
)

# Configuration
ECOSYSTEM_MODELS = {
    'tropical_forest': TropicalForest,
    'temperate_forest': TemparateForest,
    'intensive_land_use': IntensiveLandUse,
    'mangroves': Mangroves,
    'grassland': Grassland
}

ECOSYSTEM_DISPLAY_NAMES = {
    'tropical_forest': 'Tropical Forest',
    'temperate_forest': 'Temperate Forest',
    'intensive_land_use': 'Intensive Land Use',
    'mangroves': 'Mangroves',
    'grassland': 'Grassland'
}


def main():
    try:
        st.set_page_config(
            page_title="Ecosystem Valuation Tool",
            page_icon="🌱",
            layout="wide"
        )
    except:
        pass  # Ignore if not supported in older Streamlit versions

    st.title("🌱 Ecosystem Valuation Tool")
    st.markdown("---")
    St_Utils.inject_responsive_css()

    # Initialize session state
    if 'extracted_values' not in st.session_state:
        st.session_state.extracted_values = {}
    if 'extraction_done' not in st.session_state:
        st.session_state.extraction_done = False

    # Introduction
    st.markdown("""
    **Welcome to the Ecosystem Valuation Tool**

    This application estimated the annual value of ecosystem services across different 
    ecosystems based on value transfer functions. You can assess the total value 
     of various ecosystem services for your specific project location, based on spatial environmental 
     variables and selected project variables.
    """)

    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")

        # Google Earth Engine Project
        st.subheader("Google Earth Engine")
        gee_project = st.text_input(
            "Project ID",
            placeholder="your-gee-project-id",
            help="Enter your Google Earth Engine project ID"
        )

        if st.button("Initialize GEE"):
            if not gee_project:
                st.error("Please enter your GEE project ID")
            else:
                try:
                    ee.Authenticate(force=True)
                    ee.Initialize(project=gee_project)
                    st.success(f"✅ Connected to GEE project: {gee_project}")
                    st.session_state.gee_initialized = True
                except Exception as e:
                    st.error(f"❌ Failed to initialize GEE: {str(e)}")
                    st.session_state.gee_initialized = False

        st.markdown("---")

        # Ecosystem Type Selection
        st.subheader("Ecosystem Type")
        ecosystem_type = st.selectbox(
            "Select ecosystem type:",
            options=list(ECOSYSTEM_DISPLAY_NAMES.keys()),
            format_func=lambda x: ECOSYSTEM_DISPLAY_NAMES[x],
            help="Choose the ecosystem type that best describes your study area"
        )

    # Main content area
    if ecosystem_type:
        model_class = ECOSYSTEM_MODELS[ecosystem_type]
        ecosystem_display_name = ECOSYSTEM_DISPLAY_NAMES[ecosystem_type]

        st.markdown("### Basic Project Parameters")



        # Initialize active tab in session state
        if 'active_location_tab' not in st.session_state:
            st.session_state.active_location_tab = "manual"

        st.markdown("""
        <style>
            /* Main container for tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 2px;
            }

            /* Individual tab appearance */
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                white-space: pre-wrap;
                background-color: #F0F2F6; /* Background for inactive tabs */
                border-radius: 4px 4px 0px 0px; /* Rounded top corners */
                gap: 1px;
                padding-top: 10px;
                padding-bottom: 10px;
                padding-left: 20px;
                padding-right: 20px;
                border: 1px solid #ddd; /* Add a border to all tabs */
                border-bottom: none; /* Remove bottom border for tab itself */
            }

            /* Active (selected) tab appearance */
            .stTabs [aria-selected="true"] {
                background-color: #FFFFFF; /* White background for active tab */
                border-bottom: none; /* Ensure no bottom border to blend with content frame */
            }

        </style>
        """, unsafe_allow_html=True)

        tab_manual, tab_polygon = st.tabs(["📍 Enter Manually", "🗺️ Draw Polygon"])


        # Initialize widget keys in session state if they don't exist
        if 'lat_input' not in st.session_state:
            st.session_state.lat_input = 20
        if 'lon_input' not in st.session_state:
            st.session_state.lon_input = 20
        if 'area_input' not in st.session_state:
            st.session_state.area_input = 1000

        with tab_manual:
            if st.button("🔄 Use Manual Input", key="use_manual_input", help="Click to use manual coordinates"):
                st.session_state.active_location_tab = "manual"
                #st.rerun()

            col_params, col_map = st.columns([1, 1])
            with col_params:
                if st.session_state.active_location_tab == "manual":
                    st.success("✅ **Manual input is active**")
                else:
                    st.warning("⚠️ Polygon mode is active - click 'Use Manual Input' to switch")

                latitude = st.number_input(
                    "Latitude",
                    min_value=-90.0,
                    max_value=90.0,
                    step=0.01,
                    format="%.6f",
                    key="lat_input"
                )

                longitude = st.number_input(
                    "Longitude",
                    min_value=-180.0,
                    max_value=180.0,
                    step=0.01,
                    format="%.6f",
                    key="lon_input"
                )

                area_hectares = st.number_input(
                    "Project Area (hectares)",
                    min_value=1,
                    step=1,
                    format="%d",
                    key="area_input"
                )

            with col_map:
                st.markdown("**Map Preview**")
                # Show a preview map with the manually entered coordinates
                preview_map = folium.Map(location=[latitude, longitude], zoom_start=10)
                folium.Marker(
                    location=[latitude, longitude],
                    popup=f"Location: {latitude:.6f}, {longitude:.6f}",
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(preview_map)
                st_folium(preview_map, key="preview_map", height=400)

        with tab_polygon:
            if st.button("🔄 Use Polygon Input", key="use_polygon_input", help="Click to use polygon coordinates"):
                st.session_state.active_location_tab = "polygon"
                st.rerun()

            # Initialize session state for polygon data
            if 'saved_polygon' not in st.session_state:
                st.session_state.saved_polygon = None
            if 'polygon_centroid' not in st.session_state:
                st.session_state.polygon_centroid = None

            col_params, col_map = st.columns([1, 1])

            with col_params:
                # Show which mode is active
                if st.session_state.active_location_tab == "polygon":
                    st.success("✅ **Polygon input is active**")
                else:
                    st.warning("⚠️ Manual mode is active - click 'Use Polygon Input' to switch")

                # Show current coordinates from polygon
                if st.session_state.polygon_centroid is not None:
                    latitude = st.session_state.polygon_centroid[0]
                    longitude = st.session_state.polygon_centroid[1]
                    area_hectares = st.session_state.polygon_area

                    #st.success("**Coordinates from Polygon:**")
                    st.write(f"**Latitude:** {latitude:.6f}")
                    st.write(f"**Longitude:** {longitude:.6f}")
                    st.write(f"**Estimated Area:** {area_hectares:.2f} hectares")

                else:
                    st.warning("**No polygon drawn yet**")
                    st.info("Draw a polygon on the map to automatically set coordinates")
                    # Use current manual input values as fallback
                    latitude = st.session_state.lat_input
                    longitude = st.session_state.lon_input
                    area_hectares = st.session_state.area_input


                # Button to clear polygon
                if st.session_state.saved_polygon is not None:
                    if st.button("🗑️ Clear Polygon", key="clear_poly"):
                        st.session_state.saved_polygon = None
                        st.session_state.polygon_centroid = None
                        st.success("Polygon cleared!")
                        st.rerun()

            with col_map:
                st.markdown("**Interactive Map - Draw Polygon**")

                # Create folium map centered on current coordinates
                map_center = [latitude if latitude != 0.0 else 0.0, longitude if longitude != 0.0 else 0.0]
                m = folium.Map(location=map_center, zoom_start=10)

                # Add saved polygon if it exists
                if st.session_state.saved_polygon is not None:
                    folium.Polygon(
                        locations=st.session_state.saved_polygon,
                        color='blue',
                        weight=2,
                        fill=True,
                        fillColor='lightblue',
                        fillOpacity=0.3,
                        popup="Saved Polygon"
                    ).add_to(m)

                    # Add centroid marker
                    if st.session_state.polygon_centroid is not None:
                        folium.Marker(
                            location=st.session_state.polygon_centroid,
                            popup=f"Centroid: {st.session_state.polygon_centroid[0]:.6f}, {st.session_state.polygon_centroid[1]:.6f}",
                            icon=folium.Icon(color='red', icon='star')
                        ).add_to(m)

                # Add drawing functionality
                folium.plugins.Draw(
                    export=False,
                    position='topleft',
                    draw_options={
                        'polyline': False,
                        'rectangle': True,
                        'polygon': True,
                        'circle': False,
                        'marker': False,
                        'circlemarker': False,
                    }
                ).add_to(m)

                # Display the map and capture drawing events
                map_data = st_folium(m, key="polygon_map", height=400)

                # Process drawn polygons
                if map_data['all_drawings'] and len(map_data['all_drawings']) > 0:
                    # Get the last drawn polygon
                    last_drawing = map_data['all_drawings'][-1]

                    if last_drawing['geometry']['type'] in ['Polygon', 'Rectangle']:
                        # Extract coordinates
                        coords = last_drawing['geometry']['coordinates'][0]

                        # Convert to shapely polygon for calculations
                        polygon_coords = [(coord[0], coord[1]) for coord in coords[:-1]]
                        shapely_polygon = Polygon(polygon_coords)
                        centroid = shapely_polygon.centroid
                        area = St_Utils.get_geodesic_area(shapely_polygon)

                        # Convert coordinates to lat/lon format for folium
                        folium_coords = [(coord[1], coord[0]) for coord in polygon_coords]

                        # Automatically update the polygon centroid
                        st.session_state.polygon_centroid = [centroid.y, centroid.x]
                        st.session_state.saved_polygon = folium_coords
                        st.session_state.polygon_area = area

                        # Display current polygon info
                        st.success("✅ Polygon saved!")
                        st.write(f"**Centroid:** {centroid.y:.6f}, {centroid.x:.6f}")
                        st.write(
                            f"**Estimated Area:** {area:.2f} hectares")

                # Set the final coordinates based on which tab is active
                if st.session_state.active_location_tab == "manual":
                    final_latitude = st.session_state.lat_input
                    final_longitude = st.session_state.lon_input
                    final_area = st.session_state.area_input
                else:  # polygon tab is active
                    if st.session_state.polygon_centroid is not None:
                        final_latitude = st.session_state.polygon_centroid[0]
                        final_longitude = st.session_state.polygon_centroid[1]
                        final_area = st.session_state.polygon_area
                    else:
                        final_latitude = st.session_state.lat_input
                        final_longitude = st.session_state.lon_input
                        final_area = st.session_state.area_input
        st.markdown("---")
        # Get location information based on coordinates
        county, country = St_Utils.get_location_info(final_latitude, final_longitude)

        # Display location information
        location_text = ""
        if county and country:
            location_text = f" | Location: {county}, {country}"
        elif country:
            location_text = f" | Location: {country}"



        st.subheader(f"Analysis for: {ecosystem_display_name}{location_text}")
        # Optionally show coordinates
        if final_latitude != 0.0 or final_longitude != 0.0:
            st.caption(f"Coordinates: {final_latitude:.6f}, {final_longitude:.6f}")
        st.markdown("---")

        col4, col5,  = st.columns(2)
        # Project Variables Section
        with col4:
            st.markdown("### Project Variables")
            st.markdown("Select which ecosystem services apply to your project:")

            project_variables = {}

            # Create columns for better layout
            cols = st.columns(2)
            for i, pvar_obj in enumerate(model_class.PROJECT_VARIABLES):
                display_name = St_Utils.get_project_variable_display_info(pvar_obj)

                var_key = pvar_obj.variable.name

                with cols[i % 2]:
                    project_variables[var_key] = st.checkbox(
                        display_name,
                        key=f"proj_{var_key}_{ecosystem_type}"
                    )
        with col5:

            # Model Variables Section
            st.markdown("### Spatial Variables")

            # Model variables inputs
            float_variables = {}
            cols = st.columns(2)
            for i, var_obj in enumerate(model_class.VARIABLES):
                display_name, tooltip = St_Utils.get_variable_display_info(var_obj)

                # Get the form field key
                if hasattr(var_obj, 'lc') and var_obj.lc is not None:
                    buffer = var_obj.var.buffer if var_obj.var.buffer else 0
                    var_key = var_obj.lc.get_name(buffer=buffer)
                else:
                    var_key = var_obj.var.name

                # Get default value from extracted values if available
                default_value = 0.0
                if var_key in st.session_state.extracted_values:
                    try:
                        default_value = float(st.session_state.extracted_values[var_key])
                    except (ValueError, TypeError):
                        default_value = 0.0

                # Create input field with session state key for persistence
                session_key = f"var_{var_key}_{ecosystem_type}"

                # Initialize session state if not exists
                if session_key not in st.session_state:
                    st.session_state[session_key] = default_value

                # If we just extracted values, update the session state
                if st.session_state.extraction_done and var_key in st.session_state.extracted_values:
                    try:
                        st.session_state[session_key] = float(st.session_state.extracted_values[var_key])
                    except (ValueError, TypeError):
                        pass
                with cols[i % 2]:
                    float_variables[var_key] = st.number_input(
                        f"{display_name}",
                        value=st.session_state[session_key],
                        step=0.01,
                        format="%.2f",
                        help=tooltip if tooltip else None,
                        key=session_key
                    )

            if st.button("🔄 Extract Spatial Values from GEE", type="primary",
                         use_container_width=True):
                if not st.session_state.get('gee_initialized', 0):
                    st.error("Please initialize Google Earth Engine first")
                else:
                    with st.spinner(f"Extracting values from Google Earth Engine for {final_latitude:.6f}, {final_longitude:.6f} {final_area}... "):
                        extracted_values, error = St_Utils.extract_values(model_class, final_latitude, final_longitude, final_area)

                        if error:
                            st.error(f"Extraction failed: {error}")
                        else:
                            # Store extracted values in session state
                            st.session_state.extracted_values = extracted_values
                            st.session_state.extraction_done = True
                            st.success(f"✅ Extracted {len(extracted_values)} variables")
                            st.rerun()  # Rerun to update the input fields

            # Show extraction status
            if st.session_state.extraction_done and st.session_state.extracted_values:
                st.info(f"✅ Using extracted values from GEE ({len(st.session_state.extracted_values)} variables)")

        st.markdown("---")


        # Calculate Value Button
        st.markdown("### 💰 Calculate Ecosystem Value")

        if st.button("Calculate Value", type="primary", use_container_width=True):
            # Validate inputs
            if not all([latitude != 0 or longitude != 0, area_hectares > 0]):
                st.error("Please provide valid latitude, longitude, and area values")
            elif not any(float_variables.values()):
                st.error("Please provide values for the model variables (use 'Extract Values' or enter manually)")
            else:
                # Calculate ecosystem value
                value_per_ha, error = St_Utils.calculate_ecosystem_value(
                    model_class, float_variables, project_variables, area_hectares
                )

                if error:
                    st.error(f"Calculation failed: {error}")
                else:
                    total_value = value_per_ha * area_hectares

                    # Display results
                    st.success("✅ Calculation Complete!")

                    # Create results display
                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            label="Value per hectare per annum",
                            value=f"${value_per_ha:,.2f}",
                            help="USD per hectare per year"
                        )

                    with col2:
                        st.metric(
                            label="Total annual value",
                            value=f"${total_value:,.2f}",
                            help="Total USD per year for the entire project area"
                        )

                    # Additional info
                    st.info(f"""
                    **Project Summary:**
                    - Ecosystem Type: {ecosystem_display_name}
                    - Location: ({latitude}, {longitude})
                    - Project Area: {area_hectares:,.0f} hectares

                    This value represents the annual flow of ecosystem services benefits for the specified project area.
                    """)

        # Display current inputs summary
        with st.expander("Current Inputs Summary"):
            st.write("**Basic Parameters:**")
            st.write(f"- Location: ({latitude}, {longitude})")
            st.write(f"- Area: {area_hectares} hectares")

            st.write("**Model Variables:**")
            for key, value in float_variables.items():
                st.write(f"- {key.replace('_', ' ').title()}: {value}")

            st.write("**Selected Project Variables:**")
            selected_vars = [key.replace('_', ' ').title() for key, value in project_variables.items() if value]
            if selected_vars:
                for var in selected_vars:
                    st.write(f"- {var}")
            else:
                st.write("- None selected")

        # Clear extracted values button
        if st.session_state.extraction_done:
            st.markdown("---")
            if st.button("🗑️ Clear Extracted Values", type="secondary"):
                st.session_state.extracted_values = {}
                st.session_state.extraction_done = False
                st.rerun()


if __name__ == "__main__":
    main()