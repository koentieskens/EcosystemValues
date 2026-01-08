import math
from ..models.benefit_models import IntensiveLandUse, Grassland, TropicalForest, TemparateForest
from ..variables.variables import BenefitVariable, ClimateVariable, CountryVariable, Var
from typing import Union, List, Optional
from ..variables.project_variables import ProjectVariables, Pvar, EcosystemServices

class Predict:
    """Calculate ecosystem service value using regression equation"""
    @staticmethod
    def log_p1(value: float) -> float:
        """return natural log of value + 1 if value > 0, 0 otherwise"""
        return math.log(value + 1) if (value + 1) > 0 else 0.0

    @staticmethod
    def predict_value(
            model_class: Union[IntensiveLandUse, Grassland, TropicalForest, TemparateForest],
            ecosystem_service:Pvar,
            value_type: Pvar,
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
                    if ecosystem_service.variable.value[2] != es_type:
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