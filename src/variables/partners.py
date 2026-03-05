from dataclasses import dataclass

@dataclass
class PartnerData:
    """Dataclass to store metadata for a variable. This template will be used to create variables"""
    name: str
    full_name: str
    url: str
    logo: str

class Partner:
    DUKE = PartnerData(
        name='Duke',
        full_name='Duke University Nicholas School of the Environment',
        url='https://www.nicholas.duke.edu/',
        logo='src/images/partners/duke.png'
    )

    PROGREEN = PartnerData(
        name='Progreen',
        full_name='Progreen',
        url='https://www.progreen.info/',
        logo='src/images/partners/progreen.jpg'
    )

    FSD = PartnerData(
        name='FSD',
        full_name='Foundation for Sustainable Development',
        url='https://www.fsd.nl/',
        logo='src/images/partners/fsd.png'
    )

    UNIQUE = PartnerData(
        name='Unique',
        full_name='Unique Land Use',
        url='https://www.unique-landuse.de/en',
        logo='src/images/partners/unique.png'
    )

    IUCN = PartnerData(
        name='IUCN',
        full_name='International Union for Conservation of Nature',
        url='https://www.iucn.org/',
        logo='src/images/partners/iucn.png'
    )

    ECU = PartnerData(
        name='ECU',
        full_name='East Carolina University',
        url='https://www.ecu.edu/',
        logo='src/images/partners/ecu.png'
    )

    ELD = PartnerData(
        name='ELD',
        full_name='The Economics of Land Degradation',
        url='https://www.eld-initiative.org/en/',
        logo='src/images/partners/eld.png'
    )

    GFDRR = PartnerData(
        name='GFDRR',
        full_name='Global Facility for Disaster Risk Reduction',
        url='https://www.gfdrr.org/',
        logo='src/images/partners/gfdrr.png'
    )

    NBSINVEST = PartnerData(
        name='NBSInvest',
        full_name='NBSInvest',
        url='https://www.worldbank.org/en/topic/environment/brief/investing-in-nature-based-solutions#1',
        logo='src/images/partners/nbsinvest.png'
    )

    GPNBS = PartnerData(
        name='GPNBS',
        full_name='Global Program on Nature Based Solutions fro Climate Resilience',
        url='https://www.naturebasedsolutions.org/',
        logo='src/images/partners/gpnbs.png'
    )

    GPS = PartnerData(
        name='GPS',
        full_name='Global Program on Sustainability',
        url='https://www.worldbank.org/en/programs/global-program-on-sustainability',
        logo='src/images/partners/gps.png'
    )

    UCSC = PartnerData(
        name='UCSC',
        full_name='University of California, Santa Cruz',
        url='https://www.ucsc.edu/',
        logo='src/images/partners/ucsc.jpg'
    )

    FAO = PartnerData(
        name='FAO',
        full_name='Food and Agriculture Organization of the United Nations',
        url='https://www.fao.org/',
        logo='src/images/partners/fao.png'
    )

    US = PartnerData(
        name='GPNBS',
        full_name='Global Program on Nature Based Solutions fro Climate Resilience',
        url='https://www.naturebasedsolutions.org/',
        logo='src/images/NBS_GFDRR_Admin_WBG_2.avif'
    )