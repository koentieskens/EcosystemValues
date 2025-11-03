import streamlit as st
import ee
import sys
import os

# Add the project root to the path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.app_utils.utils import St_Utils
from src.models.benefit_models import (
    TropicalForest, TemparateForest, IntensiveLandUse,
    Mangroves, Grassland
)

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


def main():
    try:
        st.set_page_config(
            page_title="Ecosystem Valuation Tool",
            page_icon="🌱",
            layout="wide"
        )
    except:
        pass  # Ignore if not supported in older Streamlit versions

    st.title("🌱 Ecosystem Valuation Tool")
    st.markdown("---")

    # Initialize session state
    if 'extracted_values' not in st.session_state:
        st.session_state.extracted_values = {}
    if 'extraction_done' not in st.session_state:
        st.session_state.extraction_done = False

    # Introduction
    st.markdown("""
    **Welcome to the Ecosystem Valuation Tool**

    This application estimated the annual value of ecosystem services across different 
    ecosystems based on value transfer functions. You can assess the total value 
     of various ecosystem services for your specific project location, based on spatial environmental 
     variables and selected project variables.
    """)

    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")

        # Google Earth Engine Project
        st.subheader("Google Earth Engine Authorization")
        gee_project = st.text_input(
            "Project ID",
            placeholder="your-gee-project-id",
            help="Enter your Google Earth Engine project ID"
        )

        if st.button("Initialize GEE"):
            if not gee_project:
                st.error("Please enter your GEE project ID")
            else:
                try:
                    ee.Authenticate(force=True)
                    ee.Initialize(project=gee_project)
                    st.success(f"✅ Connected to GEE project: {gee_project}")
                    st.session_state.gee_initialized = True
                except Exception as e:
                    st.error(f"❌ Failed to initialize GEE: {str(e)}")
                    st.session_state.gee_initialized = False

        st.markdown("---")

        # Ecosystem Type Selection
        st.subheader("Ecosystem Type")
        ecosystem_type = st.selectbox(
            "Select ecosystem type:",
            options=list(ECOSYSTEM_DISPLAY_NAMES.keys()),
            format_func=lambda x: ECOSYSTEM_DISPLAY_NAMES[x],
            help="Choose the ecosystem type that best describes your study area"
        )

    # Main content area
    if ecosystem_type:
        model_class = ECOSYSTEM_MODELS[ecosystem_type]
        ecosystem_display_name = ECOSYSTEM_DISPLAY_NAMES[ecosystem_type]



        # Basic Parameters
        st.markdown("### Basic Project Parameters")
        col1, col2, col3 = st.columns(3)

        with col1:
            latitude = st.number_input(
                "Latitude",
                min_value=-90.0,
                max_value=90.0,
                value=0.0,
                step=0.01,
                format="%.6f"
            )

        with col2:
            longitude = st.number_input(
                "Longitude",
                min_value=-180.0,
                max_value=180.0,
                value=0.0,
                step=0.01,
                format="%.6f"
            )

        with col3:
            area_hectares = st.number_input(
                "Project Area (hectares)",
                min_value=1,
                value=100,
                step=1,
                format="%d"
            )
        # Get location information based on coordinates
        county, country = St_Utils.get_location_info(latitude, longitude)

        # Display location information
        location_text = ""
        if county and country:
            location_text = f" | Location: {county}, {country}"
        elif country:
            location_text = f" | Location: {country}"

        st.subheader(f"Analysis for: {ecosystem_display_name}{location_text}")

        # Optionally show coordinates
        if latitude != 0.0 or longitude != 0.0:
            st.caption(f"Coordinates: {latitude:.6f}, {longitude:.6f}")

        st.markdown("---")

        col4, col5,  = st.columns(2)
        # Project Variables Section
        with col4:
            st.markdown("### Project Variables")
            st.markdown("Select which ecosystem services apply to your project:")

            project_variables = {}

            # Create columns for better layout
            cols = st.columns(2)
            for i, pvar_obj in enumerate(model_class.PROJECT_VARIABLES):
                display_name = St_Utils.get_project_variable_display_info(pvar_obj)

                var_key = pvar_obj.variable.name

                with cols[i % 2]:
                    project_variables[var_key] = st.checkbox(
                        display_name,
                        key=f"proj_{var_key}_{ecosystem_type}"
                    )
        with col5:

            # Model Variables Section
            st.markdown("### Spatial Variables")

            # Model variables inputs
            float_variables = {}
            cols = st.columns(2)
            for i, var_obj in enumerate(model_class.VARIABLES):
                display_name, tooltip = St_Utils.get_variable_display_info(var_obj)

                # Get the form field key
                if hasattr(var_obj, 'lc') and var_obj.lc is not None:
                    buffer = var_obj.var.buffer if var_obj.var.buffer else 0
                    var_key = var_obj.lc.get_name(buffer=buffer)
                else:
                    var_key = var_obj.var.name

                # Get default value from extracted values if available
                default_value = 0.0
                if var_key in st.session_state.extracted_values:
                    try:
                        default_value = float(st.session_state.extracted_values[var_key])
                    except (ValueError, TypeError):
                        default_value = 0.0

                # Create input field with session state key for persistence
                session_key = f"var_{var_key}_{ecosystem_type}"

                # Initialize session state if not exists
                if session_key not in st.session_state:
                    st.session_state[session_key] = default_value

                # If we just extracted values, update the session state
                if st.session_state.extraction_done and var_key in st.session_state.extracted_values:
                    try:
                        st.session_state[session_key] = float(st.session_state.extracted_values[var_key])
                    except (ValueError, TypeError):
                        pass
                with cols[i % 2]:
                    float_variables[var_key] = st.number_input(
                        f"{display_name}",
                        value=st.session_state[session_key],
                        step=0.01,
                        format="%.2f",
                        help=tooltip if tooltip else None,
                        key=session_key
                    )

            if st.button("🔄 Extract Spatial Values from GEE", type="primary",
                         use_container_width=True):
                if not st.session_state.get('gee_initialized', 0):
                    st.error("Please initialize Google Earth Engine first")
                else:
                    with st.spinner("Extracting values from Google Earth Engine..."):
                        extracted_values, error = St_Utils.extract_values(model_class, latitude, longitude, area_hectares)

                        if error:
                            st.error(f"Extraction failed: {error}")
                        else:
                            # Store extracted values in session state
                            st.session_state.extracted_values = extracted_values
                            st.session_state.extraction_done = True
                            st.success(f"✅ Extracted {len(extracted_values)} variables")
                            st.rerun()  # Rerun to update the input fields

            # Show extraction status
            if st.session_state.extraction_done and st.session_state.extracted_values:
                st.info(f"✅ Using extracted values from GEE ({len(st.session_state.extracted_values)} variables)")

        st.markdown("---")


        # Calculate Value Button
        st.markdown("### 💰 Calculate Ecosystem Value")

        if st.button("Calculate Value", type="primary", use_container_width=True):
            # Validate inputs
            if not all([latitude != 0 or longitude != 0, area_hectares > 0]):
                st.error("Please provide valid latitude, longitude, and area values")
            elif not any(float_variables.values()):
                st.error("Please provide values for the model variables (use 'Extract Values' or enter manually)")
            else:
                # Calculate ecosystem value
                value_per_ha, error = St_Utils.calculate_ecosystem_value(
                    model_class, float_variables, project_variables, area_hectares
                )

                if error:
                    st.error(f"Calculation failed: {error}")
                else:
                    total_value = value_per_ha * area_hectares

                    # Display results
                    st.success("✅ Calculation Complete!")

                    # Create results display
                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            label="Value per hectare per annum",
                            value=f"${value_per_ha:,.2f}",
                            help="USD per hectare per year"
                        )

                    with col2:
                        st.metric(
                            label="Total annual value",
                            value=f"${total_value:,.2f}",
                            help="Total USD per year for the entire project area"
                        )

                    # Additional info
                    st.info(f"""
                    **Project Summary:**
                    - Ecosystem Type: {ecosystem_display_name}
                    - Location: ({latitude}, {longitude})
                    - Project Area: {area_hectares:,.0f} hectares

                    This value represents the annual flow of ecosystem services benefits for the specified project area.
                    """)

        # Display current inputs summary
        with st.expander("Current Inputs Summary"):
            st.write("**Basic Parameters:**")
            st.write(f"- Location: ({latitude}, {longitude})")
            st.write(f"- Area: {area_hectares} hectares")

            st.write("**Model Variables:**")
            for key, value in float_variables.items():
                st.write(f"- {key.replace('_', ' ').title()}: {value}")

            st.write("**Selected Project Variables:**")
            selected_vars = [key.replace('_', ' ').title() for key, value in project_variables.items() if value]
            if selected_vars:
                for var in selected_vars:
                    st.write(f"- {var}")
            else:
                st.write("- None selected")

        # Clear extracted values button
        if st.session_state.extraction_done:
            st.markdown("---")
            if st.button("🗑️ Clear Extracted Values", type="secondary"):
                st.session_state.extracted_values = {}
                st.session_state.extraction_done = False
                st.rerun()


if __name__ == "__main__":
    main()