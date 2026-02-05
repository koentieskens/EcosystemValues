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
        name='Cross-slope measure',
        full_name='Cross-slope measure',
        description='NBS 4 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )

    NBS_10 = NBSData(
        name='Improved ground/ vegetation cover',
        full_name='Improved ground/ vegetation cover',
        description='NBS 10 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )

    NBS_14 = NBSData(
        name='Integrated soil fertility management',
        full_name='Integrated soil fertility management',
        description='NBS 14 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )

    NBS_16 = NBSData(
        name='Minimal soil disturbance',
        full_name='Minimal soil disturbance',
        description='NBS 16 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )

    NBS_21 = NBSData(
        name='Rotational systems (crop rotation, fallows, shifting cultivation)',
        full_name='Rotational systems (crop rotation, fallows, shifting cultivation)',
        description='NBS 21 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )

    NBS_30 = NBSData(
        name='Trees in plots',
        full_name='Trees in plots',
        description='NBS 30 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )

    NBS_31 = NBSData(
        name='Integrated crop livestock',
        full_name='Integrated crop livestock',
        description='NBS 31 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )

    NBS_32 = NBSData(
        name='Water management',
        full_name='Water management',
        description='NBS 32 is a certain NBS that we calculated costs for',
        data_source='WOCAT'
    )