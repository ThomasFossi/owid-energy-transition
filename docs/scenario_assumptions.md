# Scenario Assumptions & Implementation Framework

## 1. Overview of Scenario Pathways
To evaluate forward-looking decarbonization trajectories through 2035, we model three distinct policy pathways. These scenarios test sovereign grid resilience against varying renewable expansion velocities and fossil phase-down rates.

---

## 2. Baseline Anchors ($t_0 = 2022$)
All scenario projections are anchored to historical 2022 sovereign baselines extracted from cleaned OWID records (`src/energy_transition/data.py`):
* **Baseline Generation ($E_0$):** Total renewable and fossil generation values established at year-end 2022.
* **Demographic Vectors ($\text{Pop}_0$ and $g_{\text{pop}}$):** Sovereign population bases and UN-derived annual compound growth rates.
* **Thermal Emission Factors ($EF_{\text{fossil}}$):** Reverse-engineered from 2022 fuel mixes and held constant across the projection window to isolate generation policy impact.

---

## 3. Parametric Specifications by Scenario

### A. Business-As-Usual (BAU)
* **Design Rationale:** Extrapolates historical trends without structural policy intervention.
* **Mathematical Rule:** Evaluates Ordinary Least Squares (OLS) linear slopes ($r_{\text{slope}}, f_{\text{slope}}$) over the historical 2010–2022 window.
* **Equation:**
  $$\text{Ren}_{\text{BAU}}(t) = \max\left(0, \text{Ren}_{0} + r_{\text{slope}} \cdot t\right)$$
  $$\text{Fos}_{\text{BAU}}(t) = \max\left(0, \text{Fos}_{0} + f_{\text{slope}} \cdot t\right)$$

### B. Accelerated Policy
* **Design Rationale:** Represents moderate, regionally differentiated climate policy commitments.
* **Parametric Rules:** 
  * For emerging economies (`CMR`, `KEN`), renewables scale at an **8%** annual compound growth rate while fossil generation declines by **2%/yr**.
* **Equation:**
  $$\text{Ren}_{\text{Acc}}(t) = \text{Ren}_{0} \cdot (1 + 0.08)^t, \quad \text{Fos}_{\text{Acc}}(t) = \text{Fos}_{0} \cdot (1 - 0.02)^t$$

### C. COP30 Belém 1.5°C Mission (Modelling Benchmark)
* **Design Rationale:** Enforces the global renewable tripling target established under the **COP28 UAE Consensus** ($3\text{x}$ capacity growth over 8 years, translating to a top-down CAGR of $g_{\text{ren}} = 3^{1/8} - 1 \approx \mathbf{14.72\%}$) through 2030, paired with an implementation roadmap.
* **Parametric Rules:**
  * Renewable generation scales at **14.72%/yr** through 2030 ($t \le 8$).
  * Fossil generation undergoes accelerated phase-out ($d_{\text{fos}}$) set at **8%/yr** for emerging developing grids (`CMR`, `KEN`) and **18%/yr** for industrialized thermal grids (`DEU`, `USA`, `CHN`).
* **Equation:**
  $$\text{Ren}_{\text{COP30}}(t) = \text{Ren}_{0} \cdot (1 + 0.1472)^t \quad (\text{for } t \le 8)$$
  $$\text{Fos}_{\text{COP30}}(t) = \text{Fos}_{0} \cdot (1 - d_{\text{fos}})^t$$

---

## 4. Modeling Caveats & Assumptions Note
As documented in the methodology, applying the global **14.72%** renewable tripling CAGR to individual countries serves as an **illustrative top-down modeling benchmark** to stress-test local infrastructure scaling requirements. Sovereign deployment rates will ultimately be governed by local financing availability, grid modernization constraints, and official NDCs.