# Global Energy Transition & Decarbonization Analytics

An empirical analysis of macro-energy transition pathways, power sector decarbonization, and electricity access elasticity across global and African economies using the Our World in Data (OWID) World Energy Dataset.

---

## 1. Executive Summary & Core Findings

This project investigates the divergence between macro primary energy consumption and power grid decarbonization from 1990 to 2024, focusing on an expanded 8-country comparative cohort: **Cameroon (`CMR`)**, **Egypt (`EGY`)**, **Kenya (`KEN`)**, **South Africa (`ZAF`)**, **Germany (`DEU`)**, **France (`FRA`)**, **China (`CHN`)**, and the **United States (`USA`)**.

### Key Empirical Takeaways:
1. **Primary vs. Power Decarbonization:** High renewable penetration on electricity grids (e.g., Germany >44%, Kenya >87%) often masks persistent primary fossil dependency (transportation, industrial heat, chemicals), where fossil fuels still account for over 75% of primary consumption in several advanced economies.
2. **The Demographic Dilution Effect:** In emerging economies, gross generation additions do not translate directly into per-capita access. In Cameroon, a **+136.2%** increase in gross power generation between 2000 and 2022 was heavily absorbed by an **+85.3%** population surge, yielding only a **+27.5%** net gain in per-capita electricity.
3. **Transition Regimes & Elasticity ($\varepsilon$):**
   * **Substitution / Decoupling ($\varepsilon < 0$):** Industrialized nations (USA, DEU, FRA) deploy renewables to displace existing thermal/nuclear baseload while per-capita power consumption contracts due to structural efficiency.
   * **Demographically Diluted Expansion ($0 < \varepsilon < 1$):** Sub-Saharan economies (CMR, KEN) expand renewable supply, but rapid demographic growth requires higher capacity factors to achieve per-capita equity.
   * **High Expansion Leverage ($\varepsilon > 1$):** Regimes (EGY) where centralized grid expansion outpaces demographic trends.

---

## 2. Project Architecture

```text
owid-energy-transition/
├── data/
│   ├── owid-energy-data.csv                    # Raw dataset (excluded via .gitignore)
│   ├── processed_transition_benchmark_2022.csv # Cross-sectional intensity table
│   └── processed_growth_elasticity_2000_2022.csv
├── figures/
│   ├── global_and_african_power_transition.png # Multi-panel generation trajectory
│   ├── energy_matrix_intensity_vs_access.png   # Bubble chart (gCO2/kWh vs. kWh/person)
│   └── access_growth_dilution_analysis.png     # Parity & demographic dilution plots
├── notebooks/
│   └── 01_global_energy_transition.ipynb       # End-to-end analytical pipeline
├── src/                                        # Modular scripts
├── .gitignore
└── README.md
---

## 3. Data Hygiene & Methodological Framework

* **Entity Isolation:** Separated sovereign nations (`iso_code.notna()`) from regional aggregates (e.g., `ASEAN`, `World`, `Africa (EI)`) to prevent double-counting.
* **Structural Zero Imputation:** Missing values for non-existent or emerging technologies (solar, wind, nuclear prior to utility deployment) were imputed as physical zeros (`0.0`) rather than interpolated.
* **Segmented Interior Interpolation:** Linear interpolation was restricted strictly to internal census gaps ($\le 2$ consecutive years) for legacy base fuels (coal, oil, gas, hydro) without boundary extrapolation.
* **Authoritative 2022 Benchmark:** Selected 2022 as the reference year to ensure 100% data completeness across multi-agency census reporting lags for lifecycle carbon intensity ($\text{gCO}_2/\text{kWh}$) and population metrics.

---

## 4. Benchmark Snapshot (2022)

| Country | ISO | Per-Capita Elec (kWh) | Grid Carbon Intensity ($\text{gCO}_2$/kWh) | Renewable Share (%) | Fossil Share (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **France** | `FRA` | 7,068.02 | 78.54 | 24.20 | 12.88 |
| **Kenya** | `KEN` | 238.88 | 109.57 | 87.81 | 12.19 |
| **Cameroon** | `CMR` | 294.94 | 280.98 | 64.91 | 35.09 |
| **United States** | `USA` | 12,551.87 | 410.39 | 22.35 | 59.65 |
| **Germany** | `DEU` | 6,741.65 | 419.74 | 44.37 | 49.50 |
| **Egypt** | `EGY` | 1,924.38 | 570.04 | 11.82 | 88.18 |
| **China** | `CHN` | 6,208.84 | 586.75 | 30.18 | 65.10 |
| **South Africa** | `ZAF` | 3,834.18 | 729.02 | 9.88 | 85.90 |

---

## 5. Setup & Reproduction

```bash
# Clone the repository
git clone <remote-url>
cd owid-energy-transition

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download dataset
curl -L -o data/owid-energy-data.csv [https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv](https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv)

# Execute notebook
jupyter notebook notebooks/01_global_energy_transition.ipynb