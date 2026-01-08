import ee
import wbgapi as wb


class GeeImageExtractor:

    @staticmethod
    def get_accessibility(gee_path: str = None, name: str = 'accessibility', **kwargs):

        timeToCityImg = ee.Image(gee_path)
        # to mask out water
        land_cover = ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V-C3/Global")
        # mask out water areas
        waterMask = land_cover.select("discrete_classification").first().neq(200)

        mask = timeToCityImg.neq(-9999).add(waterMask).eq(2)
        timeToCityImg = timeToCityImg.mask(mask).rename(name)
        return timeToCityImg

    @staticmethod
    def get_population_age(gee_path: str = None, name: str = 'population_age', **kwargs):

        population_age = ee.ImageCollection(gee_path).mosaic()
        pop_age = population_age.expression(
            ee.String('( (b(1)+b(19))*1 + (b(2)+b(20))*2.5 + (b(3)+b(21))*7.5 + ')
            .cat('(b(4)+b(22))*12.5 + (b(5)+b(23))*17.5 + (b(6)+b(24))*22.5 + ')
            .cat('(b(7)+b(25))*27.5 + (b(8)+b(26))*32.5 + (b(9)+b(27))*37.5 + ')
            .cat('(b(10)+b(28))*42.5 + (b(11)+b(29))*47.5 + (b(12)+b(30))*52.5 + ')
            .cat('(b(13)+b(31))*57.5 + (b(14)+b(32))*62.5 + (b(15)+b(33))*67.5 + ')
            .cat('(b(16)+b(34))*72.5 + (b(17)+b(35))*77.5 + (b(18)+b(36))*82.5) / b(0)'), {})
        population_age = pop_age.rename(name)

        return population_age

    @staticmethod
    def get_protection_status(gee_path: str = None, name: str = 'protection_status', year: int = 2024, **kwargs):

        # get protected areas (only definitive ones, not the proposed ones
        protection_status = ee.FeatureCollection(gee_path).filter(
            ee.Filter.eq('PA_DEF', '1')
        )
        # tranlate to image
        prot_area_image = protection_status.reduceToImage(
            properties=['STATUS_YR'],
            reducer=ee.Reducer.min(),
            #scale=300
        )
        current_year = prot_area_image.lte(year)

        binary_image = current_year.updateMask(current_year)
        binary_image = binary_image.unmask(0).rename(name)

        return binary_image

    @staticmethod
    def get_protection_status2(gee_path: str = None, name: str = 'protection_status', year: int = 2024):
        image = ee.Image(gee_path)
        image_year = image.lte(year).unmask(0).rename(name)
        return image_year

    @staticmethod
    def get_land_cover(gee_path: str = None, name: str = 'land_cover', year: int = 2024):
        """
        Gets the land cover image corresponding to the specified year from the specified
        Google Earth Engine (GEE) path. The land cover is based on the Climate Change
        Initiative (CCI) land cover products for the years 1992 to 2022. It ensures
        that the year falls within the valid range (1992–2022). If the year is outside
        this range, it adjusts the year to the nearest valid boundary. The function
        returns the resulting image with the specified band name.
        This code was adapted from openforisearthmap gee JS repository

        Parameters
        ----------
        gee_path : str, optional
            Google Earth Engine path of the base image to use (defaults to None).

        name : str, optional
            Name of the resulting band in the returned image (defaults to 'land_cover').

        year : int, optional
            Year for which the land cover should be retrieved within the range [1992, 2022]
            (defaults to None).

        Returns
        -------
        ee.Image
            An Earth Engine imagery object with the specified band name and data
            corresponding to the specified year.
        """
        cci_lc_stack = ee.Image(gee_path)\
            .addBands(ee.Image("projects/ee-maidiesinitam/assets/cci-2019").select([0], ["b28"])) \
            .addBands(ee.Image("projects/ee-maidiesinitam/assets/cci-2020").select([0], ["b29"])) \
            .addBands(ee.Image("projects/ee-maidiesinitam/assets/cci-2021").select([0], ["b30"])) \
            .addBands(ee.Image("projects/ee-maidiesinitam/assets/cci-2022").select([0], ["b31"]))

        year = ee.Number(year)
        year = ee.Number(ee.Algorithms.If(year.gt(2022), 2022, year))
        year = ee.Number(ee.Algorithms.If(year.lt(1992), 1992, year))
        band_sequence = year.subtract(1992).add(1).int16()

        image = ee.Image(
            cci_lc_stack.select([ee.String('b').cat(band_sequence)], ['cci'])
        ).rename(name)
        return image

    @staticmethod
    def calculate_date_distance_from_year(collection: ee.ImageCollection, year: int, **kwargs):
        """
        Adds a property to each image in the collection with the absolute date distance (in milliseconds)
        from the start of a given year.

        :param collection: ee.ImageCollection to process.
        :param year: Year (int) for the reference date.
        :return: Updated ee.ImageCollection with a 'dateDist' property for each image.
        """
        date_of_interest = ee.Date.fromYMD(ee.Number(year), 1, 1)

        def add_date_dist(image):
            date_dist = ee.Number(image.get('system:time_start')).subtract(
                date_of_interest.millis()
            ).abs()
            return image.set('dateDist', date_dist)

        updated_collection = collection.map(add_date_dist)
        return updated_collection

    @staticmethod
    def get_hanpp(gee_path: str = None, name: str = 'hanpp', **kwargs):

        hanpp = ee.Image(gee_path)
        # get value per m^2
        pixel_size = ee.Number(hanpp.projection().nominalScale()).pow(2)
        hanpp_per_m = hanpp.divide(pixel_size)
        # covert to millions of kf of carbon from grams
        hanpp_per_m = hanpp_per_m.divide(ee.Image(1000)).rename(name)

        return hanpp_per_m

    @staticmethod
    def get_npp(gee_path: str = None, name: str = 'npp', year: int = 2024,**kwargs):

        collection = GeeImageExtractor.calculate_date_distance_from_year(
            ee.ImageCollection(gee_path), year
        )
        image = collection.sort('dateDist').first().unmask().select('Npp').rename(name)

        return image

    @staticmethod
    def get_npp_max(gee_path: str = None, name: str = 'npp_max', year: int = 2024,**kwargs):

        #start_date = "2001-01-01"
        #end_date = f"{year}-12-31"
        collection = ee.ImageCollection(gee_path).select('Npp')

        image = collection.max().unmask().rename(name)

        return image

    @staticmethod
    def get_npp_share(gee_path: str = None, name: str = 'npp_share', year: int = 2024,**kwargs):
        npp_year = GeeImageExtractor.get_npp(gee_path, year=year)
        npp_max = GeeImageExtractor.get_npp_max(gee_path, year=year)
        npp_share = npp_year.divide(npp_max).rename(name)
        return npp_share

    @staticmethod
    def get_human_modif_index(gee_path: str = None, name: str = 'HumanModifIndex', year: int = 2024, **kwargs):


        available_years = [1990, 1995, 2000, 2005, 2010, 2015, 2017]
        data_year = min(available_years, key=lambda x: abs(x - year))
        if data_year == 2017:
            humanModifIndex = f'{gee_path}_{data_year}_300_60land'
        else:
            humanModifIndex = f'{gee_path}_{data_year}c_300_60land'

        image = ee.Image(humanModifIndex).rename(name)

        return image

    @staticmethod
    def get_human_modif_indexb(gee_path: str = None, name: str = 'HumanModifIndex', year: int = 2024, **kwargs):
        available_years = [1990, 2000, 2010, 2015]
        data_year = min(available_years, key=lambda x: abs(x - year))
        gee_path = f'{gee_path}{data_year}'
        image = ee.Image(gee_path).select('b1').divide(65536).rename(name)
        return image


    @staticmethod
    def get_settlement(gee_path: str = None, name: str = 'settlements', year: int = 2024, **kwargs):


        available_years = range(1975, 2031, 5)
        data_year = min(available_years, key=lambda x: abs(x - year))
        settlements = f'{gee_path}/{data_year}'
        image = ee.Image(settlements).divide(100).unmask().select('built_surface').rename(name)

        return image

    @staticmethod
    def get_slope(gee_path: str = None, name: str = 'slope', **kwargs):

        srtm30 = ee.Image(gee_path).rename(name)
        slope = ee.Terrain.slope(srtm30).select('slope').rename(name)

        return slope

    @staticmethod
    def get_dry_days(gee_path: str = None, name: str = 'dry_days', dry_threshold: float = 0.001, year: int = 2024, **kwargs):

        precipitation = ee.ImageCollection(gee_path).select('total_precipitation_sum')
        year = year - 1
        if year < 1981:
            year = 1981
        date_range = ee.DateRange(f'{year}-01-01', f'{year}-12-31')

        yearCollection = precipitation.filter(ee.Filter.date(date_range))
        dry_threshold = ee.Number(dry_threshold)
        dry_days = yearCollection.map(lambda image: image.lt(dry_threshold).selfMask())
        sum_dry_days = dry_days.sum().rename(name)

        return sum_dry_days

    @staticmethod
    def get_frost_days(gee_path: str = None, name: str = 'frost_days', frost_threshold: int = 273, year: int = 2024, **kwargs) -> ee.Image:
        """

        :param gee_path: path to gee asset
        :param name: name of the output layer
        :param frost_threshold: threshold for frost days in degrees Kelvin
        :return: ee.Image of desired layer
        """

        # Daily precipitation in meters
        temperature = ee.ImageCollection(gee_path).select('temperature_2m_min')
        year = year - 1
        if year < 1981:
            year = 1981
        date_range = ee.DateRange(f'{year}-01-01', f'{year}-12-31')

        yearCollection = temperature.filter(ee.Filter.date(date_range))
        frost_threshold = ee.Number(frost_threshold)
        frost_days = yearCollection.map(lambda image: image.lt(frost_threshold))
        sum_frost_days = frost_days.sum().rename(name)

        return sum_frost_days

    @staticmethod
    def get_heat_days(gee_path: str = None, name: str = 'frost_days', heat_threshold: int = 308, year:int = 2024, **kwargs) -> ee.Image:
        """

        :param gee_path:
        :param name:
        :param heat_threshold: heat threshold in degrees kelvin. note koen: 35 C seems a little high.
        :return: ee.Image of desired layer
        """

        # Daily precipitation in meters
        temperature = ee.ImageCollection(gee_path).select('temperature_2m_max')
        year = year - 1
        if year < 1981:
            year = 1981
        date_range = ee.DateRange(f'{year}-01-01', f'{year}-12-31')

        yearCollection = temperature.filter(ee.Filter.date(date_range))
        heat_threshold = ee.Number(heat_threshold)
        heat_days = yearCollection.map(lambda image: image.gte(heat_threshold))
        sum_heat_days = heat_days.sum().rename(name)

        return sum_heat_days

    @staticmethod
    def get_mean_annual_temperature(gee_path: str = None, name: str = 'mean_annual_temperature', year: int = 2024, **kwargs):

        temperature = ee.ImageCollection(gee_path).select('temperature_2m')
        year = year - 1
        if year < 1981:
            year = 1981
        date_range = ee.DateRange(f'{year}-01-01', f'{year}-12-31')
        yearCollection = temperature.filter(ee.Filter.date(date_range))

        mean_annual_temperature = yearCollection.mean().rename(name)
        mean_annual_temperature_c = mean_annual_temperature.subtract(273.15) # to celsius note Koen: I don't understand why you would do this
                                                                             # Kelvin should perform better in regressions.

        return mean_annual_temperature_c

    @staticmethod
    def get_total_annual_precipitation(gee_path: str = None, name: str = 'total_annual_precipitation', year: int = 2024, **kwargs):

        precipitation = ee.ImageCollection(gee_path).select('total_precipitation_sum')
        year = year - 1
        if year < 1981:
            year = 1981
        date_range = ee.DateRange(f'{year}-01-01', f'{year}-12-31')
        yearCollection = precipitation.filter(ee.Filter.date(date_range))
        total_annual_precipitation = yearCollection.sum().rename(name)
        return total_annual_precipitation

    @staticmethod
    def get_mean_NDVI(gee_path: str = None, name: str = 'NDVI_mean', start_year: int = 2000, end_year: int = 2018, water_threshold=0.5, **kwargs) -> ee.Image:

        years = ee.List.sequence(start_year, end_year)
        # create water mask
        water_freq = GeeImageExtractor.get_water_freq(start_year, end_year)
        water_mask = water_freq.lt(water_threshold)


        def yearly_ndvi_percentile(year):
            start_date = ee.Date.fromYMD(year, 1, 1)
            end_date = ee.Date.fromYMD(year, 12, 31)

            ndvi = (ee.ImageCollection(gee_path)
                    .filterDate(start_date, end_date)
                    .select('NDVI')
                    .map(lambda img: img.multiply(0.0001)))  # scale MODIS NDVI

            ndvi_95 = ndvi.reduce(ee.Reducer.percentile([95])).updateMask(water_mask)
            return ndvi_95.set('year', year)

        # Generate NDVI 95th percentile for each year
        annual_ndvi = ee.ImageCollection(years.map(yearly_ndvi_percentile))

        # Compute mean NDVI over all years
        mean_ndvi = annual_ndvi.mean().rename(name)
        return mean_ndvi

    @staticmethod
    def get_senslope_NDVI(gee_path: str = None, name: str = 'NDVI_sen_slope',
                          start_year: int = 2000, end_year: int = 2018,
                          water_threshold = 0.5, **kwargs) -> ee.Image:

        years = ee.List.sequence(start_year, end_year)
        # create water mask
        water_freq = GeeImageExtractor.get_water_freq(start_year, end_year)
        water_mask = water_freq.lt(water_threshold)
        def yearly_ndvi_percentile(year):
            start_date = ee.Date.fromYMD(year, 1, 1)
            end_date = ee.Date.fromYMD(year, 12, 31)

            ndvi = (ee.ImageCollection(gee_path)
                    .filterDate(start_date, end_date)
                    .select('NDVI')
                    .map(lambda img: img.multiply(0.0001)))  # scale MODIS NDVI

            ndvi_95 = ndvi.reduce(ee.Reducer.percentile([95])).updateMask(water_mask)
            return ndvi_95.set('year', year)

        def add_year_bands(img):
            # Select and cast NDVI to float
            ndvi = img.select('NDVI_p95').toFloat()

            # Compute year difference from baseYear
            year = ee.Number(img.get('year')).subtract(start_year).toFloat()

            # Create an image with constant 'year' value
            year_img = (ee.Image.constant(year)
                        .rename('year')
                        .toFloat()
                        .setDefaultProjection(ndvi.projection())
                        .updateMask(ndvi.mask()))

            # Combine NDVI and year images into bands
            return ndvi.addBands(year_img).set('year', year)


        # Generate NDVI 95th percentile for each year
        annual_ndvi = ee.ImageCollection(years.map(yearly_ndvi_percentile))
        yearly = annual_ndvi.map(add_year_bands)
        # Compute mean NDVI over all years
        senslope_ndvi = (yearly
                         .select(['year', 'NDVI_p95'])
                         .reduce(ee.Reducer.sensSlope())
                         .select('slope')
                         .rename(name))

        return senslope_ndvi

    @staticmethod
    def get_water_freq(start_year, end_year, **kwargs):
        """
        Calculates water frequency using historical monthly water observations and smooths the
        result over the past three years.

        The function imports historical monthly water observations from JRC water frequency data,
        performs calculations to determine water frequency over three years, and applies a
        smoothing function. The smoothed water frequency is clipped to the area of interest
        (clip_aoi) and returned as an Earth Engine image.

        Raises:
            Exception: If importing or calculating water frequency fails.

        Returns:
            ee.Image: Clipped smoothed water frequency image for the area of interest.
        """

        start_year = max(1984, start_year)
        end_year = min(2019, end_year)

        start_date = ee.Date.fromYMD(start_year, 1, 1)
        end_date = ee.Date.fromYMD(end_year, 12, 31)

        JRC_HIST_WATER = "JRC/GSW1_4/MonthlyHistory"
        jrc_water_freq = (ee.ImageCollection(JRC_HIST_WATER)
                          .filterDate(start_date, end_date))

        def smoother(img):
            yearCol = ee.ImageCollection.fromImages(img.get('year_matches'))
            out = yearCol.map(lambda x:  x.eq(2).rename('water').selfMask()).select('water').reduce(
                ee.Reducer.count(),4).divide(
                    yearCol.map(lambda y: y.gt(0).selfMask()).select('water').reduce(
                        ee.Reducer.count(),4)).unmask(0).rename('water_frequency').set(
                'system:time_start',
                ee.Date(img.date().update(
                    year=ee.Number(img.date().get('year')),
                    month=7,
                    day=1,
                    hour=0,
                    minute=0,
                    second=0)).millis())
            return out

        def harmonize_ts(collection):
            """
            A function to group images per year for aggregation
            :param collection: ImageCollection
            :return: Grouped image collection
            """

            collection = collection.map(lambda img: img.set('year', ee.String(img.date().get('year'))))
            distinctYearCol = collection.distinct('year')
            filter = ee.Filter.equals(leftField='year', rightField='year')
            join = ee.Join.saveAll('year_matches')
            joinCol = ee.ImageCollection(join.apply(distinctYearCol, collection, filter))
            return joinCol

        water_ts_smooth = harmonize_ts(jrc_water_freq).map(smoother).map(
                lambda z: z.addBands(z.metadata('system:time_start').divide(3.154e10).add(1970))
            )

        water_freq = water_ts_smooth.sort('system:time_start', False).first().select('water_frequency')

        return water_freq

    @staticmethod
    def get_heavy_rain_days(gee_path: str = None, name: str = 'frost_days', rain_threshold: float = 0.05, year: int = 2024, **kwargs) -> ee.Image:
        """

        :param gee_path:
        :param name:
        :param heat_threshold: heat threshold in degrees kelvin. note koen: 35 C seems a little high.
        :return: ee.Image of desired layer
        """

        # Daily precipitation in meters
        temperature = ee.ImageCollection(gee_path).select('total_precipitation_sum')
        year = year - 1
        if year < 1981:
            year = 1981
        date_range = ee.DateRange(f'{year}-01-01', f'{year}-12-31')

        yearCollection = temperature.filter(ee.Filter.date(date_range))
        rain_days = yearCollection.map(lambda image: image.gt(rain_threshold))
        sum_rain_days = rain_days.sum().rename(name)

        return sum_rain_days

    @staticmethod
    def get_image_from_timeseries(gee_path: str = None, name: str = None, year: int = 2024, **kwargs):


        collection = GeeImageExtractor.calculate_date_distance_from_year(
            ee.ImageCollection(gee_path), year
        )
        image = collection.sort('dateDist').first().unmask().rename(name)

        return image

    @staticmethod
    def get_image_from_single_image(gee_path: str = None, name: str = None, **kwargs):

        image = ee.Image(gee_path).rename(name)
        return image

    @staticmethod
    def get_first_image_from_collection(gee_path: str = None, name: str = None, **kwargs):

        image = ee.ImageCollection(gee_path).first().rename(name)
        return image

    @staticmethod
    def get_wb(gee_path: str = 'NY.GDP.PCAP.CD',  countries: str = 'USA', year: int = 2024, **kwargs):

        df = wb.data.DataFrame(gee_path, countries)
        return df




def export_to_asset(self, image: ee.Image, asset_id: str, description: str = None, scale: int = 1000,
                    crs: str = 'EPSG:4326', max_pixels: int = 1e13, **kwargs) -> ee.batch.Task:
    """
    Exports an Earth Engine Image to Google Earth Engine Asset.

    Args:
        image (ee.Image): The image to export
        asset_id (str): The asset ID where the image should be exported to (e.g., 'users/username/asset_name')
        description (str, optional): Description for the export task. Defaults to asset_id if not provided
        scale (int, optional): The scale in meters of the output. Defaults to 1000
        crs (str, optional): The coordinate reference system. Defaults to 'EPSG:4326'
        max_pixels (int, optional): The maximum number of pixels to export. Defaults to 1e13

    Returns:
        ee.batch.Task: The export task that can be used to monitor the export progress

    Raises:
        ValueError: If image or asset_id is None
    """

    # Create the export task
    task = ee.batch.Export.image.toAsset(
        image=image,
        description=description,
        assetId=asset_id,
        scale=scale,
        crs=crs,
        region=self.bounding_box,
        maxPixels=max_pixels
    )

    # Start the task
    task.start()

    return task




