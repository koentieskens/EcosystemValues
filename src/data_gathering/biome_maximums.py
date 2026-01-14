import ee
from src.variables.variables import ModelVariable
from src.variables.spatial_variable import BenefitSpatialVariable, ClimateSpatialVariable
import geemap
from tqdm import tqdm
import pandas as pd

ee.Initialize(project='ee-koentieskens')

ecoRegions = ee.FeatureCollection('RESOLVE/ECOREGIONS/2017')

variable = ModelVariable(ClimateSpatialVariable.MEAN_NDVI_P95)
ndvi = ModelVariable(ClimateSpatialVariable.MEAN_NDVI_P95).variable.get_image(start_year=2018, end_year=2019)
intactness =  ModelVariable(BenefitSpatialVariable.BIODIVERSITY_INTACTNESS).variable.get_image(year=2020)
NPP_year = ModelVariable(BenefitSpatialVariable.NPP_YEAR).variable.get_image(year=2020)
NPP_max = ModelVariable(BenefitSpatialVariable.NPP_MAX).variable.get_image(year=2020)

NPP_share = NPP_year.divide(NPP_max)

def get_values(image, features, name):

    def extract_values(feature):
        # Get the feature geometry
        geometry = feature.geometry()

        # Reduce the image over this single geometry
        values = image.reduceRegion(
            reducer=ee.Reducer.max(),
            geometry=geometry,
            scale=5000,
            maxPixels=1e8
        )

        # Return feature with new properties
        return ee.Feature(None, {
            'ECO_NAME': feature.get('ECO_NAME'),
            name: values.get(name)  # Replace 'NDVI' with your actual band name
        })

    result = features.select(['ECO_NAME', 'BIOME_NAME']).map(extract_values)
    return result

biomes = ecoRegions.aggregate_array('BIOME_NAME').distinct().getInfo()

name = ModelVariable(ClimateSpatialVariable.MEAN_NDVI_P95).variable.name
results = []
for biome in tqdm(biomes[1:]):
    biome_ecoregions = ecoRegions.filter(ee.Filter.eq('BIOME_NAME', biome))
    result = get_values(ndvi, biome_ecoregions, name)
    results.append(result)

row_list = []
for result in tqdm(results):
    list_of_dicts = result.getInfo()['features']
    for d in list_of_dicts:
        row = d['properties']
        row_list.append(row)


def get_biome_at_point(lon, lat, ecoregions_fc):
    # Create point geometry
    point = ee.Geometry.Point([lon, lat])
    point = point.buffer(1000)
    # Filter ecoregions that contain this point
    containing_region = ecoregions_fc.filterBounds(point).first()

    # Get the BIOME_NAME
    biome_name = containing_region.get('BIOME_NAME')

    return biome_name.getInfo()


def get_max_ndvi_for_point(lon, lat, ecoregions_fc, ndvi_image):
    # Get the biome name at this point
    point = ee.Geometry.Point([lon, lat]).buffer(500)

    # Get the ecoregion at this point
    point_region = ecoregions_fc.filterBounds(point).first()

    # Get the combined geometry of all regions in this biome
    biome_geometry = point_region.geometry().simplify(maxError=10000)


    max_ndvi = ndvi_image.reduceRegion(
        reducer=ee.Reducer.max(),
        geometry=biome_geometry,
        scale=5000,
        maxPixels=1e9,
        tileScale=16,  # Let EE handle the splitting
        bestEffort=True
    )

    return max_ndvi.getInfo()['ndviP95']

# Usage
result = get_max_ndvi_for_point(5, 50, ecoRegions, ndvi)



print(f"Biome: {result['biome_name']}")
print(f"Max NDVI: {result['max_ndvi']}")

ecoRegions = ee.FeatureCollection('RESOLVE/ECOREGIONS/2017')
# Usage
biome = get_biome_at_point(-74.0, 40.7, ecoRegions)  # NYC coordinates
print(biome)

df = pd.DataFrame(row_list)
df.to_csv('c:/users/koen/documents/biome_maximums_npp_share.csv')

test = results[0].getInfo()

