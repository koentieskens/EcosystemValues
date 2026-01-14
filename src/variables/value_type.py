from src.variables import variable_template
from dataclasses import dataclass


@dataclass
class ValueTypeData(variable_template.Data):
    """Dataclass to store metadata for a variable. This template will be used to create spatial variables"""
    pass

class ValueTypeVariable(variable_template.Variable):

    def get_tooltip(self):
        return (
                f"{self.value.full_name}\n\n"
                f"{self.value.description}")

class ValueType(ValueTypeVariable):
    TOTAL_FLOW = ValueTypeData(
        name='Total_Flow',
        full_name='Total flow',
        description='Total flow is the sum of all ecosystem service flows')


    EXCHANGE_VALUE = ValueTypeData(
        name='Exchange_Value',
        full_name='Exchange value',
        description='The hypothetical price at which a service could be bought and sold in a market, reflecting its economic worth as a traded commodity, distinct from its direct utility or broader societal benefits'
    )

    CONS_SURPLUS = ValueTypeData(
        name='Cons_Surplus',
        full_name='Consumer surplus',
        description='The difference between the total economic value of a service and its direct utility, reflecting the potential benefits of the service to consumers')
