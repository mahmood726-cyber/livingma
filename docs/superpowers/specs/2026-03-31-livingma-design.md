# LivingMA — Living Meta-Analysis Dashboard
## Design Specification · 2026-03-31

### Overview
Single HTML file (~6,000–8,000 lines), dark theme, canvas charts, zero external dependencies.

**Author:** Mahmood Ahmad, Royal Free Hospital, London
**Target:** BMJ / F1000 / JAMA preprint + GitHub Pages deployment

---

### Visual Design
- Dark theme CSS vars: `--bg:#0f0f1a`, `--surface:#1a1a2e`, `--accent:#4fc3f7`, `--text:#e0e0e0`
- Matches MetaAudit / TSA Pro visual identity
- Responsive single-column layout, 4-tab interface

---

### 5 Core Features

#### 1. Timeline Cumulative MA
- Studies entered with publication dates (year or full date)
- Drag time slider → forest plot grows study-by-study
- At each time point: pooled effect, 95% CI, 95% PI, I², τ²
- Animated playback via Play button (setInterval, 500ms steps)
- Studies sorted by publication year; ties broken alphabetically

#### 2. Stability Analysis
- At each cumulative step, compute:
  - % change in estimate from previous step
  - Rolling I² trend (last 3 studies)
  - PI width trend (narrowing/widening)
- "Evidence maturity" badge when estimate stable within ±5% for ≥3 consecutive studies
- Stability chart: effect ± CI ribbon over time

#### 3. What-If Simulator
- User adds hypothetical future study (effect size + N, or 2×2 counts)
- Instant recalculation of pooled result
- Before/after side-by-side comparison panel
- Shows: Δ estimate, Δ CI width, Δ I², Δ τ²

#### 4. Change-Point Detection
- Identifies studies shifting the estimate by >10% or changing significance (p crosses 0.05)
- Marks study name + year on timeline chart
- Narrative: "RECOVERY (2020) shifted pooled RR from 0.87 to 1.09 and crossed null"
- Threshold configurable (5%, 10%, 20%)

#### 5. Alert System
- User sets thresholds:
  - Effect crosses value X (e.g., RR > 1.0 = harm signal)
  - PI wider than Y (e.g., PI width > 0.5)
  - I² exceeds Z% (e.g., I² > 75%)
- Dashboard highlights time-periods where alerts trigger (red overlay on chart)
- Alert log in Report tab

---

### Tab Structure

| Tab | Contents |
|-----|----------|
| Tab 1: Data Entry | Manual row entry + paste TSV + 3 example buttons + date column |
| Tab 2: Timeline | Main view — slider + cumulative forest + stability chart |
| Tab 3: What-If Simulator | Hypothetical study panel + before/after comparison |
| Tab 4: Report & Export | Alert log, change-point narrative, PNG download, CSV download |

---

### 3 Built-In Example Datasets

#### Example 1: SGLT2 Inhibitors for Heart Failure (2019–2022)
8 studies. Outcome: hospitalisation for HF or CV death.
Expectation: estimate stabilises rapidly around RR ≈ 0.77, narrow PI.

| Study | Year | Events E | N_E | Events C | N_C |
|-------|------|----------|-----|----------|-----|
| DAPA-HF | 2019 | 386 | 2373 | 502 | 2371 |
| EMPEROR-Reduced | 2020 | 361 | 1863 | 462 | 1867 |
| SOLOIST-WHF | 2020 | 245 | 608 | 311 | 614 |
| EMPEROR-Preserved | 2021 | 415 | 2997 | 511 | 2991 |
| DELIVER | 2022 | 512 | 3131 | 610 | 3132 |
| DAPA-CKD (HF sub) | 2020 | 63 | 468 | 87 | 472 |
| SCORED (HF sub) | 2021 | 154 | 1050 | 199 | 1050 |
| EMPULSE | 2022 | 52 | 265 | 72 | 265 |

**Story:** Evidence built rapidly 2019–2023. Estimate highly stable after 3rd study.

#### Example 2: Statins for Primary Prevention (1995–2019)
12 studies. Outcome: major cardiovascular event.
Expectation: decades of accumulation, multiple change points, estimate slowly consolidating.

| Study | Year | Events E | N_E | Events C | N_C |
|-------|------|----------|-----|----------|-----|
| WOSCOPS | 1995 | 174 | 3302 | 248 | 3293 |
| AFCAPS/TexCAPS | 1998 | 116 | 3304 | 183 | 3301 |
| PROSPER | 2002 | 408 | 2891 | 473 | 2913 |
| ALLHAT-LLT | 2002 | 631 | 5170 | 641 | 5185 |
| ASCOT-LLA | 2003 | 154 | 5168 | 185 | 5137 |
| CARDS | 2004 | 83 | 1428 | 127 | 1410 |
| MEGA | 2006 | 66 | 3866 | 101 | 3966 |
| JUPITER | 2008 | 142 | 8901 | 251 | 8901 |
| PREVEND IT | 2004 | 11 | 216 | 13 | 208 |
| HYPOS | 2005 | 4 | 100 | 7 | 100 |
| HOPE-3 | 2016 | 235 | 6361 | 304 | 6344 |
| TRACE-RA | 2019 | 58 | 1578 | 53 | 1584 |

**Story:** Benefit established by 2000; ALLHAT (2002) briefly challenged consensus; JUPITER (2008) shift; consolidation by 2016.

#### Example 3: Hydroxychloroquine for COVID-19 (2020)
8 studies. Outcome: mortality.
Expectation: early small studies suggest benefit; RECOVERY reversal dramatically shifts estimate to null/harm.

| Study | Year | Events E | N_E | Events C | N_C |
|-------|------|----------|-----|----------|-----|
| Gautret | 2020 | 0 | 20 | 2 | 16 |
| Chen Z | 2020 | 0 | 31 | 1 | 31 |
| Mahévas | 2020 | 18 | 84 | 16 | 89 |
| Tang | 2020 | 3 | 75 | 0 | 75 |
| Horby (RECOVERY) | 2020 | 421 | 1561 | 790 | 3155 |
| Cavalcanti | 2020 | 55 | 221 | 54 | 227 |
| Abd-Elsalam | 2020 | 6 | 97 | 5 | 97 |
| WHO SOLIDARITY | 2020 | 104 | 947 | 84 | 906 |

**Story:** 2020 "narrative arc" — early tiny trials suggested benefit; RECOVERY (largest) reversed to null/harm; pooled estimate crosses 1.0.

---

### Statistical Engine

- **Effect measures:** RR, OR (binary); MD, SMD (continuous)
- **Pooling method:** REML for τ² estimation (same as MetaAudit/TSA Pro)
- **CI:** HKSJ adjustment (Hartung-Knapp-Sidik-Jonkman)
- **PI:** 95% prediction interval using t-distribution (df = k−2)
- **Continuity correction:** 0.5 to all cells when any cell = 0 (binary only)

### Cumulative Engine
```
cumulativeByDate(studies) → [{
  k, date, estimate, se, ci95, pi95, I2, tau2, H2,
  w_fixed[], w_random[]
}]
```

### Stability Engine
```
stabilityAnalysis(cumResults) → {
  stable: bool, stableSince: int (study index),
  changePct: number[], piTrend: number[], I2Trend: number[]
}
```

### Change-Point Engine
```
detectChangePoints(cumResults, threshold=0.10) → [{
  studyIndex, studyName, year,
  beforeEst, afterEst, pctChange,
  significanceFlip: bool, narrative: string
}]
```

### What-If Engine
```
whatIf(studies, hypothetical) → {
  before: {estimate, ci, pi, I2, tau2},
  after:  {estimate, ci, pi, I2, tau2},
  delta:  {estimate, ci_width, I2, tau2}
}
```

---

### Canvas Charts

#### Timeline Forest (Tab 2, upper)
- Y-axis: study names (grows as slider advances)
- X-axis: log scale (RR/OR) or linear (MD/SMD)
- Pooled row: diamond at bottom
- Current time position annotated with vertical line

#### Stability Chart (Tab 2, lower)
- X-axis: cumulative study index (1…k)
- Y-axis: pooled estimate
- Effect ribbon: line ± CI shading
- PI shading (lighter)
- Change-point markers: vertical dashed lines
- Alert threshold: horizontal dotted line

#### What-If Comparison (Tab 3)
- Side-by-side: before (left) | after (right)
- Same axis scale for both panels
- Delta summary text below

---

### Alert System

User configures (stored in localStorage):
- `alertEffect`: number | null
- `alertPIWidth`: number | null
- `alertI2`: number | null

When triggered, stability chart adds red overlay band; Report tab generates alert log.

---

### Data Entry (Tab 1)

#### Binary mode (RR/OR)
| Study | Year | Events_E | N_E | Events_C | N_C |

#### Continuous mode (MD/SMD)
| Study | Year | Mean_E | SD_E | N_E | Mean_C | SD_C | N_C |

Paste from TSV (Excel copy-paste compatible).
Import validates: year is integer 1900–2100, N > 0, Events ≤ N.

---

### Export

- **PNG:** canvas `toDataURL()` — Timeline chart + Stability chart stacked
- **CSV:** all cumulative results (k, estimate, ci_low, ci_high, pi_low, pi_high, I2, tau2)
- **Report:** HTML string summarising change points, alerts, stability verdict

---

### localStorage Schema (version 1)
```json
{
  "lma_v1_studies":    "[{study rows}]",
  "lma_v1_settings":  "{effectMeasure, threshold, alerts}",
  "lma_v1_whatif":    "{hypothetical study}"
}
```

---

### File Size Target
- Lines: 6,000–8,000
- Minified size: < 200 KB

### Browser Support
- Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

---

### Safety Checklist
- [ ] `</script>` never appears literally inside `<script>` blocks
- [ ] `?? fallback` used (never `|| fallback` for numerics)
- [ ] `?? ... ||` wrapped in parens
- [ ] Div balance verified
- [ ] All canvases have aria-label
- [ ] Blob URLs revoked after use
- [ ] localStorage keys all prefixed `lma_v1_`
- [ ] No Math.random() (use seeded PRNG for any sampling)

---

*End of specification.*
