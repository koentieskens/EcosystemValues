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
    def extract_global_layers(cost_layers, lat=0.0, lon=0.0, area=1.0):
        l = []
        for layer in cost_layers:
            bucket = layer.bucket
            gcs_loc = layer.gcs_path
            gcs_path = f"gs://{bucket}/{gcs_loc}"
            value = Spatial.get_value_from_cog(gcs_path, lon, lat, area, band=layer.band)
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
    def extract_global_layer_single(layer, polygon_gdf):
        bucket = layer.bucket
        gcs_loc = layer.gcs_path
        gcs_path = f"gs://{bucket}/{gcs_loc}"
        value = Spatial.get_value_from_cog_with_polygon(gcs_path, polygon_gdf, band=layer.band)
        return value

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

from src.variables.spatial_variable import CountrySpatialVariable
import wbgapi as wb
class CurrencyConverter:

    @staticmethod
    def get_wb_value(var_id: str = None, country: str = 'USA', year: int = 2024):
        df = wb.data.DataFrame(var_id, country, year)
        value = df.loc[country, var_id]
        return value.item()


    @staticmethod
    def get_ppp_conversion_rate(country, year):
        ppp_factor = 'PA.NUS.PPP'
        df = wb.data.DataFrame(ppp_factor, country, year)
        value = df.loc[country, ppp_factor]
        return value.item()

    @staticmethod
    def get_excange_rate(country, year):
        wb_code = 'PA.NUS.FCRF'
        df = wb.data.DataFrame(wb_code, country, year)
        value = df.loc[country, wb_code]
        return value.item()

    @staticmethod
    def get_local_inflation(country, from_year, to_year):
        wb_code = 'FP.CPI.TOTL'
        cpi_data = wb.data.DataFrame(wb_code,
                                     economy=country,
                                     time=[from_year, to_year])
        from_code_col = f'YR{from_year}'
        to_code_col = f'YR{to_year}'
        inflation_rate = cpi_data.loc[country, to_code_col] / cpi_data.loc[country, from_code_col]

        return inflation_rate.item()

    @staticmethod
    def convert_ppp_to_usd(value, country, from_year, to_year):
        # calculate the value in local LCU in from year
        ppp_conv = CurrencyConverter.get_ppp_conversion_rate(country, from_year)
        value_lcu_from = value * ppp_conv

        #apply inflation rate
        inflation_rate = CurrencyConverter.get_local_inflation(country, from_year, to_year)
        value_lcu_to = value_lcu_from * inflation_rate

        #convert to USD
        exchange_rate = CurrencyConverter.get_excange_rate(country, to_year)
        value_usd_to = value_lcu_to / exchange_rate

        return value_usd_to












