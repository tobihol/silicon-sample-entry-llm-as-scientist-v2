# TASK_02 — the target enters the frame

Session 1's REPORT.md and OPEN.md were read in full. Answers first, then the session.

## Operator answers (OPEN.md §A–§D)

1. **A1 fixed.** `/workspace/benchmark` is now mounted: the official template at its
   pinned commit — survey instrument, the 16 intervention texts, codebook, validator.
2. **A2 fixed.** All seven `task.json` briefs now state the true budget: 2 scored
   submissions per task per run id.
3. **A3 confirmed — a defect, now structural.** Your two kerwer2025 calls were scored
   against the same half (a per-submission hash collision). The scorer now draws halves
   without replacement within a (run id, task), so the fresh-draw promise holds by
   construction. Read your kerwer sub-2 deltas as measuring only your damping, never a
   re-rolled half.
4. **A4 fixed.** Where a half's truth reliability is ≤ 0.001 the scorer now returns
   `null` for r_adj / r_within_adj instead of extreme finite numbers, and clamps both to
   [-1, 1] otherwise — matching the organizers' own NA-and-truncate behavior.
5. **SCAFFOLD §B resolved.** Both rows are human-on-predicted regressions, but from
   different predictors on different study families: the "~1.5 unshrunk" is the idea_01
   analytic predictor on slider megastudies; the "κ 0.85 → β 0.94" is the idea_02
   pipeline measured once, blind, on a held-out two-experiment study. No same-regression
   contradiction, and no universal κ implied. Your β = ρ·sd_true/sd_pred framing is
   consistent with the historical record; treat SCAFFOLD's row as history, not a default.
6. **Budget approved:** 2–4 `rlm()` children for train-split anchor extraction, scoped as
   in session 1. Still nothing for `claude -p` without asking first.

## This session

1. **Inventory the benchmark for real.** Everything DESIGN.md §4 says about the target
   was inferred without it. Re-derive the target picture from the actual instrument, the
   16 texts, the codebook and the validator; verify or retract your two "free mechanical
   corrections" (`distrust_post` valence; re-asked compression) against the real
   codebook; record every place the mounted truth changes a §4/§5 inference.
2. **Fresh validation budget** (new run id, 2 scored calls per task). Spend them as
   questions, as before. The Section-2 honest-floor companions you flagged in OPEN §E
   (marginal ATE repeated in every subgroup cell) are worth submitting alongside — they
   cost no extra scored calls and buy the moderation-reliability read you wanted.
3. **Produce a clean gate candidate.** A full 7-task `submission_1` set under this run id
   embodying exactly the mechanism set you want tested — your M1@κ0.5 + M3 proposal, or
   its revision after seeing the benchmark. State in REPORT.md precisely which mechanisms
   the candidate embodies and which (candidate run id, baseline run id) the operator
   should hand to the gate. The gate tests transfer; keep the candidate one coherent
   mechanism set, not a bundle of unrelated changes.
4. **Anchors:** extend with the approved children where it serves 1–3 (your named
   targets: TISP control levels for the 12-item trust scale, Pew party/race trust gaps,
   the interaction-vs-rank-1 share of a megastudy ATE table).
5. **If time remains:** draft the *structure* of a Tier-1/Tier-2 target entry —
   file formats against the validator, the synthesis path, where each number would come
   from — with no final numbers. No target prediction is submitted this session.
6. **Report** as before: REPORT.md for an operator who was away, DESIGN.md updated in
   place, open items in OPEN.md.

Budget for this session: the launcher's defaults.
