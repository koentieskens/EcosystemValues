

import streamlit as st
import folium
from streamlit_folium import st_folium
from shapely.geometry import Polygon
import geopandas as gpd
import ee
import sys
import os

from src.utils.spatial import Spatial

# Add the project root to the path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.app_utils.utils import St_Utils
from src.predictions.meta_regression import Predict
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
        self.lat = 40
        self.lon = 10
        self.area = 1
        self.ecosystem_type = None
        self.model_class = None
        self.ecosystem_display_name = None
        self.ecosystem_services = {}
        self.sub_biomes = {}
        self.value_types = {}
        self.float_variables = {}
        self.cost_layers = {}
        self.model_results = {}
        self.siikamaki_layers = {}
        self.gee_project = ''
        self.aoi_gdf = None
        self.drawn_polygon = None

    def connect_to_google(self):
        """
        Connects to Google Cloud Platform using the provided service account
        credentials stored in Streamlit secrets. It attempts to authenticate,
        set the credentials, and initialize the Earth Engine API for use.

        This method updates the session state variable `gee_initialized` to
        indicate whether the Earth Engine API has been successfully initialized.

        :raises Exception: If the Google Cloud Platform secrets cannot be loaded
            from Streamlit secrets.
        :raises Exception: If the connection to Google Cloud Platform or the
            Earth Engine API initialization fails.

        :return: None
        """
        try:
            gcp_credentials = dict(st.secrets["google_sa_secrets"])
            try:
                au = AuthenticateServiceAccount(gcp_credentials)
                au.set_credentials()
                au.initialize_ee()
                st.session_state.gee_initialized = True
            except Exception as e:
                st.error(f"❌ Failed to connect to Google Cloud: {str(e)}")
                st.session_state.gee_initialized = False
        except Exception as e:
            st.error(f"❌ Failed to open GCS Secrets: {str(e)}")


    def biome_selection_boxes(self):
        """
        Render the biome selection boxes on a Streamlit app interface, allowing the user to select a biome
        from the provided options visually. The function incorporates CSS styling for the clickable biome boxes
        and tracks the user's selection, updating the ecosystem type, corresponding model, and display name
        based on the selected biome. A status message indicating the currently selected biome is displayed.

        :return: A boolean value indicating if a selection was made.
        :rtype: bool
        """
        # Add custom CSS for the biome boxes
        st.markdown("""
        <style>
        .biome-box {
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #f8f9fa;
            transition: all 0.3s ease;
            cursor: pointer;
            height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .biome-box:hover {
            border-color: #1f77b4;
            background-color: #e8f4fd;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .biome-box.selected {
            border-color: #1f77b4;
            background-color: #e8f4fd;
            border-width: 3px;
        }

        .biome-logo {
            font-size: 48px;
            margin-bottom: 10px;
        }

        .biome-name {
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin: 0;
        }
        </style>
        """, unsafe_allow_html=True)

        # Define biome logos (you can replace these with actual image paths if you have them)
        BIOME_LOGOS = {
            'tropical_forest': '🌴',
            'temperate_forest': '🌲',
            'intensive_land_use': '🏭',
            'mangroves': '🌿',
            'grassland': '🌾'
        }

        cols = st.columns(5)

        # Track if any selection was made
        selection_made = False

        for i, (ecosystem_key, display_name) in enumerate(self.ECOSYSTEM_DISPLAY_NAMES.items()):
            with cols[i]:
                logo = BIOME_LOGOS.get(ecosystem_key, '🌱')  # Default logo if not found

                # Determine if this biome is currently selected
                is_selected = self.ecosystem_type == ecosystem_key
                box_class = "biome-box selected" if is_selected else "biome-box"

                # Create the clickable box
                if st.button(
                        f"{logo}\n\n{display_name}",
                        key=f"biome_select_{ecosystem_key}",
                        use_container_width=True
                ):
                    # Set the ecosystem type (same as sidebar selection)
                    self.ecosystem_type = ecosystem_key
                    model_class = self.ECOSYSTEM_MODELS[ecosystem_key]
                    self.model_class = model_class()
                    self.ecosystem_display_name = self.ECOSYSTEM_DISPLAY_NAMES[ecosystem_key]
                    selection_made = True
                    st.rerun()

        # Show current selection
        if self.ecosystem_type:
            st.success(f"✅ **Selected Ecosystem:** {self.ecosystem_display_name}")
        else:
            st.info("👆 **Please select a biome above to continue**")

        return selection_made

    def initialize_status(self):
        """
        Initializes the application state with default values.

        This method sets up the session state variables required for the application to function
        correctly. It ensures that all necessary session state variables are initialized and
        available with default values if they do not already exist.

        Session state variables initialized include:

        - ``extracted_values``: Dictionary to store extracted data.
        - ``extraction_done``: Boolean indicating whether data extraction has been completed.
        - ``lat_input``: Latitude input field value, initialized from the class attribute ``lat``.
        - ``lon_input``: Longitude input field value, initialized from the class attribute ``lon``.
        - ``area_input``: Area input field value, initialized from the class attribute ``area``.
        - ``saved_polygon``: Polygon data, if saved.
        - ``polygon_centroid``: Centroid of the polygon, if calculated.
        - ``active_location_tab``: Active tab selection for location input, defaults to "manual".

        :no parameters:

        :return: None
        """
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


    def tab_layout(self):
        """
        Applies custom CSS styling to the tab layout in a Streamlit application. This function modifies
        the appearance of tabs and their container to enhance aesthetics, including background colors,
        borders, dimensions, and aligning active tabs with content areas.

        :return: None
        """
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
        """
        Handles the manual input of coordinates and area-related data using a user interface.
        Allows toggling between manual input and polygon input modes, displays appropriate
        notifications based on the current mode, and provides UI components for manual input.

        :param self: Instance parameter for accessing attributes and methods.

        :return: None
        """
        if st.button("🔄 Use Manual Input", key="use_manual_input", help="Click to use manual coordinates"):
            st.session_state.active_location_tab = "manual"
            self.lat = st.session_state.lat_input
            self.lon = st.session_state.lon_input
            self.area = st.session_state.area_input
            circle = Spatial.create_circle_from_area(self.lon, self.lat, self.area)
            self.aoi_gdf = gpd.GeoDataFrame([1], geometry=[circle], crs='EPSG:4326')

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
        """
        Shows a preview map centered around the given manually entered coordinates.

        A folium map is generated with the provided latitude and longitude values.
        The map includes a marker at the specified location, showing detailed
        coordinates in the popup. The map is displayed with a fixed zoom level and
        specific styling.

        :param self: Instance of the class calling this method. Specifically
                     uses `self.lat` and `self.lon` as the coordinates for the map.
        """
        preview_map = folium.Map(location=[self.lat, self.lon], zoom_start=2)
        folium.Marker(
            location=[self.lat, self.lon],
            popup=f"Location: {self.lat:.6f}, {self.lon:.6f}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(preview_map)
        st_folium(preview_map, key="preview_map", height=700, use_container_width=True)

    def polygon_info(self):
        """
        Provides functionality to fetch and display information about a polygon, including its
        centroid coordinates and estimated area, and interact with user actions such as using
        polygon input mode or clearing polygon data.

        :Parameters:
            None directly, method leverages and modifies `st.session_state` for interacting
            with Streamlit widgets and user interface elements.

        :Raises:
            None

        :Returns:
            None
        """
        if st.button("🔄 Use Polygon Input", key="use_polygon_input", help="Click to use polygon coordinates"):
            try:
                st.session_state.active_location_tab = "polygon"
                self.lat = st.session_state.polygon_centroid[0]
                self.lon = st.session_state.polygon_centroid[1]
                self.area = st.session_state.polygon_area
                self.aoi_gdf = gpd.GeoDataFrame([1], geometry=[self.drawn_polygon], crs='EPSG:4326')
                st.rerun()
            except TypeError:
                st.session_state.active_location_tab = "manual"
                st.error("Please draw a valid polygon first!")

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
        """
        Draws an interactive map using the Folium library and Streamlit interface to facilitate
        geospatial operations such as drawing polygons and calculating associated properties.

        This method creates a map centered around specified coordinates and overlays saved polygons,
        along with their centroid markers if available within the session state. It offers interactive
        drawing functionality for adding new geometric shapes (polygons or rectangles) to the map.

        The interactive tools allow users to draw or modify geometric shapes directly on the map while
        capturing relevant geometric data such as the shape's centroid and its geodesic area.

        :param self: Reference to the current instance of the object.

        :return: None
        """
        map_center = [self.lat , self.lon]
        m = folium.Map(location=map_center, zoom_start=2)

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
        map_data = st_folium(m, key="polygon_map", height=700, use_container_width=True)

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
                self.drawn_polygon = shapely_polygon

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
            location_text = f"Location: {county}, {country}"
        elif country:
            location_text = f"Location: {country}"
        st.subheader(f"Project Details")
        st.markdown(f"Biome: {self.ecosystem_display_name}")
        st.markdown(location_text)

        # Optionally show coordinates
        if self.lat != 0.0 or self.lon != 0.0:
            st.markdown(f"Coordinates: {self.lat:.6f}, {self.lon:.6f}")
            st.markdown(f"Project Area (hectares): {self.area:,.0f}")

    def ecosystem_services_menu(self):
        if hasattr(self.model_class, 'ECOSYSTEM_SERVICES'):
            cols = st.columns(2)
            for i, pvar_obj in enumerate(self.model_class.ECOSYSTEM_SERVICES):
                display_name = pvar_obj.variable.name

                var_key = pvar_obj.variable.name

                with cols[i % 2]:
                    pvar_obj.value = st.checkbox(
                        display_name,
                        key=f"proj_{var_key}_{self.ecosystem_type}",
                        help=pvar_obj.variable.get_tooltip()
                    )
        if hasattr(self.model_class, 'SIIKAMAKI'):
            cols = st.columns(2)
            for i, pvar_obj in enumerate(self.model_class.SIIKAMAKI):
                display_name = pvar_obj.full_name
                var_key = pvar_obj.name

                with cols[i % 2]:
                    self.siikamaki_layers[var_key] = st.checkbox(
                        display_name,
                        key=f"proj_{var_key}_{self.ecosystem_type}"
                    )


    def sub_biomes_menu(self):
        if hasattr(self.model_class, 'SUB_BIOMES') and self.model_class.SUB_BIOMES:
            # Create a list of options with display names
            options = []
            for pvar_obj in self.model_class.SUB_BIOMES:
                display_name = pvar_obj.variable.full_name
                var_key = pvar_obj.variable.name
                options.append((var_key, display_name, pvar_obj))

            # Create radio button selection
            try:
                help_texts = [p.variable.get_tooltip() for p in self.model_class.SUB_BIOMES]
            except AttributeError:
                help_texts = ['']
            selected_option = st.radio(
                "Select Sub-biome:",
                options=[opt[1] for opt in options],  # Display names
                key=f"sub_biome_{self.ecosystem_type}",
                help="Choose the sub-biome that best describes your study area"+ "\n\n".join(help_texts)
            )

            # Clear all sub_biomes first
            for x, y, pvar_obj in options:
                pvar_obj.value = 0

            # Set only the selected one to True
            if selected_option:
                # Find the var_key for the selected display name
                selected_var_obj = next(pvar_obj for var_key, display_name, pvar_obj in options if display_name == selected_option)
                selected_var_obj.value = 1
        else:
            st.info("No sub-biomes available for this ecosystem type.")

    def cost_variables_menu(self):
        if hasattr(self.model_class, 'GLOBAL_LAYERS'):
            cols = st.columns(2)
            for i, pvar_obj in enumerate(self.model_class.GLOBAL_LAYERS):
                display_name = pvar_obj.full_name
                var_key = pvar_obj.name

                with cols[i % 2]:
                    self.cost_layers[var_key] = st.checkbox(
                        display_name,
                        key=f"cost_{var_key}_{self.ecosystem_type}"
                    )
        else:
            st.info("Please select a biome first")


    def model_variables_menu(self):
        if hasattr(self.model_class, 'VARIABLES'):


            for var_obj in self.model_class.VARIABLES:

                # Get the form field key
                if var_obj.lc is not None:
                    display_name = var_obj.lc.full_name
                    var_key = var_obj.lc.get_name(var_obj.buffer)
                    tool_tip = var_obj.variable.get_tooltip()
                else:
                    display_name = var_obj.variable.full_name
                    tool_tip = var_obj.variable.get_tooltip()
                    var_key = var_obj.variable.name
                print(var_key)
                default_value = 0.0
                session_key = f"var_{var_key}_{self.ecosystem_type}"

                # Initialize session state if not exists
                if session_key not in st.session_state:
                    st.session_state[session_key] = default_value

                if (st.session_state.get('extraction_done', False) and
                        st.session_state.get('update_from_extraction', False) and
                        var_key in st.session_state.get('extracted_values', {})):
                    try:
                        st.session_state[session_key] = float(st.session_state.extracted_values[var_key])
                    except (ValueError, TypeError):
                        pass

                var_obj.value = st.number_input(
                    f"{display_name}",
                    #value=st.session_state[session_key],
                    step=0.01,
                    format="%.2f",
                    help=tool_tip if tool_tip else None,
                    key=session_key
                )

            if st.button("🔄 Extract Spatial Values from GEE", type="primary",
                         use_container_width=True):
                if not st.session_state.get('gee_initialized', 0):
                    st.error("Please initialize Google Earth Engine first")
                else:
                    with st.spinner(
                            f"Extracting values from Google Earth Engine for {self.lat:.6f}, {self.lon:.6f} {self.area}... "):
                        extracted_values, error = St_Utils.extract_values(self.model_class, self.lat, self.lon,
                                                                          self.area)
                        print(extracted_values)
                        if error:
                            st.error(f"Extraction failed: {error}")
                        else:
                            # Store extracted values and set update flag
                            st.session_state.extracted_values = extracted_values
                            st.session_state.extraction_done = True
                            st.session_state.update_from_extraction = True  # Flag to trigger updates
                            st.success(f"✅ Extracted {len(extracted_values)} variables")
                            st.rerun()

            # Reset the update flag after one cycle (add this at the end of the widget creation loop)
            if st.session_state.get('update_from_extraction', False):
                st.session_state.update_from_extraction = False

            # Show extraction status
            if st.session_state.extraction_done and st.session_state.extracted_values:
                st.info(f"✅ Using extracted values from GEE ({len(st.session_state.extracted_values)} variables)")
        else:
            st.info("Please select a biome first")

    def calculate_benefit(self):
        if st.button("Calculate Benefits", type="primary", use_container_width=True):
            # Validate inputs
            if not all([self.lat != 0 or self.lon != 0, self.area > 0]):
                st.error("Please provide valid latitude, longitude, and area values")
            if not any(item.value for item in self.model_class.ECOSYSTEM_SERVICES):
                st.error("Please select at least one ecosystem service")

            else:
                # Calculate ecosystem value
                prediction_sets = {}
                for vt in self.model_class.VALUE_TYPES:
                    vt.value = 1.0
                    predicted_values = {}
                    ess = [es for es in self.model_class.ECOSYSTEM_SERVICES if es.value]

                    for es in ess:
                        predicted_value = Predict.predict_benefit(self.model_class, es, vt, self.area)
                        predicted_values[es.variable.name] = predicted_value
                    prediction_sets[vt.variable.full_name] = predicted_values
                st.success("✅ Calculation Complete!")
                siikamaki_benefits = None
                if hasattr(self.model_class, 'SIIKAMAKI'):
                    siikamaki_benefits = self.calculate_siikamaki()
                return prediction_sets, siikamaki_benefits
        else:
            return None, None

    def calculate_costs(self):
        if st.button("Calculate Costs", type="primary", use_container_width=True):
            # Validate inputs
            if not all([self.lat != 0 or self.lon != 0, self.area > 0]):
                st.error("Please provide valid latitude, longitude, and area values")

            cost_layers = []
            for pvar_obj in self.model_class.GLOBAL_LAYERS:
                var_key = pvar_obj.name
                is_selected = self.cost_layers.get(var_key, 0)
                if is_selected:
                    cost_layers.append(pvar_obj)

            cost_per_ha = St_Utils.extract_global_layers(cost_layers, self.lat, self.lon, self.area)

            return cost_per_ha
        else:
            return None

    def calculate_siikamaki(self):
        print('run siikamaki')
        # Validate inputs
        if self.aoi_gdf is not None:

            siikamaki_layers = []
            for pvar_obj in self.model_class.SIIKAMAKI:
                var_key = pvar_obj.name
                is_selected = self.siikamaki_layers.get(var_key, 0)
                if is_selected:
                    siikamaki_layers.append(pvar_obj)

            values_per_ha = St_Utils.extract_global_layer_with_polygon(siikamaki_layers, self.aoi_gdf)

            return values_per_ha
        else:
            return None


    def display_benefits(self, predicted_sets, siikamaki_benefits=None):
        # Display results
        tab_names = [t.variable.full_name for t in self.model_class.VALUE_TYPES]

        tabs = st.tabs(tab_names)
        for i, (tab_name, tab) in enumerate(zip(tab_names, tabs)):
            with tab:
                value_type = self.model_class.VALUE_TYPES[i]
                st.info(f"{value_type.variable.get_tooltip()}")
                cols = st.columns(2)
                predicted_values = predicted_sets[tab_name]

                if siikamaki_benefits is not None:
                    for benefit in siikamaki_benefits:
                        predicted_values.update(benefit)
                total_value = 0.0
                for j, key in enumerate(predicted_values):
                    with cols[j % 2]:
                        st.metric(
                            label=key,
                            value=f"${predicted_values[key]:,.2f} per ha",
                            help="USD per hectare per year"
                        )
                    total_value += predicted_values[key]
                st.markdown(f"<h3 style='text-align: right;'>Total Value per ha: ${total_value:,.2f}</h3>",
                            unsafe_allow_html=True)

    def display_costs(self, cost_per_ha):
        tv = 0
        for cost in cost_per_ha:
            try:
                k = [k for k, v in cost.items()][0]
                v = [v for k, v in cost.items()][0]
                st.metric(
                    label=k,
                    value = f"${v:,.2f}",
                    help = "USD per hectare"
                )
                tv += v
            except TypeError:
                k = [k for k, v in cost.items()][0]
                v = [v for k, v in cost.items()][0]
                st.metric(
                    label=k,
                    value=f"No cost data available for location"
                )
        return tv

    @staticmethod
    def clear_display_data():
        if 'displayed_benefits' in st.session_state:
            del st.session_state.displayed_benefits
        if 'benefits_data' in st.session_state:
            del st.session_state.benefits_data
        if 'displayed_costs' in st.session_state:
            del st.session_state.displayed_costs
        if 'costs_data' in st.session_state:
            del st.session_state.costs_data


def main():
    from src.app_utils.css import CSS
    import base64
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
    </style>
    """, unsafe_allow_html=True)

    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

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
        st.session_state.app.connect_to_google()
        st.session_state.instantiated = True


    # --------------------------------------------------- Main Page --------------------------------------------------#
    img_base64 = get_base64_image("src/images/NBS_GFDRR_Admin_WBG_2.avif")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("Ecosystem Valuation Tool")
    with col2:
        st.markdown("""
            <style>
            .bottom-align {
                display: flex;
                align-items: flex-end;
                height: 100%;
            }
            </style>
            """, unsafe_allow_html=True)

        st.markdown('<div class="bottom-align">', unsafe_allow_html=True)
        st.markdown(f"""
            <a href="https://www.naturebasedsolutions.org/" target="_blank">
                <img src="data:image/avif;base64,{img_base64}" width="1000" alt="Logo">
            </a>
            """, unsafe_allow_html=True)

        #st.image("src/images/NBS_GFDRR_Admin_WBG_2.avif")
        st.markdown('</div>', unsafe_allow_html=True)


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
    st.markdown(f"<style>{CSS.LOCATION}</style>", unsafe_allow_html=True)
    st.markdown(f"<style>{CSS.SPATIAL_VARIABLES}</style>", unsafe_allow_html=True)
    st.markdown(f"<style>{CSS.BENEFIT}</style>", unsafe_allow_html=True)
    st.markdown(f"<style>{CSS.COST}</style>", unsafe_allow_html=True)
    st.markdown(f"<style>{CSS.ESS}</style>", unsafe_allow_html=True)
    st.markdown(CSS.HIDE_ANCHOR_CSS, unsafe_allow_html=True)

    # define the ecosystem based on choice made in the side bar
    # ----------------- Sub Biomes ----------------- #
    with st.container(key='ess'):
        st.header('Select Biome')
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader('Biome selection')
            st.markdown("""
            NBS costs and benefits are estimated based on biome specific value transfer functions.
            To make sure you get the most accurate estimation for your study area, please select the biome that best
            represents your study area.""")
            st.session_state.app.biome_selection_boxes()

        with col2:
            st.subheader('Sub Category')
            st.markdown("""
            Please select the relevant sub biome below
            """)
            st.session_state.app.sub_biomes_menu()

    st.markdown("")
    # -------------------- Tabs -------------------- #
    col_loc, col_values = st.columns([2, 1])

    # create the tab layout
    with col_loc:
        with st.container(key='location'):
            st.header('Project Location')
            st.session_state.app.tab_layout()
            tab_manual, tab_polygon = st.tabs(["📍 Enter Manually", "🗺️ Draw Polygon"])

            with tab_manual:
                col_params_man, col_map_man= st.columns([1, 2])
                with col_params_man:
                    st.session_state.app.manual_input()
                    st.session_state.app.location_info()
                with col_map_man:
                    st.session_state.app.preview_map()


            with tab_polygon:
                col_params_pol, col_map_pol = st.columns([1, 2])
                with col_params_pol:
                    st.session_state.app.polygon_info()
                    st.session_state.app.location_info()
                with col_map_pol:
                    st.session_state.app.draw_map()

    with col_values:
        with st.container(key='spatial_variables'):
            st.header('Spatial Predictor Variables')
            st.session_state.app.model_variables_menu()

    st.markdown("")
    # -------------------- Benefits -------------------- #
    with st.container(key='benefits'):
        st.header('Ecosystem Benefits')
        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Ecosystem Services")
            st.markdown("""
            Select which ecosystem services you want to include in the benefit assessment.
            """)
            st.session_state.app.ecosystem_services_menu()
            prediction_sets, siikamaki_benefits = st.session_state.app.calculate_benefit()



        with col2:
            st.subheader("Benefit Estimates")
            st.markdown("""
                        Benefits are expressed in Current USD per hectare per year. Estimateions were done using meta regressions
                        base don es-valuation studies using ESVD data (Brander et al., 2025) and a recent meta regression model. for forest ecosystem 
                        services (Siikamaki et al., 2024)
                        """)
            if prediction_sets:
                st.session_state.displayed_benefits = True
                st.session_state.benefits_data = prediction_sets
            if st.session_state.get('displayed_benefits', False):
                st.session_state.app.display_benefits(st.session_state.benefits_data, siikamaki_benefits)

    # -------------------- Costs -------------------- #
    with st.container(key='costs'):
        st.header('Intervention Costs')
        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Type of Cost")

            st.markdown("""Select which costs you want to include in the cost assessment.""")
            st.session_state.app.cost_variables_menu()
            cost_per_ha = st.session_state.app.calculate_costs()

        with col2:
            st.subheader("Cost Estimates")

            if cost_per_ha:
                st.session_state.displayed_costs = True
                st.session_state.costs_data = cost_per_ha

            # Always display if we have costs data
            if st.session_state.get('displayed_costs', False):
                st.session_state.app.display_costs(st.session_state.costs_data)


if __name__ == "__main__":
    main()