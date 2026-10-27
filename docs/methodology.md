# Methodology & Mathematical Architecture

## 1. Analytical Pipeline Architecture
The analytical pipeline (`src/energy_transition/`) follows a modular structure designed to ingest raw OWID records, clean and impute time-series, calculate core development metrics, and project forward-looking decarbonization pathways.

---

## 2. Core Metric Formulations

### A. Per-Capita Electricity Supply & Demographic Dilution
To evaluate whether gross generation gains outpace population growth, annual electricity generation is normalized against sovereign mid-year population estimates:

$$\text{PerCapita}(t) = \frac{E(t) \times 10^9}{\text{Pop}(t)}$$

*Where $E(t)$ is total generation in TWh, converted to kilowatt-hours ($\text{kWh}$), and $\text{Pop}(t)$ is total population at time $t$.*

**Demographic Dilution Index:** Evaluates the annual growth differential $g_{\text{net}} = g_{\text{generation}} - g_{\text{population}}$. If $g_{\text{net}} < 0$, the grid undergoes Demographic Dilution—meaning nameplate capacity additions are absorbed entirely by population expansion rather than raising individual living standards.

### B. Access Elasticity ($\varepsilon$)
The Access Elasticity parameter measures the responsiveness of per-capita electricity access relative to renewable generation growth:

* **$\varepsilon > 1.0$ (Leverage Regime):** Per-capita access scales faster than renewable additions due to efficiency gains or decentralized scaling.
* **$0 < \varepsilon \le 1.0$ (Substitution Regime):** Access scales proportionally with renewable expansion.
* **$\varepsilon \le 0$ (Dilution Regime):** Population growth outpaces clean energy additions, resulting in stagnant or declining per-capita supply.

### C. Grid Carbon Intensity ($CI$)
Grid carbon intensity reflects the weighted average emissions per kilowatt-hour delivered:

$$CI(t) = \frac{\sum_{i} \left(E_i(t) \times EF_i\right)}{E_{\text{total}}(t)}$$

*Where $E_i$ represents generation from fuel source $i$ (coal, gas, oil, hydro, wind, solar, nuclear) and $EF_i$ represents its corresponding lifecycle emission factor ($\text{gCO}_2/\text{kWh}$).*

---

## 3. Scenario Forecasting Methodology

Projections through 2035 are calculated using three distinct parametric frameworks anchored to 2022 sovereign baselines ($t_0 = 2022$, with $t = \text{Year} - 2022$):

**1. Business-As-Usual (BAU):** 
Extrapolates historical Ordinary Least Squares (OLS) trends ($r_{\text{slope}}, f_{\text{slope}}$) evaluated over the 2010–2022 window.

$$\text{Ren}_{\text{BAU}}(t) = \max\left(0, \text{Ren}_{0} + r_{\text{slope}} \cdot t\right)$$
$$\text{Fos}_{\text{BAU}}(t) = \max\left(0, \text{Fos}_{0} + f_{\text{slope}} \cdot t\right)$$

**2. Accelerated Policy:** 
Applies moderate structural policy interventions. For emerging economies (`CMR`, `KEN`), renewables scale at an **8%** annual compound growth rate while fossil fuels decline by **2%/yr**.

$$\text{Ren}_{\text{Acc}}(t) = \text{Ren}_{0} \cdot (1 + 0.08)^t, \quad \text{Fos}_{\text{Acc}}(t) = \text{Fos}_{0} \cdot (1 - 0.02)^t$$

**3. COP30 Belém 1.5°C Mission (Modelling Benchmark):** 
Enforces the global renewable tripling target established in the **COP28 UAE Consensus** ($3\text{x}$ growth over 8 years, translating to an annual CAGR of $g_{\text{ren}} = 3^{1/8} - 1 \approx \mathbf{14.72\%}$) through 2030, paired with accelerated fossil phase-out rates ($d_{\text{fos}}$ where $d_{\text{fos}} = \mathbf{8\%/yr}$ for emerging grids and $\mathbf{18\%/yr}$ for industrialized thermal grids).

$$\text{Ren}_{\text{COP30}}(t) = \text{Ren}_{0} \cdot (1 + 0.1472)^t \quad (\text{for } t \le 8)$$
$$\text{Fos}_{\text{COP30}}(t) = \text{Fos}_{0} \cdot (1 - d_{\text{fos}})^t$$