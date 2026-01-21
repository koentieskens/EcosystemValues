
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.models.benefit_models import (
    TropicalForest, TemparateForest, IntensiveLandUse,
    Mangroves, Grassland)
import streamlit as st
from src.app_utils.utils import St_Utils
from app import EcoApp
import base64


class UIRenderer:
    # Configuration
    ECOSYSTEM_MODELS = {
        'tropical_forest': TropicalForest,
        'temperate_forest': TemparateForest,
        'intensive_land_use': IntensiveLandUse,
        'mangroves': Mangroves,
        'grassland': Grassland
    }

    ECOSYSTEM_DISPLAY_NAMES = {
        'tropical_forest': 'Tropical Forest',
        'temperate_forest': 'Temperate Forest',
        'intensive_land_use': 'Intensive Land Use',
        'mangroves': 'Mangroves',
        'grassland': 'Grassland'
    }

    BIOME_LOGOS = {
        'tropical_forest': '🌴',
        'temperate_forest': '🌲',
        'intensive_land_use': '🏭',
        'mangroves': '🌿',
        'grassland': '🌾'
    }

    def biome_selection_boxes(self):
        """
        Renders biome selection interface and returns selection data if a button was clicked.

        Returns:
            dict or None: Selection data if a biome was selected, None otherwise
        """
        cols = st.columns(len(self.ECOSYSTEM_DISPLAY_NAMES.items()))

        for i, (ecosystem_key, display_name) in enumerate(self.ECOSYSTEM_DISPLAY_NAMES.items()):
            with cols[i]:
                if self._render_biome_button(ecosystem_key, display_name):
                    self._update_session_state_with_biome(ecosystem_key)

        self._display_biome_selection()

    def _render_biome_button(self, key, display_name):
        """Returns True if button was clicked"""
        logo = self.BIOME_LOGOS.get(key, '🌱')
        return st.button(
            f"{logo}\n\n{display_name}",
            key=f"biome_select_{key}",
            use_container_width=True
        )

    def _update_session_state_with_biome(self, key):
        """Creates selection data without modifying internal state"""
        ss = st.session_state
        model_class = self.ECOSYSTEM_MODELS[key]
        ss.ecosystem_type = key
        ss.model_class = model_class()
        ss.ecosystem_display_name = self.ECOSYSTEM_DISPLAY_NAMES[key]

    def _display_biome_selection(self):
        """Displays current selection status"""
        if st.session_state.ecosystem_type:
            st.success(f"✅ **Selected Ecosystem:** {st.session_state.ecosystem_display_name}")
        else:
            st.info("👆 **Please select a biome above to continue**")

    def sub_biomes_menu(self):
        ss = st.session_state
        if hasattr(ss.model_class, 'SUB_BIOMES') and ss.model_class.SUB_BIOMES:

            selected_option = self._sub_biome_button()

            # Set only the selected one to True
            for var_obj in ss.model_class.SUB_BIOMES:
                if var_obj.variable.full_name == selected_option:
                    var_obj.value = 1
                else:
                    var_obj.value = 0
        else:
            st.info("No sub-biomes available for this ecosystem type.")


    def _sub_biome_button(self):
        ss = st.session_state
        return st.radio(
            "Select Sub-biome:",
            options=[var_obj.variable.full_name for var_obj in ss.model_class.SUB_BIOMES],  # Display names
            key=f"sub_biome_{ss.ecosystem_type}",
            help="Choose the sub-biome that best describes your study area"
        )

    def cost_spatial_variables_menu(self, vartype='cost'):
        if hasattr(st.session_state.model_class, 'VARIABLES'):
            ss = st.session_state

            if vartype == 'cost':
                model = ss.model_class.COST_MODEL
            else:
                model = ss.model_class

            if hasattr(model, 'VARIABLES'):
                for var_obj in model.VARIABLES:
                    var_obj.value = self._spatial_variable_field(var_obj, vartype=vartype)

                if st.button("🔄 Extract Spatial Values from GEE", type="primary",
                             use_container_width=True,
                             key=f'{vartype}_gee'):
                    self._get_variable_values_from_gee(vartype=vartype)

                # this is to make sure that manual edits are not automatically overwritten
                if st.session_state.get(f'{vartype}_update_from_extraction', False):
                    st.session_state[f'{vartype}_update_from_extraction'] = False
            else:
                st.info("No spatial variables needed for this biome.")
        else:
            st.info("Please select a biome first")

    def _spatial_variable_field(self, var_obj, vartype='cost'):
        ss = st.session_state

        if var_obj.lc is not None:
            display_name = var_obj.lc.full_name
            var_key = var_obj.lc.get_name(var_obj.buffer)
            tool_tip = var_obj.variable.get_tooltip()
        else:
            display_name = var_obj.variable.full_name
            var_key = var_obj.variable.name
            tool_tip = var_obj.variable.get_tooltip()

        default_value = 0.0
        session_key = f"{vartype}_var_{var_key}_{ss.ecosystem_type}"

        # Initialize session state if not exists
        if not ss.get(f'{vartype}_extraction_done', False):
            ss[session_key] = default_value

        # only update session state right after extraction is done
        if (ss.get(f'{vartype}_extraction_done', False) and
            ss.get(f'{vartype}_update_from_extraction', False) and
            var_key in ss.get(f'{vartype}_extracted_values', {})):

            try:
               ss[session_key] = float(ss[f'{vartype}_extracted_values'][var_key])
            except (ValueError, TypeError):
                pass

        value = st.number_input(
            f"{display_name}",
            step=0.01,
            format="%.2f",
            help=tool_tip if tool_tip else None,
            key=session_key
        )
        return value

    def _get_variable_values_from_gee(self, vartype='cost'):
        ss = st.session_state
        if vartype == 'cost':
            model = ss.model_class.COST_MODEL
        else:
            model = ss.model_class

        with st.spinner(f"Extracting values from Google Earth Engine..."):
            extracted_values, error = St_Utils.extract_values(model, ss.lat, ss.lon, ss.area)
            if error:
                st.error(f"Extraction failed: {error}")
            else:
                ss[f'{vartype}_extracted_values'] = extracted_values
                ss[f'{vartype}_extraction_done'] = True
                ss[f'{vartype}_update_from_extraction'] = True
                st.success(f"✅ Extracted {len(extracted_values)} variables")
                st.rerun()

    def ecosystem_services_menu(self):
        ss = st.session_state

        if ss.get('ecosystem_type', None) is not None:

            if hasattr(ss.model_class, 'ECOSYSTEM_SERVICES'):
                cols = st.columns(2)
                for i, var_obj in enumerate(ss.model_class.ECOSYSTEM_SERVICES):
                    with cols[i % 2]:
                        var_obj.value = self._ecosystem_service_button(var_obj)

            if hasattr(ss.model_class, 'SIIKAMAKI'):
                cols = st.columns(2)
                for i, var_obj in enumerate(ss.model_class.SIIKAMAKI):
                    with cols[i % 2]:
                        var_obj.value = self._ecosystem_service_button(var_obj)
        else:
            st.info("Please select a biome first")


    def _ecosystem_service_button(self, var_obj):
        ss = st.session_state
        current_value = getattr(var_obj, 'value', False)
        return st.checkbox(
            f"{var_obj.variable.full_name}",
            value=current_value,
            key=f"proj_{var_obj.variable.name}_{ss.ecosystem_type}",
            help=var_obj.variable.get_tooltip()
        )

    def display_benefits(self, predicted_sets, siikamaki_benefits=None):
        ss = st.session_state
        print(ss.ecosystem_type)
        if ss.get('ecosystem_type', None) is None:
            st.info("Please select a biome first")
            return
        else:
            tab_names = [t.variable.full_name for t in ss.model_class.VALUE_TYPES]

            tabs = st.tabs(tab_names)
            for i, (tab_name, tab) in enumerate(zip(tab_names, tabs)):
                with tab:
                    try:
                        self._benefit_type(predicted_sets, tab_name, siikamaki_benefits=siikamaki_benefits)
                    except TypeError:
                        st.info("Select ecosystem services and run calculation to display benefits.")

    def _benefit_type(self, predicted_sets, benefit_type, siikamaki_benefits=None):
        ss = st.session_state
        value_type = [vt for vt in ss.model_class.VALUE_TYPES if vt.variable.full_name == benefit_type][0]
        st.info(f"{value_type.variable.get_tooltip()}")
        cols = st.columns(2)
        predicted_values = predicted_sets[benefit_type]
        if siikamaki_benefits is not None:
            for benefit in siikamaki_benefits:
                predicted_values.update(benefit)
        total_value = 0.0
        for j, key in enumerate(predicted_values):
            with cols[j % 2]:
                st.metric(
                    label=key,
                    value=f"${predicted_values[key]:,.2f} per ha",
                    help="USD per hectare per year"
                )
            total_value += predicted_values[key]
        st.markdown(f"<h3 style='text-align: right;'>Total Value per ha: ${total_value:,.2f}</h3>",
                    unsafe_allow_html=True)

    def display_costs(self, cost_per_ha):

        for cost in cost_per_ha:
            try:
                k = [k for k, v in cost.items()][0]
                v = [v for k, v in cost.items()][0]
                st.metric(
                    label=k,
                    value = f"${v:,.2f} per ha",
                    help = "USD per hectare"
                )

            except TypeError:
                k = [k for k, v in cost.items()][0]
                st.metric(
                    label=k,
                    value=f"No cost data available for location"
                )

    @staticmethod
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

