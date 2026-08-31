# ANCHORS_L — can a content-targeting map be VALIDATED? (open item A16)

**Verdict, one line: NO for a mechanically-coded map. The *mechanism* is real and replicates
out of sample where a high-quality outcome-specific reference code exists, but it is worth only
~0.1–0.2 of the generic rank-1 term, it adds nothing measurable on top of that rank-1 term, and
on behavioural/donation outcomes a text rule essentially never fires at all (2 of 39 train cells).**

**Scope / blinding.** Train split only: `/workspace/datasets/**` (respondent-level microdata and
vendored stimulus materials), `/workspace/benchmark/**` (public instrument, the 16 texts, codebook —
no human outcomes exist there), `/workspace/run/anchors/**`, and `/workspace/run/DESIGN.md` §6.5–6.6.
**No** `inputs/val/**`, **no** `runs/**`, **no** `inputs/idea01_lib/**`, **no retrieval of any kind**
(no web, no literature, no remote repos). **Packages installed from PyPI: none.** `pypdf`, `openpyxl`,
`numpy`, `pandas` were already present in `/opt/kernel/venv`; that interpreter ran every number below.

**Companions.** `_l_rule_T1.txt` (the rule, with its pre-registration timestamp and sha256),
`_l_item_dictionaries.json` (the 55 train item dictionaries), `targeting_train.csv` (422 coded
arm × outcome rows with noise-corrected effects, rank-1 fits, residuals and codes),
`targeting_target_map.csv` (**header only** — the rule did not validate),
`targeting_target_map_UNVALIDATED.csv` (the mechanical map anyway, for the record),
`_l_sources.csv` (25 provenance rows).

---

## 0. Headline, in the order the parent asked

1. **The rule was fixed first.** `_l_rule_T1.txt` was written to disk at **2026-08-28T07:48:35Z**
   (sha256 `a463f665a4ba…`), and amended once at **07:49:40Z** (inclusion criterion only). At both
   timestamps not a single arm × outcome effect table had been built in this session; the only data
   objects in memory were stimulus texts, condition lists and outcome names. The item dictionaries
   were saved at 07:53:23Z and the first ATE table was built after that.
2. **Primary LOSO test: DOES NOT VALIDATE.** Over 4 text-vendored train studies (172 arm × outcome
   cells, 88 of them fired), regressing the rank-1-removed residual on the targeting code gives
   **beta = +0.066 pp (sandwich se 0.537)** in-sample-rank-1, **+0.208 pp (se 0.535)** with a
   cross-fitted rank-1. Leave-one-**study**-out weighted MSE **rises** by +0.0072 pp² (primary; worse
   in 4 folds of 4) and by +0.0019 pp² (cross-fitted; better in 3 folds, worse in 1 and that one is
   the highest-powered study). Arm-permutation p on the LOSO gain: **p = 0.46** (primary), **p = 0.26**
   (cross-fitted). The fitted coefficient wanders from −0.19 to +0.43 across folds and its sign flips.
3. **It does beat a weaker baseline, and that is the interesting part.** Against an
   *arm-main-effect-only* model (constant outcome loading), the same code gives
   **beta = +1.263 pp (se 0.558, t = 2.27)** and a LOSO improvement of **−0.031 pp²**, better in 3
   folds of 4, permutation **p = 0.001**. So targeting really does carry information about *which*
   outcome a message moves — it is just not information the rank-1 generic term does not already have.
   Content targeting is a **substitute for** the rank-1 loading, not a **complement to** it.
4. **Behavioural/donation sub-answer (the named deliverable): the rule almost never fires there.**
   Across all 39 behavioural/donation cells in the train split (voelkel2026 Donation, vlasceanu
   SHAREcc and WEPTcc, spampatti WEPT_90, koetke BehavFollow) RULE T-1 fires on **2 cells** — one
   full (DynamicNorm × WEPT, whose text says "planting trees") and one half. The naive fit on those
   cells looks spectacular (**+1.52 pp, se 0.34, t = 4.4**, vs −0.28 (0.57) on attitudinal cells) and
   it is an artefact of inverse-variance weighting a single cell inside an n = 59,440 study. **There
   is no train evidence for a behavioural targeting term.** See §6 — this is the most decision-relevant
   result in the file, given the gate's "donation/behavioral outcomes" failure family.
5. **Secondary, and it is positive.** voelkel2024 is dropped from the primary set (7 of 25 arms are
   videos/chatbots whose content is not vendored), but its authors published two independent expert
   coders' ratings of exactly this construct — `Reference_PA` / `Reference_SUP` / `Reference_SPV`,
   "how much does this intervention explicitly reference [that outcome]", 1–5, for all 25 arms.
   On the rank-1-removed residual of the 25 × 3 table this gives **beta = −0.217 pp per code point
   (se 0.096, t = −2.25)** — negative is beneficial there, all three outcomes are harms — with
   **leave-one-arm-out ΔMSE = −0.061 pp², arm-permutation p = 0.013**, coefficient stable across the
   25 folds (−0.15 to −0.25), and the same sign for each coder separately (−0.23, −0.16) and under a
   cross-fitted rank-1 (−0.218). **The mechanism is real.** It is simply not recoverable by a string
   rule at the sample sizes and arm counts this family of studies provides.
6. **Norm ratio.** Best estimate of the **targeted : generic norm ratio 0.12, band 0.00–0.20**
   (0.041 vlasceanu, 0.145 voelkel2026, 0.177 voelkel2024-expert; 0.57 in the 3-arm koetke study,
   which I do not weight). The targeting term carries **1–3 % of the true within-outcome
   message-level variance** (band 0–5 %); zero is inside the primary interval.
7. **Half vs full.** Half : full ≈ **0.24** on the expert code (full −0.735 ± 0.297, half
   −0.174 ± 0.368) and ≈ **0.65** on the mechanical code (full +0.392 ± 0.237, half +0.253 ± 0.255).
   The campaign's 0.5 is inside both intervals and is not contradicted; it is also not confirmed.
8. **Coverage answer.** Applied mechanically to the 16 real texts × 13 outcomes, RULE T-1 fires on
   **111 of 208 cells** (39 full-tier, 72 half-only), and on **15 cells** if you require the match to
   cover ≥ 75 % of the outcome's constituent items. It recovers all four of the authored §6.6 cells
   and grades High public trust × trust_multidimensional at 0.625, i.e. *half*, exactly as §6.6 does.
   So the authored 4-cell map is not too small **by the rule's own logic** — it is the strict tail of a
   mechanical map that is otherwise far too promiscuous, and the promiscuous part cannot be validated.

---

## 1. The rule (verbatim in `_l_rule_T1.txt`)

RULE T-1 codes `target(arm, item)` in {0, 0.5, 1} from **stimulus text + item text only**:

* **FULL (1)** — some single sentence of the stimulus matches both the item's OBJ dictionary (the
  entity the item asks about) and its PRED dictionary (the property/quantity/act it asks the
  respondent to rate). Clause F1/F2/F3 (assert, name-as-subject-of-a-claim, elicit-and-correct);
  clause F4 covers "the stimulus asks the respondent to perform the very act the item measures".
* **HALF (0.5)** — some sentence matches OBJ only: topical adjacency without the proposition.
* **ZERO** — otherwise. There is no discretionary override.
* **Outcome level** — `target(a,o)` = **mean** over the outcome's constituent items (composites are
  scored as submitted, and a message that touches 1 of 12 trust items moves the composite by ~1/12);
  `tier(a,o)` = full if any component item is full, half if any is half.

OBJ/PRED dictionaries were written from the item wording **before** any stimulus was matched and
before any residual existed (`_l_item_dictionaries.json`, 55 train items, saved 07:53Z). Inclusion
(amendment A1, 07:49Z): an arm counts only if ≥ 60 content words of its participant-visible stimulus
are vendored verbatim; a study needs ≥ 3 such arms, one shared control and ≥ 3 outcomes on all arms.

**Known weaknesses of the mechanical implementation, disclosed:** (i) sentence-level OBJ+PRED
co-occurrence is a loose proxy for "asserts the proposition" — that is why it fires on 111/208 target
cells where a human fires on 4; (ii) `distrust_post`'s PRED list contains `trust`, so any
trustworthiness claim fires on it (defensible — it is the mirror item — but it inflates coverage);
(iii) longer texts match more, and I had to truncate the state-adaptive target arm at the
POST-TREATMENT banner after it initially swallowed the whole outcome battery.

## 2. The studies

Effects are ATEs vs each study's own control, in pp of that outcome's scale range
(0–100 slider ×1, 1–5 ×25, 1–7 ×16.67, 0/1 ×100, 0–8 ×12.5, 0–20 ×5).

| study | arms | outcomes | cells | n/arm | mean ATE (pp) | var_within obs | noise floor | **true within** | sd_wth (pp) | cells full / half | outcome blocks with contrast |
|---|---|---|---|---|---|---|---|---|---|---|---|
| voelkel2026 | 10 | 9 | 90 | 1023 | +1.20 | 0.976 | 0.750 | **0.226** | 0.47 | 13 / 23 | 7 |
| vlasceanu2024 | 10 | 4 | 40 | 4577 | +1.87 | 3.835 | 0.285 | **3.550** | 1.88 | 15 / 5 | 3 |
| spampatti2023 | 6 | 4 | 24 | 849 | +0.98 | 0.501 | 0.450 | **0.051** | 0.22 | 4 / 14 | 3 |
| koetke2024_S5 | 3 | 6 | 18 | 172 | -0.02 | 3.856 | 2.092 | **1.764** | 1.33 | 10 / 6 | 4 |
| gligoric2025 | 5 | 35 | 175 | 127 | -2.41 | 3.171 | 3.611 | **-0.440** | — | 0 / 0 | 0 |
| voelkel2024 (SECONDARY) | 25 | 3 | 75 | 1009 | -1.76 | 4.314 | 0.429 | **3.885** | 1.97 | 19 / 6 | 3 |

**Dropped, and why.**
* **voelkel2024** — 7 of its 25 interventions are videos, chatbot dialogues or interactive artefacts
  whose content is not vendored as text (`7WIG` 45 words, `62VB` 70, `ILPC` 87, `172G` 82, `6256` 169,
  `MP2C` 197, `BOXM` 228 of participant-visible text). Rule 4d drops the study rather than let me
  code an arm from its title. It returns in §5 through the authors' own coding.
* **gligoric2025** — included by 4b (5 text arms, 35 occupation outcomes, 175 cells) but RULE T-1 fires
  on **0 of 175** cells: not one of the five frames names a single scientific occupation, so the code
  is identically zero and the study contributes no within-outcome contrast. Its rows are in
  `targeting_train.csv` flagged `ZERO CONTRAST`. Note also that its noise-corrected within-outcome
  variance is **negative** (−0.44 pp²) — the whole arm × occupation table is consistent with sampling
  noise, exactly as ANCHORS_H reported.
* **vlasceanu2024 / WorkTogetherNorm** — the arm's stimulus is a neighbourhood *flyer image*; the qsf
  vendors ~50 words of instructions and no flyer text. Dropped by 4a; the other 10 arms are kept.

**Noise correction — two independent estimators, and they agree.** The analytic MVN floor (which keeps
the shared-control covariance: `Sigma = diag(v_arm) + v_control * J`) and 400 stratified split-halves
(`mean(W_A ∘ W_B)`) give the same true within-outcome variance to under 1.2 % on three of four studies:

| study | analytic true within (pp²) | cross-fitted (pp²) | ratio |
|---|---|---|---|
| voelkel2026 | 0.2256 | 0.2262 | 1.002 |
| vlasceanu2024 | 3.5499 | 3.5477 | 0.999 |
| koetke2024 S5 | 1.7643 | 1.7854 | 1.012 |
| spampatti2023 | 0.0506 | 0.0401 | 0.792 |

spampatti is the exception and it is the study whose true signal is ~0.05 pp² — a 21 % disagreement on
a quantity that is 10 % of its own noise floor is not a disagreement worth anything. Sampling noise is
a median **77 %** of the raw within-outcome variance in this set (voelkel2026 0.750/0.976,
spampatti 0.450/0.501, gligoric 3.611/3.171 — over 100 %), which is far worse than ANCHORS_J's median
25 % because these are the *small* studies; correcting it is not optional.

## 3. The primary test

`W` = column-centred ATE table (outcome main effect removed). `R1` = its rank-1 SVD component
(the campaign's "arm quality × outcome loading" model). `E = W − R1`. Predictor `t_c` = the targeting
code centred within (study, outcome). Weights = 1/se². Leave-one-**study**-out; the baseline is
predicting 0, i.e. the model with no targeting term. 172 cells, 4 studies.

| residual | predictor | pooled beta (pp) | se | t | pooled LOSO ΔMSE (pp²) | folds improved | perm p (ΔMSE) |
|---|---|---|---|---|---|---|---|
| W (outcome main removed) | t_c | +0.575 | 0.683 | 0.84 | −0.009 | 3/4 | — |
| W − arm main effect | t_dc | **+1.263** | 0.558 | **2.27** | **−0.031** | 3/4 | **0.001** |
| **W − rank1 (in-sample)** | t_c | **+0.066** | 0.537 | 0.12 | **+0.0072** | **0/4** | **0.46** |
| **W − rank1 (cross-fitted)** | t_c | **+0.208** | 0.535 | 0.39 | **+0.0019** | 3/4 | **0.26** |

Per-fold, primary spec (positive Δ = the targeting term made the held-out study worse):

| held out | beta trained on the rest | ΔMSE (pp²) | Δ as % of baseline |
|---|---|---|---|
| voelkel2026 | −0.190 | +0.0058 | +1.8 % |
| vlasceanu2024 | +0.427 | +0.0118 | +1.5 % |
| spampatti2023 | +0.148 | +0.0039 | +2.6 % |
| koetke2024 S5 | −0.039 | +0.0085 | +0.9 % |

Cross-fitting the rank-1 (fit it on one random half of respondents, remove it from the table built on
the other half, 400 splits, symmetrised) is the fair version — an in-sample rank-1 on a 10 × 8 table
eats real structure along with noise — and it lifts beta from +0.07 to +0.21 and turns 3 of 4 folds
positive, but the pooled ΔMSE is still +0.0019 and the permutation p is 0.26. **Nothing here is a rule.**

Why the arm-main row is not a licence: `t_c` is essentially orthogonal to each study's rank-1 direction
(share of `t_c`'s variance lying in it: 0.010, 0.011, 0.087, 0.004). The targeting code is *not*
collinear with the generic term — it simply predicts the same cells slightly worse than the free
rank-1 loading does, and adds nothing to it.

## 4. Half tier vs full tier

Coefficients on tier dummies, centred within (study, outcome), same weights:

| residual | beta FULL (pp) | beta HALF (pp) | half : full |
|---|---|---|---|
| W − rank1 (in-sample) | +0.392 (0.237) | +0.253 (0.255) | 0.65 |
| W − rank1 (cross-fitted) | +0.439 (0.230) | +0.241 (0.250) | 0.55 |
| voelkel2024 expert code (§5) | −0.735 (0.297) | −0.174 (0.368) | **0.24** |

Reading: a **full** match is worth roughly 0.4 pp of extra effect on that cell (mechanical rule) or
0.74 pp (expert code, where "full" = reference ≥ 3.5 on the 1–5 scale). A **half** match is worth
between a quarter and two thirds of that. The campaign's 0.5 is defensible and unrefuted; if I had to
move it I would move it **down**, because the only fold-validated estimate (§5) puts it at 0.24 and the
half band there has just 6 cells.

## 5. Secondary: voelkel2024 with the authors' own reference codes

25 interventions × 3 outcomes (partisan animosity, support for undemocratic candidates, support for
partisan violence), n = 35,252, control = `Null_Control`. `Reference_PA` / `Reference_SUP` /
`Reference_SPV` are the study's own two expert coders' 1–5 ratings of how explicitly each intervention
references that outcome (inter-coder r = 0.63 / 0.92 / 0.89). This is an outcome-specific content
targeting code produced by people who had never seen my residuals.

All three outcomes are *harms*: mean ATEs are PA −4.70 pp, SUC −0.42, SPV −0.15, so a **negative** beta
means targeting **helps**.

| specification | beta (pp per code point) | se | t |
|---|---|---|---|
| W (outcome main removed) | −0.679 | 0.196 | −3.47 |
| W − arm main effect (double-centred code) | −0.596 | 0.164 | −3.63 |
| **W − rank1 (in-sample)** | **−0.217** | **0.096** | **−2.25** |
| W − rank1 (cross-fitted, 240 half-splits) | −0.218 | 0.095 | −2.28 |
| W − rank1, coder J only | −0.232 | 0.094 | −2.46 |
| W − rank1, coder N only | −0.163 | 0.084 | −1.93 |

Leave-one-**arm**-out (25 folds): ΔMSE = **−0.0609 pp²**, arm-permutation p = **0.013**, fitted beta
ranges only −0.152 to −0.250 across folds. Per outcome, corr(Reference centred, residual) is
−0.72 (SUC), −0.39 (PA), −0.01 (SPV) — so most of it is the undemocratic-candidates column, where the
arms that show pro-democracy elite cues move exactly that item. With three outcome columns, one of
them carrying the effect, this is one good study, not a law.

Implied magnitudes for the campaign: a full reference is worth **0.74 pp** on that cell beyond rank-1,
against a true message-level SD of 1.97 pp in that study — i.e. **0.37 SD of message-level variation**,
and 2.5 % of the study's true within-outcome variance.

## 6. Behavioural and donation outcomes — the named deliverable

This is the question the gate's rejection made urgent, and the answer is blunt.

| study | behavioural outcome | arms | cells fired FULL | cells fired HALF |
|---|---|---|---|---|
| voelkel2026 | Donation (up to \$1 to 5 environmental NGOs) | 10 | **0** | **0** |
| vlasceanu2024 | SHAREcc (actually posting to social media) | 10 | **0** | **0** |
| vlasceanu2024 | WEPTcc (pages of effort → trees planted) | 10 | 1 | 0 |
| spampatti2023 | WEPT_90 (same task) | 6 | **0** | **0** |
| koetke2024 S5 | BehavFollow (asked to be sent more information) | 3 | 0 | 1 |
| **total** | | **39 cells** | **1** | **1** |

Two fired cells in 39. The one full match is `DynamicNorm × WEPTcc`, fired by the sentence
*"spending time, effort, and money on initiatives to mitigate climate change (for example, planting
trees, offsetting carbon emissions)"* against the WEPT item's OBJ `tree` and PRED `plant`. Its residual
is +1.36 pp. The half match is `Personal Humility × BehavFollow`, fired by *"i am excited to continue to
learn more about this issue"* against the item's OBJ `learn more`.

Fit those two cells with inverse-variance weights inside an n = 59,440 study and you get
**beta = +1.517 pp, se 0.343, t = 4.43** on behavioural outcomes against **−0.280 (0.565)** on
attitudinal ones, and a LOSO that "improves" by −34 % and −12 % in the two folds that contain a fired
cell and by exactly 0 % in the two that do not. **That is one cell wearing a t-statistic.** I report it
because it is the shape of the mistake that a targeting term would encourage, not because it is a result.

Three things follow, and they are the practical content of this file:

1. **A text-derived targeting term cannot be the mechanism behind a donation/behavioural failure
   family.** The rule does not fire there — messages talk about climate scientists, not about donating
   to the American Meteorological Society or subscribing to a newsletter. Whatever went wrong on
   donation/behavioural outcomes, targeting is not it, and adding a targeting term will not fix it.
2. **Conversely, do not put a targeting bonus on a behavioural cell.** There are 39 train cells and
   2 of them carry any information at all; anything the entry does to `donation_ams`,
   `newsletter_signup` or `behavior_mean` on targeting grounds is fitted to a single arm of a single
   study, and ANCHORS_K already resolved `donation_ams` against a positive treatment on other grounds.
3. **On the target instrument the same pattern reappears.** Of the 111 mechanically-fired cells, the
   ones touching behaviour are: Extreme weather predictions × donation_ams (half, and only because the
   long state-adaptive text mentions donating), Interview Prof. Sebille × behavior_mean (1 of 6 items),
   Oil industry misinformation × behavior_mean (1 of 6), and three trivial 1/12-weight half matches.
   `newsletter_signup` fires on **no arm at all**.

## 7. What the rule does on the target, for the record

`targeting_target_map.csv` is **empty with a header**, because step 3 was negative and the brief asks
for exactly that. The mechanical map is preserved in `targeting_target_map_UNVALIDATED.csv`
(328 item-level rows, every one citing the clause, the OBJ and PRED patterns that fired, the literal
stimulus sentence and the literal item wording).

Its shape: **111 of 208 cells fire; 39 reach full tier; 15 cells have a match covering ≥ 75 % of the
outcome's items; 14 reach 1.0.** The strict (≥ 0.75) list is:

Consensus × belief_post · Corporate reliance × trust_post · Corporate reliance × distrust_post ·
Former skeptics × distrust_post · Funding × funding_perceptions · High public trust × trust_post ·
High public trust × distrust_post · Interview Prof. Maraun × trust_multidimensional (0.875) ·
Measurement & modeling (1) × trust_post · Oil industry misinformation × belief_post / trust_post /
distrust_post · Peer-review × trust_post / distrust_post · Portrait Prof. Cherry × trust_post.

Two things to notice. First, the mechanical rule **reproduces the authored §6.6 map**: Consensus ×
belief_post = full, Funding × funding_perceptions = full, High public trust × trust_post = full, and
High public trust × trust_multidimensional = 0.625 — *half*, which is precisely the judgement §6.6
records. The authored map is the strict tail of the mechanical one. Second, the extra 100-odd cells are
mostly `distrust_post` (the mirror item fires on any trust claim) and 1/12-weight touches of
`trust_multidimensional`; they are the promiscuity that the validation says is worthless.

**Recommendation to the campaign, stated plainly.** Keep the 3-full-plus-1-half authored map. Do not
expand it on the strength of this measurement — the expansion is exactly the part that fails LOSO.
If anything is changed, shrink the half tier from 0.5 toward 0.3, and add nothing on behavioural or
donation cells. If a targeted term is carried at all, cap its norm at **0.12 × the generic rank-1
term's norm (band 0.00–0.20)**, i.e. let it carry **1–3 % of within-outcome message-level variance**.

## 8. Recognition and blinding disclosure

I recognise most of these datasets as published papers (voelkel2026 / Climate Change Challenge,
voelkel2024 / Strengthening Democracy Challenge, vlasceanu2024 / Many Labs climate, spampatti2023,
koetke2024, gligoric2025) and I have some memory of their headline claims — that the megastudies found
small, broadly similar effects across arms, and that voelkel2024's interventions moved partisan
animosity more than the democratic-attitude outcomes. **No remembered number is used anywhere in this
file.** Every quantity was recomputed from the vendored microdata by the procedure recorded in
`_l_sources.csv`; the memory only influenced which files I opened first. In particular the
`Reference_PA/SUP/SPV` analysis in §5 uses the coding workbooks as shipped in
`/workspace/datasets/voelkel2024/downloads/`, not any published table.

I sought nothing about the target study's human outcomes and encountered nothing. No web search, no
literature, no remote repositories, no package installs. The only files I read outside
`/workspace/datasets/**` and `/workspace/benchmark/**` are the sibling anchor notes named in
`_l_sources.csv` and `DESIGN.md` §6.5–6.6.

One honesty note on ordering: the **target-side** item dictionaries (§7, `t.*`) were necessarily
written after the train analysis was complete. They were written from `codebook.csv` wording alone,
by the same procedure as the train dictionaries, and the target has no outcomes to peek at — but the
train dictionaries were pre-registered and the target ones were not, and the map is unvalidated anyway.
