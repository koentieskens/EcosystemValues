"""Shared pytest fixtures for all test modules."""
import copy
import pytest

from src.models.benefit_models import TropicalForest, IntensiveLandUse
from src.models.cost_models import IntensiveLandUseCost
from src.variables.variables import ModelVariable
from src.variables.ecosystem_service import EcosystemService
from src.variables.value_type import ValueType


@pytest.fixture
def tropical_forest_model():
    """
    Return TropicalForest class with realistic values set on all VARIABLES.

    TropicalForest.VARIABLES are shared class attributes, so we set values
    to mid-range realistic numbers before yielding and reset them afterwards
    to avoid test pollution.
    """
    # Store original values
    original_values = [var.value for var in TropicalForest.VARIABLES]

    # Realistic mid-range values (within min/max bounds for each variable)
    realistic_values = {
        'Elevation': 500.0,          # min=0, max=1572
        'slope': 3.0,                # min=0.05, max=11.2
        'totalAnnualPrecip': 1.5,    # min=0.4, max=2.8
        'biodivIntactness': 80.0,    # min=64, max=100
        'protStatus': 20.0,          # min=0, max=100
        'humanModification': 20.0,   # min=0, max=80
        'popDensity': 100.0,         # min=0.5, max=1400
        'GNIPC': 10000.0,            # min=520, max=49650
    }

    for var in TropicalForest.VARIABLES:
        name = var.variable.name if hasattr(var.variable, 'name') else None
        if name in realistic_values:
            var.value = realistic_values[name]
        elif var.lc is not None:
            # LAND_COVER variable — set to a percentage
            var.value = 30.0
        else:
            var.value = 10.0  # sensible fallback

    yield TropicalForest

    # Restore original values
    for var, orig in zip(TropicalForest.VARIABLES, original_values):
        var.value = orig


@pytest.fixture
def ilu_cost_model():
    """
    Return IntensiveLandUseCost class with realistic values set on VARIABLES.
    INPUT_VARIABLES (latitude, days) are set inside predict_cost itself.
    """
    original_values = [var.value for var in IntensiveLandUseCost.VARIABLES]

    realistic_values = {
        'GDPPC_PPP_CONTSTANT': 30000.0,
        'meanAnnualTemp': 20.0,
        'totalAnnualPrecip': 1.0,
        'slope': 5.0,
    }

    for var in IntensiveLandUseCost.VARIABLES:
        name = var.variable.name if hasattr(var.variable, 'name') else None
        if name in realistic_values:
            var.value = realistic_values[name]
        else:
            var.value = 1.0

    yield IntensiveLandUseCost

    for var, orig in zip(IntensiveLandUseCost.VARIABLES, original_values):
        var.value = orig


@pytest.fixture
def ecosystem_service_fixture():
    """ModelVariable wrapping EcosystemService.GLOBAL_CLIMATE with a coefficient."""
    return ModelVariable(EcosystemService.GLOBAL_CLIMATE, coefficient=3.513, value=1.0)


@pytest.fixture
def value_type_fixture():
    """ModelVariable wrapping ValueType.EXCHANGE_VALUE with a coefficient."""
    return ModelVariable(ValueType.EXCHANGE_VALUE, coefficient=-0.054, value=1.0)
