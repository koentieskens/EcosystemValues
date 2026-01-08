
import ee
import reverse_geocode
import pandas as pd
from iso3166 import countries
from datetime import datetime
from ..utils.spatial import Spatial
from ..variables.variables import Var, CountryVariable, BenefitVariable, ClimateVariable
from ..variables.land_cover import LandCoverGroup



class Predictions:

    def __init__(self, variables: list, lat: float, lon: float, radius: int = 10000, year=None):
        self.variables = variables
        self.values_dict = {}
        self.lat = lat
        self.lon = lon
        self.radius = radius
        self.country = self.get_country(self.lat, self.lon)
        if year is None:
            self.year = datetime.now().year -1
        else:
            self.year = year

    def get_values(self):
        for variable in self.variables:
           d = self.get_value(variable, self.lat, self.lon, radius=self.radius)
           self.values_dict.update(d)

    @staticmethod
    def get_buffer_size(radius=0, buffer=0):
        return ee.Number(buffer).add(ee.Number(radius))

    @staticmethod
    def get_optimal_scale(feature, buffer_size, scale) -> ee.Number:
        boundariesSide = ee.Number(
            ee.Geometry(feature.buffer(buffer_size).geometry()) \
                .area(100).sqrt().divide(2).round()
        )
        scale = ee.Algorithms.If(
            boundariesSide.eq(0),
            scale,
            ee.Algorithms.If(
                ee.Number(scale).gt(boundariesSide.multiply(0.4)),
                boundariesSide,
                scale
            )
        )
        return scale

    @staticmethod
    def reduce_region(image: ee.Image, feature: ee.Feature, buffer_size: ee.Number, scale: ee.Number) -> ee.Dictionary:
        value = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=feature.buffer(buffer_size).geometry(),  # add buffer around point
            scale=Predictions.get_optimal_scale(feature, buffer_size, scale),
            maxPixels=1e9
        )

        return value.getInfo()

    @staticmethod
    def get_lc(image, feature, buffer_size, scale):
        a = image.reduceRegion(
            reducer=ee.Reducer.frequencyHistogram(),
            geometry=feature.buffer(buffer_size).geometry(),
            scale=Predictions.get_optimal_scale(feature, buffer_size, scale),
            maxPixels=1e9
        )
        a_dict = list(a.getInfo().items())[0][1]
        df = pd.DataFrame(a_dict, index=[0])
        df.columns = df.columns.str.removesuffix('.0')
        df_percentage = df.div(df.sum(axis=1), axis=0) * 100
        df_percentage.reset_index(inplace=True)
        df_percentage.fillna(0, inplace=True)
        d = df_percentage.iloc[0].to_dict()
        return d

    @staticmethod
    def get_country(lat, lon):
        locations = reverse_geocode.get((lat, lon))['country_code']
        return countries.get(locations).alpha3

    def get_wb(self, variable):

        df = variable.var.get_image(countries=[self.country])
        df_val = Spatial.get_country_year_data(df, self.year)
        val = df_val.iloc[0]['value'].item()
        var = variable.var.name
        d = {var: val}
        return d


    def get_value(self, variable, lat, lon, radius=100):
        if variable.var.method == 'wb':
            value =  self.get_wb(variable)
        elif variable.var.method == 'lc':
            image = variable.var.get_image(year=self.year)
            feature = ee.Feature(ee.Geometry.Point(lon, lat), {'radius': radius})
            buffer = variable.var.buffer
            if not buffer:
                buffer = 0
            buffer_size = Predictions.get_buffer_size(radius=radius, buffer=buffer)
            lcs = Predictions.get_lc(image, feature, buffer_size, variable.var.scale)
            relevant_lcs = sum(lcs.get(key, 0) for key in variable.lc.value[1])
            header = variable.lc.get_name(buffer=buffer)
            value = {header: relevant_lcs}

        else:
            image = variable.var.get_image(year=self.year)
            feature = ee.Feature(ee.Geometry.Point(lon, lat), {'radius': radius})
            buffer = variable.var.buffer
            if not buffer:
                buffer = 0
            buffer_size = Predictions.get_buffer_size(radius=radius, buffer=buffer)
            value = Predictions.reduce_region(image, feature, buffer_size, variable.var.scale)
            value = {k: v * variable.var.multiplier for k, v in value.items()}

        return value


if __name__ == "__main__":

    variables = [
        Var(BenefitVariable.ACCESSIBILITY, ln=True, buffer=10000),
        Var(BenefitVariable.ELEVATION),
        Var(BenefitVariable.LAND_COVER, buffer=10000, lc=LandCoverGroup.FOREST),
    ]

    ee.Authenticate()
    ee.Initialize(project='ee-koentieskens')

    p = Predictions(variables, 52.15, 5.15, radius=100)
    p.get_values()
    print(p.values_dict)
