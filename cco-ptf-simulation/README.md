# Compassionism Framework Simulation

An interactive, browser-based agent-based simulation of all five [Compassionism](https://bettertobest.github.io/research-hub/) architectures — no installation required. BLEI-calibrated against 2023 US Consumer Expenditure Survey data.

**[▶ Open the simulation](https://bettertobest.github.io/compassionism-simulation/)**

---

## What's new in v3.3

- **Wage growth diminishing returns** — stability premium tapers above median wage, preventing structural compounding (Mullainathan & Shafir 2013 + Carroll 1997)
- **NBER-calibrated recession severity** — beta(5,2) distribution over [0.70, 0.95], mode ≈ 0.86 (14% income loss); replaces prior uniform distribution that overstated severe recessions
- **50× Monte Carlo with 95% CI** — publication-grade confidence intervals (mean ± 1.96·SD/√n) via Run 10× / Run 50× buttons
- **Participant stratification** — separate poverty and BLEI KPIs and charts for CCO participants vs. non-participants, testing whether CCO benefits opt-ins without harming opt-outs
- **Computed OAT sensitivity** — 11 actual mini-simulations (±20% on 5 parameters, seed 7777) replacing prior hardcoded guidance table
- **Validation suite** — 4 internal consistency checks on demand (BU monotonicity, participation threshold, CCO benefit, PTF inflation dampening)
- **JSON export** — complete parameter + time-series snapshot for replication alongside CSV
- **High Automation preset** — full integration with AI displacement wave over 25-year horizon
- **ODD protocol** — Grimm et al. (2010) ABM documentation in the Assumptions panel

---

## What this simulates

The simulation models all five integrated Compassionism architectures and their interactions:

| System | Layer | Role in the model |
|--------|-------|-------------------|
| **CCO** (Creative Currency Octaves) | Economic | Distributes Basic Units monthly; agents convert at quality-based multipliers (1×–9×) plus Φ 1.618× golden ratio bonus |
| **PTF** (Public Trust Foundations) | Asset | Community-owned essential goods; reduces agent overhead 40–60%; raises BU food utility at 2.64× premium |
| **PTH** (Public Trust Housing) | Asset | Builds Acre Equity for resident agents; housing costs settled in Basic Units; eliminates rent extraction (EDC drops to <10%) |
| **SZH** (Social Zone Harmonization) | Spatial | Zone coherence index (0.30–0.95) amplifies PTF conversion rates up to 35% and PTH Acre Equity appreciation by up to 1%/yr |
| **CIP** (Citizens Internet Portal) | Democratic | Governs merit assessment and Octave advancement; raises system stability up to 14%; reduces conversion tax leakage |

Welfare outcomes are measured against the **Basic Living Economic Index (BLEI)** — a temporal stability metric calibrated to US baseline conditions. See the [BLEI paper](https://bettertobest.github.io/research-hub/basic-living-economic-index.html).

---

## How to use

**No Python. No installation. Just open `index.html` in any browser.**

### Option A — Open locally
1. Download `index.html`
2. Double-click — opens in Chrome, Firefox, Safari, or Edge
3. Adjust controls and click **Run Simulation**

### Option B — Host on GitHub Pages
1. Upload `index.html` to your repository root
2. Go to **Settings → Pages → Source → main branch / root**
3. Live at `https://yourusername.github.io/compassionism-simulation/`

---

## Controls reference

### Scenario presets

| Preset | Systems active | Purpose |
|--------|---------------|---------|
| **Traditional Welfare** | None (BU = $0) | US baseline — no CCO, welfare transfers only |
| **CCO Only** | CCO | Basic Units active; no community infrastructure |
| **Full Integration** | All five | Optimal parameters from Monte Carlo research |
| **Stress Test** | All five (degraded) | Low participation + shocks — tests fragility |
| **High Automation** | All five + AI wave | Full integration with AI displacement over 25-year horizon (v3.3) |

### CCO parameters

| Parameter | Range | Optimal |
|-----------|-------|---------|
| Monthly BU allocation | $0–$1,800 | $1,200 |
| Max octave level | 1–9 | 6 |
| BU expiry | 1–6 months | 1 month |
| Phi Φ rate | On / Off | On (1.618×) |
| Conversion tax | 0–30% | 12% |
| Quality multiplier ceiling | 1×–9× | 9× |

### SZH parameters
- **Zone coherence index** (0.30–0.95, default 0.72): higher coherence amplifies PTF and PTH effectiveness spatially

### CIP parameters
- **Democratic participation rate** (20–95%, default 65%): higher participation improves quality accuracy, octave advancement, and stability

### Participation thresholds
- **Minimum viable:** 55% (below this, network effects collapse)
- **Optimal:** 78%

### Run options (v3.3)
- **Run Simulation** — single deterministic or random run
- **Run 3×** — variance range (min/max/mean)
- **Run 10× / 50×** — 95% confidence intervals (mean ± 1.96·SD/√n)
- **One-at-a-Time Sensitivity** — computed ±20% mini-runs (appears after first run)
- **Validation Suite** — 4 internal consistency checks

---

## Output metrics

### Economic outcomes

| Metric | Full integration | US baseline |
|--------|-----------------|-------------|
| Wealth poverty rate | <5% | ~77% |
| Gini coefficient (EDC-adjusted) | ≤0.22 | ~0.46 |
| Median wealth | $82,000 | ~$18,500 |
| System stability | ≥90% | ~65% |

### BLEI temporal stability (Johnson & Claude, 2026)

| Metric | Full integration | US baseline |
|--------|-----------------|-------------|
| Median BLEI score | 700–800+ days | ~45 days |
| % at Flourishing tier (730+ days) | >50% | ~2% |
| BLEI poverty (% Crisis+Precarious) | <3% | ~45% (yr 15) |
| Avg Extractive Drain (EDC) | <10% | 53–72% |
| Daily basic cost | $31.67 | $68.33 |

### BLEI tier definitions

| Tier | Days covered | Economic condition |
|------|-------------|-------------------|
| Crisis | <7 | Immediate survival risk |
| Precarious | 7–29 | Acute economic vulnerability |
| Threshold | 30–119 | Basic needs met, no buffer |
| Stable | 120–364 | Modest planning horizon |
| Secure | 365–729 | One-year investment horizon |
| **Flourishing** | **730+** | **Two-year entrepreneurial horizon unlocked** |

**BLEI poverty** (% Crisis + Precarious, i.e. < 30 days) is the primary poverty indicator in v3.3. It captures temporal vulnerability rather than wealth stock, and correctly classifies income-stable households who happen to hold low assets.

---

## Stress-test scenarios

1. **No CCO (BU = $0)** — Observe pure welfare-state baseline; BLEI drops to Precarious for most agents
2. **Participation collapse** — Set participation to 40%; network effects fail; Gini and poverty stagnate
3. **SZH disabled** — Compare PTF/PTH outcomes with and without spatial zone coherence
4. **CIP disabled** — Observe quality noise increase; stability drops; octave advancement slows
5. **Phi-only economy** — Set max multiplier 9×, enable Φ, participation 95%; what is the ceiling?
6. **PTF saturation** — Push PTF above 30%; observe distortion warning and Gini effects
7. **Shock resilience** — Enable shocks (beta(5,2) recession severity) with optimal vs. stress-test parameters
8. **High automation wave** — Use High Automation preset; observe heterogeneous wage displacement by automationRisk tier
9. **Non-participant equity** — Enable CCO at 78%, examine participant vs. non-participant stratification charts to verify opt-outs are not harmed

---

## Replication & validation

This simulation implements the mathematical framework from:

> Johnson, D. & Claude (Anthropic). (2026). *CCO-PTF-PTH-CIP-SZH Simulation Replication Framework v3.3*. Better To Best Research Hub. <https://bettertobest.github.io/research-hub/cco-ptf-simulation-replication.html>

BLEI calibration from:

> Johnson, D. & Claude (Anthropic). (2026). *Basic Living Economic Index: A temporal stability framework for welfare measurement under Compassionism*. Better To Best Research Hub. <https://bettertobest.github.io/research-hub/basic-living-economic-index.html>

### Core formulas

**Dual wealth accumulation:**
```
W_total(t) = W_CCO(t) + W_PTF(t) + θ × W_CCO(t) × W_PTF(t)
```
where θ = 0.15–0.25 (synergy coefficient)

**Wage growth with diminishing returns (v3.3):**
```
wage_growth = BASE + BLEI_BONUS × 1/(1 + 0.5 × max(0, wage/WAGE_MEDIAN_SIU − 1))
            + octave × OCTAVE_BONUS − popAIDisp × automationRisk
```

**Phi-enhanced conversion:**
```
CCO_enhanced = B₀ × 2^O × R_base × φ_beauty × M_PTF × M_SZH
```

**SZH PTF amplification:**
```
M_SZH = 1.30 + (ZoneCoherence − 0.50) × 0.35   [range: 1.22–1.48]
```

**BLEI score:**
```
BLEI = (Liquid assets + γ × Monthly income + BU_food_effective) / C_basic_daily
```
where C_basic_daily = $68.33 baseline → $31.67 under CCO + PTH

**Recession severity (v3.3):**
```
incomeMultiplier = 0.70 + beta(5, 2) × 0.25   [mode ≈ 0.86; range [0.70, 0.95]]
```
Calibrated against NBER post-WWII recession data; replaces Uniform(0.65, 0.85).

**Gini evolution:**
```
Gini(t) = Gini₀ × (1 − ρ_CCO − ρ_PTF − ρ_SZH − ρ_CIP)^t
```

---

## License & attribution

Released under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

**Cite as:**
> Johnson, D. & Claude (Anthropic). (2026). *Compassionism Framework Simulation* (v3.3). Better To Best Research Hub. <https://bettertobest.github.io/compassionism-simulation/>

**Research Hub:** [bettertobest.github.io/research-hub](https://bettertobest.github.io/research-hub/)  
**Wiki:** [bettertobest.github.io/research-hub/wiki](https://bettertobest.github.io/research-hub/wiki/)  
**BLEI Paper:** [basic-living-economic-index.html](https://bettertobest.github.io/research-hub/basic-living-economic-index.html)  
**Replication Framework:** [cco-ptf-simulation-replication.html](https://bettertobest.github.io/research-hub/cco-ptf-simulation-replication.html)  
**Contact:** BetterToBestResearch@gmail.com  
**Discussions:** [GitHub Discussions](https://github.com/BetterToBest/research-hub/discussions)
