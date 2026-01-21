import streamlit as st
from src.app_utils.css import CSS
from src.app_utils.calculation_engine import CalculationEngine
from src.app_utils.locations_components import LocationManager
from src.app_utils.gcp_authenticate import ConnectToGoogle
from src.app_utils.ui_components import UIRenderer
from src.app_utils.session_states import SessionStateManager as ssm


@st.cache_resource
def get_google_connection():
    gcs = ConnectToGoogle()
    gcs.connect_to_google()
    return gcs

class EcoApp:

    def __init__(self):
        self.locman = LocationManager()
        self.ui = UIRenderer()
        self.ui.sidebar.create_sidebar()
        self.calculator = CalculationEngine()


    @ssm.INIT_DONE.skip_if_true()
    def initialize(self):
        try:
            ssm.initialize_all()
            self.gcs = get_google_connection()
            st.markdown(CSS.GOOGLE_FONT, unsafe_allow_html=True)

            ssm.INIT_DONE.set(True)
        except Exception as e:
            st.error(f"Initialization failed: {e}")
            st.stop()


    def welcome(self):
        with st.container(key='welcome'):

            col1, col2 = st.columns([2, 1])
            with col1:
                st.title("Ecosystem Valuation Tool")

            with col2:
                img_base64 = self.ui.get_base64_image("src/images/NBS_GFDRR_Admin_WBG_2.avif")
                st.markdown("""
                    <style>
                    .bottom-align {
                        display: flex;
                        align-items: flex-end;
                        height: 100%;
                    }
                    </style>
                    """, unsafe_allow_html=True)

                st.markdown('<div class="bottom-align">', unsafe_allow_html=True)
                st.markdown(f"""
                    <a href="https://www.naturebasedsolutions.org/" target="_blank">
                        <img src="data:image/avif;base64,{img_base64}" width="1000" alt="Logo">
                    </a>
                    """, unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("---")


    def set_css(self):
        st.markdown(f"<style>{CSS.WELCOME}</style>", unsafe_allow_html=True)
        st.markdown(f"<style>{CSS.LOCATION}</style>", unsafe_allow_html=True)
        st.markdown(f"<style>{CSS.SPATIAL_VARIABLES}</style>", unsafe_allow_html=True)
        st.markdown(f"<style>{CSS.BENEFIT}</style>", unsafe_allow_html=True)
        st.markdown(f"<style>{CSS.COST}</style>", unsafe_allow_html=True)
        st.markdown(f"<style>{CSS.ESS}</style>", unsafe_allow_html=True)
        st.markdown(CSS.TAB_LAYOUT, unsafe_allow_html=True)
        st.markdown(CSS.HIDE_ANCHOR_CSS, unsafe_allow_html=True)

    def biomes(self):
        with st.container(key='ess'):
            st.header('Select Biome')
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader('Biome selection')
                st.markdown("""
                NBS costs and benefits are estimated based on biome specific value transfer functions.
                To make sure you get the most accurate estimation for your study area, please select the biome that best
                represents your study area.""")
                st.markdown(CSS.BIOME_SELECTION_BOX, unsafe_allow_html=True)
                self.ui.biome_selection_boxes()

            with col2:
                st.subheader('Sub Category')
                st.markdown("""
                Please select the relevant sub biome below
                """)
                self.ui.sub_biomes_menu()

        st.markdown("")

    def location(self):
        col_loc, col_values = st.columns([2, 1])

        # create the tab layout
        with col_loc:
            with st.container(key='location'):
                st.header('Project Location')
                col_params_pol, col_map_pol = st.columns([1, 2])
                with col_params_pol:

                    self.locman.polygon_info()
                    self.locman.location_info()
                with col_map_pol:
                    if self.locman.should_update_map():
                        st.session_state.cached_map = self.locman.draw_map()

        with col_values:
            with st.container(key='spatial_variables'):
                st.header('Spatial Predictor Variables')
                tab_benefit, tab_cost = st.tabs(["Benefit", "Cost"])
                with tab_benefit:
                    self.ui.spatial_variables_menu(vartype='benefit')
                with tab_cost:
                    self.ui.spatial_variables_menu(vartype='cost')

        st.markdown("")

    def benefits(self):

        with st.container(key='benefits'):
            st.header('Ecosystem Benefits')
            st.markdown("---")
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("Ecosystem Services")
                st.markdown("""
                Select which ecosystem services you want to include in the benefit assessment.
                """)
                self.ui.ecosystem_services_menu()
                self.calculator.calculate_benefit()
            with col2:
                st.subheader("Benefit Estimates")
                st.markdown("""
                Benefits are expressed in Current USD per hectare per year. Estimations were done using meta regressions
                based on es-valuation studies using ESVD data (Brander et al., 2025) and a recent meta regression model
                for forest ecosystem services (Siikamaki et al., 2024)
                """)
                prediction_sets = ssm.PREDICTION_SETS.get()
                siikamaki_benefits = ssm.SIIKAMAKI_BENEFITS.get()
                self.ui.display_benefits(prediction_sets, siikamaki_benefits)

    def costs(self):

        with st.container(key='costs'):
            st.header('Intervention Costs')
            st.markdown("---")
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("Type of Intervention")

                st.markdown("""Select which intervention you want to include in the cost assessment.""")
                self.ui.cost_variables_menu()
                cost_per_ha = self.calculator.calculate_costs()

            with col2:
                st.subheader("Cost Estimates")

                if cost_per_ha:
                    ssm.DISPLAYED_COST.set(True)
                    ssm.COST_DATA.set(cost_per_ha)

                # Always display if we have costs data
                if ssm.DISPLAYED_COST.get():
                    self.ui.display_costs(ssm.COST_DATA.get())


def main():
    st.set_page_config(
        page_title="Ecosystem Valuation Tool",
        page_icon="🌱",
        layout="wide"
    )

    app = EcoApp()
    app.set_css()
    app.initialize()
    app.welcome()
    app.biomes()
    app.location()
    app.benefits()
    app.costs()



if __name__ == "__main__":
    main()

