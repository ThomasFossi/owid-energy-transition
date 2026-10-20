"""
Unit tests for energy transition metrics and data processing functions.
"""

import pandas as pd
import pytest
from energy_transition.data import load_and_clean_data
from energy_transition.metrics import compute_2022_benchmarks

@pytest.fixture
def cleaned_data():
    """Fixture that loads and cleans data once for multiple tests."""
    try:
        return load_and_clean_data()
    except FileNotFoundError:
        pytest.skip("Raw OWID dataset not found in data/raw/ - skipping test.")

def test_data_loading_and_structure(cleaned_data):
    """Verify that the cleaned DataFrame has the expected columns and sovereign cohort."""
    expected_cols = ['country', 'iso_code', 'year', 'electricity_generation', 'population']
    for col in expected_cols:
        assert col in cleaned_data.columns, f"Missing expected column: {col}"
        
    # Verify cohort ISOs are restricted to our 8-country list
    cohort_isos = ['CMR', 'EGY', 'KEN', 'ZAF', 'DEU', 'FRA', 'CHN', 'USA']
    unique_isos = cleaned_data['iso_code'].unique()
    for iso in unique_isos:
        assert iso in cohort_isos, f"Unexpected ISO found in cohort: {iso}"

def test_2022_benchmarks_bounds(cleaned_data):
    """Verify that 2022 benchmark shares are physically bounded between 0 and 100%."""
    bench = compute_2022_benchmarks(cleaned_data)
    
    assert not bench.empty, "Benchmark DataFrame is empty for 2022."
    
    for _, row in bench.iterrows():
        # Shares should be within [0, 100] percentage bounds
        assert 0.0 <= row['renewable_share_pct'] <= 100.0, f"Invalid renewable share for {row['iso_code']}"
        assert 0.0 <= row['fossil_share_pct'] <= 100.0, f"Invalid fossil share for {row['iso_code']}"
        # Per-capita electricity must be non-negative
        assert row['per_capita_elec_kwh'] >= 0.0, f"Negative per-capita electricity for {row['iso_code']}"