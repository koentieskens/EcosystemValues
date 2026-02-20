"""Tests for src/app_utils/utils.py → St_Utils and CurrencyConverter."""
import math
import pytest
from unittest.mock import patch, MagicMock
from shapely.geometry import Polygon


# ---------------------------------------------------------------------------
# St_Utils
# ---------------------------------------------------------------------------

class TestGetGeodesicArea:
    def test_known_polygon(self):
        """
        A roughly 1-degree × 1-degree polygon at the equator has an area close
        to ~(111 km)^2 ≈ 1 233 000 ha.  We accept ±5%.
        """
        from src.app_utils.utils import St_Utils

        # Simple square near the equator (~1° × 1°)
        polygon = Polygon([
            (0.0, 0.0),
            (1.0, 0.0),
            (1.0, 1.0),
            (0.0, 1.0),
            (0.0, 0.0),
        ])
        area_ha = St_Utils.get_geodesic_area(polygon)

        # 1° × 1° at equator ≈ 111 km × 111 km ≈ 1 232 100 ha
        expected_ha = 1_232_100
        assert area_ha == pytest.approx(expected_ha, rel=0.05)

    def test_returns_positive(self):
        from src.app_utils.utils import St_Utils

        polygon = Polygon([(0, 0), (0.1, 0), (0.1, 0.1), (0, 0.1)])
        assert St_Utils.get_geodesic_area(polygon) > 0


class TestGetLocationInfo:
    def test_returns_county_and_country(self):
        """get_location_info returns a (county, country) tuple using reverse_geocode."""
        from src.app_utils.utils import St_Utils

        with patch("src.app_utils.utils.reverse_geocode.get") as mock_geo:
            mock_geo.return_value = {
                "county": "Berlin",
                "country_code": "DE",
            }
            county, country = St_Utils.get_location_info(52.5, 13.4)

        assert county == "Berlin"
        # iso3166 maps DE → Germany
        assert "Germany" in country or country == "DE"  # fallback if iso lookup varies

    def test_zero_coords_return_empty(self):
        """lat=0, lon=0 returns ('', '') without calling reverse_geocode."""
        from src.app_utils.utils import St_Utils

        with patch("src.app_utils.utils.reverse_geocode.get") as mock_geo:
            result = St_Utils.get_location_info(0.0, 0.0)

        mock_geo.assert_not_called()
        assert result == ("", "")


# ---------------------------------------------------------------------------
# CurrencyConverter
# ---------------------------------------------------------------------------

class TestConvertPppToUsd:
    def test_expected_usd_value(self):
        """
        convert_ppp_to_usd(100, 'NLD', 2020, 2024):
          - ppp_conv = 0.8 → value_lcu_from = 80
          - inflation_rate = 1.1 → value_lcu_to = 88
          - exchange_rate = 0.9 → value_usd_to = 88/0.9 ≈ 97.78
        """
        from src.app_utils.utils import CurrencyConverter

        with patch.object(CurrencyConverter, "get_ppp_conversion_rate", return_value=0.8), \
             patch.object(CurrencyConverter, "get_local_inflation", return_value=1.1), \
             patch.object(CurrencyConverter, "get_excange_rate", return_value=0.9):
            result = CurrencyConverter.convert_ppp_to_usd(100, "NLD", 2020, 2024)

        expected = (100 * 0.8 * 1.1) / 0.9
        assert result == pytest.approx(expected, rel=1e-6)


class TestConvertUsdYear:
    def test_year_adjusted_conversion(self):
        """
        convert_usd_year(100, 'NLD', 2020, 2024):
          - exchange_from = 0.9, exchange_to = 1.0, inflation = 1.05
          - lcu_from = 100 * 0.9 = 90
          - lcu_to = 90 * 1.05 = 94.5
          - usd_to = 94.5 / 1.0 = 94.5
        """
        from src.app_utils.utils import CurrencyConverter

        def mock_exchange(country, year):
            return 0.9 if year == 2020 else 1.0

        with patch.object(CurrencyConverter, "get_excange_rate", side_effect=mock_exchange), \
             patch.object(CurrencyConverter, "get_local_inflation", return_value=1.05):
            result = CurrencyConverter.convert_usd_year(100, "NLD", 2020, 2024)

        expected = (100 * 0.9 * 1.05) / 1.0
        assert result == pytest.approx(expected, rel=1e-6)


# ---------------------------------------------------------------------------
# wb360.get_worldbank_data  (mocked requests)
# ---------------------------------------------------------------------------

class TestWb360GetWorldbankData:
    def test_returns_obs_value(self):
        """get_worldbank_data parses OBS_VALUE from a mocked API JSON response."""
        from src.utils import wb360

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "value": [{"OBS_VALUE": "1.234"}]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("src.utils.wb360.requests.get", return_value=mock_response):
            result = wb360.get_worldbank_data(
                database_id="IMF_WEO",
                indicator="IMF_WEO_PPPEX",
                ref_area="NLD",
                timePeriodFrom=2020,
                timePeriodTo=2020,
            )

        assert result == "1.234"

    def test_request_exception_is_raised(self):
        """A requests.exceptions.RequestException propagates out of get_worldbank_data."""
        import requests
        from src.utils import wb360

        with patch("src.utils.wb360.requests.get",
                   side_effect=requests.exceptions.RequestException("timeout")):
            with pytest.raises(requests.exceptions.RequestException):
                wb360.get_worldbank_data("IMF_WEO", "IMF_WEO_PPPEX", "NLD")
