from ..variables.variables import BenefitVariable, ClimateVariable, CountryVariable, Var
from ..variables.land_cover import LandCoverGroup
from ..variables.project_variables import ProjectVariables, Pvar
from ..variables.global_layers import GCSLayer

class TropicalForest:

    VARIABLES = [
        Var(BenefitVariable.SLOPE, ln=True, coefficient=-0.445),
        Var(BenefitVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=11.922),
        Var(BenefitVariable.LAND_COVER, lc=LandCoverGroup.FOREST, coefficient=0.025),
        Var(BenefitVariable.POP_DENSITY, ln=True, coefficient=0.19),
        Var(CountryVariable.GNI_PER_CAPITA, ln=True, coefficient=-0.308)
    ]

    CONSTANTS = {
        'Intercept':1.342,
        'Area_ha_ln': -0.347
    }

    PROJECT_VARIABLES = [
        Pvar(ProjectVariables.TROPICAL_MIXED_FORESTS,0.701),
        Pvar(ProjectVariables.TROPICAL_DRY_FORESTS, 0.216),
        Pvar(ProjectVariables.WATER_PROV, 2.689),
        Pvar(ProjectVariables.POLLINATION, 0.386),
        Pvar(ProjectVariables.CLIMATE_REG, 2.601),
        Pvar(ProjectVariables.EROSION_REG, 1.104),
        Pvar(ProjectVariables.EXISTENCE_BEQUEST, 1.586),
        Pvar(ProjectVariables.TOTAL_FLOW, 0.004),
        Pvar(ProjectVariables.EXCHANGE_VALUE, -1.461),
        Pvar(ProjectVariables.CONS_SURPLUS, -1.834)
    ]

    GLOBAL_LAYERS = [
        GCSLayer.RESTORATION_OPPORTUNITY_COST,
        GCSLayer.EXOTIC_IMPLEMENTATION_COST,
        GCSLayer.NATIVE_IMPLEMENTATION_COST,
        GCSLayer.REGENERATION_IMPLEMENTATION_COST
    ]


class TemparateForest:
    VARIABLES = [
        Var(BenefitVariable.LAND_COVER, lc=LandCoverGroup.FOREST, coefficient=0.013, buffer=10000),
        Var(BenefitVariable.POP_DENSITY, ln=True, coefficient=0.147, buffer=10000),
        Var(CountryVariable.GNI_PER_CAPITA, ln=True, coefficient=-0.432)
    ]

    CONSTANTS = {
        'Intercept': 0.573,
        'Area_ha_ln': -0.142
    }

    PROJECT_VARIABLES = [
        Pvar(ProjectVariables.TEMPERATE_EVERGREEN_FOREST, 1.318),
        Pvar(ProjectVariables.FOOD, 1.221),
        Pvar(ProjectVariables.RAW_MATERIALS, 1.071),
        Pvar(ProjectVariables.WATER_PROV, -0.585),
        Pvar(ProjectVariables.POLLINATION, 1.494),
        Pvar(ProjectVariables.CLIMATE_REG, 1.435),
        Pvar(ProjectVariables.EROSION_REG, 1.15),
        Pvar(ProjectVariables.AIR_QUALITY, 0.769),
        Pvar(ProjectVariables.RECREATION_TOURISM, 0.52),
        Pvar(ProjectVariables.EXISTENCE_BEQUEST, 1.082),
        Pvar(ProjectVariables.TOTAL_FLOW, 0.177),
        Pvar(ProjectVariables.EXCHANGE_VALUE, -2.028)
    ]

    GLOBAL_LAYERS = [
        GCSLayer.RESTORATION_OPPORTUNITY_COST,
        GCSLayer.EXOTIC_IMPLEMENTATION_COST,
        GCSLayer.NATIVE_IMPLEMENTATION_COST,
        GCSLayer.REGENERATION_IMPLEMENTATION_COST
    ]


class IntensiveLandUse:
    VARIABLES = [
        Var(BenefitVariable.HUMAN_MODIF_INDEX, coefficient=2.395),
        Var(BenefitVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=6.038),
        Var(BenefitVariable.ECOSYSTEM_CONDITION, ln=True, coefficient=3.332),
        Var(ClimateVariable.DRY_DAYS, ln=True, coefficient=1.908),
        Var(ClimateVariable.HEAVY_RAIN_DAYS, ln=True,coefficient=-1.51),
        Var(ClimateVariable.MEAN_ANNUAL_TEMPERATURE, ln=True, coefficient=1.062),
        Var(ClimateVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True,coefficient=4.591),
        Var(ClimateVariable.MEAN_NDVI_P95, ln=True, coefficient=-5.734),
        Var(BenefitVariable.POP_DENSITY, ln=True,coefficient=-0.305),
        Var(CountryVariable.GNI_PER_CAPITA, ln=True, coefficient=0.043),

    ]

    CONSTANTS = {
        'Intercept': -14.448,
        'Area_ha_ln': -0.175
    }

    PROJECT_VARIABLES = [
        Pvar(ProjectVariables.CROPLAND_ANNUAL, 1.099),
        Pvar(ProjectVariables.MONOCULTURE_PERRENIAL, 1.7),
        Pvar(ProjectVariables.FOOD, 0.641),
        Pvar(ProjectVariables.BIO_CONTROL, 0.571),
        Pvar(ProjectVariables.WATER_FLOW_REG, 1.754),
        Pvar(ProjectVariables.EROSION_REG, 1.632),
        Pvar(ProjectVariables.MAINTAIN_LIFE_CYCLE, -3.623),
        Pvar(ProjectVariables.MAINTAIN_SOIL, -1.697),
        Pvar(ProjectVariables.RECREATION_TOURISM, -0.951),
        Pvar(ProjectVariables.COGNITIVE_DEVELOPMENT, -3.57),
        Pvar(ProjectVariables.EXISTENCE_BEQUEST, 2.312),
        Pvar(ProjectVariables.TOTAL_FLOW, 2.025),
        Pvar(ProjectVariables.EXCHANGE_VALUE, 1.899),
        Pvar(ProjectVariables.CONS_SURPLUS, -0.428)
    ]

    GLOBAL_LAYERS = [
        GCSLayer.RESTORATION_OPPORTUNITY_COST,
        GCSLayer.EXOTIC_IMPLEMENTATION_COST,
        GCSLayer.NATIVE_IMPLEMENTATION_COST,
        GCSLayer.REGENERATION_IMPLEMENTATION_COST
    ]


class Mangroves:
    VARIABLES = [
        Var(BenefitVariable.HUMAN_MODIF_INDEX, coefficient=-1.832),
        Var(ClimateVariable.DRY_DAYS, ln=True, coefficient=0.533),
        Var(ClimateVariable.HEAVY_RAIN_DAYS, ln=True, coefficient=-0.871),
        Var(ClimateVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, coefficient=1.486),
        Var(ClimateVariable.MEAN_NDVI_P95, ln=True, coefficient=-2.295),
        Var(BenefitVariable.POP_DENSITY, ln=True, coefficient=0.222),
        Var(CountryVariable.GNI_PER_CAPITA, ln=True, coefficient=0.542),

    ]

    CONSTANTS = {
        'Intercept': 0.813,
        'Area_ha_ln': -0.284
    }

    PROJECT_VARIABLES = [
        Pvar(ProjectVariables.FOOD, 0.018),
        Pvar(ProjectVariables.RAW_MATERIALS, -0.675),
        Pvar(ProjectVariables.CLIMATE_REG, 1.164),
        Pvar(ProjectVariables.EROSION_REG, 0.672),
        Pvar(ProjectVariables.RECREATION_TOURISM, -0.793),
        Pvar(ProjectVariables.EXISTENCE_BEQUEST, -1.015),
        Pvar(ProjectVariables.TOTAL_FLOW, -0.187),
        Pvar(ProjectVariables.EXCHANGE_VALUE, -0.133),
        Pvar(ProjectVariables.CONS_SURPLUS, -0.743)
    ]

    GLOBAL_LAYERS = [
        GCSLayer.RESTORATION_OPPORTUNITY_COST,
        GCSLayer.EXOTIC_IMPLEMENTATION_COST,
        GCSLayer.NATIVE_IMPLEMENTATION_COST,
        GCSLayer.REGENERATION_IMPLEMENTATION_COST
    ]


class Grassland:
    VARIABLES = [
        Var(BenefitVariable.HUMAN_MODIF_INDEX, coefficient=10.507),
        Var(BenefitVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=28.11),
        Var(BenefitVariable.ECOSYSTEM_CONDITION, ln=True, coefficient=3.153),
        Var(ClimateVariable.DRY_DAYS, ln=True, coefficient=-3.294),
        Var(ClimateVariable.HEAVY_RAIN_DAYS, ln=True, coefficient=2.691),
        Var(ClimateVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, coefficient=-4.768),
        Var(ClimateVariable.MEAN_NDVI_P95, ln=True, coefficient=-7.525),
        Var(BenefitVariable.POP_DENSITY, ln=True, coefficient=--1.097, buffer=10000),
        Var(CountryVariable.GNI_PER_CAPITA, ln=True, coefficient=-0.648),

    ]

    CONSTANTS = {
        'Intercept': 12.228,
        'Area_ha_ln': 0.311
    }

    PROJECT_VARIABLES = [
        Pvar(ProjectVariables.FOOD, 2.216),
        Pvar(ProjectVariables.RAW_MATERIALS, -0.593),
        Pvar(ProjectVariables.WATER_PROV, -1.986),
        Pvar(ProjectVariables.WASTE_TREATMENT, -3.426),
        Pvar(ProjectVariables.CLIMATE_REG, 0.608),
        Pvar(ProjectVariables.EROSION_REG, -4.422),
        Pvar(ProjectVariables.RECREATION_TOURISM, -1.596),
        Pvar(ProjectVariables.EXISTENCE_BEQUEST, 0.6),
        Pvar(ProjectVariables.TOTAL_FLOW, -0.004),
        Pvar(ProjectVariables.EXCHANGE_VALUE, 0.76),
        Pvar(ProjectVariables.CONS_SURPLUS, -0.445)
    ]

    GLOBAL_LAYERS = [
        GCSLayer.RESTORATION_OPPORTUNITY_COST,
        GCSLayer.EXOTIC_IMPLEMENTATION_COST,
        GCSLayer.NATIVE_IMPLEMENTATION_COST,
        GCSLayer.REGENERATION_IMPLEMENTATION_COST
    ]


