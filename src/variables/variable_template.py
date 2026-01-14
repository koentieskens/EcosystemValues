from enum import Enum
from dataclasses import dataclass

@dataclass
class Data:
    """Dataclass to store metadata for a variable. This template will be used to create variables"""
    name: str
    full_name: str
    description: str

class Variable(Enum):

    @property
    def name(self):
        """Get the name of the variable used in further processing."""
        return self.value.name

    @property
    def full_name(self):
        """Get the full name of the variable used for displaying purposes"""
        return self.value.full_name

    @property
    def description(self):
        """Get the description of the variable. Used for tooltip"""
        return self.value.description

class Var:

    def __init__(self, var: Enum, ln:bool=False, lc:Enum=None, buffer:int=None, coefficient:float=None):
        self.var = var
        self.ln = ln
        self.lc = lc
        self.buffer = buffer
        self.coefficient = coefficient
        self.value = 0