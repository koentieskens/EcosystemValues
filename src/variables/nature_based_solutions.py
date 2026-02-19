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
        description='Cross slope are Constructed on Sloping Lands in the Form of Earth or Soil Bunds, Stone Lines, or Vegetative Strips etc., for Reducing Runoff Velocity and Soil Erosion.',
        data_source='Original meta-analytic value function using SLM cost data from Reynolds et al., 2024, https://wocat.net/documents/1122/WOCAT_Methodological_Paper_Final_Draft.pdf'
    )

    NBS_10 = NBSData(
        name='Improved ground/ vegetation cover',
        full_name='Improved ground/ vegetation cover',
        description='Any Measures that aim to improve the ground cover through dead material/mulch/vegetation.',
        data_source='Original meta-analytic value function using SLM cost data from Reynolds et al., 2024, https://wocat.net/documents/1122/WOCAT_Methodological_Paper_Final_Draft.pdf'
    )

    NBS_14 = NBSData(
        name='Integrated soil fertility management',
        full_name='Integrated soil fertility management',
        description='IFSM Aims at Managing Soil by Combining  Different Methods of Soil Fertility Amendment Together with Soil and Water Conservation. IFSM is Based on Three Principles: 1)Maximising the Use of Organic Sources of Fertilizer(e.g. Manure and Compost Application, Nitrogen-Fixing Green Manure and Cover Crops). 2) Minimising the Loss of Nutrients. 3) Judiciously Using Inorganic Fertilizer According to the Needs and Economic Availability.',
        data_source='Original meta-analytic value function using SLM cost data from Reynolds et al., 2024, https://wocat.net/documents/1122/WOCAT_Methodological_Paper_Final_Draft.pdf'
    )

    NBS_16 = NBSData(
        name='Minimal soil disturbance',
        full_name='Minimal soil disturbance',
        description='Refers to no-tillage or low soil disturbance only in small strips and/ or shallow depth and direct seeding.',
        data_source='Original meta-analytic value function using SLM cost data from Reynolds et al., 2024, https://wocat.net/documents/1122/WOCAT_Methodological_Paper_Final_Draft.pdf'
    )

    NBS_21 = NBSData(
        name='Rotational systems (crop rotation, fallows, shifting cultivation)',
        full_name='Rotational systems (crop rotation, fallows, shifting cultivation)',
        description='Is the practice of growing a series of dissimilar/ different types of crops/ plants in the same area in sequenced season, letting it fallow for a period of time, shifting cultivation is an agricultural system in which plots of land are cultivated temporarily, then abandoned and allowed to revert to their natural vegetation while the cultivator moves on to another plot.',
        data_source='Original met-analytic value function using SLM cost data from Reynolds et al., 2024, https://wocat.net/documents/1122/WOCAT_Methodological_Paper_Final_Draft.pdf'
    )

    NBS_30 = NBSData(
        name='Trees in plots',
        full_name='Trees in plots',
        description='Trees in plots',
        data_source='Original met-analytic value function using SLM cost data from Reynolds et al., 2024, https://wocat.net/documents/1122/WOCAT_Methodological_Paper_Final_Draft.pdf'
    )

    NBS_31 = NBSData(
        name='Integrated crop livestock',
        full_name='Integrated crop livestock',
        description='Optimizes the uses of crop and livestock resources through interaction and the creation of synergies.',
        data_source='Original met-analytic value function using SLM cost data from Reynolds et al., 2024, https://wocat.net/documents/1122/WOCAT_Methodological_Paper_Final_Draft.pdf'
    )

    NBS_32 = NBSData(
        name='Water management',
        full_name='Water management',
        description='Involves the protection of springs, rivers, and lakes from pollution, high water flows(floods), or over-abstraction of water, as well as protection measures against damage from waterbodies (e.g. river bank erosion, floods, tidal erosion).',
        data_source='Original met-analytic value function using SLM cost data from Reynolds et al., 2024, https://wocat.net/documents/1122/WOCAT_Methodological_Paper_Final_Draft.pdf'
    )