# Global Energy Transition & COP30 Predictive Analytics

**Author:** Pascal Thomas Fossi Tambo ([GitHub Profile](https://github.com/ThomasFossi))  
**Repository:** [owid-energy-transition](https://github.com/ThomasFossi/owid-energy-transition)

---

## 1. Problem Statement & Engineering Relevance
While industrializing and developing economies require massive expansions in electricity access to eradicate energy poverty, high population growth rates can dilute gross generation gains (meaning that, renewable capacity additions are absorbed simply maintaining per-capita supply for new citizens rather than raising living standards). This project analyzes 30+ years of macro-energy and power grid data across an 8-country cohort (**CMR, EGY, KEN, ZAF, DEU, FRA, CHN, USA**), evaluating historical trajectories against the global renewable-capacity tripling target established in the COP28 UAE Consensus (First Global Stocktake) and subsequent implementation pathways through COP30 (Belém)..

---

## 2. Three Key Findings
1. **The Clean Poverty Paradox:** Sub-Saharan grids like Kenya (`KEN`) and Cameroon (`CMR`) operate with low carbon intensities ($\sim 110\text{--}280\text{ gCO}_2/\text{kWh}$) compared to industrial economies, yet suffer a 40-to-50x deficit in per-capita electricity supply ($\sim 238\text{--}294\text{ kWh/person}$). [View Trilemma Matrix](figures/energy_matrix_intensity_vs_access.png)
2. **The Demographic Dilution Effect:** In Cameroon (`CMR`), gross electricity generation expanded by $+136.23\%$ between 2000 and 2022, but because population grew by $+85.30\%$, net per-capita access grew by only $+27.49\%$. More than 80% of gross generation growth was absorbed by population expansion. [View Dilution Analysis](figures/access_growth_dilution_analysis.png)
3. **COP30 Belém 1.5°C Leverage:** Modeling the COP30 Axis 1 renewable tripling mandate ($14.72\%$ CAGR through 2030) alongside the Baku-to-Belém USD $1.3\text{T}$ finance roadmap projects per-capita access scaling to $\sim 813\text{--}945\text{ kWh}$ by 2035 while driving grid carbon intensity below $45\text{ gCO}_2/\text{kWh}$. [View Scenario Fan Charts](figures/cop30_scenario_projections_2035.png)

---

## 3. Data Sources, Coverage & Licence
* **Primary Dataset:** Our World in Data (OWID) Energy Database (compiled from Ember, Energy Institute Statistical Review of World Economics, and UN population revisions).
* **Coverage:** 8 sovereign national entities (`CMR`, `EGY`, `KEN`, `ZAF`, `DEU`, `FRA`, `CHN`, `USA`) over the historical window `1990–2024`.
* **Licence:** MIT Open-Source Licence. Raw data files are excluded via `.gitignore` and retrieved locally from `data/raw/`.

---

## 4. Methodology, Equations & Explicit Assumptions
* **Data Hygiene & Imputation:** Emerging technologies (solar, wind) prior to utility deployment are imputed as strict physical zeros ($0.0\text{ TWh}$), reflecting actual technological absence rather than missing records. Legacy base fuels utilize segmented interior linear interpolation capped at $\le 2$ consecutive years with no boundary extrapolation.
* **Demographic Dilution Identity:**
  $$1 + g_{\text{pc}} = \frac{1 + g_{\text{generation}}}{1 + g_{\text{population}}}$$
* **Descriptive Access Elasticity ($\varepsilon_{\text{access}}$):**
  $$\varepsilon_{\text{access}} = \frac{\%\Delta \text{ Per-Capita Electricity}}{\%\Delta \text{ Renewable Generation}}$$
  *Note: $\varepsilon_{\text{access}}$ is a descriptive scaling indicator, not a causal elasticity.*
* **Top-Down Global Ambition vs. Sovereign NDCs:** The $14.72\%$ annual renewable growth rate is derived mathematically from the global tripling target established under the COP28 UAE Consensus ($3^{1/8} - 1$). Applying this rate to individual countries in the COP30 scenario is an **illustrative modeling assumption** to test local infrastructure requirements under a global benchmark, not an official country-specific NDC commitment.
### Data Dictionary & Variable Definitions

| Variable Name | Type | Units | Description & Meaning | Treatment & Cleaning Notes |
| :--- | :--- | :--- | :--- | :--- |
| `electricity_generation` | Raw (OWID) | Terawatt-hours (TWh) | Total gross annual electricity generation from all power sources. | Imputed zeros for missing historical early-year entries where technology was absent. |
| `renewables_electricity` | Raw (OWID) | Terawatt-hours (TWh) | Electricity generation from solar, wind, hydro, geothermal, and biomass. | Strictly zero-imputed prior to utility commercialization. |
| `fossil_electricity` | Raw (OWID) | Terawatt-hours (TWh) | Combined generation from coal, oil, and natural gas thermal power plants. | Segmented linear interpolation capped at $\le 2$ consecutive missing years. |
| `population` | Raw (OWID) | Persons | Total mid-year sovereign population estimate (UN revisions). | Used as the denominator for demographic dilution and per-capita scaling. |
| `per_capita_electricity` | Derived | kWh / person | Annual electricity generation normalized by total national population. | Calculated as: $\frac{\text{electricity\_generation} \times 10^9}{\text{population}}$ |
| `carbon_intensity_elec` | Raw (OWID) | $\text{gCO}_2 / \text{kWh}$ | Average lifecycle greenhouse gas emissions per unit of electricity generated. | Derived from thermal efficiencies and fuel carbon coefficients. |
| `elasticity_eps` ($\varepsilon$) | Derived | Dimensionless | Access Elasticity: ratio of per-capita access growth to renewable generation growth. | Used to classify countries into substitution, dilution, or leverage regimes. |

---

## 5. Historical Validation & Limitations
* **Energy Balance & Scenario Verification:** Automated unit tests (`pytest`) verify that fuel shares remain bounded between $0\%$ and $100\%$ and that historical calculations match multi-agency benchmarks.
* **Parameterized Scenario & Policy Testing:** The test suite independently validates every projection scenario (`BAU`, `Accelerated Policy`, `COP30 Belém 1.5°C`) across all physical bounds, and asserts that policy mandates achieve higher renewable generation and lower carbon intensity than Business-As-Usual by 2035.
* **Limitations:** Historical carbon intensity metrics rely on country-reported thermal efficiency averages. Baseline fossil emission factors are reverse-engineered from 2022 anchors and held constant across future projections.

---

## 6. Scenario Results, Uncertainty & Engineering Implications
* **Business-As-Usual (BAU):** Extrapolates historical 2010–2022 Ordinary Least Squares (OLS) trends. Results in stagnation or regression of per-capita access in developing regions.
* **Accelerated Policy:** Models moderate policy interventions (e.g., $8\%$ renewable CAGR for Sub-Saharan grids).
* **COP30 Belém 1.5°C Scenario (Modelling Benchmark):** Applies the global $14.72\%$ renewable expansion CAGR as a top-down stress test through 2030 alongside the Baku-to-Belém finance roadmap. This evaluates the physical generation scaling required in developing (CMR, KEN) and industrialized (DEU) grids to meet global climate benchmarks, while explicitly noting that national deployment rates will be governed by sovereign policy constraints and local financing availability.

### Scenario Sensitivity & Robustness Validation
To ensure model resilience against varying policy assumptions, we performed a parameter sweep varying the **Renewable Expansion CAGR (`g_ren`)** between 10.0% and 20.0% alongside **Fossil Phase-Down Rates (`d_fos`)** between -5%/yr and -18%/yr through 2030:

* **Fossil Dominance on Grid Intensity:** Sensitivity sweeps reveal that grid decarbonization speed is significantly more sensitive to the **fossil phase-down rate** than variations in renewable CAGR. Even with aggressive renewable scale-up (20%), if thermal generation declines slowly (-5%/yr), grid carbon intensity floors remain elevated due to residual baseline emissions.
* **Internal Conservation Consistency:** All scenario records maintain strict physical bounds ($\ge 0$ generation and emissions), with per-capita access scaling dynamically against population compound growth rates.

### Formal Scenario Mathematical Formulations
Projections through 2035 are computed using parametric growth equations anchored to 2022 sovereign baselines ($t_0 = 2022$). For each forecast year index $t$ (where $t = \text{Year} - 2022$), the scenarios are defined as follows:

1. **Business-As-Usual (BAU):**
   Extrapolates historical Ordinary Least Squares (OLS) trends ($r_{\text{slope}}, f_{\text{slope}}$) evaluated over the 2010–2022 window:
   $$\text{Ren}_{\text{BAU}}(t) = \max\left(0, \text{Ren}_{0} + r_{\text{slope}} \cdot t\right)$$
   $$\text{Fos}_{\text{BAU}}(t) = \max\left(0, \text{Fos}_{0} + f_{\text{slope}} \cdot t\right)$$

2. **Accelerated Policy:**
   Applies moderate structural policy interventions. For emerging economies (`CMR`, `KEN`), renewables scale at an $8\%$ annual compound growth rate while fossil fuels decline by $2\%/\text{yr}$:
   $$\text{Ren}_{\text{Acc}}(t) = \text{Ren}_{0} \cdot (1 + 0.08)^t, \quad \text{Fos}_{\text{Acc}}(t) = \text{Fos}_{0} \cdot (1 - 0.02)^t$$

3. **COP30 Belém 1.5°C Mission (Modelling Benchmark):**
   Enforces the global renewable tripling target established in the **COP28 UAE Consensus** ($3$x growth over 8 years, translating to an annual CAGR of $g_{\text{ren}} = 3^{1/8} - 1 \approx 14.72\%$) through 2030, paired with accelerated fossil phase-out rates ($d_{\text{fos}}$):
   $$\text{Ren}_{\text{COP30}}(t) = \text{Ren}_{0} \cdot (1 + 0.1472)^t \quad (\text{for } t \le 8)$$
   $$\text{Fos}_{\text{COP30}}(t) = \text{Fos}_{0} \cdot (1 - d_{\text{fos}})^t$$
   *(Where $d_{\text{fos}} = 0.08/\text{yr}$ for emerging grids and $0.18/\text{yr}$ for industrialized thermal grids).*
   
---

## 7. Installation & Reproduction Instructions
Clone the repository, create a virtual environment, install the package in editable mode, and execute the pipeline:

# Clone repository
git clone https://github.com/ThomasFossi/owid-energy-transition.git
cd owid-energy-transition

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Run automated test suite
pytest


## 8. Roadmap & Contact
* **Interactive Dashboard:** Streamlit web application currently in development (`app/dashboard.py` — **Coming Soon**).
* **Future Roadmap:** Implementation of seasonal hydro/solar dispatch simulations for African river basins to model hydrological volatility.
* **Contact:** Pascal Thomas Fossi Tambo — [GitHub Issues](https://github.com/ThomasFossi/owid-energy-transition/issues)