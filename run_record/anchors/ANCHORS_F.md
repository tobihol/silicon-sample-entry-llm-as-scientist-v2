# ANCHORS_F — party (and other-moderator) x message-family MODERATION PRIOR, train split only

Run: idea_03, sub-agent job "party x message-family moderation prior".
Scope: `/workspace/datasets/*` (TRAIN) + `/workspace/benchmark` (design only) + `/workspace/run/anchors/levels.csv`
(itself a train-split product). **No validation data, no `runs/`, no `inputs/`, no web, no retrieval,
no remembered published numbers.** Every number below was computed in this session from respondent-level
train data. Python: `/opt/kernel/venv/bin/python`. One package was installed from PyPI (`openpyxl 3.1.5`,
needed for `vlasceanu2024/data63.xlsx`); that is the one permitted network use.

Machine-readable companions in `/workspace/run/anchors/`:
`moderation_prior.csv` (33 rows, the headline table), `headroom_rule_coefficients.csv`,
`headroom_rule_LOSO_shrinkage.csv`, `moderator_ceilings.csv`, `party_headroom_gaps_by_construct.csv`.

Everything is in **percentage points of each outcome's scale range**.
"Interaction contrast" for a cell = `ATE(arm, outcome | level A) - ATE(arm, outcome | level B)`,
which is exactly what Section 2 of the target scores.

---

## 0. THE METHOD FIX THAT CHANGES THE ANSWER — read this first

My first pass reproduced the standard result you would get from naive SEs: a clear, headroom-shaped
condition x party interaction in the design twin, split-half-corrected `sd_true = 0.73 pp`, and a
headroom model with `R2 = 0.88`. **That was an artifact and it is now retracted.**

All arms in a megastudy share **one control group**. The k arm-level ATEs within an outcome are
therefore positively correlated (`Cov(ATE_a, ATE_b) = Var(control mean)`), and the same is true of the
interaction contrasts. Treating the cells as independent:

* **understates** the SE of any average over arms (v26 party grand mean: naive SE 0.152, correct 0.315 — 2.1x),
* **overstates** the within-outcome (arm-specific) noise floor, so arm-specific structure looks smaller than it is,
* and **understates** the between-outcome noise floor, so outcome-level structure looks bigger than it is.

Everything below uses the **full covariance matrix of the whole cell vector**, built from per-respondent
influence functions of each within-subgroup ANCOVA (`IF_i = (X'X)^-1 x_i r_i`, sandwich; subgroup levels
are disjoint sets of respondents so `Cov(ATE^A, ATE^B) = 0`, but arms and outcomes inside a level are
fully covaried). Wald statistics are `c' V^-1 c`.

**The machine is placebo-calibrated.** Random 50/50 "fake moderator" splits of the same respondents:
voelkel2026 null `chi2` mean 96.7 (df 90, sd 14.5, 95th pct 118.1) over 18 draws;
voelkel2024 null `chi2` mean 194.0 (df 200, sd 26.4, 95th pct 225.6, max 263.3) over 20 draws.
So the machine is very slightly anti-conservative in v26 and has fatter-than-chi2 tails in v24;
I use the **empirical** placebo quantiles, not the nominal ones, for every verdict.

---

## 1. What was mined

| study | design | n | arms | outcomes | moderators used | estimator |
|---|---|---|---|---|---|---|
| `voelkel2026` (CCC) | **the target's design twin** — climate messages, all outcomes 0-100 sliders, pre+post | 13,821 | 10 + pooled control (n=3,183) | 9 (8 attitude + Donation) | party3, ideology7, education3, age, gender, race5, income | ANCOVA on the pre-measure |
| `voelkel2024` (SDC) | democracy megastudy, post-only (out of domain, kept as a power check) | 34,119 | 25 + null control | 8 | party3, ideology, education, age, gender, race | DIM |
| `vlasceanu2024` global | 63-country climate tournament; country x ideology-tertile cell demeaning | 59,440 | 11 + control | 4 (Belief, Policy, Sharing 0/1, WEPT 0-8) | within-country ideology tertiles | DIM |
| `vlasceanu2024` US | US subsample of the same | 8,253 | 11 + control | 4 | US ideology tertiles | DIM |
| `geiger2026` / van der Linden 2019 US consensus RCT | 1 message vs control, pre+post | 6,301 | 1 + control | 6 (belief, cause, worry, policy, certainty 1-7; consensus 0-100) | party (2-level) | ANCOVA |

Datasets checked and **not** usable for a condition x party interaction: `gligoric2025` (message arms
randomised among conservatives only — no party contrast exists), `koetke2024` (political conviction only,
no party), `agley2021`/`wellcome` (no party), `hackenburg2025` (730 arms x ~26 respondents/arm — the
per-arm interaction SE is ~14 pp, uninformative), `spampatti2023` (outcome semantics per-statement, not
arm-level; skipped rather than risk a garbage anchor), `attari2016` (no control arm),
`schmidbetsch2019` (presence-of-advocate contrast, not message content).

---

## 2. ANSWER TO Q1 — how big is a condition x party interaction contrast, noise-corrected

`rms_true` = sqrt(max(mean(c^2) - trace(V)/n, 0)), i.e. the noise-corrected root-mean-square of the whole
cell vector **including its mean**. `UB95` adds `1.645 * sqrt(2*trace(V@V))/n`.

| study | moderator | cells | grand mean +/- SE | mean per-cell noise SD | **rms_true** | rms_true UB95 | omnibus `chi2`/df (p) |
|---|---|---|---|---|---|---|---|
| voelkel2026 | party R-D, all 9 outcomes | 90 | **-0.36 +/- 0.32** | 1.44 | **0.80** | 1.38 | 87.7/90 (0.55) |
| voelkel2026 | party R-D, 8 attitude sliders | 80 | **-0.26 +/- 0.22** | 0.89 | **0.57** | 0.78 | — |
| voelkel2026 | ideology Con-Lib | 90 | -0.32 +/- 0.35 | 1.61 | 0.56 | 1.40 | 82.0/90 (0.71) |
| voelkel2024 | party R-D (non-climate) | 200 | +0.02 +/- 0.40 | 1.73 | **0.00** | 0.43 | 204.5/200 (0.40) |
| vlasceanu global | ideology, Belief+Policy only | 22 | +0.21 +/- 0.75 | 1.12 | **0.00** | 0.89 | 22.4/22 (0.43) |
| vlasceanu global | ideology, Sharing+WEPT (behavioural) | 22 | **-3.73 +/- 1.32** | — | **3.70** | 4.40 | 42.9/22 (0.005) |
| vlasceanu US | ideology | 44 | +0.47 +/- 2.58 | 4.94 | 3.42 | ~5 | 75.3/44 (0.002)* |
| geiger/vdL2019 | party R-D | 6 | **+2.39 +/- 0.63** | 1.09 | **3.53** | 3.72 | 42.0/6 (<1e-6) |

`*` vlasceanu-US is nested inside vlasceanu-global; treat it as the same study.

**Headline for Q1.** On **0-100 attitude sliders in a properly powered multi-arm climate megastudy**, the
noise-corrected dispersion of the condition x party interaction contrast is **0.5-0.8 pp**, and the
omnibus test cannot reject zero (v26: `chi2 = 87.7` on 90 df against an empirical null whose mean is 96.7 —
the observed statistic is literally *below* the placebo mean). The 95% ceiling is **~1.4 pp**.

Two places where it is genuinely bigger:
* **Behavioural / binary / effortful outcomes** (vlasceanu Sharing 0/1 and WEPT): `rms_true = 3.7 pp`,
  grand mean **-3.7 +/- 1.3 pp** against conservatives. In v26 the Donation outcome carries all of the
  excess variance too (per-outcome excess `+3.38 pp^2` vs negative excess for all 8 attitude outcomes).
* **A single-arm study whose outcome is the message's own claim** (vdL2019: the message states "97% of
  scientists agree"; the outcome is "what % agree?"). There the R-D interaction is +7.06 +/- 1.14 pp on
  perceived consensus and +5.56 +/- 1.50 on certainty. The target study has no such outcome.

---

## 3. ANSWER TO Q2 (THE KEY QUESTION) — multiplicative headroom vs content-specific

### 3a. Variance decomposition of the interaction table

Two-way (arm x outcome) decomposition of the v26 party interaction vector, with the full covariance:

| component | observed SD | noise SD | **true SD** | GLS test |
|---|---|---|---|---|
| grand mean | -0.355 | 0.315 | — | t = -1.13, ns |
| **outcome main effect** (all arms move together on an outcome) | 0.843 | 0.796 | **0.28** | `d chi2 = 21.9` on 8 df — **exceeds all 14 placebo draws** (placebo mean 7.5) |
| arm main effect (a message has a party signature across outcomes) | 0.755 | 0.505 | 0.56 | `d chi2 = 10.2` on 9 df (placebo mean 8.1) — **ns** |
| arm x outcome residual | 1.339 | 1.212 | 0.57 | `chi2 = 52.9` on 72 df (placebo mean 68.6) — **ns** |

Per-outcome, the observed within-outcome variance of the interaction contrasts is **below the noise floor
for all 8 attitude outcomes** (excess = -0.17, -0.16, -0.25, -0.17, -0.42, -0.58, -0.59, -0.17 pp^2);
only Donation is positive (+3.38 pp^2, on a noise floor of 12.2 pp^2, i.e. itself noise).
voelkel2024: arm main effect p = 0.66, arm x outcome p = 0.22, nothing.
vlasceanu global on Belief+Policy: `chi2 = 22.4` on 22 df.

> **There is no detectable content-specific (arm-level) party interaction anywhere in the train split.**
> The only reliable structure is a per-OUTCOME party differential shared by every arm.

### 3b. Does headroom explain the per-outcome component?

Signed headroom `H(o, l) = 100 - baseline(o, l)` for outcomes the messages push **up**, and
`= baseline(o, l)` for outcomes they push **down** (the target's `distrust_post` is the down case).
`hgap(o) = (H_R - H_D)/H_all`. Marginal ATE on outcome o is `am(o)`.
GLS fits of the outcome-level contrast vector `m(o)` (full covariance):

| model | v26 party resid `chi2`/df | geiger resid `chi2`/df |
|---|---|---|
| zero | 25.2/9 (p=0.003) | 42.0/6 (p<1e-6) |
| constant only | 23.0/8 (0.003) | 36.4/5 (<1e-6) |
| const + b*`am` (pure proportional) | 22.8/7 (0.002) | 6.6/4 (0.16) |
| const + b*(H_R-H_D) (raw headroom, pp) | **3.3/7 (0.86)** | 15.5/4 (0.004) |
| const + b*`hgap` (relative headroom) | 5.7/7 (0.58) | 15.3/4 (0.004) |
| **const + lambda * `am` x `hgap` (ATE-scaled headroom)** | **1.6/7 (0.98)** | **4.5/4 (0.35)** |

The **ATE-scaled headroom model is the only one that fits both**:

```
interaction(o) = delta + lambda * am(o) * (H_R(o) - H_D(o)) / H_all(o)
```

| study | delta (pp) | lambda | LOO-CV R^2 on outcome-level true variance |
|---|---|---|---|
| voelkel2026, party | **-2.264 +/- 0.473** | **2.840 +/- 0.614** | **1.00** |
| voelkel2026, ideology (same n, different moderator) | -1.952 +/- 0.547 | 2.218 +/- 0.618 | 1.00 |
| geiger/vdL2019, party | -1.736 +/- 0.799 | 1.457 +/- 0.258 | 0.97 |
| vlasceanu global, ideology | -0.103 +/- 0.698 | 10.55 +/- 4.00 | -1.54 |
| voelkel2024, party (non-climate) | -0.079 +/- 0.361 | -0.21 +/- 2.06 | n/a (no signal) |

**So the headroom model, in its ATE-scaled form, explains essentially 100% of the outcome-level party
interaction wherever that interaction exists.** `headroom_model_r2` in `moderation_prior.csv` is this
number. But note the two failure modes:

1. **`delta` and `lambda` are collinear inside a study** (v26's outcomes all sit at `hgap` 0.17-1.03,
   so `delta` is an extrapolation to `hgap = 0`) and they **do not agree across studies**: `delta` is
   ~-2 pp in the two climate studies with big party gaps and ~0 in voelkel2024 / vlasceanu, where the
   party headroom gap is itself ~0. Fitting `delta = -2.13` and applying it to voelkel2024 would predict
   about -2 pp per cell where the truth is 0.02 +/- 0.40.
2. The **naive unscaled multiplicative model fails badly**: through-origin `c = gamma * am * hgap` gives
   `gamma = 0.047 +/- 0.124` in v26 (i.e. **zero**), even though Republicans have 1.2x-3.1x the headroom
   of Democrats on those outcomes. Republicans do *not* move proportionally more just because they are
   further from the ceiling; the proportional gain is almost exactly cancelled by a flat responsiveness
   penalty.

### 3c. Honest leave-one-STUDY-out transfer test

Fit `(delta, lambda)` on the other studies, predict the held-out study's cells, sweep a shrinkage
`kappa` on the prediction, and score noise-corrected cell-level MSE (pp^2). `kappa = 0` is the exact-zero floor.

| kappa | voelkel2026 | geiger | voelkel2024 | vlasceanu | **mean** |
|---|---|---|---|---|---|
| 0.0 (exact zero) | 0.639 | 12.450 | 0.000 | 6.518 | **4.902** |
| 0.3 | 0.353 | 0.901 | 0.000 | 4.158 | 1.353 |
| **0.5** | 0.244 | 0.000 | 0.634 | 3.157 | **1.009** |
| 0.7 | 0.199 | 3.822 | 1.761 | 2.614 | 2.099 |
| 1.0 (rule as fitted) | 0.253 | 19.753 | 4.143 | 2.658 | 6.701 |

**A non-zero party prior is defensible only at about half strength.** At `kappa = 0.5` the transferred
headroom rule cuts average held-out true MSE from 4.90 to 1.01 pp^2 (rmse 2.21 -> 1.00 pp) and helps
3 of 4 held-out studies; at full strength it is *worse than zero* on average. The one study it hurts at
`kappa = 0.5` is voelkel2024 (+0.63 pp^2 where the truth is exactly 0).

**Recommended transferable rule (brief-only, no fitting on the target):**

```
interaction_pp(arm, outcome, R minus D) = 0.5 * ( -2.13 + 1.665 * am(outcome) * hgap(outcome) )
```

identical for every arm (no arm term), with `am(outcome)` = your own predicted marginal ATE for that
outcome and `hgap` from party baselines. Pooled coefficients from v26 + geiger; `n = 20,122`.
Everything else in Section 2 stays at exact zero.

**Caveat I want on the record.** This rule is carried by two studies, its intercept is an extrapolation,
and its most spectacular success (geiger) is a design the target does not share (single arm, outcome =
the message's literal claim). The target's 13 outcomes are attitude sliders like v26's, where the whole
true signal is `rms 0.57 pp`. If you want one number: on the target's 11 attitude outcomes, the honest
expectation is that the exact-zero floor loses only ~0.5 pp rmse, and the rule can recover at most
about half of that.

---

## 4. ANSWER TO Q3 — message families and backfire

### 4a. Family x party in the design twin

voelkel2026's 10 arms grouped by content (the closest available analogue of your target families;
v26 has no integrity/conflict-of-interest or scientist-as-person arm, so those two target families are
**unanchored**):

| family (v26 arms) | cells | R-D interaction (pp) | t |
|---|---|---|---|
| CONS_VALUES (Purity, Binding, Free Market, System Preservation) | 36 | **+0.11 +/- 0.37** | +0.28 |
| DISTANCE (High Social Distance) | 9 | -0.23 +/- 0.56 | -0.42 |
| EVIDENCE / CONSENSUS (Consensus 1, Consensus 2) | 18 | **-0.50 +/- 0.45** | -1.11 |
| WARMTH (Warmth Framing) | 9 | **-0.79 +/- 0.54** | -1.47 |
| THREAT (Gains, Dire-But-Solvable) | 18 | -0.97 +/- 0.45 | -2.15 |

Family contrasts: CONS_VALUES - EVIDENCE `+0.61 +/- 0.44`; CONS_VALUES - WARMTH `+0.90 +/- 0.53`;
EVIDENCE - WARMTH `+0.29 +/- 0.59`. **Omnibus family x party `chi2 = 3.77` on 4 df, p = 0.44.**

> **Largest observed family x party differential = ~0.9 pp (values-matched framing vs warmth framing),
> in favour of Republicans, and it is not distinguishable from zero.** The direction is the one theory
> predicts (moral-reframing arms relatively better on Republicans; warmth and evidence arms relatively
> better on Democrats), but the evidence does not license a signed family term.

One cross-study hint pointing the same way and also not significant: in geiger/vdL the *evidence*
message (consensus) had a **+2.4 pp** R-D advantage — the opposite sign to v26's EVIDENCE cell. Two
studies, opposite signs, neither individually decisive. **Do not sign a family term.**

### 4b. Backfire among Republicans

Republican-only subgroup ATEs, all arms x outcomes:

| study / level | cells | mean ATE (pp) | % negative | **% significantly negative (p<.05)** | min |
|---|---|---|---|---|---|
| voelkel2026 Republicans | 90 | +0.78 | 23.3% | **1.1%** (1 cell) | -6.57 |
| voelkel2026 Republicans, 8 attitude outcomes only | 80 | +1.06 | 16.2% | **0%** | -0.77 |
| voelkel2026 Democrats | 90 | +1.14 | 13.3% | 1.1% | -3.44 |
| vlasceanu global Conservatives | 44 | +0.45 | 29.5% | **11.4%** (5 cells) | -9.17 |
| vlasceanu global Liberals | 44 | +2.21 | 20.5% | 6.8% | -6.08 |
| geiger/vdL Republicans | 6 | +8.79 | 0% | 0% | +1.66 |

The single significantly-negative Republican cell in v26 is `Gains Framing x Donation` (-6.57 +/- 2.64),
a behavioural outcome. **All five** significantly-negative conservative cells in vlasceanu are `WEPT`
(the effortful tree-planting task) — and liberals are negative there too, so it is an outcome property,
not a party backfire. On attitude sliders the Republican mean ATE is **positive on every single outcome**
in v26 (+0.29 to +1.68 pp).

> **Backfire among Republicans on attitude outcomes: 0 of 80 cells in the design twin, 0 of 22 in
> vlasceanu's attitude outcomes. It does not exist at a size you could detect with n=18,000.**
> The Republican/Democrat ATE *ratio* is 0.69 over all 9 v26 outcomes but **0.81 on the 8 attitude
> outcomes** (Rep +1.06 vs Dem +1.32 pp); 0.20 in vlasceanu (dragged down by the behavioural outcomes;
> on Belief+Policy alone conservatives average +1.59 pp with min -0.32); 1.37 in geiger. A defensible
> statement is "Republicans respond about 70-80% as much as Democrats on attitude outcomes, and never
> negatively".

---

## 5. ANSWER TO Q4 — the other five moderators, and the measured ceiling on "near zero"

Grand mean of the whole cell vector and its noise-corrected dispersion, with the correct covariance:

| study | moderator (contrast) | cells | grand mean +/- SE | **rms_true** | **rms_true UB95** | omnibus p (empirical) |
|---|---|---|---|---|---|---|
| voelkel2026 | education (HS- vs BA+) | 90 | +0.15 +/- 0.37 | **0.00** | 1.11 | 0.11 nominal, ns empirical |
| voelkel2026 | age (60+ vs <40) | 90 | -0.42 +/- 0.36 | 1.05 | 1.68 | 0.50 |
| voelkel2026 | gender (M-F) | 90 | **-0.63 +/- 0.30** | 0.27 | 1.11 | 0.031 nominal, **ns vs empirical null (95th pct 118.1 vs observed 116.7)** |
| voelkel2026 | race Black-White | 90 | +0.55 +/- 0.46 | 0.00 | 1.60 | 0.35 |
| voelkel2026 | race Hispanic-White | 90 | -0.11 +/- 0.53 | 0.00 | 1.31 | 0.97 |
| voelkel2026 | income (low-high) | 90 | -0.27 +/- 0.37 | 0.00 | 1.09 | 0.49 |
| voelkel2024 | education | 200 | +0.08 +/- 0.52 | 0.00 | 0.90 | 0.40 |
| voelkel2024 | age | 200 | +0.54 +/- 0.45 | 1.11 | 1.49 | **<0.001, exceeds all 20 placebos; arm-main p<0.001** |
| voelkel2024 | gender | 200 | +0.10 +/- 0.37 | 0.40 | 0.90 | 0.071, ns empirical |
| voelkel2024 | race Black-White | 200 | +0.18 +/- 0.56 | 0.00 | 1.33 | 0.088, ns empirical |
| voelkel2024 | race Hispanic-White | 200 | -0.05 +/- 0.95 | 1.33 | 2.57 | **<0.001, exceeds all placebos** |

> **In the design twin, education / gender / race / income all have observed cell variance BELOW the
> noise floor (`rms_true` estimate = 0) with a 95% ceiling of ~1.1-1.6 pp, and every grand mean is
> within +/-0.65 pp of zero. An exact-zero floor for these five is honest.**

The two exceptions are both in `voelkel2024`, the out-of-domain democracy megastudy: **age** (real
arm-level moderation, `rms_true = 1.11 pp`) and **race Hispanic-White** (`rms_true = 1.33 pp`). Neither
replicates in the climate twin, and both sit in a domain where the outcomes (partisan animosity, support
for political violence) have demographic structure the climate outcomes do not. I would not transfer them.
The most I would say: **if you want a non-zero non-party moderator anywhere, age is the only candidate,
and its ceiling is ~1.0-1.7 pp with a point estimate of 0 in the climate twin.**

---

## 6. Inputs the rule needs — party headroom gaps by construct (train split)

From `levels.csv` (train-split control levels, weighted where weights exist). `hdiff = H_R - H_D` in pp;
positive = Republicans have more room in the direction messages push.

| construct | k rows | Democrat | Republican | **hdiff (pp)** |
|---|---|---|---|---|
| trust in scientists, **2019-2024 only** (ANES 20/24, GSS 21-24, Pew w42/w100/w114) | 9 | 78.1 | 59.2 | **+18.9** |
| trust in scientists, GSS 1973-2018 (31 waves) | 31 | 67.9 | 69.6 | **-1.7** (sign flipped historically — never average across the break) |
| trust in **environmental research scientists** (Pew W42, 5 items) | 6 | 75.0 | 59.1 | **+16.0** |
| trust in medical scientists | 4 | 76.3 | 63.6 | +12.7 |
| perceived scientific consensus | 1 | 72.4 | 60.8 | +11.5 |
| climate belief | 3 | 78.0 | 54.0 | +24.0 |
| climate policy support (general) | 1 | 82.0 | 62.1 | +19.8 |
| climate policies specific | 2 | 65.2 | 40.2 | +25.0 |
| climate concern | 3 | 77.5 | 39.6 | **+37.9** |
| climate worry | 1 | 71.4 | 46.3 | +25.1 |
| climate behaviour intent | 2 | 45.6 | 22.4 | +23.2 |
| climate intent (non-political) | 2 | 62.3 | 46.4 | +16.0 |
| climate candidate | 2 | 39.1 | 27.1 | +12.1 |

Full rows in `party_headroom_gaps_by_construct.csv`. Pew W135 climate-scientist competence items
(ENV26a-d, party-lean) run Dem 74-88 vs Rep 40-48, i.e. `hdiff` +30 to +40 — the largest gaps in the
train split, and the closest published-format analogue to the target's trust battery.

**Structural note for the target.** The trust-family constructs have a *smaller* party headroom gap
(+16 to +19) than the climate-attitude constructs (+20 to +38). Under the fitted rule, smaller `hgap`
means a *more negative* R-D interaction. So mechanically the rule predicts the target's trust outcomes
to have a slightly more negative R-D interaction than its belief/concern/policy outcomes — but every one
of these numbers is within +/-1 pp once `kappa = 0.5` is applied.

---

## 7. What I would actually submit for Section 2

1. **Every arm-specific term: exactly 0.** Measured ceiling on arm-specific party interaction SD is
   ~0.6 pp and the observed value is 0 in 3/3 powered studies. This is the single most defensible line
   in this document.
2. **Every education / gender / race / income term: exactly 0.** Ceiling 1.1 pp, point estimate 0.
3. **Age: 0**, with a noted 1.0-1.7 pp ceiling from the out-of-domain study.
4. **Party: either exactly 0, or the half-strength outcome-level headroom term** in section 3c, applied
   identically to all 16 arms within an outcome. The LOSO evidence says the half-strength rule beats
   exact zero on average across held-out studies (mean true MSE 1.01 vs 4.90 pp^2) but loses on the one
   study whose true interaction is exactly zero. On the target's attitude outcomes the whole quantity at
   stake is ~0.5 pp rmse.
5. **If the target's `donation_ams` and `newsletter_signup` get a party term at all, make it negative
   for Republicans**, of order -1.5 pp (range -5 to +1). These are the only cells where the train split
   shows a reliable non-zero party interaction (vlasceanu Sharing/WEPT: -3.7 +/- 1.3 pp; v26 Donation:
   -1.1 +/- 2.0 pp). Note `donation_ams` has scale_range 10 so $0.10 = 1.0 pp, and `newsletter_signup`
   has scale_range 1 so 1 percentage point of signup = 1.0 pp — a -1.5 pp party interaction on signup
   means Republicans' treatment lift is 1.5 signup-points smaller than Democrats'.

## 8. Recognition disclosure

I recognised voelkel2026, voelkel2024, vlasceanu2024 and van der Linden 2019 as published studies. No
published result, abstract or remembered number was used anywhere; every figure above was computed in
this session from the vendored respondent-level files, and where my computed numbers would differ from
a published headline (e.g. I use ANCOVA and a shared-control covariance the papers do not), mine stand.
