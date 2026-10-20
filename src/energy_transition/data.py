"""
Data ingestion and preprocessing module for global energy transitions.
We are implementing sovereign entity filtering, zero imputation, and segmented interpolation.
"""

import os
import pandas as pd

def load_and_clean_data(raw_data_path: str = "data/raw/owid-energy-data.csv") -> pd.DataFrame:
    """
    Loads the raw OWID energy dataset, filters for sovereign entities within 
    the 8-country cohort (1990-2024), and applies physics-based imputation.
    """
    if not os.path.exists(raw_data_path):
        raise FileNotFoundError(f"Raw data file not found at {raw_data_path}. Please place owid-energy-data.csv there.")
        
    raw_df = pd.read_csv(raw_data_path)
    
    # Isolating sovereign entities by filtering out non-sovereign entries (e.g., regions, continents)
    sovereign_df = raw_df[raw_df['iso_code'].notna()].copy()
    sovereign_df = sovereign_df[~sovereign_df['iso_code'].str.startswith('OWID_')].copy()
    
    # Defining the 8-country cohort for analysis: Cameroon, Egypt, Kenya, South Africa, Germany, France, China, USA
    cohort_isos = ['CMR', 'EGY', 'KEN', 'ZAF', 'DEU', 'FRA', 'CHN', 'USA']
    
    analysis_df = sovereign_df[
        (sovereign_df['iso_code'].isin(cohort_isos)) &
        (sovereign_df['year'].between(1990, 2024))
    ].sort_values(['iso_code', 'year']).reset_index(drop=True)
    
    # Structural zero imputation for emerging technologies (solar, wind, nuclear, other renewables, biofuels)
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
    
    analysis_df[legacy_cols] = (
        analysis_df.groupby('iso_code')[legacy_cols]
        .transform(lambda s: s.interpolate(method='linear', limit=2, limit_area='inside'))
    )
    
    return analysis_df