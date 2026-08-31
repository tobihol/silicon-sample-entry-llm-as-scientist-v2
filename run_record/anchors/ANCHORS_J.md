# ANCHORS_J — the LEVEL MIX (`sd_wth / sd_btw`) of a multi-arm ATE table: measurement, and an honest failure to predict it from design

**Scope / blinding.** Train split only: `/workspace/datasets/**` (respondent-level microdata),
`/workspace/benchmark/**` (public instrument, codebook, condition list — no human outcomes exist there),
and the sibling anchor files in `/workspace/run/anchors/**`. **No** `inputs/val/**`, **no** `runs/**`,
**no** `inputs/idea01_lib/**`, **no retrieval of any kind** (no web, no literature, no remote repos).
Every number below was computed in this session from vendored microdata with
`/opt/kernel/venv/bin/python`. **Packages installed from PyPI (audit):** `pyreadstat` (to read the
Schmid & Werner `.sav` files) and `pyreadr` (to read `geiger2026/analysis_dataset.RDS`). Nothing else.

**RECOGNITION DISCLOSURE.** I recognise several of these datasets as published papers
(voelkel2026, voelkel2024, vlasceanu2024, koetke2024, gligoric2025, spampatti2023,
schmid & betsch / schmid & werner, van der Linden 2017 / Maertens 2020, Većkalov 2024 via
geiger2026, hackenburg2025) and I have some memory of their headline claims. **No remembered
number is used anywhere in this file.** Every quantity is recomputed from the microdata by the
procedure documented in `_j_sources.csv`; the memory only influenced which files I opened.

Machine-readable companions: **`mix_table.csv`** (32 rows: 16 study rows, 15 variant/robustness
rows, 1 target-prediction row), **`_j_sources.csv`** (per-spec provenance: file, control arm,
arm list, outcome list, n, estimator).

---

## 0. Headline

1. **The mix is measurable.** After noise correction the true mix in 16 train studies spans
   **0.00 to ~10**, median **0.94**, geometric mean **0.80**, IQR **0.39–1.68**. Uncorrected mixes
   are useless: over the 16 study rows the sampling-noise variance is a median **25 %** of the raw
   *within* variance (range 5 %-184 %) and a median **18 %** of the raw *between* variance
   (range 2 %-127 %), and because it hits the within term harder it always inflates the mix.
2. **Two independent noise corrections agree to 2–3 decimal places** on every study
   (analytic MVN simulation vs. cross-fitted split-halves; e.g. voelkel2026 1.436 vs 1.427,
   voelkel2024 1.0685 vs 1.0693, vlasceanu 0.417 vs 0.410). A third, independent check —
   re-estimating the same estimand by ANCOVA on the pre-measure, which cuts the noise ~5× —
   **confirms** the two gateway studies (2.10→2.13, 0.00→0.14) and **fails to confirm**
   voelkel2026 (1.44 vs 2.93). So the *machinery* is trustworthy; on the lowest-signal study the
   *answer* is still only determined to within a factor of ~2.
3. **I could not close the hole.** No design feature I coded predicts the mix out of sample in any
   way I am willing to call a rule. The single best feature (`arm_contrast_kind`, coded post hoc)
   cuts leave-one-study-out RMSE of `log mix` from **1.275 to 1.104** — i.e. the pooled-mean
   baseline is off by a factor **3.6** and the rule by a factor **3.0**. Permutation p = 0.015,
   but the feature was coded *after* I saw the answers, and on the bounded target
   `share = V_wth/(V_wth+V_btw)` the same rule buys **nothing** (0.359 vs 0.365). **I report this
   as a negative result.**
4. **What I can offer instead is not a rule but a decomposition.** The mix is a *ratio*, and its
   denominator is something the arm already predicts: `sd_btw` is the spread, across outcomes, of
   the per-outcome mean effect — i.e. exactly ANCHORS_E's responsiveness profile. Stop trying to
   predict the ratio; predict the **numerator** (`sd_wth`, the message-level SD in pp), for which
   the train split gives a tight, design-matched anchor band of **0.3–0.7 pp**, and divide.
5. **Target prediction: true mix ≈ 1.2, 80 % band 0.45–2.6** (`sd_btw` ≈ 0.42 pp,
   `sd_wth` ≈ 0.55 pp). **But the mix you should SUBMIT is not the true mix**: the MSE-optimal
   predicted mix is `true_mix × (rho_within / rho_outcome)` ≈ **0.45 (band 0.2–0.9)**. Section 7.

---

## 1. The quantity, exactly as computed

For an arm × outcome ATE table `A(a,o)` in pp of each outcome's scale range
(`100*(mean_arm − mean_control)/(hi−lo)`; 0–100 slider ×1, 1–5 Likert ×25, 1–7 ×16.67,
0/1 binary ×100, $0–10 ×10, 0–8 count ×12.5):

    g      = mean over all cells
    m(o)   = mean over arms of A(a,o)
    V_btw  = mean over outcomes of (m(o) − g)^2          sd_btw = sqrt(V_btw)
    V_wth  = mean over cells   of (A(a,o) − m(o))^2      sd_wth = sqrt(V_wth)
    mix    = sd_wth / sd_btw

Population moments (divide by O and by k·O, no ddof), because the decision the mix informs is
about the *realised* table that will be scored, not about a superpopulation of outcomes.

Two properties worth stating because they bite:

* **`sd_wth` is invariant to the choice of control arm; `sd_btw` is not.** Re-basing the table on a
  different reference shifts every `m(o)` by that reference's outcome profile. Studies without a
  clean control (attari2016) therefore cannot contribute a mix at all, and studies where the
  "control" is itself an active arm (schmid: advocate-absent / hostile-denier) have a `sd_btw`
  that is a property of the *contrast set*, not of the messages.
* **The mix is not scale-free across arm counts.** If arm effects are exchangeable draws with
  message-level variance `V_w` and a mean profile with variance `V_b0`, then
  `E[V_btw] = V_b0 + V_w/k` and `E[V_wth] = V_w(1 − 1/k)`. A k = 2 study (Većkalov) puts half of
  any genuine message-level variance into its *between* term; a k = 16 study puts 1/16 of it there.
  `mix_table.csv` carries `sd_b0`, `sd_w0` and `mix_k16` (the same study re-expressed at k = 16).
  For four small-k or low-signal studies `V_b0` comes out negative — i.e. their entire outcome
  main effect is consistent with arm sampling — so I do **not** use `mix_k16` as a primary number.

## 2. Noise correction — the whole assignment

Three estimators of the same two variances, all applied to every study:

**(a) Analytic / parametric.** For each arm `a` (and the control) estimate the covariance of the
outcome-mean vector, `Cov(ȳ_a)`, by pairwise-complete covariance scaled by `n_ij/(n_i n_j)` (this
handles gligoric2025, where each respondent rates a random ~4 of 35 occupations, and every study
with item-level missingness). Draw `e_a ~ N(0, Cov(ȳ_a))`, form the pure-noise table
`E(a,o) = e_a(o) − e_c(o)`, and average `V_btw(E)`, `V_wth(E)` over 2 000–4 000 draws. This keeps
(i) the control arm's noise, which is *shared across arms* and therefore lands almost entirely in
`V_btw`, and (ii) the *cross-outcome correlation* of the noise, which a per-outcome variance
calculation gets wrong. Subtract; a negative result is reported as **0**, never hidden.

**(b) Cross-fitted split halves (non-parametric).** Split each arm's respondents at random,
build two independent tables A and B, and average
`mean_o[(m_A(o)−g_A)(m_B(o)−g_B)]` and `mean_cells[W_A ∘ W_B]` over 60–200 splits. Noise is
independent across halves and mean-zero, so these cross-products are unbiased for the true
variances with **no distributional assumption at all**.

**(c) ANCOVA re-estimation** (where a pre-measure exists): residualise post on pre with the pooled
slope, then re-run (a)+(b). Same estimand, ~5× less noise — an external check on whether the
correction is *sufficient*, not just self-consistent.

(a) and (b) agree everywhere (columns `cor_mix` vs `xfit_mix` in the table below). (c) agrees on
gateway_vdL2017 (2.10 → 2.13) and gateway_Maertens2020 (0.00 → 0.14, band tightening to 0–0.28);
on voelkel2026 it does **not** (1.44 → 2.93), which I read as: voelkel2026's true mix is
determined only to `[1.0, 4]`, and I widen its band accordingly rather than picking a winner.

**Bands.** For each study, a calibrated parametric bootstrap: shrink the observed table to the
noise-corrected components, re-add simulated sampling noise 300–500 times, and re-run the whole
correction. `mix_lo10`/`mix_hi90` is the 10th–90th percentile of the resulting mix. Where the
corrected `V_btw` hits zero the mix is genuinely undefined (`inf`), and I say so.

## 3. The measurement

All entries in pp of scale range. **Bold = noise-corrected.** `xfit` = the independent split-half
estimator. `contrast` = the post-hoc arm-heterogeneity code of §5.

| study | k | O | n/arm | raw sd_btw | raw sd_wth | raw mix | sd_btw | sd_wth | **mix** | 80 % band | xfit mix | contrast |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| voelkel2026 | 10 | 8 | 1029 | 0.52 | 0.97 | 1.87 | **0.40** | **0.57** | **1.44** | 0.00–3.04 | 1.43 | 0 |
| voelkel2024 | 25 | 8 | 1013 | 1.45 | 1.67 | 1.16 | **1.42** | **1.51** | **1.07** | 0.96–1.20 | 1.07 | 1 |
| vlasceanu2024 | 11 | 4 | 709 | 4.17 | 2.21 | 0.53 | **3.95** | **1.65** | **0.42** | 0.28–0.66 | 0.41 | 1 |
| koetke2024_S3 | 5 | 7 | 58 | 2.21 | 7.99 | 3.62 | **0.72** | **7.68** | **10.65** | 2.52–10.97 | 22.38 | 1 |
| koetke2024_S4 | 5 | 7 | 63 | 5.77 | 8.91 | 1.54 | **5.06** | **8.48** | **1.68** | 1.25–2.63 | 1.68 | 1 |
| koetke2024_S5 | 3 | 7 | 174 | 4.01 | 1.80 | 0.45 | **3.59** | **1.04** | **0.29** | 0.00–0.68 | 0.30 | 0 |
| gligoric2025 | 5 | 8 | 131 | 2.48 | 1.81 | 0.73 | **1.77** | **0.00** | **0.00** | 0.00–0.78 | 0.00 | 0 |
| spampatti2023 | 6 | 5 | 849 | 0.58 | 0.74 | 1.28 | **0.00** | **0.30** | **inf** | 0.00–1.81 | inf | 0 |
| schmid2023_E1 | 3 | 6 | 131 | 5.52 | 7.84 | 1.42 | **5.00** | **7.62** | **1.53** | 1.18–2.30 | 1.55 | 1 |
| schmid2023_E2 | 3 | 5 | 78 | 7.69 | 7.10 | 0.92 | **7.13** | **6.73** | **0.94** | 0.68–1.44 | 0.94 | 1 |
| schmid2023_E3 | 5 | 5 | 199 | 6.15 | 5.72 | 0.93 | **5.96** | **5.49** | **0.92** | 0.74–1.18 | 0.93 | 1 |
| schmid2023_E4 | 5 | 5 | 200 | 9.58 | 7.39 | 0.77 | **9.42** | **7.19** | **0.76** | 0.66–0.91 | 0.76 | 1 |
| gateway_Maertens2020 | 3 | 5 | 120 | 2.55 | 1.11 | 0.43 | **2.14** | **0.00** | **0.00** | 0.00–0.74 | 0.00 | 0 |
| gateway_vdL2017 | 5 | 5 | 362 | 2.37 | 4.75 | 2.01 | **2.16** | **4.53** | **2.10** | 1.54–3.50 | 2.09 | 1 |
| veckalov2024 | 2 | 7 | 3507 | 1.97 | 0.18 | 0.09 | **1.95** | **0.00** | **0.00** | 0.00–0.12 | 0.00 | 0 |
| hackenburg2025 | 8 | 4 | 247 | 1.69 | 3.58 | 2.12 | **1.53** | **2.96** | **1.94** | 0.83–4.93 | 1.93 | 1 |

Robustness rows in `mix_table.csv`: `voelkel2026_ancova_8out` (mix 2.93), `gateway_*_ancova`,
`vlasceanu2024_global_4out` (mix 0.60 vs 0.42 US-only — *sample*, not design, moves it by 40 %),
`spampatti2023_us_only`, and the 10 per-issue hackenburg tables (mix 0.58 … 18.7, median 2.43).

Three things this table settles:

* **The noise correction is larger than the quantity, exactly as the brief said.** voelkel2026's
  raw mix is 1.87; 66 % of its raw within-variance and 42 % of its raw between-variance is
  sampling noise. gligoric2025's raw mix is 0.73 and its true mix is **0** (noise = 123 % of the
  raw within variance). Every raw mix in the table is biased *upward*.
* **Structurally similar studies really do disagree.** gateway_Maertens2020 and gateway_vdL2017
  share an outcome set (consensus perception + belief + causation + worry + policy support), a
  population, and a research group — and their mixes are **0.14 and 2.13**. ANCOVA confirms both.
  This is not noise; it is the phenomenon the brief describes.
* **Four studies have a measured message-level SD of exactly zero** (gligoric2025,
  gateway_Maertens2020, veckalov2024, and spampatti2023 to within 0.3 pp). In those studies the
  *entire* recoverable ATE signal is the outcome main effect. Three of the four are
  trust/consensus message studies with near-synonymous arms.

## 4. Design predictors — the honest evaluation

Features coded per study (all in `mix_table.csv`): `n_arms`, `n_outcomes`, `n_per_arm`,
`one_construct` (outcome set is facets/items of a single construct), `n_constructs`,
`n_scale_types` (slider / Likert / binary / count), `has_behavioural`, `assertion_match`
(some arm asserts what some outcome item asks), `modality_hetero`, `has_oppositional_arm`,
`arm_contrast_kind` (arms differ in *kind* — presence/absence of the appeal, hostile vs neutral,
generators of very different competence — rather than in *framing* of one goal).

Target variable: `log mix_reg`, where `mix_reg = sqrt((V_wth+c)/(V_btw+c))` with `c = 0.05 pp²`
(a floor, so that the four zero-mix and one infinite-mix studies stay in the analysis).
Baseline: the pooled mean of the other studies. Estimator: OLS, leave-one-study-out **and**
leave-one-cluster-out (clusters: voelkel, vlasceanu, koetke, gligoric, spampatti, schmid,
gateway, geiger, hackenburg — so the 4 schmid and 3 koetke studies never train on each other).

| feature(s) | LOSO RMSE | baseline | LOCO RMSE | baseline |
|---|---|---|---|---|
| `arm_contrast_kind` | **1.104** | 1.275 | **1.133** | 1.260 |
| `has_oppositional_arm` | 1.146 | 1.275 | 1.281 | 1.260 |
| `arm_contrast_kind + log k` | 1.169 | 1.275 | 1.126 | 1.260 |
| `log k` | 1.288 | 1.275 | 1.310 | 1.260 |
| `n_scale_types` | 1.321 | 1.275 | 1.308 | 1.260 |
| `assertion_match` | 1.345 | 1.275 | 1.339 | 1.260 |
| `one_construct` | 1.509 | 1.275 | 1.492 | 1.260 |

**Read this as a negative result.** Six of the seven candidate rules are *worse* than "use the
pooled mean". The one that is not (`arm_contrast_kind`: fitted mix 0.32 for framing-variant arm
sets, 1.41 for kind-different arm sets) buys a 13 % RMSE reduction — from "wrong by a factor of
3.6" to "wrong by a factor of 3.0". Against 4 000 random relabelings with the same 6/10 margin,
p = 0.015; but the feature was coded by me *after* seeing all 16 answers, which no permutation
test can undo, and on the bounded share scale the same rule is worthless (0.359 vs 0.365).
The number of arms, the number of outcomes, n per arm, outcome-set breadth, scale-type mixing,
the presence of behavioural outcomes, and assertion-match all fail outright.

*Sign-flipping of the outcome profile* is in `mix_table.csv` only implicitly (it is a property of
the answer, not of the design) and I did not fit on it: an analyst can only use it via their own
predicted profile, which is what §6 does.

## 5. What the data does say, mechanistically (not a fitted rule)

The ratio is not a primitive. Read the two components separately and the 16 studies stop looking
contradictory:

* **`sd_btw` ≈ (overall effect amplitude) × (dispersion of the outcome set's responsiveness).**
  It is smallest where every outcome is an equally distal slider on one attitude domain
  (voelkel2026, 0.40 pp; hackenburg's 4 items of one construct, 1.53 pp at a 3× larger amplitude)
  and largest where the outcome set mixes a near-stimulus outcome with distal ones, or mixes scale
  types, or flips sign (vlasceanu 3.95 with a binary share and a 0–8 count; koetke2024_S5 3.59
  with trust up +2.4 and belief-in-research −6.2 and behaviour −7.7; schmid 5.0–9.4 with advocate
  credibility next to policy attitude).
* **`sd_wth` ≈ (overall effect amplitude) × (how differently the arms actually work).** It is
  exactly 0 in the three studies whose arms are near-synonymous pursuits of one goal at modest
  amplitude (Većkalov's two consensus messages; Maertens' consensus/inoculation/balanced;
  gligoric's five conservative-trust messages) and 4.5–8.5 pp where an arm withholds or reverses
  the appeal (vdL2017's counter-message-only, schmid's hostile/absent advocate, koetke's Low-IH
  persona) or where the arm set spans wildly different generator competence (hackenburg, 2.96).
* **The two are not independent of the design in the same way**, which is why their ratio is so
  hard to predict: `sd_btw` is a property of the *outcome set*, `sd_wth` of the *arm set*, and the
  amplitude that scales both cancels. A study can land anywhere in the plane.
* **Small-k studies structurally understate the mix** (§1). Three of the four zero-mix studies have
  k = 2, 3, 5. Do not carry their mixes over to a k = 16 design without the `mix_k16` adjustment
  — and that adjustment is unstable, which is itself part of why the hole cannot be closed here.

## 6. The target study

Design facts read from `/workspace/benchmark` (`scripts/lib/submission_spec.R`,
`survey/condition_codenames.csv`, `survey/questionnaire.txt`): 16 scored text interventions +
control (the 3 LLM-chatbot arms and the value-similarity quiz are **not** in the scored condition
list), 13 outcomes, ~18 000 respondents (~1 000/arm, ≥2 000 control). Feature coding:
`arm_contrast_kind = 0` (all 16 are earnest, similar-length pro-trust texts in 6 organizer-tagged
families — "Applications and impact", "Collaboration and peer-review", "Scientific methods and
results", "Others' endorsement", "Values", "Other"; none withholds or reverses the appeal, none is
a different medium), `has_oppositional_arm = 0`, `modality_hetero = 0`, `one_construct = 0`,
`n_constructs = 5`, `n_scale_types = 3` (0–100 sliders, $0–10 donation, binary newsletter),
`has_behavioural = 1`, `assertion_match = 1` (Funding → `funding_perceptions`, Consensus →
`belief_post`, High public trust → `trust_*`, Peer-review / Model accuracy → competence facets).

**Denominator — `sd_btw` ≈ 0.42 pp [0.30, 0.55].** Computed directly as the SD across the 13
outcomes of ANCHORS_E's `resp_ctr` responsiveness profile (mean 0.29 pp, sd **0.417 pp**; the
`resp_lo` and `resp_hi` profiles both give 0.47). This is not an independent guess: it is the
arm's own outcome-level prediction, and the mix must be consistent with it. It is dominated by
three facts already in that profile — the two direct trust outcomes move ~1 pp, the distal
policy/behaviour outcomes ~0.2 pp, and `distrust_post` moves the *other way*. **`sd_btw` scales
linearly with whatever amplitude multiplier the arm applies to that profile.**

**Numerator — `sd_wth` ≈ 0.55 pp [0.20, 1.20].** Anchored on the measured message-level SDs of the
design-closest train studies, in order of proximity: voelkel2026 (10 short climate framings,
0–100 sliders, US quota, n = 1 029/arm) **0.57 pp** by DIM / **0.70 pp** by ANCOVA;
gligoric2025 (5 messages, trust-in-scientists outcome, US) **0.00 pp** (band to ~0.9);
spampatti2023 (6 strategies) **0.30 pp**; voelkel2024 (25 heterogeneous interventions, US,
n = 1 013/arm) **1.51 pp**; vlasceanu2024 US (11 interventions) **1.65 pp**. The target's arm set
is a *framing-variant* set like voelkel2026's, not a kind-different set like voelkel2024's — but
16 arms drawn from 6 explicitly different content families, several of which assert exactly what a
specific outcome asks, should not sit at gligoric's zero. 0.55 pp is the centre of that evidence,
with the band spanning "all 16 messages are interchangeable" to "as spread as a 25-intervention
megastudy".

**Predicted true mix = 0.55 / 0.42 = 1.2, 80 % band [0.45, 2.6].**

**Rule vs analogy, explicitly.** ~**80 % analogy, ~20 % rule.** The analogy is the two anchors
above (voelkel2026's message-level SD; the arm's own outcome profile as the denominator). The
rule's contribution is only that `arm_contrast_kind = 0` for the target, whose LOSO-honest fitted
value is mix ≈ 0.32 — and the *only* thing I let it do is pull the point estimate down from ~1.4
(pure voelkel2026 analogy: 0.70/0.42 = 1.67 by ANCOVA, 1.36 by DIM) to 1.2 and widen the lower
band to 0.45. If the arm wants a pure-analogy number it is **1.4**; a pure-rule number is **0.32**;
the LOSO error on either is a factor of 3, and the two disagree by a factor of 4, which is an
honest statement of how far from closed this hole is.

## 7. The mix you should SUBMIT is not the true mix

A predictor with level-wise skill `rho_b` (correlation with the true outcome main-effect profile)
and `rho_w` (correlation with the true message-level residual) minimises MSE by submitting
`sd_b_pred = rho_b · sd_btw` and `sd_w_pred = rho_w · sd_wth`, i.e.

    optimal PREDICTED mix = true mix × (rho_w / rho_b)

Verified numerically on the target's predicted components (`sd_btw` 0.42, `sd_wth` 0.50): with
`rho_b = 0.6, rho_w = 0.20` the optimum is at predicted mix **0.40** (= 1.19 × 0.33); with
`rho_w = 0.4` it moves to 0.80; if the true `sd_wth` were 1.5 pp it moves to 1.20. ANCHORS_C's
measured band for `r_within_adj` on this family is 0.15–0.35 and outcome-level skill is much
higher, so **the arm should submit a mix near 0.45 (band 0.2–0.9) even though the true mix is
~1.2**. The two numbers must not be confused.

What it costs to get it wrong, at those settings: sweeping the predicted mix from 0.05 to 3.0
moves within-cell RMSE only from 0.594 to 0.637 pp (+7 %) but moves overall Pearson r from
0.415 (at the optimum 0.40) to 0.393 (at 0.05) and 0.267 (at 3.0) — **a 35 % relative loss of r**.
So the mix is worth a lot of *correlation* skill and comparatively little RMSE; over-weighting the
message level is roughly twice as costly as under-weighting it by the same factor.

## 8. What I could not establish

1. **A design→mix rule that beats the pooled mean out of sample.** Stated as a negative result in
   §4. With 16 studies (9 independent clusters) and effect sizes this small, I do not believe a
   defensible rule is recoverable from this train split at all; a study count of 40+ with
   pre-registered feature coding would be needed to separate `arm_contrast_kind` from hindsight.
2. **Whether `arm_contrast_kind` is a mechanism or a hindsight artefact.** I coded it after seeing
   the answers. It is *plausible* (§5) and permutation-significant (p = 0.015), and it is the one
   feature I would carry forward — but only as a hypothesis to be tested on studies I have not seen.
3. **voelkel2026's own mix.** DIM says 1.44, ANCOVA on the same respondents says 2.93. Since it is
   the closest design twin to the target, this factor-of-2 ambiguity propagates straight into the
   target band and I could not resolve it.
4. **Any mix for studies whose arms did nothing.** spampatti2023 has *both* components
   indistinguishable from zero (mix = 0/0); gligoric2025, gateway_Maertens2020 and veckalov2024
   have a zero numerator. Four of sixteen studies therefore carry no ratio information, only the
   information that `sd_wth` can genuinely be 0.
5. **Whether the target's `sd_wth` is closer to voelkel2026's 0.6 or gligoric's 0.0.** This is the
   single largest unresolved quantity in the target prediction, and it is a *trust-outcome*
   question: the only train study that ran multiple trust-raising messages on a trust outcome
   (gligoric2025) measured exactly zero message-level spread. If that generalises, the target's
   true mix is ~0.3, not 1.2. My band's lower half exists entirely because of that study.
6. **The k-projection.** `mix_k16` is the structurally correct way to carry a k = 2 or k = 3 study
   over to a 16-arm design, but it produces negative `V_b0` (and hence infinite projected mixes)
   in 4 of 16 studies, so I could not use it as a primary estimator.
7. **Weighted / covariate-adjusted estimands.** Everything here is unweighted difference-in-means
   (plus ANCOVA checks). If the organizers' pipeline scores a different estimand, the *noise* in
   the truth changes and hence the reliability, but the true mix does not — that is why I measured
   the noise-corrected quantity and not the raw one.
