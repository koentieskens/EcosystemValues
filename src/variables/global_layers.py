from .spatial_variable import GlobalLayer, GlobalLayerData


class GCSLayer(GlobalLayer):

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

