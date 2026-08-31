# ANCHORS_K — the two behavioural cells (`donation_ams`, `newsletter_signup`)

**Author:** `anchors-behav` (train-split analyst, independent read).
**Scope obeyed:** only `/workspace/datasets/**`, `/workspace/benchmark/**`, and (after forming my own
view) `/workspace/run/anchors/**` + `DESIGN.md`. No `inputs/val`, no `runs/`, no `idea01_lib`, no
retrieval of any kind. **Packages installed for the audit: `openpyxl` (3.1.5), `pypdf` (6.16.2).**
Every number below is in `_k_sources.csv` with its file, n, and formula; per-arm rows are in
`behavioural_ates.csv` (91 rows).

---

## 0. Headline answers

| quantity | centre | band | what sets it |
|---|---|---|---|
| `donation_ams` mean ATE over the 16 arms | **−0.7 pp** | **−2.0 … +0.6** | `voelkel2026` (design twin, identical placebo controls): −1.39 raw / **−1.69 ANCOVA** ± 0.90; `vlasceanu2024` WEPT −2.25 ± 0.63; partly offset by recipient alignment + lottery |
| `donation_ams` between-arm SD | **0.3 pp** | 0.0 … 0.8 | `voelkel2026` noise-corrected between-arm SD = **exactly 0.00** across 10 read-only message arms (raw 1.19 vs mean SE 1.65) |
| `newsletter_signup` mean ATE | **+0.4 pp** | **−1.2 … +1.8** | `vlasceanu2024` share +3.31 ± 0.71 at base 37.4 % → ~+1.9 pp at base 13 % → ×construct distance; against `koetke2024` S5 opt-in −8.0 ± 4.6 |
| `newsletter_signup` between-arm SD | **0.5 pp** | 0.2 … 1.2 | `vlasceanu2024` share corrected SD 1.17 pp at base 37.4 %, rescaled for base rate and for the target's far greater arm homogeneity |
| assumed `newsletter_signup` control base rate | **13 %** | 8 … 20 % | **not establishable from the train split** — stated so the ATE can be re-derived if it moves |

**Recommendation on the exact zero: do not predict an exact zero for `donation_ams`, and do not
predict +0.05 either. Predict a small negative (−0.7 pp).** Working: with ~1,000/arm and ~2,000
control, the scored truth is a *half* sample, so a `donation_ams` cell's truth carries SE ≈ 2.1 pp
(SD ≈ 38 pp of range). Under my posterior (mean −0.7, SD 0.9) the expected directional credit is
**0.62 for a negative prediction, 0.50 for an exact zero, 0.38 for a positive one.** A negative
also minimises expected squared error, because the posterior mean is negative. The parent's
current +0.05 is the *worst* of the three options: it forfeits the guaranteed half-credit of a
zero without buying the 0.62 of the correct sign.

---

## 1. Method

1. Column-scan **all 14 experimental train datasets** for any real behavioural follow-through
   variable (regex over `donat|petition|volunteer|sign.?up|subscri|newsletter|opt.?in|WEPT|
   dictator|cents|allocat|bookmark|upvote|click|follow|share`). The complete list found is in
   §2; there is nothing else (source K35).
2. For each, build the arm-level ATE vs that study's own control in **pp of that outcome's scale
   range**, with Welch SEs, plus a pooled treated-vs-control "common shift" and a
   **noise-corrected between-arm SD** = `sqrt(max(0, var(ATE) − mean(SE²)))`.
3. For each behavioural outcome, compute the **matched attitude ATE in the same respondents** and
   the ratio.
4. Then three mechanism tests that the earlier sibling did not run:
   **(i)** ANCOVA on pre-treatment attitudes (available in `voelkel2026`), which is the
   better-powered estimate; **(ii)** a **direct/indirect decomposition** — re-estimate the ATE
   holding *post*-treatment attitudes fixed; **(iii)** a **fatigue falsification** — correlate the
   arm-level behavioural ATE with the arm's reading time.

---

## 2. The complete train-split inventory of behavioural follow-through

| study | behavioural outcome | what it actually is | n (tr / ct) | pooled ATE (pp) | SE | corrected between-arm SD |
|---|---|---|---|---|---|---|
| **`voelkel2026`** | `Donation` | 0–100 **cents of a certain $1 of own pay**, split across 5 named climate NGOs, remainder paid to you; strictly the **last** DV | 10,127 / 3,046 | **−1.385** (ANCOVA −1.686) | 0.937 (0.897) | **0.000** |
| **`vlasceanu2024`** | `WEPTcc` | pages of a tedious number-screening task (0–8) that earns money **for an environmental fund**; near the end | 54,307 / 5,085 | **−2.248** | 0.628 | 2.451 |
| `vlasceanu2024` US | `WEPTcc` | same | 7,584 / 669 | **−3.626** | 1.761 | 2.714 |
| `vlasceanu2024` | `SHAREcc` | *"Are you willing to share this information on your social media? If yes, please do it now"* — **immediately after** the message | 40,101 / 3,905 | **+6.398** (+3.31 if "no social media"→0) | 0.838 (0.71) | 2.582 (1.169) |
| **`voelkel2024`** | `PA_DG` | dictator game: split **50 real cents** with an out-partisan **participant** | 26,340 / 5,568 | **+4.221** (pro-message direction) | 0.378 | 2.864 |
| **`koetke2024` S5** | `Behavior Follow` | *"After the survey, would you be interested in being sent information and tips…?"* | 467 / 150 | **−8.026** | 4.635 | 0.000 |
| `spampatti2023` | `WEPT_90` | same WEPT, 0–8 | 5,095 / 853 | +0.676 | 1.048 | 0.000 |
| `bago2025` | upvotes / bookmarks | engagement **with the stimulus feed itself** | 1,002 / 997 | +2.58 / −0.25 | 0.91 / 0.41 | n/a (2 arms) |

Nothing else exists. `gligoric2025`, `hackenburg2025`, `tappin2023`, `agley2021`, `attari2016`,
`geiger2026`, `gatewaybelief`, `schmidbetsch2019` have **no** behavioural follow-through variable.

Two design caveats that must be applied before reading the table:
* **`spampatti2023` has no neutral control** — its control also read the disinformation, so the
  contrast is message-vs-message and any *message-vs-nothing* common shift is differenced out.
  Its +0.68 is therefore not evidence against a common negative shift; it is silent on it.
* **`bago2025` is not a follow-through ask** — the "behaviour" is engaging with the stimulus, not
  doing something for a third party afterwards. It belongs in a different family.

---

## 3. Q(a) — sign and magnitude of behaviour relative to attitudes in the same respondents

| study | behaviour | behavioural ATE | matched attitude ATE | **ratio** |
|---|---|---|---|---|
| `voelkel2026` | donation → climate NGOs | −1.385 | +1.52 (mean of 8 outcomes) | **−0.91** |
| `vlasceanu2024` global | WEPT effort | −2.248 | +1.21 (belief/policy) | **−1.86** |
| `vlasceanu2024` US | WEPT effort | −3.626 | +3.86 | **−0.94** |
| `koetke2024` S5 | opt-in to info | −8.026 | +2.15 (METI trust) | **−3.73** |
| `vlasceanu2024` global | share the message | +6.398 | +1.21 | **+5.29** |
| `voelkel2024` | DG → out-partisan | +4.221 | +4.812 (thermometer only) | **+0.88** |

**There is no single ratio.** The sign is bimodal, and it splits cleanly on *what kind of act the
study asks for*, not on how "behavioural" it is:

* **Class A — the act IS the attitude, addressed to the entity the message was about, and it is
  elicited in the same frame as the attitude items.** `voelkel2024`'s dictator game: money to the
  out-partisan the message told you to feel warmer toward. It tracks the attitude at **0.88×**
  with arm-level **r = 0.832** over 26 arms (against the *independent* thermometer half — see the
  correction in §7). `vlasceanu2024`'s share-the-message sits here too: cheap, expressive,
  immediate, +6.4 pp.
* **Class B — the study makes a NEW request of the respondent, costing money or effort, on behalf
  of the cause the message just advocated, later in the survey.** `voelkel2026` donation,
  `vlasceanu2024` WEPT, `koetke2024` opt-in. All three are **negative**, and the two well-powered
  ones are −1.4 and −2.2 pp while the same respondents' attitudes moved **+1.2 to +1.5 pp up**.

The target's `donation_ams` is unambiguously Class B in structure (a new money request on behalf of
a third-party organisation) with a Class-A recipient (the very group the message is about). That
tension is the whole prediction problem, and I resolve it in §6.

### The quantitative form of the Class-B effect

Decomposing `voelkel2026` (K07/K08):

| path | estimate |
|---|---|
| total (ANCOVA on 8 pre-treatment covariates) | **−1.686 ± 0.897** (t = −1.88) |
| **direct** (also holding the 8 *post*-treatment attitudes fixed) | **−2.424 ± 0.906** (t = −2.67, p = 0.008) |
| indirect, through the raised attitudes | **+0.74** |

The identical decomposition on `vlasceanu2024`'s WEPT: total −2.18 ± 0.63, **direct −2.53 ± 0.63**,
indirect +0.35. (Post-treatment conditioning is not causal-mediation-safe; read it as a
description, not an identified mediation.)

Two very different behavioural asks, two different countries-mixes, two different stakes — and the
**direct effect is −2.4 and −2.5 pp**. That is the most reproducible number in this file, and it
gives a usable functional form:

> **beh_ATE ≈ −2.5 pp + ~0.5 × (attitude ATE)**

Check: `voelkel2026` att +1.5 → −1.75 (observed −1.39/−1.69 ✓). `vlasceanu` global att +1.2 →
−1.9 (observed −2.25 ✓). `koetke` att +2.1 → −1.4 (observed −8.0, but 1.4 SE away ✓).
It fails on `vlasceanu` US (predicts −0.6, observed −3.6) — see §4, where the US WEPT is
contaminated by effort depletion.

**The behavioural effect is therefore NOT a shrunken copy of the attitude effect.** It is a
roughly constant negative offset plus a modest positive pass-through. A bigger attitude effect
pushes it toward zero but does not, at realistic sizes, make it positive.

---

## 4. Q(b) — common shift or arm-specific noise? And is it fatigue?

**It is a common shift, and it is not fatigue** — in the study whose arms look like the target's.

* `voelkel2026`, 10 short read-only message arms: raw between-arm SD of the donation ATE = 1.188 pp,
  mean arm SE = 1.647 pp ⇒ **noise-corrected between-arm SD = exactly 0.000**. Nine of ten arms
  negative. The three placebo controls land at 61.01 / 61.61 / 62.00 — a 1-pp spread, exactly the
  sampling noise. So the donation cell carries **one number, repeated**, and no arm signal.
* Arm-level `corr(donation ATE, mean attitude ATE) = −0.276`, slope −0.40 (n = 10). The donation
  cell tells you nothing about which arm worked.
* **Fatigue falsified for `voelkel2026`:** `corr(donation ATE, median treatment reading time) =
  +0.077`; control reading times (58–84 s) sit *inside* the treatment range (51–156 s). The
  longest-read arm (Warmth, 156 s) has a donation ATE of −0.37, the near-zero of the set. Whatever
  produces the −1.4 is content, not depletion.
* **Fatigue confirmed for `vlasceanu2024`, and only there:** its arms differ enormously in effort
  (2 s to 350 s of writing/reading), and `corr(WEPT ATE, condition time) = −0.791`,
  `corr(WEPT ATE, SHARE ATE) = −0.612`. Its corrected between-arm SD is 2.45 pp — real, but it is
  an artefact of a design the target does not share. **The target's 16 arms are all short read-only
  texts, like `voelkel2026`'s.** So I import `voelkel2026`'s structure (SD ≈ 0), not
  `vlasceanu2024`'s.
* Party: `voelkel2026` donation ATE by party is D −0.33 ± 1.34, R −1.46 ± 1.47, "Neither"
  −5.05 ± 2.62. No credible party moderation of the donation effect (the "Neither" cell is a
  small-n outlier). I would predict **near-zero party moderation** on this cell.

---

## 5. Q(c) — mechanism

Ranked by how well each survives the data:

1. **Solicitation / persuasion-knowledge reactance (best supported).** A persuasive message
   followed by a request for money or effort on behalf of the same cause reframes the whole survey
   as a solicitation. Predicts: negative; independent of message content (so ≈ zero between-arm
   variance); not mediated by attitudes (so a *direct* effect that survives conditioning on them);
   not related to reading time. All four predictions hold in `voelkel2026`.
2. **Moral licensing / "I've already engaged" (partly supported, not separable from 1).** After
   forty sliders expressing climate support, the marginal dollar feels redundant. Predicts the same
   four signatures as (1); I cannot distinguish them with train data. Both are "the ask arrives
   after the respondent has already paid in attitude".
3. **Effort/attention depletion (supported only where the arms are effortful).** Explains
   `vlasceanu2024`'s arm ordering (r = −0.79 with reading time) and its larger negative, but is
   **falsified as an explanation of the `voelkel2026` common shift** and therefore should carry
   ~no weight for the target, whose arms are all short reads and whose donation item is **not at
   the end of the survey** (see §6, item 4).
4. **Stake size (no train evidence either way).** `voelkel2026` ($1, certain) and `voelkel2024`
   (50¢, certain) both show ~60 % of the endowment given; nothing in the split varies the nominal
   stake while holding everything else fixed. **I could not establish a stake effect.**
5. **Numeric anchor of the elicitation (no evidence, and it should not affect the ATE).** The
   target uses an 11-option horizontal grid with `$0` leftmost and no default; `voelkel2026` used
   five sliders starting at 0. Both anchor low. Anchors move the *level*, not plausibly the
   treatment *difference*.
6. **Floor effects (matters for the newsletter, not the donation).** `voelkel2026`'s donation is
   U-shaped (31.0 % at 0, 49.3 % at 100), i.e. the *opposite* of a floor: the mass is at the
   extremes and the measure is very responsive in principle. `newsletter_signup` at ~13 % sits
   where the binary's pp-efficiency is halved (§8).

---

## 6. Q — the recipient question, adjudicated

**Direct evidence: none. There is no train-split experiment in which money is offered to a
scientific society, and none in which the recipient's identity is randomised while the message is
held fixed.** That is the honest answer, and I state it plainly.

**Indirect evidence: one contrast, and it points positive, but it is confounded three ways.**

| study | recipient | is the recipient the message's subject? | behaviour vs attitude |
|---|---|---|---|
| `voelkel2024` | an out-partisan **person** | **yes** — the message is about out-partisans | **+0.88×**, r = 0.832 across 26 arms |
| `voelkel2026` | five climate **advocacy NGOs** | only obliquely — the message is about climate change, not about NGOs | **−0.91×**, r = −0.28 |
| `vlasceanu2024` | an environmental **fund** | no | −0.94 to −1.86× |

So the one case where the money went to *the entity the message was about* is the one case where
the money tracked the attitude. Confounds I cannot remove: (i) topic (democracy vs climate);
(ii) survey position (`voelkel2024`'s DG sat early, inside a randomised DV block; `voelkel2026`'s
donation was strictly last); (iii) **`PA_DG` is literally half of that study's own primary
animosity composite** — I use the independent thermometer half to get 0.88× and r = 0.83, which is
the defensible version of the claim (§7).

**Four target-specific facts I verified myself in `survey.qsf`, which move the number:**

1. **The $10 is a lottery — confirmed independently, I agree with the earlier sibling.** Verbatim
   (`QID1721185865`): *"After data collection is complete, we will randomly select **100
   participants** from this study to receive a $10 bonus payment."* With ~18,000 respondents,
   p ≈ 0.56 %; the expected cost of donating a dollar is **$0.0056**. This is a near-hypothetical
   allocation wearing a $10 label. Cheap acts behave more like attitudes ⇒ **push toward positive**.
2. **AMS is framed as the message's own subject.** *"a non-profit, non-partisan society of 12,000
   scientists and other professionals that supports climate change research… you help AMS to
   advance science for the benefit of society."* Sixteen near-synonymous messages arguing that
   climate scientists are competent, honest, benevolent and open, followed by an offer to fund a
   society of scientists. This is the `voelkel2024` alignment configuration ⇒ **push toward
   positive**.
3. **Counter-argument I take seriously:** the tighter the alignment, the more transparent the
   solicitation. "We told you to trust scientists, now give scientists money" is precisely the
   sequence that triggers persuasion-knowledge. Alignment is not unambiguously positive.
4. **NEW, and not in ANCHORS_I: neither behavioural item is at the end of the survey.** The
   `SurveyFlow` puts `donation` **and** `subscription newsletter` inside a
   `BlockRandomizer(7, EvenPresentation = false)` over the *secondary* outcome blocks (trust single
   post, donation, distrust single post, scientists' role, funding, institutional trust,
   newsletter), always **after** the primary 12-item trust battery and **before** the tertiary
   block. So each behavioural item lands at a *random* position in the middle of the post-treatment
   battery — on average considerably earlier than `voelkel2026`'s strictly-last donation. This
   (a) removes the end-of-survey depletion component, and (b) means half of respondents meet the
   newsletter offer before the donation and half after, which averages out across arms but adds
   within-cell variance ⇒ **small push toward positive** for `donation_ams`, and a caution that the
   two behavioural cells are not independent within a respondent.

**Assembly for `donation_ams`:**

```
direct solicitation effect                     −2.5   (voelkel2026 & vlasceanu2024, both −2.4/−2.5)
+ 0.5 × (target attitude ATE ≈ +2.5 pp)        +1.25
+ recipient alignment (voelkel2024, 1 study)   +0.4   (wide: 0 … +1.5)
+ lottery / near-zero felt cost                +0.2   (wide: 0 … +0.8)
+ not-at-end-of-survey (block randomised)      +0.0   (0 … +0.5; already inside the −2.5 spread)
------------------------------------------------------------
centre                                         −0.65  → report −0.7 pp
```
Band **−2.0 … +0.6**. `P(true sign is positive) ≈ 0.30`.

---

## 7. `newsletter_signup`

**Base rate.** **I could not establish this from the train split, and I say so.** No train dataset
contains an external-link subscription. The two in-survey single-click analogues are
`koetke2024` S5 at **44.0 %** and `vlasceanu2024`'s share at **53.5 %** (US control, "no social
media" → NA) / **41.4 %** ("no social media" → 0). The target requires leaving the survey, opening
an external tab, choosing a free tier and entering an email, then self-reporting it — one to two
orders of friction higher, partly offset by unverified self-report. I assume **13 %, band 8–20 %**,
and everything below scales with it.

**Why the base rate is not a detail.** A binary's ATE in pp of range is
`100·φ(Φ⁻¹(1−p))·(latent shift in SD)`. At p ≈ 0.44–0.53 (both train analogues) φ ≈ 0.40, the
maximum; at p = 0.13, φ = 0.212 — **53 % of the efficiency**. Importing a measured pp ratio from a
50 %-base-rate binary without this correction overstates the newsletter ATE by ~2×.

I independently re-derived and **ratify** ANCHORS_I's κ: regressing `voelkel2024`'s dichotomised
`SPV_D` arm ATEs on `100·φ(z*)·ΔSPV/sd_SPV` gives **r = 0.974, slope = 1.394** over 26 arms at a
13.9 % base rate — a base rate almost identical to my newsletter assumption. So the Gaussian
conversion works, with a ~1.4 inflation for latent right-skew.

**The two directional signals conflict, and I do not hide it:**

| source | act | base rate | ATE (pp) | rescaled to p = 13 % | comment |
|---|---|---|---|---|---|
| `vlasceanu2024` global, "no social media"→0 | share the message | 37.4 % | **+3.31 ± 0.71** | **+1.85** | but it is *the message itself*, immediate, zero-cost |
| `koetke2024` S5 | opt in to be sent info | 44.0 % | **−8.03 ± 4.64** | **−4.25** | but the message was that the scientist is *uncertain about her findings* — a content-specific reason to want the tips less |

I weight `vlasceanu` more (n = 44,006 vs 617) but discount it heavily for construct distance: the
target's ask is not "share what you just read", it is "subscribe to a third party's newsletter".
Applying a construct-distance factor of 0.2–0.5 to +1.85 gives **+0.37 … +0.93**; the `koetke`
signal and the Class-B solicitation penalty pull the lower end below zero.

**`newsletter_signup` mean ATE = +0.4 pp, band −1.2 … +1.8, at an assumed 13 % base rate.**
If the base rate is 20 %, multiply by 1.15; if 8 %, multiply by 0.78.

**Between-arm SD = 0.5 pp** (band 0.2–1.2): `vlasceanu`'s share has a corrected between-arm SD of
1.169 pp at 37.4 %, → 0.65 pp at 13 %, shrunk by ~0.7 because the target's 16 arms are far more
homogeneous (16 near-synonymous trust messages) than `vlasceanu`'s 11 (which included letter
writing and guided visualisation). I expect the warmth/parasocial arms (`Scientist community
helpers`, `Former skeptics`, the three named-scientist portraits/interviews) to sit at the top of
the newsletter ordering and the technical arms (`Measurement & modeling`, `Model accuracy`) at the
bottom — but that is a hypothesis, not a measurement, and 0.5 pp is inside the noise anyway.

Unlike the donation, I do **not** recommend an exact zero here: the expected directional credit for
+0.4 under my posterior is 0.577 vs 0.50 for a zero.

---

## 8. Where I agree and disagree with ANCHORS_I, cell by cell

Read after forming my own view. Every shared number I recomputed from the microdata.

| item | ANCHORS_I | me | verdict |
|---|---|---|---|
| $10 is a lottery, p ≈ 0.56 %, cost $0.0056/$ | yes | yes, verbatim from `QID1721185865` | **agree, independently confirmed** |
| AMS framing verbatim | yes | yes | **agree** |
| `voelkel2026` donation control 61.5 %, 31.0 % at 0, 49.3 % at 100 | yes | 61.54, 31.0 %, 49.3 % | **agree exactly** |
| `voelkel2026` donation ATEs −3.95…+0.53, mean −1.38, 9/10 negative | yes | identical | **agree exactly** |
| `voelkel2026` `sd_true ≈ 0` for donation | yes (raw 1.19 < mean SE 1.65) | corrected SD = 0.000 | **agree** |
| `koetke2024` S5 opt-in 44.0 %, arms −4.8/−9.4/−10.2 | yes | identical | **agree exactly** |
| `vlasceanu2024` US share 53.5 % / +7.70; "no social"→0 → 41.4 % / +4.30 | yes | 53.5/+7.70 and 41.4/+4.24 | **agree** (my +4.24 vs their +4.30 is a rounding/denominator nuance) |
| κ ≈ 1.4 from `SPV`→`SPV_D`, r = 0.974 | yes | r = 0.974, slope 1.394 | **agree, independently reproduced** |
| newsletter base rate 11.5 %, band 5–20 % | 11.5 % | 13 %, band 8–20 % | **agree in substance**; my centre is 1.5 pp higher because self-report of an unverified action inflates |
| newsletter ATE centre | +0.40 | +0.40 | **agree** |
| `voelkel2024` DG "moved with attitudes, ~0.9× the matched thermometer" | yes | 0.877× vs `PA_Out`, r = 0.832 over 26 arms | **agree — but with a correction** |
| — the correction | not noted | **`PA` ≡ (`PA_Out` + `PA_DG`)/2 exactly, for all 31,835 rows.** The DG is *half* of that study's own animosity composite, so any DG-vs-`PA` comparison is partly mechanical (r = 0.951). The defensible statement uses the independent thermometer half only: ratio 0.877, r = 0.832. | **new; ANCHORS_I's claim survives, its comparator does not** |
| `donation_ams` ATE centre | **+0.05**, P(positive) ≈ 0.45, "an exact zero is defensible" | **−0.7**, P(positive) ≈ 0.30, "an exact zero is dominated" | **disagree — this is the substantive disagreement** |
| `donation_ams` band | −1.2 … +0.8 | −2.0 … +0.6 | **disagree**: the band should be asymmetric downward, because both well-powered Class-B studies are negative and the ANCOVA (−1.69 ± 0.90) puts the twin's point estimate below their lower bound |
| donation between-arm SD | not stated | 0.3 pp (band 0–0.8) | **new** |
| the negative is a *direct* effect, not attitude-mediated | not tested | direct −2.42 ± 0.91 (v26), −2.53 ± 0.63 (vlasceanu) | **new, and it is what upgrades "one mechanism" from assertion to measurement** |
| fatigue as the explanation | implicitly plausible | **falsified for `voelkel2026`** (r = +0.08 with reading time; control reading times inside the treatment range), confirmed only for `vlasceanu2024` (r = −0.79) | **new** |
| position of the two behavioural items | treated as end-of-survey | **both are inside a 7-block randomiser over the SECONDARY outcomes**, never last | **new; corrects a shared background assumption** |
| `donation_ams` control level $4.40 | 61.5 − 8 − 8 + 5 + 3 | I did not re-derive it; it is outside my remit and I have no better anchor | **no opinion** — but note that the ATE band does not depend on it |
| donation response shape (tri-modal) | 0.288/…/0.175/…/0.217 | I re-checked their two shape inputs: `voelkel2026` U-shape (31.0 % at 0, 49.3 % at max) ✓, and `voelkel2024` **48.42 % exactly at the 50/50 midpoint** (15,449 / 31,908 non-missing) ✓ | **agree, both inputs reproduced**; their tri-modal reading is consistent with both sources |

---

## 9. What I could NOT establish

1. **The sign of the recipient-alignment effect for a scientific society.** No train experiment
   randomises the recipient, and none uses a scientific society. My +0.4 pp alignment adjustment
   rests on a *single* study (`voelkel2024`) with a different topic, a different survey position,
   and a partly mechanical comparator. If the parent wants one number to stress-test, it is this.
2. **The `newsletter_signup` control base rate.** Nothing in the split measures an external-link
   opt-in. 13 % is a construction, not a measurement, and it is the largest lever on the newsletter
   ATE.
3. **Whether stake size matters.** Both train allocation tasks are ~$0.50–$1.00 and both give ~60 %
   of the endowment. Nothing spans $1 → $10, and nothing spans certain → lottery.
4. **Whether the two behavioural items interfere with each other.** Because both sit in the same
   7-block randomiser, ~half of respondents are asked for money after being asked to subscribe and
   half before. Licensing between the two is plausible in either direction; I have no train
   analogue with two behavioural asks in one survey.
5. **Whether the −2.5 pp direct effect is reactance or licensing.** Their observable signatures are
   identical in these data.
6. **Any per-arm ordering for `donation_ams`.** `voelkel2026` says there is nothing to order
   (corrected between-arm SD = 0.000). I would not spend prediction variance on this cell.

---

## 10. Recognition disclosure

I recognise `vlasceanu2024`, `voelkel2024` and `voelkel2026` as published megastudies and I have a
general memory that the first reported weak or absent behavioural effects. **No remembered result
was used as a number.** Every figure in this file, including every sign, was computed in this
session from the vendored microdata (`data63.xlsx`, `data_notimers.csv`,
`SDC - Data - Recoded.csv`, `CCC - Data - Recoded.csv`, `Study5CleanData.csv`,
`Showdown_short.csv`, `anonim_df.csv`) with the formulas recorded in `_k_sources.csv`. Two
target-study facts (the lottery; the block randomisation of the behavioural items) come from
`/workspace/benchmark/survey/survey.qsf`, which is public template material, not human outcome
data. I encountered no human outcome data from the target study.
