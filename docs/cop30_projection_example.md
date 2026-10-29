# Trace-Reproducible Example: COP30 Projection for Kenya (KEN)

## 1. Objective

This document provides a fully transparent, step-by-step numerical trace of the **COP30 Belém 1.5°C Modeling Benchmark** applied to Kenya (`KEN`). It answers the question: *How does an emerging East African grid transition from its 2022 historical baseline toward 2030/2035 climate benchmarks under the COP28 global renewable tripling mandate, and how are intermediate per-capita and carbon intensity metrics derived?*

## 2. Historical Baseline

* **Country / Region:** Kenya (`KEN`, ISO code: `KEN`)

* **Indicator:** Renewable Electricity Generation & Per-Capita Access

* **Historical Baseline Year:** $t_0 = 2022$

* **Observed Baseline Values (OWID Dataset):**

  * Baseline Renewable Generation ($\text{Ren}_0$): $11.38\text{ TWh}$

  * Baseline Fossil & Thermal Generation ($\text{Fos}_0$): $1.58\text{ TWh}$

  * Baseline Total Generation ($\text{Tot}_0$): $12.96\text{ TWh}$

  * Baseline Population ($\text{Pop}_0$): $54.25\text{ million persons}$

  * **Implied Population Growth Rate ($g_{\text{pop}}$):** $2.2\%/\text{yr}$ ($0.022$). *Note on rationale:* This compound annual growth rate is derived empirically from the historical 2010–2022 UN World Population Prospect revisions embedded in the OWID dataset for Kenya, reflecting sustained demographic expansion typical of East African emerging economies.

* **Data Source:** Our World in Data (OWID) Energy Database, aggregating Ember global electricity data and UN World Population Prospects. Source files located in `data/raw/`.

* **Units:** Terawatt-hours ($\text{TWh}$) for generation, million persons for population, $\text{kWh/person}$ for per-capita supply, and $\text{gCO}_2/\text{kWh}$ for carbon intensity.

* **Target Projection Year:** 2030 ($t = 8$) and 2035 ($t = 13$).

* **Scenario Applied:** COP30 Belém 1.5°C Mission Benchmark.

* **Code Location:** `src/energy_transition/scenarios.py` within function `run_cop30_forecasts()`.

## 3. Methodology

Projections are computed using parametric compound growth equations anchored to 2022 baseline values. For each forecast year $yr$, elapsed time steps are calculated as $t = yr - 2022$:

**1. Renewable Expansion (**$14.72\%$ **CAGR):**
Derived from the COP28 UAE Consensus global tripling target ($3\text{x}$ growth over 8 years, where $g_{\text{ren}} = 3^{1/8} - 1 \approx 14.72\%$).

$$
\text{Ren}_{\text{COP30}}(t) = \text{Ren}_{0} \cdot (1 + 0.1472)^t \quad (\text{for } t \le 8)
$$

**2. Fossil Phase-Down (**$8\%/\text{yr}$ **for emerging grids):**

$$
\text{Fos}_{\text{COP30}}(t) = \text{Fos}_{0} \cdot (1 - 0.08)^t
$$

**3. Population Compound Growth:**

$$
\text{Pop}(t) = \text{Pop}_{0} \cdot (1 + g_{\text{pop}})^t
$$

**4. Per-Capita Electricity Supply:**

$$
\text{PerCapita}(t) = \frac{(\text{Ren}(t) + \text{Fos}(t)) \times 10^9}{\text{Pop}(t)}
$$

**5. Grid Carbon Intensity ($\text{gCO}_2/\text{kWh}$):**
Carbon intensity is calculated dynamically as the weighted average emissions across all generation sources divided by total generation. Specifically, the implied fossil emission factor ($\text{EF}_{\text{fossil}}$) is derived from the 2022 baseline:

$$
\text{EF}_{\text{fossil}} = \max\left(\frac{\text{CI}_0 \cdot \text{Tot}_0}{\max(\text{Fos}_0, 0.01)}, 550.0\right)
$$

For each projection year $t$, grid carbon intensity ($\text{CI}(t)$) is computed as:

$$
\text{CI}(t) = \frac{(\text{Fos}(t) \cdot \text{EF}_{\text{fossil}}) + (\text{Ren}(t) \cdot 20.0)}{\text{Tot}(t)}
$$

*(Assuming a nominal lifecycle emissions factor of $20.0\text{ gCO}_2/\text{kWh}$ for renewables such as geothermal and hydro).*

## 4. Worked Calculation, Functions & Code Trace

### Step A: Intermediate Values for Year 3 ($t = 3$, corresponding to 2025)

* **1. Renewable Generation Expansion:**
  

  $$
  \text{Ren}(3) = 11.38 \cdot (1 + 0.1472)^3 \approx 17.18\text{ TWh}
  $$

  * **Code Implementation & Function:** Calculated in `src/energy_transition/scenarios.py` under `run_cop30_forecasts()`.

  * **Corresponding Code Snippet:**

    ```
    cop_ren = ren_2022 * ((1 + cop30_ren_cagr) ** years_elapsed)
    
    ```

* **2. Fossil Generation Phase-Down (**$8\%/\text{yr}$**):**
  

  $$
  \text{Fos}(3) = 1.58 \cdot (1 - 0.08)^3 = 1.58 \cdot (0.7787) \approx 1.23\text{ TWh}
  $$

  * **Code Implementation & Function:** Calculated in `src/energy_transition/scenarios.py` under `run_cop30_forecasts()`.

  * **Corresponding Code Snippet:**

    ```
    cop_fos = fos_2022 * ((1 - 0.08) ** years_elapsed)
    
    ```

* **3. Total Generation (**$\text{Tot}_3$**):**
  

  $$
  \text{Tot}(3) = 17.18 + 1.23 = 18.41\text{ TWh}
  $$

* **4. Population Expansion (**$2.2\%/\text{yr}$**):**
  

  $$
  \text{Pop}(3) = 54.25 \cdot (1 + 0.022)^3 \approx 57.64\text{ million persons}
  $$

* **5. Per-Capita Access Endpoint:**
  

  $$
  \text{PerCapita}(3) = \frac{18.41 \times 10^9\text{ kWh}}{57,640,000\text{ persons}} \approx 317.57\text{ kWh/person}
  $$

* **6. Grid Carbon Intensity:**
  

  $$
  \text{CI}(3) = \frac{(1.23 \cdot \text{EF}_{\text{fossil}}) + (17.18 \cdot 20.0)}{18.41} \approx 80.2\text{ gCO}_2/\text{kWh}
  $$

### Step B: Summary Trajectory Table (`KEN` COP30 Scenario)

| Year | Status | Renewable Gen ($\text{TWh}$) | Fossil Gen ($\text{TWh}$) | Total Gen ($\text{TWh}$) | Population (M) | Per-Capita ($\text{kWh/person}$) | Grid Intensity ($\text{gCO}_2/\text{kWh}$) | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| **2022 (**$t=0$**)** | Historical | $11.38$ | $1.58$ | $12.96$ | $54.25$ | $238.89$ | $109.6$ | 
| **2025 (**$t=3$**)** | Projected | $17.18$ | $1.23$ | $18.41$ | $57.64$ | $319.39$ | $80.2$ | 
| **2030 (**$t=8$**)** | Projected | $34.14$ | $0.81$ | $34.95$ | $64.29$ | $543.63$ | $40.5$ | 

## 5. Validation & Test Verification

The calculations traced above are verified programmatically in our automated test suite located at `tests/test_projection_example.py`.

## 6. Reproduction Instructions

To reproduce this projection and run the test suite locally:

1. **Activate Virtual Environment:**

   ```
   source venv/bin/activate
   
   ```

2. **Execute Automated Scenario Tests:**

   ```
   pytest tests/test_projection_example.py -v -s
   
   ```