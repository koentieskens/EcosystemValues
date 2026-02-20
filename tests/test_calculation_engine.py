"""Tests for src/app_utils/calculation_engine.py → CalculationEngine."""
import math
import pytest
from unittest.mock import patch, MagicMock, call

from src.variables.variables import ModelVariable
from src.variables.ecosystem_service import EcosystemService
from src.variables.value_type import ValueType


# ---------------------------------------------------------------------------
# Helpers / shared mock factories
# ---------------------------------------------------------------------------

def _make_project_location(lat=50.0, lon=10.0, area=100.0):
    return {"lat": lat, "lon": lon, "area": area}


def _make_model_class_mock():
    """
    Build a minimal mock model class that CalculationEngine.calculate_benefit
    expects: VALUE_TYPES, ECOSYSTEM_SERVICES, no SIIKAMAKI attribute.
    """
    es = ModelVariable(EcosystemService.WOOD_PROVISION, coefficient=1.183, value=1.0)
    es.global_layer = None  # not a vector layer ES

    vt_exchange = ModelVariable(ValueType.EXCHANGE_VALUE, coefficient=-0.054, value=1.0)
    vt_cons = ModelVariable(ValueType.CONS_SURPLUS, coefficient=-1.378, value=1.0)

    model_cls = MagicMock()
    model_cls.VALUE_TYPES = [vt_exchange, vt_cons]
    model_cls.ECOSYSTEM_SERVICES = [es]
    # no SIIKAMAKI on the mock
    del model_cls.SIIKAMAKI
    return model_cls, es, vt_exchange


# ---------------------------------------------------------------------------
# calculate_benefit
# ---------------------------------------------------------------------------

class TestCalculateBenefit:
    """
    Tests for CalculationEngine.calculate_benefit.

    We mock:
    - streamlit (st.button → True so the body executes, st.success/error → no-op)
    - ssm session state variables
    - Predict.predict_benefit
    - CurrencyConverter.convert_ppp_to_usd
    - reverse_geocode.get
    """

    def _run_calculate_benefit(self, mock_predict_return=500.0):
        """
        Wire up all mocks and invoke calculate_benefit.
        Returns (engine, ssm_mock, prediction_sets_holder).
        """
        from src.app_utils.calculation_engine import CalculationEngine

        model_cls, es, vt_exchange = _make_model_class_mock()
        prediction_sets = {}

        with patch("src.app_utils.calculation_engine.st") as mock_st, \
             patch("src.app_utils.calculation_engine.ssm") as mock_ssm, \
             patch("src.app_utils.calculation_engine.Predict.predict_benefit",
                   return_value=mock_predict_return) as mock_predict, \
             patch("src.app_utils.calculation_engine.CurrencyConverter.convert_ppp_to_usd",
                   return_value=1.0) as mock_convert, \
             patch("src.app_utils.calculation_engine.CurrencyConverter.convert_usd_year",
                   return_value=1.0), \
             patch("src.app_utils.calculation_engine.reverse_geocode.get",
                   return_value={"country_code": "NLD"}):

            # st.button → True so the if-block runs
            mock_st.button.return_value = True

            mock_ssm.PROJECT_LOCATION.get.return_value = _make_project_location()
            mock_ssm.MODEL_CLASS.get.return_value = model_cls
            mock_ssm.PREDICTION_SETS.get.return_value = prediction_sets
            mock_ssm.BENEFITS_UPDATED.set = MagicMock()

            engine = CalculationEngine()
            engine.calculate_benefit()

        return engine, mock_ssm, mock_predict, prediction_sets

    def test_predict_benefit_is_called(self):
        """predict_benefit() is called at least once during calculate_benefit."""
        _, _, mock_predict, _ = self._run_calculate_benefit()
        assert mock_predict.called

    def test_result_stored_in_prediction_sets(self):
        """After calculate_benefit(), PREDICTION_SETS contains the ecosystem service key."""
        _, mock_ssm, _, prediction_sets = self._run_calculate_benefit(mock_predict_return=250.0)
        # prediction_sets is mutated in-place by the engine
        all_values = {k: v for d in prediction_sets.values() for k, v in d.items()}
        assert len(all_values) > 0, "prediction_sets should contain at least one result"

    def test_benefits_updated_flag_set(self):
        """ssm.BENEFITS_UPDATED.set(True) is called on success."""
        _, mock_ssm, _, _ = self._run_calculate_benefit()
        mock_ssm.BENEFITS_UPDATED.set.assert_called_with(True)


# ---------------------------------------------------------------------------
# calculate_costs  — NBS branch (IntensiveLandUseCost)
# ---------------------------------------------------------------------------

class TestCalculateCosts:
    """
    Tests for CalculationEngine.calculate_costs using the NBS branch
    (model_class.COST_MODEL has NBS attribute but no GLOBAL_LAYERS).
    """

    def _run_calculate_costs(self, predict_cost_return=1500.0):
        from src.app_utils.calculation_engine import CalculationEngine
        from src.models.benefit_models import IntensiveLandUse

        # Use IntensiveLandUse as a realistic model class (its COST_MODEL has NBS)
        nbs_var = IntensiveLandUse.COST_MODEL.NBS[0]
        nbs_var.value = 1.0  # mark it as selected

        result_holder = {}

        with patch("src.app_utils.calculation_engine.st") as mock_st, \
             patch("src.app_utils.calculation_engine.ssm") as mock_ssm, \
             patch("src.app_utils.calculation_engine.Predict.predict_cost",
                   return_value=predict_cost_return) as mock_predict_cost, \
             patch("src.app_utils.calculation_engine.CurrencyConverter.convert_ppp_to_usd",
                   return_value=1.0), \
             patch("src.app_utils.calculation_engine.CurrencyConverter.convert_usd_year",
                   return_value=1.0), \
             patch("src.app_utils.calculation_engine.reverse_geocode.get",
                   return_value={"country_code": "NLD"}):

            mock_st.button.return_value = True
            mock_ssm.PROJECT_LOCATION.get.return_value = _make_project_location(lat=30.0)
            mock_ssm.MODEL_CLASS.get.return_value = IntensiveLandUse
            mock_ssm.COST_EXTRACTION_DONE.get.return_value = True

            engine = CalculationEngine()
            result = engine.calculate_costs()
            result_holder["result"] = result
            result_holder["mock_predict_cost"] = mock_predict_cost

        return result_holder

    def test_predict_cost_is_called(self):
        """predict_cost() is called once during calculate_costs."""
        holder = self._run_calculate_costs()
        assert holder["mock_predict_cost"].called

    def test_predict_cost_called_with_correct_area_and_lat(self):
        """predict_cost is called with area=100 ha and lat=30.0 from project location."""
        holder = self._run_calculate_costs()
        mock_predict_cost = holder["mock_predict_cost"]
        call_kwargs = mock_predict_cost.call_args
        # area_hectares is the 3rd positional arg, latitude is 4th
        args = call_kwargs[0]  # positional args tuple
        assert args[2] == pytest.approx(100.0)  # area_hectares
        assert args[3] == pytest.approx(30.0)   # latitude

    def test_result_is_list_of_dicts(self):
        """calculate_costs returns a list of {'NBS Total Cost': value} dicts."""
        holder = self._run_calculate_costs(predict_cost_return=2000.0)
        result = holder["result"]
        assert isinstance(result, list)
        assert len(result) > 0
        assert "NBS Total Cost" in result[0]

    def test_cost_value_is_positive(self):
        """The returned cost value is positive."""
        holder = self._run_calculate_costs(predict_cost_return=2000.0)
        result = holder["result"]
        cost = result[0]["NBS Total Cost"]
        assert cost > 0
