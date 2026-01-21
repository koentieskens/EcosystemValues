import streamlit as st
from src.predictions.meta_regression import Predict
from src.app_utils.utils import St_Utils
from src.app_utils.session_states import SessionStateManager as ssm

class CalculationEngine:

    def calculate_benefit(self):

        if st.button("Calculate Benefits", type="primary", use_container_width=True):


            model_class = ssm.MODEL_CLASS.get()
            prediction_sets = ssm.PREDICTION_SETS.get()
            for vt in model_class.VALUE_TYPES:
                vt.value = 1.0
                predicted_values = {}
                ess = [es for es in model_class.ECOSYSTEM_SERVICES if es.value]

                for es in ess:
                    predicted_value = Predict.predict_benefit(model_class, es, vt, ssm.PROJECT_LOCATION.get()['area'])
                    predicted_values[es.variable.name] = predicted_value
                    if vt.variable.name == 'Cons_Surplus':
                        es.cons_surplus = predicted_value
                    if vt.variable.name == 'Exchange_Value':
                        es.exchange_value = predicted_value
                prediction_sets[vt.variable.full_name] = predicted_values

            if hasattr(model_class, 'SIIKAMAKI'):
                siikamaki_benefits = self._calculate_siikamaki()
                ssm.SIIKAMAKI_BENEFITS.set(siikamaki_benefits)

            ssm.BENEFITS_UPDATED.set(True)
            st.success("Calculation Complete!")


    def _calculate_siikamaki(self):

        model_class = ssm.MODEL_CLASS.get()
        # Validate inputs
        if ssm.AOI_GDF.get() is not None:

            siikamaki_layers = [var_obj for var_obj in model_class.SIIKAMAKI if var_obj.value]
            values_per_ha = []
            for var_obj in siikamaki_layers:
                layer = var_obj.variable
                value = St_Utils.extract_global_layer_single(layer, ssm.AOI_GDF.get())
                dict_pair = {layer.full_name: value}
                values_per_ha.append(dict_pair)
                var_obj.cons_surplus = value
                var_obj.exchange_value = value

            return values_per_ha
        else:
            return None

    def calculate_costs(self):
        model_class = ssm.MODEL_CLASS.get()
        if st.button("Calculate Costs", type="primary", use_container_width=True):

            if hasattr(model_class.COST_MODEL, 'GLOBAL_LAYERS'):
                cost_layers = [var_obj.variable for var_obj in model_class.COST_MODEL.GLOBAL_LAYERS if var_obj.value]
                cost_per_ha = St_Utils.extract_global_layers(cost_layers, **ssm.PROJECT_LOCATION.get())
                return cost_per_ha

            elif hasattr(model_class.COST_MODEL, 'NBS'):
                predicted_values = {}
                nbss = [nbs for nbs in model_class.COST_MODEL.NBS if nbs.value]

                for nbs in nbss:
                    area = ssm.PROJECT_LOCATION.get()['area']
                    lat = ssm.PROJECT_LOCATION.get()['lat']
                    predicted_value = Predict.predict_cost(model_class.COST_MODEL, nbs, area, lat)
                    predicted_values[nbs.variable.name] = predicted_value

                st.success("Calculation Complete!")
                result = [{key: float(value)} for key, value in predicted_values.items()]
                return result

            else:
                return None
        else:
            return None