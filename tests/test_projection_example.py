import pytest
from energy_transition.data import load_and_clean_data
from energy_transition.scenarios import run_cop30_forecasts

def test_projection_matches_verified_example():
    """
    Regression test ensuring Kenya's COP30 projection for year 2025 (t=3) 
    matches expected theoretical benchmarks within acceptable numerical tolerance.
    """
    df = load_and_clean_data()
    
    # Isolate and print filtered 2022 raw baseline columns for Kenya
    baseline_cols = [
        'iso_code', 'year', 'population', 
        'renewables_electricity', 'fossil_electricity', 
        'nuclear_electricity', 'carbon_intensity_elec'
    ]
    kenya_2022_baseline = df[(df['iso_code'] == 'KEN') & (df['year'] == 2022)][baseline_cols]
    print("\n=== FILTERED RAW 2022 BASELINE DATA (KENYA) ===")
    print(kenya_2022_baseline.to_string(index=False))
    
    forecast_df = run_cop30_forecasts(df)
    
    # Filter for Kenya COP30 results and print the full projection table
    kenya_cop30 = forecast_df[
        (forecast_df["iso_code"] == "KEN") & 
        (forecast_df["scenario"].str.contains("COP30", case=False, na=False))
    ]
    print("\n--- Full Kenya COP30 Projections ---")
    print(kenya_cop30[["year", "renewables_twh", "fossil_twh", "total_twh", "per_capita_kwh"]].to_string(index=False))
    
    match = kenya_cop30[kenya_cop30["year"] == 2025]
    
    assert not match.empty, "No records found for Kenya (KEN) in COP30 2025 forecast output."
    kenya_2025 = match.iloc[0]
    
     # Analytically derived target benchmarks from our worked example
    expected_renewable_twh = 17.18
    expected_fossil_twh = 1.23
    expected_total_twh = expected_renewable_twh + expected_fossil_twh
    expected_per_capita_kwh = 319.40

    # Allow a reasonable relative tolerance (e.g., 5%) for theoretical vs algorithmic differences
    tolerance_rel = 0.01
    
    # Verify that the forecasted values are within the expected tolerance of the analytically derived benchmarks
    assert kenya_2025["renewables_twh"] == pytest.approx(expected_renewable_twh, rel=tolerance_rel)
    assert kenya_2025["fossil_twh"] == pytest.approx(expected_fossil_twh, rel=tolerance_rel)
    assert kenya_2025["total_twh"] == pytest.approx(expected_total_twh, rel=tolerance_rel)
    
    # Verify per-capita access equivalence within tolerance
    actual_per_capita = kenya_2025["per_capita_kwh"]
    assert actual_per_capita == pytest.approx(expected_per_capita_kwh, rel=tolerance_rel)