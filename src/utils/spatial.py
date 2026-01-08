import os
import ee
import math
import reverse_geocode
from iso3166 import countries
import pandas as pd
import numpy as np
from shapely.geometry import Polygon
from pyproj import Geod
import geopandas as gpd
import rioxarray as rxr
import rasterio as rio
from rasterio.windows import from_bounds
from rasterstats import zonal_stats




class Spatial:


    @staticmethod
    def get_area_crs(aoi) -> int:

        # Note: This method by Koen
        # make sure the input is in wgs 84
        aoi = aoi.to_crs(4326)

        lon = aoi.geometry.centroid[0].x
        lat = aoi.geometry.centroid[0].y

        """Based on lat and lng, return best utm epsg-code"""
        utm_band = str((math.floor((lon + 180) / 6) % 60) + 1)

        if len(utm_band) == 1:
            utm_band = '0' + utm_band

        if lat >= 0:
            epsg_code = '326' + utm_band
            return int(epsg_code)

        epsg_code = '327' + utm_band
        return int(epsg_code)

    @staticmethod
    def add_country_iso3(gdf):
        import warnings

        # Suppress the specific GeoPandas warning for geographic CRS
        warnings.filterwarnings("ignore", message="Geometry is in a geographic CRS")

        lat = gdf.geometry.centroid.y
        lon = gdf.geometry.centroid.x
        coords = [(latitude, longitude) for latitude, longitude in zip(lat, lon)]

        locations = [reverse_geocode.get(coord)['country_code'] for coord in coords]
        country = [countries.get(cc).alpha3 for cc in locations]
        gdf['country'] = country
        return gdf

    @staticmethod
    def get_country_year_data(wb_df, target_year):
        """
        Extract country-value pairs for a specific year, filling NaN values with closest available year.

        Args:
            wb_df: DataFrame from wb.data.DataFrame with countries as index and year columns (YR1995, etc.)
            target_year: Year to extract (e.g., 2020)

        Returns:
            DataFrame with 'country' and 'value' columns
        """


        # Create the target column name
        target_col = f'YR{target_year}'

        # Check if target year exists in columns
        if target_col not in wb_df.columns:
            wb_df[target_col] = np.nan

        # Create result dataframe
        result = pd.DataFrame({
            'country': wb_df.index,
            'value': wb_df[target_col],
            'year': int(target_year)
        }).reset_index(drop=True)

        # Find rows with NaN values
        nan_mask = result['value'].isna()

        if nan_mask.any():
            print(f"Found {nan_mask.sum()} countries with missing data for {target_year}")

            # For each country with NaN, find closest year with data
            for idx in result[nan_mask].index:
                country = result.loc[idx, 'country']
                country_data = wb_df.loc[country]

                # Get all non-NaN values with their year distances
                available_years = []
                for col in wb_df.columns:
                    if col.startswith('YR') and pd.notna(country_data[col]):
                        year = int(col[2:])  # Extract year from YRxxxx
                        distance = abs(year - target_year)
                        available_years.append((distance, country_data[col], year))

                # Use value from closest year
                if available_years:
                    closest_value = min(available_years, key=lambda x: x[0])[1]
                    closest_year = min(available_years, key=lambda x: x[0])[2]
                    result.loc[idx, 'value'] = closest_value
                    result.loc[idx, 'year'] = int(closest_year)
                    print(f"Filled {country} with {int(closest_year)}  data")

        return result
    @staticmethod
    def create_circle_from_area(lon, lat, area_ha, ellips='WGS84', num_points=64):
        """
        Create a circle polygon with specified area in square meters

        Parameters:
        - center_point: (lon, lat) tuple
        - area_sqm: desired area in square meters
        - ellps: ellipsoid (default 'WGS84')
        - num_points: number of points to approximate circle

        Returns:
        - shapely Polygon geometry
        """
        center_point = (lon, lat)
        g = Geod(ellps=ellips)
        # get area in square meters
        area_sqm = area_ha * 10000
        # Calculate radius
        radius_meters = math.sqrt(area_sqm / math.pi)

        # Create circle points
        circle_points = []
        for i in range(num_points):
            azimuth = 360.0 * i / num_points
            lon, lat, _ = g.fwd(center_point[0], center_point[1], azimuth, radius_meters)
            circle_points.append((lon, lat))

        circle_points.append(circle_points[0])  # Close polygon

        return Polygon(circle_points)

    @staticmethod
    def get_value_from_cog(cog_path, lon, lat, area_ha,  buffer_degrees = 0.1, band = 1):
        circle_geom = Spatial.create_circle_from_area(lon, lat, area_ha)
        circle_gdf = gpd.GeoDataFrame([1], geometry=[circle_geom], crs='EPSG:4326')

        buffered_circle = circle_geom.buffer(buffer_degrees)
        buffered_bounds = buffered_circle.bounds

        data_array, transform, no_data_value = Spatial.read_cog(cog_path, buffered_bounds, band=band)

        stats = zonal_stats(
            circle_gdf,
            data_array,
            affine=transform,
            stats=['mean'],
            nodata=no_data_value,
            all_touched=True
        )
        return stats[0]['mean']

    @staticmethod
    def get_value_from_cog_with_polygon(cog_path, polygon_gdf, buffer_degrees=0.1, band=1):


        buffered_aoi = polygon_gdf.buffer(buffer_degrees)
        polygon = buffered_aoi.geometry.squeeze()

        buffered_aoi_bounds = polygon.bounds


        data_array, transform, no_data_value = Spatial.read_cog(cog_path, buffered_aoi_bounds, band=band)

        stats = zonal_stats(
            polygon_gdf,
            data_array,
            affine=transform,
            stats=['mean'],
            nodata=no_data_value,
            all_touched=True
        )
        return stats[0]['mean']

    @staticmethod
    def read_cog(cog_path, bounds, band=1):
        with rio.open(cog_path) as src:
            window = from_bounds(*bounds, src.transform)
            nodata_value = src.nodata
            # Read only the windowed data
            raster_array = src.read(band, window=window)  # rasterio is 1-indexed

            # Get transform for the windowed area
            transform = src.window_transform(window)

        return raster_array, transform, nodata_value


if __name__ == '__main__':


    lon, lat = (-11.4, 15.09)
    area_ha = 100
    bucket_name = "nbs-tool-public"
    cog_filename = "data/global_data/cost/se_plan/opportunity_cost.tif"
    gcs_path = f"gs://{bucket_name}/{gcs_path}"
    value = Spatial.get_value_from_cog(gcs_path, lon, lat, area_ha)
    print(value)

    from shapely.geometry import Polygon

    # Create a test polygon in Cameroon (around Yaoundé area)
    # Coordinates are in longitude, latitude format for Shapely
    cameroon_coords = [
        (11.5180, 3.8480),  # Point 1
        (11.5220, 3.8480),  # Point 2
        (11.5240, 3.8520),  # Point 3
        (11.5220, 3.8560),  # Point 4
        (11.5180, 3.8540),  # Point 5
        (11.5160, 3.8500),  # Point 6
    ]
    import geopandas as gpd
    test_drawn_polygon = Polygon(cameroon_coords)
    aoi_gdf = gpd.GeoDataFrame([1], geometry=[test_drawn_polygon], crs='EPSG:4326')
    polygon_gdf = aoi_gdf
    bucket_name = "nbs-tool-public"
    gcs_path = "data/global_data/benefit/siikamaki/wat_2020_global_4326.tif"
    cog_path = f"gs://{bucket_name}/{gcs_path}"









