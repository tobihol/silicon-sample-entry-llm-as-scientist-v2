# TASK_02B — continuation of TASK_02 after an operator-side interruption

Session s2 (run `20260827T202417Z_s2`) was cut off ~11 minutes in by an operator-side
process failure — nothing you did, and nothing about the environment's rules. Its 14
scored calls stand; the score files are under `runs/20260827T202417Z_s2/val/`. You were
mid-way through the benchmark inventory when it stopped.

TASK_02 is unchanged; this session completes it. One budget rule on top: **TASK_02's
scored-call budget was already spent under s2.** This run id's fresh budget is not extra —
submit a scored call only if a specific question cannot be answered any other way, and if
you do, name that question in REPORT.md.

Everything else as TASK_02 specifies, from where s2 left off:

1. Finish the benchmark inventory; verify or retract DESIGN §4's target inferences
   (including the two "free mechanical corrections") against the real instrument,
   codebook and validator.
2. Declare the gate candidate: state in REPORT.md whether s2's `submission_1` set is the
   candidate, exactly which mechanisms it embodies, and which (candidate run id, baseline
   run id) the operator should hand to the gate.
3. Section-2 honest-floor companions, anchors extension (the approved 2–4 `rlm()`
   children), and the target-entry structure draft, as TASK_02 §§2, 4, 5.
4. Report: REPORT.md rewritten for this session, DESIGN.md updated in place, OPEN.md
   items closed or added.
