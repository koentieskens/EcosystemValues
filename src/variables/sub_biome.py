from src.variables import variable_template
from dataclasses import dataclass


@dataclass
class SubBiomeData(variable_template.Data):
    """Dataclass to store metadata for a variable. This template will be used to create spatial variables"""

class SubBiomeVariable(variable_template.Variable):

    def get_tooltip(self):
        return (
                f"{self.value.name}\n\n"
                f"{self.value.description}")

class SubBiome(SubBiomeVariable):

    TROPICAL_MIXED_FORESTS = SubBiomeData(
        name='Tropical_mixed_forest',
        full_name='Tropical mixed forest',
        description='Tropical mixed forests are found in tropical areas and are characterized by seasonal rainfall patterns with distinct long wet and shorter dry seasons'
    )

    TROPICAL_DRY_FORESTS = SubBiomeData(
        name='Tropical_Dry_Forest',
        full_name='Tropical dry forest',
        description='Tropical dry forests are found in tropical areas and are characterized by seasonal rainfall patterns with distinct wet and long dry seasons'
    )

    TEMPERATE_EVERGREEN_FOREST = SubBiomeData(
        name='Temperate_Evergreen_Forest',
        full_name='Temperate evergreen forest',
        description='Temperate evergreen forests are dominated by coniferous trees that retain their foliage year-round'
    )

    CROPLAND_ANNUAL = SubBiomeData(
        name='Cropland_Annual',
        full_name='Cropland annual',
        description='Cropland annual refers to agricultural areas used for growing annual crops that complete their life cycle in one growing season'
    )

    MONOCULTURE_PERENNIAL = SubBiomeData(
        name='Monoculture_Perennial',
        full_name='Monoculture perennial',
        description='Monoculture perennial represents agricultural systems focused on single species of perennial crops that live for multiple years'
    )

    OTHER = SubBiomeData(
        name='Other',
        full_name='Other',
        description='Other sub-biome type not specifically categorized above'
    )