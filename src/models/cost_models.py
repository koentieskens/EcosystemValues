from ..variables.variables import BenefitVariable, ClimateVariable, CountryVariable, Var
from ..variables.land_cover import LandCoverGroup
from ..variables.project_variables import ProjectVariables, Pvar
from ..variables.global_layers import GCSLayer

class TropicalForest:

    GLOBAL_LAYERS = [
        GCSLayer.RESTORATION_OPPORTUNITY_COST,
        GCSLayer.EXOTIC_IMPLEMENTATION_COST,
        GCSLayer.NATIVE_IMPLEMENTATION_COST,
        GCSLayer.REGENERATION_IMPLEMENTATION_COST
    ]
