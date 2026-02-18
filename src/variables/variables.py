
from typing import Union
from dataclasses import dataclass
from typing import Optional, Any
from src.variables.land_cover import LandCoverGroup


@dataclass
class ModelVariable:
    variable: Union[str, Any]  # Can be string or domain object
    coefficient: Optional[float] = None
    ln: bool = False
    ihs: bool = False
    buffer: Optional[int] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    value: float = 0
    lc: LandCoverGroup = None
    cost_value: float = 0
    cons_surplus: float = 0
    exchange_value: float = 0


    @property
    def name(self):
        if self.lc is not None:
            name = self.lc.name
        else:
            name = self.variable.name if hasattr(self.variable, 'name') else self.variable
        return name

    @property
    def full_name(self):
        if self.lc is not None:
            full_name = self.lc.full_name
        else:
            full_name = self.variable.full_name if hasattr(self.variable, 'full_name') else self.variable
        return full_name

    @property
    def description(self):
        if self.lc is not None:
            description = self.lc.description
        else:
            description = self.variable.description if hasattr(self.variable, 'description') else self.variable
        return description


