# Global Energy Transition & COP30 Predictive Analytics

**Author:** Pascal Thomas Fossi Tambo ([GitHub Profile](https://github.com/ThomasFossi))  
**Repository:** [owid-energy-transition](https://github.com/ThomasFossi/owid-energy-transition)

---

## 1. Problem Statement & Engineering Relevance
While industrializing and developing economies require massive expansions in electricity access to eradicate energy poverty, high population growth rates can dilute gross generation gains (meaning that, renewable capacity additions are absorbed simply maintaining per-capita supply for new citizens rather than raising living standards). This project analyzes 30+ years of macro-energy and power grid data across an 8-country cohort (**CMR, EGY, KEN, ZAF, DEU, FRA, CHN, USA**), evaluating historical trajectories against UNFCCC COP30 (Belém 2025) decarbonization and tripling mandates through 2035.

---

## 2. Three Key Findings
1. **The Clean Poverty Paradox:** Sub-Saharan grids like Kenya (`KEN`) and Cameroon (`CMR`) operate with low carbon intensities ($\sim 110\text{--}280\text{ gCO}_2/\text{kWh}$) compared to industrial economies, yet suffer a 40-to-50x deficit in per-capita electricity supply ($\sim 238\text{--}294\text{ kWh/person}$). [View Trilemma Matrix](figures/energy_matrix_intensity_vs_access.png)
2. **The Demographic Dilution Effect:** In Cameroon (`CMR`), gross electricity generation expanded by $+136.23\%$ between 2000 and 202, but because population grew by $+85.30\%$, net per-capita access grew by only $+27.49\%$. More than 80% of gross generation growth was absorbed by population expansion. [View Dilution Analysis](figures/access_growth_dilution_analysis.png)
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
  $$\varepsilon_{\text{access}} = \frac{\%\Delta \text{ Per-Capita Electricity}}{\%\Delta \text{ Renewable Generation Generation}}$$
  *Note: $\varepsilon_{\text{access}}$ is a descriptive scaling indicator, not a causal elasticity.*

---

## 5. Historical Validation & Limitations
* **Energy Balance Verification:** Automated unit tests (`pytest`) verify that fuel shares remain bounded between $0\%$ and $100\%$ and that historical calculations match multi-agency benchmarks.
* **Limitations:** Historical carbon intensity metrics rely on country-reported thermal efficiency averages. Baseline fossil emission factors are reverse-engineered from 2022 anchors and held constant across future projections.

---

## 6. Scenario Results, Uncertainty & Engineering Implications
* **Business-As-Usual (BAU):** Extrapolates historical 2010–2022 Ordinary Least Squares (OLS) trends. Results in stagnation or regression of per-capita access in developing regions.
* **Accelerated Policy:** Models moderate policy interventions (e.g., $8\%$ renewable CAGR for Sub-Saharan grids).
* **COP30 Belém 1.5°C Mission:** Enforces the UNFCCC renewable tripling mandate ($14.72\%$ CAGR to 2030) and an orderly fossil phase-out ($\mathbf{-8\%/\text{yr}}$ in emerging grids, $\mathbf{-18\%/\text{yr}}$ in industrialized thermal grids).

---

## 7. Installation & Reproduction Instructions
Clone the repository, create a virtual environment, install the package in editable mode, and execute the pipeline:

```bash
# Clone repository
git clone [https://github.com/ThomasFossi/owid-energy-transition.git](https://github.com/ThomasFossi/owid-energy-transition.git)
cd owid-energy-transition

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Run automated test suite
pytest

```
## 8. Roadmap & Contact
* **Interactive Dashboard:** Streamlit web application currently in development (`app/dashboard.py` — **Coming Soon**).
* **Future Roadmap:** Implementation of seasonal hydro/solar dispatch simulations for African river basins to model hydrological volatility.
* **Contact:** Pascal Thomas Fossi Tambo — [GitHub Issues](https://github.com/ThomasFossi/owid-energy-transition/issues)