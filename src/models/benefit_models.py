from src.variables.spatial_variable import BenefitSpatialVariable, ClimateSpatialVariable, CountrySpatialVariable
from src.variables.variables import ModelVariable
from ..variables.land_cover import LandCoverGroup
from ..variables.ecosystem_service import EcosystemService
from ..variables.global_layers import GlobalLayer
from src.variables.sub_biome import SubBiome
from src.variables.value_type import ValueType
from src.models import cost_models

class TropicalForest:
    CONSTANTS = {
        'Intercept': -20.789,
        'Area_ha_ln': -0.323,
        'Total_flow': 0.271
    }

    VARIABLES = [
        ModelVariable(BenefitSpatialVariable.ELEVATION, ln=True, coefficient=0.566),
        ModelVariable(BenefitSpatialVariable.SLOPE, ln=True, coefficient=-0.511),
        ModelVariable(ClimateSpatialVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, coefficient=-0.679),
        ModelVariable(BenefitSpatialVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=5.793),
        ModelVariable(BenefitSpatialVariable.PROTECTION_STATUS, ln=True, coefficient=-0.334),
        ModelVariable(BenefitSpatialVariable.LAND_COVER, lc=LandCoverGroup.FOREST, coefficient=0.007, buffer=50000),
        ModelVariable(BenefitSpatialVariable.HUMAN_MODIF_INDEX, ln=True, coefficient=-1.096, buffer=50000),
        ModelVariable(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=0.202, buffer=10000),
        ModelVariable(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=0.012)
    ]

    ECOSYSTEM_SERVICES = [
        ModelVariable(EcosystemService.WOOD_PROVISION, coefficient=1.183),
        #ModelVariable(EcosystemService.WILD_FISH_PROVISION, coefficient=1.519),
        #ModelVariable(EcosystemService.WATER_SUPPLY, coefficient=3.771),
        ModelVariable(EcosystemService.AIR_FILTRATION, coefficient=2.438),
        #ModelVariable(EcosystemService.GLOBAL_CLIMATE, coefficient=3.513),
        ModelVariable(EcosystemService.POLLINATION, coefficient=1.069),
        ModelVariable(EcosystemService.RAINFALL_REGULATION, coefficient=3.369),
        ModelVariable(EcosystemService.RIVER_FLOOD_REGULATION, coefficient=2.758),
        ModelVariable(EcosystemService.SOIL_EROSION_REGULATION, coefficient=1.548),
        #ModelVariable(EcosystemService.RECREATION, coefficient=-0.271),
    ]

    SUB_BIOMES = []

    VALUE_TYPES = [
        ModelVariable(ValueType.EXCHANGE_VALUE, coefficient=-0.054),
        ModelVariable(ValueType.CONS_SURPLUS, coefficient=-1.378)
    ]

    INTERACTIONS = [
        ('Provisioning', ModelVariable(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=0.053)),
        ('Cultural', ModelVariable(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=0.203)),
        ('Provisioning', ModelVariable(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=0.144)),
        ('Regulating and Maintenance', ModelVariable(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=0.455))
    ]

    SIIKAMAKI = [
        ModelVariable(GlobalLayer.FOREST_HABITAT_VALUE),
        ModelVariable(GlobalLayer.FOREST_NONWOOD_PRODUCTS_VALUE),
        ModelVariable(GlobalLayer.FOREST_RECREATION_VALUE),
        ModelVariable(GlobalLayer.FOREST_WATER_SERVICE_VALUE)
    ]

    COST_MODEL = cost_models.BUSCH

    GLOBAL_LAYERS = [
        GlobalLayer.RESTORATION_OPPORTUNITY_COST,
        GlobalLayer.EXOTIC_IMPLEMENTATION_COST,
        GlobalLayer.NATIVE_IMPLEMENTATION_COST,
        GlobalLayer.REGENERATION_IMPLEMENTATION_COST
    ]


class TemparateForest:

    CONSTANTS = {
        'Intercept': -24.389,
        'Area_ha_ln': -0.15,
        'Total_flow': 0.187
    }

    VARIABLES = [
        ModelVariable(ClimateSpatialVariable.MEAN_NDVI_P95, ln=True, coefficient=-6.854),
        ModelVariable(ClimateSpatialVariable.DRY_DAYS, ln=True, coefficient=2.663),
        ModelVariable(ClimateSpatialVariable.MEAN_ANNUAL_TEMPERATURE, ln=True, coefficient=-0.737),
        ModelVariable(ClimateSpatialVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, coefficient=2.063),
        ModelVariable(BenefitSpatialVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=4.000),
        ModelVariable(BenefitSpatialVariable.ROAD_DENSITY, ln=True, coefficient=0.352, buffer=10000),
        ModelVariable(BenefitSpatialVariable.SETTLEMENTS, ln=True, coefficient=0.912, buffer=10000),
        ModelVariable(BenefitSpatialVariable.LAND_COVER, lc=LandCoverGroup.FOREST, coefficient=0.004, buffer=30000),
        ModelVariable(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=-0.199, buffer=10000),
        ModelVariable(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=0.154)
    ]

    SUB_BIOMES = [
        ModelVariable(SubBiome.TEMPERATE_EVERGREEN_FOREST, coefficient=1.835),
        ModelVariable(SubBiome.OTHER, coefficient= 0.00)
    ]

    ECOSYSTEM_SERVICES = [
        #ModelVariable(EcosystemService.WILD_ANIMAL_PROVISION, coefficient=-1.993),
        ModelVariable(EcosystemService.WOOD_PROVISION, coefficient= -0.426),
        #ModelVariable(EcosystemService.WATER_SUPPLY, coefficient= -2.601),
        ModelVariable(EcosystemService.AIR_FILTRATION, coefficient=-0.834),
        ModelVariable(EcosystemService.NUTRIENT_RETENTION, coefficient=-3.167),
        ModelVariable(EcosystemService.RAINFALL_REGULATION, coefficient=-1.218),
        ModelVariable(EcosystemService.SOIL_EROSION_REGULATION, coefficient=-0.731),
        ModelVariable(EcosystemService.SOIL_QUALITY_REGULATION, coefficient=-1.791),
        #ModelVariable(EcosystemService.RECREATION, coefficient= -1.771),
    ]

    VALUE_TYPES = [
        ModelVariable(ValueType.EXCHANGE_VALUE, coefficient=-1.929),
        ModelVariable(ValueType.CONS_SURPLUS, coefficient=-0.649)
    ]

    INTERACTIONS = [
        ('reg', ModelVariable(BenefitSpatialVariable.BIODIVERSITY_INTACTNESS, coefficient=-0.414)),
        ('cult', ModelVariable(BenefitSpatialVariable.BIODIVERSITY_INTACTNESS, coefficient=1.222))
    ]

    SIIKAMAKI = [
        ModelVariable(GlobalLayer.FOREST_HABITAT_VALUE),
        ModelVariable(GlobalLayer.FOREST_NONWOOD_PRODUCTS_VALUE),
        ModelVariable(GlobalLayer.FOREST_RECREATION_VALUE),
        ModelVariable(GlobalLayer.FOREST_WATER_SERVICE_VALUE)
    ]

    COST_MODEL = cost_models.BUSCH

    GLOBAL_LAYERS = [
        GlobalLayer.RESTORATION_OPPORTUNITY_COST,
        GlobalLayer.EXOTIC_IMPLEMENTATION_COST,
        GlobalLayer.NATIVE_IMPLEMENTATION_COST,
        GlobalLayer.REGENERATION_IMPLEMENTATION_COST
    ]


class IntensiveLandUse:
    CONSTANTS = {
        'Intercept': 2.529,
        'Area_ha_ln': -0.256,
        'Total_flow': 2.505
    }

    VARIABLES = [
        ModelVariable(BenefitSpatialVariable.NPP_SHARE, ln=True, coefficient=0.986),  # EPI_ln -> NPP_SHARE
        ModelVariable(BenefitSpatialVariable.NIGHT_LIGHT, coefficient=-0.053),  # nightLight
        ModelVariable(ClimateSpatialVariable.DRY_DAYS, ln=True, coefficient=-2.351),  # dryDays_ln
        ModelVariable(ClimateSpatialVariable.MEAN_ANNUAL_TEMPERATURE, ln=True, coefficient=1.278),  # Temp_mean_ln
        ModelVariable(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=0.639),  # GNIPC_ln
        ModelVariable(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=0.252, buffer=10000)  # popDensity_buf_A_ln (buffer A = 10km)
    ]


    SUB_BIOMES = [
        ModelVariable(SubBiome.CROPLAND_ANNUAL, coefficient=1.108),  # Cropland_Annual
        ModelVariable(SubBiome.MONOCULTURE_PERENNIAL, coefficient= 1.524),
        ModelVariable(SubBiome.OTHER, coefficient=0.00)
    ]

    ECOSYSTEM_SERVICES = [
        ModelVariable(EcosystemService.CROP_PROVISION, coefficient= 1.614),  # S_Crop_Prov
        ModelVariable(EcosystemService.WOOD_PROVISION, coefficient=0.876),  # S_Wood_Prov
        ModelVariable(EcosystemService.LIVESTOCK_PROVISION, coefficient= -1.418),  # S_Livestock
        ModelVariable(EcosystemService.POLLINATION, coefficient=1.087),  # S_Pollination
        ModelVariable(EcosystemService.SOIL_EROSION_REGULATION, coefficient= 2.174),  # S_Soil_Erosion_Reg
        ModelVariable(EcosystemService.WATER_FLOW_REGULATION, coefficient=6.46),  # S_Water_Flow_Reg
        ModelVariable(EcosystemService.RECREATION, coefficient= -1.062),  # S_Recreation
        ModelVariable(EcosystemService.VISUAL_AMENITY, coefficient= -1.889)  # S_Visual_Amenity
    ]

    VALUE_TYPES = [
        ModelVariable(ValueType.EXCHANGE_VALUE, coefficient=2.102),  # Exchange value
        ModelVariable(ValueType.CONS_SURPLUS, coefficient= 0.547)  # Consumer surplus
    ]

    INTERACTIONS = [
        ('Provisioning', ModelVariable(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=-0.192)),  # GNIPC_ESprov
        ('Provisioning', ModelVariable(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=0.34))  # PopD_ESprov
    ]

    COST_MODEL = cost_models.IntensiveLandUseCost

    GLOBAL_LAYERS = [
        GlobalLayer.RESTORATION_OPPORTUNITY_COST,
        GlobalLayer.EXOTIC_IMPLEMENTATION_COST,
        GlobalLayer.NATIVE_IMPLEMENTATION_COST,
        GlobalLayer.REGENERATION_IMPLEMENTATION_COST
    ]


class Mangroves:
    CONSTANTS = {
        'Intercept': -2.275,
        'Area_ha_ln': -0.275,
        'Total_flow': -0.365
    }

    VARIABLES = [
        ModelVariable(BenefitSpatialVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=1.211),  # biodivIntactness_ln
        ModelVariable(BenefitSpatialVariable.FRAGMENTATION, ln=True, coefficient=-0.895, buffer=10000),  # fragmentation_buf_A_ln (buffer A = 10km)
        ModelVariable(ClimateSpatialVariable.DRY_DAYS, ln=True, coefficient=0.612),  # dryDays_ln
        ModelVariable(ClimateSpatialVariable.HEAVY_RAIN_DAYS, ln=True, coefficient=-0.928),  # rainDays_ln -> HEAVY_RAIN_DAYS
        ModelVariable(ClimateSpatialVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, coefficient=1.475),  # Precip_total_ln
        ModelVariable(ClimateSpatialVariable.MEAN_NDVI_P95, ln=True, coefficient=-2.507),  # NDVI_ln
        ModelVariable(BenefitSpatialVariable.LAND_COVER, coefficient=0.003, buffer=30000, lc=LandCoverGroup.MANGROVE),
        ModelVariable(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=0.309, buffer=10000),  # popDensity_buf_A_ln (buffer A = 10km)
        ModelVariable(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=0.461)  # GNIPC_ln
    ]

    SUB_BIOMES = []

    ECOSYSTEM_SERVICES = [
        ModelVariable(EcosystemService.WILD_FISH_PROVISION, coefficient=0.562),  # S_Wild_Fish_Prov
        ModelVariable(EcosystemService.AQUACULTURE, coefficient=0.793),  # S_Aquaculture
        ModelVariable(EcosystemService.WOOD_PROVISION, coefficient=-0.199),  # S_Wood_Prov
        ModelVariable(EcosystemService.WILD_ANIMAL_PROVISION, coefficient= -0.895),  # S_Wild_Animal_Prov
        ModelVariable(EcosystemService.SOIL_EROSION_REGULATION, coefficient=0.768),  # S_Soil_Erosion_Reg
        ModelVariable(EcosystemService.GLOBAL_CLIMATE, coefficient=2.075)  # S_Global_Climate
    ]

    VALUE_TYPES = [
        ModelVariable(ValueType.EXCHANGE_VALUE, coefficient=-0.058),  # Exchange value
        ModelVariable(ValueType.CONS_SURPLUS, coefficient= -0.731)  # Consumer surplus
    ]

    INTERACTIONS = []
    COST_MODEL = cost_models.BUSCH
    GLOBAL_LAYERS = [
        GlobalLayer.RESTORATION_OPPORTUNITY_COST,
        GlobalLayer.EXOTIC_IMPLEMENTATION_COST,
        GlobalLayer.NATIVE_IMPLEMENTATION_COST,
        GlobalLayer.REGENERATION_IMPLEMENTATION_COST
    ]


class Grassland:
    CONSTANTS = {
        'Intercept': 25.815,
        'Area_ha_ln': 0.223,
        'Total_flow': -1.131
    }

    VARIABLES = [
        ModelVariable(BenefitSpatialVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=6.928),  # biodivIntactness_ln
        ModelVariable(BenefitSpatialVariable.NPP_SHARE, ln=True, coefficient=0.427),  # EPI_ln -> NPP_SHARE
        ModelVariable(BenefitSpatialVariable.HUMAN_MODIF_INDEX, ln=True, coefficient=1.708),  # humanModification_ln
        ModelVariable(ClimateSpatialVariable.DRY_DAYS, ln=True, coefficient=-7.536),  # dryDays_ln
        ModelVariable(ClimateSpatialVariable.HEAVY_RAIN_DAYS, ln=True, coefficient=3.39),  # rainDays_ln -> HEAVY_RAIN_DAYS
        ModelVariable(ClimateSpatialVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, coefficient=-9.538),  # Precip_total_ln
        ModelVariable(ClimateSpatialVariable.MEAN_NDVI_P95, ln=True, coefficient=3.432),  # NDVI_ln
        ModelVariable(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=-0.936, buffer=10000),# popDensity_buf_A_ln (buffer A = 10km)
        ModelVariable(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=-1.309)  # GNIPC_ln
    ]

    ECOSYSTEM_SERVICES = [
        ModelVariable(EcosystemService.WILD_ANIMAL_PROVISION, coefficient= -0.481),  # S_Wild_Animal_Prov
        ModelVariable(EcosystemService.WATER_SUPPLY, coefficient= -1.271),  # S_Water_Supply
        ModelVariable(EcosystemService.GRAZED_BIOMASS_PROVISION, coefficient=1.567),  # S_Grazed_Biomass
        ModelVariable(EcosystemService.LIVESTOCK_PROVISION, coefficient= 4.625),  # S_Livestock
        ModelVariable(EcosystemService.POLLINATION, coefficient= 0.603),  # S_Pollination
        ModelVariable(EcosystemService.NUTRIENT_RETENTION, coefficient= -3.6),  # S_Nutrient_Retention
        ModelVariable(EcosystemService.RIVER_FLOOD_REGULATION, coefficient=-4.297),  # S_River_Flood_Reg
        ModelVariable(EcosystemService.SOIL_EROSION_REGULATION, coefficient=-6.053),  # S_Soil_Erosion_Reg
        ModelVariable(EcosystemService.RECREATION, coefficient= -1.504)  # S_Recreation
    ]

    VALUE_TYPES = [
        ModelVariable(ValueType.EXCHANGE_VALUE, coefficient=0.968),  # Exchange value
        ModelVariable(ValueType.CONS_SURPLUS, coefficient= -0.078)  # Consumer surplus
    ]

    SUB_BIOMES = []

    INTERACTIONS = []
    COST_MODEL = cost_models.GrasslandCost
    GLOBAL_LAYERS = [
        GlobalLayer.RESTORATION_OPPORTUNITY_COST,
        GlobalLayer.EXOTIC_IMPLEMENTATION_COST,
        GlobalLayer.NATIVE_IMPLEMENTATION_COST,
        GlobalLayer.REGENERATION_IMPLEMENTATION_COST
    ]


