# Data Sources & Provenance

## 1. Data Origin & Provenance
The empirical foundation of this project is the **Our World in Data (OWID) Energy Database**, which aggregates and harmonizes records from:
* **Ember:** Global electricity data, power sector transitions, and clean energy generation.
* **Energy Institute Statistical Review of World Economics:** Historical fossil fuel consumption and primary energy mixes.
* **United Nations (UN) Population Divisions:** Annual demographic revisions used for per-capita normalization and dilution modeling.

---

## 2. Fundamental Physical Distinctions: Capacity vs. Generation vs. Intensity
Through out this modeling project and as we came to find out to be a general point of oversight in energy systems modelling, confusing capacity, generation, and emissions intensity is a fundamental error. This repository strictly distinguishes between these three distinct physical dimensions:

* **Installed Capacity ($P_{\text{cap}}$, Units: MW or GW):**
  * *Definition:* The maximum possible instantaneous power output rating of power plants installed within a sovereign grid. 
  * *Role:* Represents infrastructure capital stock and potential ceiling, but does *not* equal energy produced.
* **Energy Generation ($E$, Units: MWh or TWh over a specified period):**
  * *Definition:* The cumulative electrical energy integrated over a temporal duration (typically 1 calendar year, $8,760\text{ hours}$):
    $$E = \int_{0}^{8760} P(t) \, dt$$
  * *Relationship to Capacity:* Connected via the **Capacity Factor ($CF$)**:
    $$\text{Annual Energy (MWh)} = \text{Capacity (MW)} \times 8,760\text{ hours} \times CF$$
  * *Role:* Used as the primary mass-balance metric in our generation and demographic dilution models.
* **Emissions Intensity ($CI$, Units: $\text{gCO}_2/\text{kWh}$):**
  * *Definition:* The lifecycle or operational greenhouse gas mass emitted per unit of electrical energy delivered to the grid.
  * *Relationship to Total Emissions:* Total annual emissions ($M$, in metric tons or Mt) are computed as:
    $$M = \frac{E_{\text{fossil\_kWh}} \times CI_{\text{fossil}}}{10^6}$$

---

## 3. Variables, Units, and Temporal Resolutions
* **Spatial Coverage:** 8 sovereign national entities (`CMR`, `EGY`, `KEN`, `ZAF`, `DEU`, `FRA`, `CHN`, `USA`).
* **Temporal Resolution:** Annual time-series spanning `1990–2024`.

| Variable Name | Source Key | Units | Temporal Resolution | Physical Description |
| :--- | :--- | :--- | :--- | :--- |
| `electricity_generation` | OWID / Ember | TWh / year | Annual (1990–2024) | Total gross annual electricity generation from all aggregated sources. |
| `renewables_electricity` | OWID / Ember | TWh / year | Annual (1990–2024) | Cumulative generation from solar, wind, hydro, geothermal, and biomass. |
| `fossil_electricity` | OWID / Institute | TWh / year | Annual (1990–2024) | Combined thermal generation from coal, oil, and natural gas combustion. |
| `population` | UN Revisions | Persons | Annual (1990–2024) | Total mid-year sovereign population estimate. |
| `carbon_intensity_elec` | OWID / Ember | $\text{gCO}_2/\text{kWh}$ | Annual (1990–2024) | Carbon dioxide emissions per kilowatt-hour of electricity generated. |

---

## 4. Handling Missing or Anomalous Values
To prevent data contamination prior to model ingestion (`src/energy_transition/data.py`), missing values undergo strict cleaning:
* **Zero-Imputation for Emerging Tech:** Solar and wind generation entries prior to utility-scale deployment are imputed as strict physical zeros ($0.0\text{ TWh}$), reflecting actual technological absence rather than missing data records.
* **Interior Linear Interpolation:** Legacy fossil and hydro time-series utilize segmented interior linear interpolation strictly capped at $\le 2$ consecutive missing years. Boundary extrapolation (filling missing values at start/end edges) is not sound practice and therefore not done in this project.

---

## 5. Pre-Model Transformations
Before entering the metric calculation and scenario forecasting, raw tables undergo:
1. **Entity Filtering:** Isolation of the targeted 8-country comparative cohort.
2. **Per-Capita Normalization:** Scaling total generation against annual population vectors.
3. **Demographic Dilution Indexing:** Calculating annual growth differentials between gross generation and population expansion.