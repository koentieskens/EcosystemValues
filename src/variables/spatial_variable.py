from enum import Enum
from dataclasses import dataclass
import copy

@dataclass
class VariableData:
    """Dataclass to store metadata for a variable. This template will be used to create spatial variables"""
    name: str
    full_name: str
    description: str
    aggregation: str
    unit: str
    gee_path: str
    alt_path: str
    extraction_function: callable
    source: str
    scale: int
    multiplier: float = 1.0
    method: str | None = None
    buffer: int | None = None


class Variable(Enum):
    def get_image(self, **kwargs):
        """Get the image for the variable."""
        return self.value.extraction_function(gee_path=self.gee_path, name=self.name, **kwargs)

    @property
    def name(self):
        """Get the name of the variable used in further processing."""
        name = self.value.name
        if self.buffer is not None:
            if self.buffer == 10000:
                name += '_buf_A'
            elif self.buffer == 30000:
                name += '_buf_B'
            elif self.buffer == 50000:
                name += '_buf_C'
            else:
                name = name + '_' + str(self.buffer)

        return name

    @property
    def alt_path(self):
        """
        Get the GEE path of the alternative source. This alternative source is what was originally in the FAO code
        If it differs from gee_path I (koen) have changed it to a public source
        """
        return self.value.alt_path

    @property
    def gee_path(self):
        """Get the GEE path of the variable."""
        return self.value.gee_path

    @property
    def extraction_function(self):
        """Get the extraction function of the variable."""
        return self.value.extraction_function

    @property
    def full_name(self):
        """
        Returns FUll name of the variable for printing and logging functionality
        """
        return self.value.full_name

    @property
    def scale(self):
        """
        Returns desired scale of the variable
        """
        return self.value.scale

    @property
    def multiplier(self):
        """
        Returns desired scale of the variable
        """
        try:
            multiplier = self.value.multiplier
        except:
            multiplier = None
        return multiplier

    @property
    def description(self):
        """Get the description of the variable."""
        return self.value.description

    @property
    def aggregation(self):
        """Get the aggregation method for the variable."""
        return self.value.aggregation

    @property
    def unit(self):
        """Get the unit of measurement for the variable."""
        return self.value.unit

    @property
    def source(self):
        """Get the data source/reference for the variable."""
        return self.value.source

    @property
    def method(self):
        """Get the data extracting method group for the variable."""
        return self.value.method

    @property
    def buffer(self):
        """Get the buffer witdth for the variable."""
        return self.value.buffer

    @buffer.setter
    def buffer(self, value):
        """Set the buffer witdth for the variable."""
        self.value.buffer = value

    @classmethod
    def to_dataframe(cls):
        """
        Create a pandas DataFrame with one row for each enum member and a column for each parameter.

        Returns:
            pd.DataFrame: DataFrame containing all enum members and their properties
        """
        import pandas as pd

        data = []
        for member in cls:
            row = {
                'name': member.value.name,
                'full_name': member.value.full_name,
                'description': getattr(member.value, 'description', None),
                'aggregation': getattr(member.value, 'aggregation', None),
                'unit': getattr(member.value, 'unit', None),
                'gee_path': member.value.gee_path,
                'alt_path': member.value.alt_path,
                'extraction_function': member.value.extraction_function.__name__ if hasattr(
                    member.value.extraction_function, '__name__') else str(member.value.extraction_function),
                'source': getattr(member.value, 'source', None),
                'scale': member.value.scale,
                'multiplier': getattr(member.value, 'multiplier', None)
            }
            data.append(row)

        return pd.DataFrame(data)

@dataclass
class GlobalLayerData:
    """Dataclass to store metadata for a variable. This template will be used to create spatial variables"""
    name: str
    full_name: str
    description: str
    unit: str
    gcs_path: str
    source: str
    scale: int
    band: int
    bucket: str

class GlobalLayer(Enum):

    @property
    def name(self):
        """Get the name of the variable used in further processing."""
        return self.value.name

    @property
    def gcs_path(self):
        """Get the GEE path of the variable."""
        return self.value.gcs_path

    @property
    def full_name(self):
        """
        Returns FUll name of the variable for printing and logging functionality
        """
        return self.value.full_name

    @property
    def scale(self):
        """
        Returns desired scale of the variable
        """
        return self.value.scale

    @property
    def description(self):
        """Get the description of the variable."""
        return self.value.description

    @property
    def unit(self):
        """Get the unit of measurement for the variable."""
        return self.value.unit

    @property
    def source(self):
        """Get the data source/reference for the variable."""
        return self.value.source

    @property
    def band(self):
        """Get the band of the variable."""
        return self.value.band

    @property
    def bucket(self):
        """Get the bucket where the data is stored in GCS."""
        return self.value.bucket

    @classmethod
    def to_dataframe(cls):
        """
        Create a pandas DataFrame with one row for each enum member and a column for each parameter.

        Returns:
            pd.DataFrame: DataFrame containing all enum members and their properties
        """
        import pandas as pd

        data = []
        for member in cls:
            row = {
                'name': member.value.name,
                'full_name': member.value.full_name,
                'description': getattr(member.value, 'description', None),
                'unit': getattr(member.value, 'unit', None),
                'gcs_path': member.value.gee_path,
                'source': getattr(member.value, 'source', None),
                'scale': member.value.scale,
            }
            data.append(row)

        return pd.DataFrame(data)
