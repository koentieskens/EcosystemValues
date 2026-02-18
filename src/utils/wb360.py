
import requests
from typing import Optional, Dict, Any


def get_worldbank_data(
        database_id: str,
        indicator: str,
        ref_area: str,
        **kwargs
) -> str:
    """
    Fetch data from World Bank Data360 API.

    Args:
        database_id (str): Database identifier (e.g., 'IMF_WEO')
        indicator (str): Indicator code (e.g., 'IMF_WEO_PPPEX')
        ref_area (str): Reference area/country code (e.g., 'ARG')

    Returns:
        Dict: JSON response from the API

    Raises:
        requests.exceptions.RequestException: If the API request fails
    """
    base_url = "https://data360api.worldbank.org/data360/data"

    params = {
        'DATABASE_ID': database_id,
        'INDICATOR': indicator,
        'REF_AREA': ref_area,
        'SKIP':0
    }

    params.update(kwargs)

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()['value'][0]['OBS_VALUE']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        raise


if __name__ == "__main__":
    # Using the same parameters as your original URL
    data = get_worldbank_data(
        database_id="IMF_WEO",
        indicator="IMF_WEO_PPPEX",
        ref_area="ARG",
        period_from=2020,
        period_to=2020
    )
    print(data)
