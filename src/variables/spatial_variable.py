
from dataclasses import dataclass
from src.variables import variable_template
from ..extract_data.get_images import GeeImageExtractor as GEE

@dataclass
class SpatialData(variable_template.Data):
    """Dataclass to store metadata for a variable. This template will be used to create spatial variables"""
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

    def get_image(self, **kwargs):
        """Get the image for the variable."""
        return self.extraction_function(gee_path=self.gee_path, name=self.name, **kwargs)

    def get_tooltip(self):
        return f'{self.description}'

    def get_name(self):
        """Get the name of the variable used in further processing."""
        name = self.name
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
            if hasattr(var, 'name'):
                row = {
                    'name': var.value.name,
                    'full_name': var.value.full_name,
                    'description': getattr(var.value, 'description', None),
                    'aggregation': getattr(var.value, 'aggregation', None),
                    'unit': getattr(var.value, 'unit', None),
                    'gee_path': var.value.gee_path,
                    'alt_path': var.value.alt_path,
                    'extraction_function': var.value.extraction_function.__name__ if hasattr(
                        var.value.extraction_function, '__name__') else str(var.value.extraction_function),
                    'source': getattr(var.value, 'source', None),
                    'scale': var.value.scale,
                    'multiplier': getattr(var.value, 'multiplier', None)
                }
                data.append(row)

        return pd.DataFrame(data)


class BenefitSpatialVariable:
    """Enum to represent spatial variables that can be extracted for given points."""

    ACCESSIBILITY = SpatialData(
        name='accessibility',
        full_name='Accessibility',
        description='Time to nearest city/town in minutes',
        aggregation='mean',
        unit='minutes',
        gee_path='projects/ee-maidiesinitam/assets/valueFunctions/accessibility_city_2015',
        alt_path='projects/ee-maidiesinitam/assets/valueFunctions/accessibility_city_2015',
        extraction_function=GEE.get_accessibility,
        source='https://www.nature.com/articles/nature25181',
        scale=927
    )

    AIRPOLLUTION = SpatialData(
        name='airPollution',
        full_name='Air pollution',
        description='Concentration of PM2.5 in micrograms per cubic meter',
        aggregation='mean',
        unit='ug/M^3',
        alt_path='projects/sat-io/open-datasets/GLOBAL-SATELLITE-PM25/ANNUAL',
        gee_path='projects/ee-maidiesinitam/assets/nasa-pm-25',
        extraction_function=GEE.get_image_from_timeseries,
        source='https://www.earthdata.nasa.gov/data/catalog/sedac-ciesin-sedac-sdei-gwrpm25-mmsaod-4gl03-4.03#toc-copy-citation',
        scale=1113
    )

    ALIEN_SPECIES = SpatialData(
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

    ECOSYSTEM_CONDITION = SpatialData(
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

    BIODIVERSITY_INTACTNESS = SpatialData(
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

    ES_DIVERSITY = SpatialData(
        name='ecosysDiv',
        full_name='Ecosystem diversity',
        description='Index of ecosystem diversity',
        aggregation='mean',
        unit='Index 0-1',
        gee_path='projects/ee-maidiesinitam/assets/valueFunctions/ecosystemDiversity',
        alt_path='projects/ee-maidiesinitam/assets/valueFunctions/ecosystemDiversity',
        extraction_function=GEE.get_image_from_single_image,
        source='https://onlinelibrary.wiley.com/doi/10.1111/geb.12365',
        scale=927,
        multiplier=1e-4
    )

    FRAGMENTATION = SpatialData(
        name='fragmentation',
        full_name='Landscape fragmentation',
        description='Fragmentation based on Global Human Modification Index',
        aggregation='mean',
        multiplier=100,
        unit='Index 0-1',
        gee_path="CSP/HM/GlobalHumanModification",
        alt_path="CSP/HM/GlobalHumanModification",
        extraction_function=GEE.get_first_image_from_collection,
        source='https://developers.google.com/earth-engine/datasets/catalog/CSP_HM_GlobalHumanModification',
        scale=1002
    )

    HANPP = SpatialData(
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

    HUMAN_MODIF_INDEX = SpatialData(
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

    LANDSCAPE_DIVERSITY = SpatialData(
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

    NIGHT_LIGHT = SpatialData(
        name='nightLight',
        full_name='Night time light',
        description='Annual values for night time light in nanoWatts/cm2/yr',
        aggregation='mean',
        unit='nanoWatts/cm2/sr',
        gee_path='projects/ee-maidiesinitam/assets/Harmonized_NTL',
        alt_path='projects/ee-maidiesinitam/assets/Harmonized_NTL',
        extraction_function=GEE.get_image_from_timeseries,
        source='https://www.nature.com/articles/s41597-020-0510-y',
        scale=927
    )

    NPP_YEAR = SpatialData(
        name='NPP_year',
        full_name='Net Primary Production',
        description='Net Primary Productivity in kg C/m2',
        aggregation='mean',
        unit='kg C/m2',
        gee_path="MODIS/061/MOD17A3HGF",
        alt_path="MODIS/061/MOD17A3HGF",
        extraction_function=GEE.get_npp,
        source='https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD17A3HGF',
        scale=463
    )

    NPP_MAX = SpatialData(
        name='NPP_max',
        full_name='Net Primary Production Max',
        description='Maximum value of Net Primary Productivity from 2001 - project year in kg C/m2',
        aggregation='mean',
        unit='kg C/m2',
        gee_path="MODIS/061/MOD17A3HGF",
        alt_path="MODIS/061/MOD17A3HGF",
        extraction_function=GEE.get_npp_max,
        source='https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD17A3HGF',
        scale=463
    )

    NPP_SHARE = SpatialData(
        name='NPP_share',
        full_name='Net Primary Production',
        description='Current NPP divided byMaximum value of Net Primary Productivity from 2001 in kg C/m2',
        aggregation='mean',
        unit='kg C/m2',
        multiplier=100,
        gee_path="MODIS/061/MOD17A3HGF",
        alt_path="MODIS/061/MOD17A3HGF",
        extraction_function=GEE.get_npp_share,
        source='https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD17A3HGF',
        scale=463
    )

    POP_AGE = SpatialData(
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

    POP_DENSITY = SpatialData(
        name='popDensity',
        full_name='Population Density',
        description='Population density in persons per square kilometer',
        aggregation='mean',
        unit='persons per km^2',
        gee_path="CIESIN/GPWv411/GPW_Population_Density",
        alt_path="CIESIN/GPWv411/GPW_Population_Density",
        extraction_function=GEE.get_image_from_timeseries,
        source='https://developers.google.com/earth-engine/datasets/catalog/CIESIN_GPWv411_GPW_Population_Density',
        scale=927
    )

    PROTECTED_AREA_CONNECTIVITY = SpatialData(
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

    PROTECTION_STATUS = SpatialData(
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

    ROAD_DENSITY = SpatialData(
        name='roadDensity',
        full_name='Road Density',
        description='Total length of roads in meters per square kilometer',
        aggregation='mean',
        unit='m/km2',
        gee_path="users/philipaudebert/GRIP/GRIP_World_RoadDensity",
        alt_path="users/philipaudebert/GRIP/GRIP_World_RoadDensity",
        extraction_function=GEE.get_image_from_single_image,
        source='https://www.globio.info/download-grip-dataset',
        scale=9276
    )

    SETTLEMENTS = SpatialData(
        name='settlements',
        full_name='Percentage of built-up land',
        description='Percentage of area classified as built-up land',
        aggregation='mean',
        unit='pct',
        gee_path="JRC/GHSL/P2023A/GHS_BUILT_S",
        alt_path='JRC/GHSL/P2023A/GHS_BUILT_S',
        extraction_function=GEE.get_settlement,
        source='https://developers.google.com/earth-engine/datasets/catalog/JRC_GHSL_P2023A_GHS_BUILT_S',
        scale=100
    )

    ELEVATION = SpatialData(
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

    LAND_COVER = SpatialData(
        name='land_cover',
        full_name='Land Cover',
        description='Land Cover classification using ESA CCI gobal landcover product for historic availability',
        aggregation='mean',
        unit='LC classes',
        gee_path='users/openforisearthmap/CCI_LC/ESACCI-LC-L4-LCCS-Map-300m-P1Y-1992_2018_v2_1_1',
        alt_path='TBD',
        extraction_function=GEE.get_land_cover,
        source='https://www.esa-landcover-cci.org/',
        scale=300,
        method='lc'
    )

    SLOPE = SpatialData(
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

class ClimateSpatialVariable:

    DRY_DAYS = SpatialData(
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

    FROST_DAYS = SpatialData(
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

    HEAVY_RAIN_DAYS = SpatialData(
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

    MEAN_ANNUAL_TEMPERATURE = SpatialData(
        name='meanAnnualTemp',
        full_name='Mean Annual Temperature',
        description='Mean Annual Temperature in degrees Celsius',
        aggregation='mean',
        unit='degrees C',
        gee_path="ECMWF/ERA5_LAND/DAILY_AGGR",
        alt_path='TBD',
        extraction_function=GEE.get_mean_annual_temperature,
        source='https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_DAILY_AGGR',
        scale=11132
    )

    TOTAL_ANNUAL_PRECIPITATION = SpatialData(
        name='totalAnnualPrecip',
        full_name='Total Annual Precipitation',
        description='Total Annual Precipitation in m',
        aggregation='mean',
        unit='m',
        gee_path="ECMWF/ERA5_LAND/DAILY_AGGR",
        alt_path='TBD',
        extraction_function=GEE.get_total_annual_precipitation,
        source='https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_DAILY_AGGR',
        scale=11132
    )

    MEAN_NDVI_P95 = SpatialData(
        name='ndviP95',
        full_name='NDVI',
        description='95th percentile score of annual NDVI',
        aggregation='mean',
        unit='NDVI index',
        gee_path='NOAA/CDR/AVHRR/NDVI/V5',
        alt_path='TBD',
        extraction_function=GEE.get_mean_NDVI,
        source='https://developers.google.com/earth-engine/datasets/catalog/NOAA_CDR_AVHRR_NDVI_V5',
        scale=5000
    )

class CountrySpatialVariable:

    GDP_PER_CAPITA = SpatialData(
        name='GDPPC',
        full_name='Global Domestic Product Per Capita per country',
        description='Global Domestic Product Per Capita per country in USD',
        aggregation='Country value',
        unit='USD',
        gee_path='NY.GDP.PCAP.CD',
        alt_path='TBD',
        extraction_function=GEE.get_wb,
        source='https://data.worldbank.org/indicator/NY.GDP.PCAP.CD',
        scale=300,
        method='wb'
    )

    GDP_PER_CAPITA_PPP = SpatialData(
        name='GDPPC_PPP',
        full_name='Global Domestic Product Per Capita per country, PPP',
        description='GDPPC for country, in International Dollars',
        aggregation='Country value',
        unit='USD',
        gee_path='NY.GDP.PCAP.PP.CD',
        alt_path='TBD',
        extraction_function=GEE.get_wb,
        source='https://data.worldbank.org/indicator/NY.GDP.PCAP.CD',
        scale=300,
        method='wb'
    )

    GDP_PER_CAPITA_PPP_CONSTANT = SpatialData(
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

    GNI_PER_CAPITA = SpatialData(
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

    GNI_PER_CAPITA_PPP = SpatialData(
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

    GNI_PER_CAPITA_PPP_CONSTANT = SpatialData(
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

    GINI = SpatialData(
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

    PPP = SpatialData(
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

class OtherSpatialVariable:
    SENSLOPE_NDVI_P95_2018 = SpatialData(
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

