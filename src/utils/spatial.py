import os
import ee
import math
import reverse_geocode
from iso3166 import countries
import pandas as pd
import numpy as np


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



