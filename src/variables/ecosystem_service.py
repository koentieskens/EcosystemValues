from src.variables import variable_template
from dataclasses import dataclass

@dataclass
class EcosystemServiceData(variable_template.Data):
    """Dataclass to store metadata for a variable. This template will be used to create spatial variables"""
    SEEA_clas1: str
    SEEA_clas2: str
    SEEA_clas3: str
    SEAA_Code: str
    data_source: str
    description: str
    unit: str = 'USD per ha per year'
    welfare: bool = True,
    exchange: bool = True,

    def get_tooltip(self):
        return (f"SEEA Classification\n\n"
                f"Category: {self.SEEA_clas1} | "
                f"Subtype: {self.SEEA_clas3}\n\n"
                f"{self.description}\n\n"
                f"Value estimate based on: {self.data_source}")

class EcosystemService:

    WOOD_PROVISION = EcosystemServiceData(
        name='Wood Provision',
        full_name='Wood Provision',
        SEEA_clas1='Provisioning',
        SEEA_clas2='Biomass provisioning services',
        SEEA_clas3='Wood provisioning services',
        SEAA_Code='1.5',
        description='Wood provisioning services are the ecosystem contributions to the growth of trees and other woody biomass in both cultivated (plantation) and uncultivated production contexts that are harvested by economic units for various uses including timber production and energy. This service excludes contributions to non-wood forest products. This is a final ecosystem service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=True,
        exchange=True,
    )

    WILD_FISH_PROVISION = EcosystemServiceData(
        name='Wild Fish Provision',
        full_name='Wild Fish Provision',
        SEEA_clas1='Provisioning',
        SEEA_clas2='Biomass provisioning services',
        SEEA_clas3='Wild fish and other natural aquatic products provisioning services',
        SEAA_Code='1.6',
        description='Wild fish and other natural aquatic biomass provisioning services are the ecosystem contributions to the growth of fish and other aquatic biomass that are captured in uncultivated production contexts by economic units for various uses, primarily food production. This is a final ecosystem service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=True,
        exchange=True,
    )

    AQUACULTURE = EcosystemServiceData(
        name='Aquaculture Provision',
        full_name='Aquaculture Provision',
        SEEA_clas1='Provisioning',
        SEEA_clas2='Biomass provisioning services',
        SEEA_clas3='Aquaculture provisioning services',
        SEAA_Code='1.4',
        description='Aquaculture provisioning services are the ecosystem contributions to the growth of animals and plants (e.g. fish, shellfish, seaweed) in aquaculture facilities that are harvested by economic units for various uses. This is a final ecosystem service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=False,
        exchange=True,
    )

    WILD_ANIMAL_PROVISION = EcosystemServiceData(
        name='Wild Animals Provision',
        full_name='Wild Animals Provision',
        SEEA_clas1='Provisioning',
        SEEA_clas2='Biomass provisioning services',
        SEEA_clas3='Wild animals, plants and other biomass provisioning services',
        SEAA_Code='1.7',
        description='Wild animals, plants and other biomass provisioning services are the ecosystem contributions to the growth of wild animals, plants and other biomass that are captured and harvested in uncultivated production contexts by economic units for various uses. The scope includes non-wood forest products (NWFP) and services related to hunting, trapping and bio-prospecting activities; but excludes wild fish and other natural aquatic biomass (included in previous class). This is a final ecosystem service',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=True,
        exchange=True,
    )

    CROP_PROVISION = EcosystemServiceData(
        name='Crop Provision',
        full_name='Crop Provision',
        SEEA_clas1='Provisioning',
        SEEA_clas2='Biomass provisioning services',
        SEEA_clas3='Crop provisioning services',
        SEAA_Code='1.1',
        description='Crop provisioning services are the ecosystem contributions to the growth of cultivated plants that are harvested by economic units for various uses including food and fibre production, fodder and energy. This is a final ecosystem service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=True,
        exchange=True,
    )

    GRAZED_BIOMASS_PROVISION = EcosystemServiceData(
        name='Grazed Biomass Provision',
        full_name='Grazed Biomass Provision',
        SEEA_clas1='Provisioning',
        SEEA_clas2='Biomass provisioning services',
        SEEA_clas3='Grazed biomass provisioning services',
        SEAA_Code='1.2',
        description='Grazed biomass provisioning services are the ecosystem contributions to the growth of grazed biomass that is an input to the growth of cultivated livestock. This service excludes the ecosystem contributions to the growth of crops used to produce fodder for livestock (e.g., hay, soybean meal). These contributions are included under crop provisioning services. This is a final ecosystem service but may be intermediate to livestock provisioning services.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=False,
        exchange=True,
    )

    LIVESTOCK_PROVISION = EcosystemServiceData(
        name='Livestock Provision',
        full_name='Livestock Provision',
        SEEA_clas1='Provisioning',
        SEEA_clas2='Biomass provisioning services',
        SEEA_clas3='Livestock provisioning services',
        SEAA_Code='1.3',
        description='Livestock provisioning services are the ecosystem contributions to the growth of cultivated livestock and livestock products (e.g., meat, milk, eggs, wool, leather), that are used by economic units for various uses, primarily food production. This is a final ecosystem service. No distinct livestock provisioning services to be recorded if grazed biomass provisioning services are recorded as a final ecosystem service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=False,
        exchange=True,
    )

    PEST_CONTROL = EcosystemServiceData(
        name='Pest Control',
        full_name='Pest Control',
        SEEA_clas1='Regulating and Maintenance',
        SEEA_clas2='Biological control services',
        SEEA_clas3='Pest control services',
        SEAA_Code='2.18',
        description='Biological control services are the ecosystem contributions to the reduction in the incidence of species that may prevent or reduce the effects of pests on biomass production processes or other economic and human activity. This is may be recorded as a final or intermediate service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=True,
        exchange=True,
    )

    NUTRIENT_RETENTION = EcosystemServiceData(
        name='Nutrient Retention',
        full_name='Nutrient Retention',
        SEEA_clas1='Regulating and Maintenance',
        SEEA_clas2='Water purification services (water quality amelioration)',
        SEEA_clas3='Retention and breakdown of nutrients',
        SEAA_Code='2.9',
        description='Water purification services are the ecosystem contributions to the restoration and maintenance of the chemical condition of surface water and groundwater bodies through the breakdown or removal of nutrients and other pollutants by ecosystem components that mitigate the harmful effects of the pollutants on human use or health. This may be recorded as a final or intermediate ecosystem service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=True,
        exchange=True,
    )

    WATER_SUPPLY = EcosystemServiceData(
        name='Water Supply',
        full_name='Water Supply',
        SEEA_clas1='Provisioning',
        SEEA_clas2='Water supply',
        SEEA_clas3='Water supply',
        SEAA_Code='1.9',
        description='Water supply services reflect the combined ecosystem contributions of water flow regulation, water purification, and other ecosystem services to the supply of water of appropriate quality to users for various uses including household consumption. This is a final ecosystem service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=True,
        exchange=True,
    )

    AIR_FILTRATION = EcosystemServiceData(
        name='Air Filtration',
        full_name='Air Filtration',
        SEEA_clas1='Regulating and Maintenance',
        SEEA_clas2='Air filtration services',
        SEEA_clas3='Air filtration services',
        SEAA_Code='2.4',
        description='Air filtration services are the ecosystem contributions to the filtering of air-borne pollutants through the deposition, uptake, fixing and storage of pollutants by ecosystem components, particularly plants, that mitigates the harmful effects of the pollutants. This is most commonly a final ecosystem service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=False,
        exchange=True,
    )

    GLOBAL_CLIMATE = EcosystemServiceData(
        name='Global Climate Regulation',
        full_name='Global Climate Regulation',
        SEEA_clas1='Regulating and Maintenance',
        SEEA_clas2='Global climate regulation services',
        SEEA_clas3='Global climate regulation services',
        SEAA_Code='2.1',
        description='Global climate regulation services are the ecosystem contributions to the regulation of the chemical composition of the atmosphere and oceans that affect global climate through the accumulation and retention of carbon and other GHG (e.g., methane) in ecosystems and the ability of ecosystems to remove (sequester) carbon from the atmosphere. This is a final ecosystem service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=True,
        exchange=True,
    )

    POLLINATION = EcosystemServiceData(
        name='Pollination',
        full_name='Pollination',
        SEEA_clas1='Regulating and Maintenance',
        SEEA_clas2='Pollination services',
        SEEA_clas3='Pollination services',
        SEAA_Code='2.17',
        description='Pollination services are the ecosystem contributions by wild pollinators to the fertilization of crops that maintains or increases the abundance and/or diversity of other species that economic units use or enjoy. This may be recorded as a final or intermediate service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=False,
        exchange=True,
    )

    WATER_FLOW_REGULATION = EcosystemServiceData(
        name='Water Flow Regulation',
        full_name='Water Flow Regulation',
        SEEA_clas1='Regulating and Maintenance',
        SEEA_clas2='Water flow regulation services',
        SEEA_clas3='Baseline flow maintenance services',
        SEAA_Code='2.11',
        description='Water regulation services are the ecosystem contributions to the regulation of river flows and groundwater and lake water tables. They are derived from the ability of ecosystems to absorb and store water, and gradually release water during dry seasons or periods through evapotranspiration and hence secure a regular flow of water. This may be recorded as a final or intermediate ecosystem service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=False,
        exchange=True,
    )

    VISUAL_AMENITY = EcosystemServiceData(
        name='Visual Amenity',
        full_name='Visual Amenity',
        SEEA_clas1='Cultural',
        SEEA_clas2='Visual amenity services',
        SEEA_clas3='Visual amenity services',
        SEAA_Code='3.2',
        description='Visual amenity services are the ecosystem contributions to local living conditions, in particular through the biophysical characteristics and qualities of ecosystems that provide sensory benefits, especially visual. This service combines with other ecosystem services, including recreation-related services and noise attenuation services to underpin amenity values. This is a final ecosystem service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=True,
        exchange=True,
    )

    RAINFALL_REGULATION = EcosystemServiceData(
        name='Rainfall Regulation',
        full_name='Rainfall Regulation',
        SEEA_clas1='Regulating and Maintenance',
        SEEA_clas2='Rainfall pattern regulation services (at sub-continental scale)',
        SEEA_clas3='Rainfall pattern regulation services (at sub-continental scale)',
        SEAA_Code='2.2',
        description='Rainfall pattern regulation services are the ecosystem contributions of vegetation, in particular forests, in maintaining rainfall patterns through evapotranspiration at the sub-continental scale. Forests and other vegetation recycle moisture back to the atmosphere where it is available for the generation of rainfall. Rainfall in interior parts of continents fully depends upon this recycling. This may be a final or intermediate service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=False,
        exchange=True,
    )

    RIVER_FLOOD_REGULATION = EcosystemServiceData(
        name='River Flood Mitigation',
        full_name='River Flood Mitigation',
        SEEA_clas1='Regulating and Maintenance',
        SEEA_clas2='Flood mitigation services',
        SEEA_clas3='River flood mitigation services',
        SEAA_Code='2.14',
        description='River flood mitigation services are the ecosystem contributions of riparian vegetation which provides structure and a physical barrier to high water levels and thus mitigates the impacts of floods on local communities. River flood mitigation services will be supplied together with peak flow mitigation services in providing the benefit of flood protection. This is a final ecosystem service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=True,
        exchange=True,
    )

    SOIL_EROSION_REGULATION = EcosystemServiceData(
        name='Soil Erosion Control',
        full_name='Soil Erosion Control',
        SEEA_clas1='Regulating and Maintenance',
        SEEA_clas2='Soil and sediment retention services',
        SEEA_clas3='Soil erosion control services',
        SEAA_Code='2.6',
        description='Soil erosion control services are the ecosystem contributions, particularly the stabilising effects of vegetation, that reduce the loss of soil (and sediment) and support use of the environment (e.g., agricultural activity, water supply). This is may be recorded as a final or intermediate service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=True,
        exchange=True,
    )

    SOIL_QUALITY_REGULATION = EcosystemServiceData(
        name='Soil Quality Regulation',
        full_name='Soil Quality Regulation',
        SEEA_clas1='Regulating and Maintenance',
        SEEA_clas2='Soil quality regulation services',
        SEEA_clas3='Soil quality regulation services',
        SEAA_Code='2.5',
        description='Soil quality regulation services are the ecosystem contributions to the decomposition of organic and inorganic materials and to the fertility and characteristics of soils, e.g., for input to biomass production. This is most commonly recorded as an intermediate service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=True,
        exchange=True,
    )

    RECREATION = EcosystemServiceData(
        name='Recreation',
        full_name='Recreation',
        SEEA_clas1='Cultural',
        SEEA_clas2='Recreation-related services',
        SEEA_clas3='Recreation-related services',
        SEAA_Code='3.1',
        description='Recreation-related services are the ecosystem contributions, in particular through the biophysical characteristics and qualities of ecosystems, that enable people to use and enjoy the environment through direct, in-situ, physical and experiential interactions with the environment. This includes services to both locals and non-locals (i.e. visitors, including tourists). Recreation-related services may also be supplied to those undertaking recreational fishing and hunting. This is a final ecosystem service.',
        data_source='https://www.sciencedirect.com/science/article/pii/S2212041624000123?via%3Dihub',
        welfare=True,
        exchange=True,
    )

    COASTAL_PROTECTION = EcosystemServiceData(
        name='Coastal protection services',
        full_name='Coastal protection services',
        SEEA_clas1='Regulating and Maintenance',
        SEEA_clas2='Flood control services',
        SEEA_clas3='Coastal protection services',
        SEAA_Code='3.1',
        description='Coastal protection services are ecosystem contributions of linear elements in the seascape (e.g. coral reefs, sand banks, dunes or mangrove ecosystems along the shore) to protecting the shore and thus mitigating the impacts of tidal surges or storms on local communities. These are final ecosystem services.',
        data_source='https://www.nature.com/articles/s41598-020-61136-6',
        welfare=False,
        exchange=True,
    )