# ANCHORS_C — rank structure of megastudy ATE tables (train split)

Run: idea_03 / 20260827T203601Z_s2b. Source: `/workspace/run/anchors/_rank_run.py` +
`_rank_lib.py`, executed to completion, N_SPLITS = 40, noise-simulation nsim = 500.
Full numeric output: `/workspace/run/anchors/rank_structure.csv` (8 rows x 42 cols).

**Execution note.** No spec crashed and no estimator/noise-correction math was changed.
The only incident: the first launch aborted at `pd.read_excel` with
`ModuleNotFoundError: openpyxl`; on immediate retry `openpyxl 3.1.5` imported fine from
`/opt/kernel/venv` and all 8 specs completed. Nothing was installed. Runtime ~90 s, so
N_SPLITS was left at 40.

All quantities are **per-cell variances in pp^2 of each outcome's scale range**; ATEs are
in pp. "within" = the ATE table column-centred (outcome main effect removed), i.e. the
message-level signal. "true" = noise-corrected (analytic column-centred sampling-noise
floor subtracted). "cv_" = cross-fitted across independent stratified half-samples.

---

## 1. Datasets, size, and the raw variance split

| dataset | n_arms | n_out | n/arm | mean ATE (pp) | var_total | var_outcome | var_within_obs | noise floor | **var_within_TRUE** | mean_se^2 |
|---|---|---|---|---|---|---|---|---|---|---|
| voelkel2026_post_9out * | 10 | 9 | 1023 | +1.20 | 2.048 | 1.072 | 0.976 | 0.750 | **0.226** | 1.111 |
| voelkel2026_post_8att | 10 | 8 | 1024 | +1.52 | 1.206 | 0.267 | 0.939 | 0.615 | **0.324** | 0.911 |
| voelkel2026_ancova_8att | 10 | 8 | 1024 | +1.19 | 0.707 | 0.101 | 0.605 | 0.122 | **0.484** | 0.177 |
| voelkel2024_post_8out | 25 | 8 | 1002 | -1.07 | 4.898 | 2.094 | 2.805 | 0.513 | **2.291** | 0.635 |
| vlasceanu2024_us_4out | 11 | 4 | 643 | +2.96 | 22.256 | 17.351 | 4.905 | 2.185 | **2.719** | 4.927 |
| vlasceanu2024_us_3out * | 11 | 3 | 628 | +5.18 | 6.033 | 3.444 | 2.589 | 2.058 | **0.531** | 4.680 |
| vlasceanu2024_global_4out | 11 | 4 | 4601 | +1.69 | 13.874 | 10.017 | 3.856 | 0.286 | **3.570** | 0.614 |
| vlasceanu2024_global_3out | 11 | 3 | 4489 | +3.02 | 9.335 | 6.239 | 3.096 | 0.267 | **2.829** | 0.572 |

`*` = **low-reliability spec, do not quote its shares.** Both have `sd_cv_share_rank1` > 5
(the cross-fitted denominator `cv_true_within_var_half` crosses zero across splits) and
`splithalf_r_within` <= 0.14. `voelkel2026_post_9out` is wrecked by adding Donation
(var_outcome 0.267 -> 1.072, mean_se^2 0.911 -> 1.111); `vlasceanu2024_us_3out` by SHAREcc
being a 0/1 item at n~630/arm (mean_se^2 = 4.68 pp^2).

**Signal fractions.** Share of *total* ATE variance that is the outcome main effect:
0.14 (v26 ancova), 0.22 (v26 post-8att), 0.43 (v24), 0.67-0.78 (vlasceanu). Share of the
*true* (noise-free) signal that is message-level rather than outcome-level:
0.83 (v26 ancova), 0.55 (v26 post-8att), 0.52 (v24), 0.26-0.31 (vlasceanu global).

**True message-level SD (pp):** v26 = **0.57-0.70**, v24 = **1.51**, vlasceanu global =
1.68-1.89. Outcome-main-effect SD (pp): v26 = 0.32-0.52, v24 = 1.45, vlasceanu = 2.50-4.17.

**ANCOVA is the single largest measured lever.** Same 10 arms, same 8 outcomes, same n:
switching post-only DIM -> ANCOVA(pre) cuts `mean_se^2` from 0.911 to 0.177 (5.1x) and the
within-outcome noise floor from 0.615 to 0.122 (5.0x). Split-half `r_within` goes
0.217 -> 0.663; split-half r of the rank-1 arm scores goes 0.229 -> 0.881. Implied residual
SD falls from ~26.4 pp to ~11.8 pp of range.

---

## 2. How much structure a rank-1 fit captures

`rank1_share_of_true_within` is the in-sample noise-corrected share; `cv_share_rank1_half`
is the honest cross-fitted share (fit rank-1 on half A, project onto half B, symmetrised,
divided by `cv_true_within_var_half` = mean(W_A * W_B)).

| dataset | rank1_share (in-sample) | **cv_share_rank1_half** | sd | cv_share_rank2_half | sd | **cv_share_armmain_half** | armmain_share (in-sample) |
|---|---|---|---|---|---|---|---|
| voelkel2026_post_9out * | 1.383 | 0.625 | 5.902 | 0.644 | 2.889 | 0.221 | 1.660 |
| voelkel2026_post_8att | 1.371 | **0.692** | 0.490 | 0.762 | 0.314 | **0.672** | 1.679 |
| voelkel2026_ancova_8att | 0.824 | **0.839** | 0.030 | 0.971 | 0.029 | **0.817** | 0.837 |
| voelkel2024_post_8out | 0.678 | **0.677** | 0.011 | 0.860 | 0.011 | **0.479** | 0.515 |
| vlasceanu2024_us_4out | 0.847 | **0.908** | 0.184 | 0.932 | 0.137 | **-0.049** | 0.101 |
| vlasceanu2024_us_3out * | 0.402 | 0.170 | 5.477 | 0.486 | 2.511 | 1.119 | 1.908 |
| vlasceanu2024_global_4out | 0.716 | **0.723** | 0.013 | 0.931 | 0.005 | **0.209** | 0.216 |
| vlasceanu2024_global_3out | 0.830 | **0.827** | 0.011 | 0.963 | 0.002 | **0.551** | 0.563 |

In-sample shares > 1 (v26 post specs, `armmain_share` 1.66-1.91) mean the analytic noise
floor slightly exceeds what the SVD component actually contains at that SNR; treat them as
"saturated, ~1" and use the cross-fitted column instead.

**Median over the 6 reliable specs: rank-1 = 0.775, rank-2 = 0.932, arm-main = 0.515.**
Rank-2 buys a further **+5 to +21 pp** of true within-variance over rank-1
(v26 ancova +13.2, v24 +18.3, vla_global_4out +20.8, vla_global_3out +13.6, us_4out +2.4).

---

## 3. Is the message effect one number per arm?

`armmain` = constant loading across outcomes (arm row mean applied to every outcome).

- The **arm dimension** is essentially one scalar: `corr(arm row-mean of W, rank-1 arm
  score)` = **0.997** (v26 ancova), **0.998** (v26 post-8att), **0.964** (v24), **0.947**
  (vla global 3out). Which arm is strong is a single latent number.
- The **outcome dimension** is *not* constant. Rank-1 loading vectors (normalised to
  mean|loading| = 1) and their CV:
  - v26 ancova (8 attitudinal 0-100 sliders): Belief .86, Concern 1.32, Policies 1.22,
    Intent 1.33, PoliciesSp .66, Candidate .80, Companies 1.08, IntentNp .72 — **CV 0.254**,
    corr(loading, outcome mean effect) = 0.07.
  - v26 post-8att: **CV 0.303**, corr with outcome mean = 0.19.
  - v24 (8 outcomes incl. partisan animosity): PA 2.59, ADA .93, SPV .04, SUC 1.16,
    OppBip .74, SocDistrust .92, SocDis 1.06, BEPF .56 — **CV 0.684**,
    corr(loading, outcome mean) = **-0.896** (PA is both the largest mean effect and by far
    the most arm-discriminating outcome).
  - vla global 3out: Belief .36, Policy .46, SHAREcc 2.18 — **CV 0.837**,
    corr(loading, outcome mean) = **0.997** (driven by the 0/1 SHARE scale).
- Consequence: the rank-1 vs arm-main gap tracks loading CV.
  Homogeneous outcome sets -> gap is negligible (v26 ancova 0.839 vs 0.817, **+0.022**;
  v26 post-8att 0.692 vs 0.672, +0.020). Heterogeneous outcome sets -> large
  (v24 0.677 vs 0.479, **+0.198**; vla global 4out 0.723 vs 0.209, **+0.514**).
- Arm-effect spread for reference (rank-1 arm scores, pp): v26 ancova mean|s| = 1.69,
  range -3.43 .. +2.57; v26 post-8att mean|s| = 1.90, range -4.13 .. +3.71;
  v24 (25 arms) mean|s| = 3.07, range -6.69 .. +6.29.

---

## 4. Split-half reliabilities and the ceiling on r_within

Stratified-by-arm halves, 40 draws; mean (SD).

| dataset | r_full | r_within | r_rank1_arm_scores | r_arm_row_mean |
|---|---|---|---|---|
| voelkel2026_post_9out * | 0.379 (0.120) | 0.125 (0.147) | 0.172 (0.273) | 0.105 (0.249) |
| voelkel2026_post_8att | 0.262 (0.130) | 0.217 (0.149) | 0.229 (0.216) | 0.247 (0.219) |
| voelkel2026_ancova_8att | 0.619 (0.059) | 0.663 (0.044) | 0.881 (0.058) | 0.892 (0.053) |
| voelkel2024_post_8out | 0.788 (0.022) | 0.692 (0.029) | 0.863 (0.041) | 0.795 (0.050) |
| vlasceanu2024_us_4out | 0.748 (0.089) | 0.388 (0.125) | -0.390 (0.532) | -0.017 (0.242) |
| vlasceanu2024_us_3out * | 0.374 (0.186) | 0.141 (0.164) | 0.086 (0.292) | 0.258 (0.207) |
| vlasceanu2024_global_4out | 0.944 (0.020) | 0.864 (0.039) | 0.685 (0.595) | 0.804 (0.075) |
| vlasceanu2024_global_3out | 0.930 (0.029) | 0.853 (0.053) | 0.857 (0.067) | 0.875 (0.052) |

**The noise correction validates.** The analytic prediction
`rel_half = V_true / (V_true + 2*noise_floor)` reproduces the measured split-half
`r_within` almost exactly: 0.131 vs 0.125, 0.209 vs 0.217, 0.665 vs 0.663, 0.691 vs 0.692,
0.384 vs 0.388, 0.114 vs 0.141, 0.862 vs 0.864, 0.841 vs 0.853. The decomposition is
trustworthy.

**Ceiling on any predictor's raw r against a HALF-sample truth = sqrt(split-half r).**

| dataset | ceiling r_within | ceiling r_full |
|---|---|---|
| voelkel2026_post_9out * | 0.354 | 0.616 |
| voelkel2026_post_8att | **0.466** | 0.512 |
| voelkel2026_ancova_8att | **0.814** | 0.786 |
| voelkel2024_post_8out | **0.832** | 0.887 |
| vlasceanu2024_us_4out | 0.623 | 0.865 |
| vlasceanu2024_us_3out * | 0.376 | 0.612 |
| vlasceanu2024_global_4out | 0.930 | 0.972 |
| vlasceanu2024_global_3out | 0.923 | 0.964 |

An omniscient predictor of the *true* table gets at most these numbers on raw r; that is
precisely what the organizers' attenuation correction (r_adj / r_within_adj) divides out,
so r_adj has ceiling 1 — but only if the reliability estimate used is the right one.

**Projection to a 17-arm x 13-outcome trust megastudy at n ~ 1,000/intervention.**
The column-centred noise floor is exactly `(1 - 1/k) * sigma_pp^2 / n_per_arm`
(the control's variance cancels under arm-centring), with k = 16 message arms:

| outcome SD (pp of range) | noise floor, full | noise floor, half | rel_half at sd_true_within = 0.4 / 0.6 / 0.8 / 1.2 pp |
|---|---|---|---|
| 18 | 0.304 | 0.608 | 0.208 / 0.372 / 0.513 / 0.703 |
| 22 | 0.454 | 0.908 | 0.150 / 0.284 / 0.414 / 0.613 |
| 26 | 0.634 | 1.268 | 0.112 / 0.221 / 0.336 / 0.532 |
| 30 | 0.844 | 1.688 | 0.087 / 0.176 / 0.275 / 0.460 |

Ceilings on raw r_within = sqrt of those, e.g. sigma = 22 pp and sd_true_within = 0.6 pp
gives **rel_half 0.284, ceiling r_within 0.533**. The voelkel2026 post-only anchor
(sigma ~26 pp, sd_true_within ~0.57 pp) sits at rel_half 0.209 / ceiling 0.457.

---

## 5. MSE-optimal shrink kappa

Decompose a prediction into outcome column means (kept) + message-level residual W_p, and
score against a half-sample truth. The MSE-optimal scale on W_p is exactly

    kappa* = corr(W_p, W_TRUE) * SD(W_TRUE) / SD(W_p)
           = r_within_adj / spread_ratio_within

kappa* does **not** depend on the truth half's noise (noise is orthogonal in expectation),
only on true skill and on how wide your own residuals are. If the predictor's within-outcome
spread is calibrated to the true spread, **kappa* = r_within_adj, i.e. keep exactly as large
a fraction of your message-level prediction as your attenuation-corrected within-outcome
skill.** At kappa*, the fraction of true within-variance removed is rho^2.

Projected behaviour on the two target-matched anchors (predictor assumed spread-calibrated,
outcome means perfect):

| rho = r_within_adj | kappa* | v26_ancova: r_within vs half / RMSE_within | v24: r_within vs half / RMSE_within |
|---|---|---|---|
| 0.10 | 0.10 | 0.082 / 0.692 pp | 0.083 / 1.506 pp |
| 0.15 | 0.15 | 0.122 / 0.688 pp | 0.125 / 1.497 pp |
| 0.20 | 0.20 | 0.163 / 0.681 pp | 0.166 / 1.483 pp |
| 0.25 | 0.25 | 0.204 / 0.673 pp | 0.208 / 1.466 pp |
| 0.30 | 0.30 | 0.245 / 0.663 pp | 0.249 / 1.444 pp |
| 0.40 | 0.40 | 0.326 / 0.637 pp | 0.332 / 1.387 pp |
| 0.50 | 0.50 | 0.408 / 0.602 pp | 0.416 / 1.311 pp |

(kappa = 0 baselines: 0.695 pp and 1.514 pp. On voelkel2026 post-8att the numbers are
harsher still: rho = 0.30 buys r_within 0.137 and RMSE 0.543 vs 0.569 pp.)

---

## 6. What this means for predicting a 17-arm x 13-outcome trust megastudy

- **Most of the recoverable variance is the outcome column mean, not the message.** On
  design-matched anchors the outcome main effect is 14-43% of total ATE variance and it is
  the part measured with the highest reliability; on scale-heterogeneous sets it is 67-78%.
  Getting the 13 per-outcome mean shifts right dominates overall Pearson r
  (r_full 0.34-0.61 in the projection above even when message-level skill is only 0.10-0.30).
  Spend prediction effort there first; `r_within` is the only metric that cannot be bought
  this way.
- **The arm effect is one latent scalar per message, times a per-outcome sensitivity
  loading.** `corr(arm row-mean, rank-1 score) = 0.947-0.998` in every reliable anchor;
  cross-fitted rank-1 captures a median **0.775** of true within-outcome variance. So the
  right parameterisation is `ATE[a,o] = mu[o] + s[a] * L[o]`, not `mu[o] + s[a]`.
- **The loading vector is worth predicting; genuine arm x outcome interaction is not.**
  Constant loading (arm-main) captures only a median **0.515** cross-fitted, versus 0.775
  for rank-1 — the whole gap is the loading, and it is large exactly when outcomes differ in
  scale/base-rate/proximality (v24 loading CV 0.684, vlasceanu 0.837) and small when they are
  homogeneous sliders (v26 CV 0.254-0.303, rank-1 beats arm-main by only +0.02). For 13
  trust outcomes on a common instrument, expect loading CV nearer 0.25-0.40: predict a
  modest per-outcome sensitivity (bigger for proximal trust-in-scientists items, smaller for
  distal policy/behaviour items), then stop.
- **Rank >= 2 is off the table.** Rank-2 adds only +5 to +21 pp of true within-variance
  in-sample, and that residual is not reliably estimable at n ~ 1,000/arm: at the
  target-matched noise floor a half-sample truth has `rel_half` ~ 0.15-0.41, so anything
  beyond a rank-1 outer product is being fitted against noise. Predict no idiosyncratic
  arm x outcome cell deviations.
- **Keep only kappa = r_within_adj of your message-level residual.** With a spread-calibrated
  predictor the MSE-optimal shrink is numerically equal to your attenuation-corrected
  within-outcome skill; if your residual spread is inflated by a factor `spread_ratio`,
  divide by it. Realistic ex-ante skill on this family is small, so the honest default is
  **kappa in the 0.15-0.35 band, i.e. discard 65-85% of the message-level spread you would
  naively submit** — and note that kappa never changes r_within (a correlation is
  scale-free); it only protects RMSE, alpha/beta calibration and spread_ratio.
- **Expected returns are small in absolute pp and that is normal.** True message-level SD
  is 0.57-0.70 pp on the closest anchor (voelkel2026, n ~ 1,024/arm, 0-100 sliders) and
  1.51 pp on the 25-arm anchor. A rho = 0.30 predictor moves within-outcome RMSE from
  0.695 to 0.663 pp. Do not trade a correct outcome-mean profile for message-level ambition.
- **Reliability, not skill, will set the numbers you see.** Measured split-half `r_within`
  on target-matched, post-only DIM anchors is **0.217** (voelkel2026) to **0.692**
  (voelkel2024, 25 arms and 3x the true signal). If the target's true message-level SD is
  near voelkel2026's, the ceiling on raw r_within against a half-sample truth is ~0.46-0.53,
  and a diagnostic below that is not evidence of failure. Any per-task diagnostic computed
  on a table with `rel_half` < ~0.2 is uninterpretable (the two starred specs above have
  split-half SDs of 0.147-0.164 on r_within itself).
- **Covariate adjustment is the biggest available multiplier and it is free.** Pre-measure
  ANCOVA on identical data cut the within-outcome noise floor 5.0x and raised split-half
  `r_within` from 0.217 to 0.663 and rank-1 arm-score reliability from 0.229 to 0.881. If
  the target's scoring pipeline admits a pre-measure- or covariate-adjusted estimand, that
  choice is worth more than any modelling improvement measured here; if it does not, the
  post-only reliabilities above are the operative ceilings and should be quoted as such.
