# ANCHORS_A — empirical ATE anchors from two multi-arm climate message megastudies

Source: TRAIN split only (`/workspace/datasets/voelkel2026`, `/workspace/datasets/vlasceanu2024`).
All effects in **percentage points of each outcome's scale range**: `ate_pp = 100*(mean_arm - mean_control)/(hi-lo)`.

## 0. What was computed

**voelkel2026 (CCC)** — n=13,821; 10 message arms vs. 3 pooled innocuous-text controls (`ConditionR`,
control n=3,183). 9 outcomes, all 0-100: `Belief, Concern, Policies, Intent, PoliciesSp, Candidate,
Companies, IntentNp` (each pre+post; composites exactly as the authors' `Step 2 - Preparation.R` builds
them) plus post-only `Donation` (= 100 - share allocated to the non-climate charity, 0-100).
90 arm x outcome cells.
- `voelkel2026_ates.csv` = **post-only** ATE (arm post mean - control post mean).
- `voelkel2026_ates_ancova.csv` = **ANCOVA** ATE (post ~ pre_centred + arm dummies), 8 outcomes x 10 arms
  = 80 cells. Donation has no pre-measure and is absent.

**vlasceanu2024** — US subsample only, n=8,253; 11 intervention arms vs. Control (n=669).
4 outcomes: `Belief` = mean(Belief1-4), 0-100; `Policy` = mean(Policy1-9), 0-100;
`Sharing` = SHAREcc, binary 0-1 (range 1, so 1 pp = 1 point of share); `WEPT` = WEPTcc, 0-8 pages of the
effortful tree-planting task. 44 cells. `vlasceanu2024_ates.csv`.
A **global (all 63 countries, n=59,432)** table is written as `vlasceanu2024_ates_global_context.csv`
for contrast — it is much better powered and I lean on it below.

CSV columns: `arm, outcome, ate_pp, se_pp, n_arm, n_control, control_mean_pp, outcome_sd_pp, p, p_bh`
(`se_pp` = unpooled two-sample SE; `p_bh` = Benjamini-Hochberg across the whole table).

---

## 1. Distribution of ate_pp (pooled over all arm x outcome cells)

| table | n_cells | mean | median | sd | min | max | q25 | q75 | iqr | mean_abs | mean_se | frac_pos | frac_BH<.05 | frac_p<.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| voelkel_post | 90.0 | 1.201 | 1.219 | 1.439 | -3.947 | 5.374 | 0.672 | 2.093 | 1.421 | 1.58 | 1.025 | 0.822 | 0.122 | 0.322 |
| voelkel_ancova | 80.0 | 1.189 | 1.311 | 0.846 | -0.761 | 3.666 | 0.703 | 1.672 | 0.969 | 1.262 | 0.419 | 0.925 | 0.625 | 0.688 |
| vlasceanu_us | 44.0 | 2.956 | 3.677 | 4.772 | -8.557 | 10.318 | 1.313 | 6.211 | 4.898 | 4.932 | 2.115 | 0.795 | 0.591 | 0.682 |
| vlasceanu_global | 44.0 | 1.69 | 1.115 | 3.768 | -6.296 | 10.606 | 0.194 | 3.039 | 2.845 | 2.979 | 0.723 | 0.75 | 0.682 | 0.705 |

**Headline.** In a properly controlled short-message climate megastudy (voelkel2026), the *typical*
arm x outcome effect is **~+1.2 pp of scale range**, the whole table lives in **[-1, +4] pp**, and the
across-cell SD is **0.85 pp (ANCOVA) / 1.44 pp (post-only, which is 70 % sampling noise)**.
82-93 % of cells are positive but only **12 % (post-only) survive BH correction**; with the pre-measure
covariate that rises to 63 %.

vlasceanu2024-US looks 3-4x bigger, but see §6 — its control arm read *nothing*, its US control n is only
669, and the US is the single most responsive of 63 countries. The global table (mean +1.7 pp,
belief +1.35 pp) is the more honest anchor and it agrees with voelkel2026.


## 2. Per-outcome distribution


**voelkel_post**  (`sd_arms_true` = across-arm SD after subtracting sampling noise = the real message-to-message spread)

| outcome | n_arms | mean | median | sd_across_arms | sd_arms_true | min | max | frac_pos | frac_sig_bh | mean_se | ctl_mean | out_sd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Belief_Post | 10.0 | 1.42 | 1.35 | 1.02 | 0.78 | -0.1 | 3.06 | 0.9 | 0.3 | 0.81 | 65.44 | 22.56 |
| Candidate_Post | 10.0 | 1.47 | 1.49 | 0.77 | 0.39 | 0.17 | 2.77 | 1.0 | 0.1 | 0.8 | 32.53 | 22.05 |
| Companies_Post | 10.0 | 1.29 | 1.13 | 0.91 | 0.4 | -0.53 | 2.44 | 0.9 | 0.0 | 1.0 | 70.86 | 27.59 |
| Concern_Post | 10.0 | 1.7 | 1.65 | 1.34 | 0.98 | -0.6 | 3.86 | 0.9 | 0.2 | 1.12 | 60.42 | 31.18 |
| Donation | 10.0 | -1.38 | -1.43 | 1.19 | 0.0 | -3.95 | 0.53 | 0.1 | 0.0 | 1.65 | 61.54 | 45.39 |
| IntentNp_Post | 10.0 | 1.03 | 0.98 | 1.03 | 0.72 | -0.57 | 3.4 | 0.9 | 0.1 | 0.89 | 54.55 | 24.45 |
| Intent_Post | 10.0 | 2.78 | 2.46 | 1.11 | 0.7 | 1.47 | 5.37 | 1.0 | 0.3 | 1.05 | 33.83 | 29.26 |
| PoliciesSp_Post | 10.0 | 1.45 | 1.11 | 0.76 | 0.24 | 0.7 | 3.16 | 1.0 | 0.1 | 0.88 | 53.29 | 24.23 |
| Policies_Post | 10.0 | 1.06 | 1.21 | 1.1 | 0.69 | -0.77 | 2.52 | 0.7 | 0.0 | 1.04 | 68.01 | 29.05 |

**voelkel_ancova**  (`sd_arms_true` = across-arm SD after subtracting sampling noise = the real message-to-message spread)

| outcome | n_arms | mean | median | sd_across_arms | sd_arms_true | min | max | frac_pos | frac_sig_bh | mean_se | ctl_mean | out_sd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Belief_Post | 10.0 | 1.16 | 1.18 | 0.98 | 0.93 | -0.34 | 3.12 | 0.9 | 0.6 | 0.37 | 65.44 | 22.56 |
| Candidate_Post | 10.0 | 1.25 | 1.16 | 0.62 | 0.47 | 0.45 | 2.14 | 1.0 | 0.5 | 0.48 | 32.53 | 22.05 |
| Companies_Post | 10.0 | 0.77 | 0.96 | 0.81 | 0.73 | -0.46 | 1.75 | 0.8 | 0.5 | 0.42 | 70.9 | 27.59 |
| Concern_Post | 10.0 | 1.22 | 1.38 | 0.99 | 0.95 | -0.76 | 2.47 | 0.9 | 0.7 | 0.37 | 60.44 | 31.18 |
| IntentNp_Post | 10.0 | 1.17 | 1.3 | 0.58 | 0.49 | 0.11 | 2.19 | 1.0 | 0.8 | 0.37 | 54.52 | 24.45 |
| Intent_Post | 10.0 | 1.84 | 1.52 | 1.02 | 0.96 | 0.65 | 3.67 | 1.0 | 0.7 | 0.44 | 33.86 | 29.26 |
| PoliciesSp_Post | 10.0 | 1.34 | 1.33 | 0.52 | 0.39 | 0.72 | 2.05 | 1.0 | 0.7 | 0.43 | 53.3 | 24.23 |
| Policies_Post | 10.0 | 0.76 | 1.04 | 0.87 | 0.78 | -0.64 | 1.65 | 0.8 | 0.5 | 0.47 | 68.01 | 29.05 |

**vlasceanu_us**  (`sd_arms_true` = across-arm SD after subtracting sampling noise = the real message-to-message spread)

| outcome | n_arms | mean | median | sd_across_arms | sd_arms_true | min | max | frac_pos | frac_sig_bh | mean_se | ctl_mean | out_sd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Belief | 11.0 | 4.54 | 4.36 | 1.68 | 1.29 | 2.23 | 7.38 | 1.0 | 0.64 | 1.67 | 66.46 | 29.68 |
| Policy | 11.0 | 3.29 | 3.12 | 1.55 | 1.27 | 1.27 | 6.22 | 1.0 | 0.64 | 1.33 | 62.52 | 24.13 |
| Sharing | 11.0 | 7.7 | 7.17 | 1.82 | 0.0 | 5.35 | 10.32 | 1.0 | 0.64 | 3.08 | 53.47 | 48.9 |
| WEPT | 11.0 | -3.7 | -2.71 | 3.61 | 3.24 | -8.56 | 1.88 | 0.18 | 0.45 | 2.38 | 63.15 | 43.98 |

**vlasceanu_global**  (`sd_arms_true` = across-arm SD after subtracting sampling noise = the real message-to-message spread)

| outcome | n_arms | mean | median | sd_across_arms | sd_arms_true | min | max | frac_pos | frac_sig_bh | mean_se | ctl_mean | out_sd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Belief | 11.0 | 1.35 | 1.22 | 1.0 | 0.95 | -0.64 | 3.07 | 0.91 | 0.64 | 0.49 | 77.73 | 24.05 |
| Policy | 11.0 | 1.17 | 0.95 | 1.1 | 1.07 | -0.31 | 3.03 | 0.82 | 0.64 | 0.4 | 68.89 | 19.67 |
| Sharing | 11.0 | 6.55 | 6.54 | 2.83 | 2.71 | 1.34 | 10.61 | 1.0 | 0.91 | 1.15 | 48.48 | 49.81 |
| WEPT | 11.0 | -2.31 | -1.96 | 2.6 | 2.53 | -6.3 | 0.91 | 0.27 | 0.55 | 0.86 | 62.48 | 43.16 |


Reading of §2: **which outcomes move.** In voelkel2026 every attitudinal family moves by a similar
+0.8 to +1.8 pp; the only family that is *distinct* is `Intent_Post` (personal behavioural intent,
+2.8 pp post-only / +1.8 ANCOVA — the largest) and `Donation` (the only **costly, zero-sum behavioural**
outcome: mean **-1.4 pp**, no arm significant, `sd_arms_true = 0.00` — i.e. the entire arm-to-arm spread
on Donation is sampling noise). The same pattern in vlasceanu: attitudes up, the effortful **WEPT**
behaviour **down** (-2.3 pp globally; message reading costs attention before an effortful task), and the
cheap `Sharing` click way up (+6.6 pp on a 0/1 outcome).

**Rule:** attitude/policy/intent sliders all move together and by nearly the same amount;
costly behaviour does not move or moves the wrong way.

---

## 3. Variance decomposition of the ATE table (outcome-level vs message-level)

| table | total_sd | sd_between_outcomes | sd_across_arms_within_outcome | sd_arm_main_effect | sd_interaction | ratio_within_over_between |
|---|---|---|---|---|---|---|
| voelkel_post | 1.439 | 1.098 | 1.041 | 0.713 | 0.724 | 0.948 |
| voelkel_ancova | 0.846 | 0.34 | 0.82 | 0.683 | 0.433 | 2.413 |
| vlasceanu_us | 4.772 | 4.81 | 2.323 | 0.95 | 2.044 | 0.483 |
| vlasceanu_global | 3.768 | 3.655 | 2.06 | 0.963 | 1.756 | 0.564 |

Sum-of-squares shares of the total variance in the arm x outcome table (raw, noise included):

| table | pct_outcome | pct_arm | pct_interaction | grand_mean |
|---|---|---|---|---|
| voelkel_post | 52.35 | 22.36 | 25.29 | 1.2 |
| voelkel_post_noDonation | 22.15 | 51.49 | 26.36 | 1.52 |
| voelkel_ancova | 14.31 | 59.49 | 26.21 | 1.19 |
| vlasceanu_us | 77.96 | 3.69 | 18.35 | 2.96 |
| vlasceanu_global | 72.21 | 6.08 | 21.72 | 1.69 |

Noise-corrected (sampling variance subtracted) version of the two SDs and their ratio:

| table | sd_within_true | sd_between_outcomes_true | ratio |
|---|---|---|---|
| voelkel_post | 0.617 | 0.919 | 0.671 |
| voelkel_post_noDon | 0.655 | 0.096 | 6.8 |
| voelkel_ancova | 0.744 | 0.313 | 2.378 |
| vlasceanu_us | 1.854 | 4.516 | 0.411 |
| vlasceanu_global | 1.989 | 3.61 | 0.551 |

**Reading.** Two regimes:

* When one outcome is qualitatively different (voelkel's `Donation`, vlasceanu's `WEPT`/`Sharing`),
  **outcome-level variance dominates: 52-78 % of the table's variance is "which outcome", 4-22 % is
  "which message", ~20-26 % is the interaction.**
* Restricted to the homogeneous slider families (voelkel, 8 attitudinal outcomes), the picture flips:
  **outcome level only 14-22 %, message main effect 51-59 %, interaction 26 %.** The *true*
  between-outcome SD there is only **0.10-0.31 pp** versus a true within-outcome across-arm SD of
  **0.65-0.74 pp** (ratio 2.4-6.8).

So: **if the target's 13 outcomes are all trust-in-scientists-family sliders, expect the outcome main
effect to contribute little and the message main effect + interaction to contribute most; if some
outcomes are behavioural/costly, the outcome main effect will dominate the r.**
This directly governs the gap between the benchmark's overall Pearson r and its
`r within outcomes`: the overall r is inflated by whatever outcome-level structure exists.

---

## 4. Split-half reliability of the ATE table (20 random splits of respondents)

This is the direct analogue of the benchmark's "Human 1 vs Human 2 replication reference": each half
recomputes the whole ATE table, and I correlate the two halves.
`r_within` = mean-centre each side within outcome, then correlate.
`r_adj` (symmetric) = cov(l,h) / sqrt(var_true_l * var_true_h) with `var_true = var(est) - mean(se^2)`;
`r_adj_onesided` = cov(l,h) / (sd(l)*sqrt(var_true_h)) exactly as specified (still attenuated by l's own
noise, so it is the more conservative number and the better model of "noiseless prediction vs one noisy
human half").

|  | r | r_within | r_adj | r_within_adj | r_adj_onesided | r_within_adj_onesided | sd_half | sd_true | sd_within_half | sd_within_true | mean_se | mean_se_cent |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| voelkel_post | 0.367 | 0.122 | 1.742 | 1.822 | 0.833 | 0.441 | 1.737 | 0.837 | 1.326 | 0.444 | 1.45 | 1.192 |
| voelkel_ancova | 0.616 | 0.667 | 1.045 | 0.998 | 0.805 | 0.818 | 0.941 | 0.727 | 0.858 | 0.703 | 0.593 | 0.487 |
| vlasceanu_us | 0.751 | 0.383 | 1.348 | 1.447 | 1.04 | 0.816 | 5.091 | 3.94 | 2.695 | 1.628 | 2.992 | 1.985 |
| vlasceanu_global | 0.944 | 0.877 | 1.033 | 1.016 | 0.988 | 0.944 | 3.821 | 3.656 | 2.05 | 1.905 | 1.022 | 0.696 |

SD across 20 splits of `r` / `r_within`: voelkel_post .085/.116, voelkel_ancova .066/.049,
vlasceanu_us .070/.117, vlasceanu_global .027/.032.

**This is the single most important anchor.** For a megastudy of voelkel2026's size
(n≈13.5k, 10 arms, ~1,060/arm, 3,180 control) and *post-only* ATEs, **two random halves of the same
humans correlate only r = 0.37 overall and r = 0.12 within outcomes.** The target study is the same
order of magnitude (~18,000 respondents, 16 arms + control), so the human replication reference on
`r_within` is plausibly **0.1-0.4**, not 0.8. Any prediction that achieves r_within ≈ 0.3 against one
human half is close to the human ceiling.

Corollaries:
1. **Attenuation correction matters enormously here.** `r_adj` for voelkel_post is 1.74 (i.e. the true
   ATE pattern is essentially fully shared between halves; all the loss is noise). The scored `r_adj` is
   therefore much more forgiving than raw r — but it is also very unstable (SD 0.76 across splits) when
   `var_true` is small relative to `mean(se^2)`.
2. **Signal-to-noise in the full-sample table**: true ATE SD / mean SE = 0.96 (voelkel post-only),
   1.75 (voelkel ANCOVA), 2.0 (vlasceanu US), 5.1 (vlasceanu global).
3. **Pre-measure/covariate adjustment roughly doubles reliability** (r 0.37 -> 0.62; r_within 0.12 -> 0.67)
   by cutting the SE from 1.03 to 0.42 pp. If the target's scoring pipeline uses a covariate-adjusted
   estimator, expect much higher achievable r than post-only.

Full-sample (not half) true-signal SDs — **these are the numbers a predictor's spread should match**:

| table | sd_obs | sd_true | sd_within_obs | sd_within_true | mean_se | mean_se_cent | signal_noise |
|---|---|---|---|---|---|---|---|
| voelkel_post | 1.439 | 0.98 | 0.993 | 0.486 | 1.025 | 0.843 | 0.956 |
| voelkel_post_noDon | 1.105 | 0.557 | 0.975 | 0.58 | 0.948 | 0.779 | 0.588 |
| voelkel_ancova | 0.846 | 0.734 | 0.783 | 0.702 | 0.419 | 0.344 | 1.751 |
| vlasceanu_us | 4.772 | 4.224 | 2.24 | 1.683 | 2.115 | 1.403 | 1.997 |
| vlasceanu_global | 3.768 | 3.685 | 1.986 | 1.913 | 0.723 | 0.492 | 5.098 |

Note `sd_obs` (what you see in a finite table) is **much larger than `sd_true`**. A calibrated
predictor should submit a table with SD ≈ `sd_true`, not `sd_obs`: for voelkel-like designs that is
**~0.7-1.0 pp overall and ~0.5-0.7 pp within outcome**, against an observed human-half SD of ~1.7 pp.
Submitting the observed spread over-disperses by ~2x and the benchmark's `spread_ratio` will say so.

---

## 5. Ordering of arms by average effect, and its stability

Mean pairwise **Spearman rank correlation of the arm ordering between outcomes**:

| table | mean pairwise Spearman across outcomes |
|---|---|
| voelkel post-only, all 9 outcomes | 0.40 (range -0.79 to 0.92) |
| voelkel post-only, 8 attitudinal (drop Donation) | 0.62 (0.30 to 0.92) |
| voelkel ANCOVA, 8 outcomes | **0.71** (0.25 to 0.90) |
| vlasceanu US, all 4 | 0.04 (-0.74 to 0.69) |
| vlasceanu US, 3 (drop WEPT) | 0.48 (0.36 to 0.69) |
| vlasceanu global, 3 (drop WEPT) | 0.53 (0.36 to 0.81) |

**The arm ordering is real and moderately stable across *attitudinal* outcomes (ρ ≈ 0.5-0.7) and
essentially uncorrelated once a costly-behaviour outcome is included.**

voelkel2026 arm ranking (ANCOVA, mean over 8 outcomes, pp):

| rank | arm | mean ate_pp | sd of within-outcome z |
|---|---|---|---|
| 1 | System Preservation Framing | 2.07 | 0.45 |
| 2 | Consensus Framing 2 | 1.77 | 0.72 |
| 3 | Purity Framing | 1.74 | 0.63 |
| 4 | Dire But Solvable Framing | 1.63 | 0.60 |
| 5 | Gains Framing | 1.61 | 0.39 |
| 6 | Free Market Framing | 1.24 | 0.42 |
| 7 | High Social Distance Framing | 0.69 | 0.46 |
| 8 | Consensus Framing 1 | 0.62 | 0.52 |
| 9 | Binding Framing | 0.50 | 0.47 |
| 10 | Warmth Framing | 0.02 | 0.31 |

Range best-to-worst = **2.05 pp**; interquartile range of arm means ≈ 1.0 pp. Note the *two* consensus
messages differ by 1.15 pp — **wording, not construct, is a large share of the arm variance**.

vlasceanu US arm ranking (mean over Belief/Policy/Sharing, pp):
LetterFutureGen 7.09 ≈ PsychDistance 7.16 ≈ CollectAction 6.91 > SystemJust 5.62 > BindingMoral 4.96 ≈
SciConsens 4.84 ≈ FutureSelfCont 4.79 ≈ NegativeEmotions 4.70 > WorkTogetherNorm 3.76 ≈ DynamicNorm 3.74 >
PluralIgnorance 3.35. Range 3.8 pp.

**Cross-sample stability of the arm ordering** (US table vs. all-63-country table, per outcome, Pearson):
Belief .82, Policy .94, Sharing .77, WEPT .92. So the *relative* ranking of messages replicates well
across independent populations even when the *level* does not.

---

## 6. Caveats you must carry into a forecast

1. **voelkel2026 is pre/post.** Control-arm post responses are primed by the pre-measures, so post-only
   ATEs are attenuated relative to a clean between-subjects design; conversely the pre-measure makes
   ANCOVA very powerful. If the target is post-only with no pre-measure, use the **post-only** table.
2. **voelkel2026 has zero trust outcomes.** It anchors *magnitude on 0-100 sliders*, not trust content.
3. **vlasceanu2024's control read nothing at all**, so its "effects" mix message content with mere
   exposure/priming/demand. Its US control n=669 is small and its control mean sits low, which shifts the
   whole US column up: every one of 11 arms is positive on Belief with mean +4.5 pp, while the same 11
   arms average only **+1.35 pp** globally. Country-level Belief ATEs (14 countries with n>1200) run
   Germany -4.0 ... USA +4.5, SD across countries 2.09 pp against a mean SE of 1.95 pp — i.e. **true
   cross-country heterogeneity SD ≈ 0.75 pp; most of the US's apparent exceptionalism is noise.**
   Treat vlasceanu-US as an *upper* bound and vlasceanu-global as the anchor.
4. `Sharing` is binary: 1 pp of range = 1 percentage point of the share rate. Binary/behavioural-click
   outcomes move **5-10x more in pp-of-range** than 0-100 sliders, because sliders compress.

---

## 7. Concrete rules of thumb for a forecaster

Against a **placebo-text control**, a single short persuasive climate message delivered in a survey:

| outcome family | expected mean ATE (pp of range) | true arm-to-arm SD (pp) | practical range |
|---|---|---|---|
| Climate belief / accuracy (0-100 slider) | **+1.2** | **0.8-0.9** | -0.5 to +3.2 |
| Climate concern / risk (0-100 slider) | **+1.2 to +1.7** | **0.9-1.0** | -0.8 to +3.9 |
| General policy support (0-100 slider) | **+0.8 to +1.1** | **0.7-0.8** | -0.8 to +2.5 |
| Specific policy support (0-100 slider) | **+1.3 to +1.5** | **0.3-0.4** | +0.7 to +3.2 |
| Political / candidate choice | **+1.3 to +1.5** | **0.4-0.5** | +0.2 to +2.8 |
| Personal behavioural intention | **+1.2 to +2.8** | **0.5-1.0** | +0.1 to +5.4 |
| Corporate-accountability attitude | **+0.8 to +1.3** | **0.4-0.7** | -0.5 to +2.4 |
| Cheap online behaviour (share a post, binary) | **+6 to +8** | **2.7** | +1 to +11 |
| Costly / effortful behaviour (donate, WEPT) | **-2 to 0** | **0-3** (mostly noise) | -8 to +1 |

Compact one-liners:

* *"A short persuasive climate text moves a 0-100 attitudinal slider by about **+1.2 pp of scale range**,
  with arm-to-arm true SD of about **0.7 pp**; the best of 10-16 messages gets about **+2.5 pp**, the
  worst about **0.0 pp**."*
* *"Predict essentially the same value for every attitudinal outcome within an arm: the true
  between-outcome SD of the mean effect is only **0.1-0.3 pp** among homogeneous sliders."*
* *"Costly behaviour: predict **0 or slightly negative**, with no arm-to-arm structure."*
* *"Your submitted table's SD should be about **0.8-1.0 pp overall / 0.6-0.7 pp within outcome**, not the
  ~1.7 pp you would see in one human half. The extra is sampling noise you cannot and should not predict."*
* *"The human-vs-human reference on a study this size is r ≈ 0.37 overall and r ≈ 0.12 within outcomes
  for post-only ATEs. Judge yourself against that, not against 1.0."*
* *"Sign is the easy win: ~82-93 % of arm x outcome attitudinal cells are positive. Predicting a small
  positive everywhere already earns most of the directional-agreement credit; the skill is in the
  arm-level ordering, worth about ±1 pp."*
