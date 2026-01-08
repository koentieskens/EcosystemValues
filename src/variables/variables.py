
from .spatial_variable import Variable, VariableData
from ..extract_data.get_images import GeeImageExtractor as GEE
from .land_cover import LandCoverGroup


class BenefitVariable(Variable):
    """Enum to represent spatial variables that can be extracted for given points."""

    ACCESSIBILITY = VariableData(
        name='accessibility',
        full_name='Accessibility',
        description='Time to nearest city/town',
        aggregation='mean',
        unit='minutes',
        gee_path='projects/ee-maidiesinitam/assets/valueFunctions/accessibility_city_2015',
        alt_path='projects/ee-maidiesinitam/assets/valueFunctions/accessibility_city_2015',
        extraction_function=GEE.get_accessibility,
        source='https://www.nature.com/articles/nature25181',
        scale=927
    )

    AIRPOLLUTION = VariableData(
        name='airPollution',
        full_name='Air pollution',
        description='Concentration of PM2.5',
        aggregation='mean',
        unit='ug/M^3',
        alt_path='projects/sat-io/open-datasets/GLOBAL-SATELLITE-PM25/ANNUAL',
        gee_path='projects/ee-maidiesinitam/assets/nasa-pm-25',
        extraction_function=GEE.get_image_from_timeseries,
        source='https://www.earthdata.nasa.gov/data/catalog/sedac-ciesin-sedac-sdei-gwrpm25-mmsaod-4gl03-4.03#toc-copy-citation',
        scale=1113
    )

    ALIEN_SPECIES = VariableData(
        name='alienSpecies',
        full_name=' Alien species',
        description='Number of species that are non-native',
        aggregation='mean',
        unit='number of species',
        gee_path='projects/ee-maidiesinitam/assets/valueFunctions/alienSpeciesImg',
        alt_path='projects/ee-maidiesinitam/assets/valueFunctions/alienSpeciesImg',
        extraction_function=GEE.get_image_from_single_image,
        source='https://onlinelibrary.wiley.com/doi/full/10.1111/geb.12517?msockid=27defa03f1f565bc00c9efb6f0f164ab',
        scale=5000
    )

    ECOSYSTEM_CONDITION = VariableData(
        name='EII',
        full_name='Ecosystem Integrity Index',
        description='Ecosystem Integrity Index',
        aggregation='mean',
        unit='Index 0-1',
        multiplier=100,
        gee_path='projects/ee-maidiesinitam/assets/valueFunctions/eii_padj_v5140524_reprojected',
        alt_path='projects/ee-maidiesinitam/assets/valueFunctions/eii_padj_v5140524_reprojected',
        extraction_function=GEE.get_image_from_single_image,
        source='https://www.biorxiv.org/content/10.1101/2022.08.21.504707v2.abstract',
        scale=1175
    )

    BIODIVERSITY_INTACTNESS = VariableData(
        name='biodivIntactness',
        full_name='Biodiversity intactness',
        description='Index of biodiversity intactness',
        aggregation='mean',
        unit='Index 0-1',
        multiplier=100,
        gee_path='users/ABC-Map/biodiversity',
        alt_path='users/ABC-Map/biodiversity',
        extraction_function=GEE.get_image_from_single_image,
        source='https://www.science.org/doi/10.1126/science.aaf2201',
        scale=927
    )

    ES_DIVERSITY = VariableData(
        name='ecosysDiv',
        full_name='Ecosystem diversity',
        description='Ecossytem Diversity',
        aggregation='mean',
        unit='Index 0-1',
        gee_path='projects/ee-maidiesinitam/assets/valueFunctions/ecosystemDiversity',
        alt_path='projects/ee-maidiesinitam/assets/valueFunctions/ecosystemDiversity',
        extraction_function=GEE.get_image_from_single_image,
        source='https://onlinelibrary.wiley.com/doi/10.1111/geb.12365',
        scale=927,
        multiplier=1e-4
    )

    FRAGMENTATION = VariableData(
        name='fragmentation',
        full_name='Fragmentation',
        description='Fragmentation based on Global HUman Modification Index',
        aggregation='mean',
        multiplier=100,
        unit='Index 0-1',
        gee_path="CSP/HM/GlobalHumanModification",
        alt_path="CSP/HM/GlobalHumanModification",
        extraction_function=GEE.get_first_image_from_collection,
        source='https://developers.google.com/earth-engine/datasets/catalog/CSP_HM_GlobalHumanModification',
        scale=1002
    )

    HANPP = VariableData(
        name='hanpp',
        full_name='Human Appropriation of Net Primary Production',
        description='Human Appropriation of Net Primary Productivity',
        aggregation='mean',
        unit='NEEDS SPECIFICATION!!',
        gee_path="projects/ee-maidiesinitam/assets/valueFunctions/hanpp",
        alt_path="projects/ee-maidiesinitam/assets/valueFunctions/hanpp",
        extraction_function=GEE.get_hanpp,
        source='https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2006JD007377',
        scale=27829,
        multiplier=1e4
    )

    HUMAN_MODIF_INDEX = VariableData(
        name='humanModification',
        full_name='Human Modification Index',
        description='Human Modification Index',
        aggregation='mean',
        unit='Index 0-1',
        multiplier=100,
        alt_path="projects/sat-io/open-datasets/GHM/ghm_v15",
        gee_path='projects/ee-maidiesinitam/assets/valueFunctions/ghm',
        extraction_function=GEE.get_human_modif_indexb,
        source='https://essd.copernicus.org/articles/12/1953/2020/essd-12-1953-2020-discussion.html',
        scale=300
    )

    LANDSCAPE_DIVERSITY = VariableData(
        name='landscapeDiv',
        full_name='Topographic Diversity',
        description='Ecologically-Relevant Maps of Landforms and Physiographic Diversity for Climate Adaptation Planning',
        aggregation='mean',
        unit='Index 0-1',
        multiplier=100,
        gee_path="CSP/ERGo/1_0/Global/ALOS_topoDiversity",
        alt_path='CSP/ERGo/1_0/Global/ALOS_topoDiversity',
        extraction_function=GEE.get_image_from_single_image,
        source='https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0143619',
        scale=270
    )

    NIGHT_LIGHT = VariableData(
        name='nightLight',
        full_name='Night time light',
        description='Annual values for night time light',
        aggregation='mean',
        unit='nanoWatts/cm2/sr',
        gee_path='projects/ee-maidiesinitam/assets/Harmonized_NTL',
        alt_path='projects/ee-maidiesinitam/assets/Harmonized_NTL',
        extraction_function=GEE.get_image_from_timeseries,
        source='https://www.nature.com/articles/s41597-020-0510-y',
        scale=927
    )

    NPP_YEAR = VariableData(
        name='NPP_year',
        full_name='Net Primary Production',
        description='Net Primary Productivity',
        aggregation='mean',
        unit='kg C/m2',
        gee_path="MODIS/061/MOD17A3HGF",
        alt_path="MODIS/061/MOD17A3HGF",
        extraction_function=GEE.get_npp,
        source='https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD17A3HGF',
        scale=463
    )

    NPP_MAX = VariableData(
        name='NPP_max',
        full_name='Net Primary Production Max',
        description='Maximum value of Net Primary Productivity from 2001 - project year',
        aggregation='mean',
        unit='kg C/m2',
        gee_path="MODIS/061/MOD17A3HGF",
        alt_path="MODIS/061/MOD17A3HGF",
        extraction_function=GEE.get_npp_max,
        source='https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD17A3HGF',
        scale=463
    )

    NPP_SHARE = VariableData(
        name='NPP_share',
        full_name='Net Primary Production share',
        description='Maximum value of Net Primary Productivity from 2001 - project year divided by NPP of project year',
        aggregation='mean',
        unit='kg C/m2',
        multiplier=100,
        gee_path="MODIS/061/MOD17A3HGF",
        alt_path="MODIS/061/MOD17A3HGF",
        extraction_function=GEE.get_npp_share,
        source='https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD17A3HGF',
        scale=463
    )

    POP_AGE = VariableData(
        name='popAge',
        full_name='Population age',
        description='Average population age',
        aggregation='mean',
        unit='Years',
        gee_path="WorldPop/GP/100m/pop_age_sex_cons_unadj",
        alt_path="WorldPop/GP/100m/pop_age_sex_cons_unadj",
        extraction_function=GEE.get_population_age,
        source='https://developers.google.com/earth-engine/datasets/catalog/WorldPop_GP_100m_pop_age_sex_cons_unadj',
        scale=300
    )

    POP_DENSITY = VariableData(
        name='popDensity',
        full_name='Population Density',
        description='Population density',
        aggregation='mean',
        unit='persons per km^2',
        gee_path="CIESIN/GPWv411/GPW_Population_Density",
        alt_path="CIESIN/GPWv411/GPW_Population_Density",
        extraction_function=GEE.get_image_from_timeseries,
        source='https://developers.google.com/earth-engine/datasets/catalog/CIESIN_GPWv411_GPW_Population_Density',
        scale=927
    )

    PROTECTED_AREA_CONNECTIVITY = VariableData(
        name='protConn',
        full_name='Connectivity of protected areas',
        description='Percentage of connected protected land',
        aggregation='mean',
        unit='pct',
        gee_path="projects/ee-maidiesinitam/assets/valueFunctions/protConnImage",
        alt_path="projects/ee-maidiesinitam/assets/valueFunctions/protConnImage",
        extraction_function=GEE.get_image_from_single_image,
        source='linkinghub.elsevier.com/retrieve/pii/S0006320717312284',
        scale=300
    )

    PROTECTION_STATUS = VariableData(
        name='protStatus',
        full_name='Protection Status',
        description='Percentage of area listed as protected',
        aggregation='mean',
        unit='pct',
        alt_path="WCMC/WDPA/current/polygons",
        gee_path='projects/ee-maidiesinitam/assets/valueFunctions/wdpa-image-aug2024',
        extraction_function=GEE.get_protection_status2,
        source='https://developers.google.com/earth-engine/datasets/catalog/WCMC_WDPA_current_polygons',
        scale=300,
        multiplier=100
    )

    ROAD_DENSITY = VariableData(
        name='roadDensity',
        full_name='Road Density',
        description='Length of roads per square kilometer',
        aggregation='mean',
        unit='m/km2',
        gee_path="users/philipaudebert/GRIP/GRIP_World_RoadDensity",
        alt_path="users/philipaudebert/GRIP/GRIP_World_RoadDensity",
        extraction_function=GEE.get_image_from_single_image,
        source='https://www.globio.info/download-grip-dataset',
        scale=9276
    )

    SETTLEMENTS = VariableData(
        name='settlements',
        full_name='Built-up',
        description='Percentage of area classified as built-up land',
        aggregation='mean',
        unit='pct',
        gee_path="JRC/GHSL/P2023A/GHS_BUILT_S",
        alt_path='JRC/GHSL/P2023A/GHS_BUILT_S',
        extraction_function=GEE.get_settlement,
        source='https://developers.google.com/earth-engine/datasets/catalog/JRC_GHSL_P2023A_GHS_BUILT_S',
        scale=100
    )

    ELEVATION = VariableData(
        name='Elevation',
        full_name='Elevation',
        description='Elevation in meters',
        aggregation='mean',
        unit='m',
        gee_path='USGS/SRTMGL1_003',
        alt_path='USGS/SRTMGL1_003',
        extraction_function=GEE.get_image_from_single_image,
        source='https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003',
        scale=300
    )

    LAND_COVER = VariableData(
        name='land_cover',
        full_name='Land Cover',
        description='Land Cover classification using ESA CCI lgobal ladncover product for historic availability',
        aggregation='mean',
        unit='LC classes',
        gee_path='users/openforisearthmap/CCI_LC/ESACCI-LC-L4-LCCS-Map-300m-P1Y-1992_2018_v2_1_1',
        alt_path='TBD',
        extraction_function=GEE.get_land_cover,
        source='https://www.esa-landcover-cci.org/',
        scale=300,
        method='lc'
    )

    SLOPE = VariableData(
        name='slope',
        full_name='Slope',
        description='Slope in degrees',
        aggregation='mean',
        unit='degrees',
        gee_path='USGS/SRTMGL1_003',
        alt_path='USGS/SRTMGL1_003',
        extraction_function=GEE.get_slope,
        source='https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003',
        scale=300
    )

class ClimateVariable(Variable):

    DRY_DAYS = VariableData(
        name='dryDays',
        full_name='Number of dry days per year',
        description='Dry days (precip<1mm)',
        aggregation='mean',
        unit='Number of annual days',
        gee_path="ECMWF/ERA5_LAND/DAILY_AGGR",
        alt_path='TBD',
        extraction_function=GEE.get_dry_days,
        source='https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_DAILY_AGGR',
        scale=11132
    )

    FROST_DAYS = VariableData(
        name='frostDays',
        full_name='Number of frost days per year',
        description='Frost days (min T<0°C)',
        aggregation='mean',
        unit='Number of annual days',
        gee_path="ECMWF/ERA5_LAND/DAILY_AGGR",
        alt_path='TBD',
        extraction_function=GEE.get_frost_days,
        source='https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_DAILY_AGGR',
        scale=11132
    )

    HEAVY_RAIN_DAYS = VariableData(
        name='heavyRainDays',
        full_name='Number of heavy rain days',
        description='Heavy rain days (precip>50mm)',
        aggregation='mean',
        unit='Number of annual days',
        gee_path="ECMWF/ERA5_LAND/DAILY_AGGR",
        alt_path='TBD',
        extraction_function=GEE.get_heavy_rain_days,
        source='https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_DAILY_AGGR',
        scale=11132
    )

    MEAN_ANNUAL_TEMPERATURE = VariableData(
        name='meanAnnualTemp',
        full_name='Mean Annual Temperature',
        description='Mean Annual Temeprature',
        aggregation='mean',
        unit='degrees C',
        gee_path="ECMWF/ERA5_LAND/DAILY_AGGR",
        alt_path='TBD',
        extraction_function=GEE.get_mean_annual_temperature,
        source='https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_DAILY_AGGR',
        scale=11132
    )

    TOTAL_ANNUAL_PRECIPITATION = VariableData(
        name='totalAnnualPrecip',
        full_name='Total Annual Precipitation',
        description='Total Annual Precipitation in mm',
        aggregation='mean',
        unit='mm',
        gee_path="ECMWF/ERA5_LAND/DAILY_AGGR",
        alt_path='TBD',
        extraction_function=GEE.get_total_annual_precipitation,
        source='https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_DAILY_AGGR',
        scale=11132
    )

    MEAN_NDVI_P95 = VariableData(
        name='ndviP95',
        full_name='NDVI 95',
        description='95th percentile score of annual NDVI',
        aggregation='mean',
        unit='NDVI index',
        gee_path='NOAA/CDR/AVHRR/NDVI/V5',
        alt_path='TBD',
        extraction_function=GEE.get_mean_NDVI,
        source='https://developers.google.com/earth-engine/datasets/catalog/NOAA_CDR_AVHRR_NDVI_V5',
        scale=5000
    )


class CountryVariable(Variable):

    GDP_PER_CAPITA = VariableData(
        name='GDPPC',
        full_name='Global Domestic Product Per Capita per country',
        description='GDPPC for project year',
        aggregation='Country value',
        unit='USD',
        gee_path='NY.GDP.PCAP.CD',
        alt_path='TBD',
        extraction_function=GEE.get_wb,
        source='https://data.worldbank.org/indicator/NY.GDP.PCAP.CD',
        scale=300,
        method='wb'
    )

    GDP_PER_CAPITA_PPP = VariableData(
        name='GDPPC_PPP',
        full_name='Global Domestic Product Per Capita per country, PPP',
        description='GDPPC for project year, PPP',
        aggregation='Country value',
        unit='USD',
        gee_path='NY.GDP.PCAP.PP.CD',
        alt_path='TBD',
        extraction_function=GEE.get_wb,
        source='https://data.worldbank.org/indicator/NY.GDP.PCAP.CD',
        scale=300,
        method='wb'
    )

    GDP_PER_CAPITA_PPP_CONSTANT = VariableData(
        name='GDPPC_PPP_CONTSTANT',
        full_name='Global Domestic Product Per person employed (constant 2021 PPP $)',
        description='GDPPC for project year, PPP',
        aggregation='Country value',
        unit='USD',
        gee_path='SL.GDP.PCAP.EM.KD',
        alt_path='TBD',
        extraction_function=GEE.get_wb,
        source='https://data.worldbank.org/indicator/SL.GDP.PCAP.EM.KD',
        scale=300,
        method='wb'
    )

    GNI_PER_CAPITA = VariableData(
        name='GNIPC',
        full_name='Gross National Income Per Capita per country',
        description='GNIPC for project year',
        aggregation='Country value',
        unit='USD',
        gee_path='NY.GNP.PCAP.CD',
        alt_path='TBD',
        extraction_function=GEE.get_wb,
        source='https://data.worldbank.org/indicator/NY.GNP.PCAP.KD',
        scale=300,
        method='wb'
    )

    GNI_PER_CAPITA_PPP = VariableData(
        name='GNIPC_PPP',
        full_name='Gross National Income Per Capita per country PPP',
        description='GNIPC for project year PPP',
        aggregation='Country value',
        unit='USD',
        gee_path='NY.GNP.PCAP.PP.CD',
        alt_path='TBD',
        extraction_function=GEE.get_wb,
        source='https://data.worldbank.org/indicator/NY.GNP.PCAP.PP.KD',
        scale=300,
        method='wb'
    )

    GNI_PER_CAPITA_PPP_CONSTANT = VariableData(
        name='GNIPC_PPP_CONSTANT',
        full_name='Adjusted net national income per capita (constant 2015 US$)',
        description='GNIPC for project year PPP',
        aggregation='Country value',
        unit='USD',
        gee_path='NY.ADJ.NNTY.PC.KD',
        alt_path='TBD',
        extraction_function=GEE.get_wb,
        source='https://data.worldbank.org/indicator/NY.ADJ.NNTY.PC.KD',
        scale=300,
        method='wb'
    )

    GINI = VariableData(
        name='GINI',
        full_name='GINI Inequality coefficient',
        description='GINI Inequality coefficient per country',
        aggregation='Country value',
        unit='Index',
        gee_path='SI.POV.GINI',
        alt_path='TBD',
        extraction_function=GEE.get_wb,
        source='https://data.worldbank.org/indicator/SI.POV.GINI',
        scale=300,
        method='wb'
    )

    PPP = VariableData(
        name='PPP_factor',
        full_name='PPP conversion factor',
        description='PPP Conversion factor per country',
        aggregation='Country value',
        unit='Factor',
        gee_path='PA.NUS.PPPC.RF',
        alt_path='TBD',
        extraction_function=GEE.get_wb,
        source='https://data.worldbank.org/indicator/PA.NUS.PPPC.RF',
        scale=300,
        method='wb'
    )

class OtherVariable(Variable):
    SENSLOPE_NDVI_P95_2018 = VariableData(
        name='ndviP05Senslope',
        full_name='NDVI 95 Sen Slope',
        description='Sen slope of NDVI P95',
        aggregation='mean',
        unit='TBD',
        gee_path='NOAA/CDR/AVHRR/NDVI/V5',
        alt_path='TBD',
        extraction_function=GEE.get_senslope_NDVI,
        source='https://developers.google.com/earth-engine/datasets/catalog/NOAA_CDR_AVHRR_NDVI_V5',
        scale=300
    )

class Var:

    def __init__(self, var: BenefitVariable, ln:bool=False, lc:LandCoverGroup=None, buffer:int=None, coefficient:float=None):
        self.var = var
        self.ln = ln
        self.lc = lc
        self.var.buffer = buffer
        self.coefficient = coefficient
        self.value = 0


