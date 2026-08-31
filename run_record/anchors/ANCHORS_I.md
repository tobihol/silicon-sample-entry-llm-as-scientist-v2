# ANCHORS_I — the two behavioural cells, and the adjudication of OPEN ITEM A9

Sub-agent job, train-split only. Sources: `/workspace/datasets/**`, `/workspace/benchmark/**`
(public template: instrument, qsf, codebook), and prior `anchors/*.md|*.csv`.
No validation data, no `runs/`, no `inputs/`, no web, no retrieval of any kind.
Package install used: **`pyreadstat`** (via `uv pip install --python <kernel python>`), to read
`gss7224_r3a.dta` and `ATP_W42.sav`; `pypdf` was already present. Nothing else was installed.

All numbers below are in **percentage points of the item's scale range** unless a dollar sign
or a "%" is attached. Machine-readable companions: `donation_shape.csv`,
`behavioural_levels.csv`, `_i_sources.csv`.

---

## 0. Headline answers

| outcome | control level | band | control sd | \|ATE\| centre (pp) | ATE band (pp) |
|---|---|---|---|---|---|
| `donation_ams` | **$4.40** (44 pp) | $3.30 – $5.50 | 3.83 ($) | **+0.05** | −1.2 … +0.8 |
| `newsletter_signup` | **11.5 %** | 5 – 20 % | 0.319 | **+0.40** | −0.4 … +1.0 |
| `trust_multidimensional` | **65.0** | 61 – 69 | **21** | +1.00 | +0.2 … +2.0 |
| `trust_post` | **66.0** | 61 – 71 | 28 | +1.05 | +0.2 … +2.2 |
| `distrust_post` (not reversed) | **32.0** | 26 – 40 | 28 | −0.75 | −1.6 … 0.0 |

**A9 verdict: ANCHORS_D (60–67) is closer than ANCHORS_E (69).** Recommended 65, band 61–69.
E's 69 is ~4 pp high for three separable reasons, each of which I could measure:
(a) E credited the 0–100 slider format with **+2 to +4 pp**; the only within-split calibration
of that bridge gives **+1.0 pp** (§3.3);
(b) E used a climate penalty of −4 to −5; three independent measurements put it at
**−4 to −10, best estimate −5.5** (§3.2);
(c) E applied **no** 2023→2026 time decrement; GSS gives **−1.5 pp** (§3.4).

---

## 1. Method

Every estimate is built as an explicit decomposition, one term at a time, each term measured
against a named train-split source with its own uncertainty, and then re-assembled. Where two
routes to the same quantity exist I report both and average them with stated weights instead of
picking the one I like. Binary-vs-continuous comparisons are made in **two** units: raw
percentage points of scale range (what the benchmark scores) and latent-SD units (what
transfers across base rates), because the two answer different questions and the environment
scores the first while generalisation lives in the second.

The latent-threshold conversion used throughout is

&nbsp;&nbsp;&nbsp;&nbsp;`ATE_binary_pp = 100 · φ(z*) · κ · δ`,&nbsp;&nbsp;`z* = Φ⁻¹(1−p)`,&nbsp;&nbsp;`ATE_continuous_pp = sd · δ`

with `δ` the shift in latent SDs and `κ` a skew correction. **This is not assumed — it is
validated in §2.3 on `voelkel2024` at r = 0.974 across 26 arms**, with `κ ≈ 1.4`.

---

## 2. Q1 and Q2 — the two behavioural cells

### 2.1 What the target's stimulus actually is (from `survey.qsf`, not from the codebook line)

Two facts in the qsf change the priors and are not in `codebook.csv`:

1. **The $10 is a lottery, not a payment.** `QID1721185865`: *"After data collection is complete,
   we will randomly select **100 participants** from this study to receive a $10 bonus payment.
   If you are selected, the amount you allocate to yourself will be paid to you as a bonus, and
   the amount you allocate to the organization will be donated on your behalf."* With ~18,000
   respondents the selection probability is ≈ 0.56 %, so the **expected cost of donating a
   dollar is ≈ $0.0056**. This is a nominally-$10, effectively-near-hypothetical allocation.
2. **AMS is described warmly and explicitly de-politicised.** `QID1721185866`: *"a non-profit,
   **non-partisan** society of 12,000 scientists and other professionals that supports climate
   change research … you help AMS to advance science for the benefit of society."* The choice is
   an 11-option single-answer horizontal grid, and the instruction enumerates three focal
   options: *"keep all $10 / donate all $10 / or choose any split in between."*
3. **Newsletter signup is a real external action, self-reported.** The offer page links out to
   an external Substack in a new tab; the scored item is the respondent's own report that they
   subscribed. Friction is high (leave the survey, enter an email, choose the free tier) but
   verification is zero, so the measured rate is *action rate + over-report − abandonment*.

### 2.2 `donation_ams`

**(a) The control mean.** Two well-powered train-split allocation tasks bracket the construct:

| source | task | control level | n |
|---|---|---|---|
| `voelkel2026` | 100 cents of a **certain $1**, split across 5 famous environmental NGOs (TNC, WWF, EDF, NRDC, Sierra Club) + keep | **61.5 %** of the endowment (sd 45.3) | 3,046 |
| `voelkel2024` | dictator game, self vs an out-partisan | **61.4 %** (sd 24.9) | 31,908 |

Both land at 61 %. The target differs on four axes; my adjustments, each signed and sized:

| axis | direction | size |
|---|---|---|
| single **obscure** recipient (AMS) vs five household-name charities | ↓ | −8 |
| **$10 nominal** vs $1 nominal (share given falls with nominal stake) | ↓ | −8 |
| **lottery** payment (p ≈ 0.006) vs certain payment — near-zero felt cost | ↑ | +5 |
| context: the item follows a 12-item trust battery about climate scientists, and AMS is framed as *supporting climate research* | ↑ | +3 |
| discrete 11-point grid vs a 5-slider allocation | ≈ 0 (reshapes, see (b)) | 0 |

61.5 − 8 − 8 + 5 + 3 ≈ **44 % ⇒ $4.40**. Band **$3.30 – $5.50**. Confidence: **low** — this is an
extrapolation across a stake change, a recipient change and an incentive-structure change that
no train dataset spans, exactly as ANCHORS_E warned.

**(b) The response shape** (`donation_shape.csv`, control arm, integers 0…10):

| $ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| p | **.288** | .050 | .065 | .055 | .035 | **.175** | .030 | .030 | .035 | .020 | **.217** |

mean 4.38, sd 3.83, and it is **tri-modal, not Gaussian and not U-shaped**. The three spikes and
their relative sizes come from data, not from folklore:

- **Floor spike.** `voelkel2026` control: 31.0 % gave exactly 0 with five famous charities and a
  $1 stake. A single obscure recipient at a $10 stake cannot give *less* zero-mass; 0.288 is if
  anything conservative. (I hold it just under 0.31 because the lottery structure lowers the
  felt cost.)
- **Ceiling spike.** `voelkel2026` had 49.3 % at the maximum — but that is a **$1** maximum. The
  ceiling spike is the single most stake-sensitive feature of allocation tasks; I cut it to
  0.217. This is the largest single judgement call in the file and it is where the mean is most
  fragile: moving `p(10)` by ±0.05 moves the mean by ±$0.50, i.e. the whole band.
- **Midpoint spike.** `voelkel2026` shows a clean 50/50 spike (4.2 % at exactly 50 against
  neighbours at 0.1–0.5 %, i.e. ~10× the local density). `voelkel2024`'s self-vs-other dictator
  shows the *same* mechanism at industrial scale: **48.4 % choose exactly 50**. The target's
  instruction explicitly names "any split in between", which licenses the equal split. I set
  0.175 — between voelkel2026's weak charity midpoint and voelkel2024's dominant self-vs-other
  midpoint, because the target's frame is keep-vs-donate (charity-like) but with the split made
  salient (dictator-like).
- Interior mass tilts toward small token gifts ($2–$3 > $6–$7), with a small bump at $8; this is
  the ordinary shape of an 11-point give/keep grid and is the least-constrained part.

**(c) The ATE band, and whether the sign is even positive.** It is not reliably positive.

`voelkel2026` is the only well-powered climate-domain donation experiment in the split, and it
is the design twin: 10 message arms × ~1,065, donation ATEs run **−3.95 … +0.53, mean −1.38 pp,
nine of ten negative**, while *the same arms* moved belief +1.42 and concern +1.70. Money moved
**opposite** to attitudes. The between-arm sd (1.19) is below the mean standard error (1.65), so
`sd_true ≈ 0`: this is one common negative shift, not arm heterogeneity — which makes it a
*mechanism* (post-persuasion reluctance to also pay), not a fluke of one arm.

Against that, `voelkel2024`'s dictator moved with attitudes (mean |ATE| 4.38, ~0.9× the matched
thermometer) — but there the money was *directly about the manipulated object* (an out-partisan).
The target sits in between: AMS is a scientific society, so the money is closer to the
manipulated construct (trust in climate scientists) than a climate charity was to a climate
message, which is the argument for not simply importing −1.38.

Recommendation: **centre +0.05 pp (≈ $0.005/arm), band −1.2 … +0.8 pp**, P(true sign positive)
≈ 0.45. Predicting an exact zero here is defensible and earns half directional credit; predicting
a confidently positive donation effect is the single most likely way to lose this cell.

### 2.3 `newsletter_signup`

**(a) Control rate: 11.5 %, band 5–20 %.** No train dataset measures an external-link
newsletter opt-in, so this is built bottom-up and cross-checked:

- The closest *in-survey* opt-ins are far higher and are not comparable: `koetke2024` S5's
  "follow this scientist's work" checkbox = **44.0 %**; `vlasceanu2024`'s "willing to share this
  on social media" = **53.5 %** (US control). Both are single-click, in-survey, unverified. The
  target requires leaving the survey and completing an external subscription — one or two orders
  of friction higher.
- Composition check: with the census-quota party mix (~45 % D / 13 % I / 42 % R) and plausible
  by-party rates of 19 / 10 / 4 %, the aggregate is **11.6 %**. Two independent constructions
  landing at 11–12 % is why I keep ANCHORS_E's 12 rather than moving it, but I narrow the band
  from 4–25 to 5–20.
- Self-report inflates and abandonment deflates; they partly cancel. If the target's fieldwork
  used any nudge or reminder the rate could reach 20 %; if the external tab is a hard barrier it
  could fall to 5 %.

**(b) ATE band: −0.4 … +1.0 pp, centre +0.40 pp.** Derivation in (c).

**(c) The measured binary-vs-slider responsiveness ratio — this is the part that should change
the parent's model.**

First, the threshold conversion is *validated*, not assumed. `voelkel2024` reports both `SPV`
(continuous, sd 20.3) and `SPV_D` (its dichotomisation, base rate 13.9 %) for the same 26 arms.
Regressing the observed dichotomised ATE on `100·φ(z*)·(ΔSPV/sd_SPV)`:

> **slope 1.405, r = 0.974, 26 arms.**

So the Gaussian conversion recovers the binary ATE almost perfectly up to a scale factor
κ ≈ 1.4, the factor arising because the latent is right-skewed (real density at the threshold
exceeds the Gaussian φ). This is the single most useful measurement in this file.

Second, the two genuine binary-behaviour-vs-attitude-scale experiments:

| study | binary | base rate | binary ATE (pp) | scale ATE (pp) | **ratio in pp** | **ratio in latent SD** |
|---|---|---|---|---|---|---|
| `vlasceanu2024` US | willing to share on social media | 53.5 % | +7.70 | belief slider +4.54 (sd 31.8) | **1.70** | **1.36** |
| `vlasceanu2024` global | same | 48.5 % | +6.52 | belief slider +1.33 (sd 24.6) | **4.91** | **3.02** |
| `vlasceanu2024` US, "no social media"→0 | same | 41.4 % | +4.30 | +4.54 | 0.95 | 0.77 |
| `koetke2024` S5 | opt in to follow the scientist | 44.0 % | −4.8 / −9.4 / −10.2 | METI +1.6 / +3.1 / +1.9 | **negative** | **negative** |

Three conclusions, in order of how much they matter:

1. **"A binary is scale-efficient" is a base-rate statement, not a property of binaries.** All
   four measurements above sit at base rates of 41–54 %, i.e. at `φ(z*) ≈ 0.39–0.40`, the
   *maximum* of the density — the most pp-efficient point a binary can occupy. The target's
   newsletter sits at ~11.5 %, where `φ(z*) = 0.194`, **half** the efficiency. Importing a
   measured ratio of 1.7–4.9 from a 50 %-base-rate binary to a 12 %-base-rate binary would
   overstate the newsletter ATE by ~2×.
2. **The right formula, with the parent's 0.45 recovered but re-derived:**

   > `resp_pp(newsletter) = [100 · φ(Φ⁻¹(1−p)) · κ / sd_primary] × η_construct`
   > `= [100 × 0.194 × 1.4 / 21] × η_construct = 1.29 × η_construct`

   With `η_construct` (construct distance from trust-in-climate-scientists to a climate-newsletter
   opt-in) at 0.2–0.5, centre 0.35 — the same 2–3-step decay ANCHORS_E fits for the distal
   attitude outcomes — this gives **0.26 … 0.65, centre 0.45 pp**. The parent's 0.45 multiplier
   is *numerically right and mechanically wrong*: it is not scale efficiency (which is ~0.9–1.3
   here), it is scale efficiency **×** construct distance, and it will break if the assumed base
   rate moves. **Recommend replacing the flat 0.45 with the formula**, so that a revision of the
   11.5 % base rate automatically revises the ATE: at p = 0.05 the factor falls to 0.65×, at
   p = 0.20 it rises to 1.15×.
3. **Sign is not locked.** `koetke2024` S5 raised measured trust and *lowered* the opt-in in all
   three arms (−4.8, −9.4, −10.2 pp, n ≈ 155/arm, |t| ≈ 1–1.8). Combined with `voelkel2026`'s
   donation result, the pattern across the split is that **persuasive messages reliably move
   attitudes up and behavioural follow-through down or nowhere**. My ATE band therefore opens
   below zero (−0.4) even though the centre is positive.

Answer to the parent's literal question — *does a message that moves an attitude slider by X pp
of its range move a binary opt-in by more or less than X pp?* — **more, if the binary sits near
50 % (measured 1.7–4.9× in `vlasceanu2024`); about the same or less if it sits near 10–15 %
(0.8–0.9× scale efficiency), and then less again after construct distance (≈0.3–0.5×).**

---

## 3. Q3 — OPEN ITEM A9 adjudicated

### 3.0 Why this is tractable at all

`tisp` carries **the target's own instrument**. Checking
`core-questionnaire_english.pdf` against `codebook.csv` item by item: **ten of the twelve items
are verbatim** with only the referent swapped ("most scientists" → "most climate scientists") —
honest/dishonest, ethical/unethical, sincere/insincere, concerned about people's wellbeing,
eager to improve others' lives, considerate of others' interests, open to feedback, willing to
be transparent, attention to others' views, intelligent/unintelligent. The two that differ:
TISP's *"how expert or inexpert"* → target's *"how incompetent or competent"*, and TISP's
*"how qualified … when it comes to conducting high-quality research"* → target's bare
*"how unqualified or qualified"*. TISP's `CLIM_TRUST` — *"To what extent do you trust scientists
in your country who work on climate change?" (Not at all … Very strongly)* — is the target's
`trust_post` item with the referent generalised and the format coarsened.

So the target's primary outcome = TISP's scale, **referent-shifted** and **format-shifted**,
fielded ~3 years later in a quota sample. Four correction terms, each measured separately.

### 3.1 Term (i): the generic-scientist level in the target's own wording

`tisp` US, n = 2,559, weighted by `WEIGHT_CNTRY`, fielded 2022–23:

| | mean | se | sd |
|---|---|---|---|
| **12-item composite** | **71.52** | 0.41 | 20.62 |
| competence facet | 78.60 | 0.41 | 20.60 |
| integrity facet | 71.06 | 0.45 | 22.29 |
| benevolence facet | 70.35 | 0.45 | 22.66 |
| openness facet | 66.05 | 0.50 | 24.99 |
| `TRUST_PEW` (generic single confidence item) | 70.95 | 0.56 | 28.12 |

Weighting barely moves it (unweighted 71.69). **Term (i) = 71.5 ± 0.5** (the sampling
uncertainty is negligible next to every other term).

Two structural facts worth carrying: the **facet ordering** competence ≫ integrity ≈ benevolence
> openness, with competence sitting **+7.1** above the composite; and the near-equality of the
12-item composite and the single generic confidence item (+0.6), which is what lets me move
between single-item and composite anchors below. The **Pew W42** environmental-scientist battery
reproduces the same offset independently: reweighting its five items to the target's four-facet
structure gives a composite of 69.4 with "does a good job conducting research" at 75.4, i.e.
competence **+6.1** above the composite.

### 3.2 Term (ii): the climate-referent penalty — **−5.5 pp, band −2 to −10**

Three independent measurements, in ascending magnitude:

| measurement | design | penalty |
|---|---|---|
| `pew_atp` W42 2019: environmental research scientists vs medical research scientists, **same 5 items, same 2,226 people** | within person | **+0.4** (se 0.56) |
| `tisp` 2022–23: `CLIM_TRUST` vs the 12-item generic composite, **same 2,557 people** | within person | **−4.50** (se 0.46) |
| `tisp`: `CLIM_TRUST` vs `TRUST_PEW` (single vs single) | within person | **−3.92** (se 0.48) |
| `gligoric2025` 2024 control (n=2,248): climatologists (61.8) vs the 35-occupation grand mean (71.8) | within person, between labels | **−9.9** |

Reading them together:

- The Pew reading is a **lower bound**: "environmental research scientist" is not politicised the
  way "climate scientist" is, and 2019 predates the post-2020 trust collapse.
- The gligoric reading is an **upper bound**: its items are *credible / trustworthy* only (a
  global evaluative pair, not a four-facet battery), respondents rate 35 occupation labels in one
  rapid grid so contrast effects are amplified (oceanographers 75.8 vs climatologists 61.8 — a
  17.5 pp spread inside one grid), and "climatologist" is a rarer label than "climate scientist".
  A useful calibration falls out of it though: its 35-occupation grand mean (71.8) coincides with
  TISP's generic composite (71.5), so the −9.9 is a *label* effect, not a format or sample effect.
- TISP's −4.0 to −4.5 is the best-identified estimate but measures the penalty on a **global
  trust** item, not on a descriptive attribute battery.

I take **−5.5**, TISP-weighted and shaded down toward gligoric, because the facets most likely to
carry an extra climate-specific penalty (integrity, openness) are 6 of the 12 items in the target
composite but 0 of the 1 item in `CLIM_TRUST`. I could *not* establish that asymmetry directly —
see §5.

### 3.3 Term (iii): the response-format effect — **+1.0 pp, band −2 to +3. Not +2 to +4.**

This is where E's 69 mostly comes from and it does not survive measurement.

`vlasceanu2024` asks, **of the control condition only**, two 0–100 sliders about climate
scientists (US n = 581/628, 2022, quota panel, untreated):

- *"On average, how competent are climate change research scientists?"* → **68.71** (sd 27.09;
  9.0 % at exactly 100, 25.3 % ≥ 90, 1.4 % at 0, 2.8 % at 50)
- *"On average, how much do you trust scientific research about climate change?"* → **67.86**
  (sd 28.82; 10.0 % at 100)

Quantile-matching TISP's weighted `CLIM_TRUST` category shares (10.3 / 7.5 / 21.7 / 25.1 / 35.5 %)
onto that slider ECDF gives the empirical realisation map

> `E[slider | 5-pt category] = 7.3 / 29.2 / 57.7 / 76.9 / 94.0` (vs the linear 0 / 25 / 50 / 75 / 100)

i.e. sliders **pull the top box down from 100 to ~94** and **push the bottom box up from 0 to
~7** — the top-box pile-up is 35.5 % on the 5-point item but only 9–10 % at exactly 100 on the
slider. Applying that map to TISP's pooled 12-item category shares
(3.5 / 6.4 / 22.7 / 35.2 / 32.2 %) gives **72.52 against the linear 71.52: a format effect of
+1.0 pp**, positive because the 12-item composite has much less bottom-box mass than `CLIM_TRUST`
does, so the floor lift outweighs the ceiling haircut.

ANCHORS_D's "+6 pp for a 0–100 format" came from the ANES **feeling thermometer** (78.0 with
29.4 % at exactly 100). A thermometer is a warmth rating with a notorious 100-pile; it is not the
same instrument as a bipolar-anchored attribute slider, and it should not be used as the bridge.
**Recommend retiring the +2…+4 slider bonus and using +1 ± 2.**

### 3.4 Term (iv): time trend 2022–23 → 2025–26 — **−1.5 pp, band −4 to +1**

`gss` `consci`, weighted (`wtssps`), recomputed here: 2018 70.75 → 2021 70.33 → **2022 63.15** →
**2024 62.16**. The collapse happened in 2021–22; the 2022→2024 slope is only −0.5 pp/yr. TISP
was fielded across 2022–23, i.e. after the collapse. Linear extrapolation of the post-collapse
slope to a 2025–26 field date gives **−1.5 pp** relative to TISP. The band is asymmetric upward
because climate *attitudes* did not fall at all in the same window (CCAM "happening" 71.2 → 71.4
across 2008–2024) and because a 2025–26 US context of federal science-funding conflict plausibly
*raises* Democratic trust while lowering Republican trust, with a near-zero net.

### 3.5 Term (v): census-quota opt-in sample vs probability panel — **0 ± 3 pp, weakest term**

I could not identify this cleanly and I am reporting it as unresolved rather than inventing a
number. What I could establish:

- Within TISP, weighting changes the composite by **0.17 pp** (71.69 unweighted → 71.52 weighted),
  so the *weighting* half of the term is negligible for a scale like this one.
- `gligoric2025` (2024, quota, unweighted) has a 35-occupation grand mean of **71.8**, sitting on
  top of TISP's weighted 71.5 — no visible quota-panel penalty at the aggregate.
- The `vlasceanu2024` US control sample is **not** liberal-skewed (mean social-ideology slider
  55.4/100, i.e. slightly right of centre), so its 68.7 is not inflated by composition.
- Counter-signal: `koetke2024`'s Prolific samples put a 14-item trust scale at 79.6–82.7, far
  above any probability benchmark — but the referent there is a specific scientist in a vignette,
  not "most scientists", so it does not identify a sample effect either.

The target quotas on **age, gender and race/ethnicity only** — not party, education or income —
so composition on the two variables that matter most for this outcome is uncontrolled. That is a
real source of level risk that no amount of train-split work removes.

### 3.6 Assembly, two independent routes

**Route A (TISP-anchored, weight 0.55):**
71.5 (generic) − 5.5 (climate) + 1.0 (format) − 1.5 (time) + 0 (sample) = **65.5**

**Route B (direct slider anchor, weight 0.25):** `vlasceanu2024`'s 0–100 slider competence item
about climate scientists = 68.7 in 2022. Converting a competence reading to the four-facet
composite requires subtracting the competence offset, measured twice independently (TISP +7.1,
Pew W42 +6.1); "competent" is the softest of the target's three competence items so I use +5.
68.7 − 5.0 − 1.5 (time) = **62.2**. (If "competent" behaves instead like TISP's "expert" item,
+1.9, this route gives 65.3 — the route's own internal spread is ±1.5.)

**Route C (`geiger2026`/Većkalov, weight 0.08):** US control cell, trust in climate scientists
1–7, raw 80.3 but composed of 78 left-leaning vs 28 right-leaning respondents. Re-weighting to a
CCAM-like ideology split (26 / 41 / 31) gives **71.3**; −1.5 time → 69.8. n = 125, low weight.

**Route D (`gligoric2025`, weight 0.12):** climatologists 61.8 in a 2024 quota sample on a
credible/trustworthy pair; adjusting +2 toward a four-facet composite and −1 for time → **62.8**.

Weighted: 0.55(65.5) + 0.25(62.2) + 0.08(69.8) + 0.12(62.8) = **64.9**.

> **`trust_multidimensional` control level = 65.0, band 61–69.**

### 3.7 `trust_post`, `distrust_post`, and the composite's SD

**`trust_post`** — *"How much do you trust climate scientists?" 0 = not at all … 100 = very
strongly*. This is `CLIM_TRUST` with the format changed. Three anchors:
`tisp` `CLIM_TRUST` 67.0 (weighted, 2022–23) + 1.0 (format) − 1.5 (time) = 66.5;
`vlasceanu2024` `Trust_sci2_1` 67.9 (slider, 2022) − 1.5 = 66.4;
Većkalov re-weighted 71.3 − 1.5 = 69.8 (n = 125).
> **`trust_post` = 66.0, band 61–71, sd 28** (single items: TISP `CLIM_TRUST` sd 32.5 on 5-pt,
> vlasceanu sliders 27.1 and 28.8).

Note this puts `trust_post` **1 pp above** the composite, where ANCHORS_E put it 2 pp *below*.
The justification is that for *generic* scientists in TISP the global single item and the 12-item
composite are within 0.6 pp of each other, so there is no general "single items read lower" rule
to import; the composite is dragged down by its openness facet while the global trust item is not.

**`distrust_post`** — *"How much do you distrust climate scientists?"*, **not reverse-coded**,
so higher = more distrust. No train-split source measures a trust/distrust item pair, so this is
the least-evidenced of the five and I say so. Structural reasoning: for a well-anchored
complementary pair on the same 0–100 grid the two means sum to slightly under 100 (ambivalent
respondents place both near the middle; strong trusters floor the distrust item), typically
95–99. With `trust_post` at 66 that gives **32**, band **26–40**, sd 28. Expect a **large floor
spike** (~20–25 % at exactly 0) — this matters for the Section-3 OVL/KS/W1 metrics far more than
the mean does. Its ATE is the trust ATE reflected: **−0.75 pp centre**, and the sign must be
negative wherever `trust_post` is positive (the ANCHORS_E valence rule is correct and I confirm
it: the item is *not* reversed in cleaning, unlike `funding_perceptions`).

**Control SD of the primary composite.** Three estimates:
TISP's 12-item composite has sd 20.6 on the 5-point grid; the empirical slider map applied
item-by-item gives 17.0, and adding the measured within-category slider dispersion (variance
40.3 per item, correlated across items at ρ ≈ 0.2–0.5) brings it back to 17.3–17.6 — but that
map was calibrated on a distribution with a much fatter bottom tail than the composite has, so it
under-disperses. A composition build-up is more trustworthy: with the census-quota party mix and
a party gap of ~28 pp on this construct (D ≈ 78 / I ≈ 64 / R ≈ 50 at .45/.13/.42), between-party
sd ≈ 13.1 and within-party sd ≈ 17–18, giving **√(170 + 289…324) ≈ 21.4–22.3**.
> **Recommend control sd = 21, band 18–24.** (For comparison, `voelkel2026`'s multi-item 0–100
> slider composites run sd 22–29 and TISP's single items run sd 22–28.)

---

## 4. What changed relative to ANCHORS_D / ANCHORS_E

| item | D | E | **here** | why |
|---|---|---|---|---|
| `trust_multidimensional` level | 60–67 | 69 | **65 (61–69)** | slider bonus +1 not +3; climate penalty −5.5; −1.5 time |
| `trust_post` | — | 67 | **66** | direct `CLIM_TRUST` anchor; now *above* the composite, not below |
| `distrust_post` | — | 34 | **32** | complement of a 66 trust level, sum ≈ 98 |
| composite control sd | — | — | **21** | new |
| slider-vs-Likert format bonus | +6 (thermometer) | +2…+4 | **+1 (−2…+3)** | quantile-matched map, TISP × vlasceanu |
| `donation_ams` level | — | $3.40 | **$4.40** | lottery structure (p ≈ 0.006) found in the qsf; two 61 % allocation anchors |
| `donation_ams` shape | — | "bimodal" | **tri-modal, `donation_shape.csv`** | midpoint spike is 4 %(voelkel2026) to 48 %(voelkel2024) — cannot be omitted |
| `newsletter_signup` level | — | 12 % | **11.5 % (5–20)** | band narrowed; party build-up cross-check |
| `newsletter_signup` responsiveness | — | flat 0.45 | **formula: 1.29 × η, centre 0.45** | 0.45 is base-rate × construct-distance, not "scale efficiency" |
| binary↔continuous conversion | — | asserted | **validated r = 0.974, κ = 1.4** | `voelkel2024` SPV vs SPV_D |

---

## 5. What I could NOT establish

1. **The facet-differential climate penalty.** I assumed climate scientists lose more on
   integrity/openness than on competence. `pew_atp` W42 gives the *opposite* within-person result
   for environmental vs medical scientists (env is rated **better** on "admits mistakes" +2.1 and
   "transparent about conflicts of interest" +1.8, worse on "does a good job" −1.8), and
   `gligoric2025` shows no meaningful gap between its credible and trustworthy items for
   climatologists (control arm: 62.5 vs 61.2). So the assumption is unsupported and possibly backwards. If it
   is backwards, the composite penalty is smaller than −5.5 and the level moves toward 67.
2. **The quota-panel/mode effect (term v).** Reported as 0 ± 3 with the evidence in §3.5. It is
   the term I would most want a held-out check on.
3. **Any direct anchor for `distrust_post`.** No train dataset has a trust/distrust item pair.
   The 32 is a modelled complement, not a measurement.
4. **The `donation_ams` ceiling spike.** `p(10) = 0.217` is a stake-scaled guess off
   `voelkel2026`'s 0.493 at a $1 stake; no train dataset spans a $1→$10 stake change in the same
   task. The mean is roughly linear in this one parameter.
5. **Whether the newsletter self-report over- or under-states the true action rate.** Both
   directions are plausible and neither is measurable here.
6. **`hackenburg2025`, `spampatti2023`, `agley2021`, `attari2016`, `tappin2023`, `bago2025`
   contributed nothing to Q2** — none pairs a genuine spontaneous behavioural binary with an
   attitude scale under the same randomisation. `bago2025`'s upvote/bookmark are forced
   per-headline tasks (concurring with ANCHORS_E); `spampatti2023`'s and `vlasceanu2024`'s WEPT
   are effortful-task counts, not opt-ins.

---

## 6. Recognition disclosure

Every dataset used here is on the **train** split, where reading outcomes is explicitly
permitted, and every number in this file was computed from the vendored microdata in this
session — none is quoted from memory. For completeness:

- I recognise `tisp` as Cologna et al.'s TISP Many Labs trust-in-scientists study,
  `vlasceanu2024` as the global climate-intervention tournament, `voelkel2024` as the
  Strengthening Democracy Challenge, `voelkel2026` as the climate-messages megastudy,
  `koetke2024` as the intellectual-humility/trust experiments, `gligoric2025` as the
  scientist-occupation trust study, and `pew_atp`/`gss`/`anes`/`ccam`/`wellcome` as the standard
  public series. I did not consult any recollection of their published numbers; every statistic
  above is reproducible from the file paths and column names listed in `_i_sources.csv`.
- **Target study:** I have general awareness that megastudies on trust in climate scientists
  exist as a genre, and the benchmark template names its instrument openly. I have **no**
  knowledge of the target study's human results, pilots, preprints or toplines, I did not seek
  any, and nothing in this file is derived from anything but the train split and the public
  template.
- No web access, no remote repositories, no literature lookup was attempted at any point. The
  only network use was `uv pip install pyreadstat`.
