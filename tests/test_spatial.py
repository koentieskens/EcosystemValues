"""Tests for src/utils/spatial.py → Spatial class."""
import math
import numpy as np
import pandas as pd
import pytest
import geopandas as gpd
from unittest.mock import MagicMock, patch
from shapely.geometry import Polygon, Point

from src.utils.spatial import Spatial


# ---------------------------------------------------------------------------
# get_area_crs
# ---------------------------------------------------------------------------

def _make_gdf(lon, lat):
    """Helper: GeoDataFrame with a single-point geometry in EPSG:4326."""
    geom = Point(lon, lat)
    return gpd.GeoDataFrame([{"geometry": geom}], crs="EPSG:4326")


class TestGetAreaCrs:
    def test_northern_hemisphere(self):
        """Centroid in northern hemisphere → EPSG 326xx."""
        gdf = _make_gdf(lon=10.0, lat=50.0)  # Germany region
        epsg = Spatial.get_area_crs(gdf)
        assert 32600 < epsg < 32700, f"Expected 326xx EPSG, got {epsg}"

    def test_southern_hemisphere(self):
        """Centroid in southern hemisphere → EPSG 327xx."""
        gdf = _make_gdf(lon=-46.0, lat=-23.0)  # São Paulo region
        epsg = Spatial.get_area_crs(gdf)
        assert 32700 < epsg < 32800, f"Expected 327xx EPSG, got {epsg}"

    def test_equator_assigned_northern(self):
        """Centroid exactly on equator (lat=0) is assigned 326xx."""
        gdf = _make_gdf(lon=0.0, lat=0.0)
        epsg = Spatial.get_area_crs(gdf)
        assert 32600 < epsg < 32700


# ---------------------------------------------------------------------------
# create_circle_from_area
# ---------------------------------------------------------------------------

class TestCreateCircleFromArea:
    def test_returns_polygon(self):
        """create_circle_from_area returns a shapely Polygon."""
        result = Spatial.create_circle_from_area(lon=10.0, lat=50.0, area_ha=100)
        assert isinstance(result, Polygon)

    def test_approx_correct_area(self):
        """
        The geodesic area of the created circle polygon is within 5% of the
        requested area.
        """
        from pyproj import Geod

        target_ha = 500.0
        polygon = Spatial.create_circle_from_area(lon=10.0, lat=50.0, area_ha=target_ha)
        g = Geod(ellps="WGS84")
        computed_area_m2, _ = g.geometry_area_perimeter(polygon)
        computed_ha = abs(computed_area_m2) / 10_000

        assert computed_ha == pytest.approx(target_ha, rel=0.05), (
            f"Circle area {computed_ha:.1f} ha deviates >5% from requested {target_ha} ha"
        )


# ---------------------------------------------------------------------------
# get_country_year_data
# ---------------------------------------------------------------------------

class TestGetCountryYearData:
    def _make_wb_df(self):
        """Build a minimal World Bank-style DataFrame."""
        data = {
            "YR2018": [1000.0, np.nan],
            "YR2019": [1050.0, 2000.0],
            "YR2020": [np.nan, 2100.0],
        }
        return pd.DataFrame(data, index=["USA", "BRA"])

    def test_returns_target_year_values(self):
        wb_df = self._make_wb_df()
        result = Spatial.get_country_year_data(wb_df, 2019)
        usa_row = result[result["country"] == "USA"]
        assert usa_row["value"].iloc[0] == pytest.approx(1050.0)

    def test_fills_missing_year_with_nearest(self):
        """
        When target year has NaN, the closest available year's value is used.
        USA has no 2020 value but has 2019; BRA has no 2018 but has 2019.
        """
        wb_df = self._make_wb_df()

        # USA in 2020 is NaN → nearest is 2019 → 1050.0
        result = Spatial.get_country_year_data(wb_df, 2020)
        usa_row = result[result["country"] == "USA"]
        assert not pd.isna(usa_row["value"].iloc[0])
        assert usa_row["value"].iloc[0] == pytest.approx(1050.0)

    def test_missing_target_column_created(self):
        """When the target year column doesn't exist, a NaN column is created and filled."""
        wb_df = self._make_wb_df()  # only has 2018, 2019, 2020
        result = Spatial.get_country_year_data(wb_df, 2025)
        # All values should be filled from nearest available (2020 or 2019)
        assert result["value"].notna().all()


# ---------------------------------------------------------------------------
# add_country_iso3
# ---------------------------------------------------------------------------

class TestAddCountryIso3:
    def test_appends_country_column(self):
        """add_country_iso3 appends an ISO3 'country' column to the GeoDataFrame."""
        geom = Point(10.0, 51.0)  # Germany
        gdf = gpd.GeoDataFrame([{"geometry": geom}], crs="EPSG:4326")

        with patch("src.utils.spatial.reverse_geocode.get") as mock_get:
            mock_get.return_value = {"country_code": "DE"}
            result = Spatial.add_country_iso3(gdf)

        assert "country" in result.columns
        assert result["country"].iloc[0] == "DEU"


# ---------------------------------------------------------------------------
# get_value_from_cog  (mocked rasterio + zonal_stats)
# ---------------------------------------------------------------------------

class TestGetValueFromCog:
    def test_returns_mean_from_raster(self):
        """
        get_value_from_cog returns the mean value extracted via zonal_stats
        from the mocked raster.

        We mock Spatial.read_cog (which uses rasterio internally) and
        zonal_stats to avoid real I/O and Affine-type validation.
        """
        expected_mean = 42.5
        fake_array = np.array([[40.0, 45.0]])
        fake_transform = MagicMock()
        fake_nodata = -9999

        with patch.object(Spatial, "read_cog",
                          return_value=(fake_array, fake_transform, fake_nodata)), \
             patch("src.utils.spatial.zonal_stats",
                   return_value=[{"mean": expected_mean}]):
            result = Spatial.get_value_from_cog(
                cog_path="gs://fake-bucket/fake.tif",
                lon=10.0,
                lat=50.0,
                area_ha=100.0
            )

        assert result == pytest.approx(expected_mean)
