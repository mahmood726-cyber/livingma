# LivingMA — Living Meta-Analysis Dashboard

A single-file, offline browser dashboard for cumulative (timeline) meta-analysis
with what-if scenario analysis.

## What it does

- **Cumulative timeline**: sorts studies by year and pools the accumulating
  evidence at each step.
- **Pooling**: random-effects with REML τ² estimation and Knapp–Hartung (HKSJ)
  confidence intervals (with the ad-hoc `max(1, q)` variance floor), plus a
  prediction interval for k ≥ 3.
- **Effect measures**: log RR, log OR, mean difference, and standardised mean
  difference (Hedges' g). RR/OR are pooled on the log scale and back-transformed
  for display.
- **Change-point detection**: a heuristic flag when the pooled estimate changes
  by more than a user-set percentage between consecutive steps, or when its
  significance status flips.
- **Stability monitoring**: marks the timeline stable once recent changes stay
  within tolerance, and tracks I² and prediction-interval width over time.
- **What-if analysis**: add a hypothetical study and see its effect on the
  pooled estimate, CI, I², and τ².
- **Export**: CSV of the cumulative results and a text/HTML report.

## Usage

Open `livingma.html` in a browser (no server or network needed). Load one of the
built-in examples (SGLT2 inhibitors, statins, hydroxychloroquine) or enter your
own 2×2 / continuous study data.

## Tests

`tests/test_livingma.py` is a Selenium suite (Chrome headless) covering page
load, tab navigation, example loading, pooling, what-if, and the report. Run:

```
python -m pytest tests/test_livingma.py -q
```

## Notes / limitations

- Change-point detection is a percent-change + significance-flip heuristic, not a
  CUSUM or Bayesian online change-point model.
- Trial-sequential-analysis decision boundaries are not implemented.
- The timeline assumes studies arrive in publication-year order.
</content>
