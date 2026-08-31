# Silicon Sample Benchmark — method registration form

Fill in every item before the prediction lock; this file ships inside your repo's Zenodo release
(see the README's *Deposit* step). This form covers **one entry** (one repo / one Zenodo release,
`primary` or `secondary-k` — see the README's *What counts as a submission*); if you submit several
entries, fill one form per entry. Items marked **★**
must be disclosed **fully publicly** (never escrowed or withheld). Items marked **†** must be at
minimum escrowed — they may be sealed from the public, but never withheld from the core team. Items
not applicable to your approach: write `N/A`. When several models serve different pipeline stages, complete the model
sections (B) once per model. See the call's *Disclosure policy* for escrow rules.

---

## 0 · Approach identity and output
- **0.1 Team ★** — team_31. Registered members: Tobias Holtdirk (LMU Munich, corresponding contact: tobias.holtdirk@lmu.de) and Bolei Ma (LMU Munich). Contributor, not a registered member: Haiwen Huang (MPI-IS).
- **0.2 Plain-language summary ★** — Dataset acquisition → agent loop → derivation of individual-level rows. The predictions are analysis-first: the loop predicts the study's published analysis table — the 16 × 13 table of treatment effects, the control-condition levels, and the response distributions — and the individual-level rows are synthesized backwards from it, so that re-running the benchmark's analyses on the rows reproduces the table. The loop has a free strategy and externally administered testing. No restriction on how the agent makes predictions: it is free to use scripts, simulator calls, or anything else. The restrictions sit on information instead: there are held-out data that are excluded from its container, and feedback comes only through an oracle (only 2 submissions per study allowed). Its outcome was to write and fit an explicit structural model on a train split of eleven published message experiments. No human wrote or edited any predicted number.
- **0.3 Submission tier & approach family ★** — Tier 1. Family: direct forecasting (analysis-level effect forecast; no per-respondent simulation, no survey walk-through); autonomous agent, single model (scoped sub-agents of the same model); literature-conditioned (structural model fitted on published experiments and survey aggregates).
- **0.4 Pipeline diagram** — dataset acquisition → prime-agent loop → derivation of individual-level rows → `predictions/team_31_T1_primary_v1.csv`.
- **0.5 Coverage ★** — 208 predicted cells = 16 interventions × 13 outcomes, all 17 conditions present, every cell exactly once, no NA.

## A · Scope of LLM use
- **A.1 Purpose** — N/A
- **A.2 Degree of automation ★** — Fully automated; no human in the loop at prediction time.

## B · Model / system details (once per model)
- **B.1 Model name(s)** — `claude-opus-5` (Anthropic), as an autonomous agent via Prime Agent 0.7.2 (release pinned in `utils/prime/Dockerfile`) over the Claude Code CLI 2.1.220. Every session's launch snapshot and event log records the model id, for the main agent and the sub-agents alike; no other model was called.
- **B.2 Access & context mode** — Subscription login (no API key), agentic chat sessions in a Docker container with the repository mounted: seven main sessions 2026-08-27 → 2026-08-28, one internal-test fork and one head-to-head fork 2026-08-28 (run ids: `run_record/campaign/scoreboard.csv`). Sub-agents ran as separate stateless calls scoped to the train split.
- **B.3 Configuration** — Provider-default sampling (no temperature/top-p overrides exposed by the CLI); thinking level high (recorded in every session's `run.json`); per-session budgets from `idea_03/launch.env` (24 h wall / 800 turns / 24 M tokens).
- **B.4 Customization** — No fine-tuning. No web retrieval, by frozen rule (the container had outbound network for the model API and permitted package installs); every session transcript leak-audited, 14 audits, all CLEAN. Tool use: the agent had a Python/R sandbox with the mounted train split, the benchmark package, the organizers' scoring code (read-only), and a scoring oracle for the seven validation studies. Agentic scaffold: Prime Agent with the frozen `APPEND_SYSTEM.md` appended to the system prompt.
- **B.5 Persistent memory** — Across sessions the agent's durable state was its own files in the mounted run tree (`DESIGN.md`, `REPORT.md`, `OPEN.md`, `anchors/`, `tools/`).
- **B.6 Inference stack** — N/A (hosted model).
- **B.7 Ensembles** — None. Single agent; the entry is a deterministic function of the anchor tables and the code.

## C · Prompts
- **C.1 Exact prompts** — The frozen system append and the first session brief are deposited in `code_repository` (`llm-as-scientist-v2/run/.prime/agent/APPEND_SYSTEM.md`, `llm-as-scientist-v2/run/TASK_01.md`).
- **C.2 System-wide instructions** — `APPEND_SYSTEM.md`. It contains the objective (sealed held-out studies are what count; validation is instrumental), the environment mechanics (fresh-draw truths, 2-submission budget, diagnostics-only feedback, promotion gate), all public target information, and blinding rules.
- **C.3 Prompt-design rationale** — Designed after a predecessor arm (idea_02) overfit validation feedback: the prompt carries objective and information only, and the restrictions live in the environment.

## D · Persona / profile construction (Tiers 1–2)
- **D.1 Profile source** — Synthetic demographic profiles drawn to the benchmark's census quotas by `run_record/target_entry.py` (`spec()` reads the moderator levels from the shipped `submission_spec.R`/`codebook.csv`). Control levels by subgroup come from published survey aggregates (`run_record/anchors/levels.csv`, 2,220 rows — Pew ATP, GSS, ANES, CCAM, TISP).
- **D.2 Profile verbalization** — N/A.
- **D.3 Assignment & weighting** — 54,000 rows over all 17 conditions: 3,000 per intervention, 6,000 control, quota-matched on the six moderators; no reuse across conditions; residuals mean-matched within every condition × moderator-level cell (iterative marginal centring, `--exact`) so the rows reproduce the intended table to 0.024 pp.

## E · Stimulus and survey administration
- **E.1 Stimulus presentation** — The agent read the 16 intervention texts verbatim from the benchmark package.
- **E.2 Survey walk-through** — N/A.
- **E.3 Response elicitation** — N/A.

## F · Stochasticity and aggregation
- **F.1 Runs & seeds** — The prediction table is deterministic given the anchor tables and code (no sampling). Backward synthesis uses a fixed seed in `target_entry.py`; regenerating the rows from `run_record/target_entry_v5_table.csv` reproduces the deposited file byte-for-byte. The agent sessions themselves are not bit-reproducible (LLM sampling), but every session transcript is archived (K.2).
- **F.2 Aggregation rule** — N/A (single deterministic table).

## G · Validation & post-processing
- **G.1 Human validation** — None. No human reviewed, edited or selected any predicted value.
- **G.2 Post-processing** — The agent decided on the following post processing: Predicted effects in percentage points of scale range are converted to native units per outcome (0–100 sliders; `donation_ams` in dollars, scale 10; `newsletter_signup` as a proportion) by `level_transform.py`; composite outcomes are synthesised on their item lattices (`K_ITEMS`). No refusals/missing values arise. Effective N per condition: 3,000 per intervention, 6,000 control.
- **G.3 Calibration corrections** — The agent decided on the following calibration: Two amplitude constants were gate-promoted on validation data: a study-uniform shrinkage of the *message-level* component κ = 0.20 in the many-arm regime, and outcome-level amplitude `LAM_BTW` = 1.00 (`DESIGN.md` §9–§12). One constant, `A_MULT` = 0.55 (assertion-match size), was measured on train data under a pre-registered two-sided rule (`run_record/campaign/…PREREG_S7.md`). All fits used held-out *published* studies or the train split only; the target study's data do not exist anywhere in the pipeline.

## H · Learning and conditioning components
- **H.1 Fine-tuning data** — N/A. No fine-tuning.
- **H.2 Context & retrieval corpora** — No retrieval. Material in the agent's working context: the benchmark package (instrument, texts, codebook, validator), the organizers' scoring code, the train-split datasets listed under I.2, the validation briefs (design only). All are in `code_repository`.

## I · Data inputs, blinding, and competing interests
- **I.1 Competing interests ★** — no relationship with LLM-vendor entities beyond being customers.
- **I.2 External human data †** — Train split mounted to the agent (all public, documented with licences in `code_repository/data/README.md`): agley2021, bago2025, gatewaybelief (van der Linden 2019 and Veckalov replications), geiger2026, gligoric2025, hackenburg2025, koetke2024, schmidbetsch2019, spampatti2023, tappin2023, vlasceanu2024, voelkel2024, voelkel2026, plus survey aggregates from Pew ATP, GSS, ANES, CCAM, TISP, ACS/CES, SCE, Wellcome. Held out as validation studies (outcomes sealed from the agent, scored by the oracle only): goldwert2026, kim2024, dablander2025, altenmueller2024, beall2017, orchinik2024, kerwer2025. Held out entirely (internal test / referee, never mounted): bbprime2025, bokemper2022; hewitt2026 excluded as memorisation risk. Respondent-level extracts from restricted sources (Pew, CCAM, ANES) are not deposited; only aggregate anchor tables are (`run_record/anchors/`).
- **I.3 Blinding attestation ★** — "Signed for team_31 by Tobias Holtdirk, 2026-08-31; covers both registered members (Tobias Holtdirk, Bolei Ma) and the contributor Haiwen Huang."
- **I.4 Contamination note †** — claude-opus-5; training-data and reliable-knowledge cutoff **May 2026** (Anthropic models documentation, checked 2026-08-31).

## J · Internal selection procedure
- **J.1 Design-space search †** — The agent's design choices were scored on the seven validation studies through the oracle and promoted by a leave-one-study-out gate (`run_record/campaign/scoreboard.csv`). Selection between the team's candidate methods used held-out published studies (bbprime2025, bokemper2022): this entry became primary after clearing a pre-registered bar on the sealed bbprime2025 score, opened only after the entry was frozen.

## K · Reproducibility & frozen artifacts
- **K.1 Code & materials** — `code_repository`: https://github.com/tobihol/silicon-sample-submission (directory `llm-as-scientist-v2/` — holding the campaign environment and start state.) Snapshot DOI: [10.5281/zenodo.22214502](https://doi.org/10.5281/zenodo.22214502) (`metadata.json.code_doi`). The agent's work products duplicated in this deposit under `run_record/`. No secrets; synthesis seed documented in `run_record/target_entry.py`.
- **K.2 Raw output logs †** — Complete session transcripts for s1–s7 and both forks, received from the operator on 2026-08-30 and assembled into one bundle (161 files, 305 MB): the ten JSON event logs (every message, tool call and sub-agent update), the oracle's scoring log and full-truth records, the three gate decisions, both forks' task directories, per-session launch snapshots (model, thinking, budgets, git commit, frozen-definition hash), the harness ledger, and the Prime Agent session transcripts with per-call sub-agent usage. The only edits: the operator's local home path replaced by a placeholder, and the operator's removal of credential placeholders. Chain of custody: the operator independently recorded the SHA-256 of all ten exec logs before hand-over; the escrow copies match (the two that differ are exactly the files that contained the home path). `MANIFEST.sha256` lists every file; **its own SHA-256 is `78632b5c3b2c2b3ca6b2a3b1c6e0fe86d86bc18ea4e8eb2eeed36719718cc2cd`** (the public hash for escrow). **Disclosure class for this item: B (escrowed)** — the transcripts quote verbatim stimulus texts of validation studies whose data are released without a licence (goldwert2026, orchinik2024, dablander2025), which we may analyse but not redistribute; the bundle is therefore deposited as a *restricted-access* Zenodo record available to the organizers on request, DOI [10.5281/zenodo.22214549](https://doi.org/10.5281/zenodo.22214549). The entry itself is class A: a deterministic function of `run_record/anchors/*.csv` + `run_record/target_model.py` + `run_record/target_entry.py`, all open in this deposit.
- **K.3 Computational resources** — Agent: ≈ 198 M tokens over ten sessions (main agent 80.1 M + train-split sub-agents 117.8 M; per-session detail in the escrowed transcripts, K.2).

## L · Disclosure class
**B · Escrowed** (one item). Every ★ item and every other item is public in this deposit or in `code_repository`; the single escrowed item is K.2, the raw agent logs (161 files, 305 MB), deposited as a restricted-access Zenodo record available to the organizers on request because the transcripts quote verbatim stimulus texts of validation studies released without a licence. Its public commitment is the SHA-256 of the bundle's `MANIFEST.sha256`, `78632b5c3b2c2b3ca6b2a3b1c6e0fe86d86bc18ea4e8eb2eeed36719718cc2cd`, and the manifest itself is reproduced in `raw_model_logs/`. The prediction file is a deterministic function of the open `run_record/` materials, so the escrow does not affect reproducibility of the entry.

★ items must always be public (never escrowed or withheld); † items must be at minimum escrowed. Full
policy: <https://janpfander.github.io/llm_predictions_megastudy/#disclosure>
