from enum import Enum
from typing import Union

class EcosystemServices(Enum):
    WOOD_PROVISION = 'wood_provision', 'Wood provision', 'prov'
    WILD_FISH_PROVISION = 'wild_fish_provision', 'Wild fish provision', 'prov'
    AQUACULTURE = 'aquaculture', 'Aquaculture', 'prov'
    WILD_ANIMAL_PROVISION = 'wild_animal_provision', 'Wild animal provision', 'prov'
    CROP_PROVISION = 'crop_provision', 'Crop provision', 'prov'
    GRAZED_BIOMASS_PROVISION = 'grazed_biomass_provision', 'Grazed biomass provision', 'prov'
    LIVESTOCK_PROVISION = 'livestock_provision', 'Livestock provision', 'prov'
    PEST_CONTROL = 'pest_control', 'Pest control', 'preg'
    NUTRIENT_RETENTION = 'nutrient_retention', 'Nutrient retention', 'reg'
    WATER_SUPPLY = 'water_supply', 'Water supply', 'prov'
    AIR_FILTRATION = 'air_filtration', 'Air filtration', 'reg'
    GLOBAL_CLIMATE = 'global_climate', 'Global climate', 'reg'
    POLLINATION = 'pollination', 'Pollination', 'reg'
    WATER_FLOW_REGULATION = 'water_flow_regulation', 'Water flow regulation', 'reg'
    VISUAL_AMENITY = 'visual_amenity', 'Visual amenity', 'cul'
    RAINFALL_REGULATION = 'rainfall_regulation', 'Rainfall regulation', 'reg'
    RIVER_FLOOD_REGULATION = 'river_flood_regulation', 'River flood regulation', 'reg'
    SOIL_EROSION_REGULATION = 'soil_erosion_regulation', 'Soil erosion regulation', 'reg'
    SOIL_QUALITY_REGULATION = 'soil_quality_regulation', 'Soil quality regulation', 'reg'
    RECREATION = 'recreation', 'Recreation', 'cul'

class ProjectVariables(Enum):
    TROPICAL_MIXED_FORESTS = 'Tropical_Mixed_Forest', 'Tropical mixed forest'
    TROPICAL_DRY_FORESTS = 'Tropical_Dry_Forest', 'Tropical dry forest'
    TEMPERATE_EVERGREEN_FOREST = 'Temperate_Evergreen_Forest', 'Temperate evergreen forest'
    CROPLAND_ANNUAL = 'Cropland_Annual', 'Cropland annual'
    MONOCULTURE_PERENNIAL = 'Monoculture_Perennial', 'Monoculture perennial'
    OTHER = 'Other', 'Other'
    FOOD = 'Food', 'Food'
    AIR_QUALITY = 'Air_Quality', 'Air quality'
    RECREATION_TOURISM = 'Recreation_Tourism', 'Recreation tourism'
    RAW_MATERIALS = 'Raw_Materials', 'Raw materials'
    WATER_PROV = 'Water_Prov', 'Water provision'
    POLLINATION = 'Pollination', 'Pollination'
    CLIMATE_REG = 'Climate_Reg', 'Climate regulation'
    EROSION_REG = 'Erosion_Reg', 'Erosion regulation'
    EXISTENCE_BEQUEST = 'Existence_Bequest', 'Existence bequest'
    TOTAL_FLOW = 'Total_Flow', 'Total flow'
    EXCHANGE_VALUE = 'Exchange_Value', 'Exchange value'
    CONS_SURPLUS = 'Cons_Surplus', 'Consumer surplus'
    BIO_CONTROL = 'Bio_Control', 'Bio control'
    WATER_FLOW_REG = 'Water_Flow_Reg', 'Water flow regulation'
    MAINTAIN_LIFE_CYCLE = 'Maintain_Life_Cycle', 'Maintain life cycle'
    MAINTAIN_SOIL = 'Maintain_Soil', 'Maintain soil'
    COGNITIVE_DEVELOPMENT = 'Cognitive_Development', 'Cognitive development'
    WASTE_TREATMENT = 'Waste_Treatment', 'Waste treatment'


class Pvar:

    def __init__(self, variable: Union[ProjectVariables, EcosystemServices], coefficient: float):
        self.variable = variable
        self.coefficient = coefficient
        self.value = 0
