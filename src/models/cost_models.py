from ..variables.variables import ModelVariable
from ..variables.spatial_variable import BenefitSpatialVariable, ClimateSpatialVariable, CountrySpatialVariable
from ..variables.global_layers import GlobalLayer
from src.variables.nature_based_solutions import NBS
from src.variables.cost_input import CostInput

class TropicalForest:

    GLOBAL_LAYERS = [
        GlobalLayer.RESTORATION_OPPORTUNITY_COST,
        GlobalLayer.EXOTIC_IMPLEMENTATION_COST,
        GlobalLayer.NATIVE_IMPLEMENTATION_COST,
        GlobalLayer.REGENERATION_IMPLEMENTATION_COST
    ]


class IntensiveLandUse:
    CONSTANTS = {
        'Intercept': -0.5672346,
        'Area_ha_ln': -0.3493724,
    }

    INPUT_VARIABLES = [
        ModelVariable(CostInput.LATITUDE, ln=True, coefficient=3.79909),
        ModelVariable(CostInput.ESTABLISHMENT_DAYS, ln=True, coefficient=0.1205117),
        ModelVariable(CostInput.MAINTENANCE_DAYS, ln=True, coefficient=0.80314774),
    ]

    VARIABLES = [
        ModelVariable(CountrySpatialVariable.GDP_PER_CAPITA_PPP_CONSTANT, ln=True, buffer=10000, coefficient=0.2543724),
        ModelVariable(ClimateSpatialVariable.MEAN_ANNUAL_TEMPERATURE, ln=True, buffer=10000, coefficient=1.397741),
        ModelVariable(ClimateSpatialVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, buffer=10000, coefficient=-1.020533),
        ModelVariable(BenefitSpatialVariable.SLOPE, ln=True, buffer=10000, coefficient=0.9725203)
    ]

    QUADRATICS = [
        ModelVariable(ClimateSpatialVariable.MEAN_ANNUAL_TEMPERATURE, ln=True, buffer=10000, coefficient=-0.5519715),
        ModelVariable(ClimateSpatialVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, buffer=10000, coefficient=0.5297093),
        ModelVariable(BenefitSpatialVariable.SLOPE, ln=True, buffer=10000, coefficient=0.9725203),
        ModelVariable(CostInput.LATITUDE, ln=True, coefficient=-0.616287),
        ModelVariable(CostInput.ESTABLISHMENT_DAYS, ln=True, coefficient=0.1205117),
        ModelVariable(CostInput.MAINTENANCE_DAYS, ln=True, coefficient=-0.0594578),
    ]

    NBS = [
        ModelVariable(NBS.NBS_4, coefficient=-0.8122672),
        ModelVariable(NBS.NBS_10, coefficient=0.2556073),
        ModelVariable(NBS.NBS_14, coefficient=0.1359859),
        ModelVariable(NBS.NBS_16, coefficient=0.2088671),
        ModelVariable(NBS.NBS_21, coefficient=1.141219),
        ModelVariable(NBS.NBS_30, coefficient=0.6927834),
        ModelVariable(NBS.NBS_31, coefficient=0.626235),
        ModelVariable(NBS.NBS_32, coefficient=0.2069697),
    ]
