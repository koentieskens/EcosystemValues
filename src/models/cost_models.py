from src.variables.variables import ModelVariable
from src.variables.spatial_variable import BenefitSpatialVariable, ClimateSpatialVariable, CountrySpatialVariable
from src.variables.global_layers import GlobalLayer
from src.variables.nature_based_solutions import NBS
from src.variables.cost_input import CostInput

class BUSCH:

    GLOBAL_LAYERS = [
        ModelVariable(GlobalLayer.RESTORATION_OPPORTUNITY_COST),
        ModelVariable(GlobalLayer.EXOTIC_IMPLEMENTATION_COST),
        ModelVariable(GlobalLayer.NATIVE_IMPLEMENTATION_COST),
        ModelVariable(GlobalLayer.REGENERATION_IMPLEMENTATION_COST)
    ]


class IntensiveLandUseCost:
    CONSTANTS = {
        'Intercept': -0.5672346,
        'Area_ha_ln': -0.3493724,
    }

    INPUT_VARIABLES = [
        ModelVariable(CostInput.LATITUDE, ihs=True, coefficient=3.79909),
        ModelVariable(CostInput.ESTABLISHMENT_DAYS, ihs=True, coefficient=0.1205117),
        ModelVariable(CostInput.MAINTENANCE_DAYS, ihs=True, coefficient=0.80314774),
    ]

    VARIABLES = [
        ModelVariable(CountrySpatialVariable.GDP_PER_CAPITA_PPP_CONSTANT, ihs=True, buffer=10000, coefficient=0.2543724, group='Socio-economic'),
        ModelVariable(ClimateSpatialVariable.MEAN_ANNUAL_TEMPERATURE, ihs=True, buffer=10000, coefficient=1.397741, group='Climate'),
        ModelVariable(ClimateSpatialVariable.TOTAL_ANNUAL_PRECIPITATION, ihs=True, buffer=10000, coefficient=-1.020533, group='Climate'),
        ModelVariable(BenefitSpatialVariable.SLOPE, ihs=True, buffer=10000, coefficient=0.9725203, group='Landscape')
    ]

    QUADRATICS = [
        ModelVariable(ClimateSpatialVariable.MEAN_ANNUAL_TEMPERATURE, ihs=True, buffer=10000, coefficient=-0.5519715),
        ModelVariable(ClimateSpatialVariable.TOTAL_ANNUAL_PRECIPITATION, ihs=True, buffer=10000, coefficient=0.5297093),
        ModelVariable(BenefitSpatialVariable.SLOPE, ihs=True, buffer=10000, coefficient=-0.3114993),
        ModelVariable(CostInput.LATITUDE, ihs=True, coefficient=-0.616287),
        ModelVariable(CostInput.MAINTENANCE_DAYS, ihs=True, coefficient=-0.0594578),
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
        ModelVariable(NBS.NBS_33, coefficient=0.00),
    ]

    @classmethod
    def update_quadratics_values(cls):
        """Update the value of each ModelVariable in QUADRATICS to match
        the value from the corresponding variable in INPUT_VARIABLES or VARIABLES"""

        # Create a mapping of variable types to their values
        variable_values = {}

        # Collect values from INPUT_VARIABLES
        for var in cls.INPUT_VARIABLES:
            if hasattr(var, 'value') and var.value is not None:
                variable_values[var.variable.name] = var.value

        # Collect values from VARIABLES (will override INPUT_VARIABLES if same variable exists)
        for var in cls.VARIABLES:
            if hasattr(var, 'value') and var.value is not None:
                variable_values[var.variable.name] = var.value

        # Update QUADRATICS values
        for quadratic_var in cls.QUADRATICS:
            if quadratic_var.variable.name in variable_values:
                quadratic_var.value = variable_values[quadratic_var.variable.name]


class MangroveCost:
    CONSTANTS = {
        'Intercept': -2.14,
        'Area_ha_ln': -0.005,
    }

    INPUT_VARIABLES = [
        ModelVariable(CostInput.COST_YEARS, ln=True, coefficient=0.748),
    ]

    VARIABLES = [
        ModelVariable(CountrySpatialVariable.GDP_PER_CAPITA, ln=True, coefficient=0.938),
        ModelVariable(CountrySpatialVariable.PPP, ln=True, coefficient=2.245)
    ]

    NBS = [
        ModelVariable(NBS.HYDROLOGICAL_MANGROVE_RESTORATION, coefficient=0.00),
        ModelVariable(NBS.PLANTING_MANGROVES, coefficient=1.274),
    ]
