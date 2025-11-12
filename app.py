from gc import is_finalized

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
from src.app_utils.gcp_authenticate import AuthenticateServiceAccount

class EcoApp:

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

    def __init__(self):
        self.lat = 50
        self.lon = 5
        self.area = 1
        self.ecosystem_type = None
        self.model_class = None
        self.ecosystem_display_name = None
        self.project_variables = {}
        self.float_variables = {}
        self.cost_layers = {}
        self.model_results = {}
        self.gee_project = ''

    def connect_to_google(self):
        if st.button("Connect to data"):
            gcp_credentials = dict(st.secrets["google_sa_secrets"])

            try:
                au = AuthenticateServiceAccount(gcp_credentials)
                au.set_credentials()
                au.initialize_ee()
                st.session_state.gee_initialized = True
            except Exception as e:
                st.error(f"❌ Failed to connect to Google Cloud: {str(e)}")
                st.session_state.gee_initialized = False

    def gee_auth(self):

        # Google Earth Engine Project
        self.gee_project = st.text_input(
            "Project ID",
            placeholder="your-gee-project-id",
            help="Enter your Google Earth Engine project ID"
        )

        if st.button("Initialize GEE"):
            if not self.gee_project:
                st.error("Please enter your GEE project ID")
            else:
                try:
                    ee.Authenticate()
                    ee.Initialize(project=self.gee_project)
                    st.success(f"✅ Connected to GEE project: {self.gee_project}")
                    st.session_state.gee_initialized = True
                except Exception as e:
                    st.error(f"❌ Failed to initialize GEE: {str(e)}")
                    st.session_state.gee_initialized = False

    def select_ecosystem(self):

        self.ecosystem_type = st.selectbox(
            "Select ecosystem type:",
            options=list(self.ECOSYSTEM_DISPLAY_NAMES.keys()),
            format_func=lambda x: self.ECOSYSTEM_DISPLAY_NAMES[x],
            help="Choose the ecosystem type that best describes your study area",
            on_change=st.rerun
        )

        self.model_class = self.ECOSYSTEM_MODELS[self.ecosystem_type]
        self.ecosystem_display_name = self.ECOSYSTEM_DISPLAY_NAMES[self.ecosystem_type]
        #st.rerun()

    def initialize_status(self):

        if 'extracted_values' not in st.session_state:
            st.session_state.extracted_values = {}
        if 'extraction_done' not in st.session_state:
            st.session_state.extraction_done = False
        if 'lat_input' not in st.session_state:
            st.session_state.lat_input = self.lat
        if 'lon_input' not in st.session_state:
            st.session_state.lon_input = self.lon
        if 'area_input' not in st.session_state:
            st.session_state.area_input = self.area
        if 'saved_polygon' not in st.session_state:
            st.session_state.saved_polygon = None
        if 'polygon_centroid' not in st.session_state:
            st.session_state.polygon_centroid = None
        if 'active_location_tab' not in st.session_state:
            st.session_state.active_location_tab = "manual"

    def sidebar(self):

        with st.sidebar:
            self.gee_auth()

            st.markdown("---")

            self.select_ecosystem()

            st.markdown('---')

    def tab_layout(self):

        # CSS code to get the tabs to look nice
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
                        border-radius: 8px 8px 0px 0px; /* Rounded top corners */
                        gap: 1px;
                        padding-top: 3px;
                        padding-bottom: 3px;
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

    def manual_input(self):

        if st.button("🔄 Use Manual Input", key="use_manual_input", help="Click to use manual coordinates"):
            st.session_state.active_location_tab = "manual"
            self.lat = st.session_state.lat_input
            self.lon = st.session_state.lon_input
            self.area = st.session_state.area_input
            st.rerun()

        if st.session_state.active_location_tab == "manual":
            st.success("✅ **Manual input is active**")
        else:
            st.warning("⚠️ Polygon mode is active - click 'Use Manual Input' to switch")

        st.number_input(
            "Latitude",
            min_value=-90.0,
            max_value=90.0,
            step=0.01,
            format="%.6f",
            key="lat_input"
        )

        st.number_input(
            "Longitude",
            min_value=-180.0,
            max_value=180.0,
            step=0.01,
            format="%.6f",
            key="lon_input"
        )

        st.number_input(
            "Project Area (hectares)",
            min_value=1,
            step=1,
            format="%d",
            key="area_input"
        )

    def preview_map(self):
        # Show a preview map with the manually entered coordinates
        preview_map = folium.Map(location=[self.lat, self.lon], zoom_start=7)
        folium.Marker(
            location=[self.lat, self.lon],
            popup=f"Location: {self.lat:.6f}, {self.lon:.6f}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(preview_map)
        st_folium(preview_map, key="preview_map", height=400, use_container_width=True)

    def polygon_info(self):

        if st.button("🔄 Use Polygon Input", key="use_polygon_input", help="Click to use polygon coordinates"):
            st.session_state.active_location_tab = "polygon"
            self.lat = st.session_state.polygon_centroid[0]
            self.lon = st.session_state.polygon_centroid[1]
            self.area = st.session_state.polygon_area
            st.rerun()

        # Show which mode is active
        if st.session_state.active_location_tab == "polygon":
            st.success("✅ **Polygon input is active**")
        else:
            st.warning("⚠️ Manual mode is active - click 'Use Polygon Input' to switch")

        # Show current coordinates from polygon
        if st.session_state.polygon_centroid is not None:
            lat = st.session_state.polygon_centroid[0]
            lon = st.session_state.polygon_centroid[1]
            area = st.session_state.polygon_area

            st.success("**Coordinates from Polygon:**")
            st.write(f"**Latitude:** {lat:.6f}")
            st.write(f"**Longitude:** {lon:.6f}")
            st.write(f"**Estimated Area:** {area:,.2f} hectares")

        else:
            st.warning("**No polygon drawn yet**")
            st.info("Draw a polygon on the map to automatically set coordinates")


        # Button to clear polygon
        if st.session_state.saved_polygon is not None:
            if st.button("🗑️ Clear Polygon", key="clear_poly"):
                st.session_state.saved_polygon = None
                st.session_state.polygon_centroid = None
                st.success("Polygon cleared!")
                st.rerun()

    def draw_map(self):
        print('draw_map')
        # Create folium map centered on current coordinates
        map_center = [self.lat , self.lon]
        m = folium.Map(location=map_center, zoom_start=7)

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
        map_data = st_folium(m, key="polygon_map", height=400, use_container_width=True)

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
                self.lat = centroid.y
                self.lon = centroid.x
                self.area = area

                # Display current polygon info
                st.success("✅ Polygon saved!")
                st.write(f"**Centroid:** {centroid.y:.6f}, {centroid.x:.6f}")
                st.write(f"**Estimated Area:** {area:,.2f} hectares")

    def location_info(self):

        # Get location information based on coordinates
        county, country = St_Utils.get_location_info(self.lat, self.lon)

        # Display location information
        location_text = ""
        if county and country:
            location_text = f" | Location: {county}, {country}"
        elif country:
            location_text = f" | Location: {country}"

        st.subheader(f"{self.ecosystem_display_name}{location_text}")
        # Optionally show coordinates
        if self.lat != 0.0 or self.lon != 0.0:
            st.caption(f"Coordinates: {self.lat:.6f}, {self.lon:.6f}")

    def project_variables_menu(self):

        cols = st.columns(2)
        for i, pvar_obj in enumerate(self.model_class.PROJECT_VARIABLES):
            display_name = St_Utils.get_project_variable_display_info(pvar_obj)

            var_key = pvar_obj.variable.name

            with cols[i % 2]:
                self.project_variables[var_key] = st.checkbox(
                    display_name,
                    key=f"proj_{var_key}_{self.ecosystem_type}"
                )
    def cost_variables_menu(self):

        cols = st.columns(2)
        for i, pvar_obj in enumerate(self.model_class.GLOBAL_LAYERS):
            display_name = pvar_obj.full_name
            var_key = pvar_obj.name

            with cols[i % 2]:
                self.cost_layers[var_key] = st.checkbox(
                    display_name,
                    key=f"cost_{var_key}_{self.ecosystem_type}"
                )

    def model_variables_menu(self):


        cols = st.columns(2)
        for i, var_obj in enumerate(self.model_class.VARIABLES):
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
            session_key = f"var_{var_key}_{self.ecosystem_type}"

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
                self.float_variables[var_key] = st.number_input(
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
                with st.spinner(
                        f"Extracting values from Google Earth Engine for {self.lat:.6f}, {self.lon:.6f} {self.area}... "):
                    extracted_values, error = St_Utils.extract_values(self.model_class, self.lat, self.lon, self.area)

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

    def calculate_value(self):
        if st.button("Calculate Value", type="primary", use_container_width=True):
            # Validate inputs
            if not all([self.lat != 0 or self.lon != 0, self.area > 0]):
                st.error("Please provide valid latitude, longitude, and area values")
            elif not any(self.float_variables.values()):
                st.error("Please provide values for the model variables (use 'Extract Values' or enter manually)")
            else:
                # Calculate ecosystem value
                value_per_ha, error = St_Utils.calculate_ecosystem_value(
                    self.model_class, self.float_variables, self.project_variables, self.area
                )
                cost_layers = []
                for pvar_obj in self.model_class.GLOBAL_LAYERS:
                    var_key = pvar_obj.name
                    is_selected = self.cost_layers.get(var_key, 0)
                    if is_selected:
                        cost_layers.append(pvar_obj)

                cost_per_ha = St_Utils.extract_global_layers(cost_layers, self.lat, self.lon, self.area)

                if error:
                    st.error(f"Calculation failed: {error}")
                else:
                    total_value = value_per_ha * self.area

                    # Display results
                    st.success("✅ Calculation Complete!")

                    # Create results display
                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            label="Annual benefit",
                            value=f"${value_per_ha:,.2f}",
                            help="USD per hectare per year"
                        )
                        for cost in cost_per_ha:
                            k = [k for k, v in cost.items()][0]
                            v = [v for k, v in cost.items()][0]
                            st.metric(
                                label=k,
                                value = f"${v:,.2f}",
                                help = "USD per hectare"
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
                    - Ecosystem Type: {self.ecosystem_display_name}
                    - Location: ({self.lat}, {self.lon})
                    - Project Area: {self.area:,.0f} hectares

                    This value represents the annual flow of ecosystem services benefits for the specified project area.
                    """)



def main():

    #-------------------------------------------------- Main config --------------------------------------------------#
    st.set_page_config(
        page_title="Ecosystem Valuation Tool",
        page_icon="🌱",
        layout="wide"
    )
    # Instantiate the main class
    if 'instantiated' not in st.session_state:
        st.session_state.instantiated = False

    if not st.session_state.instantiated:
        st.session_state.app = EcoApp()
        st.session_state.app.initialize_status()
        st.session_state.instantiated = True

    # --------------------------------------------------- Side Bar ---------------------------------------------------#
    with st.sidebar:

        st.markdown("## **🌱 Ecosystem Valuation Tool**")

        st.session_state.app.location_info()
        st.markdown("---")

        st.header('Configuration')
        st.subheader('Data Access')
        st.session_state.app.connect_to_google()
        st.markdown("---")

        st.subheader('Ecosystem Type')
        st.session_state.app.select_ecosystem()
        st.markdown("---")

    # --------------------------------------------------- Main Page --------------------------------------------------#
    # Main Page
    st.title("🌱 Ecosystem Valuation Tool")
    st.markdown("---")
    # Introduction
    st.markdown(
    """
    **Welcome to the Ecosystem Valuation Tool**

    This application estimated the annual value of ecosystem services across different ecosystems based on value
    transfer functions. You can assess the total value of various ecosystem services for your specific project location,
    based on spatial environmental variables and selected project variables.
    """
    )
    # define the ecosystem based on choice made in the side bar

    # -------------------- Tabs -------------------- #
    # create the tab layout
    st.session_state.app.tab_layout()
    st.header('Project Location')
    tab_manual, tab_polygon = st.tabs(["📍 Enter Manually", "🗺️ Draw Polygon"])
    with tab_manual:
        col_params_man, col_map_man = st.columns([1, 1])
        with col_params_man:
            st.session_state.app.manual_input()
        with col_map_man:
            st.session_state.app.preview_map()

    with tab_polygon:
        col_params_pol, col_map_pol = st.columns([1, 1])
        with col_params_pol:
            st.session_state.app.polygon_info()
        with col_map_pol:
            st.session_state.app.draw_map()
    # -------------------- Variables -------------------- #
    st.header('Variables')
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Benefits")
        st.markdown("""
        Select which ecosystem services you want to include in the benefit assessment.
        """)
        st.session_state.app.project_variables_menu()
        st.subheader("Cost")
        st.markdown("""
               Select which costs you want to include in the cost assessment.
               """)
        st.session_state.app.cost_variables_menu()
    with col2:
        st.subheader("Spatial Variables")
        st.session_state.app.model_variables_menu()
    # -------------------- Output -------------------- #
    st.markdown("---")
    st.session_state.app.calculate_value()


if __name__ == "__main__":
    main()