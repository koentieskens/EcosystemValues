import streamlit as st
import math
import reverse_geocode
from iso3166 import countries
from shapely.geometry import Polygon
from pyproj import CRS, Transformer, Geod
from ..extract_data.predictions import Predictions
from ..utils.spatial import Spatial


class St_Utils:
    """Streamlit utility functions"""

    @staticmethod
    def get_variable_display_info(var_obj):
        """Extract display information from a variable object"""
        try:
            if hasattr(var_obj, 'lc') and var_obj.lc is not None:
                return var_obj.lc.value[2], var_obj.lc.value[2]

            variable_enum = var_obj.variable
            if hasattr(variable_enum.value, 'description'):
                name = variable_enum.value.description
                tooltip = variable_enum.value.description
            else:
                name = str(variable_enum.value).replace('_', ' ').title()
                tooltip = name

            return name, tooltip
        except Exception as e:
            return str(var_obj.variable).replace('_', ' ').title(), ""

    @staticmethod
    def get_project_variable_display_info(project_var_obj):
        """Extract display information from a project variable object"""
        try:
            var_enum = project_var_obj.variable
            if hasattr(var_enum.value, '__len__') and len(var_enum.value) >= 2:
                return var_enum.value[1]
            else:
                return str(var_enum.value).replace('_', ' ').title()
        except:
            return "Unknown Variable"

    @staticmethod
    def extract_values(model_class, lat, lon, area_hectares):
        """Extract values using the Predictions class"""
        try:
            # Calculate radius from area (assuming perfect circle)
            area_m2 = area_hectares * 10000
            radius = math.sqrt(area_m2 / math.pi)

            # Create list of variables from the current model
            variables = model_class.VARIABLES

            # Create Predictions instance and extract values
            p = Predictions(variables, lat, lon, radius=int(radius))
            p.get_values()

            return p.values_dict, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def extract_global_layers(cost_layers, lat, lon, area_hectares):
        l = []
        for layer in cost_layers:
            bucket = layer.bucket
            gcs_loc = layer.gcs_path
            gcs_path = f"gs://{bucket}/{gcs_loc}"
            value = Spatial.get_value_from_cog(gcs_path, lon, lat, area_hectares, band=layer.band)
            d = {layer.full_name:  value}
            l.append(d)

        return l

    @staticmethod
    def extract_global_layer_with_polygon(layers, polygon_gdf):
        l = []
        for layer in layers:
            bucket = layer.bucket
            gcs_loc = layer.gcs_path
            gcs_path = f"gs://{bucket}/{gcs_loc}"
            value = Spatial.get_value_from_cog_with_polygon(gcs_path, polygon_gdf, band=layer.band)
            d = {layer.full_name: value}
            l.append(d)
        return l

    @staticmethod
    def get_location_info(lat, lon):
        """Get county and country information from coordinates"""
        try:
            # to start the app with no location
            if lat == 0.0 and lon == 0.0:
                return "", ""

            # Get location data
            location_data = reverse_geocode.get((lat, lon))

            # Get county/city (using city as county equivalent)
            county = location_data.get('county', '')

            # Get country name
            country_code = location_data.get('country_code', '')
            if country_code:
                country_obj = countries.get(country_code)
                country = country_obj.name if country_obj else country_code
            else:
                country = ''

            return county, country
        except Exception as e:
            return "", ""


    @staticmethod
    def get_geodesic_area(polygon: Polygon):

        g = Geod(ellps='WGS84')
        geod_area = abs(g.geometry_area_perimeter(polygon)[0])

        return geod_area / 10000




