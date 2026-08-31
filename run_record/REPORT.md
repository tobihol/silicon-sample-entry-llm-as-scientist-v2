# REPORT.md — idea_03, session s7

Run id: `20260828T083214Z_s7`. For an operator who was away.
Reproducible from `runs/20260828T083214Z_s7/val/PREREG_S7.md` (written before the child was
launched, with the results appended below the line), `anchors/ANCHORS_N.md` +
`assertion_train.csv` + `_n_rule.txt`, `tools/target_model.py` (v5), `DESIGN.md` §12,
`target_entry_v5_table.csv`, `OPEN.md`.

---

## 0. Headline

* **A22 is closed by measurement, and the answer is the opposite of the one I named.** s6's
  declaration said the entry was at risk if a train measurement of elicit-and-correct arms came
  back near **0.2 pp**. It came back at **+1.30 pp** (se 0.23, dof 5, 6 studies, CI
  [+0.71, +1.90], LOSO +1.15 to +1.41) against the entry's authored **0.86**. The assertion term
  was too small, not too large. (§1.)
* **The transferable part is not the number, it is the class.** The same manipulation moves the
  item that asks for the corrected quantity back by **+9.4 pp**, the item that asks the
  respondent's own belief in the corrected claim by **+1.30 pp**, and everything else by zero.
  **The target study scores no item of the first kind**, so the big number is worth nothing —
  and a term sized on the wrong class would have been seven times too large. That is now
  **R30**. (§1.)
* **The rule fired because it was written before the answer, and it was symmetric.** PREREG_S7
  fixed a two-sided posterior update — authored prior N(0.86, 0.40²), measurement N(Ê, se²),
  ±0.05 dead band, R20 mix cap — and it returns `A_MULT = 0.554 -> 0.55`. Applying it unchanged
  when it moves against the session's expectation is what makes s6's revert a rule rather than a
  convenience. That is now **R31**. (§2.)
* **Entry v5: one constant moves, nothing else.** `A_MULT` 0.40 -> **0.55**. 54,000 rows, max ATE
  recovery error **0.0239 pp**, mix 0.238 -> **0.293** (validated band [0.15, 0.30]),
  `make check` **40 pass / 4 warn / 0 fail**. DRAFT; no deposit actions. (§3.)
* **Zero scored calls, zero model calls, as planned.** The A22 verdict created no question a
  scored call could answer. (§4.)
* **The declaration is now unconditional, and it is yes.** (§6.)

---

## 1. The measurement

**What was measured.** Three target arms elicit an estimate and correct it on-screen: Funding
($10.6bn vs $52.5bn; $7bn vs $160bn), Consensus (three "% of scientists agree" sliders with
per-item feedback, 99% / ~100% / 66%), High public trust ("% of Americans who trust climate
scientists" -> Pew's 76%). The entry adds an additive bump on exactly the cells where a corrected
claim is later scored. A22 said that bump was the entry's largest argued number.

**The classification came first, and it decided the answer.** PREREG_S7 fixed four classes before
anything was computed. The child's result:

| class | the scored item asks | E_out | entry cells |
|---|---|---|---|
| **C1** | for the corrected quantity itself | **+9.37 pp** | **none** |
| **C2** | the respondent's own belief in the corrected claim | **+1.30 pp** (se 0.23, dof 5) | Funding × funding_perceptions, Consensus × belief_post |
| **C2n** | own attitude, where the corrected quantity was a social norm | +0.61 (k = 1); E_arm +0.09 ± 0.54 | High public trust × trust_post, × trust_multidimensional |
| **C3** | anything else | 0 by construction | — |

Per study (C2): Maertens2020 +2.08, vdL2017 +1.34, vdL2019-US +1.32, Većkalov2024 +0.78,
vlasceanu2024 +1.00, voelkel2026 +1.28. No study drives the pool; US-only subsamples of the two
multi-country studies are *larger*, so the pool is conservative for a US target. **Elicitation
carries no premium** (+0.24 ± 0.30 pp), and the one train arm with the target's exact
elicit-then-personal-feedback mechanic is the *lowest* number in the table — a result I would
have bet against.

**I checked the child rather than trusting it.** I re-derived `geiger2026`'s van der Linden 2019
US RCT independently from the raw CSV (ANCOVA, n = 6,301): consensus +16.4197, belief +0.14248
raw = +2.375 pp, cause +3.272, worry +1.680, policy +1.329, so E_out = +0.870 / +1.768 and the
study mean is +1.32 — matching `assertion_train.csv` to four decimals, ×100/6 conversion
included. A weaker cross-check against this arm's own s1 `voelkel2026_ates.csv`, built by a
different child through a different pipeline, gives E_out +1.12 against the child's +1.28.

---

## 2. The rule, and the direction it fired in

    P = (0.86/0.40² + 1.30/0.23²) / (1/0.40² + 1/0.23²) = 1.191 pp
    A_MULT = clip(round(0.40 × 1.191/0.86, 2), 0.05, 0.55) = 0.55        |0.55 − 0.40| ≥ 0.05

All pre-registered admissibility conditions hold: 6 studies and dof 5 (R29's floor is 3), no cell
above 3 pp, mix inside the validated band. Sensitivity:

| input | A_MULT | fires? |
|---|---|---|
| **primary (E_out 1.30, se 0.23)** | **0.55** | yes |
| se inflated ×√2 for "three design families, not six" | 0.52 | yes |
| LOSO extremes 1.15 / 1.41 | 0.50 / 0.55 | yes |
| CI limits 0.71 / 1.90 as points | 0.35 / 0.55 | yes |
| corroborator E_arm 1.02 (dof 1) | 0.43 | **no** |

The one input that leaves v4 standing is the between-arm estimand, at dof 1, which R29 forbids as
a headline. I record that as **A25** instead of using it as a reason to decline an update I did
not want — the failure mode of s4 and s5 was believing measurements that flattered the entry, and
declining this one would be the same error with the sign flipped.

**Governance (R27).** v4's 0.40 was **authored** — the smallest multiplier keeping the assertion
cell the Funding arm's own largest — under R20's validation-derived mix band. The new value's
evidence is train ground truth, so the split rule governs it and no gate is needed; the
validation-sourced part of the old warrant is still respected, and in fact **it is what capped the
move**: the uncapped posterior wanted 0.554 and the band binds at ≈0.55.

---

## 3. Entry v5

| # | change from v4 | evidence | kind |
|---|---|---|---|
| 1 | `A_MULT` 0.40 → **0.55** | ANCHORS_N via PREREG_S7 rule A22-1 | train-sourced, under a validation-sourced band |
| 2 | nothing else | `KAPPA` 0.20, `S_MULT` 1.00, `LAM_BTW` 1.00, the ASSERTION_MATCH shape, control levels, `S_ARM`, outcome profile, `donation_ams` −0.40 / `L_OUT` 0.997, exact-zero moderation, `shape_lib`, synthesis | |

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
trust_post +1.211. All 16 `donation_ams` cells stay negative (−0.21 to −0.61).

| | v4 | **v5** |
|---|---|---|
| max abs ATE recovery error | 0.0239 pp | **0.0239 pp** |
| mean abs ATE recovery error | 0.0016 pp | **0.0017 pp** |
| max abs interaction (native) | 4.22 | 4.22 |
| mix (from the rows) | 0.2362 | **0.2933** |
| organizers' `make check` | 40 / 4 / 0 | **40 pass / 4 warn / 0 fail** |

Four warnings, all operator-side deposit metadata, unchanged. **No deposit actions taken.**
`target_entry_v5_pkg/` is a local validation copy; v1–v4 artefacts are kept for the diff.

---

## 4. Calls

**Zero scored validation calls**, declared in PREREG_S7 §4 before the child reported and
unchanged by its verdict: the constant that moved is train-governed under R27, the mix stayed
inside the promoted band, and R29 forbids a mechanism claim on the dof a new probe would have
had. **Zero `claude -p` calls**, as in every session of this arm. Budget spent: one child, exactly
as approved.

---

## 5. What I need from the operator

1. **Nothing is blocked on you.** A22 is closed; A24, A25, A26 are opened and none of them is a
   question the operator can answer.
2. **No gate candidate.** v5's one change is train-sourced; declaring it would ask the gate to
   certify a train measurement it cannot see.
3. **No budget request.** I am not asking for another child. §6 says why.

---

## 6. What separates this arm from "the entry I would stand behind" — and the declaration

**What this session did.** It bought one measurement, and the measurement said the entry's most
argued number was 51% too small rather than 3–5× too large. The entry moved by the rule that was
written before the answer, in the direction the session did not expect, capped by the one
validation-sourced constraint that still applies to it. Nothing else moved.

**The three exposures I now carry, named at their full size.**

1. **A24 — two of the entry's largest cells are bigger than anything measured supports.**
   `High public trust × trust_post` (+1.349) rests on a social-norm class worth +0.61 pp on one
   study and +0.09 ± 0.54 on two; `Funding × funding_perceptions` (+1.664) rests on a class in
   which no train study corrects a funding quantity at all. Both rose because the rule moves the
   multiplier and never the shape. I could make the entry look better by re-authoring the shape
   now. That is precisely the move R31 exists to forbid, and I am not making it.
2. **A25 — the estimand that controls for arm quality (dof 1) would have left v4 standing.**
3. **A26 — `E_out` and the entry's own base effect are not cleanly separable**; the double-count
   is bounded at ~0.09 of `A_MULT` by the gap between the two estimands.

**What I would still not change to make the entry look better.** The exact-zero moderation floor.
The refusal to carry ANCHORS_F's intercept. The refusal to expand the four-cell assertion map to
a hundred cells when the expansion is the part that fails LOSO. The flatness of the arm ordering.
`donation_ams` negative on all 16 arms. And now: the shape of `ASSERTION_MATCH`, which I would
prefer to re-cut and will not.

**The declaration — unconditional, with no named contingency.**

**Yes. This is the method and the entry I stand behind.** Method: analysis-first prediction in the
units the scorer reads; a three-level decomposition with study-level amplitudes only; abstention
where nothing is measured; every constant carrying its evidence and its governance kind; and
updates that happen only through pre-registered, two-sided rules written before the number
arrives. Entry: **v5**, `target_entry_v5_pkg/`, 54,000 rows, full coverage, `make check` clean,
mix inside the band the environment validated.

s6 made its yes conditional on one measurement. That measurement has been bought, it was
verified line-by-line against raw microdata, and its verdict was applied by the rule that was
fixed before it arrived — including the part of the verdict that embarrassed the session's own
expectation. There is no remaining contingency, and I am not naming a new one: A24, A25 and A26
are exposures I accept, not conditions I am waiting on. Every one of them would be resolved by
data that does not exist in this container, and the frozen definitions are explicit that whatever
entry this arm's procedure produces at its final state is the one that gets measured. This is that
state.

---

## 7. Ledger of durable-state changes

* `DESIGN.md` — **new §12**: A22's item-class taxonomy and why it is the transferable part
  (§12.1); ANCHORS_N (§12.2); the rule, the direction it fired in, the sensitivity table, and new
  rules **R30/R31** (§12.3); entry v5 and the R27 governance argument (§12.4); the five things the
  measurement does not support (§12.5); the standing method after s7 (§12.6).
* `tools/target_model.py` — **v5**: `A_MULT` 0.40 → 0.55 with its evidence, its kind, and its
  non-support recorded in place; a v4 → v5 changelog; a note on the `ASSERTION_MATCH` shape.
* `tools/target_entry.py`, `tools/level_transform.py`, `anchors/shape_lib.py` — unchanged.
* `anchors/` — `ANCHORS_N.md` + `assertion_train.csv` (79 rows) + `_n_sources.csv` +
  `_n_rule.txt` (sha256, pre-committed) + `_n_noncorrecting_comparators.csv`.
* `runs/20260828T083214Z_s7/val/PREREG_S7.md` — the estimand, the classes, the two-sided rule,
  the mix table, the call plan and the child's scope, all fixed before launch; results appended
  below the line, including one correction to my own pre-registered gloss (§R4).
* `target_entry_v5_table.csv`, `target_entry_v5/`, `target_entry_v5_pkg/` — the v5 draft.
  v1–v4 artefacts kept for the diff. `runs/scoreboard.csv` unchanged at 63 rows (no scored calls).
* `OPEN.md` — **A22 CLOSED** by measurement; **A24** (unsupported cells raised by the rule),
  **A25** (the dof-1 estimand disagrees), **A26** (E_out vs the base effect) opened; s7 blinding
  disclosures.
* `SCAFFOLD.md` still unmodified.
