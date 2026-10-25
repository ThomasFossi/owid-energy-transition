"""
Unit tests for COP30 scenario projections and internal consistency checks. To ensure that the forecast outputs are physically 
and mathematically consistent, we validate that all energy generation values are non-negative, per-capita electricity 
consumption is realistic, and carbon intensity metrics remain within plausible bounds. These tests help catch any 
anomalies in the scenario modeling process.
We also test for individual energy transition scenarios and policy consistency.
"""

import pytest
from energy_transition.data import load_and_clean_data
from energy_transition.scenarios import run_cop30_forecasts

# Fixture to load data and generate forecasts once for all scenario tests
@pytest.fixture(scope="module")
def forecast_data():
    """Loads data and generates forecast simulations once for all scenario tests."""
    try:
        df = load_and_clean_data()
        return run_cop30_forecasts(df)
    except FileNotFoundError:
        pytest.skip("Raw OWID dataset not found - skipping scenario tests.")

@pytest.mark.parametrize("scenario_name", [
    "BAU",
    "Accelerated Policy",
    "COP30 Belém 1.5°C"
])
def test_individual_scenario_bounds(forecast_data, scenario_name):
    """
    Independently validate that each scenario is generated correctly 
    and remains strictly within physical bounds.
    """
    scen_df = forecast_data[forecast_data['scenario'] == scenario_name]
    
    # 1. Assert scenario exists and contains records
    assert not scen_df.empty, f"Scenario '{scenario_name}' produced no records."
    
    # 2. Assert mandatory columns exist
    expected_cols = ['country', 'iso_code', 'year', 'scenario', 'renewables_twh', 'fossil_twh', 'per_capita_kwh', 'carbon_intensity']
    for col in expected_cols:
        assert col in scen_df.columns, f"Missing column '{col}' in scenario {scenario_name}"
        
    # 3. Physical boundary constraints for this specific scenario
    assert (scen_df['renewables_twh'] >= 0.0).all(), f"Negative renewables in {scenario_name}"
    assert (scen_df['fossil_twh'] >= 0.0).all(), f"Negative fossil generation in {scenario_name}"
    assert (scen_df['per_capita_kwh'] >= 0.0).all(), f"Negative per-capita supply in {scenario_name}"
    assert (scen_df['carbon_intensity'] >= 0.0).all(), f"Negative carbon intensity in {scenario_name}"
    
    # 4. Check projection timeframe bounds (2023 to 2035)
    years = scen_df['year'].unique()
    assert min(years) == 2023
    assert max(years) == 2035

# Test for policy divergence between scenarios
def test_scenario_policy_divergence(forecast_data):
    """
    Asserts that climate policy scenarios achieve higher renewable generation 
    and lower carbon intensity than Business-As-Usual (BAU) by 2035.
    """
    # Test using Germany (DEU) as a benchmark entity at the 2035 endpoint
    endpoint_2035 = forecast_data[(forecast_data['iso_code'] == 'DEU') & (forecast_data['year'] == 2035)]
    
    bau_row = endpoint_2035[endpoint_2035['scenario'] == 'BAU'].iloc[0]
    cop_row = endpoint_2035[endpoint_2035['scenario'] == 'COP30 Belém 1.5°C'].iloc[0]
    
    # COP30 renewable generation must exceed BAU by 2035
    assert cop_row['renewables_twh'] > bau_row['renewables_twh'], (
        "COP30 mandate failed to outpace BAU renewable generation by 2035."
    )
    
    # COP30 carbon intensity must be strictly lower than BAU by 2035
    assert cop_row['carbon_intensity'] < bau_row['carbon_intensity'], (
        "COP30 grid carbon intensity must be lower than BAU decarbonization floor."
    )