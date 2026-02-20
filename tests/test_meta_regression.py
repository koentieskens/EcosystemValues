"""Tests for src/predictions/meta_regression.py → Predict class."""
import math
import pytest

from src.predictions.meta_regression import Predict
from src.variables.variables import ModelVariable
from src.variables.ecosystem_service import EcosystemService
from src.variables.value_type import ValueType


# ---------------------------------------------------------------------------
# Pure math helpers
# ---------------------------------------------------------------------------

class TestLogP1:
    def test_positive_value(self):
        """log_p1(9) == log(10)"""
        assert Predict.log_p1(9) == pytest.approx(math.log(10))

    def test_zero(self):
        """log_p1(0) == log(1) == 0"""
        assert Predict.log_p1(0) == pytest.approx(0.0)

    def test_negative_guard(self):
        """log_p1(-2) returns 0 because value+1 = -1 is not > 0"""
        assert Predict.log_p1(-2) == 0.0


class TestIhs:
    def test_zero(self):
        """ihs(0) == arcsinh(0) == 0"""
        assert Predict.ihs(0) == pytest.approx(0.0)

    def test_reverse_is_inverse(self):
        """ihs_reverse(ihs(x)) ≈ x (mathematical identity)"""
        x = 5.0
        assert Predict.ihs_reverse(Predict.ihs(x)) == pytest.approx(x, rel=1e-9)


class TestAreaLimiter:
    def test_below_limit(self):
        """Values below the 1000 ha cap pass through unchanged."""
        assert Predict.area_limiter(500) == 500

    def test_above_limit(self):
        """Values above the default 1000 ha cap are clipped to 1000."""
        assert Predict.area_limiter(2000) == 1000

    def test_exact_limit(self):
        """Value equal to the limit is unchanged."""
        assert Predict.area_limiter(1000) == 1000

    def test_custom_limit(self):
        """Custom limit is respected."""
        assert Predict.area_limiter(300, limit=200) == 200


# ---------------------------------------------------------------------------
# Prediction tests (use conftest fixtures)
# ---------------------------------------------------------------------------

class TestPredictBenefit:
    def test_returns_positive_float(self, tropical_forest_model, ecosystem_service_fixture, value_type_fixture):
        """predict_benefit() returns a positive float given valid inputs."""
        result = Predict.predict_benefit(
            model_class=tropical_forest_model,
            ecosystem_service=ecosystem_service_fixture,
            value_type=value_type_fixture,
            area_hectares=100.0
        )
        assert isinstance(result, float)
        assert result > 0.0

    def test_respects_value_bounds(self, tropical_forest_model, ecosystem_service_fixture, value_type_fixture):
        """
        Setting variable values beyond their max_value must produce the same
        result as setting them exactly at max_value (because predict_benefit
        caps values before computing).
        """
        # Set all bounded variables to their max_value
        for var in tropical_forest_model.VARIABLES:
            if var.max_value is not None:
                var.value = var.max_value

        result_at_max = Predict.predict_benefit(
            model_class=tropical_forest_model,
            ecosystem_service=ecosystem_service_fixture,
            value_type=value_type_fixture,
            area_hectares=100.0
        )

        # Now push values well beyond max
        for var in tropical_forest_model.VARIABLES:
            if var.max_value is not None:
                var.value = var.max_value * 10

        result_beyond_max = Predict.predict_benefit(
            model_class=tropical_forest_model,
            ecosystem_service=ecosystem_service_fixture,
            value_type=value_type_fixture,
            area_hectares=100.0
        )

        assert result_at_max == pytest.approx(result_beyond_max, rel=1e-9), (
            "Result should be the same when variable values are capped at max_value"
        )

    def test_larger_area_affects_result(self, tropical_forest_model, ecosystem_service_fixture, value_type_fixture):
        """
        Area_ha_ln coefficient is negative for TropicalForest (-0.323),
        so a larger area should produce a smaller per-ha benefit.
        """
        result_small = Predict.predict_benefit(
            model_class=tropical_forest_model,
            ecosystem_service=ecosystem_service_fixture,
            value_type=value_type_fixture,
            area_hectares=10.0
        )
        result_large = Predict.predict_benefit(
            model_class=tropical_forest_model,
            ecosystem_service=ecosystem_service_fixture,
            value_type=value_type_fixture,
            area_hectares=1000.0
        )
        assert result_large < result_small


class TestPredictCost:
    def test_returns_positive_float(self, ilu_cost_model):
        """predict_cost() with IntensiveLandUseCost returns a positive float."""
        nbs = [ModelVariable(variable='NBS_test', coefficient=0.5, value=1.0)]
        result = Predict.predict_cost(
            model_class=ilu_cost_model,
            nbss=nbs,
            area_hectares=200.0,
            latitude=30.0
        )
        assert isinstance(result, float)
        assert result > 0.0

    def test_area_is_capped_at_1000(self, ilu_cost_model):
        """
        Areas above 1000 ha are capped before use, so cost for 2000 ha
        must equal cost for 1000 ha.
        """
        nbs = [ModelVariable(variable='NBS_test', coefficient=0.5, value=1.0)]
        cost_1000 = Predict.predict_cost(
            model_class=ilu_cost_model, nbss=nbs,
            area_hectares=1000.0, latitude=30.0
        )
        cost_2000 = Predict.predict_cost(
            model_class=ilu_cost_model, nbss=nbs,
            area_hectares=2000.0, latitude=30.0
        )
        assert cost_1000 == pytest.approx(cost_2000, rel=1e-9)
