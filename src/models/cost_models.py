from ..variables.variables import Var
from ..variables.spatial_variable import BenefitSpatialVariable, ClimateSpatialVariable, CountrySpatialVariable
from ..variables.land_cover import LandCoverGroup
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
        Var('Latitude', ln=True, coefficient=3.79909),
        Var(CostInput.ESTABLISHMENT_DAYS, ln=True, coefficient=0.1205117),
        Var(CostInput.MAINTENANCE_DAYS,  ln=True, coefficient=0.80314774),
    ]

    VARIABLES = [
        Var(CountrySpatialVariable.GDP_PER_CAPITA_PPP_CONSTANT, ln=True, buffer=10000, coefficient=0.2543724),
        Var(ClimateSpatialVariable.MEAN_ANNUAL_TEMPERATURE, ln=True, buffer=10000, coefficient=1.397741),
        Var(ClimateSpatialVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, buffer=10000, coefficient=-1.020533),
        Var(BenefitSpatialVariable.SLOPE, ln=True, buffer=10000, coefficient=0.9725203)
    ]

    QUADRATICS = [
        Var(ClimateSpatialVariable.MEAN_ANNUAL_TEMPERATURE, ln=True, buffer=10000, coefficient=-0.5519715),
        Var(ClimateSpatialVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, buffer=10000, coefficient=0.5297093),
        Var(BenefitSpatialVariable.SLOPE, ln=True, buffer=10000, coefficient=0.9725203),
        Var('Latitude', ln=True, coefficient=-0.616287),
        Var(CostInput.ESTABLISHMENT_DAYS, ln=True, coefficient=0.1205117),
        Var(CostInput.MAINTENANCE_DAYS, ln=True, coefficient=-0.0594578),
    ]

    NBS = [
        Var(NBS.NBS_4, coefficient=-0.8122672),
        Var(NBS.NBS_10, coefficient=0.2556073),
        Var(NBS.NBS_14, coefficient=0.1359859),
        Var(NBS.NBS_16, coefficient=0.2088671),
        Var(NBS.NBS_21, coefficient=1.141219),
        Var(NBS.NBS_30, coefficient=0.6927834),
        Var(NBS.NBS_31, coefficient=0.626235),
        Var(NBS.NBS_32, coefficient=0.2069697),
    ]
