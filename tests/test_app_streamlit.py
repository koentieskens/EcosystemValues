"""
Streamlit integration tests using streamlit.testing.v1.AppTest.

Each test runs the full app.py script in a headless environment, optionally
simulates widget interactions, and asserts that no uncaught Python exceptions
occur.  All calls that require live credentials or network access (GCP / GEE,
World Bank API, reverse_geocode) are patched so the suite runs fully offline.
"""
import pytest
from contextlib import ExitStack
from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest

from src.models.benefit_models import TropicalForest, IntensiveLandUse, Grassland

APP_PATH = "app.py"

# ---------------------------------------------------------------------------
# Re-usable mock return values
# ---------------------------------------------------------------------------
FAKE_MAP_DATA = {"all_drawings": [], "last_active_drawing": None}
FAKE_GEOCODE = {"country_code": "NLD", "county": "Utrecht"}
FAKE_LOCATION = {"lat": 51.9, "lon": 5.1, "area": 100.0}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _apply_patches(stack: ExitStack):
    """
    Register all patches that prevent real network / file-system side effects.
    Called inside an ExitStack so they are all torn down together.
    """
    # Folium map component — returns an empty map-data dict
    stack.enter_context(
        patch("src.app_utils.locations_components.st_folium",
              return_value=FAKE_MAP_DATA)
    )
    # reverse_geocode — used in location activation and benefit calculation
    stack.enter_context(
        patch("src.app_utils.locations_components.St_Utils.get_location_info",
              return_value=("Utrecht", "Netherlands"))
    )
    stack.enter_context(
        patch("src.app_utils.utils.reverse_geocode.get",
              return_value=FAKE_GEOCODE)
    )
    stack.enter_context(
        patch("src.app_utils.calculation_engine.reverse_geocode.get",
              return_value=FAKE_GEOCODE)
    )
    # GCP auth — replaced by a no-op so no secrets are needed
    stack.enter_context(
        patch("src.app_utils.gcp_authenticate.ConnectToGoogle.connect_to_google")
    )


def _make_at(session_overrides: dict | None = None) -> AppTest:
    """
    Create an AppTest instance with GCP initialisation pre-skipped and any
    extra session-state values applied.
    """
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.session_state["init_done"] = True           # skip GCP auth / EE init
    if session_overrides:
        for key, value in session_overrides.items():
            at.session_state[key] = value
    return at


def _run(at: AppTest) -> AppTest:
    """Run the app with all standard patches active."""
    with ExitStack() as stack:
        _apply_patches(stack)
        at.run()
    return at


def _click_and_run(at: AppTest, button_label: str) -> AppTest:
    """Click the first button whose label matches, then re-run the app."""
    for btn in at.button:
        if btn.label == button_label:
            btn.click()
            break
    return _run(at)


def _find_button(at: AppTest, label: str):
    """Return the first button matching `label`, or None."""
    for btn in at.button:
        if btn.label == label:
            return btn
    return None


# ---------------------------------------------------------------------------
# 1. Initial load
# ---------------------------------------------------------------------------

class TestInitialLoad:
    def test_app_loads_without_exception(self):
        """
        The app renders from scratch (with init skipped) without raising any
        uncaught Python exception.
        """
        at = _make_at()
        _run(at)
        assert len(at.exception) == 0, f"Unexpected exception: {at.exception}"

    def test_biome_selection_header_is_present(self):
        """The 'Select Biome' header is rendered on the initial load."""
        at = _make_at()
        _run(at)
        headers = [h.value for h in at.header]
        assert any("Biome" in h for h in headers), (
            f"Expected 'Select Biome' header, found: {headers}"
        )


# ---------------------------------------------------------------------------
# 2. Biome selection buttons
# ---------------------------------------------------------------------------

class TestBiomeButtons:
    """Each biome button should set the model class without raising."""

    @pytest.mark.parametrize("key,display_name,expected_type", [
        ("tropical_forest",    "Tropical Forest",    TropicalForest),
        ("intensive_land_use", "Intensive Land Use",  IntensiveLandUse),
        ("grassland",          "Grassland",           Grassland),
    ])
    def test_biome_button_sets_model_class(self, key, display_name, expected_type):
        at = _make_at()
        _run(at)                               # initial render

        # Find the biome button by key and click it
        clicked = False
        for btn in at.button:
            if btn.key == f"biome_select_{key}":
                btn.click()
                clicked = True
                break

        assert clicked, f"Button 'biome_select_{key}' not found"
        _run(at)                               # re-render after click

        assert len(at.exception) == 0, f"Unexpected exception: {at.exception}"
        assert at.session_state["ecosystem_type"] == key
        assert isinstance(at.session_state["model_class"], expected_type)


# ---------------------------------------------------------------------------
# 3. Location — Activate Manual Input
# ---------------------------------------------------------------------------

class TestManualInput:
    def test_activate_manual_input_sets_location(self):
        """
        Clicking 'Activate Manual Input' stores the lat/lon/area in
        project_location and sets location_activated to True.
        """
        at = _make_at()
        _run(at)

        btn = _find_button(at, "Activate Manual Input")
        assert btn is not None, "'Activate Manual Input' button not found"
        btn.click()
        _run(at)

        assert len(at.exception) == 0, f"Unexpected exception: {at.exception}"
        assert at.session_state["location_activated"] is True
        loc = at.session_state["project_location"]
        assert loc is not None
        assert "lat" in loc and "lon" in loc and "area" in loc

    def test_activate_polygon_without_polygon_shows_error_not_exception(self):
        """
        Clicking 'Activate Polygon Input' without having drawn a polygon
        should NOT raise an uncaught exception — the app handles it gracefully
        with st.error().
        """
        at = _make_at()
        _run(at)

        btn = _find_button(at, "Activate Polygon Input")
        assert btn is not None, "'Activate Polygon Input' button not found"
        btn.click()
        _run(at)

        assert len(at.exception) == 0, f"Unexpected exception: {at.exception}"


# ---------------------------------------------------------------------------
# 4. Calculate Benefits
# ---------------------------------------------------------------------------

class TestCalculateBenefits:
    def _setup_for_benefits(self, monkeypatch):
        """
        Pre-seed session state and mark the first ecosystem service as
        selected so that calculate_benefit() actually calls predict_benefit().
        """
        # Mark first ecosystem service as selected (value=1)
        monkeypatch.setattr(TropicalForest.ECOSYSTEM_SERVICES[0], "value", 1)

        at = _make_at({
            "init_done": True,
            "model_class": TropicalForest(),
            "ecosystem_type": "tropical_forest",
            "ecosystem_display_name": "Tropical Forest",
            "location_activated": True,
            "project_location": FAKE_LOCATION,
            "polygon_centroid": (FAKE_LOCATION["lat"], FAKE_LOCATION["lon"]),
            "prediction_sets": {},
        })
        return at

    def test_calculate_benefits_no_exception(self, monkeypatch):
        """
        With a biome selected and location set, clicking Calculate Benefits
        (with mocked prediction) must not raise any uncaught exception.
        """
        at = self._setup_for_benefits(monkeypatch)
        _run(at)   # initial render

        btn = _find_button(at, "Calculate Benefits")
        assert btn is not None, "'Calculate Benefits' button not found"
        btn.click()

        with ExitStack() as stack:
            _apply_patches(stack)
            stack.enter_context(
                patch("src.app_utils.calculation_engine.Predict.predict_benefit",
                      return_value=500.0)
            )
            stack.enter_context(
                patch("src.app_utils.calculation_engine.CurrencyConverter.convert_ppp_to_usd",
                      return_value=1.0)
            )
            stack.enter_context(
                patch("src.app_utils.calculation_engine.CurrencyConverter.convert_usd_year",
                      return_value=1.0)
            )
            at.run()

        assert len(at.exception) == 0, f"Unexpected exception: {at.exception}"

    def test_calculate_benefits_updates_state(self, monkeypatch):
        """After a successful run the benefits_updated flag is True."""
        at = self._setup_for_benefits(monkeypatch)
        _run(at)

        btn = _find_button(at, "Calculate Benefits")
        assert btn is not None
        btn.click()

        with ExitStack() as stack:
            _apply_patches(stack)
            stack.enter_context(
                patch("src.app_utils.calculation_engine.Predict.predict_benefit",
                      return_value=250.0)
            )
            stack.enter_context(
                patch("src.app_utils.calculation_engine.CurrencyConverter.convert_ppp_to_usd",
                      return_value=1.0)
            )
            stack.enter_context(
                patch("src.app_utils.calculation_engine.CurrencyConverter.convert_usd_year",
                      return_value=1.0)
            )
            at.run()

        assert at.session_state["benefits_updated"] is True


# ---------------------------------------------------------------------------
# 5. Calculate Costs
# ---------------------------------------------------------------------------

class TestCalculateCosts:
    def _setup_for_costs(self, monkeypatch):
        """Pre-seed state for cost calculation (IntensiveLandUse / NBS branch)."""
        # Mark first NBS as selected
        monkeypatch.setattr(IntensiveLandUse.COST_MODEL.NBS[0], "value", 1)

        at = _make_at({
            "init_done": True,
            "model_class": IntensiveLandUse(),
            "ecosystem_type": "intensive_land_use",
            "ecosystem_display_name": "Intensive Land Use",
            "location_activated": True,
            "project_location": FAKE_LOCATION,
            "polygon_centroid": (FAKE_LOCATION["lat"], FAKE_LOCATION["lon"]),
            "cost_extraction_done": True,   # NBS branch requires this flag
        })
        return at

    def test_calculate_costs_no_exception(self, monkeypatch):
        """
        With ILU selected and cost variables extracted, clicking Calculate
        Costs (with mocked prediction) must not raise any uncaught exception.
        """
        at = self._setup_for_costs(monkeypatch)
        _run(at)

        btn = _find_button(at, "Calculate Costs")
        assert btn is not None, "'Calculate Costs' button not found"
        btn.click()

        with ExitStack() as stack:
            _apply_patches(stack)
            stack.enter_context(
                patch("src.app_utils.calculation_engine.Predict.predict_cost",
                      return_value=1500.0)
            )
            stack.enter_context(
                patch("src.app_utils.calculation_engine.CurrencyConverter.convert_ppp_to_usd",
                      return_value=1.0)
            )
            stack.enter_context(
                patch("src.app_utils.calculation_engine.CurrencyConverter.convert_usd_year",
                      return_value=1.0)
            )
            at.run()

        assert len(at.exception) == 0, f"Unexpected exception: {at.exception}"

    def test_calculate_costs_stores_cost_data(self, monkeypatch):
        """After a successful cost calculation cost_data is set in session state."""
        at = self._setup_for_costs(monkeypatch)
        _run(at)

        btn = _find_button(at, "Calculate Costs")
        assert btn is not None
        btn.click()

        with ExitStack() as stack:
            _apply_patches(stack)
            stack.enter_context(
                patch("src.app_utils.calculation_engine.Predict.predict_cost",
                      return_value=1500.0)
            )
            stack.enter_context(
                patch("src.app_utils.calculation_engine.CurrencyConverter.convert_ppp_to_usd",
                      return_value=1.0)
            )
            stack.enter_context(
                patch("src.app_utils.calculation_engine.CurrencyConverter.convert_usd_year",
                      return_value=1.0)
            )
            at.run()

        cost_data = at.session_state["cost_data"]
        assert cost_data is not None
        assert isinstance(cost_data, list)
        assert len(cost_data) > 0


# ---------------------------------------------------------------------------
# 6. Extract Spatial Variables (GEE) button — offline mock
# ---------------------------------------------------------------------------

class TestExtractGeeButton:
    def test_extract_benefit_gee_button_no_exception(self, monkeypatch):
        """
        Clicking 'Extract Spatial Values from GEE' for benefit variables
        with GEE mocked must not raise an uncaught exception.
        """
        at = _make_at({
            "init_done": True,
            "model_class": TropicalForest(),
            "ecosystem_type": "tropical_forest",
            "location_activated": True,
            "project_location": FAKE_LOCATION,
        })
        _run(at)

        # Find the benefit GEE extract button by key
        btn = None
        for b in at.button:
            if b.key == "benefit_gee":
                btn = b
                break

        assert btn is not None, "'benefit_gee' button not found"
        btn.click()

        with ExitStack() as stack:
            _apply_patches(stack)
            # Mock GEE extraction to return realistic fake values
            fake_extracted = {
                var.variable.name: 50.0
                for var in TropicalForest.VARIABLES
                if not var.lc
            }
            stack.enter_context(
                patch("src.app_utils.ui_components.St_Utils.extract_values",
                      return_value=(fake_extracted, None))
            )
            at.run()

        assert len(at.exception) == 0, f"Unexpected exception: {at.exception}"
