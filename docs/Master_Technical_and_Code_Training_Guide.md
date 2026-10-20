Here is the complete, self-contained **Master Technical & Code Teaching Guide** covering the entire `owid-energy-transition` pipeline from start to finish.

Every phase of the project is broken down line-by-line so you can understand both the **software engineering mechanics** (Pandas vectorization, NumPy regression, Matplotlib architecture, Git version control) and the **physical energy systems rationale** behind every design choice.

---

## Module 1: Environment Architecture & Data Ingestion

### 1.1 Virtual Environment & Dependency Pinning

Before writing analytical code, isolating your Python environment ensures that global system packages on your Linux machine do not conflict with project-specific library versions.

```bash
# Create an isolated virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment in the current bash shell
source venv/bin/activate

# Export exact installed package versions for reproducibility
pip freeze > requirements.txt

```

* **`python3 -m venv venv`:** Invokes Python's built-in `venv` module to create a self-contained directory (`venv/`) containing its own Python binary and `site-packages` folder.
* **`source venv/bin/activate`:** Modifies your shell's `$PATH` environment variable so that running `python` or `pip` points strictly to `/home/ablaze/projects/owid-energy-transition/venv/bin/`.


* **`pip freeze > requirements.txt`:** Queries all currently installed libraries and their exact semantic versions (e.g., `pandas==2.2.2`, `numpy==1.26.4`) and redirects (`>`) the standard output into a text file. Anyone cloning your repository (`[https://github.com/ThomasFossi/owid-energy-transition](https://github.com/ThomasFossi/owid-energy-transition)`) can run `pip install -r requirements.txt` to recreate the exact mathematical environment.



---

### 1.2 Library Imports & Dataset Loading

```python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load raw Our World in Data (OWID) Energy dataset
data_path = os.path.join('..', 'data', 'owid-energy-data.csv')
raw_df = pd.read_csv(data_path)

```

* **`os.path.join('..', 'data', 'owid-energy-data.csv')`:** Because your Jupyter notebook lives inside `notebooks/01_global_energy_transition.ipynb`, `'..'` instructs the operating system to move **up one parent directory** to the project root (`owid-energy-transition/`), then step into `data/`. Using `os.path.join()` instead of hardcoded slashes (`'../data/...'`) guarantees the script works across Linux, macOS, and Windows.



---

## Module 2: Physics-Based Data Hygiene & Imputation

Raw global energy datasets suffer from two major structural traps: **regional double-counting** and **false missingness (`NaN`)**. Here is how our pipeline solves both:

### 2.1 Sovereign Entity Isolation & Cohort Filtering

```python
# 1. Isolate sovereign nations from regional/continental aggregates
sovereign_df = raw_df[raw_df['iso_code'].notna()].copy()

# 2. Define the 8-country comparative cohort and time window (1990 - 2024)
cohort_isos = ['CMR', 'EGY', 'KEN', 'ZAF', 'DEU', 'FRA', 'CHN', 'USA']
analysis_df = sovereign_df[
    (sovereign_df['iso_code'].isin(cohort_isos)) &
    (sovereign_df['year'].between(1990, 2024))
].sort_values(['iso_code', 'year']).reset_index(drop=True)

```

* **`raw_df['iso_code'].notna()`:** In the OWID dataset, rows like `World`, `Africa (EI)`, `OECD`, and `ASEAN` are included alongside individual countries. However, OWID leaves the 3-letter ISO-3166 alpha-3 code (`iso_code`) blank (`NaN`) for regional aggregates (except `OWID_WRL`). Filtering with `.notna()` strips out continental aggregates so they never skew statistical distributions.
* **`.copy()`:** When you filter a Pandas DataFrame (`raw_df[...]`), Pandas often returns a *view* (a memory pointer to the original table) rather than an independent object. Calling `.copy()` allocates a fresh block in RAM, preventing the notorious `SettingWithCopyWarning` when we modify columns later.
* **`.isin(cohort_isos)` & `.between(1990, 2024)`:** Vectorized boolean masks that evaluate in C-speed across tens of thousands of rows simultaneously without slow Python `for` loops.
* **`.sort_values(['iso_code', 'year']).reset_index(drop=True)`:** Sorting chronologically within each country is **mandatory** before performing any time-series interpolation or rolling window math. `reset_index(drop=True)` discards the scrambled original row numbers and creates a clean `0, 1, 2, ... N` index.

---

### 2.2 Structural Zero Imputation vs. Segmented Interior Interpolation

```python
# Emerging technologies: Missing values prior to utility deployment are physical zeros (0.0)
emerging_tech_cols = [
    'solar_electricity', 'wind_electricity', 'nuclear_electricity',
    'other_renewable_electricity', 'biofuel_electricity'
]
analysis_df[emerging_tech_cols] = analysis_df[emerging_tech_cols].fillna(0.0)

# Legacy base fuels: Interpolate strictly internal census gaps (<= 2 years) within each country
legacy_cols = [
    'hydro_electricity', 'coal_electricity', 'gas_electricity', 'oil_electricity',
    'renewables_electricity', 'fossil_electricity', 'electricity_generation',
    'primary_energy_consumption', 'carbon_intensity_elec', 'population'
]

analysis_df[legacy_cols] = (
    analysis_df.groupby('iso_code')[legacy_cols]
    .transform(lambda s: s.interpolate(method='linear', limit=2, limit_area='inside'))
)

```

* **Why `.fillna(0.0)` is used for `emerging_tech_cols`:** If Cameroon or Kenya has `NaN` for `solar_electricity` in 1994, it is not because census officials forgot to measure utility solar farms—it is because utility-scale grid-tied solar PV did not physically exist on that grid in 1994. Imputing `0.0` reflects physical reality.
* **Why `.groupby('iso_code')...transform(...)` is critical for `legacy_cols`:**
* If you ran `analysis_df[legacy_cols].interpolate()` across the whole table *without* `.groupby('iso_code')`, Pandas would interpolate across country boundaries—stitching the end of Cameroon (`2024`) to the beginning of China (`1990`)!
* Grouping by `iso_code` first isolates each country's time series independently.
* **`limit=2`:** Restricts linear interpolation to brief administrative reporting hiccups (maximum 1 or 2 missing years). If a country is missing 10 consecutive years of data, interpolating a straight line across a decade would fabricate history.
* **`limit_area='inside'`:** Strictly forbids **boundary extrapolation**. It will only fill gaps *surrounded* by valid historical measurements (e.g., filling `2014` if `2013` and `2015` exist), and will never project values into `2023–2024` if the agency hasn't reported them yet.



---

## Module 3: Cross-Sectional Benchmarking & The Energy Trilemma (`2022`)

### 3.1 Extracting the 2022 Authoritative Benchmark

```python
# Select 2022 as the authoritative multi-agency benchmark year
bench_2022 = analysis_df[analysis_df['year'] == 2022].copy()

# Derive Per-Capita Electricity (kWh/person) and Fuel Shares (%) if not pre-populated
bench_2022['per_capita_elec_kwh'] = (bench_2022['electricity_generation'] * 1e9) / bench_2022['population']
bench_2022['renewable_share_pct'] = (bench_2022['renewables_electricity'] / bench_2022['electricity_generation']) * 100
bench_2022['fossil_share_pct']    = (bench_2022['fossil_electricity'] / bench_2022['electricity_generation']) * 100

# Sort by Grid Carbon Intensity (cleanest to most carbon-intensive)
bench_table = bench_2022[[
    'country', 'iso_code', 'per_capita_elec_kwh', 
    'carbon_intensity_elec', 'renewable_share_pct', 'fossil_share_pct'
]].sort_values('carbon_intensity_elec').round(2)

```

* **Why `2022` instead of `2024`?** While European and North American grids (`DEU`, `FRA`, `USA`) report preliminary generation within months, non-OECD electricity emission factors (`carbon_intensity_elec`) and UN demographic revisions experience a 18–24 month multi-agency verification lag. Choosing `2022` guarantees **100% matrix completeness** across all 8 nations without dropping African benchmarks (`CMR`, `KEN`, `EGY`, `ZAF`).
* **Unit Dimensionality (`* 1e9`):** OWID reports `electricity_generation` in **Terawatt-hours ($\text{TWh}$)**, where $1\text{ TWh} = 10^{12}\text{ Wh} = 10^9\text{ kWh}$. Multiplying by `1e9` before dividing by `population` converts national Terawatt-hours into individual **Kilowatt-hours per person ($\text{kWh/person}$)**.

---

### 3.2 Visualizing the Energy Trilemma Matrix (Bubble Plot)

```python
fig, ax = plt.subplots(figsize=(11, 7))

# Log-scale X-axis to handle the 50x disparity between Kenya (239 kWh) and USA (12,552 kWh)
ax.set_xscale('log')

scatter = ax.scatter(
    x=bench_2022['per_capita_elec_kwh'],
    y=bench_2022['carbon_intensity_elec'],
    s=bench_2022['renewable_share_pct'] * 8 + 60,  # Bubble area scaled by Renewable Share %
    c=bench_2022['iso_code'].map(palette_map),
    alpha=0.85, edgecolors='black', linewidth=1.5
)

```

* **Why `ax.set_xscale('log')` is essential:** In 2022, Kenya consumed $238.88\text{ kWh/person}$ and Cameroon $294.94\text{ kWh/person}$, whereas the United States consumed $12,551.87\text{ kWh/person}$. On a standard linear X-axis, `KEN` and `CMR` would be crushed on top of each other against the left border (`x = 0`), while `USA` sits far to the right. A base-10 logarithmic scale gives equal visual spacing to every order of magnitude ($10^2\text{ kWh}$, $10^3\text{ kWh}$, $10^4\text{ kWh}$), clearly exposing the **"Clean Poverty Paradox"** (where `KEN` and `CMR` have low carbon intensity but severe access deficits).
* **`s=bench_2022['renewable_share_pct'] * 8 + 60`:** Encodes a third analytical dimension into a 2D plot by mapping the marker surface area (`s`) to each grid's renewable electricity share, adding a baseline constant (`+ 60`) so countries with low renewable shares (`ZAF` at $9.88\%$, `EGY` at $11.82\%$) remain clearly visible.

---

## Module 4: Demographic Dilution & Access Elasticity ($\varepsilon$)

### 4.1 Pivoting Longitudinal Endpoints (`2000` vs. `2022`)

```python
# Filter strictly to the 2000 and 2022 endpoints
endpoints = analysis_df[analysis_df['year'].isin([2000, 2022])].copy()

# Pivot table so 2000 and 2022 become side-by-side columns for each metric
pivoted = endpoints.pivot(
    index=['country', 'iso_code'],
    columns='year',
    values=['electricity_generation', 'renewables_electricity', 'population', 'per_capita_electricity']
)

# Compute percentage growth rates (2000 -> 2022)
gen_growth_pct = ((pivoted['electricity_generation'][2022] - pivoted['electricity_generation'][2000]) 
                  / pivoted['electricity_generation'][2000]) * 100

pop_growth_pct = ((pivoted['population'][2022] - pivoted['population'][2000]) 
                  / pivoted['population'][2000]) * 100

pc_growth_pct  = ((pivoted['per_capita_electricity'][2022] - pivoted['per_capita_electricity'][2000]) 
                  / pivoted['per_capita_electricity'][2000]) * 100

ren_growth_pct = ((pivoted['renewables_electricity'][2022] - pivoted['renewables_electricity'][2000]) 
                  / pivoted['renewables_electricity'][2000]) * 100

```

* **How `.pivot()` works:** Instead of writing complex nested loops to subtract a country's 2000 value from its 2022 value, `.pivot()` reshapes the DataFrame into a hierarchical index (MultiIndex) where each metric has two sub-columns: `[2000]` and `[2022]`. This allows you to subtract the entire `2000` column vector from the `2022` column vector in a single line of code.
* **The Mathematical Identity of Demographic Dilution:**
Because $\text{Per-Capita Electricity} = \frac{\text{Gross Generation}}{\text{Population}}$, the growth factor of per-capita electricity over time is governed by the ratio of two growth factors:

$$1 + g_{\text{per-capita}} = \frac{1 + g_{\text{generation}}}{1 + g_{\text{population}}}$$



In **Cameroon (`CMR`)**, gross generation expanded by $g_{\text{generation}} = +136.23\%$ ($2.3623\times$), while population expanded by $g_{\text{population}} = +85.30\%$ ($1.8530\times$):

$$1 + g_{\text{per-capita}} = \frac{2.3623}{1.8530} \approx 1.2749 \implies \mathbf{+27.49\% \text{ net per-capita gain}}$$



This proves why gross megawatt additions alone are a misleading metric in rapidly growing developing nations.

---

### 4.2 Access Elasticity ($\varepsilon_{\text{access}}$) & Regime Classification

```python
# Compute Access Elasticity with respect to Renewable Expansion
elasticity_eps = pc_growth_pct / ren_growth_pct

# Vectorized regime classification using np.select
conditions = [
    elasticity_eps < 0,
    (elasticity_eps >= 0) & (elasticity_eps <= 1.0),
    elasticity_eps > 1.0
]
choices = [
    'Substitution / Decoupling',
    'Demographically Diluted Expansion',
    'High Expansion Leverage'
]
transition_regime = np.select(conditions, choices, default='Unclassified')

```

* **Understanding $\varepsilon_{\text{access}}$:** Borrowed from microeconomic elasticity theory, $\varepsilon_{\text{access}} = \frac{\%\Delta\text{ Per-Capita Electricity}}{\%\Delta\text{ Renewable Generation}}$ measures how many percentage points of individual electricity access a country gains for every $1\%$ increase in renewable generation.
* **Why `np.select(conditions, choices)` is superior to `if/elif/else`:** Standard Python `if/elif` statements cannot evaluate an entire Pandas Series at once without `.apply()`, which is slow. `np.select()` takes a list of boolean masks (`conditions`) and maps them simultaneously to string labels (`choices`):
1. **$\varepsilon < 0$ (`Substitution / Decoupling`):** Seen in `DEU` ($-0.005$), `USA` ($-0.041$), `FRA` ($-0.314$), and `ZAF` ($-0.010$). Renewable generation grew (`ren_growth_pct > 0`), but per-capita electricity contracted (`pc_growth_pct < 0`) due to energy efficiency improvements, industrial offshoring, or grid load-shedding (in South Africa's case).
2. **$0 \le \varepsilon \le 1$ (`Demographically Diluted Expansion`):** Seen in `CMR` ($0.499$), `KEN` ($0.126$), and `CHN` ($0.444$). Both renewables and per-capita access grew, but a $1\%$ surge in renewables yielded less than a $1\%$ gain in per-capita access.
3. **$\varepsilon > 1$ (`High Expansion Leverage`):** Seen in `EGY` ($1.154$), where massive natural gas capacity additions expanded total per-capita supply faster than renewable additions alone.



---

## Module 5: COP30 Belém (`2025`) Scenario Forecasting (`2023–2035`)

### 5.1 Translating Treaty Mandates into Parametric Equations

From the **COP30 Executive Report (Belém, November 2025)**:

1. **Axis 1 Action Agenda (Tripling Renewables by 2030):** Mobilizes a USD $1\text{ trillion}$ investment plan to triple global renewable capacity by 2030, backed by USD $148\text{--}150\text{ billion}$ annually for grids and storage via UNEZA.



$$r_{\text{COP30}} = 3^{(1/8)} - 1 \approx 0.147202 \quad (\mathbf{14.72\% \text{ CAGR}})$$


2. **Baku-to-Belém Roadmap to 1.3T (2035 Horizon):** Mobilizes USD $1.3\text{ trillion}$ annually for developing countries by 2035 alongside the **Global Implementation Accelerator** and **Belém Mission for $1.5^\circ\text{C}$**. In our code, this allows emerging grids (`CMR`, `KEN`) to sustain the $14.72\%$ compound growth rate through 2035 while retiring diesel/heavy-fuel-oil generators at $-8\%/\text{yr}$.


3. **Roadmap for Transitioning Away from Fossil Fuels:** Initiates a just, orderly, and equitable transition away from fossil fuels. In our code, industrialized emitters (`DEU`) triple renewables by 2030 and decay coal/gas generation exponentially at $-18\%/\text{yr}$.



---

### 5.2 Complete Walkthrough of the Forecasting & Stitching Code

```python
# 1. Fit linear historical slope (2010 - 2022) for BAU baseline
ren_slope = np.polyfit(sub['year'], sub['renewables_electricity'], 1)[0]
fos_slope = np.polyfit(sub['year'], sub['fossil_electricity'], 1)[0]

# 2. Compute country-specific implied fossil emission factor (gCO2/kWh)
total_2022 = ren_2022 + fos_2022 + nuc_2022
implied_fossil_ef = max((ci_2022 * total_2022) / max(fos_2022, 0.01), 550.0)

# 3. Dynamic Generation-Weighted Carbon Intensity inside the 2023-2035 loop
ci_val = ((f_val * implied_fossil_ef) + (r_val * 20.0)) / tot_val

# 4. Seamless Array Stitching for Visualization
yrs_stitched = np.insert(f_sub['year'].values, 0, 2022)
per_cap_stitched = np.insert(f_sub['per_capita_kwh'].values, 0, last_per_cap)

```

* **`np.polyfit(x, y, 1)[0]`:** Performs Ordinary Least Squares (OLS) linear regression ($y = m \cdot t + b$) over the `2010–2022` window and returns `[m, b]`. Indexing `[0]` grabs the annual slope $m$ ($\text{TWh/year}$).
* **`implied_fossil_ef`:** Reverse-engineers each country's baseline thermal emission factor from its 2022 grid intensity (`ci_2022`), ensuring Germany's lignite/hard-coal fleet is penalized appropriately compared to gas/oil fleets.
* **`ci_val` Formula:** Assigns a physical lifecycle floor of **$20.0\text{ gCO}_2/\text{kWh}$** to renewable generation (accounting for embodied carbon in solar silicon, wind turbine steel, and hydro civil works) and weights it against residual fossil generation (`f_val * implied_fossil_ef`).
* **`np.insert(..., 0, ...)`:** Prepends the `2022` empirical data point onto index `0` of each `2023–2035` forecast array so the plotted scenario curves (`BAU`, `Accelerated Policy`, `COP30 Belém 1.5°C`) branch continuously out of the solid black historical curve without a visual gap.



---

## Module 6: Complete Summary of 2030 & 2035 Model Outputs

| Country | ISO | Scenario | Renewables 2030 (TWh) | Renewables 2035 (TWh) | Per-Capita 2030 (kWh) | Per-Capita 2035 (kWh) | Carbon Intensity 2030 ($\text{gCO}_2$/kWh) | Carbon Intensity 2035 ($\text{gCO}_2$/kWh) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Cameroon** | `CMR` | `BAU` | 6.11 | 6.62 | 297.36 | 291.84 | 338.16 | 357.48 |
| **Cameroon** | `CMR` | `Accelerated Policy` | 9.79 | 14.39 | 352.67 | 415.29 | 175.39 | 123.52 |
| **Cameroon** | `CMR` | `COP30 Belém 1.5°C` | **15.87** | **31.53** | **500.18** | **813.78** | **86.09** | **43.24** |
| **Kenya** | `KEN` | `BAU` | 15.79 | 18.55 | 259.34 | 265.31 | 72.54 | 49.50 |
| **Kenya** | `KEN` | `Accelerated Policy` | 21.06 | 30.95 | 346.01 | 444.63 | 72.71 | 53.20 |
| **Kenya** | `KEN` | `COP30 Belém 1.5°C` | **34.14** | **67.84** | **539.69** | **945.15** | **40.39** | **26.87** |
| **Germany** | `DEU` | `BAU` | 351.17 | 413.45 | 6,342.90 | 6,349.12 | 316.94 | 233.59 |
| **Germany** | `DEU` | `Accelerated Policy` | 400.99 | 494.40 | 6,044.25 | 6,446.29 | 211.67 | 124.39 |
| **Germany** | `DEU` | `COP30 Belém 1.5°C` | **754.62** | **1,058.39** | **9,405.71** | **12,302.30** | **78.49** | **36.31** |

---
