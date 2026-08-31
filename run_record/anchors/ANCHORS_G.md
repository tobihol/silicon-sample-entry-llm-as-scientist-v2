# ANCHORS_G — control-condition response-shape library (Section 3)

**Scope.** Train-split tables only. Nothing here is a prediction about the target
study's *levels*: this file supplies the SHAPE of a response distribution given
its mean, plus how that shape moves when a treatment moves the mean.

**Blinding.** Read only `/workspace/datasets/**`, `/workspace/benchmark/**`
(instrument / codebook / QSF — no human outcomes exist there) and
`/workspace/run/anchors/**`. No retrieval of any kind was performed; no
remembered published result is used as a number. Every figure below is computed
from microdata in this container. Recognition disclosure: `voelkel2026`,
`vlasceanu2024`, `tisp`, `spampatti2023`, `koetke2024` are published studies I
recognise; all numbers are recomputed here from their deposited microdata, which
is the train split and is explicitly readable.

**Deliverables.** `ANCHORS_G.md` (this file), `shape_library.csv` (159 rows of
measured shape statistics + fitted recipe parameters), `shape_lib.py`
(importable sampler, self-test passes under `/opt/kernel/venv/bin/python`).

---

## 0. The single most important structural fact

Read `/workspace/benchmark/codebook.csv` + `survey/questionnaire.txt` +
`survey/survey.qsf` first. **The target has no Likert items at all.** Every one
of the 13 scored outcomes is built from *integer 0–100 sliders*, except
`donation_ams` (whole dollars $0–$10) and `newsletter_signup` (0/1):

| target outcome | construction | response class |
|---|---|---|
| `trust_multidimensional` (PRIMARY) | mean of 12 slider items (4 subscales × 3) | mean of k=12 sliders |
| `trust_post`, `distrust_post`, `belief_post`, `policy_general` | single slider | k=1 slider |
| `funding_perceptions` | `100 − funding_5`, single slider | k=1 slider (reflected) |
| `policy_role_mean` | mean of 4 sliders | k=4 |
| `concern_mean` | mean of 3 sliders | k=3 |
| `inst_trust_mean` | mean of 5 sliders | k=5 |
| `policy_specific_mean` | mean of 7 sliders | k=7 |
| `behavior_mean` | mean of 6 sliders | k=6 |
| `donation_ams` | whole dollars $0–10 | 11-point discrete |
| `newsletter_signup` | Yes/No → 1/0 | Bernoulli |

So class (c) in the task brief ("mean of k Likert items rescaled to 0–100") does
not occur; there is **no coarse Likert lattice anywhere**. The relevant
discreteness is (i) the integer 0–100 slider lattice and (ii) the 1/k lattice
created by averaging k of them.

The target's sliders are Qualtrics `Slider / HBAR`, `GridLines = 10`,
`NumDecimals = 0`, `CSSliderMin/Max = 0/100`, `ShowValue = true`, empty by
default. **`vlasceanu2024`'s `usa_1.qsf` has the byte-identical
`Configuration`**, and `voelkel2026` reproduces the same heaping profile. Those
two are therefore the reference corpus (47 items, n ≈ 8k–14k each).
`hackenburg2025` and `bago2025` use a different slider UI and heap about twice as
hard (P(multiple of 5) 0.66 vs 0.40); they are reported as a sensitivity band and
are deliberately **not** used for the defaults.

---

## 1. Headline: how much a Gaussian costs you

Metrics computed exactly as Section 3 does — on the outcome's full scale range,
here the integer grid 0…100 — between the *empirical* pmf of each reference item
and a candidate pmf with the same mean.

| candidate | OVL (↑) | KS (↓) | W1 (↓, pp) |
|---|---|---|---|
| clipped Gaussian, **given the true SD** | 0.776 | 0.104 | 4.99 |
| shape_lib, mean only | 0.848 | 0.065 | 2.81 |
| shape_lib, mean + SD | 0.852 | 0.052 | 1.77 |

47 single slider items; shape_lib wins OVL on 46/47. **W1 falls by 65 %, KS by
half, OVL rises by 0.076.** The Gaussian is handed the true SD and still loses,
because its error is the *shape*: no integer lattice, no 0/50/100 spikes, and a
bell where the data are flat.

Composites (8 voelkel2026 scales, k = 3–6):

| scale | k | rbar | ovl_lib | ovl_g | ks_lib | ks_g | w1_lib | w1_g |
|---|---|---|---|---|---|---|---|---|
| Belief_Pre | 3.000 | 0.540 | 0.872 | 0.851 | 0.041 | 0.043 | 1.346 | 1.703 |
| Concern_Pre | 3.000 | 0.900 | 0.857 | 0.778 | 0.060 | 0.099 | 2.582 | 5.309 |
| Policies_Pre | 3.000 | 0.820 | 0.869 | 0.845 | 0.051 | 0.093 | 1.046 | 4.518 |
| Intent_Pre | 4.000 | 0.690 | 0.882 | 0.813 | 0.056 | 0.090 | 1.808 | 3.607 |
| PoliciesSp_Pre | 4.000 | 0.510 | 0.862 | 0.872 | 0.056 | 0.058 | 1.892 | 1.540 |
| Candidate_Pre | 4.000 | 0.420 | 0.847 | 0.869 | 0.052 | 0.034 | 2.278 | 1.384 |
| Companies_Pre | 3.000 | 0.820 | 0.877 | 0.848 | 0.048 | 0.094 | 1.096 | 4.227 |
| IntentNp_Pre | 6.000 | 0.390 | 0.932 | 0.912 | 0.020 | 0.033 | 0.710 | 1.657 |

mean OVL 0.875 vs 0.848; KS 0.048 vs 0.068; W1 1.59 vs 2.99.
**Honest caveat:** for a composite with *many, weakly correlated* items
(k ≥ 4, r̄ ≤ 0.55) the CLT does most of the work and a Gaussian is already close
— it beats the library on OVL for `PoliciesSp` (k=4, r̄=.51) and `Candidate`
(k=4, r̄=.42). The library's advantage is concentrated in (a) all single sliders
and (b) high-r̄ composites, where the Gaussian is badly wrong (`Concern`, r̄=.90:
W1 5.31 → 2.58).

---

## 2. Class (a) — single 0–100 slider (attitude / trust toward a group)

Corpus: 47 items, US, matched slider UI. `voelkel2026` belief/concern/policy/
intention/company/candidate batteries + `vlasceanu2024` belief, 9 climate
policies, perceived consensus, **trust in scientists** (`Trust_sci1_1`,
`Trust_sci2_1`) and trust in government.

Pooled: mean 58.3, SD **30.0 ± 3.0**, skew −0.41, **excess kurtosis −0.50 (range
−1.46 … +1.20)**, P(0) 0.048, P(50) 0.042, P(100) 0.133, P(integer) **1.000**,
P(multiple of 5) 0.402, P(multiple of 10) 0.308.

By mean band (this is the mean → shape law):

| mean band | n_items | mean | SD | skew | kurt | P(0) | P(50) | P(100) | P(x%5==0) | P(x%10==0) |
|---|---|---|---|---|---|---|---|---|---|---|
| (0, 35] | 5.000 | 30.214 | 29.012 | 0.770 | -0.428 | 0.138 | 0.056 | 0.022 | 0.393 | 0.293 |
| (35, 45] | 3.000 | 38.437 | 30.967 | 0.392 | -0.961 | 0.125 | 0.071 | 0.029 | 0.409 | 0.310 |
| (45, 55] | 10.000 | 50.073 | 32.424 | -0.054 | -1.163 | 0.060 | 0.055 | 0.080 | 0.381 | 0.284 |
| (55, 65] | 7.000 | 60.112 | 30.871 | -0.472 | -0.848 | 0.031 | 0.044 | 0.118 | 0.391 | 0.287 |
| (65, 75] | 19.000 | 69.427 | 29.433 | -0.877 | -0.208 | 0.019 | 0.029 | 0.189 | 0.410 | 0.321 |
| (75, 100] | 3.000 | 77.598 | 24.709 | -1.224 | 0.961 | 0.008 | 0.023 | 0.269 | 0.456 | 0.375 |

Decile grid (0,10,…,100) by mean band:

| mean band | q0 | q10 | q20 | q30 | q40 | q50 | q60 | q70 | q80 | q90 | q100 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| (0, 35] | 0.0 | 0.0 | 1.8 | 7.2 | 13.2 | 21.4 | 32.8 | 48.0 | 53.8 | 74.4 | 100.0 |
| (35, 45] | 0.0 | 0.3 | 4.7 | 14.3 | 24.3 | 36.7 | 48.7 | 52.0 | 67.3 | 86.3 | 100.0 |
| (45, 55] | 0.0 | 3.4 | 13.8 | 28.3 | 42.8 | 50.9 | 60.3 | 72.4 | 83.7 | 96.3 | 100.0 |
| (55, 65] | 0.0 | 9.1 | 31.0 | 46.9 | 54.0 | 64.1 | 73.7 | 81.7 | 91.0 | 99.4 | 100.0 |
| (65, 75] | 0.0 | 20.1 | 45.6 | 57.0 | 68.6 | 77.3 | 84.8 | 92.3 | 98.4 | 99.8 | 100.0 |
| (75, 100] | 0.0 | 45.0 | 57.0 | 69.3 | 77.3 | 84.7 | 92.0 | 98.0 | 100.0 | 100.0 | 100.0 |

### Heaping profile (multiplier over the local off-the-5-grid baseline)

| value | multiplier |
|---|---|
| 100 | **11.8×** |
| 50 | **4.07×** |
| 0 | 2.56× |
| 25, 75 | 1.96× |
| other multiples of 10 | 1.68× |
| multiples of 5 that are not multiples of 10 | 1.16× |
| everything else | 1.00 |

Notice how mild the non-endpoint heaping is: after you have modelled 0, 50 and
100 explicitly, an integer-uniform interior with a ~1.7× bump on the tens
reproduces P(x % 10 == 0) = 0.31 and P(x % 5 == 0) = 0.40 to within 0.01. The
whole "sliders pile up on round numbers" story is, empirically, **almost entirely
the three points 0 / 50 / 100**.

### Parametric recipe (implemented in `shape_lib.slider_pmf`)

For a target mean m (0–100), write mm = m/100.

1. `P(0) = logistic(0.4611 − 6.5048·mm)`
   `P(100) = logistic(0.4611 − 6.5048·(1 − mm))`
   (one pooled fit over both endpoints, 94 item-endpoints, R² = 0.85)
2. `P(50) = clip(0.0598 − 0.1235·|mm − 0.5|, 0.004, 0.12)`   (R² = 0.18 — weak)
3. Interior on the integers 1…99 (excluding 50):
   `p(v) ∝ h(v) · Beta_pdf(v/100 ; a, b)` with **a + b = κ = 2.07**
   (method-of-moments over the 47 items: mean 2.07, SD 0.46 — note Beta(1,1) =
   uniform has a+b = 2, which is *why* the interior is flat), and h(v) the
   heaping profile above.
4. Solve the Beta location by bisection so the pmf mean is exactly m. If you also
   know the SD, solve a + b for it too (SD is monotone decreasing in a + b).

Default SD if you do not have one: `SD = −88.62·mm² + 88.41·mm + 10.42`
(R² = 0.42 across items; peaks at 32.5 near mm = 0.5, falls to ~24 at mm = 0.8).

Fitted model output, for sanity:

| mean | sd | p0 | p50 | p100 | deciles |
|---|---|---|---|---|---|
| 30 | 29.0000 | 0.1839 | 0.0351 | 0.0164 | [0.0, 1.0, 6.0, 13.0, 22.0, 32.0, 46.0, 57.0, 75.0] |
| 40 | 30.7000 | 0.1052 | 0.0475 | 0.0310 | [0.0, 8.0, 17.0, 26.0, 37.0, 50.0, 58.0, 71.0, 85.0] |
| 50 | 31.0000 | 0.0578 | 0.0598 | 0.0578 | [6.0, 18.0, 29.0, 40.0, 50.0, 60.0, 71.0, 82.0, 94.0] |
| 60 | 30.6000 | 0.0310 | 0.0475 | 0.1052 | [15.0, 29.0, 43.0, 51.0, 63.0, 74.0, 83.0, 92.0, 100.0] |
| 65 | 29.9000 | 0.0226 | 0.0413 | 0.1400 | [20.0, 36.0, 50.0, 60.0, 71.0, 80.0, 89.0, 96.0, 100.0] |
| 70 | 28.8000 | 0.0164 | 0.0351 | 0.1839 | [25.0, 43.8, 55.0, 68.0, 78.0, 87.0, 94.0, 99.0, 100.0] |
| 80 | 25.2000 | 0.0086 | 0.0227 | 0.3016 | [40.0, 60.0, 74.0, 84.0, 92.0, 97.0, 100.0, 100.0, 100.0] |

---

## 3. Classes (b) and (c) — the mean of k slider items

Compositing changes the shape a lot, and it does so through exactly three
mechanisms. All three are reproduced automatically by
`shape_lib.composite_sample`, which draws k *dependent* slider items through a
t-copula and averages them.

| scale | k | rbar | mean | SD_comp | SD_item | SD_classical | P(0) | P(100) | P(int) | min_j P(item=100) | ratio |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Belief_Pre | 3.000 | 0.539 | 65.185 | 22.409 | 27.003 | 22.474 | 0.003 | 0.021 | 0.345 | 0.028 | 0.750 |
| Concern_Pre | 3.000 | 0.902 | 60.583 | 31.046 | 32.113 | 31.043 | 0.019 | 0.058 | 0.395 | 0.076 | 0.774 |
| Policies_Pre | 3.000 | 0.819 | 67.831 | 28.648 | 30.486 | 28.593 | 0.010 | 0.160 | 0.461 | 0.192 | 0.831 |
| Intent_Pre | 4.000 | 0.689 | 34.535 | 27.838 | 31.835 | 27.882 | 0.055 | 0.011 | 0.322 | 0.029 | 0.375 |
| PoliciesSp_Pre | 4.000 | 0.509 | 52.670 | 23.512 | 29.583 | 23.519 | 0.011 | 0.014 | 0.277 | 0.034 | 0.415 |
| Candidate_Pre | 4.000 | 0.423 | 34.741 | 21.400 | 28.415 | 21.403 | 0.064 | 0.001 | 0.319 | 0.007 | 0.198 |
| Companies_Pre | 3.000 | 0.817 | 72.175 | 26.277 | 27.984 | 26.221 | 0.006 | 0.180 | 0.477 | 0.215 | 0.836 |
| IntentNp_Pre | 6.000 | 0.389 | 54.651 | 22.682 | 32.471 | 22.754 | 0.004 | 0.011 | 0.181 | 0.059 | 0.179 |

1. **SD shrinks by the classical factor** `sqrt((1 + (k−1)·r̄)/k)`. Column
   `SD_classical` vs `SD_comp` above: agreement to **< 0.3 %** on all 8 scales.
   This is the single most useful composite fact: a k=12 scale with r̄ = 0.66 has
   SD = 0.83 × the item SD; a k=7 scale with r̄ = 0.42 has SD = 0.68 × item SD.
2. **The 1/k lattice.** P(the composite is an integer) drops from 1.00 to 0.46
   (k=3), 0.32 (k=4), 0.18 (k=6). Support size is k·100 + 1. Any synthesiser
   that emits composites off the 1/k lattice is instantly distinguishable from
   the humans on a fine grid.
3. **Endpoint masses collapse**, because the composite is at the ceiling only if
   *every* item is: `P(comp = 100) ≈ c(r̄) · min_j P(item_j = 100)` with
   c ≈ 0.8 for r̄ > 0.8, ≈ 0.4 for r̄ ≈ 0.5–0.7, ≈ 0.18 for r̄ ≈ 0.4 (column
   `ratio`). Correspondingly, excess kurtosis rises toward 0 as k grows and r̄
   falls — a k=7, r̄=0.42 composite is nearly Gaussian in the interior.

### Inter-item correlations for the target's own scales

Computed from `tisp` US (n = 2,559) — which fields *the exact 12-item,
four-dimension trust-in-scientists scale the target uses*, the same four
policy-role items, and 5 of the target's 7 specific-policy items — and from
`voelkel2026`.

| target composite | k | r̄ | source | Cronbach α implied |
|---|---|---|---|---|
| `trust_competence` | 3 | 0.657 | tisp US (expert/intellig/qualified) | 0.85 |
| `trust_integrity` | 3 | 0.674 | tisp US (honest/ethical/sincere) | 0.86 |
| `trust_benevolence` | 3 | 0.635 | tisp US (concerned/improve/otherint) | 0.84 |
| `trust_openness` | 3 | 0.699 | tisp US (open/trans/otherviews) | 0.87 |
| **`trust_multidimensional`** | 12 | **0.613** | tisp US, all 12 items | 0.95 |
| (same, at the subscale level) | 4 | 0.774 | tisp US, 4 subscale means | 0.93 |
| `policy_role_mean` | 4 | 0.594 | tisp US `NORMPERC_*` — literally the same 4 items | 0.85 |
| `concern_mean` | 3 | 0.902 | voelkel2026 `Concern_Pre_1..3` (0–100 sliders) | 0.96 |
| `policy_specific_mean` | 7 | 0.390 | tisp US `CLIM_POLSUPPORT_*`, 5 of the 7 items | 0.82 |
| `behavior_mean` | 6 | 0.389 | voelkel2026 `IntentNp_Pre_1..6`, a 6-item intention battery | 0.79 |
| `inst_trust_mean` | 5 | **0.60 (assumed, band .45–.75)** | no direct train anchor — see below | 0.88 |

Caveats you must carry:
* tisp items are 1–5 Likert, the target's are 0–100 sliders. Coarse
  discretisation attenuates correlations by roughly 5–8 %, so the slider r̄ is
  probably a little *higher*. `shape_lib`'s defaults apply a +8 % adjustment to
  the tisp-derived values (0.613 → 0.66, 0.657–0.699 → 0.72, 0.594 → 0.64) and
  leave the two slider-derived values alone.
* `inst_trust_mean` (EPA / NASA / NOAA / universities / federal government) has
  **no clean train anchor**. Bounds: same-target multi-item grids in
  voelkel2026 give r̄ ≈ 0.82 (`Companies`, 3 items); a genuinely heterogeneous
  institution battery (Pew ATP W42: elected officials / media / military /
  scientists / religious leaders / principals / business) would give far less.
  EPA/NASA/NOAA are one facet, universities and the federal government two
  others, so 0.60 (α ≈ 0.88) is the working value; 0.45–0.75 changes the
  composite SD by only ±9 %, so the exposure is small. **Flagged as the weakest
  number in this file.**
* `concern_mean`: voelkel2026's Concern battery is very tight (r̄ = 0.90); the
  target's third concern item ("relative to other issues…") is more distinct, so
  the library default is shaded down to 0.85.

Model output at a common mean of 65 for each target composite class:

| cls | k | rbar | sd_at_65 | p0 | p100 | kurt | lattice |
|---|---|---|---|---|---|---|---|
| trust_subscale | 3 | 0.7200 | 26.9000 | 0.0086 | 0.0638 | -0.6500 | 1/3 |
| trust_multidimensional | 12 | 0.6600 | 24.7000 | 0.0021 | 0.0182 | -0.5300 | 1/12 |
| policy_role_mean | 4 | 0.6400 | 25.5000 | 0.0049 | 0.0411 | -0.5500 | 1/4 |
| concern_mean | 3 | 0.8500 | 28.6000 | 0.0129 | 0.0892 | -0.7800 | 1/3 |
| inst_trust_mean | 5 | 0.6200 | 24.8000 | 0.0039 | 0.0318 | -0.5200 | 1/5 |
| policy_specific_mean | 7 | 0.4200 | 21.0000 | 0.0007 | 0.0081 | -0.2300 | 1/7 |
| behavior_mean | 6 | 0.4200 | 21.3000 | 0.0010 | 0.0104 | -0.2500 | 1/6 |

---

## 4. Class (d) — donation out of a $10 endowment

The target item: *"Of the $10 bonus, how much would you like to donate to the
American Meteorological Society (AMS)?"*, whole dollars, integers 0–10,
`scale_range = 10` so **$0.10 = 1.0 pp**.

Two train anchors bracket the family:

**(A) voelkel2026 bonus allocation** (n = 13,173; allocate a bonus across 5
climate organisations vs keep). On its native 0–100 scale: mean 60.5, SD 45.4,
skew −0.45, **excess kurtosis −1.67**, P(0) = 0.317, P(100) = 0.481, P(50) =
0.045; deciles 0,0,0,0,50,90,100,100,100,100. Collapsed to $0–$10 bins:

| $ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| % | 32.6 | 0.8 | 1.6 | 0.5 | 0.6 | 4.5 | 0.9 | 0.9 | 4.9 | 3.5 | 49.2 |

mean $6.05, SD $4.55. Shape: **strongly U-shaped / bimodal**, mass at the two
ends, a clear "give exactly half" spike.

**(B) spampatti2023 WEPT** (n = 6,816), a *costly* effort-donation, rescaled to
$0–10: P(0) = 0.493, then monotone decay 16.0, 10.5, 6.6, 4.5, 3.2, 3.2, 3.7,
3.2 %; mean $2.01, SD $2.82. Shape: **zero-inflated, monotone decaying, tiny
ceiling mass**.

(For completeness, voelkel2024's `PA_DG` dictator game is a *third* family: 48 %
sit exactly on the equal split. It is anchored on "half", not on 0/all, and is
**not** the right analogue for a donate-to-a-charity item.)

### Mean-indexed recipe

Pooling 18 voelkel2026 party × age cells (cell means $5.16–$7.39) with 29
spampatti ideology × country cells (cell means $1.33–$3.23) gives a single smooth
family over $1.3–$7.4:

* `logit P($0)  = 0.3712 − 0.1945 · mean$`   (R² = 0.76)
* `logit P($10) = −5.4682 + 0.8964 · mean$`  (R² = 0.95)
* `SD = 1.937 + 0.420 · mean$`               (R² = 0.89)
* interior $1–$9 from a bounded heaped Beta with a $5 multiplier of **5.8×**
  (measured: the $5 bin holds 4.52 % against ~0.78 % log-interpolated from $4/$6)

| mean $ | P($0) | P($10) | SD |
|---|---|---|---|
| 1 | 0.544 | 0.010 | 2.36 |
| 2 | 0.496 | 0.025 | 2.78 |
| 3 | 0.447 | 0.058 | 3.20 |
| 4 | 0.400 | 0.132 | 3.62 |
| 5 | 0.354 | 0.272 | 4.04 |
| 6 | 0.311 | 0.478 | 4.46 |
| 7 | 0.271 | 0.691 | 4.88 |

**P($0) is the fragile parameter.** The two anchors disagree about its *level* at
a given mean (WEPT sits ~0.10 above the allocation extrapolation), because they
differ in whether the money is a windfall being split or a real cost. The target
is a windfall being split (family A) but with a genuine forgone bonus (family B);
the pooled fit deliberately sits between them. If you have a view about the mean,
you can bound P($0) ∈ [0.30, 0.55] almost regardless of it.

---

## 5. Class (e) — binary opt-in

Shape is fully determined by the mean, so only the base rate matters. Train
anchors for *behavioural* opt-ins measured inside an online survey:

| anchor | task | rate |
|---|---|---|
| koetke2024 Study 4 | behavioural follow-through (`Switch`) | **28.9 %** (107/370) |
| vlasceanu2024 US | agree to share the climate message on social media | **45.3 %** (3,734/8,242) |

A newsletter subscription is a lower-cost, lower-salience commitment than
sharing but requires a positive click; the two anchors bracket it. Sample as
`Bernoulli(p)`; there is nothing else to get right. Note `scale_range = 1`, so
**1 percentage point of sign-up rate = 1.0 pp of the score**, which makes this
the outcome where a base-rate error is scored most brutally.

---

## 6. How the shape moves between control and a treated arm

This is what drives the variance-ratio column, and the answer is clean.

Estimated on voelkel2026, 13 arms × 9 post-treatment outcomes (117 arm × outcome
cells), with outcome fixed effects:

| quantity | estimate | s.e. | reading |
|---|---|---|---|
| d SD / d mean | **+0.021** | 0.040 | n.s. — **variance ratio = 1.003 for a +2 pp ATE** |
| d P(ceiling) / d mean | +0.0036 | 0.0007 | +0.7 pp of ceiling mass per +2 pp ATE |
| d P(floor) / d mean | −0.0010 | 0.0004 | −0.2 pp of floor mass per +2 pp ATE |
| d logit P(ceiling) / d mean | +0.094 | 0.030 | (equivalent, on the log-odds scale) |
| d q10 / d mean | 0.98 | | |
| d q25 / d mean | 1.19 | | |
| d q50 / d mean | 1.18 | | |
| d q75 / d mean | 1.07 | | |
| d q90 / d mean | 0.93 | | |

**A +2 pp ATE shifts the whole distribution, it does not move mass.** Every
decile moves by ~1.0–1.2 × the ATE; the SD does not change; the endpoint masses
change only by the small amount that the shift pushes across the boundary.
Therefore:

* **Predict variance ratio ≈ 1.00 for all 16 × 13 treated cells.** Anything else
  is noise-fitting. (The only outcome where I would allow a deviation is
  `donation_ams`, where the mass sits on the two endpoints so a mean change
  mechanically changes the variance: `d SD/d mean = +0.42` per dollar.)
* Do **not** rebuild a treated arm's shape from scratch at its own mean using the
  cross-item law in §2. The cross-*item* SD law (dSD/dmean ≈ −0.30 pp per pp at
  mean 70) reflects different item *content*, not treatment response, and would
  give a variance ratio of 0.975 instead of 1.003 for a +2 pp ATE — a 3 % error
  on every treated cell. `shape_lib.sample(..., control_mean=…)` handles this by
  locking the treated arm's SD to the control arm's SD.

---

## 7. Using `shape_lib.py`

```python
import numpy as np, shape_lib as S
rng = np.random.default_rng(0)

ctrl = S.sample("trust_multidimensional", 1200, 62.4, rng)          # control arm
trt  = S.sample("trust_multidimensional", 600, 64.1, rng,
                control_mean=62.4)                                   # treated arm
don  = S.sample("donation_ams", 600, 3.10, rng)                      # $0-10 ints
nl   = S.sample("newsletter_signup", 600, 0.27, rng)                 # 0/1

vals, p = S.pmf("trust_post", 61.0)          # the exact pmf on 0..100
S.composite_sd(item_sd=29.0, k=12, rbar=0.66)  # classical composite SD
```

Optional keywords: `sd_target` (item SD), `rbar`, `k`, `item_means` (a length-k
list — use it when a scale mixes an extreme item with a moderate one, since the
composite's ceiling mass is governed by the *least* extreme item), `df`
(copula tail dependence; 3 by default, `None` for a Gaussian copula).

`/opt/kernel/venv/bin/python shape_lib.py` runs the self-test: 15 classes checked
against their empirical mean / SD / P(floor) / P(ceiling), plus lattice, heaping
and treated-arm checks. Runtime ~7 s, numpy + scipy only.

---

## 8. Limitations, honestly

1. **P(50) is poorly predicted** by the mean (R² = 0.18; items range 0.006–0.101).
   If a target item has an explicit midpoint label its P(50) will be higher than
   the library's default — `funding_5` is exactly such an item ("0 = far too
   little, **50 = about right**, 100 = far too much"), so I would raise its
   midpoint mass to ~0.12–0.20 by hand. `distrust_post` and `trust_post` have no
   midpoint label and should use the default.
2. **Item heterogeneity within a composite** is the residual error. The library
   assumes identical marginals unless you pass `item_means`; with equal
   marginals it over-predicts the composite ceiling mass by ~0.014 on average
   (e.g. `Belief_Pre`: 0.035 predicted vs 0.021 observed), because in reality the
   *least* extreme item caps the composite.
3. **Reflected outcomes.** `funding_perceptions = 100 − funding_5` and
   `distrust_post` are not reverse-coded. The slider law is not symmetric in the
   mean once you condition on item content, but the fitted endpoint law *is*
   symmetric by construction, so reflecting is safe: shape(m) reflected =
   shape(100 − m).
4. **The slider UI matters.** If the target's respondents behave like
   `hackenburg2025`'s (P(mult of 5) 0.66 instead of 0.40), the heaping profile
   should be sharpened ~2×. I judge that unlikely: the target's QSF matches
   `vlasceanu2024` exactly, including `GridLines = 10` and `ShowValue`.
5. **Low-r̄, high-k composites are nearly Gaussian** and the library gives no
   advantage there (`policy_specific_mean` k=7 r̄=.42, `behavior_mean` k=6
   r̄=.42). It still gives the right 1/k lattice, which a Gaussian never will.
6. `inst_trust_mean`'s r̄ is assumed, not measured (§3).
7. The donation family is extrapolated from two tasks that are not the target's
   task; the *shape family* (U-shaped with a half-spike, or zero-inflated
   decaying) is well supported, the *P($0) level* is not.
