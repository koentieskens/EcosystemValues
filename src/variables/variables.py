
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
    value: float = 0
    lc: LandCoverGroup = None

    @property
    def name(self):
        return self.variable.name if hasattr(self.variable, 'name') else self.variable

