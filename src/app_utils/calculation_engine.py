import streamlit as st
from src.predictions.meta_regression import Predict
from src.app_utils.utils import St_Utils
from src.app_utils.session_states import SessionStateManager as ssm
from src.app_utils.utils import CurrencyConverter
import reverse_geocode
import math
import numpy as np
from iso3166 import countries

class CalculationEngine:

    def calculate_benefit(self):
        """
        Calculates and updates the ecosystem service benefits based on various model
        parameters and user-defined project locations. The calculation incorporates
        benefit prediction, value type conversions, and updates prediction sets
        accordingly. An optional Siikamaki calculation is performed if supported by
        the model class.
        """
        if st.button("Calculate Benefits", type="primary", use_container_width=True):
            try:
                lat = ssm.PROJECT_LOCATION.get()['lat']
                lon = ssm.PROJECT_LOCATION.get()['lon']
                locations = reverse_geocode.get((lat, lon))['country_code']
                country = countries.get(locations).alpha3

                model_class = ssm.MODEL_CLASS.get()
                prediction_sets = ssm.PREDICTION_SETS.get()
                # get the ppp conversion factor to 2024 USD
                conversion_factor = self.convert_to_usd(1, country)
                for vt in model_class.VALUE_TYPES:
                    vt.value = 1.0
                    predicted_values = {}
                    ess = [es for es in model_class.ECOSYSTEM_SERVICES if es.value and es.global_layer is None]
                    if vt.variable.name == 'Cons_Surplus':
                        ess = [es for es in ess if es.variable.welfare]
                    if vt.variable.name == 'Exchange_Value':
                        ess = [es for es in ess if es.variable.exchange]

                    for es in ess:
                        predicted_value = Predict.predict_benefit(model_class, es, vt, ssm.PROJECT_LOCATION.get()['area'])
                        converted_value = predicted_value * conversion_factor
                        predicted_values[es.variable.name] = converted_value
                        if vt.variable.name == 'Cons_Surplus':
                            es.cons_surplus = converted_value

                        if vt.variable.name == 'Exchange_Value':
                            es.exchange_value = converted_value
                    if vt.variable.name == 'Exchange_Value':
                        ess = [es for es in model_class.ECOSYSTEM_SERVICES if es.value and es.global_layer is not None]
                        if len(ess) > 0:
                            conversion_factor = CurrencyConverter.convert_usd_year(1, country, 2020, 2024)
                            for es in ess:
                                val = St_Utils.extract_value_from_gpkg(es.global_layer, lat, lon)
                                converted_value = val * conversion_factor
                                #making sure it returns 0 if Menendez returns nan
                                if not isinstance(converted_value, (int, float)) or math.isnan(converted_value):
                                    converted_value = 0

                                if vt.variable.name == 'Cons_Surplus':
                                    es.cons_surplus = np.nan
                                    predicted_values[es.variable.name] = np.nan
                                if vt.variable.name == 'Exchange_Value':
                                    es.exchange_value = converted_value
                                    predicted_values[es.variable.name] = converted_value

                    prediction_sets[vt.variable.full_name] = predicted_values

                if hasattr(model_class, 'SIIKAMAKI'):
                    siikamaki_benefits = self._calculate_siikamaki()
                    ssm.SIIKAMAKI_BENEFITS.set(siikamaki_benefits)

                ssm.BENEFITS_UPDATED.set(True)
                st.success("Calculation Complete!")
            except IndexError:
                st.error("We could not find appropriate benefit predictions for your location. Please make sure your location is suitable for the selected biome.")
            except Exception as e:
                st.error(f"Error calculating benefits: {e}")


    @staticmethod
    def convert_to_usd(value, country, from_year=2020, to_year=2024):
        """
        Converts a monetary value from a specific country's purchasing power
        parity (PPP) to its equivalent in US dollars for given years using
        a currency conversion system.

        This method provides an easy interface for converting currency
        based on PPP adjustments between specified years.

        :param value: Monetary value in the international $ to be converted.
        :type value: float
        :param country: The country of the local currency. in ISO 3166-1 alpha-3 format.
        :type country: str
        :param from_year: The initial year for the PPP adjustment, with a
            default value of 2020.
        :type from_year: int, optional
        :param to_year: The final year for the PPP adjustment, with a
            default value of 2024.
        :type to_year: int, optional
        :return: The equivalent monetary value in US dollars in {from_year}.
        :rtype: float
        """
        print('converting')
        return CurrencyConverter.convert_ppp_to_usd(value, country, from_year, to_year)

    def _calculate_siikamaki(self):
        """
        Calculates values per hectare for selected layers based on Siikamaki model.

        This method processes a set of layers defined by the provided Siikamaki
        model class. For each layer that has an associated enabled variable,
        it calculates values per hectare by extracting global layer values
        using the specified area of interest (AOI). Each layer's value is then
        stored in the corresponding variable object and a list summarizing these
        values is returned. If no AOI is provided, the function returns None.

        :param self: The class instance from which this private method is invoked.
        :return: A list of dictionaries where each dictionary represents a layer
                 and its calculated value per hectare, or None if no AOI is
                 defined.
        :rtype: list[dict[str, Any]] or None
        """
        model_class = ssm.MODEL_CLASS.get()
        # Validate inputs
        if ssm.AOI_GDF.get() is not None:

            siikamaki_layers = [var_obj for var_obj in model_class.SIIKAMAKI if var_obj.value]
            lat = ssm.PROJECT_LOCATION.get()['lat']
            lon = ssm.PROJECT_LOCATION.get()['lon']
            locations = reverse_geocode.get((lat, lon))['country_code']
            country = countries.get(locations).alpha3
            # Siikamaki values are in 2017 int $
            conversion_factor = self.convert_to_usd(1, country, from_year=2017)
            values_per_ha = []
            for var_obj in siikamaki_layers:
                layer = var_obj.variable
                value = St_Utils.extract_global_layer_single(layer, ssm.AOI_GDF.get())
                converted_value = value * conversion_factor
                dict_pair = {layer.full_name: converted_value}
                values_per_ha.append(dict_pair)
                var_obj.cons_surplus = converted_value
                var_obj.exchange_value = converted_value

            return values_per_ha
        else:
            return None

    def calculate_costs(self):
        """
        Calculate costs based on the cost model and project location data.

        This method calculates costs either using global layers or nature-based solutions
        (NBS) associated with the provided model class. It identifies the project location,
        determines the appropriate cost calculation method (based on availability of global
        layers or NBS), and performs the cost prediction. For global layers, it retrieves and
        converts the costs to USD. For NBS, it calculates predicted values for each selected NBS
        and converts them to USD. If no applicable cost model exists, the method returns None.

        The calculation can only proceed when the "Calculate Costs" button is pressed. Data
        is processed and returned based on the attributes of the accessed cost model.

        :returns:
            - If global layers are available, the converted cost per hectare as a float.
            - If nature-based solutions are used, a list of dictionaries containing the
              predicted costs converted to USD.
            - None if no applicable cost model is found or if the button is not pressed.
        """
        model_class = ssm.MODEL_CLASS.get()


        try:
            lat = ssm.PROJECT_LOCATION.get()['lat']
            lon = ssm.PROJECT_LOCATION.get()['lon']
            locations = reverse_geocode.get((lat, lon))['country_code']
            country = countries.get(locations).alpha3

            if hasattr(model_class.COST_MODEL, 'GLOBAL_LAYERS'):
                # Bush et al values are in 2020 USD
                conversion_factor = CurrencyConverter.convert_usd_year(1, country, 2020, 2024)
                cost_layers = [var_obj.variable for var_obj in model_class.COST_MODEL.GLOBAL_LAYERS if var_obj.value]
                cost_per_ha = St_Utils.extract_global_layers(cost_layers, **ssm.PROJECT_LOCATION.get())
                try:
                    converted_costs = [{k: v * conversion_factor for k, v in d.items()} for d in cost_per_ha]
                except TypeError:
                    #TODO this needs ot be handled at the root and explained to the user that there is no dat for EU and US
                    st.warning('No forest restoration data available for this area')
                    return None

                # AV = PV * r/(1-(1+r)^(-1*years)) (from email from Luke Brander)
                #convert to annual values from present values
                def annualize(pv, r, years):
                    try:
                        av = pv * r / (1 - (1 + r)**(-1 * years))
                    except TypeError:
                        av = 0

                    return av
                annualized_costs = [{k: annualize(v, 0.05, 30) for k, v in d.items()} for d in converted_costs]

                annualized_lookup = {k: v for cost_dict in annualized_costs for k, v in cost_dict.items()}

                # Update cost_layers items
                for var_obj in model_class.COST_MODEL.GLOBAL_LAYERS:
                    if var_obj.variable.full_name in annualized_lookup:
                        var_obj.cost_value = annualized_lookup[var_obj.variable.full_name]

                return annualized_costs

            elif hasattr(model_class.COST_MODEL, 'NBS'):
                if not ssm.COST_EXTRACTION_DONE.get():
                    st.warning('Please extract cost spatial variables first in menu above')
                    return None
                predicted_values = {}
                nbss = [nbs for nbs in model_class.COST_MODEL.NBS if nbs.value]
                # Cost values are in 2021 int $
                if model_class.COST_MODEL.__name__ == 'MangroveCost':
                    conversion_factor = CurrencyConverter.convert_usd_year(1, country, 2020, 2024)
                else:
                    conversion_factor = self.convert_to_usd(1, country, from_year=2021)

                area = ssm.PROJECT_LOCATION.get()['area']
                lat = ssm.PROJECT_LOCATION.get()['lat']
                for nbs in nbss:
                    predicted_value = Predict.predict_cost(model_class.COST_MODEL, nbs, area, lat)
                    converted_value = predicted_value * conversion_factor
                    predicted_values[nbs.variable.name] = converted_value
                    nbs.cost_value = converted_value

                st.success("Calculation Complete!")
                result = [{key: float(value)} for key, value in predicted_values.items()]

                return result

            else:
                return None
        except Exception as e:
            st.error(f"Error calculating costs: {e}")
