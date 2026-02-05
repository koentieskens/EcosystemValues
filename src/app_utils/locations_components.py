import streamlit as st

import math
import folium
import geopandas as gpd

from streamlit_folium import st_folium
from shapely.geometry import Polygon, Point
from src.app_utils.utils import St_Utils
from src.app_utils.session_states import SessionStateManager as ssm

class LocationManager:

    def polygon_info(self):

        st.subheader("Polygon Input")
        if st.button("Activate Polygon Input", key="activate_polygon", help="Click to activate polygon"):
            self._activate_polygon()

        # Show which mode is active
        if ssm.LOCATION_ACTIVATED.get():
            if ssm.LOCATION_TYPE.get() == 'polygon':
                st.success("✅ **Polygon input is active**")
            elif ssm.LOCATION_TYPE.get() == 'manual':
                st.warning("""Currently using manual location input values.
                If you want to use a polygon to define the location,
                use the drawing tools on the map to draw an area of interest and activate it.
                """)
        else:
            st.warning("Use the drawing tools on the map to draw an area of interest and activate it!")

        st.subheader("Manual Input")
        lat = st.number_input("Latitude", value=ssm.MANUAL_CENTROID.get()[0])
        lon = st.number_input("Longitude", value=ssm.MANUAL_CENTROID.get()[1])
        area = st.number_input("Area (hectares)", value=ssm.MANUAL_AREA.get())
        ssm.MANUAL_CENTROID.set((lat, lon))
        ssm.MANUAL_AREA.set(area)
        ssm.TEMP_MANUAL_POLYGON.set(self.create_circle_gdf(lat, lon, area)[1])

        if st.button("Activate Manual Input", key="activate_manual_input", help="Click to activate manual input"):
            self._activate_manual_input()

        if ssm.LOCATION_ACTIVATED.get():
            if ssm.LOCATION_TYPE.get() == 'manual':
                st.success("✅ **Manual input is active**")
            elif ssm.LOCATION_TYPE.get() == 'polygon':
                st.warning("""Currently using map location input values.
                If you want to use manual latitude, longitude and area inputs to define the location,
                provide them here and activate manual input.
                """)
        else:
            st.warning("Provide latitude, longitude, and area values and activate.")


        if st.session_state.saved_polygon is not None:
            self.clear_location()

    def clear_location(self):
        if st.button("🗑️ Clear Location", key="clear_location"):
            ssm.SAVED_POLYGON.set(None)
            ssm.POLYGON_CENTROID.set(None)
            ssm.LOCATION_ACTIVATED.set(False)
            ssm.BENEFITS_UPDATED.reset()
            ssm.BENEFITS_EXTRACTION_DONE.reset()
            ssm.COST_EXTRACTED_VALUES.reset()
            ssm.BENEFITS_EXTRACTED_VALUES.reset()
            ssm.COST_EXTRACTION_DONE.reset()
            ssm.COST_DATA.reset()
            ssm.DISPLAYED_COST.reset()
            ssm.DISPLAYED_BENEFITS.reset()
            ssm.COST_UPDATED.reset()
            ssm.COST_UPDATE_FROM_EXTRACTION.reset()
            ssm.SAVED_REGION.reset()
            ssm.SAVED_COUNTRY.reset()
            st.success("AOI cleared!")
            st.rerun()

    def create_circle_gdf(self, lat, lon, area):
        center_point = Point(lon, lat)
        gdf_point = gpd.GeoDataFrame([1], geometry=[center_point], crs='EPSG:4326')

        # Project to a suitable UTM zone or use Web Mercator for approximate calculations
        gdf_projected = gdf_point.to_crs('EPSG:3857')  # Web Mercator

        # Create circle with exact radius in meters
        radius = math.sqrt((area * 10000) / math.pi)
        circle_projected = gdf_projected.geometry[0].buffer(radius)

        # Create GeoDataFrame with the circle
        gdf_circle_projected = gpd.GeoDataFrame([1], geometry=[circle_projected], crs='EPSG:3857')

        # Convert back to WGS84 if needed
        gdf_circle = gdf_circle_projected.to_crs('EPSG:4326')
        circle_polygon = gdf_circle.geometry[0]
        locations = [[lat, lon] for lon, lat in circle_polygon.exterior.coords]

        return gdf_circle, locations

    def should_update_map(self):
        # Define what parameters affect the map
        current_state = {
            'coordinates': ssm.PROJECT_LOCATION.get(),
            'polygon_data': st.session_state.get('polygon_data', None),
            'zoom_level': st.session_state.get('zoom_level', None),
            'selected_location': st.session_state.get('selected_location', None),
            # Add other location-related session state keys
        }

        # Compare with last known state
        if not hasattr(self, '_last_map_state'):
            self._last_map_state = current_state
            return True

        if self._last_map_state != current_state:
            self._last_map_state = current_state
            return True

        return False

    def _activate_polygon(self):

        try:
            ssm.LOCATION_ACTIVATED.set(True)
            ssm.LOCATION_TYPE.set('polygon')
            centroid = ssm.DRAWN_POLYGON.get().centroid
            ssm.POLYGON_CENTROID.set((centroid.y, centroid.x))
            ssm.PROJECT_LOCATION.set({'lat': ssm.POLYGON_CENTROID.get()[0], 'lon': ssm.POLYGON_CENTROID.get()[1], 'area':ssm.POLYGON_AREA.get()})
            ssm.SAVED_POLYGON.set(ssm.UNSAVED_POLYGON.get())
            ssm.AOI_GDF.set(gpd.GeoDataFrame([1], geometry=[ssm.DRAWN_POLYGON.get()], crs='EPSG:4326'))
            ssm.ZOOM_LEVEL.set(10)
            county, country = St_Utils.get_location_info(ssm.PROJECT_LOCATION.get()['lat'],
                                                         ssm.PROJECT_LOCATION.get()['lon'])
            ssm.SAVED_COUNTRY.set(country)
            ssm.SAVED_REGION.set(county)
            st.rerun()
        except TypeError:
            ssm.LOCATION_ACTIVATED.set(False)
            st.error("Please draw a valid polygon first!")

    def _activate_manual_input(self):

        try:
            ssm.LOCATION_ACTIVATED.set(True)
            ssm.LOCATION_TYPE.set('manual')
            ssm.PROJECT_LOCATION.set({'lat': ssm.MANUAL_CENTROID.get()[0], 'lon': ssm.MANUAL_CENTROID.get()[1], 'area':ssm.MANUAL_AREA.get()})
            ssm.POLYGON_CENTROID.set(ssm.MANUAL_CENTROID.get())
            ssm.SAVED_POLYGON.set(ssm.TEMP_MANUAL_POLYGON.get())
            gdf = self.create_circle_gdf(ssm.MANUAL_CENTROID.get()[0], ssm.MANUAL_CENTROID.get()[1], ssm.MANUAL_AREA.get())[0]
            ssm.AOI_GDF.set(gdf)
            ssm.ZOOM_LEVEL.set(10)
            county, country = St_Utils.get_location_info(ssm.PROJECT_LOCATION.get()['lat'],
                                                         ssm.PROJECT_LOCATION.get()['lon'])
            ssm.SAVED_COUNTRY.set(country)
            ssm.SAVED_REGION.set(county)
            st.rerun()
        except TypeError:
            ssm.LOCATION_ACTIVATED.set(False)
            st.error("Please provide valid latitude, longitude, and area values first!")

    def draw_map(self):

        map_center = [ssm.PROJECT_LOCATION.get()['lat'] , ssm.PROJECT_LOCATION.get()['lon']]

        m = folium.Map(location=map_center,
                       zoom_start=ssm.ZOOM_LEVEL.get(),
                       tiles='cartodbpositron',
                       world_copy_jump=True,  # This helps with coordinate wrapping
                       no_wrap=False)  # Allow coordinate wrapping


        self._show_saved_polygon(m)
        # Add drawing functionality
        self._add_drawing_tools(m)

        # Display the map and capture drawing events
        map_data = st_folium(m, key="polygon_map", height=700, use_container_width=True)

        # Process drawn polygons
        if map_data['all_drawings'] and len(map_data['all_drawings']) > 0:
            # Get the last drawn polygon
            last_drawing = map_data['all_drawings'][-1]

            if last_drawing['geometry']['type'] in ['Polygon', 'Rectangle']:
                # Extract coordinates
                self._save_drawing(last_drawing)

    @ssm.SAVED_POLYGON.skip_if_none()
    def _show_saved_polygon(self, m):

        folium.Polygon(
            locations=ssm.SAVED_POLYGON.get(),
            color='blue',
            weight=2,
            fill=True,
            fillColor='lightsalmon',
            fillOpacity=0.3,
            popup="Saved Polygon"
        ).add_to(m)

        # Add centroid marker
        folium.Marker(
            location=[ssm.PROJECT_LOCATION.get()['lat'], ssm.PROJECT_LOCATION.get()['lon']],
            icon=folium.Icon(color='red', icon='star')
        ).add_to(m)

    @ssm.SAVED_POLYGON.skip_if_none()
    def _show_manual_polygon(self, m):

        folium.Polygon(
            locations=ssm.MANUAL_POLYGON.get(),
            color='blue',
            weight=2,
            fill=True,
            fillColor='lightsalmon',
            fillOpacity=0.3,
            popup="Saved Polygon"
        ).add_to(m)

        # Add centroid marker
        folium.Marker(
            location=[ssm.PROJECT_LOCATION.get()['lat'], ssm.PROJECT_LOCATION.get()['lon']],
            icon=folium.Icon(color='red', icon='star')
        ).add_to(m)

    def _add_drawing_tools(self, m):
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

    def _save_drawing(self, last_drawing):


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
        ssm.POLYGON_CENTROID.set((centroid.y, centroid.x))
        ssm.UNSAVED_POLYGON.set(folium_coords)
        ssm.POLYGON_AREA.set(area)
        ssm.DRAWN_POLYGON.set(shapely_polygon)

    def location_info(self):

        # Get location information based on coordinates
        if ssm.LOCATION_ACTIVATED.get():

            county, country = St_Utils.get_location_info(ssm.PROJECT_LOCATION.get()['lat'], ssm.PROJECT_LOCATION.get()['lon'])
            ssm.SAVED_COUNTRY.set(country)
            ssm.SAVED_REGION.set(county)

            # Display location information
            location_text = ""
            if county and country:
                location_text = f"**Location**: {county} | {country}"
            elif country:
                location_text = f"**Location**: {country}"
            st.subheader(f"Project Details")
            st.write(location_text)
            lat = ssm.PROJECT_LOCATION.get()['lat']
            lon = ssm.PROJECT_LOCATION.get()['lon']
            area = ssm.PROJECT_LOCATION.get()['area']
            st.write(f"**Latitude:** {lat:.6f}")
            st.write(f"**Longitude:** {lon:.6f}")
            biome = ssm.ECOSYSTEM_DISPLAY_NAME.get() or 'No Biome selected yet'
            st.write(f"**Biome**: {biome}")
            st.write(f"**Estimated Area:** {area:,.2f} hectares")

def main():
    st.set_page_config(
        page_title="Ecosystem Valuation Tool",
        page_icon="🌱",
        layout="wide"
    )
    ssm.initialize_all()
    lm = LocationManager()
    lm.polygon_info()
    st.markdown("---")
    lm.draw_map()
    lm.location_info()

if __name__ == "__main__":
    main()