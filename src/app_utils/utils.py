import streamlit as st
import math
import reverse_geocode
from iso3166 import countries
from ..extract_data.predictions import Predictions


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
