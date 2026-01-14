from src.variables import variable_template
from dataclasses import dataclass


@dataclass
class CostInputData(variable_template.Data):
    """Dataclass to store metadata for a variable. This template will be used to create spatial variables"""
    pass

class CostInputVariable(CostInputData):

    def get_tooltip(self):
        return f"{self.description}"

class CostInput(CostInputVariable):
    MAINTENANCE_DAYS = CostInputData(
        name='Maintenance_Days',
        full_name='Maintenance labor days',
        description='Maintenance labor days are the number of labor days per hectare required to maintain the NBS')
    ESTABLISHMENT_DAYS = CostInputData(
        name='Establishment_Days',
        full_name='Establishment labor days',
        description='Establishment labor days are the number of labor days per hectare required to establish the NBS')