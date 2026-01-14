
from typing import Union
from src.variables.land_cover import LandCoverGroup
from src.variables.cost_input import CostInput
from src.variables.ecosystem_service import EcosystemService
from src.variables.nature_based_solutions import NBS
from src.variables.global_layers import GlobalLayer
from src.variables.spatial_variable import BenefitSpatialVariable, ClimateSpatialVariable, CountrySpatialVariable
from src.variables.sub_biome import SubBiome
from src.variables.value_type import ValueType


class Var:

    def __init__(self,
                 variable: Union[
                     CostInput, EcosystemService, NBS, GlobalLayer, BenefitSpatialVariable, ClimateSpatialVariable,
                  CountrySpatialVariable, SubBiome, ValueType],
                 ln:bool=False,
                 ihs:bool=False,
                 lc:LandCoverGroup=None,
                 buffer:int=None,
                 coefficient:float=None
                 ):
        self.variable = variable
        self.ln = ln
        self.ihs = ihs
        self.lc = lc
        self.buffer = buffer
        self.coefficient = coefficient
        self.value = 0


