from dataclasses import dataclass
from src.variables import variable_template

@dataclass
class GlobalLayerData( variable_template.Data):
    """Dataclass to store metadata for a variable. This template will be used to create spatial variables"""
    unit: str
    gcs_path: str
    source: str
    scale: int
    band: int
    bucket: str

    @classmethod
    def to_dataframe(cls):
        """
        Create a pandas DataFrame with one row for each enum member and a column for each parameter.

        Returns:
            pd.DataFrame: DataFrame containing all enum members and their properties
        """
        import pandas as pd

        variables = [getattr(cls, attr) for attr in dir(cls)
                     if not attr.startswith('_') and not callable(getattr(cls, attr))]

        data = []
        for var in variables:
            if hasattr(var, 'name'):  # Only include your data objects
                row = {
                    'name': var.name,
                    'full_name': var.full_name,
                    'description': getattr(var, 'description', None),
                    'unit': getattr(var, 'unit', None),
                    'gcs_path': getattr(var, 'gee_path', None),
                    'source': getattr(var, 'source', None),
                    'scale': getattr(var, 'scale', None),
                }
                data.append(row)

        return pd.DataFrame(data)

    def get_tooltip(self):
        return f'{self.description}\n\nSource: {self.source}'


class GlobalLayer:

    RESTORATION_OPPORTUNITY_COST = GlobalLayerData(
        name="RESTORATION_OPPORTUNITY_COST",
        full_name= "Restoration Opportunity Cost",
        description="""NBS annual opportunity cost based on Busch et al. (2024),
        Costs are summed over a period of 30 years and time-discounted at a rate of 5% annually.""",
        gcs_path="data/global_data/cost/se_plan/opportunity_cost.tif",
        unit='2020 USD/ha/yr',
        source='https://www.nature.com/articles/s41558-024-02068-1',
        scale=1000,
        band=1,
        bucket='nbs-tool-public'
    )

    REGENERATION_IMPLEMENTATION_COST = GlobalLayerData(
        name="REGENERATION_IMPLEMENTATION_COST",
        full_name="Implementation Cost (natural regeneration)",
        description="""Implementation cost of restoring tree cover for passive regeneration based on Busch et al. (2024),
        Costs are summed over a period of 30 years and time-discounted at a rate of 5% annually.""",
        gcs_path="data/global_data/cost/se_plan/implementation_cost.tif",
        unit='2020 USD/ha',
        source='https://www.nature.com/articles/s41558-024-02068-1',
        scale=1000,
        band=1,
        bucket='nbs-tool-public'
    )

    NATIVE_IMPLEMENTATION_COST = GlobalLayerData(
        name="NATIVE_IMPLEMENTATION_COST",
        full_name="Implementation Cost (native species)",
        description="""Implementation cost of restoring tree cover for plantation of native species based on Busch et al. (2024),
        Costs are summed over a period of 30 years and time-discounted at a rate of 5% annually.""",
        gcs_path="data/global_data/cost/se_plan/implementation_cost.tif",
        unit='2020 USD/ha',
        source='https://www.nature.com/articles/s41558-024-02068-1',
        scale=1000,
        band=2,
        bucket='nbs-tool-public'
    )

    EXOTIC_IMPLEMENTATION_COST = GlobalLayerData(
        name="EXOTIC_IMPLEMENTATION_COST",
        full_name="Implementation Cost (introduced species)",
        description="""Implementation cost of restoring tree cover for plantation of introduced species based on Busch et al. (2024),
        Costs are summed over a period of 30 years and time-discounted at a rate of 5% annually.""",
        gcs_path="data/global_data/cost/se_plan/implementation_cost.tif",
        unit='2020 USD/ha',
        source='https://www.nature.com/articles/s41558-024-02068-1',
        scale=1000,
        band=3,
        bucket='nbs-tool-public'
    )

    FOREST_RECREATION_VALUE = GlobalLayerData(
        name="FOREST_RECREATION_VALUE",
        full_name="Recreation, hunting and fishing",
        description="Recreation-related services are the ecosystem contributions, in particular through the biophysical characteristics and qualities of ecosystems, that enable people to use and enjoy the environment through direct, in-situ, physical and experiential interactions with the environment. This includes services to both locals and non-locals (i.e., visitors, including tourists). Recreation-related services may also be supplied to those undertaking recreational fishing and hunting. This is a final ecosystem service.",
        gcs_path="data/global_data/benefit/siikamaki/rec_2020_global_4326.tif",
        unit='2020 USD/ha',
        source='https://documents.worldbank.org/en/publication/documents-reports/documentdetail/099101124145545368',
        scale=10000,
        band=1,
        bucket='nbs-tool-public'
    )

    FOREST_NONWOOD_PRODUCTS_VALUE = GlobalLayerData(
        name="FOREST_NONWOOD_PRODUCTS_VALUE",
        full_name="Non-wood forest products",
        description="Wild animals, plants and other biomass provisioning services are the ecosystem contributions to the growth of wild animals, plants and other biomass that are captured and harvested in uncultivated production contexts by economic units for various uses. The scope includes non-wood forest products (NWFP) and services related to hunting, trapping and bio-prospecting activities; but excludes wild fish and other natural aquatic biomass (included in previous class). This is a final ecosystem service.",
        gcs_path="data/global_data/benefit/siikamaki/nwfp_2020_global_4326.tif",
        unit='2020 USD/ha',
        source='https://documents.worldbank.org/en/publication/documents-reports/documentdetail/099101124145545368',
        scale=10000,
        band=1,
        bucket='nbs-tool-public'
    )

    FOREST_WATER_SERVICE_VALUE = GlobalLayerData(
        name="FOREST_WATER_SERVICE_VALUE",
        full_name="Forest Water Service Value",
        description="A combination of water related services: Water supply, Water purification services, rainfall pattern regulation services, soil erosion control services, Baseline flow maintenance services, Peak flow mitigation services, and River flood mitigation services",
        gcs_path="data/global_data/benefit/siikamaki/wat_2020_global_4326.tif",
        unit='2020 USD/ha',
        source='https://documents.worldbank.org/en/publication/documents-reports/documentdetail/099101124145545368',
        scale=10000,
        band=1,
        bucket='nbs-tool-public'
    )

    FOREST_HABITAT_VALUE = GlobalLayerData(
        name="FOREST_HABITAT_VALUE",
        full_name="Habitat and species protection",
        description="Ecosystem and species appreciation concerns the wellbeing that people derive from the existence and preservation of the environment for current and future generations, irrespective of any direct or indirect use.",
        gcs_path="data/global_data/benefit/siikamaki/hab_2020_global_4326.tif",
        unit='2020 USD/ha',
        source='https://documents.worldbank.org/en/publication/documents-reports/documentdetail/099101124145545368',
        scale=10000,
        band=1,
        bucket='nbs-tool-public'
    )


@dataclass
class GlobalVectorLayerData( variable_template.Data):
    """Dataclass to store metadata for a variable. This template will be used to create spatial variables"""
    unit: str
    gcs_path: str
    source: str
    layer: str
    bucket: str


    @classmethod
    def to_dataframe(cls):
        """
        Create a pandas DataFrame with one row for each enum member and a column for each parameter.

        Returns:
            pd.DataFrame: DataFrame containing all enum members and their properties
        """
        import pandas as pd

        variables = [getattr(cls, attr) for attr in dir(cls)
                     if not attr.startswith('_') and not callable(getattr(cls, attr))]

        data = []
        for var in variables:
            if hasattr(var, 'name'):  # Only include your data objects
                row = {
                    'name': var.name,
                    'full_name': var.full_name,
                    'description': getattr(var, 'description', None),
                    'gcs_path': getattr(var, 'gee_path', None),
                    'source': getattr(var, 'source', None),
                }
                data.append(row)

        return pd.DataFrame(data)

    def get_tooltip(self):
        return f'{self.description}\n\nSource: {self.source}'

class GlobalVectorLayer:

    MANGROVE_FLOOD_BENEFITS = GlobalVectorLayerData(
        name="MANGROVE_FLOOD_BENEFITS",
        full_name="Mangrove flood benefits",
        description="""This work measures the flood protection service of mangroves all over the world for two climatic conditions: (1) Cyclonic- i.e., the conditions high-intensity extreme waves and storm surge induced by tropical cyclones and (2) Non-cyclonic, i.e., the “regular” waves generated by low-intensity local storms.""",
        gcs_path="/vsigs/nbs-tool-public/data/global_data/benefit/menendez/UCSC_CWON_studyunits.gpkg",
        unit='2020 USD',
        source='https://www.nature.com/articles/s41598-020-61136-6',
        layer='UCSC_CWON_studyunits',
        bucket='nbs-tool-public'
    )