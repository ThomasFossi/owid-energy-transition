"""
Scenario modeling module for energy transitions.
This module implements Business-As-Usual, Accelerated Policy, and COP30 Belém 1.5°C (Tripling) projections.
"""

import numpy as np
import pandas as pd

def run_cop30_forecasts(analysis_df: pd.DataFrame) -> pd.DataFrame:
    """
    Runs parametric grid and access forecasts through 2035 across three distinct scenarios:
    1. Business-As-Usual (BAU)
    2. Accelerated Policy
    3. COP30 Belém 1.5°C (Tripling Renewables + Baku-to-Belém 1.3T Finance)
    """
    target_isos = ['CMR', 'KEN', 'DEU']
    hist_window = analysis_df[
        (analysis_df['iso_code'].isin(target_isos)) & 
        (analysis_df['year'].between(2010, 2022))
    ].copy()

    forecast_years = np.arange(2023, 2036)
    forecast_records = []

    # COP30 Axis 1 Mandate: Tripling renewables from 2022 to 2030 => (3.0 ** (1/8)) - 1 = ~14.72% CAGR
    cop30_ren_cagr = (3.0 ** (1 / 8)) - 1

    for iso in target_isos:
        sub = hist_window[hist_window['iso_code'] == iso].sort_values('year')
        country_name = sub['country'].iloc[0]
        
        # Extract 2022 baseline anchor values
        base_2022 = sub[sub['year'] == 2022].iloc[0]
        pop_2022 = base_2022['population']
        ren_2022 = base_2022['renewables_electricity']
        fos_2022 = base_2022['fossil_electricity']
        nuc_2022 = base_2022['nuclear_electricity']
        ci_2022  = base_2022['carbon_intensity_elec']

        # Computing historical demographic CAGR (Compound Annual Growth Rate) & OLS linear generation slopes (TWh/yr)
        n_yrs = 2022 - 2010
        pop_cagr = (pop_2022 / sub[sub['year'] == 2010]['population'].iloc[0]) ** (1 / n_yrs) - 1
        ren_slope = np.polyfit(sub['year'], sub['renewables_electricity'], 1)[0]
        fos_slope = np.polyfit(sub['year'], sub['fossil_electricity'], 1)[0]
        
        # Derived implied fossil emission factor (gCO2/kWh) from 2022 baseline
        total_2022 = ren_2022 + fos_2022 + nuc_2022
        implied_fossil_ef = max((ci_2022 * total_2022) / max(fos_2022, 0.01), 550.0)
        
        for yr in forecast_years:
            years_elapsed = yr - 2022
            proj_pop = pop_2022 * ((1 + pop_cagr) ** years_elapsed)
            
            # ---------------- 1. Business-As-Usual (BAU) ----------------
            bau_ren = max(0.0, ren_2022 + ren_slope * years_elapsed)
            bau_fos = max(0.0, fos_2022 + fos_slope * years_elapsed)
            bau_nuc = 0.0 if iso == 'DEU' else nuc_2022
            
            # ---------------- 2. Moderate Accelerated Policy ----------------
            if iso in ['CMR', 'KEN']:
                acc_ren = ren_2022 * ((1 + 0.08) ** years_elapsed)
                acc_fos = fos_2022 * ((1 - 0.02) ** years_elapsed)
            else:
                acc_ren = ren_2022 + (ren_slope * 1.5) * years_elapsed
                acc_fos = fos_2022 * ((1 - 0.10) ** years_elapsed)
            acc_nuc = 0.0
            
            # ---------------- 3. COP30 Belém 1.5°C Mission ----------------
            if iso in ['CMR', 'KEN']:
                cop_ren = ren_2022 * ((1 + cop30_ren_cagr) ** years_elapsed)
                cop_fos = fos_2022 * ((1 - 0.08) ** years_elapsed)
            else:
                if yr <= 2030:
                    cop_ren = ren_2022 * ((1 + cop30_ren_cagr) ** years_elapsed)
                else:
                    ren_2030 = ren_2022 * 3.0
                    cop_ren = ren_2030 * ((1 + 0.07) ** (yr - 2030))
                cop_fos = fos_2022 * ((1 - 0.18) ** years_elapsed)
            cop_nuc = 0.0

            scenarios = [
                ('BAU', bau_ren, bau_fos, bau_nuc),
                ('Accelerated Policy', acc_ren, acc_fos, acc_nuc),
                ('COP30 Belém 1.5°C', cop_ren, cop_fos, cop_nuc)
            ]
            
            for scen_name, r_val, f_val, n_val in scenarios:
                tot_val = r_val + f_val + n_val
                per_cap = (tot_val * 1e9) / proj_pop
                ci_val = ((f_val * implied_fossil_ef) + (r_val * 20.0)) / tot_val
                ren_share = (r_val / tot_val) * 100
                
                forecast_records.append({
                    'country': country_name, 'iso_code': iso, 'year': yr, 'scenario': scen_name,
                    'renewables_twh': r_val, 'fossil_twh': f_val, 'total_twh': tot_val,
                    'renewable_share_pct': ren_share, 'per_capita_kwh': per_cap, 'carbon_intensity': ci_val
                })

    return pd.DataFrame(forecast_records)