# Limitations, Uncertainties & Future Improvements

## 1. Data & Historical Limitations
* **Thermal Efficiency Averages:** Historical carbon intensity calculations rely on country-reported aggregate thermal efficiency averages rather than plant-level heat-rate data, introducing minor estimation variance in legacy coal and gas emissions.
* **Missing Early-Year Records:** For emerging technologies in specific developing entities (`CMR`, `KEN`), historical data prior to utility commercialization required strict zero-imputation. While mathematically sound, this creates step-changes when initial commercial deployment begins.

---

## 2. Modeling Simplifications & Assumptions
* **Constant Fossil Emission Factors:** Baseline fossil emission factors ($EF_{\text{fossil}}$) derived from 2022 anchors are held constant across future projections through 2035. This isolates the impact of generation mix shifts but omits potential efficiency gains or fuel-switching (e.g., coal-to-gas transitions) within the thermal fleet itself.
* **Top-Down Global Ambition vs. Sovereign NDCs:** As established in our methodology, applying the global **14.72%** renewable tripling CAGR to individual countries serves as an **illustrative top-down modeling stress-test** rather than an official, legally binding national NDC commitment. Actual national deployment will depend heavily on localized grid constraints, capital availability, and sovereign policy enforcement.
* **Exclusion of Storage & Grid Congestion:** The model focuses on gross generation and demographic dilution balances, assuming sufficient transmission capacity and battery storage buildout to absorb intermittent renewable surges without curtailment penalties.

---

## 3. Future Roadmap & Improvements
* **Hourly Dispatch Simulation:** Expanding the current annual aggregated framework into seasonal hydro/solar dispatch models for African river basins (`docs/roadmap.md`).
* **Dynamic Cost-Optimization:** Integrating levelized cost of electricity (LCOE) learning curves and localized financing discount rates into the scenario engine.