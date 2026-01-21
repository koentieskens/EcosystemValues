import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely.geometry import Polygon
from src.app_utils.utils import St_Utils

class LocationManager:
    def __init__(self):
        self.initialize_values()

    def initialize_values(self):
        ss = st.session_state

        states = [
            'location_activated',
            'polygon_centroid',
            'saved_polygon',
            'polygon_area',
            'drawn_polygon',
            'aoi_gdf',
            'unsaved_polygon'
        ]
        for state in states:
            if state not in ss:
                setattr(ss, state, None)

        if 'zoom_level' not in ss:
            ss.zoom_level = 2
        if 'lat' not in ss:
            ss.lat = 40
        if 'lon' not in ss:
            ss.lon = 10
        if 'area' not in ss:
            ss.area = 1

    def polygon_info(self):

        ss = st.session_state
        if st.button("Activate Polygon Input", key="activate_polygon", help="Click to activate polygon"):
            self._activate_polygon()

        # Show which mode is active
        if ss.get('location_activated', False):
            st.success("✅ **Polygon input is active**")
        else:
            st.warning("⚠️ Activate a valid Polygon first!")

        # Button to clear polygon
        if st.session_state.saved_polygon is not None:
            if st.button("🗑️ Clear Polygon", key="clear_poly"):
                ss.saved_polygon = None
                ss.polygon_centroid = None
                ss.location_activated = False
                st.success("Polygon cleared!")
                st.rerun()

    def _activate_polygon(self):
        ss = st.session_state
        try:
            ss.location_activated = True
            ss.lat = ss.polygon_centroid[0]
            ss.lon = ss.polygon_centroid[1]
            ss.area = ss.polygon_area
            ss.saved_polygon = ss.unsaved_polygon
            ss.aoi_gdf = gpd.GeoDataFrame([1], geometry=[ss.drawn_polygon], crs='EPSG:4326')
            ss.zoom_level = 11
            st.rerun()
        except TypeError:
            st.location_activated = False
            st.error("Please draw a valid polygon first!")

    def draw_map(self):
        ss = st.session_state
        map_center = [ss.lat , ss.lon]

        m = folium.Map(location=map_center, zoom_start=ss.zoom_level, tiles='cartodbpositron')

        # Add saved polygon if it exists
        if ss.saved_polygon is not None:
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

    def _show_saved_polygon(self, m):
        ss = st.session_state
        folium.Polygon(
            locations=ss.saved_polygon,
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
                popup=f"Centroid: {ss.polygon_centroid[0]:.6f}, {ss.polygon_centroid[1]:.6f}",
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
        ss = st.session_state

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
        ss.polygon_centroid = [centroid.y, centroid.x]
        ss.unsaved_polygon = folium_coords
        ss.polygon_area = area
        ss.drawn_polygon = shapely_polygon

    def location_info(self):
        ss = st.session_state
        # Get location information based on coordinates
        if ss.get('location_activated', False):

            county, country = St_Utils.get_location_info(ss.lat, ss.lon)

            # Display location information
            location_text = ""
            if county and country:
                location_text = f"**Location**: {county} | {country}"
            elif country:
                location_text = f"**Location**: {country}"
            st.subheader(f"Project Details")
            st.write(location_text)
            lat = ss.polygon_centroid[0]
            lon = ss.polygon_centroid[1]
            area = ss.polygon_area
            st.write(f"**Latitude:** {lat:.6f}")
            st.write(f"**Longitude:** {lon:.6f}")
            biome = ss.get('ecosystem_display_name') or 'No Biome selected yet'
            st.write(f"**Biome**: {biome}")
            st.write(f"**Estimated Area:** {area:,.2f} hectares")

def main():
    st.set_page_config(
        page_title="Ecosystem Valuation Tool",
        page_icon="🌱",
        layout="wide"
    )
    lm = LocationManager()
    lm.polygon_info()
    st.markdown("---")
    lm.draw_map()
    lm.location_info()

if __name__ == "__main__":
    main()