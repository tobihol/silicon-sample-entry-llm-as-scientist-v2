# idea_03 campaign log (operator: Haiwen)

Operator-side record. Lives in docs/, never mounted. Times UTC.

## 2026-08-27 — setup on Haiwen's machine

- `data/` from Tobi's data.zip; disk-only derived files rebuilt and verified byte-identical
  to the zip's carves (details: the four rebuild steps below). dablander halves sha256
  16/16 identical to the zip's index — the environment is provably Tobi-equivalent.
  - orchinik2024 + dablander2025: `idea_01/run/tools/build_*.py` in-container; built-in
    published-n checks all passed.
  - goldwert2026 texts: new `utils/heldout/build_goldwert_texts.py` (docx extraction;
    7 video-marked arms, matching the adapter's note exactly).
  - kerwer2025 derived: new `utils/heldout/rebuild_kerwer_derived.py` (microdata inversion,
    round-trip-checked).
- `setup_idea03.sh` green end to end. Container smoke test: 10 excluded datasets absent,
  inputs mounted, prime-agent 0.7.2 + claude 2.1.220 OK.
- Dockerfile fix: pre-create `/home/agent/.prime` agent-owned (docker made it root-owned as
  a mountpoint parent, so `/login` died with EACCES writing `.config.json`).
- One-command driver `run_idea03.sh` (repo root): preflight, oracle, session, audits;
  `login` / `token` / `login-callback` subcommands for the two credentials.

## 2026-08-27 — session 1 (run 20260827T194235Z_s1)

19:42Z start, ~20:04Z end (~22 min). All 14 scored calls spent within 15 min of first
submission: sub-1 honest/unshrunk on all 7; sub-2 = identical-file replication control on
the three reliable tasks (kim, dablander, altenmueller) + κ-damped magnitude test on the
four weak ones. Agent-declared mechanism test, not a retry. No refused events.

The wrapper process was killed at ~20:04Z (operator-side task stop), cutting the session's
final gate/refine step and run.sh's post-run stage. Recovered manually: frozen re-check
(intact), unsigned-prompt check (clean), ledger promotion (4 entries + 1 refinement),
best-effort after-snapshot, both audits (leak audit 101 files CLEAN; sibling scan 121
files, 0 hits). Deliverables complete: REPORT.md, DESIGN.md, OPEN.md, anchors/ (967
train-split cells), scoreboard.csv (14 rows).

### Environment defects the session surfaced (OPEN.md A1–A4), and fixes

| # | defect | fix (all operator-side; frozen defs untouched) |
|---|---|---|
| A1 | `/workspace/benchmark` EMPTY — template is a git submodule, never initialized on this machine (setup miss) | `git submodule update --init` → 546f928 checked out |
| A2 | briefs said "at most 5 submissions" (stale idea_02 text) vs frozen budget 2 | all 7 `task.json` corrected to "2 scored submissions per run id" |
| A3 | kerwer2025 scored twice against the SAME half (per-k hash collision, 1/16 per task) — violates the frozen fresh-draw promise | `pick_half` now draws without replacement per (run_id, task): k-th call takes the k-th entry of a seeded permutation; tested 0/600 collisions, deterministic |
| A4 | r_adj/r_within_adj exploded to ±10⁴ where half reliability ≈ 0 (orchinik) | null when reliability ≤ 1e-3, clamped to [-1,1] otherwise — matches organizers' adjusted_metrics NA + truncation |

Oracle restarted 20:08Z with the fixes. Already-written score files left as the record.

### SCAFFOLD §B adjudication (agent's question 3)

Both β rows are human-on-predicted regressions, but from different predictors on
different study families: "~1.5 unshrunk" is idea_01's analytic predictor on the slider
megastudies (cf. docs/heldout-pair-2026-08-25.md: sliders β≈1.6, trust batteries 0.63–0.68);
"κ0.85→β0.94" is idea_02's full pipeline measured once, blind, on bokemper2022. No
same-regression contradiction; no universal κ implied. The agent's refusal to import
κ=0.85 and its β = ρ·sd_true/sd_pred framing are consistent with the record.

## 2026-08-27 — session 2 (run 20260827T202417Z_s2) + continuation s2b

s2 launched 20:24Z on TASK_02 (operator answers to OPEN A1–A4/§B + benchmark inventory +
gate candidate). Spent all 14 scored calls by 20:33Z: k=1 = replication controls on the
reliable tasks (κ=1 under its own M1) + revised damping on the weak three — the likely
gate candidate set; k=2 = further κ-response variants (goldwert β now read at 0.32 / 0.73
/ 1.52 / 2.13 across four damping settings). A4 fix verified live (orchinik r_adj null;
altenmueller half 2 null). Cut at ~20:35Z, ~11 min in, mid benchmark inventory — second
wrapper-task kill, same signature as s1's. REPORT/DESIGN not yet updated by s2.

Recovery: s2 ledger promoted (3 entries + 1 refinement) BEFORE relaunch; TASK_02B
continuation brief written (budget rule: TASK_02's scored calls were spent under s2 — the
new run id's budget is not extra). **s2b relaunched 20:36Z DETACHED** (`SSB_DETACH=1`,
container c5f71a602407, run id 20260827T203601Z_s2b) so no operator-side process kill can
reach it; exec log followed via `docker logs -f` (re-attachable). Post-run steps (snapshot,
frozen re-check, ledger, audits) are skipped by detach mode — do manually at session end.

s2b completed naturally 20:53Z (17.5 min, exit 0, zero scored calls — per TASK_02B's
budget rule). Post-run recovered manually: frozen intact, no unsigned prompt files, ledger
promoted (7 entries + 2 refinements), audits CLEAN (139 files echo-audited; 225 scanned,
0 hits). Headlines: benchmark inventoried (distrust_post verified; funding_perceptions
sign trap found; donation/newsletter scale-range units correction — behavioural pair is
32/208 cells, "small" claim retracted); Section-2 honest floors delivered (24 files, exact
zero-interaction; environment returns no moderation feedback — recorded as A6); anchors C
(rank-1 structure, shrink band 0.15–0.35, target r_within ceiling ~0.53–0.64) and D
(control levels ~60–67, party gap −27 to −31 pp); target-entry harness built and validated
offline (`make check` PASS; i.i.d. synthesis-noise finding + mean-matching fix, 15×).

**First gate run** 20:55Z: candidate s2 sub-1 (M1w@κ0.5 + M3) vs baseline s1 sub-1 →
**REJECTED**, category "scientist credibility (framings)". Verdict+category relayed to the
agent via the gate file only; operator detail in eval/gate/ left unread (channel
discipline). Agent had pre-registered "0.5 is above the optimum" before the verdict.

**Session 3 launched 20:56Z detached** (run 20260827T205641Z_s3, container 07ec56594415),
TASK_03: gate interpretation + κ≈0.2 candidate, target-side anchor children (approved),
target table v1 as draft through the harness, team_id (team_31) provided.

## 2026-08-27/28 — session 3 (run 20260827T205641Z_s3) and the first promotion

s3 ran 20:56–22:08Z (72 min, exit 0, detached — no interference). Post-run: frozen intact,
clean, ledger promoted (10 entries + 3 refinements), audits CLEAN (176 echo-audited / 343
scanned, 0 hits). Headlines: gate-rejection diagnosed at mechanism level (M3's per-cell
exemption acted as an outcome reweighting silencing the credibility family) plus a proved
invariance theorem (study-uniform κ cannot move pearson_within); a chance identical-half
draw on beall gave the campaign's only noise-free comparison — new candidate beats
baseline (RMSE_adj −18.8%, r_adj 0.493→0.535); cal_beta verified actionable in both
directions (lands 1.00±0.05 on fresh halves); two-level amplitude decomposition
(beta_between 0.38/0.42, beta_within 0.150/0.153 in the many-variant regime — the target's
regime); three children (ANCHORS_E/F/G); target table v1 with real numbers, organizer
validator 40 pass/0 fail; variance-ratchet synthesis bug found and fixed.

**Gate #2** 22:10Z: candidate s3 sub-1 (M1w-v2: uniform κ=0.20, exemption removed) vs
baseline s1 sub-1 → **PROMOTED** (first promotion of the campaign). Verdict relayed via
the gate file only; eval/gate/ detail unread.

**Session 4 launched 22:10Z detached** (run 20260827T221047Z_s4, container 092fc6f9f3d2),
TASK_04: fold promotion into the durable method; target entry v2; ANCHORS_F judgement
call endorsed (exact-zero moderation floor for v1, rule stays pre-registered); 1–2
target-side children approved; itest explicitly declared out of session scope (operator
decision, with Tobi).

## 2026-08-28 — session 4 (run 20260827T221047Z_s4)

Ran ~38 min of compute across the night (laptop sleep froze container+VM clock mid-run;
resumed on wake, finished naturally, exit 0). Post-run: frozen intact, clean, ledger
promoted (13 entries + 3 refinements), audits CLEAN (201 echo-audited / 434 scanned, 0
hits). Headlines: r_adj noise scale calibrated via scale-invariance (free replications —
sd 0.002 at 204 cells, 0.082 at 22; R17 graded reading rule; retro-certifies the promotion
at 9σ/44σ); pre-registered mix experiment (PREREG_sub2.md) returned a clean 17σ/28σ
NEGATIVE with opposite signs across tasks → **M5 self-rejected, NO gate candidate
declared** (R18 now forbids the level-reweighting family); the instrument then caught
target entry v1 contradicting the promoted method (mix 1.002 vs promoted ~0.15, caused by
oversized ASSERTION_MATCH cells; R20) → **entry v2** rebuilt, every change evidenced, mix
0.247, validator 40/0; ANCHORS_H (arm ordering unvalidatable on train — s(a) honest-weak,
LOSO r = −0.37) and ANCHORS_I (donation is a lottery → $4.40 level; binary base-rate
correction) both moved the entry. 9/14 scored calls used, 5 declined with reasons.

Its §6 self-assessment names what separates the arm from a deposit-grade entry:
(1) ASSERTION_MATCH scale set by argument, not measurement — it designed the isolating
validation question for next session; (2) A13, the unpredictable mix parameter; (3) s(a)
carried flat-ish at low amplitude as a posture. No operator actions requested beyond 1–2
children next session.

## 2026-08-28 — session 5 launched; itest fork launcher built

s5 (TASK_05: the assertion-match isolation question the agent designed; 2 children for
A13/A14; entry v3 if warranted) launched 06:07Z detached (run 20260828T060726Z_s5).

**Build item #1 done:** `utils/prime/fork_eval3.sh` — idea_03 itest fork launcher, adapted
from fork_eval.sh, dry-run validated (brief-only copy asserted; auto-refine off; ten-dataset
exclude; scored by score_oracle3 --itest into idea_03/eval/itest/ only; refuses to fork
mid-session).

**Finding for Tobi:** fork_eval.sh line 54 copies `"$ITEST_BRIEF/.."` — the whole
`data/bbprime2025/carved/` directory, which on this machine contains the SEALED truth.csv
and microdata.csv, into the fork's run tree. If idea_02's five archived forks contain
those files, the idea_02 itest scores need an asterisk (the declining curve suggests the
agent never used them, and transcripts can confirm, but the fork's own leak audit ran with
`--exclude bbprime2025` so it would not have flagged it). Check the archived forks on the
original machine: `ls .container-state/forks/idea_02/*/run/runs/*/itest/bbprime2025/`.
fork_eval3.sh copies brief-only and hard-asserts it.

## 2026-08-28 — session 5 (run 20260828T060726Z_s5) + gate #3

s5 ran 06:07–06:49Z (42 min, exit 0). Post-run: frozen intact, clean, ledger promoted
(9 entries + 3 refinements), audits CLEAN (230 echo-audited / 538 scanned, 0 hits).
Headlines: pre-registered AM-ISO experiment (PREREG_AM.md fixed before scoring) — content
targeting beats generic ordering **4/4**, clean reads beall +0.205 (12.6σ) and goldwert
+0.216 (its own promoted table as the control); first mechanism that never flipped sign.
Self-correction: r_adj is affine-invariant → s4's noise table under-counted classes;
s4's mix result downgraded to 5.3σ/0.8σ and "opposite sign" retracted (decision LAM_BTW=1
unchanged) — recorded in the prereg BEFORE this run's own reads. Entry v3: message
direction toward targeting at unchanged amplitude; donation_ams +0.05 → −0.70 with
across-arm SD 0.000 (ANCHORS_K's direct/indirect decomposition, −2.5 offset replicated
twice). ANCHORS_J closed A13 negatively (no out-of-sample mix predictor exists; asymmetric
loss favors low mix). 11/14 calls used, 3 declined with reasons.

**Gate #3** 06:51Z: candidate s5 sub-1 (M10 targeting allocation) vs baseline s3 sub-1 →
**REJECTED**, category "donation/behavioral outcomes". The agent pre-registered the
interpretation: candidate never hurt but differed materially only on the two lowest-power
tasks; the matched-amplitude AM-ISO measurement stands as primary evidence independent of
the gate. Open tension for next session: v3's A_MULT/S_MULT derive from unpromoted M10 —
the agent must reconcile that with the techniques-persist-through-the-gate rule (its A18
already flags it).

## 2026-08-28 — session 6 (run 20260828T074119Z_s6): the self-audit session

s6 ran 07:41–08:20Z (39 min, exit 0). Post-run: frozen intact, clean, ledger promoted (16
entries + 3 refinements), audits CLEAN (267 echo-audited / 600 scanned, 0 hits).

Headlines: **A18 resolved by reverting** (A_MULT/S_MULT back to the promoted state; R27:
gate governance follows the evidence base — validation-sourced constants revert on
REJECTED, train-sourced ones don't); two scored calls spent purely on instrument
calibration **retracted its own 12.6σ headline to 2.2σ** (beall's identical table returned
0.401 vs 0.535/0.543; noise table re-pooled; s4's mix probes now two nulls); the AM-ISO
saturation curve shows v3's direction change was worth +0.008 r_adj. ANCHORS_L closed A16
negatively (no mechanical targeting map validates; content targeting is a substitute for
the rank-1 loading, not a complement — and cannot explain a behavioral failure family,
2/39 cells). ANCHORS_M: recipient alignment real (+4.29±0.61, 7.1σ); donation −0.70→−0.40
with loading restored (0.997) — v3's exact zero was a floor artefact. **Entry v4** = the
promoted state + train-sourced updates; no gate candidate by design; validator 40/0.

**The declaration (REPORT §6): "Yes — this is the method and the entry I would stand
behind as-is"**, with one named contingency: **A22** (absolute pp size of
elicit-and-correct effects; if ~0.2 pp instead of 0.7–1.0, the entry's two largest cells
are 3–5× too big and it wants v5 before any deposit).

**Operator consequence:** since the frozen rule is "no prediction changes after an
internal-test score, ever", A22 must be resolved BEFORE the blind shot — s7 (one child,
A22) is the prerequisite of the itest, not an optional refinement.

## 2026-08-28 — session 7 (run 20260828T082705Z_s7): A22 closed, the declaration is unconditional

s7 ran 08:27–09:04Z (38 min, exit 0). Post-run: frozen intact, clean, ledger promoted
(8 entries + 3 refinements), audits CLEAN (292 echo-audited / 639 scanned, 0 hits).

A22 closed by measurement, opposite to the named risk: elicit-and-correct effects on
belief-class items = **+1.30 pp** (se 0.23, 6 studies, LOSO stable; verified line-by-line
against raw microdata) vs the entry's authored 0.86 — the assertion term was 51% too
SMALL. The transferable finding is the item-class taxonomy (R30): corrected-quantity items
+9.4 pp (target scores none), belief-class +1.30, else 0 — a term sized on the wrong class
would have been 7× too large. The pre-registered two-sided rule (PREREG_S7, fixed before
the child launched) fired against the session's own expectation: A_MULT 0.40 → 0.55,
capped by the validation-sourced mix band. **Entry v5**: one constant moved, nothing else;
mix 0.293 (band [0.15, 0.30]); validator 40/0. Zero scored calls, zero model calls.
Exposures A24–A26 named at full size and accepted, not conditioned on.

**The declaration (REPORT §6), unconditional: "Yes. This is the method and the entry I
stand behind."** Final candidate = entry v5 / the standing method in DESIGN.md §12.6.

**Campaign state: ready for the internal test.** fork_eval3.sh validated; blind-currency
discipline (≤2 bbprime evaluations, final candidates only) satisfied — this is the final
candidate. The itest go/no-go and the third-deposit question are the operators' (Haiwen +
Tobi), against the pre-registered bar: ≥ idea_01's 0.45–0.47 band + 0.08 r-within,
matching directional agreement. After an itest score: no prediction changes, ever.

## 2026-08-28 — THE INTERNAL TEST (blind shot #1 of 2)

Fork taken 11:31Z via fork_eval3.sh dry-prep (all gates passed: no running container,
main-tree name scan clean, brief-only copy asserted — 7 design-only files); session
launched detached 11:32Z, exited naturally 11:46Z (14 min). The agent applied the standing
method verbatim (regime: many-variant; κ=0.20 promoted; LAM_BTW=1.00; exact-zero
moderation floors on all five companions), full coverage verified cell-for-cell, one
submission ever. Sealed score written 11:46Z → **idea_03/eval/itest/score_1.json —
UNOPENED** (submission sha 689f1ba2…). Fork leak audit: 296 files CLEAN. Fork archived
read-only. Main tree post-scan: 0 hits.

**As of 11:46Z the no-prediction-changes rule is in force: entry v5 is frozen forever.**
Unsealing the score = the deposit decision (bar: r-within ≥ idea_01's 0.45–0.47 band
+ 0.08, matching directional agreement). One blind bbprime evaluation remains in the
budget. Decision owners: Haiwen + Tobi.

## 2026-08-28 — UNSEALED (operator decision, 11:58Z local 13:58): THE BAR IS CLEARED

score_1.json opened by Haiwen's instruction. Section 1 (408 cells, full truth):

| metric | idea_03 blind | reference |
|---|---|---|
| **pearson_r_within_outcomes** | **0.6159** | idea_01 frozen blind band 0.45–0.47; bar = band + 0.08 (≈0.53–0.55) |
| directional_agreement | 0.6740 | idea_01 in-sample practice on same task ~0.687–0.700 (Δ within 1 SE ≈ 0.023) |
| r_adj | 0.5300 | truth reliability 0.750 |
| cal_beta | 1.465 | κ=0.20 over-damps amplitude on this task; correlation unaffected |
| vs floors | dir +0.174 / RMSE +0.45 pp (no-effect); dir +0.096 / RMSE +0.30 pp (all-positive) | beats both |
| Section 2 subgroups | r ≈ 0 / dir ≈ 0.5 | the honest exact-zero floors, as designed |

**Verdict: r-within +0.146 to +0.166 over idea_01's blind band — clears the
pre-registered ≥ +0.08 bar with margin (~3.7 SE over the band, ~1.6 SE over the bar
top), with matching directional agreement.** Context: idea_02's five blind forks ran
0.48 → 0.43 on this same anchor; idea_03's single blind shot: 0.616.

idea_03 qualifies as a third-deposit candidate under the pre-registered criterion. The
deposit itself (template clone, v5 package, Zenodo, deposit email by Aug 31; primary
remains idea_01 target-04) is Haiwen + Tobi's to execute. The second blind bbprime
evaluation remains unspent — the criterion is met; spending it is not required.

### Open operator items

- track_progress.py doesn't parse idea_03 sessions yet (0 rows) — adapt when convenient.
- Gate not yet run: needs a candidate run vs baseline (session 2's job to produce).
- Session-1 exec log: idea_03/eval/20260827-s1_exec.log (23.5MB, 5268 events).

## 2026-08-28 — bokemper2022 head-to-head (Tobi's request)

Symmetric h2h on the post-s7 frozen state, same protocol as 08-26: fork, one session
(12:16–12:27Z, 11 min), brief-only asserted, one submission + moderator floors, zero model
calls, audits CLEAN, fork read-only. Scores (55 cells): dir 0.709 / RMSE 2.04 / r 0.206 /
β 0.94 (r-within declared uninformative here). idea_01 still leads off-family (0.764/1.80/
0.336/1.06); idea_03 second with the best calibration; idea_03 > idea_02 across the board.
Recognition asymmetry disclosed (idea_03's agent recognised the published study; memory not
used per frozen defs; idea_01's 08-26 probe was UNRECOGNISED). Paired per-cell test needs
the original machine's prediction files — flagged to Tobi. Full write-up:
docs/heldout-h2h-idea03-2026-08-28.md.
