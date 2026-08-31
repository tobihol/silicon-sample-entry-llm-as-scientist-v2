# TASK_03 — after the first gate verdict

Sessions s2+s2b's REPORT.md was read in full. Operator answers first.

## Operator answers (REPORT §7, OPEN A5–A8)

1. **The gate has run.** Verdict and failure category are in
   `runs/20260827T202417Z_s2/gate_m1w-k05-m3.json` (candidate s2 sub-1, baseline s1
   sub-1, with your n=2 caveat carried). The category named there is everything the
   environment discloses; no further detail exists on your side of the boundary.
2. **team_id: `team_31`** (registration confirmed by the organizers). Every other deposit
   identity field (contact, repo metadata, DOI wiring) stays operator-side at packaging
   time — nothing else about packaging is yours to carry.
3. **Companions (A6): correct as observed.** This environment's scorer returns Section-1
   diagnostics only, by design, and that will not change. Note the distinction: the real
   benchmark *does* score the moderator file (subgroup analyses), so an honest-floor
   companion remains a real prediction worth carrying — it just earns no feedback here.
4. **A8: correct and known.** Halves cannot repeat within a (run id, task); across run
   ids they can recur — the pool is 16 per task. Treat cross-run recurrences as what they
   are: an exact replication read, free of charge.
5. **Budget approved:** 2–3 `rlm()` children, target-side, as you proposed (outcome-level
   profile anchors in the target's own 13 outcomes; party × message-family moderation
   prior; control-condition response-shape library for Section 3). Same scoping rules as
   before. Still nothing for `claude -p` without asking.

## This session

1. **Interpret the verdict at mechanism level** — the category is all you get — and
   produce the next candidate you already pre-registered: κ ≈ 0.2 in the M1w
   parameterisation, or a revision you can defend *before* seeing any score. New run id,
   2 scored calls per task, spent as questions, as always. Declare in REPORT.md exactly
   what the next gate run should be (candidate run id, baseline run id, k).
2. **Target-side anchors** with the approved children (§ answer 5).
3. **Target table v1 — real numbers, as a draft.** Run your structural model + anchors
   through `tools/target_entry.py` end to end: 17×13 table, synthesis, `verify()`
   max-error report, validator. Mark it a draft in REPORT.md. No deposit actions — the
   operator packages separately, and no target numbers are final until the campaign's
   pre-registered bar is met.
4. **Report** as always: REPORT.md rewritten, DESIGN.md updated in place, OPEN.md moved
   forward.

Budget for this session: the launcher's defaults.
