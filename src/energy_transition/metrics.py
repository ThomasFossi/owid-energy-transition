"""
Metrics module for energy transitions.
This module handles per-capita calculations, fuel shares, demographic dilution, and elasticity regimes.
"""

import numpy as np
import pandas as pd

def compute_2022_benchmarks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts the 2022 cross-sectional benchmark snapshot and calculates 
    per-capita supply, renewable shares, and fossil shares.
    """
    bench_2022 = df[df['year'] == 2022].copy()
    
    bench_2022['per_capita_elec_kwh'] = (bench_2022['electricity_generation'] * 1e9) / bench_2022['population']
    bench_2022['renewable_share_pct'] = (bench_2022['renewables_electricity'] / bench_2022['electricity_generation']) * 100
    bench_2022['fossil_share_pct']    = (bench_2022['fossil_electricity'] / bench_2022['electricity_generation']) * 100
    
    return bench_2022[[
        'country', 'iso_code', 'per_capita_elec_kwh', 
        'carbon_intensity_elec', 'renewable_share_pct', 'fossil_share_pct'
    ]].sort_values('carbon_intensity_elec').reset_index(drop=True)


def compute_demographic_dilution_and_elasticity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivots endpoints (2000 vs 2022) to compute longitudinal growth rates,
    demographic dilution effects, and Access Elasticity (epsilon).
    """
    endpoints = df[df['year'].isin([2000, 2022])].copy()
    
    piv = endpoints.pivot(
        index=['country', 'iso_code'],
        columns='year',
        values=['electricity_generation', 'renewables_electricity', 'population', 'per_capita_electricity']
    )
    
    ren_add_twh    = piv['renewables_electricity'][2022] - piv['renewables_electricity'][2000]
    ren_growth_pct = (ren_add_twh / piv['renewables_electricity'][2000]) * 100
    gen_growth_pct = ((piv['electricity_generation'][2022] - piv['electricity_generation'][2000]) / piv['electricity_generation'][2000]) * 100
    pop_growth_pct = ((piv['population'][2022] - piv['population'][2000]) / piv['population'][2000]) * 100
    pc_growth_pct  = ((piv['per_capita_electricity'][2022] - piv['per_capita_electricity'][2000]) / piv['per_capita_electricity'][2000]) * 100

    eps_access = pc_growth_pct / ren_growth_pct

    conditions = [
        eps_access < 0,
        (eps_access >= 0) & (eps_access <= 1.0),
        eps_access > 1.0
    ]
    choices = [
        'Substitution / Decoupling',
        'Demographically Diluted Expansion',
        'High Expansion Leverage'
    ]

    result_df = pd.DataFrame({
        'ren_addition_twh': ren_add_twh,
        'ren_growth_pct': ren_growth_pct,
        'gen_growth_pct': gen_growth_pct,
        'pop_growth_pct': pop_growth_pct,
        'per_capita_growth_pct': pc_growth_pct,
        'elasticity_eps': eps_access,
        'transition_regime': np.select(conditions, choices, default='Unclassified')
    }).reset_index().sort_values('per_capita_growth_pct', ascending=False)

    return result_df