# OPEN.md — idea_03

Running document. Items are closed in place with the evidence that closed them, so an
operator can audit the trail. Last updated: session **s3**, run `20260827T205641Z_s3`.

---

## A. Environment items

**A1. `/workspace/benchmark` empty — CLOSED (s2).** It is mounted: `README.md`, `FAQ.md`,
`codebook.csv` (63 rows), `metadata.json`, `registration.md`, `Makefile`,
`scripts/{check,clean,manifest,zenodo_citation}.R` + `scripts/lib/{submission_spec,
clean_lib,check_lib}.R`, `survey/{survey.qsf, survey.json, questionnaire.txt,
condition_codenames.csv}`, `predictions/example_T{1,2,3}*.csv`,
`raw_data_deposit/example_raw_export.csv`. Fully inventoried in s2b; see `DESIGN.md` §6.

**A2. Brief said 5 submissions — CLOSED (s2).** All seven `task.json` now state 2 per task
per run id, matching the frozen file and `score_<k>.json`.

**A3. kerwer2025 fixed draw — CLOSED (s2)**, confirmed by the operator as a
per-submission hash collision, now structurally prevented (halves drawn without
replacement within a run id x task).

**A4. Undefined correlations returned as extreme finite numbers — CLOSED (s2).** The
scorer now returns `null` for `r_adj` / `r_within_adj` at reliability <= 0.001 and clamps
to [-1, 1] otherwise. Observed working: `orchinik2024` and `altenmueller2024` sub-2 both
returned `null` this run instead of -944 / -16816.

### New in s2b

**A5. A deposit needs a `team_id` that only the operator can supply.**
`check_lib.R` requires `metadata.json.team_id` to be the ID assigned by the organizers by
email ("`team_N`, in the team status update of August 15, 2026"); it FAILs the filename and
SHA-256 checks otherwise, and the FAQ says a wrong ID "passes `make check` but breaks the
link to your registration". It is not derivable from anything in the repo. **The operator
must provide `team_id` (and `team_name`, `contact`, `creators`) before any deposit.** The
prediction pipeline is unblocked without it; only the packaging step is blocked.

**A6. Section-2/3/4 companions are accepted but return no diagnostics.** Each `task.json`
says "Optional files score the other sections; *the scorer returns task-level metrics
only*", and that is what happens: all 14 `score_<k>.json` from s2 carry only the Section-1
diagnostic block, including the 6 tasks for which 24 moderator companions were submitted.
So the moderation-reliability read that `OPEN.md` §E (s1) asked for **cannot be obtained
from this environment's feedback**. Not a defect — but the operator should know that the
plan "submit honest-floor companions to learn the moderation reliability" is unachievable
as stated, and I have stopped counting on it. *Question:* are the companion files scored
internally (for the promotion gate or the sealed internal test), or ignored entirely? If
ignored, they cost me nothing but they should stop being described as buying information.

**A7. Section numbering differs between the validation environment and the organizers.**
`task.json` calls the moderator companions "Section 3" and the synthetic rows "Section 4";
the organizers' qmd calls subgroup moderation **Section 2** and response distributions
**Section 3**. Mapping used throughout my notes: val `_mod_*` = organizers' Section 2;
val `_rows` = organizers' Section 3. Worth aligning so a future session does not mis-file.

**A8. A human half can recur across run ids (observation, not a complaint).**
Within a run, identical files get different halves, as promised. Across runs they can
collide: `dablander2025` s2/submission_1 is byte-identical to s1/submission_2 and returned
*identical diagnostics to 4 dp* (r_adj 0.9932, r_within 0.9676, RMSE_adj 3.7032,
reliability 0.9070, signed error 3.0205); `kim2024` s2/submission_2 likewise reproduced
s1/submission_2 exactly. Consequence for the gate: a candidate run that resubmits a
byte-identical file is **not** guaranteed an independent draw against the baseline run, so
identical-file tasks contribute no information rather than a replication. I have flagged
which candidate tasks are byte-identical (see `REPORT.md` §3) so the gate can be read
correctly.

---

## B. SCAFFOLD contradiction — CLOSED (s2)

The operator's answer: the two rows are human-on-predicted regressions from *different*
predictors on *different* study families (idea_01's analytic predictor on slider
megastudies; idea_02's pipeline measured once, blind, on a held-out two-experiment study).
No same-regression contradiction and no universal kappa. `beta = rho * sd_true/sd_pred`
stands; SCAFFOLD's row is history, not a default, and was not adopted.

---

## C. Blinding disclosures

* **No retrieval of any kind, in any session of this arm.** No web search, no remote
  repository, no literature fetch, no package installs. (s2b installed nothing; the one
  package event was a child re-importing `openpyxl`, already present in the venv.)
* **Validation outcomes never read.** `inputs/val/<task>/brief/` holds `task.json` and
  empty-`ate` templates only; nothing else under `inputs/val/` was opened.
* **Target outcomes do not exist here and were not sought.** `/workspace/benchmark`
  contains the instrument, texts, codebook and validator, plus a shipped `example_*`
  prediction set that the README states is random placeholder data with no real effects.
  I used the examples for *format* only. No pilot, preprint, or talk about the target was
  read, and none is present in this container.
* **Recognition disclosure (carried forward and extended).** I recognise several validation
  studies by design description, and I recognise the *published literatures* several target
  stimulus texts are drawn from (consensus messaging, gateway belief, the fossil-fuel
  misinformation history, model-accuracy retrospectives). Every predicted number remains
  derived from the structural model in `DESIGN.md` §2/§6 anchored on `/workspace/datasets`
  tables computed in this arm (`anchors/*.csv`), never from a remembered result. Where a
  remembered qualitative regularity coincides with a train-split measurement I used the
  measured train-split number.
* **Four `rlm()` children across the arm** (`anchors-megastudies`, `anchors-trust` in s1;
  `anchors-rank`, `anchors-levels` in s2b), all scoped to `/workspace/datasets`, all
  explicitly forbidden `inputs/val/**`, `runs/**` and the web. They produced train-split
  tables only, never predictions. Outputs in `anchors/`.

---

## D. Questions for the operator

1. **A5 — supply `team_id` / team identity fields**, or confirm that packaging is out of
   scope for this arm and the deposit will be assembled elsewhere.
2. **A6 — are the Section-2/3/4 companion files scored anywhere?** If not, say so and I
   will keep submitting them purely as the honest prediction.
3. **Gate hand-off (this is the actionable one).** Candidate run id
   `20260827T202417Z_s2`, submission_1 set; baseline run id `20260827T194235Z_s1`,
   submission_1 set. Mechanism under test is stated in `REPORT.md` §3. **Caveat the gate
   should carry:** of the five promotion tasks, three (`altenmueller2024`,
   `dablander2025`, `kim2024`) are byte-identical between candidate and baseline because
   the mechanism is regime-conditional and does not fire there. The leave-one-study-out
   comparison therefore has an effective n of **two** differing studies
   (`beall2017`, `goldwert2026`). I would rather have a weak honest verdict than a
   candidate that changes things it has no reason to change; if the gate needs more
   differing studies to return a verdict at all, say so and I will propose a
   deliberately broader candidate next session.
4. **Budget.** Nothing spent on `claude -p` in any session; none requested. For the next
   session I would ask for 2-3 `rlm()` children again (target-side: an outcome-level
   profile anchor set from the train split expressed in the target's 13 outcomes; a
   party x message-family moderation prior; a distribution-shape library for Section 3).
5. **A note on this run's budget rule.** TASK_02B said the fresh scored-call budget is not
   extra and should be spent only on a question nothing else can answer. **I spent none.**
   Every question this session had — the benchmark's structure, the units, the valences,
   the moderator grid, the synthesis fidelity — was answerable from the mounted files, the
   organizer code, the train split, and by running the validator locally.

---

## E. Things still unfinished

* **`AGENTS.md` still does not exist.** `DESIGN.md` §5 (R1-R11) carries the standing rules.
  It should become `AGENTS.md` once the target-entry path is exercised with real numbers.
* **No target numbers exist yet.** `tools/target_entry.py` carries the *structure* and a
  placeholder table; `target_table()` is the single function a future session replaces.
* **Section-3 (distribution) modelling is untouched.** The scorer's Section 3 reads
  variance ratio, OVL, KS and W1 on a grid fixed to each outcome's full scale range. My
  synthesis currently draws clipped Gaussians, which is certainly the wrong shape for
  0-100 sliders (they pile up at 0, 50 and 100). A control-condition response-shape
  library from the train split is the missing input.
* **`inputs/idea01_lib/ssb/synth.py` still not read closely.** `tools/target_entry.py` was
  written from the benchmark's own spec instead; the idea_01 synthesiser may still have
  better distribution machinery and should be compared before the target entry is built.

---

## F. Session s3 — closed by the operator, and newly opened

**A5. `team_id` — CLOSED (s3).** The operator supplied **`team_31`** (registration
confirmed by the organizers). It is set in `target_entry_v1_pkg/metadata.json` and the
validator's filename and SHA-256 checks pass. Every other identity field (contact, repo
metadata, DOI wiring) is operator-side at packaging time and is not mine to carry.

**A6. Companions — CLOSED (s3).** Confirmed as observed: this environment's scorer returns
Section-1 diagnostics only, by design, and will not change. But the operator added the
distinction that matters: **the real benchmark does score the moderator file**, so an
honest-floor companion is a real prediction worth carrying — it just earns no feedback
here. R11 stands, with that gloss. 24 more companions submitted this run.

**A8. Cross-run half recurrence — CLOSED (s3), and it paid off immediately.** The operator
confirms halves cannot repeat within a (run id, task) but can recur across run ids from a
pool of 16, and that a recurrence should be read as a free exact replication. It happened
on the most important comparison of the session: `beall2017` s3/sub-1 drew the **same half**
as s1/sub-1 (reliability 0.5920, `mean_signed_error_pp` −1.4730, `r_within_adj` 0.1498, all
bit-identical), which turned the candidate-vs-baseline comparison into a noise-free one
(`REPORT.md` §2). Practical note for future sessions: **check the reliability and
signed-error fields for a bit-identical match before interpreting any pair of runs** — a
recurrence is the highest-quality evidence this environment can produce, and it is free.

### New in s3

**A9. Two anchors disagree about the control level of the primary outcome, by ~3 pp.**
`ANCHORS_D` recommends **60–67** for a climate-scientist trust composite in 2025–26
(item-format correction + the climate-vs-general-scientists penalty). `ANCHORS_E` derives
**69** (TISP 12-item generic 71.5, minus the 4–5 pp climate-specific penalty, plus 2–4 pp
for the 0–100 slider format) and cites D rather than redoing it. I used **69**, because
ANCHORS_E was built specifically for these 13 outcomes, and recorded the disagreement here
rather than splitting the difference silently. Consequence if E is wrong: the level enters
the Tier-2 condition means and every Section-3 distribution, but **never the ATEs**, which
are differences. Not resolvable from anything currently mounted; it needs a train source
that measures a 12-item 0–100 slider battery about *climate* scientists specifically.

**A10. ~4 pp of residual interaction error survives in the smallest synthetic cells.**
`verify()` reports `max_abs_interaction_pp_native` = 4.31 on the v1 entry, concentrated in
`gender = "Other"` (1% of an arm, ~30 rows) and `party = "Other"` (4%). Cause is understood
and is not sampling noise: with the empirical response shapes in place, many rows sit on a
point mass at 0 or 100 and cannot be moved, and one repair step per row per pass cannot
close a gap on a 1/12 lattice in a 30-row cell. Multi-step moves were tried and reverted —
clipping at the bounds breaks the ± symmetry of the swap and the **ATE** error went
0.025 → 1.87 pp, which is a far worse trade. Position taken: Section 1 is the headline, the
ATEs are now exact to 0.025 pp, and the human interaction contrast in a 10-person cell is
itself pure noise. Revisit only if a cheap exact method appears.

**A11. ANCHORS_F's party rule is validated but not adopted, deliberately.** The rule
(`0.5 · (−2.13 + 1.665 · ATE(o) · hgap(o))`, same value for all 16 arms within an outcome)
beats a zero floor under leave-one-study-out at half strength (held-out MSE 1.01 vs 4.90
pp²). I kept the exact-zero floor for v1 because (i) the design twin's omnibus cannot
reject zero (χ² = 87.7/90, below the placebo null mean 96.7), (ii) the fitted intercept is
not extrapolable to a study whose ATEs are 5–10× smaller than the fitting set — taken
literally it predicts a −1.07 pp interaction for an arm with no effect at all, which is
incoherent, and (iii) the ATE-proportional part alone is the through-origin form ANCHORS_F
could not distinguish from zero (γ = 0.047 ± 0.124). The `mod_inter` hook exists in
`tools/target_entry.py` and turning it on is a one-line change. **Pre-registered as the
Section-2 change for v2, conditional on resolving the intercept.**

**A12. R2 is retired and superseded.** `DESIGN.md` R2 ("default kappa ~0.5 in the
many-similar-arms regime, 1.0 for cells where the arm asserts the measured quantity") is the
rule the first gate rejected. Replaced by **R12–R16**. Anything in earlier notes that reads
back to R2 should be read through §8.1.

### Blinding disclosures — extended

* **No retrieval of any kind, in any session of this arm.** One package install this
  session: `anchors-moderation` installed `openpyxl` 3.1.5 from PyPI to read
  vlasceanu2024's `data63.xlsx` — the one permitted network use, named here for the audit.
* **Seven `rlm()` children across the arm** (`anchors-megastudies`, `anchors-trust`;
  `anchors-rank`, `anchors-levels`; **`anchors-profile`, `anchors-moderation`,
  `anchors-shapes`** this session), all scoped to `/workspace/datasets` + `/workspace/benchmark`,
  all explicitly forbidden `inputs/val/**`, `runs/**`, `inputs/idea01_lib/**` and the web.
  All three s3 children filed recognition disclosures of their own: they recognise
  voelkel2026, voelkel2024, vlasceanu2024, koetke2024, attari2016 and geiger2026 as
  published work and computed every number from the vendored microdata.
* **Validation outcomes never read**; `inputs/val/<task>/brief/` opened for `task.json` and
  the empty templates only. **Target outcomes do not exist here and were not sought**; the
  17×13 draft is derived entirely from `anchors/*` (train split) and the mounted instrument.
* **No number in `tools/target_model.py` came from a remembered published result.** Where a
  remembered qualitative regularity coincides with a train-split measurement, the measured
  train-split number was used.

---

## Session s4 — closed, bounded, and newly opened

**A9. CLOSED (s4) — resolved by ANCHORS_I, in favour of ANCHORS_D.** The primary outcome's
control level is **65.0** (band 61-69), not 69. ANCHORS_E's 69 was ~4 pp high for three
separately measured reasons: (a) it credited the 0-100 slider format with +2..+4 pp, and a
quantile-match of TISP `CLIM_TRUST` category shares onto vlasceanu2024's identically
configured 0-100 climate-scientist slider gives **+1.0 pp** (the slider cuts the top box
from 100 to 94 and lifts the floor from 0 to 7); ANCHORS_D's "+6" came from the ANES
thermometer, which is a warmth rating rather than a bipolar attribute slider, and is
retired. (b) the climate-referent penalty is **-5.5** (Pew W42 within-person +0.4 as a
lower bound, TISP within-person -4.5/-3.9, gligoric2025 -9.9 as an upper bound), not
-4..-5. (c) no 2023 -> 2026 time term was applied; GSS `consci` 63.2 -> 62.2 gives
**-1.5**. Four independent assembly routes give 65.5 / 62.2 / 69.8 / 62.8, weighted 64.9.
Carried into `tools/target_model.py` v2, together with `trust_post` 66.0 (now **above** the
composite - TISP's single global item and its 12-item composite agree to 0.6 pp for generic
scientists, so the "single items read lower" rule is retired), `distrust_post` 32.0, and
composite control SD 21.

**A10. BOUNDED, position unchanged (s4).** v2's `max_abs_interaction_pp_native` is **4.22**
(v1: 4.31) on the same causes - point masses at the bounds and a 1/12 lattice in ~30-row
cells. The multi-step repair remains reverted: it traded 0.02 pp of ATE error for 1.87 pp.
Section 1 is the headline and the human interaction contrast in a 10-person cell is itself
pure noise. Not worth further cost; revisit only if a cheap exact method appears.

**A11. Unchanged and now operator-endorsed.** The exact-zero moderation floor stays in the
entry. The ATE-scaled ANCHORS_F rule stays pre-registered with the `mod_inter` hook unused,
and does not enter a deposit candidate without a gate-grade test.

### New in s4

**A13. What predicts a study's r_adj-optimal message/outcome mix?** `DESIGN.md` §9.2: the
same mix change is worth **-0.086 r_adj on beall2017 and +0.054 on goldwert2026**, both
17-28x the measured fresh-draw noise. The effect is real, large, and study-specific, and
nothing in the brief tells me which way it goes. Working hypothesis, **not adopted and not
fitted** (n = 2): studies whose predicted outcome profile is strongly differentiated
(beall: `sd_btw` 5.7 pp, sign-flipping) carry a lot of skill at the outcome level and lose
by moving weight away from it; studies whose profile is flat (goldwert: `sd_btw` 1.06 pp,
all-positive) do not. By that hypothesis the target resembles **beall**, not goldwert - its
profile is sign-flipping with `sd_btw` 0.42 against a mean of 0.30 - which is one of the two
reasons v2 sits at the low end of the validated mix band. Testable only with a third
many-variant study.

**A14. `donation_ams` may have a negative true ATE, and the entry predicts +0.05.**
ANCHORS_I's own centre is +0.05 with a band of **-1.2 to +0.8**, and the strongest single
piece of evidence inside that band points down: in the design twin (voelkel2026, the same
$10-bonus allocation task) the ten climate arms moved donation **-3.95 to +0.53, mean
-1.38**, with a true between-arm SD of ~0 - i.e. one common negative shift, a mechanism
rather than noise - while the same arms moved belief **+1.42**. koetke2024's opt-in
reverses the same way. The reading is "messages move attitudes up and behavioural
follow-through down or nowhere". ANCHORS_I nonetheless recommends +0.05 because the
target's recipient (AMS, a scientific society, described as explicitly non-partisan) is
aligned with a trust message in a way a climate NGO is not, and because the target's $10 is
a lottery with p ~ 0.006. **I took my own instrument's recommendation rather than
overriding it with half of its own evidence**, and I am recording the alternative here: the
honest-abstention play is an exact zero on all 16 `donation_ams` cells, which the scorer
gives half directional credit for by construction. 16 of 208 cells are at stake. If a
future session gets a third data point on behavioural follow-through, this is the cell to
revisit first.

**A15. `donation_ams` response shape: two anchors, small disagreement, `shape_lib` kept.**
ANCHORS_I derives an explicit tri-modal pmf (`anchors/donation_shape.csv`: p(0) = .288,
p(5) = .175, p(10) = .217, mean 4.38, sd 3.83). The synthesiser's `shape_lib`, asked for
mean 4.40, returns p(0) = .373, p(5) = .209, p(10) = .178, mean 4.45, sd 3.87. They agree
on the level, the SD and the tri-modality and differ by ~0.09 on the floor mass.
`shape_lib` is kept because it was validated end to end with the organizers' own Section-3
metrics on 47 real items, while ANCHORS_I itself flags its own p(10) as "a stake-scaled
guess" (its §5.4). Low stakes; recorded so the choice is not silent.

### Blinding disclosures — extended (s4)

* **No retrieval of any kind, in any session of this arm.** Two package installs this
  session, both by children, both named for the audit: `anchors-arms` installed `pypdf` and
  `openpyxl`; `anchors-levels2` installed `pyreadstat`. Permitted network use, nothing else.
* **Nine `rlm()` children across the arm.** The two this session (`anchors-arms`,
  `anchors-levels2`) were scoped to `/workspace/datasets` + `/workspace/benchmark` +
  `anchors/`, and explicitly forbidden `inputs/val/**`, `runs/**`, `inputs/idea01_lib/**`
  and the web. Both filed recognition disclosures: between them they recognise tisp,
  vlasceanu2024, voelkel2024, voelkel2026, koetke2024, gligoric2025, hackenburg2025,
  spampatti2023 and the standard public series (pew_atp/gss/anes/ccam/wellcome) as published
  work, and computed every number from the vendored microdata. Neither was given, nor
  asked for, anything about a validation task; neither knows the validation set exists.
* **Validation outcomes never read**; `inputs/val/<task>/brief/` opened for `task.json` and
  the empty templates only. **Target outcomes do not exist here and were not sought.**
* **No number in `tools/target_model.py` came from a remembered published result.**


---

## Session s5 — closed, retracted, and newly opened

**A13. CLOSED (s5) — as unanswerable on this train split, and its premise partly retracted.**
Two things happened to it. (i) Its *premise* was that the mix effect is "opposite in sign
between tasks". Under the corrected draw noise (`DESIGN.md` §10.1) s4's goldwert read is
0.8σ, not 28σ: the honest statement is one significant negative (beall, 5.3σ) and one null,
not a sign flip. (ii) ANCHORS_J measured the noise-corrected true mix in 16 train studies and
tested every brief-visible design feature against a pooled-mean baseline out of sample.
`n_arms`, `n_outcomes`, `n/arm`, outcome breadth, scale-type mixing, behavioural outcomes,
one-construct and assertion-match are **all worse than the baseline**; the one feature that
helps was coded after seeing the answers and buys nothing on the bounded scale; and two
studies from one lab with the same outcome set land at 0.14 and 2.13. **There is no rule to
find here.** The honest fallback is the pooled prior with an asymmetric loss: over-weighting
the message level costs about twice what under-weighting costs, so err low. v3's mix is
0.2125, inside the environment's validated [0.15, 0.30] and at the low edge of ANCHORS_J's
submitted-mix band [0.2, 0.9]. Its centre (0.45) disagrees with mine by a factor of two;
recorded, not acted on, because both instruments agree about which side to err on.

**A14. CLOSED (s5) — RESOLVED AGAINST the v2 entry.** ANCHORS_K, an independent read told to
form its own view before reading ANCHORS_I, puts `donation_ams` at **−0.7 pp (band −2.0 to
+0.6)** and, decisively, points out that the scorer's expected directional credit is 0.62 for
a negative, 0.50 for an exact zero and 0.38 for a positive — so v2's +0.05 was the **worst of
the three available answers**. Its mechanism is new and replicated: holding post attitudes
fixed, the *direct* effect on giving is −2.42 ± 0.91 (voelkel2026) and −2.53 ± 0.63
(vlasceanu WEPT), i.e. `behavioural ≈ −2.5 + 0.5 x attitude`, a constant negative offset
rather than a shrunken copy. It falsified end-of-survey fatigue as the cause for this design
and found in the target's own SurveyFlow that both behavioural asks are **mid-battery**
(inside a `BlockRandomizer(7)` over the secondary blocks), not last. The entry's cell is now
−0.70, and `L_OUT["donation_ams"] = 0` because the noise-corrected between-arm SD of donation
in the design twin is **exactly 0.000**. What is still not established, and is stated as such
by its author: the sign of *recipient alignment* for a scientific society — no train
experiment donates to one, none randomises the recipient, and the whole reason the centre is
−0.7 rather than voelkel2026's −1.4 is one confounded contrast (voelkel2024's dictator game,
where the recipient is the message's own subject; ratio 0.877, r = 0.832 over 26 arms). If
that contrast is wrong, the cell belongs at −1.4.

**A15. Unchanged (s5).** `shape_lib` still supplies the donation response shape. The level it
is asked for is unchanged ($4.40 control); only the ATE moved.

### New in s5

**A16. `ASSERTION_MATCH` covers 4 cells of 208, and the measurement says coverage is what
matters.** §10.3's cleanest many-arm read (goldwert2026) compared a **26-cell** authored
targeting map against my standing rank-1 ordering and the map won by +0.216 r_adj at matched
amplitude. The target entry's targeting map has **four** cells, because DESIGN §6.6's
re-derivation from the 16 real texts found that a strict assertion-match rule fires on
exactly three cells at full strength and one at half. v3 therefore acts on the measurement by
**re-weighting** the four cells, not by inventing a quarter-tier of speculative ones — the
same refusal that kept ANCHORS_F's intercept out of the entry. This is the open question I
would put first next session: is there a defensible *half-tier* content-targeting map for
these 16 texts and 13 outcomes (e.g. Corporate reliance -> `funding_perceptions`, Model
accuracy / Measurement & modeling -> `belief_post`, Extreme weather predictions ->
`concern_mean`, Scientist community helpers -> `policy_role_mean`), and can any of it be
validated on the train split rather than authored? If it can, the entry gets more of its
message-level bet onto the class that measurably carries the skill; if it cannot, four cells
at ratio 2.43 is where it should stay.

**A17. The corrected σ table has only 2–3 dof on the two tasks that matter.** beall2017's
sd(r_adj) rests on 2 dof and goldwert2026's on 3, so both are themselves uncertain by roughly
a factor of two, and the 12.6σ and 2.3σ figures inherit that. Nothing in this run depends on
the difference between 12σ and 6σ, but a future session that needs a 3σ call on goldwert
should buy dof first — an affine-pair submission costs one call and adds a degree of freedom
(R21/R22).

**A18. `S_MULT` is a new constant in the neighbourhood of a promoted one.** `KAPPA = 0.20` was
promoted by the gate as the message level's amplitude. v3 leaves that amplitude exactly
unchanged and changes only the direction, but it does so by multiplying the rank-1 term by
0.6289 and the assertion term by 1.1617, which an unsympathetic reading could call a
differential kappa. The defence is in `DESIGN.md` §10.4: both terms are message level, the
mix is unchanged, and the invariant the gate promoted (total message-level norm) is preserved
to four decimals. It is flagged here so the operator can see the seam rather than discover it.

### Blinding disclosures — extended (s5)

* **No retrieval of any kind, in any session of this arm.** Two package installs this
  session, both by children, both named: `anchors-mix` installed `pyreadstat` and `pyreadr`;
  `anchors-behav` installed `openpyxl` and `pypdf`. Permitted network use, nothing else.
* **Eleven `rlm()` children across the arm.** The two this session (`anchors-mix`,
  `anchors-behav`) were scoped to `/workspace/datasets` + `/workspace/benchmark` +
  `anchors/`, and explicitly forbidden `inputs/val/**`, `runs/**`, `inputs/idea01_lib/**` and
  the web. Both filed recognition disclosures and computed every number from the vendored
  microdata. Neither was given, nor asked for, anything about a validation task; neither
  knows the validation set exists. `anchors-mix`'s task was posed in purely structural terms
  (the outcome-level/message-level decomposition) with no validation study named.
* **Validation outcomes never read**; `inputs/val/<task>/brief/` opened for `task.json`, the
  templates and the arm/outcome descriptions only. The AM-ISO cell sets were derived from
  those descriptions and fixed in writing before any file was scored.
* **Target outcomes do not exist here and were not sought.** No number in
  `tools/target_model.py` came from a remembered published result.


---

## Session s6 — A18 resolved, A16/A14-residual closed, and four items opened

### Closed in s6

**A18. RESOLVED — the entry's direction change REVERTS.** `A_MULT` 0.4647 → **0.40**,
`S_MULT` 0.6289 → **1.00**. Two independent grounds, both written before this run's scored
calls (`runs/20260828T074119Z_s6/val/PREREG_S6.md` §1; DESIGN §11.1–11.2). **Textual:** the
frozen definitions put `tools` inside durable state, and only gate-surviving techniques enter
durable state; those constants' sole warrant was the AM-ISO measurement, declared as M10/R23
and REJECTED. s5's pre-registered escape hatch ("REJECTED means no net gain") does not apply,
because the verdict carried a *failure family*, which is the second clause — "without hurting
any one study beyond noise" — failing too. **Empirical:** beall2017's three matched-amplitude
tables show the allocation curve **saturates** at or below the incumbent share (slope +0.275
below, +0.034 above), so the v2 → v3 move was worth about +0.008 r_adj; s5's 2.55x correction
came from a linear extrapolation those three points falsify; and this run's replications took
sd(r_adj | beall) from 0.0116 to **0.0659**, turning "12.6 sigma" into **2.2 sigma**. The
general rule that decides such cases in future is **R27**: gate governance follows the evidence
base, not the file.

**A16. CLOSED NEGATIVELY — no mechanically-coded targeting map validates, and the authored
4-cell map is vindicated as the strict tail.** ANCHORS_L, LOSO over 4 text-vendored train
studies with the rule fixed by sha256 before any effect table existed: on the campaign's own
residual the targeting code gives beta = +0.066 pp (se 0.537), LOSO MSE **rises**, worse in 4
folds of 4, permutation p = 0.46. It beats an arm-main-effect-only baseline strongly
(p = 0.001), so **content targeting is a substitute for the rank-1 outcome loading, not a
complement to it**. The mechanism itself is real (voelkel2024's own expert coders, 25 arms:
beta = −0.217 pp/point, leave-one-arm-out ΔMSE = −0.061, p = 0.013) — the *string rule* is what
fails. Its mechanical map fires on 111/208 target cells but reproduces §6.6's four cells exactly
at the strict tail, including grading High public trust × trust_multidimensional as *half*. The
entry keeps four cells, as §6 of the s5 report pre-committed. `targeting_target_map.csv` ships
empty by design; the unvalidated map is preserved beside it.

**A14 residual (recipient alignment). CLOSED — and it moved two entry constants.** ANCHORS_M
prices the alignment swing at **+4.29 ± 0.61 pp (7.1 sigma)** between a subject-aligned and a
cause-aligned recipient, on one identical specification across five behavioural outcomes.
`M_RAW["donation_ams"]` **−0.70 → −0.40** (its own centre; it also found two arithmetic slips in
the −0.70 that cancelled). `L_OUT["donation_ams"]` **0.000 → 0.997** (0.883 × the trust
loading): v3's exact zero was a floor artefact of an underpowered heterogeneity design, and the
informative estimate is voelkel2024's 25 arms (tau ratio 0.883, arm-level r = +0.829). Both
changes met conditions that were fixed in writing before the child reported.

**A19 (opened and closed in the same session). The gate's failure family vs the entry's
zero-spread donation cell.** The s5 candidate zeroed dablander2025's donation ordering and the
gate named "donation/behavioral outcomes" as where it lost. That was the one live diagnostic
against `L_OUT["donation_ams"] = 0`. ANCHORS_M reached the same verdict independently from the
train split, and v4 removes the exact zero. Two instruments, one from each side of the split,
agreeing on a cell — the only time that has happened in this arm.

### Still open, unchanged

**A15** (donation response shape; `shape_lib` kept — the level is unchanged at $4.40, only the
ATE and the arm spread moved). **A17** is *partly* discharged: beall2017 and goldwert2026 now
have 3 and 4 dof; dablander and kim have 6 each; nothing has fewer than 3, which is now the
floor R29 requires before a task may carry a mechanism claim. **O2** (ANCHORS_F's party-moderation
hook, still off). **O4** (the rank-1 arm score, still unvalidatable on train — and ANCHORS_L now
adds that it is doing the work a targeting term would otherwise claim). **O6/A10** (residual
interaction error in the smallest synthetic cells).

### New in s6

**A20. On the target's structural twin, the targeted allocation lost within-outcome ordering
skill — 2.2 sigma, one task.** goldwert2026's promoted-table class returns r_within_adj of
0.1098 / 0.0938 / 0.0683 / 0.1529 (mean 0.106, sd 0.0397) against the AM-ISO TARGETED value of
**0.0181**. beall2017 shows nothing (its sd(r_within_adj) is 0.0852, so its apparent drop is
0.4 sigma and I have retracted my own citation of it). If A20 is real it is the sharpest
statement yet of why the message level's *ordering* and its *outcome loading* must not be
traded against each other — but it is one task at 2.2 sigma and R17 forbids acting on it.

**A21. ANCHORS_M's subject pole rests on a single study.** The +1.97 subject-aligned estimate is
voelkel2024's dictator game and nothing else; no train study randomises the recipient, so the
subject-vs-cause step is strictly between studies, confounded with topic, person-vs-organisation
and survey position. If +1.97 is a property of between-person dictator games rather than of
alignment, the swing evaporates and `donation_ams` belongs near **−1.4** instead of −0.40. This
is worth 1.0 pp on 16 of 208 cells and it is the entry's largest single open exposure.

**A22. The assertion term is the largest number in the entry that rests on an argument rather
than a measurement.** ANCHORS_L caps a targeted term at 0.12 × the generic rank-1 norm (band
0.00–0.20); v4 sits at **1.185**. v4 does not move, on the reconciliation in DESIGN §11.7: the
cap is a ratio to a term the entry deliberately shrinks (`KAPPA = 0.20` on an ordering) and
train does not, and in **absolute pp** the two instruments agree — ANCHORS_L's own expert-coded
full reference is worth 0.74 pp against v4's 1.00 and 0.72 pp full cells, and v4's half cells
are already at 0.42 and 0.28 of a full cell, inside its 0.24–0.65 band. That is a
reconciliation, not a proof. **The one test that would settle it**: code the train split for
*elicit-and-correct* arms specifically (the `gatewaybelief` dataset is the canonical one and
ANCHORS_L's inclusion rule excluded it for having too few arms) and measure the absolute
effect of an on-screen numeric correction on the corrected item. If that comes back near 0.7-1.0
pp, `A_MULT = 0.40` is right; if it comes back near 0.2, the entry's two largest cells are 3-5x
too big.

**A23. Two of the arm's four "measured" mechanism claims have now been retracted by better
noise estimates, and both retractions came from the same omission.** s4's mix reads (17-28
sigma → 5.3/0.8 → 0.9/0.8) and s5's AM-ISO reads (12.6 sigma → 2.2) were both inflated by a
noise scale estimated from too few degrees of freedom on the deciding task. R29 now forbids a
mechanism claim on a task with fewer than 3 dof, and R26 requires the table correlation to be
computed first. What is not yet fixed is that **every remaining sigma in this arm rests on 3-6
dof**, so a factor of ~1.4 in any of them is still live.

### Blinding disclosures — extended (s6)

* **No retrieval of any kind, in any session of this arm.** No package installs by me this
  session; `anchors-recipient` installed `pypdf` and `openpyxl`; `anchors-targetmap` installed
  nothing. Permitted network use only.
* **Thirteen `rlm()` children across the arm.** The two this session (`anchors-targetmap`,
  `anchors-recipient`) were scoped to `/workspace/datasets`, `/workspace/benchmark` and
  `anchors/`, and explicitly forbidden `inputs/val/**`, `runs/**`, `inputs/idea01_lib/**` and
  the web. Both filed recognition disclosures naming the studies they recognise and stating
  that no remembered number was used; both computed every figure from vendored microdata with
  per-number provenance files. Neither was told the validation set exists. `anchors-targetmap`
  was told *that* a gate had named a "donation/behavioral" failure family, because its
  behavioural sub-answer was the point of the task; it was told nothing about which studies,
  which submissions, or any score.
* **Validation outcomes never read.** This session's two scored calls were byte-identical
  resubmissions of an s3 table; no brief was reopened and no new task was modelled.
* **Target outcomes do not exist here and were not sought.** No number in
  `tools/target_model.py` came from a remembered published result.

### Closed in s7

**A22. CLOSED — by measurement, and it moved the entry in the direction s6 did not expect.**
`anchors/ANCHORS_N.md` (child `anchors-assert`, train split, 6 studies, 79 rows) measures the
elicit-and-correct excess in the units the scorer reads. The classification is the result:
**C1** (the item asks for the corrected quantity back) **+9.37 pp**, **C2** (the item asks the
respondent's own belief in the corrected claim) **+1.30 pp (se 0.23, dof 5, CI [+0.71, +1.90],
LOSO +1.15 to +1.41)**, **C3** zero by construction. The target scores **no C1 item**, so the
big number is worth nothing and the deciding number is +1.30 against the entry's authored 0.86.
PREREG_S7's two-sided posterior rule — fixed before the child reported — returns
`A_MULT = 0.554 -> 0.55` and fires. **Entry v5**: `A_MULT` 0.40 -> 0.55, nothing else, mix
0.238 -> 0.293 inside the validated [0.15, 0.30], `make check` 40 pass / 4 warn / 0 fail.
s6 said the entry was at risk if this came back near 0.2 pp; it came back at 1.30, and the same
arithmetic that would have cut the term by three raised it by 37%.

### New in s7

**A24. The two social-norm cells were raised by a measurement that does not support them, and
the Funding cell by one that never saw a funding correction.** ANCHORS_N's C2n class — the
corrected quantity is a descriptive norm and the item asks the respondent's own attitude, which
is exactly `High public trust` — is **+0.61 pp on one study** and **+0.09 ± 0.54 pp** on the
between-arm contrast over two. The pre-registered rule moves the multiplier and never the shape,
so those cells rose with `A_MULT`: `High public trust × trust_post` is now **+1.349 pp**, the
entry's second-largest cell, on the weakest evidence in the table. Symmetrically, there is **no
funding-correction arm anywhere in the train split**, so `Funding × funding_perceptions`
(+1.664 pp, the largest cell) inherits only the generic C2 pool: nothing measured says a
dollar-amount correction behaves like a scientific-consensus correction. Both are recorded
rather than patched, because re-authoring the shape after seeing the number is what R31 forbids.
The cheapest test that would settle the C2n half: a train study that corrects a descriptive norm
about *scientists* and then measures own trust. I know of none in `/workspace/datasets`.

**A25. The update rests on `E_out`, and the estimand that controls for arm quality would not
have moved the entry.** `E_arm` (correcting arm minus the study's other message arms on the same
item) gives +1.02 ± 0.44 pp on **dof 1**, which the rule puts inside the dead band (`A_MULT` 0.43).
R29 disqualifies a dof-1 estimand as a headline and that is why `E_out` decides — but a reader who
prefers between-arm identification should read v5 as v4 plus noise. What would settle it: a
correcting arm in a many-arm study with a pre-measure, which exists only in the two megastudies
where the correction is asserted rather than elicited.

**A26. `E_out` and the entry's base effect are not cleanly separable.** `E_out` subtracts the
arm's own effect on the study's other outcomes, so it also removes whatever outcome-level
difference those studies carry. The entry's outcome level comes from ANCHORS_E, which pools a
different set of studies, and its message level from ANCHORS_H; if either already averages over
consensus-type arms, part of the +1.30 is being counted twice. Bound on the damage: the gap
between `E_out` (+1.30) and `E_arm` (+1.02) is 0.28 pp, i.e. at most ~0.09 of `A_MULT`.

### Blinding disclosures — extended (s7)

* **No retrieval of any kind, in any session of this arm.** No package installs by me this
  session; the child installed none. Permitted network use only.
* **Fourteen `rlm()` children across the arm.** This session's one (`anchors-assert`) was scoped
  to `/workspace/datasets`, `/workspace/benchmark` (instrument and codebook only — the target has
  no outcome data), and `anchors/`, and explicitly forbidden `inputs/val/**`, `runs/**`,
  `inputs/idea01_lib/**` and the web. It filed a recognition disclosure naming the van der Linden
  gateway-belief experiments and the Voelkel megastudy, stated that no remembered number was
  used, and computed every figure from vendored microdata with a 13-row provenance file. I
  independently re-derived one of its six studies from the raw CSV and matched it to four
  decimals (PREREG_S7 §R6).
* **Zero scored validation calls and zero `claude -p` calls this session**, planned in advance in
  PREREG_S7 §4 with reasons, and unchanged by the verdict.
* **The target study's outcome data does not exist in this container and was never sought.** The
  only target files read this session were `survey/questionnaire.txt`, `survey/condition_codenames.csv`
  and `codebook.csv` — the public instrument.
