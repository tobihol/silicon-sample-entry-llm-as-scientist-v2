# DESIGN.md — idea_03

Written in session 1 (`SSB_RUN_ID=20260827T194235Z_s1`). Everything here is mine to
change; the frozen definitions live in `.prime/agent/APPEND_SYSTEM.md`.

---

## 1. What the scoring code actually rewards

Source read: `inputs/organizer_code/statistics.R` (1,365 lines) and
`preregistration_benchmark.qmd` (1,974 lines), pinned at
`b25667b297c036e86c80a51a9594b10cd41644ac`.

### 1.1 The unit of scoring

Every estimate — ATE (Section 1) and condition x moderator interaction (Section 2) —
is converted to **percentage points of its outcome's scale range** *at pair-building
time*, before anything is pooled. 3 points on a 0–100 slider == $0.30 on the donation
== 3 pp of signup probability. Nothing is standardised by an SD (deliberately: synthetic
under-dispersion would inflate d).

Section 1 pools **16 x 13 = 208** intervention x outcome pairs into one number per
metric. Section 2 pools the interaction contrasts. Section 3 works on distributions.

### 1.2 The metric ladder, in increasing strictness

| metric | what it is | what it can and cannot see |
|---|---|---|
| directional agreement | share of same-sign pairs; **exact zeros score 0.5** | chance level is *not* 50% — it is the all-positive floor's value, i.e. the share of positive human ATEs |
| Spearman rho | rank correlation over all 208 pairs | blind to scale and offset |
| Pearson r | linear correlation over all 208 pairs | blind to scale and offset |
| **Pearson r within outcomes** | both sides mean-centred *within each outcome*, then correlated | see §1.3 |
| RMSE (pp) | mean size of errors | read against the no-effect floor and Human 2 |
| r_adj, RMSE_adj | noise-corrected versions | see §1.4 |
| alpha, beta | `lm(ATE_human ~ ATE_pred)` pooled over all 208 pairs | see §1.5 |

Uncertainty: a **cluster bootstrap over the 16 interventions** (seed 2026); the 13
outcomes are never resampled. So an approach's score is asked to survive *a different
set of messages*, not a different set of outcomes. That is the generalisation the whole
environment is built around.

### 1.3 What "Pearson r within outcomes" isolates

`pearson_within_outcome()` centres `estimate_h` and `estimate_l` on their per-outcome
means and correlates the residuals — algebraically identical to regressing human on
predicted effects with outcome fixed effects.

The pooled r mixes two skills:

* **outcome-level skill** — knowing *which outcomes move at all* under a short text
  (proximal manipulation-check-like items move a lot, distal policy/behaviour barely).
  This is generic knowledge of the literature and is comparatively easy.
* **message-level skill** — knowing *which of the 16 messages works better than which*,
  on the same outcome. This is the hard, out-of-the-box capacity.

r_within keeps only the second. **The gap between pooled r and r_within is the share of
the pooled score that came from outcome-level knowledge.** The organizers say so
explicitly, and they will report both. A submission can therefore look good on pooled r
while having *no* message-level skill — and this session measured exactly that on
myself (§3).

Corollary that governs design: for the target study the outcome-level profile across the
13 outcomes is the reliable earner, and the 16-message ordering is the speculative one.
They should be built and calibrated *separately*, because they are scored separately.

Corollary 2, structural: **with only two non-control arms, r_within degenerates.** With
K=2 arms the within-outcome residuals are +-delta/2 per outcome, so r_within collapses to
the correlation of the arm-difference profile across outcomes. With K=1 it is undefined.
Read r_within only where K is large.

### 1.4 What r_adj corrects for — and what it does not

```
var_true = var(estimate_h) - mean(se_h^2)
r_adj    = cov(l, h) / ( sd(l) * sqrt(var_true) )
mse_true = mean((h - l)^2) - mean(se_h^2);  rmse_adj = sqrt(max(mse_true, 0))
```

* **Only the reference side is corrected.** Noise in the human half inflates `sd(h)` and
  drags raw r toward 0; subtracting the known mean sampling variance restores the
  denominator. Submission-side noise is handled at the source (the Tier-1 precision
  floor), not by this formula.
* **It is not a skill inflator.** It is the correlation my predictions would have with a
  *perfectly measured* human ATE table.
* **Guard:** if `var_true <= 0` the human ATE table has no reliable variance at all and
  r_adj is undefined. This environment reports `truth_half_reliability` (= var_true /
  var_obs), which is the single most important field in the diagnostics: it says how much
  of the target there is to hit. `orchinik2024` returned **0.000** — the two passages
  moved nothing, and every correlation on that task is an artefact (§3.4).
* Noise in the *human* half never biases beta. So **beta is an unbiased read of my own
  exaggeration even against a noisy half**, whereas r is not.

### 1.5 alpha and beta, and why beta is the actionable number

`run_calibration_pooled()` fits `ATE_h = alpha + beta * ATE_l` over all pooled pairs.

* beta < 1 -> predictions exaggerate. beta = 0.5 means every difference is doubled.
* alpha != 0 -> a constant offset: a lift that applies to every message equally and that
  my predictions miss.
* `beta_adj = beta / lambda`, `lambda = 1 - mean(se_l^2)/var(ATE_l)`, exists only for
  Tier 1, and only corrects *my own* sampling noise. A Tier-1 entry near the precision
  floor prints a low raw beta purely from its own sample size. **The raw beta is the
  headline**, so the deposited Tier-1 sample must be far above the floor or I am scored
  on my own draw noise.

The identity that makes beta actionable:

```
beta = rho * sd_true(h) / sd(l)          (rho = my true skill correlation)
```

so if I submit predictions whose spread equals my honest estimate of the true spread,
**beta reads back my skill directly**, and `pred x beta` is the MSE-optimal rescaling.
This is the design principle I used for submission 1 (§2.3) and it worked: the diagnostics
came back interpretable.

Two consequences I verified algebraically and then in the scorer:

1. **r, r_adj, r_within and mean_signed_error are exactly invariant** under
   `pred -> mean(pred) + kappa*(pred - mean(pred))`. Rescaling can only ever move
   RMSE_adj, beta, spread_ratio and (through sign flips near the mean) directional
   agreement. A resubmission that only rescales cannot buy correlation. Confirmed on
   `kerwer2025`, whose r_adj moved by 1e-4 (my 3-dp rounding) across the two submissions.
2. Therefore **ordering and magnitude are two independent products**, and only the second
   is cheaply fixable after the fact.

### 1.6 The floors and the Human-2 row — what they mean for a submission

* **`Floor: no effect`** (predict 0 everywhere). Under the half-credit rule its
  directional agreement reads exactly 50%. Its RMSE is `sqrt(mean(h^2))`, i.e. the RMS of
  the human ATEs themselves — and its RMSE_adj is essentially |mean human ATE|. **This
  floor is hard to beat when the true effects are small**, because any spread I add is
  pure added error unless it is correlated with the truth. On `orchinik2024` I lost to it
  (§3.4). Calibration is undefined for it (zero-variance regressor).
* **`Floor: all positive`** (predict +1 everywhere). Only its directional agreement is
  reported, and that number *is* the empirical chance level for directional agreement —
  the share of positive human ATEs. Since all 16 target messages are designed to raise
  trust, this floor will likely sit well above 50%, and beating 50% means nothing.
* **`Human replication` (Human 2)**. A second fresh human half of the same size, scored
  exactly like a submission. It is *not* a ceiling — it carries sampling noise, and a
  synthetic sample larger than the human half can legitimately score above it. What it
  really provides is the **noise scale of the task**: Human 2's r is roughly the split-half
  reliability of the ATE table. If Human 2's r_within is 0.3, then no approach can be
  expected to score much above 0.3 on r_within, and a submission scoring 0.25 is close to
  the information-theoretic limit rather than mediocre.
* **`Wisdom of crowds`** (the field's within-pair mean) is also non-competing; the gap
  between it and the best entry measures how independent the field's errors are. I cannot
  influence it, but it tells the operator what a consensus prediction is worth.

### 1.7 Practical constraints I must satisfy

* All 17 conditions x 13 outcomes, every cell exactly once, no NA. Composites are scored
  **as submitted, never recomputed** — so a Tier-1 row set must carry composites that are
  internally consistent with its items, because both are read.
* Tier-1 floor 500 per intervention / 1,000 control. Treat as a floor, not a target: the
  raw beta is computed from effects refit on *my* rows.
* `distrust_post` is reverse-valenced, so the all-positive floor is wrong on 16 of 208
  cells by construction, and my table must carry the sign flip.
* `belief_post` / `trust_post` are re-asked (pre-measured minutes earlier) -> own-answer
  anchoring compresses them relative to the never-asked composite.

---

## 2. How I predict (session-1 method)

### 2.1 Analysis-first, structural, no simulator

I am the predictor. No per-respondent LLM generation was used this session (none was
needed, and none was budgeted). Each task's ATE table is generated by an explicit
structural model written from the brief plus train-split anchors:

```
ate_pp(arm, outcome) = base(outcome)                      # outcome-level: what moves at all
                     + sum_f  load(outcome, f) * feat(arm, f)   # message-level: low-rank
                     + specific(arm, outcome)             # sparse, only where the arm text
                                                          #   mechanically implies the item
```

`base(outcome)` carries the outcome-level skill r_adj rewards; the low-rank feature term
carries the message-level skill r_within rewards; `specific` is reserved for cells where
the arm *asserts or instantiates the quantity the outcome asks about* (a "97% of
scientists agree" arm and a "what % agree?" outcome; an arm describing arrests and an
outcome asking "how radical was this?"). Those cells are where all my real message-level
skill turned out to live (§3.2).

### 2.2 Train-split anchors (this is what the numbers are made of)

Extracted this session into `anchors/` from `/workspace/datasets` (train split; outcomes
readable without limit). Full tables in `anchors/ANCHORS_A.md`, `anchors/ANCHORS_B.md`,
`anchors/voelkel2026_ates.csv`, `anchors/vlasceanu2024_ates.csv`,
`anchors/trust_effects.csv` (967 arm x outcome cells over 11 datasets).

**Magnitude, in pp of scale range:**

| family | median abs ATE | note |
|---|---|---|
| consensus perception (asserted quantity) | 9.1 | vdL2019 US +16.2 at control mean 68; Veckalov +6.5-7.0 at control mean 85-87 |
| directly-argued policy attitude | 7.6 | hackenburg/tappin message arms |
| behaviour (costly) | 4.1 but *signed near zero or negative* | see below |
| belief | 2.3 | |
| credibility of a *specific* communicator | 1.8 (up to 21 for strong persona manipulations) | |
| concern | 1.7 | |
| **trust in scientists** | **1.17** | |

**The trust prior (decisive for the target).** 39 randomised short-text arm x trust cells:
median abs ATE 0.97 pp, IQR 0.48-1.66, p90 2.40, max 5.03, **mean signed +0.58**. Broad
multi-item trust composites only: median 0.64, mean +0.88. gligoric's five *purpose-built*
trust-raising messages at n~880/arm: +0.17, +0.17, +0.48, +0.64, +0.93. Veckalov's
consensus message on trust in climate scientists at n=3,500/arm: -0.05 and +0.71. Only
koetke S5 (a vignette that rewrites the scientist's epistemic character) exceeds 1 pp.
Persona rewrites reach +4 to +16 pp — **that is the ceiling, and it is not what a message
does.**

**The proximity gradient** (the single most transferable structure I have): asserted
construct -> one step down = x4-8; -> two steps = x10-20. vdL2019 in one study: consensus
+16.2, belief +2.17, worry +1.56, policy +1.23. Trust is **not** downstream of a consensus
message at all (x20, indistinguishable from zero).

**Behaviour reverses.** Two independent train megastudies: voelkel2026 `Donation` mean
**-1.38 pp** (SD 1.19 across 10 arms); vlasceanu2024 US `WEPT` mean **-3.70 pp** (SD 3.61).
Attitudinal outcomes in the same studies are +1 to +5. Ordering of arms is stable across
attitudinal outcomes (Spearman 0.62-0.71) and **~0 against the costly-behaviour outcome**.
So for the target's `donation_ams` and `newsletter_signup` the honest prediction is a small
effect near zero or slightly negative, with almost no message-level structure.

**Spread, noise-corrected.** voelkel2026 true arm-to-arm SD is **0.98 pp overall / 0.49 pp
within outcome** — about half of the visible spread is sampling noise. vlasceanu global
3.69 / 1.91. tappin's 48 human-written messages: SD_true 1.50 (1.16 within issue).
hackenburg's frontier-model arms: SD_true **0.00**. gligoric, spampatti and koetke
tournaments: SD_true **0.00**. Split-half r on voelkel2026 post-only: r=0.37,
**r_within=0.12** — that is the human-vs-human ceiling for a megastudy of this shape.

**Implication for the target, stated now so the gate can test it:** 16 trust-raising
messages with a mean ATE near +0.8 pp should have an arm-to-arm true SD of roughly
**0.2-0.4 pp**. The 208-cell table is close to flat; almost all recoverable variance is
*between outcomes*, and the message ranking is mostly noise.

### 2.3 The submission-1 calibration principle

I deliberately did **not** import SCAFFOLD's kappa = 0.85. That constant was fitted to a
different predictor (an LLM completion), and SCAFFOLD's own two lines about beta are
mutually inconsistent under the algebra of §1.5 (see `OPEN.md`). Instead:

> **Submission 1 sets the predicted spread equal to my honest estimate of the *true*
> spread, taken from the train-split anchors — never larger, never shrunk for safety.
> Then beta reads back my skill, and the diagnostics are interpretable.**

This is why the goldwert message-level component was rescaled to arm-to-arm SDs of
0.8-1.2 pp on the sliders and 0.35-0.55 pp on the costly behaviours, matching
voelkel2026/vlasceanu2024 true spreads rather than my raw enthusiasm.

### 2.4 The per-task models

| task | structure imposed |
|---|---|
| `altenmueller2024` | competence/warmth trade-off across institute discipline: sociological lower on expertise, higher on morality; interdisciplinary between |
| `beall2017` | **control is the four information-only arms POOLED**, so each ATE = topic offset (climate/flu/marijuana/severe weather vs the topic grand mean) + advocacy effect (non-controversial / controversial), with a topic multiplier on how hard the controversial solution bites |
| `dablander2025` | 2 (legal march / civil disobedience) x 3 (no scientist / joins / endorses) additive; radicalness treated as a manipulation check (+30 pp) |
| `goldwert2026` | megastudy regime: base(outcome) from voelkel2026/vlasceanu2024 anchors; rank-2 message term (attitude strength, action strength) with arm z-scores transferred from the train-split analogues of the same framings; costly behaviour damped and donation base **negative** |
| `kerwer2025` | additive design factors (format, n effects, COI statement, publication-bias statement, practical-relevance statement) x 4 measures x 2 topics; COI-conflict is the large negative (integrity -8 pp, anchored on koetke's -9 to -11 for character manipulations) |
| `kim2024` | proximity gradient anchored on vdL2019/Veckalov: consensus arm +11.5 on perceived consensus, +1.6 belief, +0.8 policy, **+0.7 trust**; causal-evidence arm flatter on consensus, steeper on evidence/attribution |
| `orchinik2024` | family x stated-consensus-level profiles; Institutions passage loaded on the bias items, History passage on the skill items |

---

## 3. What the diagnostics said — mechanism-level reading

14 scored calls (7 tasks x 2). Full table in `runs/scoreboard.csv`.

### 3.1 Submission 1 (honest, unshrunk)

| task | r_adj | r_within_adj | rmse_adj | beta | spread_ratio | signed err | truth reliability |
|---|---|---|---|---|---|---|---|
| altenmueller2024 | 1.000 | 1.000 | 2.45 | 1.18 | 0.69 | **-3.00** | 0.35 |
| beall2017 | 0.493 | 0.150 | 6.45 | **0.30** | 1.27 | -1.47 | 0.59 |
| dablander2025 | 0.999 | 0.970 | 3.96 | 0.81 | 1.18 | **+3.42** | 0.91 |
| goldwert2026 | 0.221 | 0.153 | 2.10 | **0.32** | 0.46 | +0.24 | 0.44 |
| kerwer2025 * | 0.104 | 0.056 | 3.30 | **0.05** | 0.72 | +1.54 | **0.13** |
| kim2024 | 0.702 | 0.760 | 3.52 | **1.37** | 0.48 | -0.05 | 0.87 |
| orchinik2024 * | n/a | n/a | 0.99 | -0.03 | 1.17 | +0.06 | **0.000** |

`*` = `counts_toward_promotion: false`.

**Failure type 1 — magnitude, and it is not one-signed.** beta ranges from 0.05 to 1.37.
Where the arms are many and similar (goldwert 0.32, beall 0.30, kerwer 0.05) I exaggerate
by 2-20x. Where the arms differ on one explicit, strong axis and few outcomes are distal
(kim 1.37) I *under*-predict. **There is no single transferable kappa**, and SCAFFOLD's
0.85 would have been wrong in both directions. What *is* transferable is the identity
beta = rho x sd_true/sd_pred: the shrink I need is my skill, and my skill is a function of
the study's regime, not a constant.

**Failure type 2 — level.** mean_signed_error ran -3.0 (altenmueller), -1.5 (beall),
+3.4 (dablander), +1.5 (kerwer). Mean over tasks +0.25, SD 2.3: **I am unbiased on
average and badly wrong per study.** alpha catches exactly this. On altenmueller both
non-control institutes scored ~3.8 pp above the economics control on average, i.e. there
is a large across-the-board lift I did not model at all. On dablander I over-credited
scientist involvement by ~3 pp everywhere except radicalness.

**Failure type 3 — message-level skill is ~0.1 outside manipulation-check cells.**
r_within_adj: 0.15 (beall), 0.15 (goldwert), 0.06 (kerwer) versus 0.97 (dablander) and
0.76 (kim). The two high values are entirely earned by cells where the arm text *asserts
the quantity the outcome asks about* (arrests -> "how radical"; "97% agree" -> "what %
agree"). **Strip those and my message-level skill is 0.06-0.15.** That is the honest
number to carry into the target, where no outcome is a manipulation check for any message.

### 3.2 Submission 2 — a declared mechanism plus a replication control

Rule declared from the brief alone, before scoring, and applied as
`pred -> mean(pred) + kappa*(pred - mean(pred))` (level preserved, spread damped):

* **kappa = 1.00** where the arms differ on one explicit strong factor with few arms
  (`altenmueller2024`, `dablander2025`, `kim2024`) — i.e. *no change*. These three are
  **fresh-draw replication controls**: identical predictions, a different random human
  half, so their movement measures pure diagnostic noise.
* **kappa = 0.55** for explicit factorial contrasts without a restating outcome
  (`beall2017`, `orchinik2024`).
* **kappa = 0.35** for many-same-goal-arms / format-variant regimes
  (`goldwert2026`, `kerwer2025`) — the target's regime.

| task | kappa | rmse_adj 1 -> 2 | beta 1 -> 2 | spread_ratio 1 -> 2 |
|---|---|---|---|---|
| beall2017 | 0.55 | 6.45 -> **4.58** (-29%) | 0.30 -> **0.49** | 1.27 -> 0.73 |
| kerwer2025 | 0.35 | 3.30 -> **2.19** (-34%) | 0.05 -> 0.15 | 0.72 -> 0.25 |
| goldwert2026 | 0.35 | 2.10 -> 2.19 (+4%) | 0.32 -> **1.52** (overshoot) | 0.46 -> 0.15 |
| orchinik2024 | 0.55 | 0.99 -> 1.17 (+17%) | -0.03 -> 0.38 | 1.17 -> 0.48 |

**Reading.** Damping does exactly what §1.5 predicts and nothing more: r_adj and
r_within_adj are unchanged to 3-4 dp everywhere (they are mathematically invariant), and
only RMSE_adj / beta / spread move. It buys a large RMSE_adj reduction precisely where
beta was far below 1 (beall -29%, kerwer -34%), and it costs where beta was already near
or above 1. On goldwert kappa=0.35 overshot beta past 1 — but note that *this draw's*
undamped beta would have been 1.52 x 0.35 = 0.53, not the 0.32 of the first draw, so the
overshoot is as much draw noise as mis-set kappa. **A kappa around 0.5, not 0.35, is the
defensible setting for the megastudy regime.**

### 3.3 What the replication controls measured (the most useful thing this session did)

Identical predictions, fresh human half:

| task | r_adj | r_within_adj | rmse_adj | beta | signed err | reliability |
|---|---|---|---|---|---|---|
| altenmueller2024 (10 cells) | 1.000 -> 0.907 | **1.000 -> 0.533** | 2.45 -> 2.13 | 1.18 -> 1.16 | -3.00 -> -1.99 | 0.35 -> 0.54 |
| dablander2025 (25 cells) | 0.999 -> 0.993 | 0.970 -> 0.968 | 3.96 -> 3.70 | 0.81 -> 0.81 | +3.42 -> +3.02 | 0.91 -> 0.91 |
| kim2024 (22 cells) | 0.702 -> 0.695 | 0.760 -> 0.817 | 3.52 -> 4.25 | **1.37 -> 1.57** | -0.05 -> -0.53 | 0.87 -> 0.90 |

**Draw-to-draw wobble with the prediction held fixed:** r_within up to +-0.47 on a 10-cell
task, beta +-0.20, RMSE_adj +-0.7 pp, mean_signed_error +-1.0 pp. On a high-signal task
(dablander, reliability 0.91) everything is stable to the third decimal.

Operational rule I adopt from this: **a diagnostic from a single task with fewer than ~50
cells, or with `truth_half_reliability` below ~0.4, must not be acted on.** That
disqualifies altenmueller, kim, kerwer and orchinik as evidence about a *method*; only
beall (96 cells, rel. 0.59) and goldwert (204 cells, rel. 0.44) carry method-level signal
on this validation set, and goldwert is the only one shaped like the target.

### 3.4 orchinik2024 and the no-effect floor

`truth_half_reliability = 0.000` on both draws: `var(estimate_h) - mean(se_h^2) <= 0`.
The 25 conditional-judgement items ("suppose 97 of 100 scientists agreed...") were moved by
*neither* passage, and every correlation the scorer returns for this task is an artefact of
that guard (r_adj printed -944 and then +1.000). My RMSE_adj of 0.99 pp is **worse than the
no-effect floor**, whose RMSE_adj on this task is about |mean human ATE| ~ 0.3 pp. I paid
1 pp of RMSE for spread that had nothing to correlate with.

Transferable lesson, which is about the *instrument* and not about this study: **hypothetical
/ conditional judgement items that every respondent answers under a stipulated premise are
close to unmovable by a short passage.** They anchor on the stipulated premise, not on the
treatment. When a brief contains such items, `base(outcome)` should be set near zero and
the message-level term suppressed entirely.

---

## 4. What I now believe about predicting the target

1. **Two products, calibrated separately.** The outcome-level profile over the 13
   outcomes is where the recoverable score is; the 16-message ordering is worth ~0.1 in
   r_within and must be submitted damped accordingly. Building them as one number and
   scaling once is what produced beta = 0.30 on beall and goldwert.
2. **The target is the low-skill regime.** 16 messages all designed to raise trust, no
   outcome that restates any message's assertion, a trust prior with median abs ATE
   ~1 pp and an expected arm-to-arm true SD of 0.2-0.4 pp. Expect r_within near 0.1 and
   Human 2 itself not far above it. Predicting a wide, confident message ranking is the
   way to lose to the no-effect floor.
3. **Levels are my largest single error and they are not fixable from validation
   feedback** (fitting them per study is the documented failure mode). They have to come
   from the control-condition anchors (TISP for the 12-item trust scale, Pew for
   party/race gaps) and from the proximity gradient, not from the predictor's enthusiasm.
4. **The costly-behaviour outcomes (`donation_ams`, `newsletter_signup`) get a small
   near-zero-or-negative base and essentially no message-level structure.** Two
   independent train megastudies agree on the sign; the all-positive floor will be wrong
   there, and so would I be if I followed it.
5. **`distrust_post` sign flip and the re-asked compression of `belief_post` /
   `trust_post`** are free, mechanical, brief-only corrections. Take them.

**Verification against the mounted benchmark (session s2b).** §4 was written before
`/workspace/benchmark` existed. Every claim above was re-checked against
`codebook.csv`, `scripts/lib/submission_spec.R`, `survey/questionnaire.txt` and
`scripts/lib/check_lib.R`. Verdicts, with the evidence, are in §6. In one line each:

| §4 claim | verdict |
|---|---|
| 1. two products, calibrated separately | **verified and strengthened** (§6.6: the message effect is ~rank-1; the outcome profile is the reliable part) |
| 2. low-skill regime, true arm SD 0.2-0.4 pp | **verified as a regime**, but the SD band is revised **up to 0.4-0.8 pp** (§6.7) |
| 3. levels come from anchors, not from feedback | **verified**; the anchor set now exists (`anchors/ANCHORS_D.md`) |
| 4. costly-behaviour outcomes get near-zero base and no message structure | **partly retracted** — the *units* were wrong (§6.3): in pp of scale range `donation_ams` and `newsletter_signup` are **not** small outcomes |
| 5a. `distrust_post` is reverse-valenced | **VERIFIED** (§6.2) — it is scored, it is not reverse-coded in cleaning, so a trust-raising arm must get a **negative** ATE |
| 5b. `belief_post` / `trust_post` are re-asked and compressed | **verified as structure, downgraded as inference** (§6.2): `belief_pre` / `trust_pre` are asked verbatim pre-treatment, so the compression mechanism is real, but the size of the compression is a hypothesis, not a mechanical correction |
| (not in §4) `funding_perceptions` | **new trap, now closed** (§6.2): it *is* reverse-coded in cleaning, so the pro-science direction is **positive** |

## 5. Standing rules for this arm (revisable on evidence)

R1. Submit spread equal to the honest estimate of *true* spread, so beta reads back skill.
R2. Damp the message-level component by expected message-level skill; default ~0.5 in the
    many-similar-arms regime, 1.0 only for cells where the arm asserts the measured quantity.
R3. Never act on a task-level diagnostic with < 50 cells or reliability < 0.4.
R4. Never fit a level or a ranking to validation feedback; only mechanisms cross the gate.
R5. Any predicted trust ATE above ~2 pp needs its warrant written into the report.
R6. Conditional/hypothetical-premise items: base ~0, no message-level term.
R7. Always convert to the scorer's unit **before** judging whether an effect is small.
    (`donation_ams` /10, `newsletter_signup` /1: $0.10 and 1 signup-point are both 1 pp.)
R8. Check every outcome's cleaning rule for a reverse-code before assigning a sign:
    `distrust_post` is not reverse-coded (so trust-up = ATE-down); `funding_perceptions`
    is (so pro-science = ATE-up).
R9. Build the message term as a *family* score (the `tag` column of
    `condition_codenames.csv`) times an outcome loading — rank-1 — and never above rank 1.
R10. Backward synthesis must be mean-matched and run well above the precision floor;
    verify by recomputing the scored quantities from the rows, not by trusting the draw.
R11. A companion file that returns no diagnostic is still worth submitting if it is the
    honest prediction, but it may not be counted as evidence for anything.

**R2 is superseded by R12-R14 (session s3, after the first gate verdict).**

R12. **A shrink constant is a STUDY-level scalar.** Apply one kappa uniformly to every
    cell of a study. Never vary kappa by cell, by outcome or by arm. Proof obligation
    discharged in §8.1: a kappa that is uniform *within* an outcome is provably invisible
    to `r_within_adj`, so a kappa that varies *across* outcomes cannot be buying
    message-level ordering — all it does is rescale the outcome profile, which is the
    component I have real skill on. That is what the first gate rejected.
R13. **Content confidence belongs in the raw prediction, or in an additive term — never
    in a kappa override.** If I believe one cell harder than the others (assertion match),
    that belief is expressed as a larger raw residual or as an explicit additive cell term
    applied after the shrink, so the shrink stays uniform and interpretable.
R14. **Amplitude is a two-level property and both levels are regime-dependent.** Carry a
    separate multiplier for the outcome profile (`lam_btw`) and for the message residual
    (`kappa`), and set both from the regime, not from the study. Measured (§8.2):
    many-variant regime (>= 6 arms that are variants of one goal) `lam_btw ~ 0.4-0.5`,
    `kappa ~ 0.15-0.20`; distinct-intervention regime (<= 5 arms) both ~ 1.
R15. **`cal_beta` is an actionable instrument, and it was verified as one** (§8.3):
    rescaling a whole table by its previously measured beta moved beta to 1.00 +/- 0.05 on
    a *fresh* half, in both the shrink and the expand direction. Treat beta as a
    measurement of amplitude error, not as a number to chase.
R16. **Synthesis must be a matched design.** One quota-exact profile deck, reused by every
    condition; moderator main effects centred on the quota; reflection rather than clipping
    at the bounds; largest-remainder integer rounding; a marginal-cell repair sweep. Every
    scored item in this instrument is integer-valued, so a synthetic table cannot carry a
    fractional cell mean and must be driven onto the lattice deliberately (§8.4).

---

## 6. The benchmark inventory (session s2b) — what the mounted target changes

`/workspace/benchmark` is the official template at its pinned commit. Read in full:
`README.md`, `FAQ.md`, `codebook.csv` (63 rows), `scripts/lib/submission_spec.R`,
`scripts/lib/check_lib.R`, `survey/questionnaire.txt` (74.8 kB, chronological),
`survey/condition_codenames.csv`, `metadata.json`, the four `predictions/example_*` files.
Cross-read with `inputs/organizer_code/{statistics.R, preregistration_benchmark.qmd}`.

### 6.1 The grid, exactly

* **17 conditions** = `control` + the 16 non-interactive intervention titles in
  `submission_spec.R`. The parent megastudy has **20** interventions plus control; the
  benchmark scopes out 4 interactive arms (3 LLM-chatbot, 1 "Value similarity" quiz).
  So per-arm n in the *scored* study is set by a 21-cell randomisation of ~18,000, and
  the human half every submission is scored against is **500/intervention, 1,000 control**.
* **13 outcomes**: `trust_multidimensional` (primary; mean of the four 3-item trust
  subscales), `trust_post`, `distrust_post`, `funding_perceptions`, `policy_role_mean`,
  `inst_trust_mean`, `belief_post`, `concern_mean`, `policy_general`,
  `policy_specific_mean`, `behavior_mean`, `donation_ams`, `newsletter_signup`.
  The 12 trust items ship in Tier 1 but are **not** among the 13.
* **6 moderators / 27 levels**: gender(3), age_band(4), race(5), education(6), income(5),
  party(4) — with the *exact* level strings enforced by `check_lib.R`. The Tier-2
  moderator grid is 17 x 27 x 13 = **5,967 cells**; the example file has 5,967 rows + header.
* Section 1 pools **16 x 13 = 208** intervention x outcome ATEs.

### 6.2 Coding and valence — the three sign traps, resolved

1. **`distrust_post` — VERIFIED reverse-valenced.** `distrust_1` ("How much do you
   *distrust* climate scientists?", 0-100) is scored *as asked*; there is no
   reverse-coding row for it in `codebook.csv` section B. A message that raises trust
   must therefore be predicted with a **negative** ATE on `distrust_post`. This is 16 of
   the 208 pooled cells (7.7%), and the organizers' `Floor: all positive` row is wrong on
   every one of them by construction. Free directional credit; also free Spearman/Pearson
   credit, because it is the only outcome whose 16 ATEs should sit on the other side of zero.
2. **`funding_perceptions` — the opposite trap, now closed.** The raw item `funding_5`
   runs 0 = *far too little* -> 100 = *far too much*, but cleaning defines
   `funding_perceptions = 100 - funding_5`. The submitted variable therefore means
   "supports more funding", and a pro-science message gets a **positive** ATE. Predicting
   the raw item's direction would have cost another 16 cells with the wrong sign.
3. **`belief_post` / `trust_post` are genuinely re-asked.** `questionnaire.txt` shows
   `belief_pre` and `trust_pre` measured **before** the condition, in verbatim-identical
   wording, for every respondent. The compression mechanism (respondents anchor on their
   own just-given answer) is real and structural. But its *magnitude* is a hypothesis, not
   a mechanical correction: the pre-item is balanced across arms, so it biases nothing —
   it only damps. Recorded as a directional prior with a stated size band (§6.7), not as a
   free correction. Corollary worth more than the prior itself: **`trust_multidimensional`
   (the primary) is NOT pre-asked**, so the primary outcome should move *more* than the
   single-item `trust_post` that asks nearly the same question. That is a within-study
   ordering prediction the scorer's outcome-level term will read.

### 6.3 Units — the largest single correction the mount produced

`preregistration_benchmark.qmd` fixes `scale_range = c(<all sliders> = 100,
donation_ams = 10, newsletter_signup = 1)`, applied once at pair-building. Consequences:

* **$0.10 of donation = 1.0 pp.** A $0.25 donation effect is 2.5 pp — larger than any
  trust-slider effect I expect anywhere in the table.
* **1 percentage point of signup = 1.0 pp.** A signup rate moving 10% -> 12% is 2.0 pp.
* So §4.4's "the behavioural outcomes are small" was **an artefact of reading them in
  native units**. They are small in dollars and probabilities and *large* in the scored
  unit; they carry 32 of the 208 cells; and the qmd says the rescaling exists precisely so
  they cannot be drowned out. They are also the two outcomes on which the train split says
  the *sign* flips (voelkel2026 donation -1.38 pp, vlasceanu2024 WEPT -3.70 pp).
  **Revision: the behavioural pair is now a high-leverage, high-variance part of the
  prediction, not a rounding error.** They are also the whole of the qmd's secondary
  "Behavioral" outcome class, which is reported separately — an entire reported cut of the
  results rests on 32 cells I had planned to treat as noise.

### 6.4 What the scorer does and does not use

* ATEs are **unadjusted OLS difference-in-means** with HC2 SEs; the qmd states plainly
  that "no scoring model uses the functions' `covariates` argument". The pre-measures are
  *not* covariates in the estimand. (ANCOVA remains the right way to read *train* anchors —
  it cut anchor noise 5x on voelkel2026, `ANCHORS_C.md` — but it must not be smuggled into
  what I predict.)
* `newsletter_signup` goes through logistic marginal effects on the probability scale for
  Section 1, and a **linear probability model** for the Section-2 interactions.
* Section 2 scores the **condition x moderator interaction coefficients** from
  `lm(y ~ condition * moderator)`, i.e. differences-in-differences against
  (`control`, first moderator level). "No moderation" = every interaction exactly 0.
  `README.md` and `FAQ.md` both name repeating the condition mean in a group's cells as
  "a real, honest prediction". The honest floor is sanctioned by the organizers.
* Composites are **read as submitted**, never recomputed. `check_lib.R` only *warns* when
  `trust_multidimensional` disagrees with its 12 items by > 0.5.
* Tier-3 `ate` is explicitly **not** range-checked; Tier-2 `mean` is, per outcome
  (0-100 / 0-10 / 0-1).

### 6.5 The 16 messages, as the design groups them

`survey/condition_codenames.csv` ships a third column, `tag`, that the README never
mentions: **the organizers' own family label for each arm.**

| family | arms |
|---|---|
| Scientific methods and results | Measurement & modeling (1), Measurement & modeling (2), Model accuracy |
| Applications and impact | Extreme weather predictions, Portrait Prof. Cherry |
| Collaboration and peer-review | Interview Prof. Maraun, Peer-review |
| Others' endorsement | Corporate reliance, Former skeptics |
| Values | Interview Prof. Sebille |
| Other | Consensus, Funding, High public trust, Oil industry misinformation, Scientist community helpers, Social justice |

This is the natural low-rank basis for the message term: predict a **family** score and
damp within-family differences hard. It is design information, not outcome information, so
it is legitimate under blinding, and it is exactly the structure `ANCHORS_C.md` says is the
only estimable one (rank-1 arm score, median 0.775 of true within-outcome variance;
rank >= 2 unestimable at n ~ 1,000/arm).

### 6.6 Assertion-match, re-derived from the real texts

Session 1's M3 said: full-size message-level claims only where the arm asserts the quantity
the item asks about. Reading the 16 texts, that rule fires on **exactly three** cells of 208,
and two of them are stronger than anything the validation set contained, because those two
arms *elicit an estimate first and then correct it in the same screen*:

* **Consensus x `belief_post`.** The arm elicits perceived scientific agreement, then
  states "99% of climate scientists agree that human activities ... are the main cause".
  `belief_post` asks how accurate "Human activities are causing climate change" is. Same
  proposition, corrected on-screen, item asked minutes later. Largest single cell in the table.
* **Funding x `funding_perceptions`.** The arm elicits agreement with "the federal
  government allocates significant resources to climate research", then argues at length
  that federal climate R&D ($10.6bn) is small next to biomedical ($52.5bn) and that only 3%
  of "climate research" programs are primarily climate. `funding_perceptions` asks exactly
  whether the government spends too much or too little. Same proposition, opposite prior,
  corrected on-screen.
* **High public trust x `trust_post` / `trust_multidimensional`** is a *weaker* match: the
  arm elicits and corrects a **descriptive norm** ("what % of Americans trust climate
  scientists" -> 76%), not the respondent's own trust. Gateway-belief transfer from a norm
  to a personal attitude is real but is a fraction of the norm shift. Half-strength, not full.

No other arm asserts a quantity any of the 13 items asks for. Everything else is damped.

### 6.7 Revised target picture (numbers as bands, not predictions)

* **Per-cell noise on the human half.** With sigma ~ 22 pp on a trust slider,
  n = 500 vs 1,000, SE(ATE) ~ 1.2-1.4 pp. `ANCHORS_C.md`'s projection for k = 16 arms
  gives a within-outcome noise floor of ~0.91 pp^2 on the half. Truth-half reliability
  for the *message-level* component then lands at **0.15-0.41** for a true within-outcome
  SD of 0.4-0.8 pp, i.e. a ceiling on r_within of **~0.39-0.64** — and that is the ceiling
  for Human 2 as well as for me.
* **True arm-to-arm SD, revised up to 0.4-0.8 pp** (was 0.2-0.4): voelkel2026's
  noise-corrected message-level SD is 0.57-0.70 pp on 8 attitudinal sliders at ~1,000/arm,
  and voelkel2024 (25 arms) 1.51 pp. The target's arms are more homogeneous in goal than
  voelkel2024's and less than a same-topic tournament, so the low end of that range.
* **Mean ATE.** Trust-message anchors (`ANCHORS_B.md`, 39 cells) put median |ATE| at
  ~1 pp with mean signed +0.58 pp; the outcome-level profile should be strongly
  decreasing with distance from "climate scientists": trust items > institutional trust >
  belief/concern > policy > behaviour intentions > costly behaviour.
* **Directional agreement's chance level** is the `Floor: all positive` row, i.e. the
  share of positive human ATEs. Predicting `distrust_post` negative is how you beat it
  without claiming any message-level skill.

### 6.8 Environment facts confirmed by running it

* `R 4.x` + `tidyverse`/`jsonlite`/`digest` are installed in this container, so
  `make check` / `make manifest` / `make clean` all run **locally, offline**. A copy of
  the template at `target_entry_scaffold/` passes `make check` end to end.
* `make manifest` fingerprints *everything* matching `predictions/<team_id>_*.csv`, and
  `check_lib.R` FAILs a Tier-1 entry that lists more than one prediction file. Tier-2/3
  mirrors must live outside `predictions/`.
* A Tier-1 entry needs `team_id`, which is assigned by the organizers by email. It is not
  in the repo and cannot be invented; the validator reports the state as *staged*.
  **This is an operator item, not a modelling one** (`OPEN.md` A5).

### 6.9 Control-level anchors (from `anchors/levels.csv`, 2,220 rows, train split only)

US adult mean trust in scientists, rescaled to 0-100 percent of each item's scale range:

| source | item | year | n | mean |
|---|---|---|---|---|
| TISP | TRUST_SCI, **12-item 1-5 composite** (the closest instrument analogue) | 2022-23 | 2,559 | **71.5** |
| TISP | CLIM_TRUST — trust in **climate** scientists | 2022-23 | 2,557 | **67.0** |
| ANES 2020 | 0-100 feeling thermometer, scientists | 2020 | 7,367 | 78.0 |
| ANES 2024 | CSES 4-pt trust in scientists | 2024 | 4,702 | 71.0 |
| GSS | `consci`, 3-pt confidence | 2024 | 2,121 | 62.2 |
| Pew ATP W100/W114 | 4-pt confidence, scientists act in best interests | 2021/22 | 7,181/5,259 | 67.0 / 66.8 |
| Pew ATP W135 | climate scientists understand *whether* it is occurring | 2023 | 8,842 | 63.7 |
| Wellcome 2020 | 4-pt trust scientists in this country | 2020 | 993 | 81.7 |
| koetke2024 S1-S5 | METI 14-item 7-pt bipolar | 2023 | 298-679 | 73.8-81.0 |

Three things follow, all of which the target's control row needs.

1. **Format drives ~20 pp of the level.** 3-4 point confidence scales land 62-67;
   1-5/7-point multi-item trust batteries land 71-81; 0-100 thermometers land ~78. The
   target's primary outcome is a **12-item 0-100 slider battery**, i.e. the TISP/METI
   family, so its control mean belongs near **68-75**, not near the 4-point-scale numbers.
   Trust in *climate* scientists specifically sits ~4 pp below trust in scientists in the
   one source that measures both on the same instrument (TISP: 67.0 vs 71.5).
2. **Headroom is ~25-30 pp, and it is not symmetric.** A control mean of ~70 on a 0-100
   slider leaves little room above and a long tail below; ceiling compression is the
   reason a +1 pp mean ATE is the right order of magnitude and +5 pp is not.
3. **The GSS series is the only long trend, and it is falling**: ~68-70 for four decades,
   70.3 in 2021, 63.2 in 2022, 62.2 in 2024. Whatever the 2026 control mean is, the recent
   direction is down, which argues against importing a pre-2020 level.

**Four refinements from `ANCHORS_D.md` that change the target's control row and the
message ordering:**

* **Climate scientists sit below scientists in general**, on the same respondents:
  TISP 67.0 vs 71.5 (-4.5); gligoric2025 climatologists 61.8 vs a 35-occupation grand mean
  of 71.7 (-9.9); Pew W135 2023 runs 63.7 (understands whether) down to 50.8 (understands
  best ways to address). Recommended control anchor for a 12-item composite fielded in
  2025-26: **generic trust ~70-72, climate-scientist trust ~60-67**.
* **Facet ordering inside the composite** (Pew W42, environmental scientists):
  competence 75.4 > benevolence 72.1 > integrity 71.4 >> **transparency 59.4, admits
  mistakes 57.5**. The target's primary averages competence, integrity, benevolence and
  **openness**, and openness runs 13-18 pp below competence. Two consequences: the primary
  composite's control mean sits below any competence-only anchor, and the arms that speak
  to openness — `Peer-review`, `Interview Prof. Maraun` (self-correction, revising results),
  `Funding` (transparency about who pays) — are aimed at the facet with the most headroom.
* **The party gap is amplified ~1.4x for climate-specific items**: median -21 pp
  (Rep - Dem) for generic trust, **-27 to -31 pp** for climate-scientist items; the same
  amplification appears in ideology within a single instrument (TISP -22.2 climate vs -9.3
  generic). It is a *level* anchor for the control row, not a moderation prediction.
* **The reality check that bounds every ATE I will write.** In the design twin
  (voelkel2026) the control arm's own pre->post drift is |d| <= 2.1 pp on all 8 outcomes.
  Nominal headroom is 22-35 pp, but between a quarter and a third of respondents are
  already at the ceiling on single-item measures (GSS 41.6%, TISP CLIM_TRUST 35.5%, ANES
  thermometer 29.4%; the 12-item composite is the least compressed at 9.9%).
  **Realistic message ATEs live in 0-3 pp**, which is the same band the trust-message
  anchors in `ANCHORS_B.md` give, arrived at from a different direction.

Subgroup gaps (party, race, education, age, gender) are in `levels.csv` under the
`moderator`/`level` columns for every source that carries demographics; `ANCHORS_D.md`
summarises them. They are level anchors for the *control* row, not moderation predictions —
the Section-2 prediction remains the honest zero-interaction floor.

---

## 7. The target entry: structure, and the one hard constraint backward synthesis hits

`tools/target_entry.py` implements the path, with placeholder numbers only:

```
S1 spec()          parse submission_spec.R + codebook.csv -> 17 x 13 x 27 grid, scale ranges
S2 target_table()  THE ONLY PLACE PREDICTED NUMBERS ENTER
                     control_mean[outcome], ate_pp[condition, outcome],
                     mod_delta[moderator level, outcome], shape[outcome]
S3 synthesize()    draw rows under census quotas
S4 verify()        recompute cells / ATEs / interaction contrasts FROM THE ROWS and
                   report max |recovered - intended|
S5 write_entry()   predictions/<team>_T1_<entry>_v1.csv (+ T2/T3 mirrors in derived/)
```

**The finding that changes the plan.** Backward synthesis is not free. Measured on the
real grid, with an intended table that is exactly flat (all ATEs 0, all interactions 0):

| synthesis | rows | mean abs ATE error | max abs ATE error | max abs interaction |
|---|---|---|---|---|
| i.i.d. draws at the precision floor | 9,000 | **0.97 pp** | 3.62 pp | 33.9 pp |
| mean-matched at the precision floor | 9,000 | 0.065 pp | 0.76 pp | 3.00 pp |
| mean-matched, 6x the floor | 54,000 | **0.027 pp** | 0.29 pp | 0.96 pp |

The first row is the trap: a Tier-1 entry built by drawing respondents independently at
the organizers' minimum injects **~1 pp of pure sampling noise into every predicted ATE** —
about twice the entire true arm-to-arm spread the target is expected to have (§6.7). The
predictions would be noise-dominated by the synthesis step, not by the prediction step, and
no amount of good analysis upstream would survive it. The two fixes, both implemented:

1. **Mean-matched residuals** (`--exact`): draw residuals, then sweep them to zero mean
   within every marginal the scorer reads — the condition cell and each condition x
   moderator-level cell (iterative marginal centring, 8 passes). Cost: nothing. Effect:
   15x lower ATE error at the same n.
2. **Oversample well past the floor.** The README is explicit that beyond precision a
   bigger pool buys nothing *for the score* — but it buys fidelity of the backward
   synthesis, which is a different thing. 6x the floor is enough to hold the moderator
   grid to ~1 pp; the rarest cells (gender "Other" x an intervention) drive the maximum.

**Consequence for the honest moderation floor.** A Tier-2 moderator file can state
"no moderation" exactly. A Tier-1 file can only state it up to synthesis noise, and at the
floor that noise is ~34 pp in the smallest cells. Since Tier 1 is scored on *every*
analysis and is the preferred tier, the entry plan is: **Tier 1, mean-matched, at several
times the floor** — and the deposit-time check is not `make check` (which cannot see this)
but `verify()`'s max-error report.

---

## 8. The first gate verdict, and what it actually diagnosed (session s3)

`runs/20260827T202417Z_s2/gate_m1w-k05-m3.json`:
**REJECTED**, failure category **"scientist credibility (framings)"**.
Candidate s2/sub-1 (M1w at kappa=0.5 + M3 exemptions), baseline s1/sub-1 (kappa=1).

Of the five promotion tasks, only `beall2017` and `goldwert2026` differed. `beall2017`
is the one with a `credibility` block (four of its twelve outcomes) and arms that are
framing variants of one op-ed. So the category points at `beall2017`'s credibility family,
and the question is *what the candidate did to it*.

### 8.1 What it did: M3 was not a cell exemption, it was an outcome-amplitude reweighting

Recovering the effective per-cell kappa from the two submission files
(`kappa = (ate_s2 - m(o)) / (ate_s1 - m(o))`) gives a completely uniform picture:
**kappa = 0.5 on eleven of beall2017's twelve outcomes and kappa = 1.0 on all eight arms
of the twelfth, `research_controversial`.** The "assertion-match cell exemption" was, in
this study, an exemption of an entire *outcome*.

That has an exact and damaging consequence. The organizers compute `pearson_within` by
centring both sides within outcome and then taking **one pooled Pearson r** over all cells
(`statistics.R:1150`). An outcome's weight in that pooled r is therefore proportional to
its within-outcome prediction spread. Leaving one outcome at full amplitude while halving
the rest re-weights the pool:

| outcome | share of within-outcome variance, s1 | same, s2 candidate |
|---|---|---|
| `research_controversial` | 0.362 | **0.694** |
| `motive_political_views` | 0.350 | 0.168 |
| the four `credibility_*` outcomes, together | 0.086 | **0.041** |
| the other six | 0.202 | 0.097 |

A single outcome went from carrying a third of my message-level bet to carrying **more than
two-thirds of it**, and the credibility family — 32 of the 96 cells, and the family the
study's framing manipulation is actually aimed at — was turned down by half relative to
everything else. The gate named exactly that family.

**And the exemption bought nothing it was supposed to buy.** M1w applied uniformly within
an outcome rescales `l_c` by a constant and leaves the pooled within-outcome correlation
*exactly* unchanged. Verified numerically in `tools/level_transform.within_invariance()`:
against a fixed truth vector, kappa = 1.0 / 0.5 / 0.2 / 0.05 all return
r_within = 0.645148. A per-outcome-differential kappa returns 0.591. So the only thing a
differential kappa can do is move the outcome profile. It cannot improve message-level
ordering, because ordering is scale-invariant.

**Mechanism-level verdict: the constant 0.5 was not the defect. The per-cell exemption was.**
Hence R12/R13, and hence the s3 candidate removes the exemption and keeps one study-level
kappa. This session's s2b reading that "kappa* = r_within_adj, measured 0.10-0.19" is
*confirmed as an estimate* but was measured on a quantity M1w cannot influence; the
r_within movements I attributed to kappa between s1 and s2 were fresh-draw noise.

### 8.2 Amplitude is two numbers, not one, and the regime sets both

Pooled `cal_beta` is a variance-weighted mix of an outcome-level slope and a message-level
slope: `beta = share_btw * beta_btw + (1 - share_btw) * beta_wth`. `share_btw` is computable
from my own submission; `beta_wth` is what `r_within_adj` estimates when the spread is
honest. Solving, on the unshrunk (kappa = 1) submissions:

| task | arms | share_btw | beta pooled | beta_within | **beta_between** |
|---|---|---|---|---|---|
| altenmueller2024 | 2 | 0.837 | 1.213 | 0.844 | 1.284 |
| kim2024 | 2 | 0.720 | 1.430 | 0.804 | 1.674 |
| dablander2025 | 5 | 0.577 | 0.801 | 0.966 | 0.681 |
| **beall2017** | 8 | 0.635 | 0.298 | **0.150** | **0.384** |
| **goldwert2026** | 17 | 0.622 | 0.318 | **0.153** | **0.418** |

`beall2017` and `goldwert2026` — 96 and 204 cells, different outcome sets, different
literatures, different halves — agree to two decimals on *both* components. That is a
**regime** effect, not a study effect: when a study's arms are many variants of one
persuasive goal, real effects are small at *every* level of the decomposition, and a
content-reading predictor over-states the outcome profile by ~2.4x and the message
ordering by ~6.5x. When the arms are a handful of qualitatively distinct interventions,
the same predictor is about right (0.68-1.67) or too flat.

Two consequences. (a) Both multipliers must be carried separately (R14). (b) The target is
a 16-near-synonymous-arm megastudy, so the target sits squarely in the many-variant regime
and both corrections apply to it — `tools/target_model.py` uses `KAPPA = 0.20`,
`LAM_BTW = 0.50`.

### 8.3 `cal_beta` verified as an actionable instrument

The obvious objection to §8.2 is that `beta` is a diagnostic computed on a noisy half and
might not be *actionable*. s3 spent two scored calls testing exactly that, on the two tasks
where `beta` is most precisely measured, in **both** directions:

| probe | prior beta (n draws) | applied lam_all | beta returned on a FRESH half | RMSE_adj |
|---|---|---|---|---|
| dablander2025 (shrink) | 0.81 (3 draws, reliability 0.90) | 0.81 | **1.041** | 3.49 -> 2.96 |
| kim2024 (expand) | 1.43 (3 draws, reliability 0.87) | 1.43 | **0.957** | 3.25 -> 3.45 |

Rescaling by the previously measured beta lands beta on 1.00 +/- 0.05 on an independent
half, in both directions. In the shrink direction RMSE_adj falls 15%; in the expand
direction it does not, which is the textbook calibration/MSE trade-off and not a
contradiction. **beta is a measurement instrument I can trust** — which is what licenses
using beall2017 + goldwert2026's beta to set the target's amplitudes (R15).
These two probes are per-study by construction and are explicitly **not** part of the gate
candidate and not claimed as promotable.

### 8.4 What the s3 candidate measured, on an identical half

`beall2017` s3/sub-1 drew **the same human half as s1/sub-1** — `truth_half_reliability`
0.5920, `mean_signed_error_pp` -1.4730 and `r_within_adj` 0.1498 are bit-identical. The
comparison is therefore free of fresh-draw noise, which is the only such comparison this
environment has produced:

| beall2017, identical half | baseline kappa = 1 | **s3 candidate, uniform kappa = 0.20** |
|---|---|---|
| `r_adj` | 0.4930 | **0.5352** |
| `r_within_adj` | 0.1498 | 0.1498 (identical — §8.1's theorem) |
| `rmse_adj_pp` | 6.4503 | **5.2362** (-18.8%) |
| `cal_beta` | 0.2985 | **0.4022** |
| `spread_ratio` | 1.2707 | **1.0238** |

Better on every metric that M1w can move, unchanged on the one it provably cannot, and
better than the *rejected* s2 candidate (r_adj 0.425, RMSE_adj 6.70) as well.

### 8.5 The synthesis fixes this session forced

Running real numbers through the harness exposed four defects that placeholder numbers hid.
Fixed in `tools/target_entry.py`, and the effect measured on a 54,000-row entry:

| defect | why it matters | fix |
|---|---|---|
| moderator composition drawn multinomially per condition | party main effects up to 16 pp x a 0.8% composition wobble = 0.3-0.6 pp of noise on **every** ATE | one quota-exact profile **deck**, reused by every condition |
| `mod_delta` not quota-centred | control level drifted 3 pp below the anchored value | subtract the quota-weighted column mean |
| `np.clip` at the bounds | one-sided mass transfer; worst on `donation_ams`, whose mean sits under one SD from the floor | reflect at the bounds, then re-centre to the intended mean |
| plain `np.round`, and a binomial signup draw | every scored item here is integer-valued; a binomial 0/1 draw puts ~0.6 pp of noise on an outcome whose whole predicted ATE is 0.3 pp | largest-remainder rounding + systematic (Madow) selection + a marginal-cell repair sweep |

| synthesis | max abs ATE error | mean abs ATE error | max abs interaction (native) |
|---|---|---|---|
| s2b best (mean-matched, 6x floor) | 0.29 pp | 0.027 pp | 0.96 |
| **s3 (matched deck, 54,000 rows)** | **0.017 pp** | **0.0011 pp** | 1.00 |

Synthesis noise on the ATEs is now ~1.5% of the smallest predicted effect instead of
comparable to it. The residual ~1 pp of interaction error lives entirely in the smallest
marginal cells (gender "Other" is 1% of an arm) and is bounded by the integer lattice
there.


---

## 9. After the first promotion (session s4): the standing method

### 9.0 The verdict

`runs/20260827T205641Z_s3/gate_m1w-v2-k02.json`: **PROMOTED**
(candidate `20260827T205641Z_s3` k=1, baseline `20260827T194235Z_s1` k=1,
`failure_category: null`). The mechanism promoted is **M1w-v2**: in the many-variant
regime, one **study-uniform** `kappa = 0.20` applied to every cell, with M3's per-cell
assertion-match exemption removed. R12/R13 are therefore no longer proposals; they are the
arm's promoted method.

### 9.1 The instrument got calibrated: how much r_adj noise a fresh draw actually carries

This is the enabling result of the session, and it cost nothing. `r_adj` is **exactly
invariant** to a whole-table rescale (`lam_all`), so every pair of submissions that differ
only in overall amplitude is a *free replication* of the same table on two independent
halves. Collecting them:

| task | n_cells | draws at one mix | mean r_adj | **sd across fresh halves** |
|---|---|---|---|---|
| altenmueller2024 | 10 | 6 | 0.980 | 0.036 |
| kim2024 | 22 | 7 | 0.752 | **0.082** |
| dablander2025 | 25 | 7 | 0.984 | 0.014 |
| beall2017 | 96 | 2 | 0.539 | **0.005** |
| goldwert2026 | 204 | 2 | 0.306 | **0.002** |

(The first three rows pool every draw of an unchanged mix; `lam_all` variants belong to the
same group because r_adj cannot see them. The last two rows pool the two draws taken at the
promoted mix.)

So on the two big many-variant tasks a difference of **0.02 in r_adj is signal**, while on
the small tasks even 0.15 is not. This supersedes R3's flat "50 cells / reliability 0.4"
cut with a graded one (**R17**), and it is what makes §9.2 readable.

### 9.2 The mix result: `lam_btw` is NOT a transferable regime constant — rejected on my own evidence

`lam_btw` does **two** things at once and s3 could not separate them: it lowers the total
amplitude *and* it doubles the message component's weight relative to the outcome profile.
s4 separated them by submitting, on the same task and run, two tables of nearly identical
total spread that differ **only** in mix:

* `submission_1` = **M5**, `lam_btw = 0.50` → amplitude ×0.517, mix (`sd_wth/sd_btw`) ×2.00
* `submission_2` = **M9**, `lam_all = 0.475` → amplitude ×0.475, mix **unchanged**

Because r_adj is scale-invariant, sub-2's r_adj is a clean fresh-half read of the *promoted*
mix. Pooling every draw ever taken at each mix:

| task | r_adj at promoted mix (0.152) | r_adj at M5 mix (0.30) | difference | in sd units |
|---|---|---|---|---|
| beall2017 | 0.5352, 0.5429 → **0.539** | 0.4103, 0.4957 → 0.453 | **−0.086** | ≈ 17 σ |
| goldwert2026 | 0.3047, 0.3074 → **0.306** | 0.3490, 0.3701 → 0.360 | **+0.054** | ≈ 28 σ |

Both are far outside draw noise, they replicate within task, and they point in **opposite
directions**. The conclusion is not "M5 is noise"; it is stronger and less comfortable:

> **The r_adj-optimal weight of the message component relative to the outcome profile is a
> property of the individual study, it is large enough to matter, and I cannot predict it
> from the brief.** A single regime constant for `lam_btw` is therefore not a mechanism —
> it is a coin flip with a real stake on each side.

**I am not declaring M5 for the gate.** My own evidence rejects it before the gate sees it,
and spending a gate slot on a mechanism I expect to fail is not what the gate is for. This
is the second time this arm has found that a *differential* re-weighting between the two
levels does not transfer (the first was M3, §8.1). The pattern is now a standing rule
(**R18**): **carry one uniform shrink and one uniform amplitude; do not ship any mechanism
whose content is a re-weighting between the outcome level and the message level.**

Why the two studies differ, as a hypothesis for a later session (not adopted, not fitted):
beall2017's predicted outcome profile is enormous and near-deterministic (`sd_btw` 5.7 pp,
manipulation-check items running to ±11 pp) — there is a great deal of skill there and
anything taken away from it costs. goldwert2026's profile is flat and small (`sd_btw` 1.06
pp, all twelve outcomes between 0.7 and 3.2 pp) — less skill there, so the message
component is relatively worth more. **Open item A13.**

### 9.3 What *is* supported about amplitude

Separately from the mix, every many-variant measurement of `cal_beta` at full amplitude has
come back **below 1**: 0.2985 and 0.3176 (kappa = 1), 0.4022 and 0.5612 (promoted kappa =
0.20). Their geometric mean, 0.475, was applied as `lam_all` in s4 sub-2 and beta landed at
**0.813 (beall) and 1.668 (goldwert)** — straddling 1 with no residual systematic bias.
So:

* a **uniform** amplitude correction of ≈ 0.5 in the many-variant regime is supported by
  four prior measurements and confirmed (as unbiased, not overshooting) by two fresh ones;
* it is **invisible to r_adj by construction** and therefore cannot be gated on the
  currency — it is an RMSE/calibration instrument only (R15, unchanged);
* the residual per-study scatter in beta (0.81 vs 1.67) is *not* reducible by anything I
  have; do not chase it.

One error to record: s4's `lam_all` was applied about **zero**, so it scaled the study grand
mean down as well as the spread. On tasks whose `mean_signed_error_pp` is already negative
that makes the level worse, and it is not what "an amplitude correction" should mean.
**R19: amplitude corrections are applied to deviations about the study grand mean `g`, never
about zero.** Fitting `g` itself to feedback stays forbidden (R4); the fix is a change of
centre, not a fitted level.

### 9.4 Where the target entry was inconsistent with its own promoted method

Applying §9.1's decomposition to the v1 target table exposed the largest open problem in
the entry, and it was invisible until the mix became measurable:

| table | `sd_btw` | `sd_wth` | **mix** |
|---|---|---|---|
| beall2017, as submitted and promoted | 5.712 | 0.867 | 0.152 |
| goldwert2026, as submitted and promoted | 1.056 | 0.165 | 0.156 |
| tested one step out (M5) | — | — | 0.30 |
| **target entry v1** | 0.233 | 0.234 | **1.002** |

The target entry was betting **half its variance** on the message level, at 6.6× the mix
that was promoted and 3× the largest mix ever tested. The cause is `ASSERTION_MATCH`: four
additive post-shrink cells (2.5 / 1.8 / 0.9 / 0.6 pp) that are ~4× larger than the entire
rest of the message component. R13 permits an additive term — it does not license one that
takes over the table. **R20: the target entry's mix must sit inside the range this
environment has actually validated for its regime.** v2 carries the message component
(including `A`) at the mix that the *closest structural analogue* preferred.

### 9.5 The promoted / rejected / open ledger — the standing method

**PROMOTED (use them; a fresh session should start here).**

| # | mechanism | evidence |
|---|---|---|
| P1 | **Analysis-first, three-level decomposition** `g + (m(o)−g) + (ate−m(o))`, every prediction built and reported at the level the benchmark scores. | the frame everything else is measured in |
| P2 | **M1w-v2 — one study-uniform `kappa = 0.20` on the message level in the many-variant regime (≥ 6 arms that are variants of one persuasive goal); `kappa = 1` in the distinct-intervention regime; no per-cell exemptions.** | gate PROMOTED (`gate_m1w-v2-k02.json`); beall +0.046 r_adj and goldwert +0.085 over baseline, both ≫ the 0.002–0.005 draw noise of §9.1 |
| P3 | **R12/R13** — a shrink constant is a study-level scalar; content confidence goes in the raw prediction or a bounded additive term, never a kappa override. | carried by the same verdict; the mechanism P2 *is* R12/R13 |
| P4 | **Moderator abstention** — an exact-zero floor for subgroup interactions unless a gate-grade test says otherwise. | the one technique in this project's history that transferred blind; operator-endorsed this session; ANCHORS_F's own placebo calibration cannot reject zero in the design twin |
| P5 | **`cal_beta` is a measurement of amplitude error, not a number to chase** (R15). | verified in both directions on fresh halves (§8.3), re-confirmed §9.3 |
| P6 | **Backward synthesis as a matched design** (R16): one quota-exact profile deck, centred moderator main effects, reflection not clipping, largest-remainder integer rounding, random-row cell repair, empirical response shapes, variance ratio 1.00. | 40 pass / 4 warn / 0 fail on the organizers' own validator; max ATE recovery error 0.025 pp |

**REJECTED, with diagnosis (do not re-propose without new evidence).**

| # | mechanism | diagnosis |
|---|---|---|
| X1 | **M3 — per-cell / per-outcome kappa exemption for assertion-match cells.** | gate REJECTED, family "scientist credibility (framings)". It was not a cell exemption but an outcome-amplitude reweighting: `research_controversial` went 36% → 69% of within-outcome variance while `credibility_*` fell 8.6% → 4.1%. And it could never have helped: a kappa uniform *within* an outcome is provably invisible to `r_within` (§8.1). |
| X2 | **M5 — `lam_btw` as a regime constant (outcome-profile amplitude ≠ message amplitude).** | rejected on own evidence before the gate, §9.2: the effect is 17–28 σ and *opposite in sign* on the only two tasks that can measure it. Not a mechanism; a study-specific parameter I cannot predict. |
| X3 | **Anything whose content is a re-weighting between the two levels** (the generalisation of X1 and X2). | R18. Two independent failures, two different implementations, one shared shape. |
| X4 | **Chaining the one-step propagation discount twice** (ANCHORS_B's original rule). | ANCHORS_E measured the decay and it *flattens* after the first step; retired in s3. |
| X5 | **Prompt-lever tinkering; per-study frozen effect tables; post-hoc rank-shifting.** | inherited from SCAFFOLD as pre-registered dead ends; nothing this arm has seen contradicts that, and this arm has never used a simulator at all. |

**OPEN (stated, not adopted).**

| # | question | status |
|---|---|---|
| O1 | What predicts a study's r_adj-optimal mix? (§9.2 hypothesis: the differentiation of the predicted outcome profile.) | **A13**; n = 2; do not fit |
| O2 | ANCHORS_F's ATE-scaled party-moderation rule. | pre-registered, hook present and unused, operator-endorsed to stay off (A11) |
| O3 | The target's `ASSERTION_MATCH` magnitudes. | the entry's largest untested bet (§9.4); bounded in v2 by R20, not resolved |
| O4 | The rank-1 arm score `s(a)`. | the weakest-evidenced object in the entry; ANCHORS_H addresses it |
| O5 | Control levels for `donation_ams`, `newsletter_signup`, and the A9 primary-level disagreement. | ANCHORS_I addresses them |
| O6 | Residual interaction error in the smallest synthetic cells. | **A10**; understood, bounded, judged not worth the ATE cost of fixing |

### 9.6 New standing rules

R17. **Read a diagnostic against its own measured draw noise, not a flat threshold.**
    sd(r_adj) across fresh halves is ≈ 0.002 at 204 cells, 0.005 at 96, 0.014–0.082 at
    10–25. R3's flat cut is replaced by: a task may support a mechanism claim only if the
    effect exceeds ~3× the sd measured for that task in §9.1.
R18. **Do not ship any mechanism whose content is a re-weighting between the outcome level
    and the message level.** Carry one uniform shrink (`kappa`, by regime) and one uniform
    amplitude (`lam_all`, about `g`). Two independent gate-or-own-evidence failures.
R19. **Amplitude corrections are applied to deviations about the study grand mean `g`,
    never about zero.**
R20. **An entry's mix (`sd_wth/sd_btw`) must sit inside the range validated for its
    regime.** Additive content terms are bounded by this, not exempt from it.
R21. **A pair of submissions differing only by a whole-table rescale is a free replication**
    (r_adj is exactly scale-invariant). Spend a second call this way whenever the primary
    question is about mix or shape rather than amplitude — it buys the noise scale for free.


---

## 10. The assertion-match measurement (session s5): the message level has a direction, and it is content targeting

### 10.1 The instrument was mis-calibrated, and the correction changes how s4 reads

`r_adj` is a Pearson correlation, so it is invariant under any positive **affine** transform
of the whole table (`p -> c*p + d`, `c > 0`) — not merely under a rescale. Damping toward the
**study grand mean** is affine (`G + k(p-G) = k*p + (1-k)G`), so those submissions are
replications too. Grouping all scored submissions into affine-equivalence classes by
`corr(p_i, p_j) > 0.999999` and pooling the within-class variance:

| task | dof | **sd(r_adj)** | s4's figure | sd of a difference | 3σ |
|---|---|---|---|---|---|
| beall2017 | 2 | **0.0116** | 0.005 | 0.016 | 0.049 |
| dablander2025 | 6 | **0.0135** | 0.014 | 0.019 | 0.057 |
| goldwert2026 | 3 | **0.0677** | 0.002 | 0.096 | 0.287 |
| kim2024 | 6 | **0.0817** | 0.082 | 0.116 | 0.347 |

s4 pooled only the *promoted-mix* class on beall and goldwert — one pair each — and missed
the second class, which differs by 0.022 and **0.091**. On goldwert the honest figure is 34x
larger than the one s4 used, and this run added a third member to that class (0.1861 against
0.3047 / 0.3074 for the identical table).

**Consequences, stated before this run's own reads (`PREREG_AM.md` §4):**

* §9.2's mix result is **not** 17σ / 28σ. beall −0.086 is **5.3σ** and goldwert +0.054 is
  **0.8σ**. The correct statement is "raising the message/outcome mix hurt on the one task
  that can measure it, and was a wash on the other" — one significant negative and one null,
  **not** an opposite-signed pair. The *decision* is unchanged (`LAM_BTW = 1.00` is the
  low-mix setting beall favours), but X2's evidence is weaker than s4 claimed and A13's
  premise — "the effect is opposite in sign between tasks" — is retracted.
* **R17 restated**: read every diagnostic against the σ above, and estimate σ from *every*
  affine class a task has, not from the most convenient one.

### 10.2 AM-ISO: the design

The entry's largest untested bet was `A_MULT`, the multiplier on the four assertion-match
cells, set in s4 by a consistency argument. The evidence behind it was a *between-study*
contrast (kim2024's `r_within_adj` 0.784 against beall's 0.092 and goldwert's 0.112), which
confounds assertion match with everything else that differs between those studies. AM-ISO
moves the contrast **inside** each study.

Fix a task's outcome profile `P(o)` and its message-level residual `R`, and split the cells
into **M** (content-targeted: the arm's own stimulus states, elicits or enacts the specific
quantity the item asks about) and **N** (generic: the prediction rests on a message-quality
ordering). Submit

* `TARGETED = P + (w/||R_M||) R_M` and `GENERIC = P + (w/||R_N||) R_N`, with
  `w = kappa*||R||` the promoted message norm.

Both carry the identical outcome profile, the identical total message norm, the identical
total variance and the identical mix; `M` is a union of whole outcomes, so both residuals
stay exactly within-outcome centred and `cov(P,q) = 0`. **They differ only in where inside
the message level the bet is placed** — a within-level question that R18 does not touch, and
that nothing in this arm had tested. The reading rule, the cell sets, the σ, the decision
rule for `A_MULT` and the prediction ("Δ > 0 on both deciding tasks") were all fixed in
`runs/20260828T060726Z_s5/val/PREREG_AM.md` before the first file was written.

### 10.3 The result: 4 of 4, and the two deciding tasks at 12.6σ and 21.5σ

| task | TARGETED | GENERIC | **Δ** | σ_Δ | **n σ** | status |
|---|---|---|---|---|---|---|
| beall2017 | 0.5451 | 0.3398 | **+0.2053** | 0.016 | **+12.6** | deciding |
| dablander2025 | 0.9881 | 0.5797 | **+0.4083** | 0.019 | **+21.5** | deciding |
| goldwert2026 | 0.4020 | 0.1861 | **+0.2159** | 0.096 | +2.3 | declared low power |
| kim2024 | 0.8732 | 0.6621 | **+0.2111** | 0.116 | +1.8 | declared low power |

Unanimous in sign; both deciding tasks pass 3σ with room. This is the first mechanism in
this arm that did **not** flip sign between tasks.

Three readings matter more than the headline.

1. **goldwert2026 is the one that speaks to the target.** There `GENERIC` was the promoted
   table *itself* (my standing 17-arm rank-1 arm-quality ordering) and `TARGETED` was a
   26-cell content-targeting map I authored from the brief that morning, carrying no
   information from my standing model at all. The authored map beat the standing model by
   **+0.216** at matched amplitude, and beat it by +0.097 against its own historical mean.
   goldwert is a 17-arm megastudy — the target's structural twin.
2. **My own authoring already does this on few-arm studies and does not on many-arm ones.**
   `alpha = ||R_M||/||R||` was 0.84 (beall), 0.99 (dablander), 0.99 (kim) — on those studies
   I had put nearly the whole message bet on the content-targeted cells by instinct. On
   goldwert, `alpha = 0`. The habit that produced the target entry is the many-arm habit:
   reach for a rank-1 arm-quality ordering. That is the habit this measurement indicts.
3. **A quantitative allocation, on the one task where it is well conditioned.** With
   `r_adj(TARGETED) = K + X`, `r_adj(GENERIC) = K + Y` and the historical promoted-table
   `r_adj = K + alpha X + beta Y`, the r_adj-optimal allocation is `s_M/s_N = X/Y`. On
   beall2017 (`alpha, beta = 0.844, 0.537`; `1-alpha-beta = -0.381`, so the noise
   amplification is a tolerable 2.6x): **X = +0.274, Y = +0.068, X/Y = 4.0 (1σ band
   2.9–6.6)** against an allocation of 1.57 actually used. My authoring is **generic-heavy
   by 2.55x, band 1.85–4.20**, and the band excludes 1.57, which was the pre-registered
   condition for reading `X/Y` as a multiplier at all. dablander returns `Y = -0.014 ± huge`
   — the generic class delivers nothing there — and kim's decomposition returns `K > 1`,
   i.e. it is out of the model's range at its own σ; both were declared low-power in advance.

**Caveat that belongs next to the headline.** On dablander and kim `alpha ≈ 0.99`, so
`GENERIC` there is a 9x amplification of a component I never seriously authored; part of
those two Δ's is "the class I thought about vs the class I did not". beall (`alpha/beta`
1.57, both classes substantively authored) and goldwert (GENERIC = the promoted table
itself) are the two clean reads, and they agree: +0.205 and +0.216.

### 10.4 What changed in the entry, and what did not

`A_MULT` is not raised as an amplitude. The **total message-level norm is identical in v2 and
v3 (1.5885 pp)**; `KAPPA` is untouched at the promoted 0.20; `LAM_BTW` stays 1.00. What
changes is the message level's **direction**: the targeted:generic norm ratio moves from
1.315 to **2.431**, the v2 ratio multiplied by the *lower* end of beall's measured correction
(1.85, not the centre 2.55 and not the upper 4.20). Implementation: `A_MULT` 0.40 -> 0.4647
and a new `S_MULT = 0.6289` on the rank-1 term, chosen jointly so the total norm is exactly
preserved. This is not a per-cell kappa override (R12/R13): both terms are message level,
the split is a direction rather than an amplitude, and R20's mix bound is not touched by it.

### 10.5 The two children: A13 answered negatively, A14 answered against the entry

**ANCHORS_J (A13 — what predicts a study's mix).** 16 train studies, arm x outcome tables
noise-corrected three independent ways (analytic MVN with the shared-control covariance,
cross-fitted split halves, ANCOVA where a pre-measure exists; (a) and (b) agree to 2–3
decimals). Noise is a median 25% of the raw within-variance and 18% of the raw between, so
**every raw mix is biased up**. True mixes run 0.00 (veckalov, Maertens2020, gligoric2025) to
2.1 (vdL2017) and 10.6 (koetke S3); median 0.94, IQR 0.39–1.68. **The rule does not exist:**
`n_arms`, `n_outcomes`, `n/arm`, outcome breadth, scale-type mixing, behavioural outcomes,
one-construct and assertion-match are all **worse out of sample than the pooled-mean
baseline** (LOSO log-mix error 1.275). One feature helps (`arm_contrast_kind`: arms differing
in kind vs framing variants of one goal, LOSO 1.104, permutation p = 0.015) and its own
author flags that it was coded after seeing the answers and buys nothing on the bounded
scale. Two studies from the same lab with the same outcome set land at 0.14 and 2.13. **A13
is closed as unanswerable on this train split**, and the honest fallback is the pooled
prior, not a fitted rule. Its target read: true mix 1.2 [0.45, 2.6], but the *submitted*
mix should be `true mix x (rho_within/rho_outcome)` ≈ **0.45 [0.2, 0.9]**, and the loss is
asymmetric — over-weighting the message level costs about twice what under-weighting costs.
v3 sits at **0.2125**, the low edge of that band and inside the validated [0.15, 0.30]. Two
instruments, one from the validation environment and one from the train split, both say the
low edge is the right side to err on; the disagreement about the centre is recorded, not
acted on.

**ANCHORS_K (A14 — `donation_ams`).** An independent read, told to form its own view before
seeing ANCHORS_I, and it **overturns the entry's cell**. It decomposed the design twin into
direct and indirect paths: holding post-treatment attitudes fixed, the direct effect on
giving is **−2.42 ± 0.91** (voelkel2026) and **−2.53 ± 0.63** (vlasceanu WEPT) — two
different asks, two datasets, the same number. The usable form is
`behavioural ATE ≈ −2.5 + 0.5 x (attitude ATE)`: a near-constant negative offset, **not** a
shrunken copy of the attitude effect. It **falsified** end-of-survey fatigue for this design
(arm-level `corr(ATE, reading time) = +0.08`; confirmed only for vlasceanu, whose arms differ
2 s to 350 s in effort, which the target does not), and it found in the target's own
SurveyFlow that donation and newsletter sit inside a `BlockRandomizer(7)` over the secondary
blocks — **mid-battery, not last** — which removes the depletion component ANCHORS_I had
implicitly leaned on. Its centre is **−0.7 pp (band −2.0 to +0.6)**, above voelkel2026's
−1.4 only because the recipient (AMS) is the message's own subject, and it is candid that
this rests on one confounded contrast (voelkel2024's dictator game, ratio 0.877, r = 0.832).
Decisive for the entry: expected directional credit is **0.62 for a negative, 0.50 for an
exact zero, 0.38 for a positive**, so v2's +0.05 was the *worst of the three* — it forfeited
the guaranteed half credit without buying the sign. It also measured the noise-corrected
between-arm SD of donation at **exactly 0.000**, so `L_OUT["donation_ams"]` goes to 0: the
whole effect is a common shift and no message-level variance is spent ordering those 16
cells. It corrected ANCHORS_I on one point (voelkel2024's `PA` is *by construction* the mean
of the dictator game and the thermometer, so their r = 0.951 is partly mechanical; the
defensible ratio is 0.877 on the independent half) and agreed with it on eleven others,
including the lottery.

### 10.6 New standing rules

R22. **Estimate a task's draw noise from every affine-equivalence class it has**, not from
    one. `r_adj` is invariant under `p -> c*p + d` for `c > 0`, so damping toward a study
    grand mean, whole-table rescaling and a pure shift are all replications. Using one class
    understated σ by 2x on beall2017 and 34x on goldwert2026.
R23. **[REWRITTEN in s6 - the original overstated what its evidence carries; see 11.2.]**
    *A message level with ZERO weight on content-targeted cells is much worse than one with
    most of its weight there; above roughly 0.7 of the message variance the curve is flat,
    and the targeted:generic ratio is not a lever.* The original form ("allocate the
    message-level budget to content-targeted cells before spending any on an arm ordering")
    was declared to the gate as M10, REJECTED, and does not survive its own data: beall2017's
    three matched-amplitude points saturate, the two confirming tasks had incumbents already
    at share 0.98, and the noise scale that made it "12.6 sigma" was 5.7x too small. What the
    evidence supports is the bounded claim above, at Stouffer 3.7 sigma over three tasks. See
    also ANCHORS_L: content targeting is a SUBSTITUTE for the rank-1 outcome loading, not a
    complement to it, so the loading is where this belongs.
R24. **A behavioural follow-through cell is a near-constant negative offset plus a small
    fraction of the attitude effect** (`≈ -2.5 + 0.5 x attitude`), not a shrunken copy of it,
    and its between-arm SD is zero. Predict the offset; do not order the arms on it.
R25. **When a predicted cell's sign is genuinely in doubt, an exact zero beats a small
    wrong-signed number and loses to a correct sign** (0.50 / 0.38 / 0.62 expected
    directional credit). A "small and faintly positive" hedge is the worst of the three
    and must never be chosen for being small.

### 10.7 The standing method after s5 (supersedes §9.5 where they differ)

**PROMOTED (unchanged):** P1 analysis-first three-level decomposition; **P2** M1w-v2, one
study-uniform `kappa = 0.20` on the message level in the many-variant regime, `kappa = 1`
otherwise, no per-cell exemptions; P3 R12/R13; P4 moderator abstention (exact-zero floor);
P5 `cal_beta` is a measurement, not a target; P6 backward synthesis as a matched design.

**DECLARED, awaiting a verdict:** **M10 / R23** — allocate the message level's *direction*
to content-targeted cells at unchanged total message norm
(`runs/20260828T060726Z_s5/GATE_CANDIDATE.json`). Its primary evidence (§10.3) does not
depend on the verdict.

**REJECTED (unchanged):** X1 M3 per-cell/per-outcome kappa exemption; X2 M5 `lam_btw` as a
regime constant — **with its evidence restated**: one significant negative (beall, 5.3σ) and
one null (goldwert, 0.8σ), not an opposite-signed pair (§10.1); X3 any between-level
re-weighting; X4 chained propagation discount; X5 prompt-lever tinkering / frozen per-study
tables / post-hoc rank-shifting.

**CLOSED since §9.5:** O1/A13 — **closed negatively**: no brief-visible design feature
predicts a study's mix out of sample (§10.5). O3 — the target's `ASSERTION_MATCH`
*magnitudes* are now bounded by measurement rather than by argument (§10.3–10.4); what
remains open is its **coverage** (OPEN A16). O5/A14 — closed against the entry (§10.5).

**STILL OPEN:** O2 ANCHORS_F's ATE-scaled party-moderation rule (pre-registered, hook unused,
operator-endorsed to stay off); O4 the rank-1 arm score `s(a)`, now carrying a smaller share
of the message level than it did in v2 and still unvalidatable on train; O6/A10 residual
interaction error in the smallest synthetic cells; **A16** targeting-map coverage; **A17**
σ has 2–3 dof where it matters; **A18** `S_MULT` sits next to a promoted constant.


---

## 11. A18 resolved, the instrument re-calibrated again, and what the entry reverted to (session s6)

Run `20260828T074119Z_s6`. Everything in §11.1–11.3 was written and decided **before** this
run's two scored calls were made and **before** either approved child reported; the
pre-registration is `runs/20260828T074119Z_s6/val/PREREG_S6.md`.

### 11.1 A18: the entry's direction change reverts, and the rule that decides it

The gate returned **REJECTED** on M10/R23 with failure family **"donation/behavioral
outcomes"** (`runs/20260828T060726Z_s5/gate_m10-targeting.json`).

**The textual argument, from the frozen definitions only.** *Refinement and memory* says
durable state has two homes, one of which is "the files you write in this directory
(`AGENTS.md`, skills, **tools**)". `tools/target_model.py` is in `tools`, so the entry
constants **are** durable state by the frozen file's own definition. *The validation
environment* says "Only techniques that help held-out studies on average, without hurting any
one study beyond noise, survive into your durable state." `A_MULT`/`S_MULT` at their v3
values had exactly one warrant — the AM-ISO measurement, declared to the gate as M10/R23 and
rejected. A constant whose sole warrant is a rejected technique cannot stay in `tools/`.

s5 §5 pre-registered an escape hatch: "a REJECTED should be read as *no net gain over an
already-targeted baseline*, not as a refutation of §2". **It does not apply**, for a reason
s5 could not have known: the verdict carried a *failure family*, which is the environment
saying the candidate **hurt** somewhere, and "without hurting any one study beyond noise" is
the second, independent clause of the promotion rule. Both clauses fail.

**R27 (new): gate governance follows the evidence base, not the file.** An entry constant
whose warrant is the *validation environment* is governed by the gate and reverts on a
REJECTED. An entry constant whose warrant is *train ground truth* is governed by the split
rule ("anything: read outcomes, fit anything, iterate without limit") and needs no gate.
Every other constant in `target_model.py` is of the second kind — ANCHORS_A–K, all train.
`A_MULT`/`S_MULT` at v3 were the only constants this entry has ever had of the first kind.
This is why `M_RAW["donation_ams"] = -0.70` and `L_OUT["donation_ams"] = 0.000` **stay**: they
are ANCHORS_K, train split, never submitted to any gate. Declaring the rule and then applying
it in both directions in the same paragraph is the point; an unexamined middle would be
keeping the first pair *because* the second pair stays.

### 11.2 The measurement did not survive its own evidence either

The revert is not only textual. Re-reading the s5 result before deciding:

**(a) The allocation curve saturates at or below where the entry already sat.** All three
beall2017 AM-ISO tables are matched-amplitude to five digits (within-outcome SS = 72.143 in
each), so the targeted **share** of message variance is the entire difference between them:

| targeted share | 0.000 | **0.712 (incumbent)** | 1.000 |
|---|---|---|---|
| r_adj | 0.3398 | **0.5352** | 0.5451 |

Slope below the incumbent +0.275 per unit share; **above it +0.034** — one eighth as steep,
with the whole remaining gain +0.0099. The entry's v2 → v3 move raised the assertion term's
share from 0.634 to 0.855 and was therefore worth about **+0.008 r_adj**. s5 derived its
"2.55× generic-heavy" correction from a *linear* decomposition `r = K + aX + bY` fitted to the
two endpoints; the three points falsify that linearity directly. **R28 (new): read a
matched-amplitude allocation curve for saturation before extrapolating it, and never price a
change against an allocation you would never ship.**

**(b) dablander2025 and kim2024 could never have borne on the question.** Their incumbent
tables already sat at targeted share **0.988** and **0.978**. Candidate-vs-baseline there
moves 1–2% of the message variance; +0.003 and +0.141 are not targeting effects.

**(c) R26 (new): bound a read by the correlation between the two tables first.** For tables
with corr = rho, the systematic part of any difference in r is at most about
`(1-rho)|r| + sqrt(1-rho^2)`. baseline vs candidate on kim2024: rho = 0.9969, bound on
Delta r_raw = 0.081, **observed 0.087** — at the ceiling of what a table difference that small
could produce, i.e. draw noise wearing a mechanism's clothes.

**(d) The noise scale was wrong by a factor of six on the deciding task.** Two scored calls
this run resubmitted the s3 promoted tables byte-identically (§11.3). beall2017 returned
**0.4006** where the same table had returned 0.5352 and 0.5429. Re-pooling every affine class
(R22):

| task | sd(r_adj) now | dof | s5 claimed | sd(r_within_adj) now |
|---|---|---|---|---|
| **beall2017** | **0.0659** | 3 | 0.0116 | 0.0852 |
| goldwert2026 | 0.0644 | 4 | 0.0677 | 0.0397 |
| dablander2025 | 0.0135 | 6 | 0.0135 | 0.0125 |
| kim2024 | 0.0817 | 6 | 0.0817 | 0.0580 |

Against the sd of a *difference* between two independently drawn halves (`sqrt(2)·sd`, which
s5 also omitted), the AM-ISO result reads:

| task | Delta | s5 said | now |
|---|---|---|---|
| beall2017 | +0.2053 | 12.6 sigma | **2.2 sigma** |
| dablander2025 | +0.4083 | 21.5 sigma | 21.4 sigma |
| goldwert2026 | +0.2159 | 2.3 sigma | 2.4 sigma |
| kim2024 | +0.2111 | 1.8 sigma | 1.8 sigma |

Only dablander clears R17's 3-sigma bar, and dablander is precisely the strawman comparison
of (b). Pooled over the three non-strawman tasks the effect is still real (Stouffer 3.7 sigma,
one-signed 4 of 4) — but what it supports is the bounded claim, not the ratio move.

**R23 is rewritten** to what its evidence carries: *a message level with **zero** weight on
content-targeted cells is much worse than one with most of its weight there; above roughly
0.7 of the message variance the curve is flat, and the targeted:generic ratio is not a lever.*
The entry has never been below 0.63.

**Two collateral corrections, both against my own earlier readings.**
* s4's mix probes are now **0.9 sigma (beall)** and 0.8 sigma (goldwert) — two nulls, having
  been read as 17/28 sigma in s4 and 5.3/0.8 sigma in s5. `LAM_BTW = 1.00` keeps its decision
  and loses this evidence: it stands because the s3 gate promoted the table carrying it.
* s6's own §1b(3) claim is half retracted. sd(r_within_adj|beall) = 0.0852, so beall's
  0.1498 → 0.1013 is 0.4 sigma and should not have been cited. goldwert is different: that
  table's own class runs 0.1098 / 0.0938 / 0.0683 / 0.1529 (mean 0.106, sd 0.0397) against the
  AM-ISO TARGETED value **0.0181 — 2.2 sigma below its own mean**. On the 17-arm task, the
  target's structural twin, the targeted allocation lost within-outcome ordering skill. One
  task at 2.2 sigma is a caution, not a result (**A20**).

### 11.3 The two scored calls, and why the other twelve were declined

Both calls were byte-identical resubmissions of the s3 promoted tables on beall2017 and
goldwert2026, declared in advance as **instrument calibration only**, with pre-registered
expectations (0.53 ± 0.02 and 0.30 ± 0.07) and an advance commitment that no number they
returned would change any constant. Both came back low (0.4006, 0.2046), each added a degree
of freedom, and together they produced §11.2(d) — the single most consequential number of the
session. After the revert the promoted table *is* the entry's method, so these are also a
fresh-half re-measurement of what the entry now does.

Twelve calls declined. Under R27 no validation-sourced measurement can move an entry constant
without a gate, and a gate needs a full-coverage candidate for a mechanism I do not have; the
one substantive question worth asking (where the saturation knee sits) is already answered by
the three points of §11.2(a) and the entry sits on the flat part either way. Buying a number I
have pre-committed not to act on is the failure mode of s4 and s5.

### 11.4 Entry v4

| # | change from v3 | evidence |
|---|---|---|
| 1 | `A_MULT` 0.4647 → **0.40**, `S_MULT` 0.6289 → **1.00** | §11.1 (text) and §11.2 (evidence). This is exactly the promoted state; the generic rank-1 ordering returns to full strength and the four assertion cells return to the v2 size. |
| 2 | nothing else | v3's two train-sourced changes (`donation_ams` −0.70, `L_OUT` 0.000) stay under R27; `KAPPA` 0.20, `LAM_BTW` 1.00, control levels, `S_ARM`, the outcome profile, the exact-zero moderation floor and the synthesis pipeline are untouched. |

Total message norm returns to v2's exactly (pooled within-outcome sd 0.1083 vs v3's 0.1098);
mix **0.2084**, inside the validated [0.15, 0.30] and at the low edge of ANCHORS_J's
train-split band. Pipeline: `--exact --n-control 6000 --n-intervention 3000`, 54,000 rows,
max ATE recovery error **0.0239 pp** (mean 0.0017), organizers' `make check`
**40 pass / 4 warn / 0 fail**, the same four operator-side deposit warnings. No deposit
actions taken.

### 11.5 New standing rules

R26. **Bound a mechanism read by the correlation between the two tables before reading it.**
    For tables with corr = rho the systematic part of any difference in r is at most about
    `(1-rho)|r| + sqrt(1-rho^2)`; a difference at that ceiling is draw noise.
R27. **Gate governance follows the evidence base, not the file.** Validation-sourced entry
    constants are gate-governed and revert on a REJECTED; train-sourced constants are
    governed by the split rule. Label every constant with which kind it is, in place.
R28. **Read an allocation curve for saturation before extrapolating it.** Two endpoints plus
    the incumbent are three points. A gain measured against an allocation you would never
    ship is not a gain over the one you do.
R29. **Buy degrees of freedom on the deciding task before, not after, making a sigma claim.**
    Two byte-identical resubmissions cost two calls and retracted a 12.6-sigma headline. Any
    task whose sd(r_adj) rests on fewer than 3 dof may not carry a mechanism claim.


### 11.6 The two children: A16 closed negatively, A14's residual closed positively

**ANCHORS_L (A16 — can a content-targeting map be *validated*?). NO, for a mechanically-coded
map, and the negative is the useful part.** Rule T-1 was written to disk with a sha256 and a
timestamp before any effect table existed. On the residual of *this campaign's own model*
(outcome profile + rank-1 arm term) across 4 text-vendored train studies (172 cells, 88 fired),
the targeting code adds nothing: beta = +0.066 pp (se 0.537), LOSO MSE **rises**, worse in 4
folds of 4, permutation p = 0.46 (cross-fitted rank-1: +0.208, p = 0.26, fold betas −0.19 to
+0.43 with a sign flip). Against an *arm-main-effect-only* baseline the same code is strongly
positive (+1.263 pp, permutation p = 0.001). **Content targeting is a substitute for the rank-1
outcome loading, not a complement to it** — which is also the cleanest reading of §11.2, since
AM-ISO's "targeted" sets were unions of whole outcomes and therefore moved the loading, not the
ordering. Its expert-coded secondary (voelkel2024's own two coders, 25 arms × 3 outcomes) shows
the *mechanism* is real — beta = −0.217 pp per code point, leave-one-arm-out ΔMSE = −0.061,
permutation p = 0.013, fold betas −0.15 to −0.25 — so what fails is the string rule, not the
idea. Behavioural sub-answer: the rule fires on **2 of 39** behavioural/donation train cells;
a text-derived targeting term cannot be the mechanism behind a donation/behavioural failure
family and no targeting bonus belongs on a behavioural cell. Coverage answer: the mechanical map
fires on 111/208 target cells but **reproduces the authored §6.6 map exactly at the strict tail**
— the authored 4-cell map is that tail, and the other ~107 cells are the part that fails LOSO.

**ANCHORS_M (A14's residual — recipient alignment). REAL, POSITIVE, LARGE, and it moves two
entry constants.** One identical specification on all five usable behavioural outcomes gives a
subject-aligned pole of +1.97 ± 0.32 against a cause-aligned pole of −2.32 ± 0.52: a swing of
**+4.29 ± 0.61 pp (7.1 sigma)**. Exactly one clean within-study contrast exists and it does not
span the subject/non-subject boundary, so the decisive step is between studies — disclosed by
its author, and kept as **A21**. It also corrects two arithmetic slips in ANCHORS_K's −0.70
that cancelled, and overturns v3's exact-zero between-arm SD **on the inference**: voelkel2026's
tau_hat = 0 has a 95% upper limit of 1.485 while the same study returns tau = 0.192 for an
attitude composite whose arms demonstrably differ, so the zero is a floor artefact of an
underpowered heterogeneity design. The informative estimate is voelkel2024's 25 arms:
tau(behaviour)/tau(attitude) = **0.883**, arm-level r = +0.829.

### 11.7 Where the two instruments disagree, and the reconciliation v4 rests on

ANCHORS_L recommends capping a targeted term at **0.12 × the generic rank-1 norm** (band
0.00–0.20). v4 sits at **1.185**. v4 does not move, and the reason is arithmetic rather than
procedural:

* the cap is a **ratio to a term the entry deliberately shrinks and train does not**. Train
  message-level arm SD is 0.47–1.97 pp; the entry's is ~0.13 pp because `KAPPA = 0.20` shrinks
  an *ordering* with almost no measured skill. R13 exists precisely to keep a design-level
  content claim out of that kappa.
* in **absolute pp — the unit the scorer reads — the two instruments agree**: ANCHORS_L's own
  expert-coded full reference is worth **0.74 pp**; v4's two full assertion cells are 1.00 and
  0.72 pp (mean 0.86). Its half:full band is 0.24–0.65 (recommendation: toward 0.3); v4's half
  cells are already at 0.42 and 0.28 of a full cell.

This reconciliation is recorded as **A22**, not as a settled fact. It is the largest single
number in the entry that rests on an argument rather than on a measurement.

## 12. A22 closed by measurement, and the entry's last argued number becomes a measured one (session s7)

Run `20260828T083214Z_s7`. One approved child (`anchors-assert` -> `anchors/ANCHORS_N.md`), zero
scored validation calls, zero model calls. Pre-registration:
`runs/20260828T083214Z_s7/val/PREREG_S7.md`, written before the child was launched.

### 12.1 The question, and the taxonomy that turned out to be the transferable part

Three of the sixteen target arms are **elicit-and-correct**: the respondent is asked for an
estimate and the next screen corrects it with a specific number (Funding: agreement with three
funding claims, corrected with $10.6bn vs $52.5bn and $7bn vs $160bn; Consensus: three "% of
scientists who agree" sliders with per-item feedback 99% / ~100% / 66%; High public trust: "% of
Americans who trust climate scientists", corrected with Pew's 76%). §6.6 authored an additive
per-cell term for exactly the cells where a corrected claim is later scored, and A22 recorded
that its size was the largest number in the entry resting on an argument.

The pre-registration's first move was to classify the *item*, not the arm:

| class | the scored item asks | target cells |
|---|---|---|
| **C1** | for the corrected quantity itself | **none** |
| **C2** | the respondent's own belief in the claim the number was evidence for | Funding × `funding_perceptions`, Consensus × `belief_post` |
| **C2n** | the respondent's own attitude, where the corrected quantity was a **social norm** | High public trust × `trust_post`, × `trust_multidimensional` |
| **C3** | anything else the arm touches | — |

This matters because of what the measurement then found: **C1 +9.37 pp, C2 +1.30 pp, C3 zero by
construction.** Almost the entire effect of a numeric correction lands on an item this benchmark
does not score. A term sized on the wrong class would have been seven times too large.

### 12.2 The measurement (ANCHORS_N, train split, 6 studies)

Estimands fixed in advance, all in pp of scale range: `E_abs` (ATE vs control, a bound only),
`E_arm` (correcting arm minus the study's other message arms on the same item), and **`E_out`**
(the arm's effect on the corrected item minus its own effect on that study's non-corrected
outcomes) — the last being the one that isolates a single-cell additive bump in a two-arm study.

| class | E_abs | **E_out** | E_arm |
|---|---|---|---|
| C1 | +10.52 | **+9.37** (dof 5) | +6.02 (dof 1) |
| **C2** | +2.45 | **+1.30, se 0.23, dof 5, CI [+0.71, +1.90]** | +1.02 (se 0.44, dof 1) |
| C2n | +0.90 | +0.61 (k = 1) | +0.09 (se 0.54, dof 1) |

Per study (C2, `E_out`): Maertens2020 +2.08, vdL2017 +1.34, vdL2019-US +1.32, Većkalov2024 +0.78,
vlasceanu2024 +1.00, voelkel2026 +1.28. LOSO +1.15 to +1.41: no study drives it. US-only
subsamples of the two multi-country studies are *larger* (+1.85, +1.12), so the pool is
conservative for a US target. **Elicitation carries no premium** (+0.24 ± 0.30 pp, confounded
with estimator), and the single train arm with the target's exact elicit-then-personal-feedback
mechanic (vlasceanu's PluralIgnorance) is the *lowest* number in the table.

I verified the pipeline myself on `geiger2026`'s vdL 2019 US RCT: ANCOVA on the pre-measure,
n = 6,301, consensus +16.4197 raw, belief +0.14248 raw = +2.375 pp, cause +3.272 pp, worry
+1.680, policy +1.329, so E_out = +0.870 / +1.768 and the study mean is +1.32 — matching
`assertion_train.csv` to four decimals, scale conversion included (PREREG_S7 §R6).

### 12.3 The rule, and the fact that it fired in the direction I did not expect

PREREG_S7 §2 fixed a **two-sided posterior update** before the child reported: authored prior
N(0.86, 0.40²) pp (the entry's two full cells are 1.00 and 0.72), measurement N(Ê, se²),
`A_MULT_new = clip(round(0.40 × P/0.86, 2), 0.05, 0.55)`, with a dead band of ±0.05 and the cap
taken from R20's validated mix range. With Ê = 1.30, se = 0.23: **P = 1.191 pp,
A_MULT = 0.554 -> 0.55, and the rule fires.**

s6's declaration named only the downward contingency ("if it comes back near 0.2 pp"). It came
back at 1.30. The rule was symmetric because it was written before the answer, and applying it
unchanged when it moves against the session's expectation is the only thing that makes the
earlier revert (§11.1) a rule rather than a preference.

Sensitivity, reported but not decisive: se inflated by √2 for the child's own "three design
families, not six independent replications" gives 0.52; LOSO extremes give 0.50 / 0.55; the CI
limits give 0.35 / 0.55; **the between-arm corroborator `E_arm` (dof 1) would give 0.43, inside
the dead band.** So the update rests on `E_out`, and a reader who prefers `E_arm` should read the
entry as v4-with-noise. R29 disqualifies `E_arm` as a headline at dof 1; that is why it is a
corroborator here and not the estimate.

**New standing rules.**

* **R30 — size a content term on the class of item the benchmark actually scores.** The C1 -> C2
  gradient is a factor of seven within the same manipulation. Before sizing any design term, ask
  which class the scored items belong to; a term measured on the wrong class is not conservative,
  it is wrong by a factor.
* **R31 — an entry constant is updated by a pre-registered, two-sided posterior with an explicit
  prior and an explicit dead band, or not at all.** Written before the measurement, it decides
  both directions; written after, it is a preference dressed as arithmetic. R31 is what made
  §11.1's revert and §12.3's increase the same operation.

### 12.4 Entry v5

| # | change from v4 | evidence | kind (R27) |
|---|---|---|---|
| 1 | `A_MULT` 0.40 -> **0.55** | ANCHORS_N (§12.2) via PREREG_S7 rule A22-1 | **train-sourced**, under a validation-sourced band |
| 2 | nothing else | `KAPPA` 0.20, `S_MULT` 1.00, `LAM_BTW` 1.00, the `ASSERTION_MATCH` shape, control levels, `S_ARM`, outcome profile, `donation_ams` −0.40 / `L_OUT` 0.997, exact-zero moderation, synthesis | |

Why 0.40 was not gate-governed and 0.55 does not need a gate: v4's value was **authored** (the
smallest multiplier keeping the assertion cell the Funding arm's own largest) subject to R20's
mix band. R27 puts governance with the evidence base — the new value's evidence is train ground
truth, and the validation-sourced part of the old warrant (the band) is still respected, with the
model-side mix moving 0.238 -> **0.293** inside the validated [0.15, 0.30] (the band binds at
A_MULT ≈ 0.565). The band is what capped the move: the uncapped posterior wanted 0.554.

The v5 table (mean ATE over 16 arms, pp of scale range, recomputed from the 54,000 deposited
rows):

| outcome | control | mean ATE | across-arm SD |
|---|---|---|---|
| trust_post | 66.0 | +1.081 | 0.146 |
| trust_multidimensional (primary) | 64.9 | +1.015 | 0.122 |
| newsletter_signup | 11.5% | +0.446 | 0.060 |
| funding_perceptions | 64.0 | +0.386 | 0.332 |
| belief_post | 68.0 | +0.342 | 0.245 |
| policy_role_mean | 67.0 | +0.300 | 0.039 |
| inst_trust_mean | 56.0 | +0.280 | 0.037 |
| concern_mean | 58.0 | +0.220 | 0.029 |
| policy_general | 66.0 | +0.200 | 0.026 |
| behavior_mean | 40.0 | +0.180 | 0.024 |
| policy_specific_mean | 61.0 | +0.170 | 0.022 |
| donation_ams | $4.40 | −0.400 | 0.116 |
| distrust_post | 32.0 | −0.750 | 0.098 |

Largest cells: **Funding × funding_perceptions +1.664**, High public trust × trust_post +1.349,
Consensus × belief_post +1.281, Interview Prof. Maraun × trust_post +1.279, Peer-review ×
trust_post +1.211. All 16 `donation_ams` cells stay negative (−0.21 to −0.61), so R25's 0.62
directional credit is intact. Pipeline `--exact --n-control 6000 --n-intervention 3000`: 54,000
rows, max ATE recovery error **0.0239 pp** (mean 0.0017), max native interaction 4.215,
organizers' `make check` **40 pass / 4 warn / 0 fail** (the same four operator-side deposit
warnings). No deposit actions taken; `target_entry_v5_pkg/` is a local validation copy.

### 12.5 What the measurement does not support, kept visible

1. **No funding-correction arm exists anywhere in the train split.** The Funding cell — now the
   entry's largest at +1.66 pp — inherits only the generic C2 pool. Nothing was measured about a
   dollar-amount correction, or about `funding_perceptions` specifically.
2. **The social-norm cells were raised by a measurement that does not support them.** C2n is
   +0.61 pp on one study and +0.09 ± 0.54 on the between-arm contrast; the rule moves the
   multiplier and not the shape, so `High public trust × trust_post` went 0.36 -> 0.495 pp inside
   the term and the cell to +1.349. This is **A24**, recorded rather than patched, because
   re-authoring the shape after seeing the number is exactly what R31 exists to prevent.
3. **The pool is four consensus experiments from two research lineages plus two megastudies** —
   three design families, not six replications.
4. **`E_out` and the base effect are not cleanly separable.** If the entry's base for these arms
   is itself an average over consensus-type arms, part of the bump is double-counted.
5. **It is not a trust result.** The one trust outcome measured under a correcting arm
   (Većkalov's `scientist_trust`, class C3) moves −0.05 / +0.71 pp — i.e. like policy support.
   The target's outcome family is trust; this measurement is dominated by belief items.

### 12.6 The standing method after s7 (supersedes §11 where they differ)

Unchanged: P1-P5, the three-level decomposition, `KAPPA = 0.20` in the many-variant regime,
`LAM_BTW = 1.00`, the exact-zero moderation floor, backward synthesis with `--exact`, R26-R29.
Added: **R30** (class-match a content term to the scored items) and **R31** (two-sided
pre-registered posterior updates with an explicit prior and dead band).

What is *not* true after s7, and I will not let the sentence run away: the entry contains no
**amplitude scalar** whose warrant is an argument — `KAPPA` and `LAM_BTW` are gate-promoted,
`A_MULT` is now train-measured, and every level and profile comes from an anchor. What remains
authored is the **shape** inside `ASSERTION_MATCH` (2.5 / 1.8 / 0.9 / 0.6 — A24), the
moderator main-effect deltas that Section 1 never reads, and the `CLIM_WEIGHT` grading. Each
carries its evidence and its kind in place; none of them is a measured number pretending to be
one.
