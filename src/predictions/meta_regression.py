import math
import numpy as np
from src.models.benefit_models import IntensiveLandUse, Grassland, TropicalForest, TemparateForest
from src.models.cost_models import IntensiveLandUseCost
from src.variables.variables import ModelVariable
from src.app_utils.utils import CurrencyConverter


from typing import Union, List, Optional


class Predict:
    """Calculate ecosystem service value using regression equation"""
    @staticmethod
    def log_p1(value: float) -> float:
        """return natural log of value + 1 if value > 0, 0 otherwise"""
        return math.log(value + 1) if (value + 1) > 0 else 0.0

    @staticmethod
    def ihs(value: float) -> float:
        """return arcsinh of value"""
        return np.arcsinh(value)

    @staticmethod
    def ihs_reverse(value: float) -> float:
        """return asinh of value"""
        return np.sinh(value)

    @staticmethod
    def predict_benefit(
            model_class: Union[IntensiveLandUse, Grassland, TropicalForest, TemparateForest],
            ecosystem_service:ModelVariable,
            value_type: ModelVariable,
            area_hectares: float) -> Optional[float]:
        """Predict ecosystem service value using regression equation"""
        try:
            # Get model constants
            intercept = model_class.CONSTANTS.get('Intercept')
            area_ln_coef = model_class.CONSTANTS.get('Area_ha_ln')
            total_flow_coef = model_class.CONSTANTS.get('Total_flow')

            # Start with intercept
            regression_sum = intercept

            # Add area term: ln(area_hectares) * area_ln_coefficient
            est = Predict.log_p1(area_hectares) * area_ln_coef
            regression_sum += est

            # Add total flow term: total_flow * total_flow_coef
            est = total_flow_coef * 1
            regression_sum += est

            # Add model variables
            for var_obj in model_class.VARIABLES:

                if hasattr(var_obj, 'ln') and var_obj.ln:
                    value = Predict.log_p1(var_obj.value)

                else:
                    value = var_obj.value

                est = var_obj.coefficient * value
                regression_sum += est

            # add ecosys service
            value = 1
            coefficient = ecosystem_service.coefficient
            est = coefficient * value
            print(est)
            regression_sum += est

            # add value type
            value = 1
            coefficient = value_type.coefficient
            est = coefficient * value
            print(est)
            regression_sum += est

            # add sub biome
            if model_class.SUB_BIOMES:
                for sub_biome in model_class.SUB_BIOMES:
                    value = sub_biome.value
                    coefficient = sub_biome.coefficient
                    est = coefficient * value
                    print(est)
                    regression_sum += est

            # add interactions
            if model_class.INTERACTIONS:
                for interaction in model_class.INTERACTIONS:
                    es_type = interaction[0]
                    if ecosystem_service.variable.SEEA_clas1 != es_type:
                        continue
                    var_obj = interaction[1]
                    if hasattr(var_obj, 'ln') and var_obj.ln:
                        value = Predict.log_p1(var_obj.value)
                    else:
                        value = var_obj.value

                    coefficient = var_obj.coefficient
                    est = coefficient * value
                    regression_sum += est

            ecosystem_value = math.exp(regression_sum)

            return ecosystem_value

        except Exception as e:
            raise e

    @staticmethod
    def predict_cost(
            model_class: Union[IntensiveLandUseCost],
            nbs: ModelVariable,
            area_hectares: float,
            latitude: float,
            est_days:int =10,
            main_days:int =50) -> Optional[float]:
        """Predict ecosystem service value using regression equation"""
        try:
            for var in model_class.INPUT_VARIABLES:
                if var.name == 'Latitude':
                    var.value = abs(latitude)
                if var.name == 'Establishment_Days':
                    var.value = est_days
                if var.name == 'Maintenance_Days':
                    var.value = main_days

            model_class.update_quadratics_values()

            # Get model constants
            intercept = model_class.CONSTANTS.get('Intercept')
            area_ln_coef = model_class.CONSTANTS.get('Area_ha_ln')

            # Start with intercept
            regression_sum = intercept
            eq = f"{intercept} (INT)"

            # Add area term: ln(area_hectares) * area_ln_coefficient
            est = Predict.ihs(area_hectares) * area_ln_coef
            regression_sum += est
            eq += f"+ {est} (AREA:{area_hectares:.2f} ha)"

            variables = model_class.INPUT_VARIABLES + model_class.VARIABLES
            # Add model variables
            for var_obj in variables:

                if hasattr(var_obj, 'ihs') and var_obj.ihs:
                    value = Predict.ihs(var_obj.value)
                else:
                    value = var_obj.value

                est = var_obj.coefficient * value
                regression_sum += est
                eq += f"+ {est}, {var_obj.name}:{var_obj.value:.2f}"

            # add nbs
            value = 1
            coefficient = nbs.coefficient
            est = coefficient * value
            regression_sum += est
            eq += f"+ {est}"

            # add interactions
            if model_class.QUADRATICS:
                for quadratic in model_class.QUADRATICS:
                    if hasattr(quadratic, 'ihs') and quadratic.ihs:
                        value = (Predict.ihs(quadratic.value))**2
                    else:
                        value = quadratic.value **2

                    coefficient = quadratic.coefficient
                    est = coefficient * value
                    regression_sum += est
                    eq += f"+ {est}"

            nbs_cost = Predict.ihs_reverse(regression_sum)
            print(nbs_cost)
            print(eq)
            return nbs_cost

        except Exception as e:
            raise e