# ANCHORS_H - the per-arm message score s(a) for the target megastudy

**Scope.** Train split (`/workspace/datasets/**`) + the target's public template
(`/workspace/benchmark/**`) only. No validation material, no `runs/`, no `inputs/idea01_lib/`,
no retrieval of any kind. One package install (`uv pip install pypdf openpyxl`) was needed to read
the vendored questionnaire PDFs and the voelkel2024 coding workbooks; that is the only network use.
Deliverables: this file, `arm_features.csv`, `arm_scores.csv`, `_h_sources.csv`.

---

## 0. Headline

**The train split does not support a confidently ordered s(a). It supports a mostly-flat s(a)
with a small, explicitly-reasoned tilt.**

Three findings drive that:

1. **Ceiling.** Across seven train message experiments the noise-corrected between-arm SD of the
   ATE is about **0.5 x the mean ATE** when it is detectable at all - and in the two studies whose
   arms are as narrowly matched as the target's (gligoric2025, whose outcome *is* trust in
   scientists; spampatti2023) the noise-corrected between-arm SD is **exactly zero**.
2. **Predictability.** Message features - mine, and the voelkel2024 authors' own expert codings
   with inter-coder r = 0.63-1.00 - predict out-of-sample arm rank at **r_adj ~ 0.0-0.25**, and in
   the leave-one-study-out test on the closest climate/trust studies the sign is **negative**
   (-0.37). Arm *type* does not carry a stable score across studies (r = -0.28 over the four types
   present in both climate megastudies).
3. **Backfire.** Across voelkel2026, vlasceanu2024, voelkel2024 and spampatti2023 (52 arms),
   **no arm was significantly net-negative**; point estimates were negative for 0-8% of arms. In
   hackenburg2025 only 2.3% of 577 competent messages were significantly negative. **No target arm
   should be predicted net-negative on the pooled ATE.**

Recommendation: keep the ordering below (correlation-type metrics are scale-free, so an ordering
with non-negative expected skill costs nothing), but **shrink the amplitude by lambda = 0.20
(defensible band 0.10-0.30)**, i.e. use `s_a_shrunk` (sd 0.12) wherever the entry's RMSE and
calibration beta are at stake.

---

## 1. Method

1. Read all 16 target intervention texts in full from `/workspace/benchmark/survey/questionnaire.txt`
   (cross-checked against `condition_codenames.csv` and `codebook.csv`), and coded every arm on a
   23-column scheme (`arm_features.csv`).
2. For each usable train experiment: extracted per-arm ATEs against that study's own control from
   the vendored microdata, converted to percentage points of each outcome's scale range, and formed
   a within-study standardised arm score (within-outcome z, averaged over outcomes) plus its
   sampling SE.
3. Coded the train arms on the *same* scheme from the vendored stimulus materials (voelkel2026
   Qualtrics questionnaire PDF, vlasceanu2024 `usa_1.qsf`, gligoric2025 `Qualtrics file.qsf`), and
   fitted feature -> within-study arm score with **leave-one-study-out** validation.
4. Independently tested feature -> arm effect where a ready-made high-quality coding exists
   (voelkel2024's two expert coders, 25 arms, leave-one-arm-out) and where the message count is
   large enough for real power (hackenburg2025, 682 messages, 10 issues, leave-one-issue-out).
5. Computed noise-corrected between-arm variance everywhere (observed variance of arm effects minus
   mean sampling variance), so the "ceiling" claims are not inflated by sampling noise.

---

## 2. Feature scheme

Codeable from the text alone, deliberately small, and the same for target and train arms.

- `n_words` - participant-visible word count (for the state-adaptive arm, one case + intro).
- `f_competence`, `f_integrity`, `f_benevolence`, `f_openness` in {0, 0.5, 1} - does the text make
  an explicit claim about that trust facet of climate scientists? `facet_coverage` is their sum.
  This is the **assertion-match** feature: how much of the outcome battery the arm actually talks about.
- `elicit_correct` - the arm asks the respondent to state a belief/estimate, then corrects it.
- `consensus_norm` / `social_proof_norm` - expert agreement / public-trust norm content.
- `named_individual`, `first_person`, `narrative_story` - portrait/interview/testimonial form.
- `process_transparency`, `admits_uncertainty` - describes how the work is done, admits error/revision.
- `numeric_evidence` - specific statistics carry the argument.
- `attack_outgroup`, `politically_coded_left`, `identity_bridge_right` - villain framing; left-coded
  moral framing; explicit bridge to a conservative audience.
- `benevolence_frame`, `practical_benefit`, `third_party_endorsement`, `self_praise`, `threat_dire`.
- `distrust_prime` - the text voices the distrust claim (or makes the respondent endorse it) before
  refuting it.
- `moralized_emotive` in [0,1] - moral/emotional load, the continuous analogue of hackenburg2025's
  `emotion_proportion` and `moral_nonmoral_ratio`.

---

## 3. Train-split results

### 3.1 The ceiling: how much true between-arm variance is there at all?

| study | arms | family / outcome | mean ATE (pp) | noise-corrected between-arm SD (pp) | ratio SD/mean |
|---|---|---|---|---|---|
| gligoric2025 (conservatives only) | 5 | **trust in scientists** (35 occupations, 1-7) | +0.20 | **0.00** | 0 |
| spampatti2023 | 6 | climate belief (inoculation arms) | +0.50 | **0.00** | 0 |
| vlasceanu2024 US | 11 | climate belief/policy/behaviour | +2.96 | 0.00 (too noisy) | - |
| vlasceanu2024 global (n=59,440) | 11 | same | +1.69 | 0.88 | 0.52 |
| voelkel2026 (ANCOVA, 8 attitudes) | 10 | climate attitudes | +1.19 | 0.67 | 0.56 |
| voelkel2024 (PA) | 25 | partisan animosity | +4.70 | 2.98 | 0.63 |
| voelkel2024 (PA/ADA/SPV avg) | 25 | democratic attitudes | +1.65 | 1.36 | 0.82 |
| hackenburg2025 (legible+on-topic) | 577 msgs / 10 issues | policy attitudes | +6.64 | ~3.0 (median issue) | 0.45 |

Reading: **true arm-main-effect SD ~ 0.5 x mean ATE** is the central case, but the two studies with
the most target-like arm sets (five ~40-word trust messages; six inoculation variants) show
**no detectable between-arm variance whatsoever**. The target's 16 arms are all substantial
(91-690 words) and all about climate scientists, i.e. narrower than voelkel2024's arm space
(chatbots, meditations, films) and wider than gligoric2025's.

### 3.2 Do features predict arm rank?

| test | design | out-of-sample skill (r_adj) |
|---|---|---|
| hackenburg2025, 7 text metrics, LOSO by issue, all 682 messages | includes degenerate small-model messages | **+0.41** |
| hackenburg2025, same, restricted to legible + on-topic messages | the regime the target is in | **+0.24** |
| voelkel2024, 11 expert-coded content features, leave-one-arm-out | PA / ADA / SPV | **+0.13 / -0.04 / +0.36** |
| voelkel2024, single features, leave-one-arm-out | 33 feature x outcome fits | 25 of 33 **negative** |
| ANCHORS_H scheme, 26 climate/trust arms, leave-one-study-out, multivariate | voelkel2026 + vlasceanu2024 + gligoric2025 | **-0.37** (negative in all 3 held-out studies) |
| ANCHORS_H scheme, best single feature (politically_coded) | same | +0.22 |
| arm-*type* transfer between the two closest climate megastudies | 4 types present in both | **-0.28** |

The only positive, replicable feature signals in the whole train split are:

- **Coherence / on-topic-ness** (hackenburg2025: legible messages +4.2pp over illegible ones,
  on-topic +5.0pp). Irrelevant for the target - all 16 arms are professionally written.
- **Emotional and moral load, negatively.** Among legible+on-topic messages, a 1 SD increase in
  `emotion_proportion` is worth **-2.09pp** (t = -3.48) and `moral_nonmoral_ratio` -0.82pp
  univariate (t = -2.57), against a mean ATE of 6.6pp. This is the single most statistically
  reliable text-level regularity available and it says: **more emotive/moralised is not better.**
- **Length is null**: -0.91pp/SD (t = -1.35) multivariate, +0.09pp/SD (t = 0.28) univariate in
  hackenburg2025; +0.29 sd-units (LOSO r = 0.03) in the climate studies. **Do not reward length.**

Everything else - narrative vs statistical, named source, consensus, threat, contact, exemplar,
production quality, engagingness - fails to transfer, usually with a negative out-of-sample sign.

### 3.3 Two matched contrasts that *are* informative

- **Myth-first penalty.** voelkel2026 ran two scientific-consensus arms. Consensus Framing I leads
  by restating and debunking a specific denialist artefact (the "31,000 signatures" petition);
  Consensus Framing II leads with the evidence and mentions the manufactured-doubt strategy later.
  Standardised arm scores: **-0.71 vs +0.76** (delta = 1.47 sd units, SE ~ 0.29). Same study, same
  outcomes, same construct: the version that puts the accusation first is much worse.
- **Norm correction on a trust outcome.** gligoric2025's `Norms` arm ("over 70% of conservative
  respondents report high confidence in scientists") was the **best of its five arms**
  (s_obs = +1.27), though the study-level between-arm SD is zero, so this is a weak, non-significant
  signal - the only direct train evidence about a public-trust-norm message on a trust outcome.

### 3.4 Backfire

Significantly net-negative arms: **0/10** (voelkel2026), **0/11** (vlasceanu2024), **0/25**
(voelkel2024), **0/6** (spampatti2023); 2.3% of 577 competent messages in hackenburg2025. The worst
point estimate anywhere in a megastudy was -0.78pp (voelkel2024 `Partisan_Threat` on partisan
animosity). Notably, the arm carrying an *anti-scientist aside* - voelkel2026's Binding Framing
("...without believing every single word that comes out of a government scientist's mouth") -
was the **worst of its ten arms** but still positive in absolute terms.

**Conclusion for the target: flag risk, do not predict a negative pooled ATE for any arm.** The
plausible negative territory is subgroup-level (Republicans x a left-coded arm), which is
ANCHORS_F's object, not s(a)'s.

---

## 4. From evidence to shrinkage

For a standardised predictor and standardised truth, the MSE-optimal multiplier is the expected
correlation `rho` between them. Pooling the four honest out-of-sample estimates
(+0.24 hackenburg, +0.15 voelkel2024 mean, -0.37 my LOSO, -0.28 type-transfer), and giving extra
weight to hackenburg (by far the most arms) and to the fact that my s(a) is *not* a fitted feature
model but an assertion-match argument that the LOSO test cannot evaluate:

**rho_hat = 0.20, 80% interval [0.05, 0.35]. Recommended lambda = 0.20.**

Two practical consequences for the parent model
`ate(a,o) = level(o) + KAPPA * s(a) * L(o) + A(a,o)`:

1. **Correlation metrics are scale-free.** Spearman rho, Pearson r and r_within are unchanged by
   lambda. So the *ordering* should be kept at full strength; shrinking it buys nothing on the
   r-family and can only hurt if it collapses to a constant (which would make r_within undefined).
2. **RMSE and calibration beta are not.** The arm-main-effect SD implied by the entry should be
   about **lambda x 0.5 = 0.10 x the mean |ATE| of that outcome** (band 0.05-0.20), i.e. if the
   predicted mean ATE on trust_multidimensional is ~2pp, the predicted spread across the 16 arms
   should have SD ~0.2pp, not ~1pp. `s_a_shrunk` (sd = 0.12) is the version to use when KAPPA is
   already calibrated against an unshrunk sd-0.6 score.

---

## 5. The delivered s(a)

`arm_scores.csv`; `s_a` is standardised to mean 0, sd 0.60; `s_a_shrunk = 0.20 * s_a`.
The ordering is built from four components, in descending order of evidential support:

| component | weight | evidence |
|---|---|---|
| `facet_coverage` (assertion match to the trust battery) | +0.40 / facet | **no direct train validation** - features do not transfer; justified only by the fact that 12 of the target's outcome items name a specific trust facet and the arms differ hugely in which facets they even mention |
| `moralized_emotive` | -0.30 | hackenburg2025, 577 messages, t = -3.48 (the strongest text-level result available) |
| `distrust_prime` | -0.25 | voelkel2026 matched Consensus-I/II contrast, delta 1.47 sd units |
| `politically_coded_left` | -0.25 | weak: mirror image of the +0.22 LOSO signal on `politically_coded` in three climate studies (train arms were mostly right-coded and scored positive) |
| `social_proof_norm` | +0.25 | gligoric2025 `Norms` best of five, non-significant |
| `identity_bridge_right` | +0.15 | same, non-significant |
| `third_party_endorsement` | +0.10 | same, non-significant |
| `elicit_correct` | -0.10 | n=1: vlasceanu2024 `PluralIgnorance` was the worst of its 11 arms |
| **length, narrative form, numeric evidence, named source, threat** | **0.00** | tested and null or non-transferring - deliberate exact zeros |


| rank | code_name | title | s_a | s_a_shrunk | conf. | reasoning |
|---|---|---|---|---|---|---|
| 1 | `flimsy fish` | Interview Prof. Maraun | +0.965 | +0.1931 | medium | Only arm asserting all four trust facets at once (self-correction=openness, "not pushing a message"=integrity, model improvement=competence); first-person scientist voice; no distrust priming. |
| 2 | `honored haddock` | Peer-review | +0.678 | +0.1355 | medium | Process-transparency + accountability content maps directly onto openness/integrity items; short, unemotional, no myth repetition; mild self-praise ("toughest test") is the only debit. |
| 3 | `complicated cockroach` | Portrait Prof. Cherry | +0.634 | +0.1269 | low | Benevolence+competence portrait of an ordinary community scientist; no numbers, no politics, no distrust mention; ordering driven by assertion-match only, hence low confidence. |
| 4 | `giant gibbon; brick bobcat` | Corporate reliance | +0.390 | +0.0780 | low | Third-party (insurer) endorsement is a costly-signal argument for competence AND non-ideological integrity; business framing is right-friendly; reflection prompt adds elaboration. |
| 5 | `practical planarian` | Extreme weather predictions | +0.303 | +0.0607 | medium | Competence+benevolence+practical benefit, state-personalised; no partisan or distrust content; the only arm with tailored relevance, which is a dose-not-content advantage. |
| 6 | `limping llama; friendly frog` | Former skeptics | +0.303 | +0.0607 | low | Identity-bridge testimonials (registered Republican meteorologist, conservative ex-congressman) give the largest expected Republican-side headroom; but narrative/testimonial content did not transfer in train. |
| 7 | `heartfelt hummingbird` | Interview Prof. Sebille | +0.282 | +0.0564 | low | Benevolence+integrity in the scientist's own voice, but the most emotionally loaded of the interview arms and mentions vulnerable populations (mild left coding); emotive penalty applied. |
| 8 | `jealous jaguar` | Consensus | +0.181 | +0.0362 | medium | Consensus + elicit-then-correct; strong on competence, weak on integrity/benevolence/openness; includes a genuine-disagreement item (66%) which is honest but dilutes; elicitation penalty. |
| 9 | `apple aardvark` | Model accuracy | +0.030 | +0.0060 | low | Strong competence claim (verified 50-year forecasts) and admitted error, but leads by restating the "models can't predict" criticism (myth-first penalty from the matched Consensus-I/II contrast). |
| 10 | `periwinkle partridge` | Scientist community helpers | -0.071 | -0.0141 | low | Pure benevolence/community frame with little competence or integrity content; warm and emotive; assertion-match to the benevolence items only. |
| 11 | `orchid orangutan; defiant dragonfly` | Measurement & modeling (2) | -0.143 | -0.0285 | medium | Competence-only exposition, jargon-dense (disdrometers, wavelet analysis); asserts rigour/reproducibility but says nothing about motives, openness or care. |
| 12 | `phony parrotfish` | Funding | -0.157 | -0.0314 | low | High facet-match on integrity/openness (salary and funding transparency) but forces respondents to state agreement with two accusations first; distrust-priming and elicitation penalties cancel the match. |
| 13 | `perfect prawn` | Measurement & modeling (1) | -0.473 | -0.0947 | medium | Longest pure-description arm; competence only, no trust claim of any kind; closest analogue in train to "informative but off-construct" arms. |
| 14 | `crushing chicken; gross grasshopper; homely halibut` | High public trust | -0.826 | -0.1652 | low | Zero direct facet content (it is a second-order belief correction), but it is the single arm type with direct train support on a trust outcome (gligoric2025 Norms arm was the best of five, n.s.), so it is held well above the bottom of the facet-only ordering. |
| 15 | `worse wildfowl` | Oil industry misinformation | -1.027 | -0.2055 | low | Longest, most adversarial arm: opens by voicing distrust, attacks an out-group, high emotive/moral load - the two text properties with the most reliable negative sign in the train split (hackenburg2025). |
| 16 | `difficult dog` | Social justice | -1.070 | -0.2141 | medium | Explicitly left-coded us-vs-them redistribution frame with the highest moral/emotive load; highest risk of Republican-side alienation; weakest facet coverage per word. |

Notes on the two ends:

- **Top.** `flimsy fish` (Interview Prof. Maraun) is the only arm that asserts all four facets at
  once, in the scientist's own voice, with no myth repetition and no partisan colour. `honored
  haddock` (Peer-review) is the cleanest openness/integrity process argument. These two are where
  assertion-match and the (weak) text-level evidence agree.
- **Bottom.** `difficult dog` (Social justice) and `worse wildfowl` (Oil industry misinformation)
  carry the highest moral/emotive load *and* out-group attack *and* (for the latter) an explicit
  distrust opening - three of the four negatively-signed components at once.
  `crushing chicken; ...` (High public trust) is last on facet coverage but pulled up by the only
  direct trust-outcome train datum; treat its position as the least stable in the table.
- **Ties broken arbitrarily** between ranks 5/6 (`practical planarian`, `limping llama; friendly
  frog`), which have identical scores to three decimals.

### Arms flagged for net-negative risk

None at the pooled-ATE level (see 3.4). Ranked by risk, and *only* as a subgroup/variance flag:

1. `difficult dog` (Social justice) - explicit redistribution framing, "the wealthiest 10%",
   scientists cast as partisans in a fight; the only arm that could plausibly be negative among
   Republicans. Train evidence for backfire *being real*: voelkel2024's `Partisan_Threat`
   (-0.78pp on the primary outcome) and voelkel2026's Binding Framing (worst of ten, and the only
   climate arm containing an anti-scientist aside). Train evidence for backfire being *rare*:
   0 significant negatives in 52 megastudy arms.
2. `worse wildfowl` (Oil industry misinformation) - repeated distrust priming across ~700 words.
3. `phony parrotfish` (Funding) - makes respondents endorse two accusations on sliders before the
   correction; the endorsement act is itself a commitment.

---

## 6. Uncertainty, and what I could not establish

- **The ordering is not validated.** Every honest out-of-sample test I ran on the train split
  returned r_adj between -0.37 and +0.24. The delivered ordering rests mainly on assertion match,
  which the train split **cannot** test, because no train study varies *what is asserted about
  scientists* while measuring *trust in scientists* on a full facet battery. If assertion match is
  wrong, s(a) is noise and the correct answer is exactly flat.
- **Out-of-support features.** Five of my features (`process_transparency`, `admits_uncertainty`,
  `self_praise`, `named_individual`, `elicit_correct`) appear 0 or 1 times among the 26 coded train
  arms. The target's arm space - portraits of scientists, peer review, funding transparency - is
  largely disjoint from the train megastudies' arm space, which varies *climate framing*. This is
  the deepest limitation of this anchor and is not fixable with the vendored data.
- **Dose could not be separated from study.** gligoric2025's ~40-word manipulations produced a
  study-level null and voelkel2026's ~300-700-word arms did not; but within study, word count is
  null. I therefore assert only the within-study version (no length term) and note that all 16
  target arms are in the "substantial dose" regime.
- **Facet-specific ordering not delivered.** I score arm *main* effects only. Whether e.g.
  Peer-review beats Portrait Cherry specifically on `trust_openness` is an arm x outcome
  interaction A(a,o); ANCHORS_E/G own that, and nothing here should be read as an A(a,o) claim.
- **`Extreme weather predictions` is state-adaptive** and the four case texts are near-identical in
  structure; I coded the common content. Its personalisation advantage is asserted, not measured.
- **spampatti2023 arm labels** were not verified against the QSF (numeric condition codes only);
  it is used for the ceiling statistic only, where labels do not matter.
- **voelkel2024 is off-topic** (democratic attitudes). It is used as evidence *about feature
  transferability*, not as evidence about climate messaging.

---

## 7. Recognition disclosure

I recognise several of these train datasets as published papers and, for some, I have general prior
knowledge of their headline claims (e.g. that megastudy message effects are small and homogeneous;
that scaling model size yields diminishing persuasion returns; that inoculation studies report
modest effects). **No remembered result entered any number in this anchor.** Every statistic above
was computed in-session from the vendored microdata and stimulus files listed in `_h_sources.csv`.
Two specific places where recognition and computation could have been confused, and how I handled them:

- **gligoric2025.** I computed a large *negative* effect for all five arms before reading the
  authors' script and discovering that only conservatives were randomised. The corrected,
  conservatives-only estimate (~0, true between-arm SD 0.00) is what is reported. The correction
  came from the vendored `R Code Main Study.R`, not from memory.
- **voelkel2026 / vlasceanu2024.** Arm names are recognisable intervention families from the
  literature. I coded features from the vendored stimulus text and took effects from the vendored
  microdata; I did not consult or rely on any recollection of which arm "won" in either paper.

No validation-set material was read. No web, repository or literature retrieval was performed.

---

## 8. Reproduction notes

- Kernel-side analysis only; one install: `uv pip install pypdf openpyxl` (PDF and XLSX readers).
- Target texts: `/workspace/benchmark/survey/questionnaire.txt`, lines 197-737.
- voelkel2026 stimulus texts: `CCC - Questionnaire - Qualtrics.pdf` (the non-Qualtrics
  questionnaire only points at the SI, which is not vendored).
- vlasceanu2024 stimulus texts: `materials/usa_1.qsf` (the `master_survey.pdf` has a broken font
  encoding and extracts as glyph indices - do not use it).
- gligoric2025 stimulus texts: `Main Study/Materials/Qualtrics file.qsf`.
- All noise corrections are `var(arm effects) - mean(sampling var)`, clipped at zero; the
  cross-outcome correlation of sampling error is ignored, which makes the reported noise floors
  slightly *conservative* (true SDs if anything smaller).
