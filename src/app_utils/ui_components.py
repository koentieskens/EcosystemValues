import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.models.benefit_models import (
    TropicalForest, TemparateForest, IntensiveLandUse,
    Mangroves, Grassland)
import streamlit as st
from src.app_utils.utils import St_Utils
from src.extract_data.predictions import Predictions
import base64
from src.app_utils.session_states import SessionStateManager as ssm
import pandas as pd


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
        'intensive_land_use': '🌽',
        'mangroves': '🌿',
        'grassland': '☘️'
    }

    def __init__(self):
        self.sidebar = Sidebar(self)

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
                    ssm.BENEFITS_UPDATED.reset()
                    ssm.BENEFITS_EXTRACTION_DONE.reset()
                    ssm.COST_EXTRACTED_VALUES.reset()
                    ssm.BENEFITS_EXTRACTED_VALUES.reset()
                    ssm.COST_EXTRACTION_DONE.reset()
                    ssm.COST_DATA.reset()
                    ssm.COST_UPDATED.reset()
                    ssm.DISPLAYED_COST.reset()
                    ssm.DISPLAYED_BENEFITS.reset()
                    ssm.COST_UPDATE_FROM_EXTRACTION.reset()
                    ssm.SIIKAMAKI_BENEFITS.reset()
                    ssm.PREDICTION_SETS.reset()
                    st.rerun()

        self._display_biome_selection()

    def _render_biome_button(self, key, display_name):
        """Returns True if button was clicked"""
        logo = self.BIOME_LOGOS.get(key, '🌱')
        is_selected = ssm.ECOSYSTEM_TYPE.get() == key
        return st.button(
            f"{logo}\n\n{display_name}",
            key=f"biome_select_{key}",
            type="primary" if is_selected else "secondary",
            use_container_width=True
        )

    def _update_session_state_with_biome(self, key):
        """Creates selection data without modifying internal state"""

        model_class = self.ECOSYSTEM_MODELS[key]
        ssm.ECOSYSTEM_TYPE.set(key)
        ssm.MODEL_CLASS.set(model_class())
        ssm.ECOSYSTEM_DISPLAY_NAME.set(self.ECOSYSTEM_DISPLAY_NAMES[key])
        ssm.BENEFITS_UPDATED.set(False)

    def _display_biome_selection(self):
        """Displays current selection status"""
        if ssm.ECOSYSTEM_TYPE.get() is not None:
            st.success(f"**Selected Ecosystem:** {ssm.ECOSYSTEM_DISPLAY_NAME.get()}")
        else:
            st.info("**Please select a biome above to continue**")

    def sub_biomes_menu(self):

        if hasattr(ssm.MODEL_CLASS.get(), 'SUB_BIOMES') and ssm.MODEL_CLASS.get().SUB_BIOMES:

            selected_option = self._sub_biome_button()

            # Set only the selected one to True
            for var_obj in ssm.MODEL_CLASS.get().SUB_BIOMES:
                if var_obj.variable.full_name == selected_option:
                    var_obj.value = 1
                else:
                    var_obj.value = 0
        else:
            st.info("No sub-biomes available for this ecosystem type.")

    def _sub_biome_button(self):

        return st.radio(
            "Select Sub-biome:",
            options=[var_obj.variable.full_name for var_obj in ssm.MODEL_CLASS.get().SUB_BIOMES],  # Display names
            key=f"sub_biome_{ssm.ECOSYSTEM_TYPE.get()}",
            help="Choose the sub-biome that best describes your study area"
        )

    def spatial_variables_menu(self, vartype='cost'):
        if hasattr(ssm.MODEL_CLASS.get(), 'VARIABLES'):

            if vartype == 'cost':
                model = ssm.MODEL_CLASS.get().COST_MODEL
            else:
                model = ssm.MODEL_CLASS.get()

            if hasattr(model, 'VARIABLES'):
                GROUP_ORDER = ['Biodiversity', 'Landscape', 'Climate', 'Socio-economic', 'Other']

                groups = {}
                for var_obj in model.VARIABLES:
                    g = getattr(var_obj, 'group', None) or 'Other'
                    groups.setdefault(g, []).append(var_obj)

                for group_name in GROUP_ORDER:
                    if group_name not in groups:
                        continue
                    st.markdown(f"**{group_name}**")
                    for var_obj in groups[group_name]:
                        var_obj.value = self._spatial_variable_field(var_obj, vartype=vartype)

                if st.button("Extract Spatial Values from GEE", type="primary",
                             use_container_width=True,
                             key=f'{vartype}_gee'):
                    self._get_variable_values_from_gee(vartype=vartype)


                if vartype == 'cost':
                # this is to make sure that manual edits are not automatically overwritten
                    if ssm.COST_UPDATE_FROM_EXTRACTION.get():
                        ssm.COST_UPDATE_FROM_EXTRACTION.set(False)

                if vartype == 'benefit':
                # this is to make sure that manual edits are not automatically overwritten
                    if ssm.BENEFITS_UPDATE_FROM_EXTRACTION.get():
                        ssm.BENEFITS_UPDATE_FROM_EXTRACTION.set(False)
            else:
                st.info("No spatial variables needed for this biome.")
        else:
            st.info("Please select a biome first")

    def _spatial_variable_field(self, var_obj, vartype='cost'):


        if var_obj.lc is not None:
            display_name = var_obj.lc.full_name
            var_key = var_obj.lc.get_name(var_obj.buffer)
            tool_tip = var_obj.variable.get_tooltip()
        else:
            display_name = var_obj.variable.full_name
            var_key = var_obj.variable.name
            tool_tip = var_obj.variable.get_tooltip()

        default_value = 0.0
        session_key = f"{vartype}_var_{var_key}_{ssm.ECOSYSTEM_TYPE.get()}"

        # Initialize session state if not exists
        if vartype == 'cost':
            if not ssm.COST_EXTRACTION_DONE.get():
                st.session_state[session_key] = default_value

            # only update session state right after extraction is done
            if (
                    ssm.COST_EXTRACTION_DONE.get() and
                    ssm.COST_UPDATE_FROM_EXTRACTION.get() and
                    var_key in ssm.COST_EXTRACTED_VALUES.get()
            ):

                try:
                    st.session_state[session_key] = float(ssm.COST_EXTRACTED_VALUES.get()[var_key])
                except (ValueError, TypeError):
                    pass

        if vartype == 'benefit':
            if not ssm.BENEFITS_EXTRACTION_DONE.get():
                st.session_state[session_key] = default_value

            # only update session state right after extraction is done
            if (
                    ssm.BENEFITS_EXTRACTION_DONE.get() and
                    ssm.BENEFITS_UPDATE_FROM_EXTRACTION.get() and
                    var_key in ssm.BENEFITS_EXTRACTED_VALUES.get()
            ):

                try:
                    st.session_state[session_key] = float(ssm.BENEFITS_EXTRACTED_VALUES.get()[var_key])
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
        if vartype == 'cost':
            model = ssm.MODEL_CLASS.get().COST_MODEL
        else:
            model = ssm.MODEL_CLASS.get()

        lat = ssm.PROJECT_LOCATION.get()['lat']
        lon = ssm.PROJECT_LOCATION.get()['lon']
        area = ssm.PROJECT_LOCATION.get()['area']
        area_m2 = area * 10000
        radius = int(math.sqrt(area_m2 / math.pi))

        variables = model.VARIABLES
        n = len(variables)

        progress_bar = st.progress(0, text="Starting extraction...")
        try:
            p = Predictions(variables, lat, lon, radius=radius)
            for i, variable in enumerate(variables):
                display_name = variable.variable.full_name
                progress_bar.progress((i + 1) / n, text=f"Extracting: {display_name}")
                d = p.get_value(variable, lat, lon, radius=radius)
                p.values_dict.update(d)

            progress_bar.progress(1.0, text="Extraction complete")
            extracted_values = p.values_dict

            if vartype == 'cost':
                ssm.COST_EXTRACTED_VALUES.set(extracted_values)
                ssm.COST_EXTRACTION_DONE.set(True)
                ssm.COST_UPDATE_FROM_EXTRACTION.set(True)
            if vartype == 'benefit':
                ssm.BENEFITS_EXTRACTED_VALUES.set(extracted_values)
                ssm.BENEFITS_EXTRACTION_DONE.set(True)
                ssm.BENEFITS_UPDATE_FROM_EXTRACTION.set(True)
            st.rerun()

        except Exception as e:
            progress_bar.empty()
            st.error(f"Extraction failed: {e}")


    def ecosystem_services_menu(self):


        if ssm.ECOSYSTEM_TYPE.get() is not None:

            if hasattr(ssm.MODEL_CLASS.get(), 'ECOSYSTEM_SERVICES'):
                cols = st.columns(2)
                for i, var_obj in enumerate(ssm.MODEL_CLASS.get().ECOSYSTEM_SERVICES):
                    with cols[i % 2]:
                        var_obj.value = self._ecosystem_service_button(var_obj)

            if hasattr(ssm.MODEL_CLASS.get(), 'SIIKAMAKI'):
                cols = st.columns(2)
                for i, var_obj in enumerate(ssm.MODEL_CLASS.get().SIIKAMAKI):
                    with cols[i % 2]:
                        var_obj.value = self._ecosystem_service_button(var_obj)
        else:
            st.info("Please select a biome first")

    def _ecosystem_service_button(self, var_obj):

        current_value = getattr(var_obj, 'value', False)
        return st.checkbox(
            f"{var_obj.variable.full_name}",
            value=current_value,
            key=f"proj_{var_obj.variable.name}_{ssm.ECOSYSTEM_TYPE.get()}",
            help=var_obj.variable.get_tooltip()
        )

    @ssm.BENEFITS_UPDATED.skip_if_false()
    def display_benefits(self, predicted_sets, siikamaki_benefits=None):

        if ssm.ECOSYSTEM_TYPE.get() is None:
            st.info("Please select a biome first")
            return
        else:
            tab_names = [t.variable.full_name for t in ssm.MODEL_CLASS.get().VALUE_TYPES]

            tabs = st.tabs(tab_names)
            for i, (tab_name, tab) in enumerate(zip(tab_names, tabs)):
                with tab:
                    try:
                        self._benefit_type(predicted_sets, tab_name, siikamaki_benefits=siikamaki_benefits)
                        ssm.BENEFITS_UPDATED.set(True)
                    except TypeError as e:
                        st.info("Select ecosystem services and run calculation to display benefits.")
            ssm.DISPLAYED_BENEFITS.set(True)

    def _benefit_type(self, predicted_sets, benefit_type, siikamaki_benefits=None):

        value_type = [vt for vt in ssm.MODEL_CLASS.get().VALUE_TYPES if vt.variable.full_name == benefit_type][0]
        st.info(f"{value_type.variable.get_tooltip()}")

        predicted_values = predicted_sets[benefit_type]
        if siikamaki_benefits is not None:
            for benefit in siikamaki_benefits:
                full_name = next(iter(benefit))
                print(full_name)
                siikamaki_list = ssm.MODEL_CLASS.get().SIIKAMAKI
                item = next((item for item in siikamaki_list if item.variable.full_name == full_name), None)

                if item.benefit_type == benefit_type:
                    predicted_values.update(benefit)

        rows = [{"Ecosystem Service": k, "Value (USD/ha/yr)": v} for k, v in predicted_values.items()]
        total_value = sum(predicted_values.values())
        rows.append({"Ecosystem Service": "Total", "Value (USD/ha/yr)": total_value})

        df = pd.DataFrame(rows)

        def bold_last_row(row):
            return ["font-weight: bold" if row.name == len(df) - 1 else "" for _ in row]

        styled = (
            df.style
            .format({"Value (USD/ha/yr)": "${:,.2f}"})
            .apply(bold_last_row, axis=1)
        )
        st.dataframe(styled, width='stretch', hide_index=True)


    def cost_variables_menu(self):

        if ssm.ECOSYSTEM_TYPE.get() is None:
            st.info("Please select a biome first")
            return
        else:
            if hasattr(ssm.MODEL_CLASS.get().COST_MODEL, 'GLOBAL_LAYERS'):
                cols = st.columns(2)
                for i, pvar_obj in enumerate(ssm.MODEL_CLASS.get().COST_MODEL.GLOBAL_LAYERS):
                    display_name = pvar_obj.variable.full_name
                    var_key = pvar_obj.variable.name

                    with cols[i % 2]:
                        pvar_obj.value = st.checkbox(
                            display_name,
                            key=f"cost_{var_key}_{ssm.ECOSYSTEM_TYPE.get()}",
                            help=pvar_obj.variable.get_tooltip()
                        )

            elif hasattr(ssm.MODEL_CLASS.get().COST_MODEL, 'NBS'):
                cols = st.columns(2)
                for i, pvar_obj in enumerate(ssm.MODEL_CLASS.get().COST_MODEL.NBS):
                    display_name = pvar_obj.variable.full_name
                    var_key = pvar_obj.variable.name
                    with cols[i % 2]:
                        pvar_obj.value = st.checkbox(
                            display_name,
                            key=f"cost_{var_key}_{ssm.ECOSYSTEM_TYPE.get()}",
                            help=pvar_obj.variable.description
                        )
            elif ssm.MODEL_CLASS.get().COST_MODEL is None:
                st.info("Cost model for this biome is unavailable")
            else:
                st.info("Please select a biome first")

    def display_costs(self, cost_per_ha):

        rows = []
        for cost in cost_per_ha:
            k = list(cost.keys())[0]
            v = list(cost.values())[0]
            try:
                rows.append({"Intervention": k, "Cost (USD/ha/yr)": float(v)})
            except (TypeError, ValueError):
                rows.append({"Intervention": k, "Cost (USD/ha/yr)": None})

        if rows:
            total_value = sum(r["Cost (USD/ha/yr)"] for r in rows if r["Cost (USD/ha/yr)"] is not None)
            rows.append({"Intervention": "Total", "Cost (USD/ha/yr)": total_value})

            df = pd.DataFrame(rows)

            def bold_last_row(row):
                return ["font-weight: bold" if row.name == len(df) - 1 else "" for _ in row]

            styled = (
                df.style
                .format({"Cost (USD/ha/yr)": lambda v: f"${v:,.2f}" if v is not None else "No data available"})
                .apply(bold_last_row, axis=1)
            )
            st.dataframe(styled, width='stretch', hide_index=True)

        ssm.COST_UPDATED.set(True)

    @staticmethod
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()


class Sidebar:

    def __init__(self, parent_renderer):
        self.parent = parent_renderer

    def create_sidebar(self):
        """Main method to create the complete sidebar"""
        with st.sidebar:
            self.title_and_about()
            st.markdown("---")

            self.location_info()
            st.markdown("---")

            self.progress_tracker()
            st.markdown("---")

            self.download_csv_button()
            st.markdown("---")

            self.website_image_link()

    def title_and_about(self):
        """Title and about information section"""
        st.title("NBS Valuation Tool")

        with st.expander("ℹ️ About this tool"):
            st.markdown("""
            The tool is an interactive application that produces site-specific estimates of restoration costs and
            ecosystem service values. Users define a project location and basic characteristics (such as biome, area,
            and the type of estimate needed). The tool then selects the most appropriate underlying model or mapped
            dataset and returns an estimated cost and/or benefit for that project. In practice, the tool supports
            early-stage decision-making, especially when teams need consistent, transparent numbers quickly.

            **How to use:**
            1. Select a biome type
            2. Define the project area
            3. Extract spatial variables
            4. Choose ecosystem services and calculate estimated benefits
            5. Choose intervention types and calculate estimated costs
            6. Download results in CSV format
            """)

    def location_info(self):
        """Display current location information"""
        st.subheader("Location")

        if ssm.LOCATION_ACTIVATED.get() and ssm.PROJECT_LOCATION.get():
            location = ssm.PROJECT_LOCATION.get()
            country = ssm.SAVED_COUNTRY.get()
            region = ssm.SAVED_REGION.get() or '-   '

            # Get location name if available
            if ssm.POLYGON_CENTROID.get():
                lat = ssm.POLYGON_CENTROID.get()[0]
                lon = ssm.POLYGON_CENTROID.get()[1]
            else:
                lat = location['lat']
                lon = location['lon']

            area = location['area']
            biome = ssm.ECOSYSTEM_DISPLAY_NAME.get() or 'Not selected'

            # Display compact location info
            st.markdown(f"""
                    **Country:** {country}  
                    **Region:** {region}  
                    **Latitude:** {lat:.4f}  
                    **Longitude:** {lon:.4f}  
                    **Area:** {area:,.2f} ha  
                    **Biome:** {biome}
                    """)


        else:
            st.info("No location set")
            st.caption("Set location in main interface")

    def progress_tracker(self):
        """Track progress flags and display status"""
        st.subheader("Progress Tracker")

        counter = 0
        # Location status
        location_status = "✅" if ssm.LOCATION_ACTIVATED.get() else "⏳"
        st.write(f"{location_status} **Location Set**")
        counter += 1

        benefit_extracted = "✅" if ssm.BENEFITS_EXTRACTION_DONE.get() else "⏳"
        st.write(f"{benefit_extracted} **Benefit Variables Extracted**")
        counter += 1

        # Variables extracted status
        if ssm.MODEL_CLASS.get() is not None:
            if hasattr(ssm.MODEL_CLASS.get().COST_MODEL, 'VARIABLES'):
                cost_extracted = "✅" if ssm.COST_EXTRACTION_DONE.get() else "⏳"
                st.write(f"{cost_extracted} **Cost Variables Extracted**")
                counter += 1


        # Benefits calculated status
        benefits_status = "✅" if ssm.BENEFITS_UPDATED.get() else "⏳"
        st.write(f"{benefits_status} **Benefits Calculated**")
        counter += 1

        # Costs calculated status (assuming you have a similar flag)
        costs_status = "✅" if ssm.COST_UPDATED.get() else "⏳"
        st.write(f"{costs_status} **Costs Calculated**")
        counter += 1

        # Overall completion
        total_steps = counter
        completed_steps = sum([
            1 if ssm.LOCATION_ACTIVATED.get() else 0,
            1 if ssm.COST_EXTRACTION_DONE.get() else 0,
            1 if ssm.BENEFITS_EXTRACTION_DONE.get() else 0,
            1 if ssm.BENEFITS_UPDATED.get() else 0,
            1 if ssm.COST_UPDATED.get() else 0
        ])

        progress_percent = (completed_steps / total_steps) * 100
        st.progress(progress_percent / 100)
        st.caption(f"Progress: {completed_steps}/{total_steps} steps complete")

    def download_csv_button(self):
        """Download CSV with variables, benefits, and costs"""
        st.subheader("Export Results")

        # Check if we have enough data to export
        has_location = ssm.LOCATION_ACTIVATED.get()
        has_variables = (ssm.COST_EXTRACTION_DONE.get() or
                         ssm.BENEFITS_EXTRACTION_DONE.get())
        has_calculations = ssm.BENEFITS_UPDATED.get()

        if has_location and has_variables and has_calculations:
            if st.button("Download CSV",
                         use_container_width=True,
                         type="primary"):
                csv_data = self._generate_csv_data()

                # Create download
                st.download_button(
                    label="⬇️ Download Results.csv",
                    data=csv_data,
                    file_name=f"ecosystem_benefits_{ssm.ECOSYSTEM_TYPE.get()}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime='text/csv',
                    use_container_width=True
                )
        else:
            st.info("Complete analysis to download results")
            if not has_location:
                st.caption("• Set location first")
            if not has_variables:
                st.caption("• Extract variables")
            if not has_calculations:
                st.caption("• Calculate benefits")

    def website_image_link(self):
        """Display image with link to website"""


        # You'll need to specify the actual image path and website URL
        image_path = "src/images/NBS.PNG"    # Adjust path as needed
        website_url = "https://www.naturebasedsolutions.org"  # Replace with actual URL

        try:
            # Display image with link
            image_base64 = self.parent.get_base64_image(image_path)
            st.markdown(
                f"""
                <a href="{website_url}" target="_blank">
                    <img src="data:image/png;base64,{image_base64}" 
                         style="width: 100%; max-width: 200px; border-radius: 10px;">
                </a>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <a href="https://github.com/koentieskens/EcosystemValues" target="_blank"
                   style="display:inline-flex; align-items:center; gap:8px; padding:8px 14px;
                          background:#006d77; color:white; border-radius:6px;
                          text-decoration:none; font-size:14px; margin-top:10px;">
                    <svg height="18" width="18" viewBox="0 0 16 16" fill="white">
                      <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38
                               0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13
                               -.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66
                               .07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15
                               -.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27
                               .68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12
                               .51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48
                               0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                    </svg>
                    GitHub Repository
                </a>
                """,
                unsafe_allow_html=True
            )

        except FileNotFoundError:
            # Fallback if image not found
            st.markdown(
                f"""
                🌱 **Ecosystem Benefits Calculator**

                [🌐 Visit our website]({website_url})
                """,
                unsafe_allow_html=True
            )

    def _generate_csv_data(self):
        """Generate CSV data combining variables, benefits, and costs"""
        import pandas as pd
        import io

        data_rows = []

        # Add location info
        if ssm.PROJECT_LOCATION.get():
            location = ssm.PROJECT_LOCATION.get()
            data_rows.append({
                'Category': 'Location',
                'Variable': 'Latitude',
                'Description': 'Latitude for project location',
                'Value': ssm.POLYGON_CENTROID.get()[0] if ssm.POLYGON_CENTROID.get() else location['lat'],
                'Unit': 'degrees',
                'Source': 'User input'
            })
            data_rows.append({
                'Category': 'Location',
                'Variable': 'Longitude',
                'Description': 'Longitude for project location',
                'Value': ssm.POLYGON_CENTROID.get()[1] if ssm.POLYGON_CENTROID.get() else location['lon'],
                'Unit': 'degrees',
                'Source': 'User input'
            })
            data_rows.append({
                'Category': 'Location',
                'Variable': 'Area',
                'Description': 'Area size for project',
                'Value': location['area'],
                'Unit': 'hectares',
                'Source': 'User input'
            })
            data_rows.append({
                'Category': 'Location',
                'Variable': 'Biome',
                'Description': 'Biome type selected',
                'Value': ssm.ECOSYSTEM_DISPLAY_NAME.get(),
                'Unit': 'type',
                'Source': 'User input'
            })

        # Add extracted variables
        if ssm.COST_EXTRACTED_VALUES.get():
            for var_obj in ssm.MODEL_CLASS.get().COST_MODEL.VARIABLES:
                data_rows.append({
                    'Category': 'Cost Variables',
                    'Variable': var_obj.name,
                    'Description': var_obj.description,
                    'Value': var_obj.value,
                    'Unit': var_obj.variable.unit,
                    'Source': var_obj.variable.source
                })

        if ssm.BENEFITS_EXTRACTED_VALUES.get():
            for var_obj in ssm.MODEL_CLASS.get().VARIABLES:
                data_rows.append({
                    'Category': 'Benefit Variables',
                    'Variable': var_obj.name,
                    'Description': var_obj.description,
                    'Value': var_obj.value,
                    'Unit': var_obj.variable.unit,
                    'Source': var_obj.variable.source
                })

        # Add calculated benefit values
        if ssm.PREDICTION_SETS.get() and ssm.BENEFITS_UPDATED.get():
            variables = ssm.MODEL_CLASS.get().ECOSYSTEM_SERVICES
            for var_obj in variables:
                data_rows.append({
                    'Category': 'Benefit - Consumer Surplus',
                    'Variable': var_obj.name,
                    'Description': var_obj.description,
                    'Value': var_obj.cons_surplus,
                    'Unit': var_obj.variable.unit,
                    'Source': var_obj.variable.data_source
                })
        if ssm.SIIKAMAKI_BENEFITS.get() and ssm.BENEFITS_UPDATED.get():
            variables = ssm.MODEL_CLASS.get().SIIKAMAKI
            for var_obj in variables:
                data_rows.append({
                    'Category': 'Benefit - Consumer Surplus',
                    'Variable': var_obj.variable.full_name,
                    'Description': var_obj.variable.description,
                    'Value': var_obj.cons_surplus,
                    'Unit': var_obj.variable.unit,
                    'Source': var_obj.variable.source
                })
        if ssm.PREDICTION_SETS.get() and ssm.BENEFITS_UPDATED.get():
            variables = ssm.MODEL_CLASS.get().ECOSYSTEM_SERVICES
            for var_obj in variables:
                data_rows.append({
                    'Category': 'Benefit - Exchange Value',
                    'Variable': var_obj.name,
                    'Description': var_obj.description,
                    'Value': var_obj.exchange_value,
                    'Unit': var_obj.variable.unit,
                    'Source': var_obj.variable.data_source
                })

        if ssm.SIIKAMAKI_BENEFITS.get() and ssm.BENEFITS_UPDATED.get():
           variables = ssm.MODEL_CLASS.get().SIIKAMAKI
           for var_obj in variables:
               data_rows.append({
                   'Category': 'Benefit - Exchange Value',
                   'Variable': var_obj.variable.full_name,
                   'Description': var_obj.variable.description,
                   'Value': var_obj.exchange_value,
                   'Unit': var_obj.variable.unit,
                   'Source': var_obj.variable.source
               })

        if ssm.COST_DATA.get():
            if hasattr(ssm.MODEL_CLASS.get().COST_MODEL, 'GLOBAL_LAYERS'):
                for layer in ssm.MODEL_CLASS.get().COST_MODEL.GLOBAL_LAYERS:
                        data_rows.append({
                            'Category': 'Costs',
                            'Variable': layer.variable.full_name,
                            'Description': layer.variable.description,
                            'Unit': 'USD per hectare per year',
                            'Value': layer.cost_value,
                            'Source': layer.variable.source
                        })
            if hasattr(ssm.MODEL_CLASS.get().COST_MODEL, 'NBS'):
                source = None
                value = None
                for layer in ssm.MODEL_CLASS.get().COST_MODEL.NBS:

                    if layer.value:
                        data_rows.append({
                            'Category': 'Costs',
                            'Variable': layer.variable.full_name,
                            'Description': layer.variable.description,
                            'Unit': 'USD per hectare per year',
                            'Source': layer.variable.data_source,
                        })
                        source = layer.variable.data_source
                        value = layer.cost_value

                data_rows.append({
                    'Category': 'Costs',
                    'Variable': 'Total Cost',
                    'Description': 'Total cost for the selected NBS techniques',
                    'Unit': 'USD per hectare per year',
                    'Source': source,
                    'Value': value
                })
        # Create DataFrame and convert to CSV
        df = pd.DataFrame(data_rows)

        # Convert to CSV string
        output = io.StringIO()
        df.to_csv(output, index=False)
        return output.getvalue()




