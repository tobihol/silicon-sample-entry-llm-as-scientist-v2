# run_record/ — the loop's recorded output

The method is the start state of the agent loop — frozen instructions, launch budgets,
oracle and gate — in the code repository (registration K.1). This folder is what the loop
produced, and the record of how:

- `target_model.py` — the predicted table: outcome-level base effects, low-rank message loading,
  sparse assertion-match terms; constants with their evidence and governance kind in the docstring
  (v5 = v4 with `A_MULT` 0.40 → 0.55 under `campaign/…PREREG_S7.md`).
- `target_entry.py`, `level_transform.py` — backward synthesis of the Tier-1 rows
  (`--exact --n-control 6000 --n-intervention 3000`) and unit transforms; `verify()` recomputes
  every ATE from the rows (max error 0.024 pp).
- `target_entry_v5_table.csv` — the 17 × 13 effect table the rows encode (pp of scale range).
- `DESIGN.md` (agent's design record, sessions s1–s7), `REPORT.md` (final session report),
  `OPEN.md` (open items, blinding disclosures per session).
- `prompts/` — the frozen system prompt (`APPEND_SYSTEM.md`, sha256 in `frozen.sha256`), the
  non-binding scaffold, and the per-session task briefs.
- `anchors/` — narrative anchor notes (`ANCHORS_A…N.md`) and **aggregate** tables extracted from
  the train split. Respondent-level extracts from restricted sources were not copied. Aggregates
  derived from Pew Research Center ATP, GSS (NORC), ANES, Yale/GMU CCAM and TISP data appear in
  `levels.csv`, `_headroom.csv`, `party_headroom_gaps_by_construct.csv`; those organisations bear
  no responsibility for the analyses or interpretations here.
- `campaign/` — validation scoreboard (63 scored calls), the three gate verdicts, the
  pre-registrations (`PREREG_AM`, `PREREG_S6`, `PREREG_S7`), and the operator's campaign log.

The environment (oracle, halves carver, gate, launcher) is in the code repository under
`utils/heldout/` and `utils/prime/`; the organizers' scoring code was mounted read-only from
their repository at commit `b25667b2` and is not redistributed.
