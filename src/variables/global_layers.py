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


class GlobalLayer:

    RESTORATION_OPPORTUNITY_COST = GlobalLayerData(
        name="RESTORATION_OPPORTUNITY_COST",
        full_name= "Restoration Opportunity Cost",
        description="NBS annual opportunity cost based on Busch et al. (2024)",
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
        description="Implementation cost of restoring tree cover for passive regeneration based on Busch et al. (2024)",
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
        description="Implementation cost of restoring tree cover for plantation of native species based on Busch et al. (2024)",
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
        description="Implementation cost of restoring tree cover for plantation of introduced species based on Busch et al. (2024)",
        gcs_path="data/global_data/cost/se_plan/implementation_cost.tif",
        unit='2020 USD/ha',
        source='https://www.nature.com/articles/s41558-024-02068-1',
        scale=1000,
        band=3,
        bucket='nbs-tool-public'
    )

    FOREST_RECREATION_VALUE = GlobalLayerData(
        name="FOREST_RECREATION_VALUE",
        full_name="Forest Recreation Value",
        description="Forest recreation value based on Siikamaki et al. (2024)",
        gcs_path="data/global_data/benefit/siikamaki/rec_2020_global_4326.tif",
        unit='2020 USD/ha',
        source='https://documents.worldbank.org/en/publication/documents-reports/documentdetail/099101124145545368',
        scale=10000,
        band=1,
        bucket='nbs-tool-public'
    )

    FOREST_NONWOOD_PRODUCTS_VALUE = GlobalLayerData(
        name="FOREST_NONWOOD_PRODUCTS_VALUE",
        full_name="Forest Non-Wood Products Value",
        description="Forest non-wood products value based on Siikamaki et al. (2024)",
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
        description="Forest water services value based on Siikamaki et al. (2024)",
        gcs_path="data/global_data/benefit/siikamaki/wat_2020_global_4326.tif",
        unit='2020 USD/ha',
        source='https://documents.worldbank.org/en/publication/documents-reports/documentdetail/099101124145545368',
        scale=10000,
        band=1,
        bucket='nbs-tool-public'
    )

    FOREST_HABITAT_VALUE = GlobalLayerData(
        name="FOREST_HABITAT_VALUE",
        full_name="Forest Habitat Value",
        description="Forest habitat value based on Siikamaki et al. (2024)",
        gcs_path="data/global_data/benefit/siikamaki/hab_2020_global_4326.tif",
        unit='2020 USD/ha',
        source='https://documents.worldbank.org/en/publication/documents-reports/documentdetail/099101124145545368',
        scale=10000,
        band=1,
        bucket='nbs-tool-public'
    )

