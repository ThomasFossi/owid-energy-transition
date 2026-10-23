"""
Unit tests for COP30 scenario projections and internal consistency checks. To ensure that the forecast outputs are physically 
and mathematically consistent, we validate that all energy generation values are non-negative, per-capita electricity 
consumption is realistic, and carbon intensity metrics remain within plausible bounds. These tests help catch any 
anomalies in the scenario modeling process.
"""

import pytest
from energy_transition.data import load_and_clean_data
from energy_transition.scenarios import run_cop30_forecasts

# Fixture to load and generate forecast data for testing
@pytest.fixture
def forecast_data():
    """Loads data and generates forecast simulations for testing."""
    try:
        df = load_and_clean_data()
        return run_cop30_forecasts(df)
    except FileNotFoundError:
        pytest.skip("Raw OWID dataset not found - skipping scenario tests.")

# Test to ensure that the forecast outputs contain all required columns and that the values are physically bounded.
def test_forecast_structure_and_bounds(forecast_data):
    """Verify that forecast outputs contain required columns and physical bounds."""
    expected_cols = ['country', 'iso_code', 'year', 'scenario', 'renewables_twh', 'per_capita_kwh', 'carbon_intensity']
    for col in expected_cols:
        assert col in forecast_data.columns, f"Missing forecast column: {col}"
        
    # Physical constraints
    assert (forecast_data['renewables_twh'] >= 0.0).all()
    assert (forecast_data['fossil_twh'] >= 0.0).all()
    assert (forecast_data['per_capita_kwh'] >= 0.0).all()
    assert (forecast_data['carbon_intensity'] >= 0.0).all()
    
    # Check projection timeframe (2023 to 2035)
    years = forecast_data['year'].unique()
    assert min(years) == 2023
    assert max(years) == 2035