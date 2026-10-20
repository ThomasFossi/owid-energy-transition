"""
Plotting module for global energy transitions.
This module handles visualization generation for benchmarks, demographic dilution, and scenario projections.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Consistent color mapping across all project visualizations
PALETTE_MAP = {
    'CMR': '#2ca02c', 'KEN': '#ff7f0e', 'EGY': '#d62728', 'ZAF': '#9467bd',
    'DEU': '#1f77b4', 'FRA': '#17becf', 'CHN': '#e377c2', 'USA': '#333333'
}

def plot_energy_trilemma(bench_df: pd.DataFrame, save_path: str = "figures/energy_matrix_intensity_vs_access.png"):
    """
    Generates the Energy Trilemma bubble matrix comparing per-capita electricity access 
    against grid carbon intensity, with bubble sizing mapped to renewable share %.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xscale('log')
    
    for _, row in bench_df.iterrows():
        iso = row['iso_code']
        ax.scatter(
            row['per_capita_elec_kwh'], row['carbon_intensity_elec'],
            s=row['renewable_share_pct'] * 9 + 70,
            color=PALETTE_MAP.get(iso, '#333333'), alpha=0.85, edgecolors='black', lw=1.5
        )
        ax.annotate(
            f"{row['country']} ({iso})\n{row['renewable_share_pct']:.1f}% Ren",
            xy=(row['per_capita_elec_kwh'], row['carbon_intensity_elec']),
            xytext=(8, 6), textcoords='offset points', fontsize=9, fontweight='bold'
        )
        
    ax.set_xlabel("Per-Capita Electricity Generation (kWh / person) [Log Scale]", fontsize=11, fontweight='bold')
    ax.set_ylabel("Grid Carbon Intensity (gCO2 / kWh)", fontsize=11, fontweight='bold')
    ax.set_title("The Energy Trilemma: Carbon Intensity vs. Access (2022 Authoritative Benchmark)", fontsize=13, fontweight='bold')
    ax.grid(True, which="both", linestyle='--', alpha=0.5)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved Energy Trilemma figure to {save_path}")


def plot_scenario_projections(analysis_df: pd.DataFrame, forecast_df: pd.DataFrame, save_path: str = "figures/cop30_scenario_projections_2035.png"):
    """
    Generates the 2x3 multi-scenario projection fan chart comparing historical records (2000-2022) 
    against future pathways through 2035 for Cameroon, Kenya, and Germany.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    target_isos = ['CMR', 'KEN', 'DEU']
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10), sharex=True)
    fig.subplots_adjust(hspace=0.28, wspace=0.22)

    scen_styles = {
        'BAU': {'color': '#7f7f7f', 'ls': '--', 'lw': 2.0, 'label': 'Business-As-Usual (BAU)'},
        'Accelerated Policy': {'color': '#1f77b4', 'ls': '-.', 'lw': 2.2, 'label': 'Accelerated Policy'},
        'COP30 Belém 1.5°C': {'color': '#2ca02c', 'ls': '-', 'lw': 2.8, 'label': 'COP30 Belém 1.5°C (Tripling)'}
    }

    for col_idx, iso in enumerate(target_isos):
        hist_sub = analysis_df[
            (analysis_df['iso_code'] == iso) & (analysis_df['year'].between(2000, 2022))
        ].sort_values('year')
        
        country_name = hist_sub['country'].iloc[0]
        last_per_cap = hist_sub[hist_sub['year'] == 2022]['per_capita_electricity'].iloc[0]
        last_ci = hist_sub[hist_sub['year'] == 2022]['carbon_intensity_elec'].iloc[0]
        
        ax_top, ax_bot = axes[0, col_idx], axes[1, col_idx]
        
        # Plotting historical records
        ax_top.plot(hist_sub['year'], hist_sub['per_capita_electricity'], color='#111111', lw=2.5, label='Historical (2000–2022)')
        ax_bot.plot(hist_sub['year'], hist_sub['carbon_intensity_elec'], color='#111111', lw=2.5, label='Historical (2000–2022)')
        
        # Stitching 2022 anchor point to 2023-2035 forecast arrays via np.insert
        for scen_name, style in scen_styles.items():
            f_sub = forecast_df[(forecast_df['iso_code'] == iso) & (forecast_df['scenario'] == scen_name)].sort_values('year')
            
            yrs_stitched = np.insert(f_sub['year'].values, 0, 2022)
            per_cap_stitched = np.insert(f_sub['per_capita_kwh'].values, 0, last_per_cap)
            ci_stitched = np.insert(f_sub['carbon_intensity'].values, 0, last_ci)
            
            ax_top.plot(yrs_stitched, per_cap_stitched, color=style['color'], linestyle=style['ls'], lw=style['lw'], label=style['label'])
            ax_bot.plot(yrs_stitched, ci_stitched, color=style['color'], linestyle=style['ls'], lw=style['lw'], label=style['label'])
        
        for ax in [ax_top, ax_bot]:
            ax.axvline(2022, color='#444444', linestyle=':', lw=1.2, alpha=0.8)
            ax.axvline(2030, color='#d62728', linestyle=':', lw=1.2, alpha=0.7)
            ax.axvspan(2022, 2035, color='#f0f4f8', alpha=0.5, zorder=0)
            ax.grid(True, linestyle='--', alpha=0.4)
            
        ax_top.set_title(f"{country_name} ({iso})\nPer-Capita Electricity Access", fontsize=12, fontweight='bold')
        if col_idx == 0:
            ax_top.set_ylabel("Per-Capita Electricity (kWh / person)", fontsize=11, fontweight='bold')

        ax_bot.set_title(f"{country_name} ({iso}) — Grid Decarbonization", fontsize=11, fontweight='bold')
        ax_bot.set_xlabel("Year", fontsize=11, fontweight='bold')
        if col_idx == 0:
            ax_bot.set_ylabel("Carbon Intensity (gCO2 / kWh)", fontsize=11, fontweight='bold')

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=4, frameon=True, fontsize=10.5)
    fig.suptitle("Historical & Projected Power Grid Trajectories (2000–2035): BAU vs. COP30 Belém 1.5°C Mandate", fontsize=14, fontweight='bold', y=1.03)

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved scenario projections figure to {save_path}")