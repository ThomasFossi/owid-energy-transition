"""
Data ingestion and preprocessing module for global energy transitions. The function returns a cleaned and filtered 
DataFrame ready for analysis, with structural zero imputation and segmented interpolation applied.
We are implementing sovereign entity filtering, zero imputation, and segmented interpolation.
"""

import os
import pandas as pd

def load_and_clean_data(raw_data_path: str = "data/raw/owid-energy-data.csv") -> pd.DataFrame:
    """
    Loads the raw OWID energy dataset, filters for sovereign entities within the 8-country cohort (1990-2024), and applies 
    physics-based imputation. 
    1990 is the earliest year with complete data for all cohort members but also is the standard benchmark for global 
    climate agreements like the Rio de Janeiro 1992 summit and the 1997 Kyoto Protocol. 
    """
    # Ensuring the raw data file exists before proceeding
    if not os.path.exists(raw_data_path):
        raise FileNotFoundError(f"Raw data file not found at {raw_data_path}. Please place owid-energy-data.csv there.")
        
    raw_df = pd.read_csv(raw_data_path)
    
    # Isolating sovereign entities by filtering out non-sovereign entries (e.g., regions, continents)
    # We want to make sure we don't include aggregate regions like "World" or "Europe" in our analysis, 
    # which would cause double counting and distort the cohort analysis.
    sovereign_df = raw_df[raw_df['iso_code'].notna()].copy()
    sovereign_df = sovereign_df[~sovereign_df['iso_code'].str.startswith('OWID_')].copy()
    
    # Defining the 8-country cohort for analysis: Cameroon, Egypt, Kenya, South Africa, Germany, France, China, USA
    cohort_isos = ['CMR', 'EGY', 'KEN', 'ZAF', 'DEU', 'FRA', 'CHN', 'USA']

    # Filtering for the cohort and the analysis window (1990-2024), a sorting step is applied to ensure chronological order for interpolation and analysis.
    analysis_df = sovereign_df[
        (sovereign_df['iso_code'].isin(cohort_isos)) &
        (sovereign_df['year'].between(1990, 2024))
    ].sort_values(['iso_code', 'year']).reset_index(drop=True)
    
    # Structural zero imputation for emerging technologies (solar, wind, nuclear, other renewables, biofuels). 
    # All missing values for these columns are filled with 0.0, reflecting the physical reality that these technologies 
    # were not deployed in certain countries or years.
    emerging_tech_cols = [
        'solar_electricity', 'wind_electricity', 'nuclear_electricity',
        'other_renewable_electricity', 'biofuel_electricity'
    ]
    analysis_df[emerging_tech_cols] = analysis_df[emerging_tech_cols].fillna(0.0)
    
    # Segmentation-based interpolation for legacy energy sources and key metrics
    legacy_cols = [
        'hydro_electricity', 'coal_electricity', 'gas_electricity', 'oil_electricity',
        'renewables_electricity', 'fossil_electricity', 'electricity_generation',
        'primary_energy_consumption', 'carbon_intensity_elec', 'population',
        'per_capita_electricity', 'fossil_share_energy'
    ]
    # Interpolation is applied within each country (iso_code) to fill in missing values for legacy energy sources and key metrics.
    # The interpolation is limited to a maximum of 2 consecutive missing years, and only applied to gaps that are bounded by existing data points (limit_area='inside').
    analysis_df[legacy_cols] = (
        analysis_df.groupby('iso_code')[legacy_cols]
        .transform(lambda s: s.interpolate(method='linear', limit=2, limit_area='inside'))
    )
    
    return analysis_df