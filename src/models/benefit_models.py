from ..variables.spatial_variable import BenefitSpatialVariable, ClimateSpatialVariable, CountrySpatialVariable
from ..variables.variables import Var
from ..variables.land_cover import LandCoverGroup
from ..variables.ecosystem_service import EcosystemService
from ..variables.global_layers import GlobalLayer
from src.variables.sub_biome import SubBiome
from src.variables.value_type import ValueType

class TropicalForest:
    CONSTANTS = {
        'Intercept': -20.789,
        'Area_ha_ln': -0.323,
        'Total_flow': 0.271
    }

    VARIABLES = [
        Var(BenefitSpatialVariable.ELEVATION, ln=True, coefficient=0.566),
        Var(BenefitSpatialVariable.SLOPE, ln=True, coefficient=-0.511),
        Var(ClimateSpatialVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, coefficient=-0.679),
        Var(BenefitSpatialVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=5.793),
        Var(BenefitSpatialVariable.PROTECTION_STATUS, ln=True, coefficient=-0.334),
        Var(BenefitSpatialVariable.LAND_COVER, lc=LandCoverGroup.FOREST, coefficient=0.007, buffer=50000),
        Var(BenefitSpatialVariable.HUMAN_MODIF_INDEX, ln=True, coefficient=-1.096, buffer=50000),
        Var(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=0.202, buffer=10000),
        Var(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=0.012)
    ]

    ECOSYSTEM_SERVICES = [
        Var(EcosystemService.WOOD_PROVISION, coefficient=1.183),
        Var(EcosystemService.WILD_FISH_PROVISION, coefficient=1.519),
        Var(EcosystemService.WATER_SUPPLY, coefficient=3.771),
        Var(EcosystemService.AIR_FILTRATION, coefficient=2.438),
        Var(EcosystemService.GLOBAL_CLIMATE, coefficient=3.513),
        Var(EcosystemService.POLLINATION, coefficient=1.069),
        Var(EcosystemService.RAINFALL_REGULATION, coefficient=3.369),
        Var(EcosystemService.RIVER_FLOOD_REGULATION, coefficient=2.758),
        Var(EcosystemService.SOIL_EROSION_REGULATION, coefficient=1.548),
        Var(EcosystemService.RECREATION, coefficient=-0.271),
    ]

    SUB_BIOMES = []

    VALUE_TYPES = [
        Var(ValueType.EXCHANGE_VALUE, coefficient=-0.054),
        Var(ValueType.CONS_SURPLUS, coefficient=-1.378)
    ]

    INTERACTIONS = [
        ('Provisioning', Var(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=0.053)),
        ('Cultural', Var(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=0.203)),
        ('Provisioning', Var(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=0.144)),
        ('Regulating and Maintenance', Var(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=0.455))
    ]

    SIIKAMAKI = [
        GlobalLayer.FOREST_HABITAT_VALUE,
        GlobalLayer.FOREST_NONWOOD_PRODUCTS_VALUE,
        GlobalLayer.FOREST_RECREATION_VALUE,
        GlobalLayer.FOREST_WATER_SERVICE_VALUE
    ]

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
        Var(ClimateSpatialVariable.MEAN_NDVI_P95, ln=True, coefficient=-6.854),
        Var(ClimateSpatialVariable.DRY_DAYS, ln=True, coefficient=2.663),
        Var(ClimateSpatialVariable.MEAN_ANNUAL_TEMPERATURE, ln=True, coefficient=-0.737),
        Var(ClimateSpatialVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, coefficient=2.063),
        Var(BenefitSpatialVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=4.000),
        Var(BenefitSpatialVariable.ROAD_DENSITY, ln=True, coefficient=0.352, buffer=10000),
        Var(BenefitSpatialVariable.SETTLEMENTS, ln=True, coefficient=0.912, buffer=10000),
        Var(BenefitSpatialVariable.LAND_COVER, lc=LandCoverGroup.FOREST, coefficient=0.004, buffer=30000),
        Var(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=-0.199, buffer=10000),
        Var(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=0.154)
    ]

    SUB_BIOMES = [
        Var(SubBiome.TEMPERATE_EVERGREEN_FOREST, coefficient=1.835),
        Var(SubBiome.OTHER,coefficient= 0.00)
    ]

    ECOSYSTEM_SERVICES = [
        Var(EcosystemService.WILD_ANIMAL_PROVISION, coefficient=-1.993),
        Var(EcosystemService.WOOD_PROVISION,coefficient= -0.426),
        Var(EcosystemService.WATER_SUPPLY,coefficient= -2.601),
        Var(EcosystemService.AIR_FILTRATION, coefficient=-0.834),
        Var(EcosystemService.NUTRIENT_RETENTION, coefficient=-3.167),
        Var(EcosystemService.RAINFALL_REGULATION, coefficient=-1.218),
        Var(EcosystemService.SOIL_EROSION_REGULATION, coefficient=-0.731),
        Var(EcosystemService.SOIL_QUALITY_REGULATION, coefficient=-1.791),
        Var(EcosystemService.RECREATION,coefficient= -1.771),
    ]

    VALUE_TYPES = [
        Var(ValueType.EXCHANGE_VALUE, coefficient=-1.929),
        Var(ValueType.CONS_SURPLUS, coefficient=-0.649)
    ]

    INTERACTIONS = [
        ('reg', Var(BenefitSpatialVariable.BIODIVERSITY_INTACTNESS, coefficient=-0.414)),
        ('cult', Var(BenefitSpatialVariable.BIODIVERSITY_INTACTNESS, coefficient=1.222))
    ]

    SIIKAMAKI = [
        GlobalLayer.FOREST_HABITAT_VALUE,
        GlobalLayer.FOREST_NONWOOD_PRODUCTS_VALUE,
        GlobalLayer.FOREST_RECREATION_VALUE,
        GlobalLayer.FOREST_WATER_SERVICE_VALUE
    ]

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
        Var(BenefitSpatialVariable.NPP_SHARE, ln=True, coefficient=0.986),  # EPI_ln -> NPP_SHARE
        Var(BenefitSpatialVariable.NIGHT_LIGHT, coefficient=-0.053),  # nightLight
        Var(ClimateSpatialVariable.DRY_DAYS, ln=True, coefficient=-2.351),  # dryDays_ln
        Var(ClimateSpatialVariable.MEAN_ANNUAL_TEMPERATURE, ln=True, coefficient=1.278),  # Temp_mean_ln
        Var(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=0.639),  # GNIPC_ln
        Var(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=0.252, buffer=10000)  # popDensity_buf_A_ln (buffer A = 10km)
    ]


    SUB_BIOMES = [
        Var(SubBiome.CROPLAND_ANNUAL, coefficient=1.108),  # Cropland_Annual
        Var(SubBiome.MONOCULTURE_PERENNIAL,coefficient= 1.524),
        Var(SubBiome.OTHER, coefficient=0.00)
    ]

    ECOSYSTEM_SERVICES = [
        Var(EcosystemService.CROP_PROVISION,coefficient= 1.614),  # S_Crop_Prov
        Var(EcosystemService.WOOD_PROVISION, coefficient=0.876),  # S_Wood_Prov
        Var(EcosystemService.LIVESTOCK_PROVISION,coefficient= -1.418),  # S_Livestock
        Var(EcosystemService.POLLINATION, coefficient=1.087),  # S_Pollination
        Var(EcosystemService.SOIL_EROSION_REGULATION,coefficient= 2.174),  # S_Soil_Erosion_Reg
        Var(EcosystemService.WATER_FLOW_REGULATION, coefficient=6.46),  # S_Water_Flow_Reg
        Var(EcosystemService.RECREATION,coefficient= -1.062),  # S_Recreation
        Var(EcosystemService.VISUAL_AMENITY,coefficient= -1.889)  # S_Visual_Amenity
    ]

    VALUE_TYPES = [
        Var(ValueType.EXCHANGE_VALUE, coefficient=2.102),  # Exchange value
        Var(ValueType.CONS_SURPLUS,coefficient= 0.547)  # Consumer surplus
    ]

    INTERACTIONS = [
        ('Provisioning', Var(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=-0.192)),  # GNIPC_ESprov
        ('Provisioning', Var(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=0.34))  # PopD_ESprov
    ]

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
        Var(BenefitSpatialVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=1.211),  # biodivIntactness_ln
        Var(BenefitSpatialVariable.FRAGMENTATION, ln=True, coefficient=-0.895, buffer=10000),  # fragmentation_buf_A_ln (buffer A = 10km)
        Var(ClimateSpatialVariable.DRY_DAYS, ln=True, coefficient=0.612),  # dryDays_ln
        Var(ClimateSpatialVariable.HEAVY_RAIN_DAYS, ln=True, coefficient=-0.928),  # rainDays_ln -> HEAVY_RAIN_DAYS
        Var(ClimateSpatialVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, coefficient=1.475),  # Precip_total_ln
        Var(ClimateSpatialVariable.MEAN_NDVI_P95, ln=True, coefficient=-2.507),  # NDVI_ln
        Var(BenefitSpatialVariable.LAND_COVER, coefficient=0.003, buffer=30000, lc=LandCoverGroup.MANGROVE),
        Var(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=0.309, buffer=10000),  # popDensity_buf_A_ln (buffer A = 10km)
        Var(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=0.461)  # GNIPC_ln
    ]

    SUB_BIOMES = []

    ECOSYSTEM_SERVICES = [
        Var(EcosystemService.WILD_FISH_PROVISION, coefficient=0.562),  # S_Wild_Fish_Prov
        Var(EcosystemService.AQUACULTURE, coefficient=0.793),  # S_Aquaculture
        Var(EcosystemService.WOOD_PROVISION, coefficient=-0.199),  # S_Wood_Prov
        Var(EcosystemService.WILD_ANIMAL_PROVISION,coefficient= -0.895),  # S_Wild_Animal_Prov
        Var(EcosystemService.SOIL_EROSION_REGULATION, coefficient=0.768),  # S_Soil_Erosion_Reg
        Var(EcosystemService.GLOBAL_CLIMATE, coefficient=2.075)  # S_Global_Climate
    ]

    VALUE_TYPES = [
        Var(ValueType.EXCHANGE_VALUE, coefficient=-0.058),  # Exchange value
        Var(ValueType.CONS_SURPLUS,coefficient= -0.731)  # Consumer surplus
    ]

    INTERACTIONS = []

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
        Var(BenefitSpatialVariable.BIODIVERSITY_INTACTNESS, ln=True, coefficient=6.928),  # biodivIntactness_ln
        Var(BenefitSpatialVariable.NPP_SHARE, ln=True, coefficient=0.427),  # EPI_ln -> NPP_SHARE
        Var(BenefitSpatialVariable.HUMAN_MODIF_INDEX, ln=True, coefficient=1.708),  # humanModification_ln
        Var(ClimateSpatialVariable.DRY_DAYS, ln=True, coefficient=-7.536),  # dryDays_ln
        Var(ClimateSpatialVariable.HEAVY_RAIN_DAYS, ln=True, coefficient=3.39),  # rainDays_ln -> HEAVY_RAIN_DAYS
        Var(ClimateSpatialVariable.TOTAL_ANNUAL_PRECIPITATION, ln=True, coefficient=-9.538),  # Precip_total_ln
        Var(ClimateSpatialVariable.MEAN_NDVI_P95, ln=True, coefficient=3.432),  # NDVI_ln
        Var(BenefitSpatialVariable.POP_DENSITY, ln=True, coefficient=-0.936, buffer=10000),# popDensity_buf_A_ln (buffer A = 10km)
        Var(CountrySpatialVariable.GNI_PER_CAPITA, ln=True, coefficient=-1.309)  # GNIPC_ln
    ]

    ECOSYSTEM_SERVICES = [
        Var(EcosystemService.WILD_ANIMAL_PROVISION,coefficient= -0.481),  # S_Wild_Animal_Prov
        Var(EcosystemService.WATER_SUPPLY,coefficient= -1.271),  # S_Water_Supply
        Var(EcosystemService.GRAZED_BIOMASS_PROVISION, coefficient=1.567),  # S_Grazed_Biomass
        Var(EcosystemService.LIVESTOCK_PROVISION,coefficient= 4.625),  # S_Livestock
        Var(EcosystemService.POLLINATION,coefficient= 0.603),  # S_Pollination
        Var(EcosystemService.NUTRIENT_RETENTION,coefficient= -3.6),  # S_Nutrient_Retention
        Var(EcosystemService.RIVER_FLOOD_REGULATION, coefficient=-4.297),  # S_River_Flood_Reg
        Var(EcosystemService.SOIL_EROSION_REGULATION, coefficient=-6.053),  # S_Soil_Erosion_Reg
        Var(EcosystemService.RECREATION,coefficient= -1.504)  # S_Recreation
    ]

    VALUE_TYPES = [
        Var(ValueType.EXCHANGE_VALUE, coefficient=0.968),  # Exchange value
        Var(ValueType.CONS_SURPLUS,coefficient= -0.078)  # Consumer surplus
    ]

    SUB_BIOMES = []

    INTERACTIONS = []

    GLOBAL_LAYERS = [
        GlobalLayer.RESTORATION_OPPORTUNITY_COST,
        GlobalLayer.EXOTIC_IMPLEMENTATION_COST,
        GlobalLayer.NATIVE_IMPLEMENTATION_COST,
        GlobalLayer.REGENERATION_IMPLEMENTATION_COST
    ]


