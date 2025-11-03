from enum import Enum

class ProjectVariables(Enum):

    TROPICAL_MIXED_FORESTS = 'Tropical_Mixed_Forest', 'Tropical mixed forest'
    TROPICAL_DRY_FORESTS = 'Tropical_Dry_Forest', 'Tropical dry forest'
    TEMPERATE_EVERGREEN_FOREST = 'Temperate_Evergreen_Forest', 'Temperate evergreen forest'
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
    CROPLAND_ANNUAL = 'Cropland_Annual', 'Cropland annual'
    MONOCULTURE_PERRENIAL = 'Monoculture_Perrenial', 'Monoculture perrenial'
    BIO_CONTROL = 'Bio_Control', 'Bio control'
    WATER_FLOW_REG = 'Water_Flow_Reg', 'Water flow regulation'
    MAINTAIN_LIFE_CYCLE = 'Maintain_Life_Cycle', 'Maintain life cycle'
    MAINTAIN_SOIL = 'Maintain_Soil', 'Maintain soil'
    COGNITIVE_DEVELOPMENT = 'Cognitive_Development', 'Cognitive development'
    WASTE_TREATMENT = 'Waste_Treatment', 'Waste treatment'


class Pvar:

    def __init__(self, variable: ProjectVariables, coefficient: float):
        self.variable = variable
        self.coefficient = coefficient
