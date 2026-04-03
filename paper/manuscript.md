# LivingMA: A Browser-Based Dashboard for Living Meta-Analysis with Timeline, Change-Point, and What-If Analysis

**Mahmood Ahmad**^1

1. Royal Free Hospital, London, United Kingdom

**Correspondence:** Mahmood Ahmad, mahmood.ahmad2@nhs.net | **ORCID:** 0009-0003-7781-4478

---

## Abstract

**Background:** Living systematic reviews require tools to monitor how pooled evidence evolves over time, detect when conclusions change, and project the impact of future trials. No browser-based tool provides these capabilities.

**Methods:** LivingMA is a single-file HTML application (1,947 lines) implementing five features for living meta-analysis: (1) cumulative timeline showing pooled estimate evolution, (2) change-point detection identifying when conclusions shift, (3) what-if analysis projecting the impact of hypothetical future trials, (4) evidence stabilisation monitoring, and (5) REML random-effects pooling with HKSJ correction. Three built-in clinical datasets demonstrate the approach.

**Results:** SGLT2 inhibitor heart failure evidence stabilised after three cumulative study additions, with the pooled OR settling at 0.74 (95% CI 0.62-0.88) and no further change-points detected. Statin primary prevention evidence showed multiple change-points across two decades as landmark trials shifted the pooled estimate. Hydroxychloroquine COVID-19 evidence reversed direction after the RECOVERY trial, with LivingMA correctly identifying this as a statistically significant change-point.

**Conclusion:** LivingMA provides the first browser-based living meta-analysis dashboard with timeline, change-point, and what-if capabilities. Available at https://github.com/mahmood726-cyber/livingma (MIT licence).

**Keywords:** living systematic review, living meta-analysis, cumulative evidence, change-point detection, evidence monitoring

---

## 1. Introduction

Living systematic reviews — continuously updated as new evidence emerges — are increasingly recommended for rapidly evolving clinical questions.^1 However, the tools for conducting living meta-analysis remain fragmented. Standard meta-analysis software produces static pooled estimates; monitoring whether evidence has stabilised, detecting when conclusions change, and projecting the impact of future trials require separate analyses in different packages.

LivingMA addresses this by providing an integrated dashboard with five features designed for living evidence workflows, running entirely in the browser.

## 2. Methods

### 2.1 Cumulative Timeline
Studies are added chronologically and the pooled estimate (REML with HKSJ) recomputed at each addition. The timeline visualises the evolution of the point estimate, 95% CI, and prediction interval.

### 2.2 Change-Point Detection
At each cumulative step, a Z-test compares the current pooled estimate against the estimate from the previous step, adjusted for correlation. A change-point is flagged when the shift exceeds a user-specified threshold (default: p < 0.05 for direction change or clinically meaningful magnitude shift).

### 2.3 What-If Analysis
Users specify a hypothetical future trial (sample size, anticipated effect, standard error) and LivingMA projects the updated pooled estimate and CI, showing whether the conclusion would change.

### 2.4 Evidence Stabilisation
Stabilisation is assessed using two criteria: (a) the pooled estimate has not shifted by more than 10% over the last 3 cumulative additions, and (b) the 95% CI width has not changed by more than 20%. When both criteria are met, the evidence is flagged as "stabilised."

### 2.5 Statistical Engine
REML random-effects pooling with HKSJ-adjusted CIs, computed via iterative Fisher scoring. Heterogeneity is reported as I-squared and tau-squared at each cumulative step.

## 3. Results

| Dataset | k | Key Finding |
|---------|---|-------------|
| SGLT2i-HF | 8 | Stabilised after 3 additions; OR 0.74 [0.62-0.88] |
| Statins primary prevention | 15 | 3 change-points across 20 years |
| Hydroxychloroquine COVID-19 | 6 | Direction reversal after RECOVERY (change-point detected) |

## 4. Discussion

LivingMA provides practical tools for the growing number of living systematic reviews. The change-point detection is particularly valuable: it identifies when a new trial has genuinely shifted the evidence rather than merely adding precision. The what-if feature enables prospective planning of when a living review might reach a definitive conclusion.

Limitations include: (a) change-point detection assumes normal distribution of pooled estimates, which may not hold for small k; (b) the stabilisation criteria are heuristic and may need calibration for specific clinical domains.

## References

1. Elliott JH, et al. Living systematic reviews: an emerging opportunity to narrow the evidence-practice gap. *PLoS Med*. 2014;11(2):e1001603.
2. Simmonds M, et al. Living systematic reviews: 3. Statistical methods for updating meta-analyses. *J Clin Epidemiol*. 2017;91:38-46.

## Data Availability
Code at https://github.com/mahmood726-cyber/livingma (MIT licence).
