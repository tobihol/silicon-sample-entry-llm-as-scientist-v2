# ANCHORS_E — outcome-level RESPONSIVENESS PROFILE and CONTROL LEVELS in the target's own 13 outcomes

Run: idea_03 sub-agent, train-split-only job. Sources: `/workspace/datasets/*` and
`/workspace/benchmark/*` (instrument/codebook only — no human outcomes exist there).
No validation data, no `inputs/`, no web, no retrieval, no remembered published numbers:
every figure below is either computed here from raw train microdata, or cited from a
train-derived anchor file in this directory (ANCHORS_A/B/C/D).

Machine-readable companions
- **`outcome_profile.csv`** — the 13-row deliverable (levels, responsiveness band, sources, notes).
- **`_e_sources.csv`** — 46 rows, one per (study x source-measure): `n_arms, n_per_arm,
  ctrl_mean_pp, mean_signed, mean_abs, rms_obs, rms_se, rms_true, sd_arms, sd_true`,
  with the target-outcome mapping in `target_outcome`.

Units throughout: **percentage points of each outcome's scale range**
(`ate_pp = 100*(mean_arm - mean_control)/(hi-lo)`), i.e. the benchmark's own unit.
For `donation_ams` scale_range = 10 so **$0.10 = 1.0 pp**; for `newsletter_signup`
scale_range = 1 so **1 percentage point of signup rate = 1.0 pp**.

---

## 0. The headline claim, in one paragraph

Responsiveness is **not a property of an outcome**; it is a property of the *distance*
between what the message asserts and what the item measures. Every train study that
measures a proximal and a distal construct in the same respondents gives the same
number for one construct step: **the downstream effect is 0.10–0.30 of the proximal
effect, central 0.21**, and it then **flattens** — the second step costs much less than
the first. Because the target's 16 interventions assert things *about climate scientists*,
**trust is the proximal outcome and everything else is downstream**. That inverts the
profile you would read off `voelkel2026`/`vlasceanu2024`, where the messages assert
climate urgency and belief/concern/policy are the proximal block. Concretely:
if `trust_multidimensional` moves 1.0 pp, the other twelve outcomes move
**0.1–0.5 pp**, the 0-100 slider families cluster at **0.17–0.30**, and the two
behavioural cells are the only ones that can plausibly move *more* (newsletter, because
a binary is scale-efficient) or *the wrong way* (donation, effortful behaviour).

---

## 1. The mapping — the deliverable's backbone

| target outcome | train source | source measure | why it maps |
|---|---|---|---|
| `trust_multidimensional` | **tisp** | 12 `TRUST_SCI_*` items (1–5) | **the target's own 12 items**, generic-scientist wording |
| | tisp | `CLIM_TRUST` (1–5) | climate-scientist referent |
| | gligoric2025 | 35-occupation / climatologist trust (7-pt bipolar) | randomised trust messages |
| | koetke2024 | METI 14-item (7-pt bipolar) | randomised vignette/text arms |
| | agley2021 | 21-item Trust in Science Inventory (1–5) | 2-arm RCT, pre+post |
| | geiger2026/Većkalov | `scientist_trust` (1–7) | trust in **climate** scientists under message randomisation |
| | attari2016 | 6-item researcher-credibility composite (−1..+1) | the only *manipulated* credibility construct in the corpus |
| `trust_post` | tisp `CLIM_TRUST`; gligoric single occupations | single-item trust | single-item version of the same construct |
| `distrust_post` | *(none)* | — | **no train source has a distrust slider**; see §5 |
| `funding_perceptions` | **gss** `natsci`, `natenvir` | 3-pt "too little / about right / too much" federal spending | **identical response semantics** to `funding_5` |
| | wellcome 2018 `Q14B` | funding-transparency 4-pt | adjacent facet, level only |
| `policy_role_mean` | **tisp** `NORMPERC_integrate/advocate/communicate/involved` | 1–5 agreement | **verbatim item match** with `policy_role_1..4` |
| `inst_trust_mean` | **pew_atp** W149 2024 agency-favourability topline | EPA / NASA / NPS / ED, 4-pt + "not sure" | EPA and NASA by name |
| | gss `confed`, `coneduc`, `consci` | 3-pt confidence | federal government, universities |
| `belief_post` | voelkel2026 `Belief_*`; vlasceanu2024 `Belief`; bago2025 `prior_cause_1`; ccam; geiger2026 | 0–100 sliders / 1–7 | human-causation belief |
| `concern_mean` | voelkel2026 `Concern_*`; ccam `worry`; anes `V202333`; geiger2026 `worry` | 0–100 / 1–7 / 5-pt | concern/worry/importance |
| `policy_general` | **voelkel2026** `Policies_*` | 0–100 slider | contains **the target's exact item** ("U.S. government should do more to reduce global warming") |
| | vlasceanu2024 `Policy`; geiger2026 `policy`; attari2016 `policy_support` | | |
| `policy_specific_mean` | voelkel2026 `PoliciesSp_*`; **tisp** `CLIM_POLSUPPORT_*` | 0–100 / 1–4 | TISP covers 5 of the target's 7 policy topics |
| `behavior_mean` | voelkel2026 `IntentNp_*` (+`Intent_*`) | 0–100 "how likely in the next 12 months" | **same stem, 3 of 6 items identical** |
| | vlasceanu2024 `WEPT`; spampatti2023 `WEPT_90` | effortful task | costly-behaviour contrast |
| `donation_ams` | **voelkel2026** `Donation` | real incentivised dictator, 100 cents across 5 environmental NGOs | only charity dictator in the corpus |
| | voelkel2024 `PA_DG` | dictator game in a 25-arm megastudy | money-vs-attitude ratio |
| `newsletter_signup` | vlasceanu2024 `Sharing` (binary) | in-survey share decision | costless binary opt-in |
| | koetke2024 S5 `Behavior Follow` (binary) | opt in to follow the scientist's work | opt-in after a trust message |
| **unmappable** | voelkel2026 `Candidate_Post`, `Companies_Post`; every `consensus_perception` row | — | the target has **no** candidate, company-action or perceived-consensus outcome. Note: *perceived consensus is the single most movable construct in the whole corpus (9.05 pp median) and the target does not score it.* |

**Outcomes with NO direct train evidence (nearest proxy in brackets):**
1. `distrust_post` — nothing. Proxy: mirror of `trust_post` with an attenuation factor.
2. `inst_trust_mean` **NOAA component** — nothing. Proxy: Pew W149 National Park Service (74) as a low-salience non-partisan science agency; NASA (67) as the upper bound.
3. `behavior_mean` **solar-panel** and **talk-to-friends-and-family** items — nothing. Proxy: voelkel2026 gives the other four.
4. `donation_ams` at a **$10 stake to a professional society** — nothing. Proxy: voelkel2026's $1 stake to five environmental NGOs (61.5%).
5. `newsletter_signup` with an **external-link subscription** — nothing. Proxy: two in-survey opt-ins (44%, 48.5%) that carry far less friction.
6. `policy_role_mean` **responsiveness** — the item wording matches TISP exactly but TISP is observational; no train study ever randomised a message and measured this construct.

---

## 2. Method

1. **Inventory.** Every `/workspace/datasets` folder with a message-vs-control contrast was
   screened. Usable: `voelkel2026`, `voelkel2024`, `vlasceanu2024`, `geiger2026` (vdL 2019 +
   Većkalov 2024), `gatewaybelief`, `gligoric2025`, `koetke2024`, `agley2021`,
   `spampatti2023`, `attari2016`, `tappin2023`, `hackenburg2025`, `schmidbetsch2019`.
   Level-only (no experiment): `tisp`, `gss`, `pew_atp`, `anes`, `ccam`, `wellcome`, `bago2025`.
   `acs`, `ces`, `sce` carry no mappable construct.
2. **Conversion.** All ATEs to pp of scale range. Per (study x source-measure) I report the
   observed `mean_abs` = mean |ATE| across arms **and** the noise-corrected
   `rms_true = sqrt( mean(ATE^2) − mean(se^2) )`, plus `sd_true` (across-arm heterogeneity
   after subtracting the sampling-variance floor). `n_arms` and `n_per_arm` are in
   `_e_sources.csv` for every row; nothing below rests on a cell with `n_per_arm < 90`
   except where explicitly flagged.
3. **Aggregation.** Because responsiveness is a distance property, cross-study pooling is
   done on **within-study ratios**, never on raw magnitudes: each study contributes
   `resp(o)/resp(reference)` where the reference is that study's proximal construct.
   Those ratios are then re-anchored so that `trust_multidimensional = 1.00`.
4. **Two independent routes to each downstream coefficient**, and I report the range they
   span rather than a point:
   - *route A (direct)* — a study that manipulated a scientist-credibility construct and
     measured a target-like outcome (attari2016; koetke S5; Većkalov).
   - *route B (structural)* — the cross-sectional regression slope `b(o | trust)` in TISP,
     multiplied by a propagation efficiency `eta` measured in route-A studies.

---

## 3. The decay evidence, study by study

### 3a. The one-step discount is 0.10–0.30 in every study that measures it

| study | proximal construct (pp) | downstream construct (pp) | ratio |
|---|---|---|---|
| **attari2016** 2019 Study 1, 6 policy topics, n≈305/cell | researcher credibility **21.9** | climate-policy support **4.72** | **0.216** (per topic 0.084–0.285) |
| **voelkel2024** SDC, 25 interventions, n≈1,020/arm | partisan animosity **4.94** | 5 step-1 outcomes **1.25–1.59** | **0.25–0.32** |
| **voelkel2024** SDC | partisan animosity 4.94 | 3 step-2 outcomes 0.79–0.98 | 0.16–0.20 |
| **geiger2026/Većkalov** all-27, n≈3,500/arm | perceived consensus **6.43** | belief 1.33 / worry 0.98 / policy 0.52 / **trust 0.33** | 0.21 / 0.15 / 0.08 / **0.05** |
| **geiger2026/vdL2019** DiD, n≈1,080/arm | perceived consensus 16.20 | belief 1.86 / worry 1.36 / policy 1.19 | 0.11 / 0.08 / 0.07 |
| **gatewaybelief** Exp1 (Maertens 2020) | perceived consensus 8.4–9.3 | belief 2.36–2.95 / action 0.97–2.26 | 0.28–0.35 / 0.10–0.24 |

**Central one-step coefficient 0.21; band 0.10–0.30.** The second step costs far less than
the first: SDC goes 1.00 → 0.29 → 0.18, not 1.00 → 0.29 → 0.08. **Do not chain a x4–5
discount twice**; the profile flattens into a floor at ~0.15–0.20 of the proximal effect.
(This corrects the naive reading of ANCHORS_B rule 3, which is right about one step and
too aggressive about two.)

### 3b. Inside the climate-attitude block the discount is ≈1.0, not 0.2

`voelkel2026` (10 short climate texts, n≈1,030/arm, ANCOVA, `_e_sources.csv` rows 0–8):

| outcome | mean\|ATE\| | rms_true | sd_true | ratio to belief |
|---|---|---|---|---|
| political behavioural intentions | 1.84 | 2.03 | 0.92 | 1.50 |
| concern | 1.38 | 1.50 | 0.92 | 1.12 |
| specific policies | 1.34 | 1.37 | 0.30 | 1.09 |
| **belief** | **1.23** | 1.44 | 0.91 | 1.00 |
| non-political behaviours | 1.17 | 1.24 | 0.44 | 0.95 |
| general policy | 0.98 | 1.02 | 0.73 | 0.80 |
| donation (real money) | 1.49 (**mean signed −1.38**) | 0.69 | 0.00 | ~0.5, wrong sign |

The whole attitude block moves together at 0.8–1.5x belief. Cross-checked structurally:
the control-arm OLS slopes on belief (concern 1.04, general policy 0.94, companies 0.89,
specific policies 0.67, non-political intentions 0.45) reproduce the ATE ratios to within
±0.3 for the attitude items, i.e. **within a construct domain the effect propagates along
the observed covariance with efficiency eta ≈ 1**. Across domains (credibility → policy;
consensus → trust) eta collapses to **0.2–0.35**. That contrast is the single most useful
structural fact in this file.

### 3c. Magnitude of the *proximal* trust effect itself

| study | arms | n/arm | mean signed | rms_true |
|---|---|---|---|---|
| gligoric2025 (5 trust messages x 2 ideology cuts, 35-occ composite) | 10 | 785 | +0.48 | **0.00** |
| agley2021 infographic, 21-item | 2 | 511 | +0.33 | 0.00 |
| geiger2026/Većkalov, 2 consensus msgs, trust in climate scientists | 2 | 3,507 | +0.33 | 0.00 |
| koetke2024 S5, 3 intellectual-humility text arms, METI | 3 | 174 | **+2.43** | — |
| koetke2024 S2–S4 persona vignettes (the scientist is *re-described*) | 5 | 150 | +4.2 … +16.4 | 8.3 |
| voelkel2024 SDC, 25 interventions on the *targeted* attitude | 26 | 1,025 | −4.87 | 5.84 |

Two regimes. **Appending a pro-science message** to a fixed target of judgement buys
0.3–1.0 pp. **Re-describing who is being judged** buys 2–16 pp. The target's 16
interventions (portraits, interviews, peer-review and measurement explainers, former
sceptics, community helpers) are *descriptions of climate scientists* but the outcome asks
about "**most** climate scientists", so the generalisation step is paid. Base for this
file: **1.0 pp, band 0.5–2.0 pp.** Everything in `outcome_profile.csv:abs_ate_pp_ctr` is
`resp_ctr x 1.0 pp` and rescales linearly if you prefer a different base.

### 3d. Between-arm spread (carried from ANCHORS_C, not re-derived)

`sd_true` in `_e_sources.csv` is 0.00 for every trust source and 0.3–0.9 for the
voelkel2026 attitude outcomes: with 16 professionally written interventions the true
arm-to-arm SD is small relative to the shared mean.

---

## 4. Control-arm levels for the other constructs (extending ANCHORS_D, which owns trust)

ANCHORS_D §1 already fixes the trust levels (12-item 1–5 composite 71.5 generic;
`CLIM_TRUST` 67.0; format effects; the 2021–24 decline; the party gap). **Not redone here.**
Levels below are new work, all weighted where a weight exists.

| construct | value | source, computed here |
|---|---|---|
| **funding_perceptions** | **66.5** (se 0.44, n=10,523) | GSS `natsci` 2021–24, scored *exactly* as `funding_perceptions` (too little=100, about right=50, too much=0). By year: 2021 68.6, 2022 66.1, 2024 64.2 — a slow decline. `natenvir` (environment) is far higher at **78.4**. Climate-*research* spending is more polarised than "scientific research" in general, so the target item should sit at or a little below `natsci`: **centre 64**. |
| **policy_role_mean** | **65.0** (se 0.52, n=2,559; sd 25.9 pp) | TISP US weighted, the **verbatim four items**: integrate 62.1, advocate 67.5, communicate 66.9, involved 63.6. (Two TISP items not in the target: outreach 80.9, independence 71.0.) Slider rendering adds ~+2 → **centre 67**. |
| **inst_trust_mean** | **~54** | Pew W149 (Jul 2024, N=9,424) agency favourability recoded very fav=100 / somewhat fav=67 / somewhat unfav=33 / very unfav=0 / not sure=50: **EPA 54.0, NASA 67.0**, NPS 73.8, Dept of Education 45.8, IRS 39. Plus GSS 2021–24 `confed` (federal executive) **33.1**, `coneduc` **47.5**. NOAA has no train measurement (proxy 60–68). Five-item mean ≈ 54, +2 for slider → **centre 56**. |
| **belief_post** | **68** | voelkel2026 control post items 72.0 / 71.8 (0–100 sliders, 2024 quota panel); vlasceanu2024 US control 66.5; bago2025 Prolific human-causation slider 70.9 (Prolific skews +5–8 vs a quota sample); CCAM "human-caused" runs lower on a binary. |
| **concern_mean** | **58** | voelkel2026 control post 60.4 (items 61.2 / 64.5 / 55.6); the target's third item ("relative to other issues") is the lowest-scoring concern item in every source (ANES 2020 importance 57.4 vs severity 62.6), pulling the composite ~2 pp below voelkel2026. |
| **policy_general** | **66** | voelkel2026 `Policies` 68.0 (composite containing the target's exact item); vlasceanu US 62.5. |
| **policy_specific_mean** | **61** | TISP US 1–4: fuel tax 41.3, public transport 51.0, sustainable energy 52.3, protect land 58.4, food tax 36.9 (5-item mean **48.0**, sd 19.7). voelkel2026 `PoliciesSp` 53.3. The target's 7 items are 5 popular (transport, renewables, forests, green jobs, clean water) + 2 tax items, so ~8–13 pp above the TISP mix. |
| **behavior_mean** | **40** | Built item-by-item from voelkel2026 control post: eat less meat 38.9, transport 46.3, fly less 52.8, give money to an environmental group 30.5 (and, not in the target, reusable bags 68.0, local food 62.7, less plastic 58.7, sign petition 47.2, join group 27.7, write official 29.9). The two target items with no analogue (install a solar panel, talk to friends and family) are respectively far below and near the middle. |
| **donation_ams** | **34 pp = $3.40** | See §6. |
| **newsletter_signup** | **12 pp = 12 %** | See §6. |

---

## 5. Notes on the three cells that need care

**`distrust_post` is not `100 − trust_post`.** It is a separate slider, not reverse-coded
in cleaning, so **higher = more distrust and the predicted ATE sign must be negative**
for an intervention that raises trust. No train source pairs a trust and a distrust slider,
so the level is inferred: the mirror of `trust_post` (=33) plus the 1–5 pp upward bias that
negatively-worded items carry in every multi-item battery here (TISP, Pew W42, agley's
un-reversed inventory), giving **34** with a wide band. Responsiveness is set below 1 in
absolute value (**−0.75**, band −1.10…−0.35) because negatively-worded items are the least
responsive members of every battery in the corpus.

**`funding_perceptions` is arm-dependent.** The "Funding" intervention asserts this
construct directly; for that one arm expect **2–3x** the profile value (i.e. 0.6–0.9 pp)
while the other 15 arms sit at 0.1–0.4 pp. The same logic applies weakly to
`policy_role_mean` for the two interview arms and to `inst_trust_mean` for the
oil-industry-misinformation and corporate-reliance arms.

**Ceiling asymmetry.** ANCHORS_D §4 shows Democrats sit at 76–85 on climate items
(15–24 pp of headroom) and Republicans at 41–53 (47–59 pp). Larger predicted effects among
Republicans are partly a headroom statement, and gligoric2025 is the counter-evidence
(five messages purpose-built for conservatives all failed).

---

## 6. `donation_ams` and `newsletter_signup` — 32 of the 208 cells

### 6a. Every real behavioural measure in the train split

| study | measure | control level | treatment shift, **in the scored unit** |
|---|---|---|---|
| **voelkel2026** | real incentivised dictator: 100 cents of a $1 bonus across 5 environmental NGOs | **61.5 % of the endowment** (sd 45.3; **29.7 % give 0, 47.2 % give all 100**, median 95) | 10 arms: **−3.95 … +0.53, mean −1.38**, rms(se) 1.65 → `rms_true` **0.69**, `sd_true` **0.00**. Nine of ten arms negative. |
| **voelkel2024** SDC | dictator game (partisan animosity domain) | 64.9 | 26 arms, mean\|ATE\| **4.38**, `rms_true` 5.15 — **0.89x** the matched attitude thermometer (4.94) |
| **vlasceanu2024** | binary in-survey share decision | **48.5 %** (global, n=3,808/arm) / 53.5 % (US) | **+6.55 pp** global (rms_true 6.99, sd_true 2.58); +7.70 pp US. **4.5x the belief slider in the same sample.** |
| **koetke2024 S5** | binary opt-in to follow the scientist's work | **44.0 %** (n≈156/arm) | −4.84, −9.38, −10.21 pp; rms(se) 5.6 → `rms_true` 6.4 but `sd_true` 0.00 — **directionally negative, statistically noise** |
| **vlasceanu2024** | WEPT (effortful page-review task, 0–8 pages) | 62.5 | **−2.31 pp** global, −3.70 US — **negative** |
| **spampatti2023** | WEPT | 18.3 | mean −0.84, `rms_true` 0.00 |
| **bago2025** | headline upvote / bookmark | — | **not usable**: both are forced per-headline tasks (99.8 % bookmark at least one), not spontaneous opt-ins |

### 6b. What that implies

- **The money cell is the one place where the sign is genuinely in doubt.** The only
  climate-domain dictator in the corpus (voelkel2026) moved *down* under 9 of 10 messages;
  the only well-powered effortful-behaviour measure (vlasceanu WEPT) also moved *down*;
  yet the only megastudy where the money was *directly about the targeted attitude object*
  (SDC) moved money as much as attitudes. The target sits in between: the AMS is a
  **scientific society**, so the donation is closer to the manipulated construct than a
  climate charity would be. Profile: **+0.12, band −0.10 … +0.40** — i.e. predict
  ≈ **$0.01 per arm** with a real possibility of zero or a small negative.
- **The signup cell is scale-efficient and can out-move the primary outcome.** One
  percentage point of signup rate is one full scored pp. vlasceanu's binary moved 4.5x its
  own belief slider. If the target's newsletter offer behaves like that, an ATE of 1–3 pp
  is possible on cells whose slider siblings move 0.2 pp. But the target's offer has real
  friction (external tab, actual subscription) which both lowers the base rate and damps
  the effect, and koetke's opt-in went the other way. Profile: **+0.45, band 0.00 … 1.60**.
- **Level warning.** `donation_ams` (34 pp = $3.40) and `newsletter_signup` (12 pp = 12 %)
  are the two weakest control levels in this file — both are extrapolations across a
  stake change and a friction change that no train dataset spans. If the operator has to
  be wrong somewhere, it will be here. Both distributions are **strongly non-normal**:
  voelkel2026's donation is U-shaped with 30 % at the floor and 47 % at the ceiling, so a
  Tier-1 backward synthesis must reproduce a bimodal, not Gaussian, donation column, and
  the $1-increment grid means only 11 support points exist.

---

## 7. The profile, assembled

`resp(o)` is normalised so `trust_multidimensional = 1.00`; `abs_ate_pp_ctr = resp_ctr x 1.0 pp`.

| outcome | level lo/**ctr**/hi | resp lo/**ctr**/hi | \|ATE\| pp | construct step from the assertion |
|---|---|---|---|---|
| `trust_multidimensional` | 62/**69**/74 | —/**1.00**/— | 1.00 | 0 (asserted) |
| `trust_post` | 60/**67**/73 | 0.85/**1.05**/1.30 | 1.05 | 0 |
| `distrust_post` | 27/**34**/42 | −1.10/**−0.75**/−0.35 | −0.75 | 0, opposite valence |
| `policy_role_mean` | 61/**67**/72 | 0.12/**0.30**/0.50 | 0.30 | 1 (same object, different construct) |
| `funding_perceptions` | 57/**64**/71 | 0.10/**0.30**/0.55 | 0.30 | 1 (2–3x on the Funding arm) |
| `inst_trust_mean` | 50/**56**/62 | 0.12/**0.28**/0.48 | 0.28 | 1 (generalisation to institutions) |
| `belief_post` | 61/**68**/74 | 0.15/**0.28**/0.45 | 0.28 | 1–2 |
| `concern_mean` | 52/**58**/64 | 0.10/**0.22**/0.38 | 0.22 | 2 |
| `policy_general` | 60/**66**/72 | 0.08/**0.20**/0.33 | 0.20 | 2 |
| `behavior_mean` | 34/**40**/46 | 0.06/**0.18**/0.35 | 0.18 | 2–3 |
| `policy_specific_mean` | 55/**61**/67 | 0.07/**0.17**/0.30 | 0.17 | 2–3 |
| `newsletter_signup` | 4/**12**/25 | 0.00/**0.45**/1.60 | 0.45 | 3, but binary/scale-efficient |
| `donation_ams` | 22/**34**/48 | −0.10/**0.12**/0.40 | 0.12 | 3, costly, **sign in doubt** |

Sanity checks the profile passes:
- The mean over the 12 non-primary outcomes is **0.22**, matching the pooled one-step
  coefficient 0.21 from §3a independently derived.
- The 0-100 slider attitude block (belief → policy_specific) spans 0.17–0.28, i.e. a
  **factor of 1.6 across seven outcomes** — consistent with voelkel2026, where the whole
  attitude block spans a factor of 1.9 (0.98–1.84).
- The implied absolute magnitudes (0.1–0.3 pp on the downstream sliders) sit inside the
  ±0–3 pp band that ANCHORS_D §4 established for every control-arm drift and message ATE
  in this family.

---

## 8. Caveats

1. **The 0.21 one-step coefficient is the load-bearing number** and it rests on six
   studies, only one of which (attari2016) runs in the *credibility → climate outcome*
   direction the target needs. attari has **no control arm** (it is a vignette-vs-vignette
   contrast) and its manipulation is 22 pp, ~20x anything the target will produce; if the
   transfer is concave in dose, 0.21 is an under-estimate for small doses, and if there is
   a fixed cost to moving a downstream attitude at all, it is an over-estimate.
2. **`voelkel2024` (SDC) is a different domain.** It is used *only* for the shape of the
   decay (1.00 / 0.29 / 0.18) and for the money-vs-attitude ratio, never for a level.
3. **Sample composition.** voelkel2026, vlasceanu2024, koetke2024, gligoric2025, bago2025
   and agley2021 are unweighted quota/convenience online panels. Levels taken from them
   (belief, concern, policy, behaviour, donation) are *panel* levels, not population
   levels; TISP, GSS, Pew, ANES and CCAM rows are weighted. Prolific samples (bago, agley,
   koetke) skew liberal and young by roughly +5–8 pp on climate items.
4. **Format.** TISP/GSS/Pew items are 1–5, 3-pt and 4-pt; the target is a 0–100 slider
   throughout. ANCHORS_D §1a measured the format effect at **+3 to +6 pp** moving from a
   coarse agreement scale to a slider/thermometer; I applied only **+2** to the two
   constructs where the item text matches exactly (`policy_role_mean`, `inst_trust_mean`),
   because a bipolar semantic-differential slider and a "how much do you trust" slider are
   not the same instrument. If the parent prefers the full +6, add ~4 pp to every
   level in §4 that came from a 1–5 or 4-pt source.
5. **Year.** All levels are anchored to 2022–2024 readings. Trust in scientists fell
   ~8 pp between 2021 and 2024 (ANCHORS_D §5) and has not recovered; climate *attitudes*
   did not fall. If the target fields in 2026 the trust levels may be another 1–3 pp lower
   and the climate-attitude levels roughly flat.
6. **`rms_true = 0` is common** in `_e_sources.csv` — it means the observed spread of the
   ATEs is fully explained by sampling noise, not that the effect is exactly zero. Do not
   read a zero there as evidence of a null; read it as "this study cannot resolve it".
7. **Study recognition.** I recognise `voelkel2026`, `vlasceanu2024`, `voelkel2024`,
   `koetke2024` and `attari2016` as published work. Every number reported here was
   computed from the vendored microdata in this container; no remembered published figure
   was used, and no validation or target-study result was consulted.
