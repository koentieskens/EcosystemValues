from ..variables.variables import BenefitVariable, ClimateVariable, CountryVariable, Var
from ..variables.land_cover import LandCoverGroup
from ..variables.project_variables import ProjectVariables, Pvar, EcosystemServices
from ..variables.global_layers import GCSLayer

class TropicalForest:
    CONSTANTS = {
        'Intercept': -20.789,
        'Area_ha_ln': -0.323,
        'Total_flow': 0.271
    }

    VARIABLES = [
        Var(BenefitVariable.ELEVATION, ln=True, coefficient=0.566),
        Var(BenefitVariable.SLOPE, ln=True, coefficient=-0.511),
        Var(ClimateVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, coefficient=-0.679),
        Var(BenefitVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=5.793),
        Var(BenefitVariable.PROTECTION_STATUS, ln=True, coefficient=-0.334),
        Var(BenefitVariable.LAND_COVER, lc=LandCoverGroup.FOREST, coefficient=0.007, buffer=50000),
        Var(BenefitVariable.HUMAN_MODIF_INDEX, ln=True, coefficient=-1.096, buffer=50000),
        Var(BenefitVariable.POP_DENSITY, ln=True, coefficient=0.202, buffer=10000),
        Var(CountryVariable.GNI_PER_CAPITA, ln=True, coefficient=0.012)
    ]

    ECOSYSTEM_SERVICES = [
        Pvar(EcosystemServices.WOOD_PROVISION, 1.183),
        Pvar(EcosystemServices.WILD_FISH_PROVISION, 1.519),
        Pvar(EcosystemServices.WATER_SUPPLY, 3.771),
        Pvar(EcosystemServices.AIR_FILTRATION, 2.438),
        Pvar(EcosystemServices.GLOBAL_CLIMATE, 3.513),
        Pvar(EcosystemServices.POLLINATION, 1.069),
        Pvar(EcosystemServices.RAINFALL_REGULATION, 3.369),
        Pvar(EcosystemServices.RIVER_FLOOD_REGULATION, 2.758),
        Pvar(EcosystemServices.SOIL_EROSION_REGULATION, 1.548),
        Pvar(EcosystemServices.RECREATION, -0.271),
    ]

    SUB_BIOMES = []

    VALUE_TYPES = [
        Pvar(ProjectVariables.EXCHANGE_VALUE, -0.054),
        Pvar(ProjectVariables.CONS_SURPLUS, -1.378)
    ]

    INTERACTIONS = [
        ('prov', Var(CountryVariable.GNI_PER_CAPITA, ln=True, coefficient=0.053)),
        ('cult', Var(CountryVariable.GNI_PER_CAPITA, ln=True, coefficient=0.203)),
        ('prov', Var(BenefitVariable.POP_DENSITY, ln=True, coefficient=0.144)),
        ('reg', Var(BenefitVariable.POP_DENSITY, ln=True, coefficient=0.455))
    ]

    SIIKAMAKI = [
        GCSLayer.FOREST_HABITAT_VALUE,
        GCSLayer.FOREST_NONWOOD_PRODUCTS_VALUE,
        GCSLayer.FOREST_RECREATION_VALUE,
        GCSLayer.FOREST_WATER_SERVICE_VALUE
    ]

    GLOBAL_LAYERS = [
        GCSLayer.RESTORATION_OPPORTUNITY_COST,
        GCSLayer.EXOTIC_IMPLEMENTATION_COST,
        GCSLayer.NATIVE_IMPLEMENTATION_COST,
        GCSLayer.REGENERATION_IMPLEMENTATION_COST
    ]




class TemparateForest:

    CONSTANTS = {
        'Intercept': -24.389,
        'Area_ha_ln': -0.15,
        'Total_flow': 0.187
    }

    VARIABLES = [
        Var(ClimateVariable.MEAN_NDVI_P95, ln=True, coefficient=-6.854),
        Var(ClimateVariable.DRY_DAYS, ln=True, coefficient=2.663),
        Var(ClimateVariable.MEAN_ANNUAL_TEMPERATURE, ln=True, coefficient=-0.737),
        Var(ClimateVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, coefficient=2.063),
        Var(BenefitVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=4.000),
        Var(BenefitVariable.ROAD_DENSITY, ln=True, coefficient=0.352, buffer=10000),
        Var(BenefitVariable.SETTLEMENTS, ln=True, coefficient=0.912, buffer=10000),
        Var(BenefitVariable.LAND_COVER, lc=LandCoverGroup.FOREST, coefficient=0.004, buffer=30000),
        Var(BenefitVariable.POP_DENSITY, ln=True, coefficient=-0.199, buffer=10000),
        Var(CountryVariable.GNI_PER_CAPITA, ln=True, coefficient=0.154)
    ]

    SUB_BIOMES = [
        Pvar(ProjectVariables.TEMPERATE_EVERGREEN_FOREST, coefficient=1.835),
        Pvar(ProjectVariables.OTHER, 0.00)
    ]

    ECOSYSTEM_SERVICES = [
        Pvar(EcosystemServices.WILD_ANIMAL_PROVISION, -1.993),
        Pvar(EcosystemServices.WOOD_PROVISION, -0.426),
        Pvar(EcosystemServices.WATER_SUPPLY, -2.601),
        Pvar(EcosystemServices.AIR_FILTRATION, -0.834),
        Pvar(EcosystemServices.NUTRIENT_RETENTION, -3.167),
        Pvar(EcosystemServices.RAINFALL_REGULATION, -1.218),
        Pvar(EcosystemServices.SOIL_EROSION_REGULATION, -0.731),
        Pvar(EcosystemServices.SOIL_QUALITY_REGULATION, -1.791),
        Pvar(EcosystemServices.RECREATION, -1.771),
    ]

    VALUE_TYPES = [
        Pvar(ProjectVariables.EXCHANGE_VALUE, -1.929),
        Pvar(ProjectVariables.CONS_SURPLUS, -0.649)
    ]

    INTERACTIONS = [
        ('reg', Var(BenefitVariable.BIODIVERSITY_INTACTNESS, coefficient=-0.414)),
        ('cult', Var(BenefitVariable.BIODIVERSITY_INTACTNESS, coefficient=1.222))
    ]

    SIIKAMAKI = [
        GCSLayer.FOREST_HABITAT_VALUE,
        GCSLayer.FOREST_NONWOOD_PRODUCTS_VALUE,
        GCSLayer.FOREST_RECREATION_VALUE,
        GCSLayer.FOREST_WATER_SERVICE_VALUE
    ]

    GLOBAL_LAYERS = [
        GCSLayer.RESTORATION_OPPORTUNITY_COST,
        GCSLayer.EXOTIC_IMPLEMENTATION_COST,
        GCSLayer.NATIVE_IMPLEMENTATION_COST,
        GCSLayer.REGENERATION_IMPLEMENTATION_COST
    ]


class IntensiveLandUse:
    CONSTANTS = {
        'Intercept': 2.529,
        'Area_ha_ln': -0.256,
        'Total_flow': 2.505
    }

    VARIABLES = [
        Var(BenefitVariable.NPP_SHARE, ln=True, coefficient=0.986),  # EPI_ln -> NPP_SHARE
        Var(BenefitVariable.NIGHT_LIGHT, coefficient=-0.053),  # nightLight
        Var(ClimateVariable.DRY_DAYS, ln=True, coefficient=-2.351),  # dryDays_ln
        Var(ClimateVariable.MEAN_ANNUAL_TEMPERATURE, ln=True, coefficient=1.278),  # Temp_mean_ln
        Var(CountryVariable.GNI_PER_CAPITA, ln=True, coefficient=0.639),  # GNIPC_ln
        Var(BenefitVariable.POP_DENSITY, ln=True, coefficient=0.252, buffer=10000)  # popDensity_buf_A_ln (buffer A = 10km)
    ]


    SUB_BIOMES = [
        Pvar(ProjectVariables.CROPLAND_ANNUAL, 1.108),  # Cropland_Annual
        Pvar(ProjectVariables.MONOCULTURE_PERENNIAL, 1.524),
        Pvar(ProjectVariables.OTHER, 0.00)
    ]

    ECOSYSTEM_SERVICES = [
        Pvar(EcosystemServices.CROP_PROVISION, 1.614),  # S_Crop_Prov
        Pvar(EcosystemServices.WOOD_PROVISION, 0.876),  # S_Wood_Prov
        Pvar(EcosystemServices.LIVESTOCK_PROVISION, -1.418),  # S_Livestock
        Pvar(EcosystemServices.POLLINATION, 1.087),  # S_Pollination
        Pvar(EcosystemServices.SOIL_EROSION_REGULATION, 2.174),  # S_Soil_Erosion_Reg
        Pvar(EcosystemServices.WATER_FLOW_REGULATION, 6.46),  # S_Water_Flow_Reg
        Pvar(EcosystemServices.RECREATION, -1.062),  # S_Recreation
        Pvar(EcosystemServices.VISUAL_AMENITY, -1.889)  # S_Visual_Amenity
    ]

    VALUE_TYPES = [
        Pvar(ProjectVariables.EXCHANGE_VALUE, 2.102),  # Exchange value
        Pvar(ProjectVariables.CONS_SURPLUS, 0.547)  # Consumer surplus
    ]

    INTERACTIONS = [
        ('prov', Var(CountryVariable.GNI_PER_CAPITA, ln=True, coefficient=-0.192)),  # GNIPC_ESprov
        ('prov', Var(BenefitVariable.POP_DENSITY, ln=True, coefficient=0.34))  # PopD_ESprov
    ]

    GLOBAL_LAYERS = [
        GCSLayer.RESTORATION_OPPORTUNITY_COST,
        GCSLayer.EXOTIC_IMPLEMENTATION_COST,
        GCSLayer.NATIVE_IMPLEMENTATION_COST,
        GCSLayer.REGENERATION_IMPLEMENTATION_COST
    ]


class Mangroves:
    CONSTANTS = {
        'Intercept': -2.275,
        'Area_ha_ln': -0.275,
        'Total_flow': -0.365
    }

    VARIABLES = [
        Var(BenefitVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=1.211),  # biodivIntactness_ln
        Var(BenefitVariable.FRAGMENTATION, ln=True, coefficient=-0.895, buffer=10000),  # fragmentation_buf_A_ln (buffer A = 10km)
        Var(ClimateVariable.DRY_DAYS, ln=True, coefficient=0.612),  # dryDays_ln
        Var(ClimateVariable.HEAVY_RAIN_DAYS, ln=True, coefficient=-0.928),  # rainDays_ln -> HEAVY_RAIN_DAYS
        Var(ClimateVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, coefficient=1.475),  # Precip_total_ln
        Var(ClimateVariable.MEAN_NDVI_P95, ln=True, coefficient=-2.507),  # NDVI_ln
        Var(BenefitVariable.LAND_COVER, coefficient=0.003, buffer=30000, lc=LandCoverGroup.MANGROVE),
        Var(BenefitVariable.POP_DENSITY, ln=True, coefficient=0.309, buffer=10000),  # popDensity_buf_A_ln (buffer A = 10km)
        Var(CountryVariable.GNI_PER_CAPITA, ln=True, coefficient=0.461)  # GNIPC_ln
    ]

    SUB_BIOMES = []

    ECOSYSTEM_SERVICES = [
        Pvar(EcosystemServices.WILD_FISH_PROVISION, 0.562),  # S_Wild_Fish_Prov
        Pvar(EcosystemServices.AQUACULTURE, 0.793),  # S_Aquaculture
        Pvar(EcosystemServices.WOOD_PROVISION, -0.199),  # S_Wood_Prov
        Pvar(EcosystemServices.WILD_ANIMAL_PROVISION, -0.895),  # S_Wild_Animal_Prov
        Pvar(EcosystemServices.SOIL_EROSION_REGULATION, 0.768),  # S_Soil_Erosion_Reg
        Pvar(EcosystemServices.GLOBAL_CLIMATE, 2.075)  # S_Global_Climate
    ]

    VALUE_TYPES = [
        Pvar(ProjectVariables.EXCHANGE_VALUE, -0.058),  # Exchange value
        Pvar(ProjectVariables.CONS_SURPLUS, -0.731)  # Consumer surplus
    ]

    INTERACTIONS = []

    GLOBAL_LAYERS = [
        GCSLayer.RESTORATION_OPPORTUNITY_COST,
        GCSLayer.EXOTIC_IMPLEMENTATION_COST,
        GCSLayer.NATIVE_IMPLEMENTATION_COST,
        GCSLayer.REGENERATION_IMPLEMENTATION_COST
    ]


class Grassland:
    CONSTANTS = {
        'Intercept': 25.815,
        'Area_ha_ln': 0.223,
        'Total_flow': -1.131
    }

    VARIABLES = [
        Var(BenefitVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=6.928),  # biodivIntactness_ln
        Var(BenefitVariable.NPP_SHARE, ln=True, coefficient=0.427),  # EPI_ln -> NPP_SHARE
        Var(BenefitVariable.HUMAN_MODIF_INDEX, ln=True, coefficient=1.708),  # humanModification_ln
        Var(ClimateVariable.DRY_DAYS, ln=True, coefficient=-7.536),  # dryDays_ln
        Var(ClimateVariable.HEAVY_RAIN_DAYS, ln=True, coefficient=3.39),  # rainDays_ln -> HEAVY_RAIN_DAYS
        Var(ClimateVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, coefficient=-9.538),  # Precip_total_ln
        Var(ClimateVariable.MEAN_NDVI_P95, ln=True, coefficient=3.432),  # NDVI_ln
        Var(BenefitVariable.POP_DENSITY, ln=True, coefficient=-0.936, buffer=10000),# popDensity_buf_A_ln (buffer A = 10km)
        Var(CountryVariable.GNI_PER_CAPITA, ln=True, coefficient=-1.309)  # GNIPC_ln
    ]

    ECOSYSTEM_SERVICES = [
        Pvar(EcosystemServices.WILD_ANIMAL_PROVISION, -0.481),  # S_Wild_Animal_Prov
        Pvar(EcosystemServices.WATER_SUPPLY, -1.271),  # S_Water_Supply
        Pvar(EcosystemServices.GRAZED_BIOMASS_PROVISION, 1.567),  # S_Grazed_Biomass
        Pvar(EcosystemServices.LIVESTOCK_PROVISION, 4.625),  # S_Livestock
        Pvar(EcosystemServices.POLLINATION, 0.603),  # S_Pollination
        Pvar(EcosystemServices.NUTRIENT_RETENTION, -3.6),  # S_Nutrient_Retention
        Pvar(EcosystemServices.RIVER_FLOOD_REGULATION, -4.297),  # S_River_Flood_Reg
        Pvar(EcosystemServices.SOIL_EROSION_REGULATION, -6.053),  # S_Soil_Erosion_Reg
        Pvar(EcosystemServices.RECREATION, -1.504)  # S_Recreation
    ]

    VALUE_TYPES = [
        Pvar(ProjectVariables.EXCHANGE_VALUE, 0.968),  # Exchange value
        Pvar(ProjectVariables.CONS_SURPLUS, -0.078)  # Consumer surplus
    ]

    SUB_BIOMES = []

    INTERACTIONS = []

    GLOBAL_LAYERS = [
        GCSLayer.RESTORATION_OPPORTUNITY_COST,
        GCSLayer.EXOTIC_IMPLEMENTATION_COST,
        GCSLayer.NATIVE_IMPLEMENTATION_COST,
        GCSLayer.REGENERATION_IMPLEMENTATION_COST
    ]


