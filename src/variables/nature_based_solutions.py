from src.variables import variable_template
from dataclasses import dataclass

@dataclass
class NBSData(variable_template.Data):
    """Dataclass to store metadata for a variable. This template will be used to create spatial variables"""
    data_source: str

    def get_tooltip(self):
        return (f"NBS Classification\n\n"
                f"Name: {self.name}"
                f"{self.description}\n\n"
                f"Value estimate based on: {self.data_source}")


class NBS:

    NBS_4 = NBSData(
        name='NBS 4',
        full_name='nbs_4',
        description='NBS 4 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )

    NBS_10 = NBSData(
        name='NBS 10',
        full_name='nbs_10',
        description='NBS 10 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )

    NBS_14 = NBSData(
        name='NBS 14',
        full_name='nbs_14',
        description='NBS 14 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )

    NBS_16 = NBSData(
        name='NBS 16',
        full_name='nbs_16',
        description='NBS 16 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )

    NBS_21 = NBSData(
        name='NBS 21',
        full_name='nbs_21',
        description='NBS 21 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )

    NBS_30 = NBSData(
        name='NBS 30',
        full_name='nbs_30',
        description='NBS 30 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )

    NBS_31 = NBSData(
        name='NBS 31',
        full_name='nbs_31',
        description='NBS 31 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )

    NBS_32 = NBSData(
        name='NBS 32',
        full_name='nbs_32',
        description='NBS 32 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )