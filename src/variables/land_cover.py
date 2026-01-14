from src.variables import variable_template
from dataclasses import dataclass

@dataclass
class LandCoverData(variable_template.Data):
    """Dataclass to store metadata for a variable. This template will be used to create spatial variables"""
    classes: list

    def get_tooltip(self):
        return f"{self.description}"

    def get_name(self, buffer:int = None):
        """Get the name of the variable used in further processing."""
        name = self.name
        if buffer is not None:
            if buffer == 10000:
                name += '_buf_A'
            elif buffer == 30000:
                name += '_buf_B'
            elif buffer == 50000:
                name += '_buf_C'
            else:
                name = name

        return name

class LandCoverGroup:
    FOREST = LandCoverData(
        name='LC_Forest',
        full_name = "Land cover: forest (%)",
        description = 'percentage of the AOI covered in forest',
        classes = ['121', '122', '130', '140', '150', '151', '152', '153', '160', '170', '180', '190'])


    MANGROVE =  LandCoverData(
        name='LC_Mangrove',
        full_name = "Land cover: mangrove (%)",
        description = 'percentage of the AOI covered in mangroves',
        classes =['100', '110', '120'])

