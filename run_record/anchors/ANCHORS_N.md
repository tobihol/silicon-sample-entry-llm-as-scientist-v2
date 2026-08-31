# ANCHORS_N — the elicit-and-correct ("assertion") excess, measured on the train split

child: `anchors-assert` | open item **A22** | train split only (`/workspace/datasets/**`)
pre-committed rule: `anchors/_n_rule.txt`, sha256 `9fe42941198ddce0d04ba8b3fd0cd3d4447afe14cd29b975eabde4e6cd8cfff8`,
committed 2026-08-28T08:36:14Z — **written to disk before any effect was computed**.
tables: `anchors/assertion_train.csv` (79 rows), `anchors/_n_noncorrecting_comparators.csv`,
provenance: `anchors/_n_sources.csv` (13 rows).

---

## 0. THE DECIDING NUMBER

**Ê(C2) = +1.30 pp, se 0.23, dof 5 (k = 6 studies), 95% CI [+0.71, +1.90].**

That is the pooled **E_out** excess: the ATE of a correcting arm on the own-belief item about the
corrected claim, minus the same arm's mean ATE on that study's other, non-corrected outcomes,
in pp of scale range. It survives leave-one-study-out with essentially no movement (range
**+1.15 to +1.41**). The alternative within-study contrast, **E_arm = +1.02 pp (se 0.44)**, agrees,
but rests on only k = 2 studies (dof 1) and must be read as corroboration, not as an independent number.

`E_abs(C2) = +2.45 pp (se 0.29, dof 5, CI [+1.70, +3.19])` is reported as an upper bound only: it
contains the base effect any message of this family has on a belief item, which the prediction model
already carries on every cell.

---

## 1. What the three target arms are, and how they classify

Read from `/workspace/benchmark/survey/questionnaire.txt` (design only; this study has no outcome data
and none was sought).

| target arm | elicited quantity Q | correction | scored cell(s) | class |
|---|---|---|---|---|
| **Funding** | agreement with 3 funding claims (0-100 sliders) | \$10.6bn vs \$52.5bn; \$7bn vs \$160bn; "3% of programs"; median salary \$80,060 | `funding_perceptions` ("is the federal government spending too much / too little on climate research?") | **C2** |
| **Consensus** | 3 x "% of scientists who agree" (0-100 sliders) | per-item feedback 99% / ~100% / 66% | `belief_post` ("Human activities are causing climate change") | **C2** |
| **High public trust** | "% of Americans who trust climate scientists" (0-100) | Pew 76% | `trust_post`, `trust_multidimensional` | **C2n** (Q is a social norm) |

All three **elicit** first and then correct with **personal feedback** (the Consensus and High-public-trust
screens are keyed to the respondent's own slider; the Funding screens rebut the respondent's own
agreement ratings item by item).

---

## 2. Inclusion: what the rule admitted, and what it threw out

Screened: every vendored dataset with a randomised message arm. The correction test (rule §1) requires
a specific numeric value, presented as the true value of an identified factual quantity Q, framed as
correcting beliefs about Q.

**Admitted — 7 study-units (6 with a C2 item, 2 with a C2n item), 5 data sources:**

| id | study | correcting arm(s) | elicited / personal feedback | other message arms | C1 | C2 | C2n | C3 |
|---|---|---|---|---|---|---|---|---|
| S1 | `gatewaybelief` Exp1 (Maertens 2020) | Consensus (= Consensus + Balanced; identical content at T2, verified by `Duration_Consensus_T1T2`) | 1 / 0 | 1 (disqualified, see §5) | PSC | Belief, HumanCausation | – | Worry, Support |
| S2 | `gatewaybelief` Exp2 (vdL 2017) | PieChartOnly (97% pie chart) | 1 / 0 | 1 (disqualified) | psc | belief, hcaused | – | worry, action |
| S3 | `geiger2026` vdL 2019 US RCT | consensus message | 1 / 0 | 0 | consensus | belief, cause | – | worry, policy |
| S4 | `geiger2026` Većkalov 2024, 27 countries | classic + updated consensus | 1 / 0 | 0 | consensus_perception, agreement_perception | belief_climate_change, belief_human_causation | – | belief_crisis, worry, action_support, scientist_trust |
| S5a | `vlasceanu2024`, 63 countries | SciConsens ("99% of expert climate scientists agree") | 0 / 0 | 9 | PerceivedSciConsensu | Belief.in.CC_1 | – | 3 belief + 9 policy |
| S5b | `vlasceanu2024` | PluralIgnorance ("You estimated X% of Americans agree ... in truth 65%") | **1 / 1** | 9 | – (item asked in control only) | – | Belief.in.CC_5 | 3 belief + 9 policy + PerceivedSciConsensu |
| S6 | `voelkel2026` CCC | Consensus Framing 1 (97%), Consensus Framing 2 (98% / 97.1%) | 0 / 0 | 8 | Check_Consensus | Belief_Post | – | 7 post composites |
| S7 | `gligoric2025` main | Norms ("over 70% of conservative respondents report high confidence in scientists") | 0 / 0 | 4 | – | – | trust_all35 | – |

**Screened and excluded, with reason:**

* `gatewaybelief` supplemental (Maertens 2025) — Control / Inoc / InocInoc; no verifiable correcting arm.
* `spampatti2023` — the "scientific consensus" inoculation *is* a correcting arm (97-99%), but the study
  measures only affect toward climate-misinformation statements: **no C1, C2 or C2n item exists**, so no
  excess is identified. Contributes only C3 rows; dropped rather than padding the table.
* `hackenburg2025` — 730 LLM-generated arms; excluded by rule (no designed quantity Q).
* `tappin2023` — 48 human persuasive essays; numbers incidental to an argument, no designated Q, no
  elicitation; fails correction-test (c).
* `bago2025`, `agley2021`, `koetke2024`, `schmidbetsch2019`, `attari2016` — no arm states a specific
  numeric value as the corrected value of an identified factual quantity.
* Within admitted studies: `vlasceanu2024` NegativeEmotions ("over 90% of the increase in temperature",
  "99% of coral reefs"), CollectAction ("40% less aggressive"), and `gligoric2025` Co-Benefit ("11% of
  GDP") all contain numbers, but the numbers are illustrative inside a broader argument and the study
  measures nothing about their Q — excluded as correcting arms, retained as non-correcting comparators.
  `voelkel2026`: a full-text scan of all ten treatments found numeric claims **only** in the two
  consensus arms.

---

## 3. Per-class results (pp of scale range)

Aggregation is fixed by rule §5: items -> (study, arm) with r = 0.5 among same-class items ->
study -> unweighted pool across studies; se = max(between-study SD/sqrt(k), sqrt(mean within var)/sqrt(k));
t-based CI on k-1 dof.

| class | E_abs | E_out | E_arm | k (E_out) |
|---|---|---|---|---|
| **C1** (item asks for Q itself) | +10.52 pp (se 2.37, dof 5, k=6, 95% CI [+4.42, +16.61]) | +9.37 pp (se 2.17, dof 5, k=6, 95% CI [+3.80, +14.94]) | +6.02 pp (se 1.80, dof 1, k=2, 95% CI [-16.84, +28.88]) | 6 |
| **C2** (own belief in the claim) | +2.45 pp (se 0.29, dof 5, k=6, 95% CI [+1.70, +3.19]) | **+1.30 pp (se 0.23, dof 5, k=6, 95% CI [+0.71, +1.90])** | +1.01 pp (se 0.44, dof 1, k=2, 95% CI [-4.56, +6.59]) | 6 |
| **C2n** (own attitude, Q a social norm) | +0.90 pp (se 0.49, dof 1, k=2, 95% CI [-5.34, +7.14]) | +0.61 pp (k = 1 study, no CI) | +0.09 pp (se 0.54, dof 1, k=2, 95% CI [-6.84, +7.01]) | 1 |
| **C3** | 0 by construction (C3 is the E_out reference) | — | — | — |

The **C1 -> C2 -> C3 gradient is the whole result**: a numeric correction moves the corrected quantity
itself by about **+9 to +10 pp**, moves the respondent's own belief in the underlying claim by about
**+1.3 pp above** the arm's own effect on unrelated outcomes, and leaves the C3 outcomes at the arm's
generic level. **The target study scores no C1 item.** The ~9 pp C1 effect is therefore worth exactly
nothing to the entry, and is reported only because it is what makes the C2 number credible: the same
manipulation that produces a 7-sigma C1 move produces a 1.3 pp C2 excess.

### Per-study C2 estimates (the headline's ingredients)

| study | E_abs | E_out | E_arm | elicited |
|---|---|---|---|---|
| gatewaybelief_Exp1_Maertens2020 | +2.62 (0.82) | **+2.08** (0.82) | n/a | 1 |
| gatewaybelief_Exp2_vdL2017 | +3.51 (0.87) | **+1.34** (0.87) | n/a | 1 |
| geiger2026_Veckalov2024_27c | +1.49 (0.27) | **+0.78** (0.27) | n/a | 1 |
| geiger2026_vdL2019_US | +2.82 (0.31) | **+1.32** (0.31) | n/a | 1 |
| vlasceanu2024_63c | +1.92 (0.51) | **+1.00** (0.51) | +0.58 | 0 |
| voelkel2026_CCC | +2.32 (0.27) | **+1.28** (0.27) | +1.45 | 0 |
| **pool** | **+2.45** | **+1.30 (se 0.23, dof 5)** | +1.02 (dof 1) | |

**LOSO on Ê(C2) = E_out:** dropping each study in turn gives
gatewaybelief->+1.15, gatewaybelief->+1.29, geiger2026->+1.41, geiger2026->+1.30, vlasceanu2024->+1.36, voelkel2026->+1.30.
Range **+1.15 to +1.41**; no study drives the pool. The smallest study-level value (+0.78, Većkalov)
and the largest (+2.08, Maertens Exp1) are the two with the strongest ceiling (93.3% and 89.6% of
the item maximum in the control arm), so the spread is not tracking anything systematic.

### C2n (the "High public trust" analogue)

Only two arms in the entire train split correct a **social norm** and then measure an own attitude:

* `vlasceanu2024` PluralIgnorance — elicited, personal feedback, exactly the target's structure:
  E_abs +1.01 pp (se 0.52), **E_out +0.61 pp**, E_arm **-0.46 pp**.
* `gligoric2025` Norms — asserted-only: E_abs +0.79 pp (se 0.83), **E_arm +0.63 pp**; no C3 item
  exists in that study, so E_out is not identified.

Pooled C2n: E_abs +0.90 pp (dof 1); **E_arm +0.09 pp (se 0.54, dof 1)**. On the estimand that matters,
the social-norm correction is **indistinguishable from zero and roughly an order of magnitude below C2**.
Both numbers rest on one study each and must be read as such.

---

## 4. Elicited vs asserted-only

I have both kinds, which is the one thing the parent flagged as decisive for transfer.

* **C2, elicited (k = 4: S1, S2, S3, S4): E_out mean +1.38 pp.**
* **C2, asserted-only (k = 2: S5a, S6): E_out mean +1.14 pp.**
* **Elicitation increment: +0.24 pp, se 0.30, t = 0.79 on ~3 dof — not distinguishable from zero.**

Two caveats that both cut against reading an elicitation premium into this:

1. The split is confounded with design: every elicited study is a classic two-arm consensus experiment
   analysed by ANCOVA on its own pre-measure; both asserted-only studies are many-arm megastudies
   analysed by post-difference. The +0.24 pp could be entirely the estimator's extra precision or the
   pre-measure's own priming.
2. **No elicited arm in the train split gave personal feedback except one — and it is the *lowest*
   number in the whole table.** `vlasceanu2024` PluralIgnorance ("You estimated X% ... in truth 65%")
   is the only train arm that reproduces the target's exact mechanic, and its E_out is +0.61 pp and its
   E_arm is **-0.46 pp**. If personal feedback carried a premium, that arm should have been the largest.

---

## 5. Deviations, operationalisations and judgement calls (all disclosed)

The rule was applied mechanically. Three points where it needed operationalising, decided **before**
any effect was computed except where stated:

* **(a) Correction-test clause (c), operationalised.** A number passes (c) iff the stimulus either
  (i) explicitly names the lay estimate/misperception it is correcting, or (ii) is the arm's single
  headline claim delivered as essentially the whole message. This is what excludes NegativeEmotions,
  CollectAction and Co-Benefit and admits sciConsensus_1, plurIg_Text, Consensus1/2_P1 and the
  gligoric Norms message. Decided at classification time, before any ATE.
* **(b) Comparator admissibility for E_arm (added after S1/S2 were computed — a real deviation, disclosed).**
  Two screens, applied uniformly: a comparator arm must be **pro-attitudinal** (designed to move the
  outcome in the same direction as the correcting arm), and must **not itself deliver the correction**
  (operationalised as: disqualified if its C1 effect is >= 50% of the correcting arm's C1 effect).
  Consequences: S2's only other message arm is `CounterOnly`, a *misinformation* arm (psc -9.3 pp,
  belief -3.1 pp) -> disqualified; S1's only other message arm is `Inoculation`, whose stimulus is not
  vendored and which moves PSC by **+8.07 pp against the correcting arm's +9.30 pp** — direct evidence
  that it carries the same 97% number -> disqualified. S3 and S4 have no other message arm at all.
  **So E_arm is identified only in S5, S6 (C2) and S5, S7 (C2n).** Had I mechanically kept the
  disqualified comparators, S1's E_arm(C2) would have been -0.87 pp and S2's +6.32 pp — i.e. the
  comparator, not the mechanism, would have been the whole estimate. This is why E_out is the headline.
* **(c) Multi-country samples.** S4 (27 countries) and S5 (63 countries) are pooled over all countries
  for maximum precision. **US-only sensitivity:** S5a C2 E_out +1.85 pp (vs +1.00 full), S4 C2 E_out
  +1.12 pp (vs +0.78 full), S5b C2n E_out +2.91 pp (vs +0.61 full) — all noisier but all **larger**,
  so the full-sample primary is if anything conservative for a US target. Not adopted, because the
  US cells (S4 US ~118/arm) cannot carry a headline.
* **(d) S1 sample.** No `Complete == TRUE` filter: `Complete` records T3 completion, which is
  post-treatment relative to the T2 outcomes; conditioning on it would be conditioning on a collider.
  Listwise on the item only, per rule §4.
* **(e) `gligoric2025` restricted to conservatives (Ideology > 5)**, because only conservatives were
  randomised to messages (verified: 0 liberals in any message arm).
* **(f) `gligoric2025` duplicate item.** `trust_climate3` (climatologists / environmental scientists /
  meteorologists) is a subset of `trust_all35`; it is computed and stored but flagged
  `primary_item = False` and excluded from the pool. Its E_arm is +0.30 pp raw / -0.05 pp vs comparators,
  i.e. it does not change the C2n verdict.
* **(g) Which items are C2 rather than C3.** Applied strictly: only the item whose *proposition is the
  one the corrected number is evidence for*. So in `vlasceanu2024` the SciConsens arm's C2 is
  Belief.in.CC_1 ("Human activities are causing climate change") and the PluralIgnorance arm's C2n is
  Belief.in.CC_5 ("Climate change is a global emergency" — the exact statement the 65% norm was about);
  worry, threat, policy support and behaviour are all C3 and flagged `downstream = 1`.

**Recognition disclosure.** I recognise S2/S3 as the van der Linden gateway-belief experiments and S6
as the Voelkel climate megastudy, and I have some memory of their published headline effects. No
remembered value was used anywhere: every number in this file was recomputed from the vendored
microdata by the code in this session, and where a published number is adjacent (vdL 2019 consensus
+16.4 pp here) it is a coincidence of correct recomputation, not a transcription.

**pp conversion checked twice.** 1-7 Likert: raw x 100/6 = x16.667 (S3 belief raw +0.1425 -> +2.37 pp).
1-5 recode: x25 (S2 hcaused raw +0.2126 -> +5.31 pp). 0-100 slider: x1 (S3 consensus raw +16.42 ->
+16.42 pp). Every row of `assertion_train.csv` carries both `ate_raw` and `scale_range`, so the
conversion is auditable.

---

## 6. Downstream vs direct, and ceilings

* **Direct.** In every consensus study the corrected quantity (C1) and the own-belief item (C2) are one
  link apart: this is the gateway-belief first stage, and the C2 effect is *by construction* partly the
  downstream consequence of the C1 move. The C2 excess measured here is therefore **not** "an extra
  push on the belief item independent of the correction" — it is the total effect of having corrected Q,
  net of whatever the message does to everything else. That is the right object for an additive per-cell
  bump, but it means the bump and the arm's base effect are not cleanly separable in the data.
* **Downstream.** Worry, risk, policy support, behavioural intention and donation are all C3 and are the
  *reference*, not the target. They receive the arm's generic effect and no excess.
* **Ceilings.** The corrected item's control mean is high everywhere: S1 belief 89.6% of maximum, S4
  belief_climate_change 93.3%, S2 86.1%, S5a 77.1%, S3 75.1%, S6 65.2%. The two most-ceilinged studies
  give the smallest C2 excess in absolute terms (S4 +0.78) and the largest (S1 +2.08), so ceiling does
  not order the estimates — but the pooled +1.30 pp is measured in populations that are, on average,
  ~80% of the way up the item. The target's `belief_post` sits in the same regime; `trust_post` does not.

---

## 7. What this does NOT support

1. **It does not support any number for the Funding cell.** There is **no funding-correction arm anywhere
   in the train split**. Zero studies. `Funding x funding_perceptions` is classed C2 by the rule, and the
   only thing this measurement says about it is what the C2 pool says about C2 cells in general
   (+1.30 pp, CI [+0.71, +1.90]). It says nothing about whether a dollar-amount correction behaves like a
   scientific-consensus correction, and nothing at all about `funding_perceptions`, an item whose
   direction is reverse-coded in cleaning and whose control mean is unknown to me.
2. **It does not support a large C2n term.** The two social-norm arms give E_arm +0.09 pp (se 0.54,
   dof 1) and the one with the target's exact elicit-with-personal-feedback mechanic gives E_arm -0.46 pp.
   With k = 2 studies I cannot exclude +1 pp, but nothing in the train split *positively supports*
   anything above ~0.6 pp for `High public trust`.
3. **It does not support an elicitation premium.** +0.24 +/- 0.30 pp, confounded with estimator and design,
   and contradicted by the single personal-feedback arm.
4. **It does not transfer the C1 number to anything the benchmark scores.** The +9.4 pp C1 excess is
   large, real and irrelevant: the target scores no item asking for a corrected quantity.
5. **It is not a trust result.** Only one admitted study measured trust in scientists under a correcting
   arm (S4 `scientist_trust`, classed C3): **-0.05 pp (classic) and +0.71 pp (updated)** — i.e. a
   consensus correction moves trust in climate scientists about as much as it moves policy support, and
   both are the C3 baseline. The target's outcome family is trust, and this measurement is dominated by
   belief items.
6. **The estimands are not independent of the base effect.** E_out and E_arm subtract different things
   (the arm's own other outcomes; the other arms' effect on the same outcome). They agree here
   (+1.30 vs +1.02), which is reassuring, but if the entry's base effect for these arms is already
   estimated from the same family of studies, adding Ê(C2) on top risks double-counting the part of the
   base effect that is itself an average over consensus-type arms.
7. **k = 6 studies, dof 5.** Four of the six are consensus-message experiments from two research groups
   (van der Linden / Maertens / Većkalov / Geiger). The effective independence of the pool is lower than
   its dof suggests; the honest reading is "three design families" (classic consensus RCT, climate
   megastudy, norm-correction), not six independent replications.
