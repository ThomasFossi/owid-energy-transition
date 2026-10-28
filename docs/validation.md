# Model Validation, Test Strategy & Robustness

## 1. Automated Testing Architecture
To ensure rigorous internal consistency and prevent regressions, the repository incorporates an automated testing suite (`tests/`) executed via GitHub Actions CI and `pytest`. The test independently validates historical cleaning functions, metric calculations, and scenario forecasting boundaries.

---

## 2. Independent Scenario & Physical Bounding Tests
As implemented in `tests/test_scenarios.py`, the test suite uses parameterized assertions to test every projection scenario (`BAU`, `Accelerated Policy`, `COP30 Belém 1.5°C`) independently across the entire 2023–2035 time horizon:

* **Non-Negative Physical Constraints:** Asserts that generation totals and per-capita supplies remain strictly non-negative ($\ge 0.0$ TWh and kWh/person).
* **Grid Carbon Intensity Limits:** Verifies that calculated carbon intensity remains bounded within realistic physical thresholds ($0 \le CI \le 1200\text{ gCO}_2/\text{kWh}$).
* **Policy Divergence Verification:** Asserts that advanced climate policy pathways (`COP30`) achieve strictly higher renewable generation and lower carbon intensity than baseline trajectories (`BAU`) by the end-point year (2035).

---

## 3. Sensitivity Analysis & Parameter Sweeps
To evaluate model resilience under varying policy assumptions, a parameter sweep was conducted varying **Renewable Expansion CAGR ($g_{\text{ren}}$)** between $10\%$ and $20\%$ alongside **Fossil Phase-Down Rates ($d_{\text{fos}}$)** between $-5\%/\text{yr}$ and $-18\%/\text{yr}$ through 2030:

* **Fossil Phase-Down Dominance:** Sensitivity checks reveal that grid decarbonization speed is significantly more sensitive to the **fossil phase-down rate** than variations in renewable CAGR. Even with aggressive renewable scale-up ($20\%$), if fossil generation declines slowly ($-5\%/\text{yr}$), grid carbon intensity floors remain elevated due to residual baseline emissions.
* **Demographic Dilution Robustness:** In high-population-growth developing entities (`CMR`, `KEN`), per-capita metrics confirm that unless renewable growth outpaces population expansion, per-capita electricity supply stagnates, validating the core demographic dilution model.