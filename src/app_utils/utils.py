import streamlit as st
import math
from shapely.geometry import Polygon, Point
from pyproj import CRS, Transformer, Geod
from ..extract_data.predictions import Predictions
from ..utils.spatial import Spatial
from ..utils import wb360
import geopandas as gpd
from src.variables.global_layers import GlobalVectorLayer
import wbgapi as wb

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
    def extract_value_from_gpkg(gpkg_layer, lat=0.0, lon=0.0):
        """
        Extracts a value from a specified Geopackage layer based on the geographic
        coordinates and computes a derived value (benefit per area) for mangrove areas.

        The method retrieves data from a specific Geopackage layer taht contains mangrove coastal flood protection es
        using bounding box filtering based on the given latitude and longitude. It locates the
        intersecting geometry and computes a per-hectare value from the extracted fields.

        :param gpkg_layer: The Geopackage layer from which the data is to be extracted.
        :param lat: The latitude of the point of interest. Defaults to 0.0.
        :param lon: The longitude of the point of interest. Defaults to 0.0.
        :return: The calculated benefit per hectare value derived from the intersecting data.
        :return type: float
        """
        gpkg_path = gpkg_layer.gcs_path
        layer = gpkg_layer.layer
        buffer = 0.01
        bbox = (lon - buffer, lat - buffer, lon + buffer, lat + buffer)
        gdf = gpd.read_file(gpkg_path, layer=layer, bbox=bbox)
        point = Point(lon, lat)
        intersecting = gdf[gdf.geometry.intersects(point)]
        benefit = intersecting.iloc[0]['Ben_Stock_2020']
        area = intersecting.iloc[0]['Mang_Ha_2020']
        per_ha = benefit / area
        return per_ha.item()

    @staticmethod
    def extract_global_layer_with_polygon(layers, polygon_gdf):
        """
        Extracts a global layer's data intersecting with a specified polygon.

        This method processes a list of layers, retrieves their data from a
        Cloud Optimized GeoTIFF (COG), and intersects the data with a given
        polygon. It creates a result dictionary associating each layer's
        full name with the computed value and returns the aggregated result.

        :param layers: List of layer objects containing bucket, gcs_path, band,
                       and full_name data.
        :type layers: list

        :param polygon_gdf: Geopandas GeoDataFrame representing the polygon
                            geometry used for the intersection.
        :type polygon_gdf: geopandas.GeoDataFrame

        :return: A list of dictionaries where each dictionary maps a layer's
                 full name to its value derived from the intersection with
                 the provided polygon.
        :rtype: list
        """
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
        """
        Extract a numerical value from a cloud-optimized GeoTIFF (COG) file based on
        the provided polygon geometry.

        This method retrieves data from a specific band of a COG file stored in Google
        Cloud Storage. The method uses the polygon geometry to extract targeted spatial
        data from the file.

        :param layer: The layer object containing metadata about the COG file, such as
            the bucket name, path to the COG file in Google Cloud Storage, and band
            to extract values from.
        :param polygon_gdf: A GeoDataFrame containing the polygon geometry used to
            intersect and extract a value from the raster data in the COG file.
        :return: Extracted numerical value corresponding to the polygon geometry
            from the specified band of the COG file.
        :rtype: float
        """
        bucket = layer.bucket
        gcs_loc = layer.gcs_path
        gcs_path = f"gs://{bucket}/{gcs_loc}"
        value = Spatial.get_value_from_cog_with_polygon(gcs_path, polygon_gdf, band=layer.band)
        return value

    @staticmethod
    def get_location_info(lat, lon):
        """Get region, country, ISO2 and ISO3 from WB Admin1 boundaries gpkg.
        Falls back to nearest polygon for ocean locations."""
        if lat == 0.0 and lon == 0.0:
            return "", "", "", ""
        try:
            gpkg_layer = GlobalVectorLayer.WB_ADMIN1_BOUNDARIES
            point = Point(lon, lat)
            buffer = 1.0
            bbox = (lon - buffer, lat - buffer, lon + buffer, lat + buffer)
            gdf = gpd.read_file(gpkg_layer.gcs_path, layer=gpkg_layer.layer, bbox=bbox)
            if gdf.empty:
                return "", "", "", ""
            intersecting = gdf[gdf.geometry.intersects(point)]
            if not intersecting.empty:
                row = intersecting.iloc[0]
            else:
                # Ocean fallback: nearest polygon by geometry distance
                gdf = gdf.copy()
                gdf['_dist'] = gdf.geometry.distance(point)
                row = gdf.loc[gdf['_dist'].idxmin()]
            region = row.get('NAM_1', '') or ''
            country = row.get('NAM_0', '') or ''
            iso2 = row.get('ISO_A2', '') or ''
            iso3 = row.get('ISO_A3', '') or ''
            return region, country, iso2, iso3
        except Exception:
            return "", "", "", ""

    @staticmethod
    def get_geodesic_area(polygon: Polygon):
        """
        Calculates the geodesic area of a given polygon using the WGS84 ellipsoid.

        This method computes the geodesic area by utilizing the geometry described by
        the `Polygon` parameter, which should be defined in geographic coordinates.

        The result is returned in hectares by dividing the computed area by 10,000.

        :param polygon: A `Polygon` object representing the geometry for which the
            geodesic area is to be calculated. The coordinates must be defined in
            latitude and longitude (geographic coordinates).
        :type polygon: Polygon
        :return: The geodesic area of the polygon in hectares.
        :rtype: float
        """
        g = Geod(ellps='WGS84')
        geod_area = abs(g.geometry_area_perimeter(polygon)[0])

        return geod_area / 10000

class CurrencyConverter:
    """
    CurrencyConverter is a utility class that provides methods for currency
    conversion, exchange rate retrieval, purchasing power parity (PPP) conversion,
    and inflation rate calculations across different years and countries.

    Its purpose is to simplify and centralize data retrieval and conversions for
    global financial calculations. The class relies on external data sources such
    as World Bank and IMF datasets to fetch required financial and economic data.


    """
    @staticmethod
    def get_wb_value(var_id: str = None, country: str = 'USA', year: int = 2024):
        df = wb.data.DataFrame(var_id, country, year)
        value = df.loc[country, var_id]
        return value.item()


    @staticmethod
    def get_ppp_conversion_rate_old(country, year):
        ppp_factor = 'PA.NUS.PPP'
        df = wb.data.DataFrame(ppp_factor, country, year)
        value = df.loc[country, ppp_factor]
        return value.item()

    @staticmethod
    @st.cache_data(show_spinner=False)
    def get_ppp_conversion_rate(country, year):
        try:
            database_id = "IMF_WEO"
            indicator = "IMF_WEO_PPPEX"
            value = float(wb360.get_worldbank_data(database_id, indicator, country, timePeriodFrom=year, timePeriodTo=year))
        except Exception as e:
            value = CurrencyConverter.get_ppp_conversion_rate_old(country, year)
        return value

    @staticmethod
    def get_excange_rate_old(country, year):
        wb_code = 'PA.NUS.FCRF'
        df = wb.data.DataFrame(wb_code, country, year)
        value = df.loc[country, wb_code]
        return value.item()

    @staticmethod
    @st.cache_data(show_spinner=False)
    def get_excange_rate(country, year):
        try:
            database_id = "IMF_IFS"
            indicator = "IMF_IFS_END_XDC_USD"
            value = float(wb360.get_worldbank_data(database_id, indicator, country, timePeriodFrom=year, timePeriodTo=year))
        except Exception as e:
            value = CurrencyConverter.get_excange_rate_old(country, year)

        return value

    @staticmethod
    def get_local_inflation_old(country, from_year, to_year):
        wb_code = 'FP.CPI.TOTL'
        cpi_data = wb.data.DataFrame(wb_code,
                                     economy=country,
                                     time=[from_year, to_year])
        from_code_col = f'YR{from_year}'
        to_code_col = f'YR{to_year}'
        inflation_rate = cpi_data.loc[country, to_code_col] / cpi_data.loc[country, from_code_col]

        return inflation_rate.item()

    @staticmethod
    @st.cache_data(show_spinner=False)
    def get_local_inflation(country, from_year, to_year):
        try:
            database_id = "FAO_CP"
            indicator = "FAO_CP_23012"
            value_from = float(wb360.get_worldbank_data(database_id, indicator, country, timePeriodFrom=f'{from_year}-01-01',
                                                        timePeriodTo=f'{from_year}-01-01'))
            value_to = float(wb360.get_worldbank_data(database_id, indicator, country, timePeriodFrom=f'{to_year}-01-01',
                                                   timePeriodTo=f'{to_year}-01-01'))
            inflation_rate = value_to / value_from
        except Exception as e:
            inflation_rate = CurrencyConverter.get_local_inflation_old(country, from_year, to_year)

        return inflation_rate

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

    @staticmethod
    def convert_usd_year(value, country, from_year, to_year):
        exchange_rate_from = CurrencyConverter.get_excange_rate(country, from_year)
        exchange_rate_to = CurrencyConverter.get_excange_rate(country, to_year)
        inflation_rate = CurrencyConverter.get_local_inflation(country, from_year, to_year)

        lcu_year_from = value * exchange_rate_from
        lcu_year_to = lcu_year_from * inflation_rate
        usd_year_to = lcu_year_to / exchange_rate_to
        return usd_year_to











