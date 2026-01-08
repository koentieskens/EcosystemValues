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

            variable_enum = var_obj.var
            if hasattr(variable_enum.value, 'description'):
                name = variable_enum.value.description
                tooltip = variable_enum.value.description
            else:
                name = str(variable_enum.value).replace('_', ' ').title()
                tooltip = name

            return name, tooltip
        except Exception as e:
            return str(var_obj.var).replace('_', ' ').title(), ""

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
    def log_p1(value):
        return math.log(value + 1) if (value + 1) > 0 else 0


    @staticmethod
    def predict_value(model_class, ecosystem_service, value_type, area_hectares):
        try:
            # Get model constants
            intercept = model_class.CONSTANTS.get('Intercept')
            area_ln_coef = model_class.CONSTANTS.get('Area_ha_ln')

            # Start with intercept
            regression_sum = intercept

            # Add area term: ln(area_hectares) * area_ln_coefficient
            est = St_Utils.log_p1(area_hectares) * area_ln_coef

            equation = f"Benefits = exp({intercept} + {area_ln_coef} * Area_ha_ln"

            regression_sum += est

            # Add model variables
            for var_obj in model_class.VARIABLES:

                if hasattr(var_obj, 'ln') and var_obj.ln:
                    value = St_Utils.log_p1(var_obj.value)
                    add_on = "_ln"
                else:
                    value = var_obj.value
                    add_on = ""

                est = var_obj.coefficient * value
                regression_sum += est
                equation += f" + {var_obj.coefficient} * {var_obj.var.name}{add_on}"

            #add ecosys service
            value = 1
            coefficient = ecosystem_service.coefficient
            est = coefficient * value
            print(est)
            regression_sum += est
            equation += f" + {value} * {coefficient} "

            # add value type
            value = 1
            coefficient = value_type.coefficient
            est = coefficient * value
            print(est)
            regression_sum += est
            equation += f" + {value} * {coefficient} "

            #add sub biome
            if model_class.SUB_BIOMES:
                for sub_biome in model_class.SUB_BIOMES:
                    value = sub_biome.value
                    coefficient = sub_biome.coefficient
                    est = coefficient * value
                    print(est)
                    regression_sum += est
                    equation += f" + {value} * {coefficient} "


            ecosystem_value = math.exp(regression_sum)

            return ecosystem_value

        except Exception as e:
            return None


    @staticmethod
    def calculate_ecosystem_value(model_class, float_variables, project_variables, area_hectares):
        """Calculate ecosystem service value using regression equation"""
        try:
            # Get model constants
            intercept = model_class.CONSTANTS.get('Intercept', 0)
            area_ln_coef = model_class.CONSTANTS.get('Area_ha_ln', 0)

            # Start with intercept
            regression_sum = intercept

            # Add area term: ln(area_hectares) * area_ln_coefficient
            regression_sum += math.log(area_hectares) * area_ln_coef

            # Add model variables (float variables)
            for var_obj in model_class.VARIABLES:
                # Get the form field key
                if hasattr(var_obj, 'lc') and var_obj.lc is not None:
                    buffer = var_obj.var.buffer if var_obj.var.buffer else 0
                    var_key = var_obj.lc.get_name(buffer=buffer)
                else:
                    var_key = var_obj.var.name

                value = float_variables.get(var_key, 0)

                if hasattr(var_obj, 'ln') and var_obj.ln:
                    value = math.log(value) if value > 0 else 0


                regression_sum += var_obj.coefficient * value

            # Add project variables (boolean variables: True=1, False=0)
            for pvar_obj in model_class.PROJECT_VARIABLES:

                var_key = pvar_obj.variable.name
                is_selected = project_variables.get(var_key, 0)
                regression_sum += pvar_obj.coefficient * (1 if is_selected else 0)

            # Calculate final value: exp(regression_sum)
            ecosystem_value = math.exp(regression_sum)

            return ecosystem_value, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def inject_responsive_css():
        """Inject CSS to make folium maps responsive"""
        st.markdown("""
        <style>
        /* Make folium maps responsive */
        .stfolium {
            width: 100% !important;
        }

        .stfolium > div {
            width: 100% !important;
        }

        /* Adjust map container */
        .folium-map {
            width: 100% !important;
            height: 60vh !important; /* 60% of viewport height */
            min-height: 400px !important;
            max-height: 600px !important;
        }

        /* Responsive breakpoints */
        @media (max-width: 768px) {
            .folium-map {
                height: 50vh !important;
                min-height: 300px !important;
            }
        }

        @media (min-width: 1200px) {
            .folium-map {
                height: 70vh !important;
                max-height: 700px !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def get_geodesic_area(polygon: Polygon):

        g = Geod(ellps='WGS84')
        geod_area = abs(g.geometry_area_perimeter(polygon)[0])

        return geod_area / 10000




