
from dataclasses import dataclass

@dataclass
class Data:
    """Dataclass to store metadata for a variable. This template will be used to create variables"""
    name: str
    full_name: str
    description: str
