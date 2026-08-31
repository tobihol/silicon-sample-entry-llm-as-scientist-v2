# ANCHORS_M — recipient alignment on the behavioural cells (`donation_ams`, `newsletter_signup`)

**Author:** `anchors-align` (train-split analyst, independent read of open item A14's residual).
**Scope obeyed:** read only `/workspace/datasets/**`, `/workspace/benchmark/**`,
`/workspace/run/anchors/**`. I did not open `inputs/val/**`, `runs/**`, `inputs/idea01_lib/**`,
or the target entry files. No retrieval of any kind.
**Packages installed this session (the one permitted network use):** `pypdf`, `openpyxl`
(via `uv pip install --python <kernel> pypdf openpyxl`).
Every number is in `_m_sources.csv` (27 rows) with file, n and formula; the coded inventory is
`recipient_alignment.csv` (122 rows, one per study × behavioural outcome × arm).

---

## 0. Headline

| quantity | my answer | ANCHORS_K / current entry |
|---|---|---|
| **recipient alignment: sign and size** | **REAL, POSITIVE, and large: +4.29 ± 0.61 pp of scale range (7.1σ)** between a costly follow-through whose recipient IS the message's subject and one whose recipient is an aligned but non-subject cause | "+0.4, wide 0…+1.5, one confounded contrast, cannot close it" |
| **clean WITHIN-study contrasts that vary recipient alignment** | **exactly one** (`voelkel2026`'s 5-recipient menu), and it does **not** span the subject / non-subject boundary. Zero train studies randomise the recipient. The subject-vs-cause comparison is strictly **between** studies. | — |
| **`donation_ams` mean ATE** | **−0.4 pp**, band **−1.6 … +1.1** | −0.70 (entry), −1.4 (the direct-path reading) |
| **recommendation** | **do NOT move to −1.4.** Keeping −0.70 is defensible and cheap (0.3 pp from my centre, inside my band). If the parent wants my number it is **−0.4**. | — |
| **`donation_ams` between-arm SD** | **≈ 0.88 × τ(trust ATE)**, i.e. ~0.35–0.45 pp, **not an exact zero** — but unscoreable either way | 0.000 / "no arm ordering to predict" |
| **`newsletter_signup`** | **keep +0.45**; my own read +0.6, band −1.0 … +2.0. The money offset does **not** contaminate the click cell. | +0.40 / +0.45 |

---

## 1. The complete inventory, coded

Independent column-name regex over every csv/xlsx in `/workspace/datasets` (M27) reproduces
ANCHORS_K's list exactly: there are **seven** behavioural follow-through outcomes in the split and
nothing else. Coded on the parent's fixed scale:

| study | outcome | recipient | relation to the message | cost | position | control level (pp) | ATE (pp) | **DIRECT** (pp) |
|---|---|---|---|---|---|---|---|---|
| `voelkel2024` | `PA_DG` | an anonymous **out-partisan participant** | **subject_of_message** | 50¢, certain | randomised DV block, mid-battery | 35.45 | **+3.95 ± 0.35** | **+1.97 ± 0.32** |
| `vlasceanu2024` | `SHAREcc` | the respondent's **own network**; the act IS the message | own_network / the message itself | one click | immediately after the message | 48.48 | **+6.42 ± 0.84** | **+5.65 ± 0.81** |
| `voelkel2026` | `Donation` (menu of 5) | five climate **NGOs** | aligned_cause | $1 of own pay, certain | strictly LAST | 61.54 | **−1.39 ± 0.94** | **−1.85 ± 0.91** |
| `vlasceanu2024` | `WEPTcc` | **Eden Reforestation Project** (1 tree/page) | aligned_cause | 8 pages of tedium | near end | 62.48 | **−2.25 ± 0.63** | **−2.55 ± 0.63** |
| `koetke2024` S5 | `Behavior Follow` | the **respondent** (info sent to self) | self | one radio button | after the trust battery | 44.00 | **−8.03 ± 4.64** | **−8.54 ± 4.56** |
| `spampatti2023` | `WEPT_90` | Eden Reforestation Project | aligned_cause | effort | near end | — | — | **uninformative** (no neutral control; the reference arm also read the disinformation) |
| `bago2025` | upvote / bookmark | none — the stimulus feed itself | n/a | click | during stimulus | — | — | **excluded** (engagement with the stimulus, not a follow-through ask) |

`DIRECT` is one identical specification everywhere: `behaviour ~ treat + post-treatment matched
attitude(s)`, OLS, individual level (M08, M14, M17, M18, M19). It is the treatment effect on the act
that does **not** run through the attitude the message moved. It is descriptive, not an identified
mediation, and I use it only to compare studies on one footing.

**Two corrections to ANCHORS_K's table.** (i) `voelkel2024` gives **38.6 %** of its endowment
(raw `PA_DG_1` mean 19.297 of 50¢; control arm 35.45 %), not ~60 % — the recoded `PA_DG` is
reverse-scored, `100 − 2×raw` (M12). ANCHORS_K's §5 item 4 ("both give ~60 %") is wrong, and with it
the claim that nothing in the split varies the level of giving: the split spans 35 %–62 %.
(ii) `voelkel2026`'s donation ATE is **−1.385 ± 0.937**, so its own reported ±0.90 SE understates
nothing, but the ANCOVA −1.686 they quote and my post-conditioning −1.848 are different estimands
and should not be averaged.

---

## 2. The one clean within-study contrast: `voelkel2026`'s five recipients

`voelkel2026` splits **100 cents across five named climate NGOs** with the remainder paid to the
respondent (M01). Message set, sample, position and stake are held exactly fixed; only the recipient
varies. This is the only clean recipient contrast in the split, and it delivers three findings.

**(a) The treatment reallocates money between recipients, and it is a large effect.**
Among donors, shares of the donated dollar move (M04):

| recipient | control share | share ATE (pp) |
|---|---|---|
| World Wildlife Fund | 35.49 % | **−1.683 ± 0.438** |
| Environmental Defense Fund | 15.07 % | **+0.673 ± 0.255** |
| Sierra Club | 13.72 % | +0.448 ± 0.256 |
| The Nature Conservancy | 22.21 % | +0.344 ± 0.325 |
| Natural Resources Defense Council | 13.51 % | +0.060 ± 0.220 |

Essentially the **entire** −1.39 pp total donation effect is the WWF cell (−1.35 of −1.39): the other
four recipients are flat or positive. A "the messages just suppress giving" story cannot produce that.

**(b) The reallocation runs along the alignment axis, not along a "shed the default" axis.**
The obvious rival explanation is that treatment makes people deliberate and the modal brand loses.
I break the tie with a measurement that uses **control respondents only**, so it cannot be
contaminated by the treatment: the slope of each recipient's cents on the respondent's own
pre-treatment climate attitude (M06).

| recipient | elasticity (cents per SD) | as % of that recipient's level |
|---|---|---|
| Environmental Defense Fund | +4.374 ± 0.259 | **+47.2 %** |
| Natural Resources Defense Council | +3.542 ± 0.241 | +42.2 % |
| Sierra Club | +2.686 ± 0.269 | +31.8 % |
| The Nature Conservancy | +2.474 ± 0.372 | +18.0 % |
| World Wildlife Fund | **−1.994 ± 0.528** | **−9.2 %** |
| *total given* | +11.082 ± 0.796 | +18.0 % |

WWF is the recipient that climate-**un**concerned respondents pick; EDF/NRDC/Sierra are the
recipients concerned respondents pick. The treatment reallocation vector is that vector, scaled
down. So the recipient shift is the **alignment** axis: money moves toward the recipients that the
attitude the message raised actually predicts. Within the five, the per-recipient *direct* effect
tracks the elasticity: slope **+0.078** % of level per % of elasticity, bootstrap 95 % CI
[−0.059, +0.209], **P(slope > 0) = 0.86** (M09, M10). Suggestive on n = 5, not decisive.

**(c) Message *content* does not steer the recipient at all.** The noise-corrected between-arm SD
of the share ATE is **exactly 0.000 for all five recipients** across the ten message arms (M05).
Free-market framing does not push money to the market-based NGO; consensus framing does not push it
to the research NGOs. **Alignment is a property of the treatment-vs-control contrast, not of which
message you read.** That is a genuinely new negative result and it constrains the mechanism: what
changes is "which cause now feels like mine", uniformly across messages.

**(d) What this contrast cannot do.** All five recipients are on the *cause-aligned* side; none is
the message's subject; and the total is constrained to $1, so a *share* gain is substitution inside
a menu and says nothing directly about whether a **solo** aligned recipient would receive more in
total. The elasticity of the **total** is +18.0 %/SD — the same as the median recipient. So this
contrast establishes that alignment is real and orders recipients, but it cannot price the
subject-vs-cause step.

---

## 3. The subject-vs-cause step: between studies, and it is big

Because no train study randomises the recipient across that boundary, I price it with the one
specification applied identically to all five usable outcomes (§1), which puts the two poles on the
same footing:

* **subject-aligned pole** — `voelkel2024`, money to the very out-partisan the message told you to
  feel warmer toward: **direct = +1.97 ± 0.32 pp**. Stable at +1.97 / +2.05 / +2.05 with 1, 3 and 12
  post-treatment attitude covariates (M14), so it is **not** an artefact of a poorly-measured
  covariate — that was my main worry and it is dead.
* **cause-aligned pole** — `voelkel2026` (−1.85 ± 0.91) and `vlasceanu2024` WEPT (−2.55 ± 0.63),
  inverse-variance pooled: **direct = −2.32 ± 0.52 pp** (M21). Two different countries-mixes, two
  different act types (money, effort), same answer.
* **swing = +4.29 ± 0.61 pp, 7.1σ** (M22).

A third, independent point sits *beyond* the subject pole: `vlasceanu2024`'s **SHARE**, where the
act is the message itself, at **+5.65 ± 0.81**. And the arm-level pass-through slopes agree with the
same ordering (M24): `voelkel2024`'s behaviour inherits the attitude ordering at **0.743, r = +0.83
over 25 arms**, while `voelkel2026`'s inherits nothing (slope −0.50, r = −0.42, on a study whose
between-arm τ is 0 for *everything*, see §5).

**So the answer to the parent's question is: yes.** A costly follow-through whose recipient is the
subject/beneficiary of the message behaves *very* differently — the sign of the direct offset flips.
ANCHORS_K's "+0.4, band 0…+1.5" understates it by an order of magnitude **as an estimate of the
alignment effect between those two configurations**.

### The three confounds, and why I still do not take the whole +4.29 to the target

1. **Topic** — democracy vs climate. Irremovable.
2. **Recipient type** — an anonymous *person* vs an *organisation*. This is the one that matters
   most. `voelkel2024`'s dictator game is money to the individual you were just told to like; it is
   an **expression** of the attitude, in the same currency. The target's AMS donation is a
   **charitable request from an institution**. Those are different acts that both happen to score
   high on "recipient = message subject".
3. **Position** — `voelkel2024`'s DG sits in a randomised DV block, `voelkel2026`'s donation is
   strictly last. No block-order variable survives in either deposit, so I could not test position;
   note that this confound pushes the *same* way as alignment for the target, whose donation item is
   also block-randomised mid-battery.

And there is a mechanism argument that cuts **against** importing the subject pole. ANCHORS_K's
best-supported mechanism is solicitation / persuasion-knowledge. That mechanism is *stronger*, not
weaker, when the beneficiary of the ask is the message's own subject: "we spent five paragraphs
telling you climate scientists are honest and benevolent — now give a society of scientists your
money" is exactly the sequence that makes a survey read as a fundraising pitch. `voelkel2024`'s DG
escapes it because the recipient is a fellow participant, not an institution asking for funds. The
target does **not** escape it.

---

## 4. `donation_ams`: centre, band, recommendation

Assembly (all in pp of scale range; `total = direct + pass-through`, the identity that holds
exactly in both source studies):

```
pass-through  = elasticity x Delta(attitude in SD)
              = 11.0 pp/SD (voelkel2026 total, M06) x ~0.048 SD
                (the campaign's own trust centre +1.0 pp on a control SD ~21 pp,
                 behavioural_levels.csv)                                  = +0.53
              x level correction 44/61.5 (if the offset scales with level) = +0.40   [band +0.2 .. +0.7]

direct        = w * (+1.97)  +  (1-w) * (-2.32)          w = weight on the subject pole
```

| w | 0.15 | 0.25 | **0.35** | 0.45 | 0.55 | 0.65 |
|---|---|---|---|---|---|---|
| direct | −1.68 | −1.25 | **−0.82** | −0.39 | +0.04 | +0.47 |
| total | −1.28 | −0.85 | **−0.42** | +0.01 | +0.44 | +0.87 |

I set **w = 0.35**. Reasons, in order of weight: the *form* of the ask is `voelkel2026`'s exactly (a
new third-party charitable request arriving after the attitude battery) and that is the single
strongest structural fact; the recipient is an institution rather than a person, which is where the
solicitation mechanism bites; against that, the recipient genuinely is the message's subject class,
the item is block-randomised mid-battery rather than last, and the $10 is a lottery
(p = 100/18,000 = 0.56 %, expected cost of a donated dollar $0.0056) so the act is nearly costless —
and in this inventory the cheaper the act, the more positive the offset.

> **`donation_ams` mean ATE = −0.4 pp, band −1.6 … +1.1** (posterior SD ≈ 0.7; P(true sign
> negative) ≈ 0.72 at the centre, but the *scored* truth on a half sample carries SE ≈ 2.1 pp, so
> the realised sign is close to a coin flip whatever we predict).

**Explicit recommendation.** **Do not move to −1.4.** That value is 1.0 pp below my centre and near
the edge of my band, and it is built by taking the −2.5 direct path from studies that sit at the
*cause-aligned* pole and giving zero credit to a step this file measures at +4.29 ± 0.61 pp.
**Keeping −0.70 is fine**: it is 0.3 pp from my centre, well inside the band, and on 16 of 208 cells
the difference between −0.70 and −0.40 is worth ~0.02 pp of pooled RMSE. If the parent wants the
best number, it is **−0.4**; if the parent wants minimal churn, **−0.70 stands.** Either is a far
better bet than −1.4.

**Two internal-consistency notes on ANCHORS_K's assembly**, offered as queries, not accusations:
its arithmetic uses "0.5 × (target attitude ATE ≈ +2.5 pp) = +1.25", but the campaign's own
`behavioural_levels.csv` puts `trust_post` at +1.05 and `trust_multidimensional` at +1.00 — under
the campaign's own attitude centre the same formula yields −2.5 + 0.5 = −2.0 before credits. And its
−2.5 offset is stated in absolute pp, while both source studies happen to sit at a control level of
~62 pp and the target's is ~44 pp; if the offset scales with the level (weakly supported — within
`voelkel2026` the biggest absolute penalty is at the biggest recipient), the imported offset should
be multiplied by 0.72. These two corrections partly cancel, which is presumably why −0.70 has held up.

---

## 5. Between-arm SD: I confirm the point estimate and **correct the inference**

| study | outcome | τ̂ (ML) | profile 95 % upper | comparator |
|---|---|---|---|---|
| `voelkel2026` (10 arms) | Donation | **0.000** | **1.485** | its own **attitude composite**: τ̂ = 0.192, upper 1.287 |
| `voelkel2026` (10 arms) | each of the 5 recipients | 0.000 | — | — |
| `voelkel2024` (25 arms) | `PA_DG` | **2.834** | 3.925 | its attitude τ̂ = 3.211, upper 4.416 → **ratio 0.883** |
| `vlasceanu2024` (11 arms) | WEPT | 2.326 | 3.935 | attitude τ̂ = 0.819 |
| `vlasceanu2024` (11 arms) | SHARE | 2.439 | 4.226 | — |

I reproduce ANCHORS_K's zero exactly (raw between-arm SD 1.188 < mean arm SE 1.647). **But the
inference drawn from it is wrong.** `voelkel2026` cannot detect between-arm heterogeneity in
*anything* — its own attitude composite, whose arms demonstrably differ, also returns τ̂ ≈ 0. Ten
arms of ~1,050 with a per-arm SE of 1.6 pp is simply an underpowered heterogeneity design. "τ = 0"
there is a **floor artefact, not a measurement of homogeneity**, and the honest statement is
τ(donation) ≤ 1.5 pp.

The informative estimate comes from the study that *can* resolve arms: `voelkel2024`, 25 arms,
τ(behaviour)/τ(attitude) = **0.883**, arm-level r = **+0.829**. So:

> **Rule: predict τ(`donation_ams`) ≈ 0.88 × τ(predicted trust ATE), and order the arms by their
> predicted trust ATE, rather than asserting an exact zero.** With 16 near-synonymous trust messages
> τ(trust) is likely 0.3–0.5 pp, giving **τ(donation) ≈ 0.35–0.45 pp**.

Practically this changes nothing scoreable — 0.4 pp of true spread against a per-cell truth SE of
~2.1 pp is invisible to `r_within_adj` — but it is better calibrated for `spread_ratio` and it costs
nothing. **Correction to "there is no arm ordering to predict": there is one, it is inherited from
the trust ordering at ~0.88×, and it is merely too small to score.**

Party moderation: I did not re-run it and I defer to ANCHORS_K's near-zero.

---

## 6. `newsletter_signup`: the money offset does **not** contaminate the click cell

The target's newsletter (M26) is: subscribe to climate scientist **Katharine Hayhoe's** "Talking
Climate" newsletter, external link, free tier, self-reported afterwards. On the parent's coding that
is `recipient_relation = subject_of_message` (a climate scientist) **and** benefit-to-self, with
`cost_type = low_cost_click` (plus real friction: new tab, email, self-report).

The negative offset in this inventory is confined to **money and effort**:

| act type | direct offset |
|---|---|
| money to a cause (`voelkel2026`) | −1.85 ± 0.91 |
| effort for a cause (`vlasceanu` WEPT) | −2.55 ± 0.63 |
| **click, aligned with the message (`vlasceanu` SHARE)** | **+5.65 ± 0.81** (n = 44,009) |
| click, self-benefit (`koetke` S5) | −8.54 ± 4.56 (n = 617) |

The one well-powered low-cost-click estimate is **strongly positive**, and it is 32× more precise
than the one negative click estimate, which is additionally content-confounded (its manipulation was
that the scientist is uncertain about her own findings — a specific reason to want fewer of her
tips). **So: no, the money-specific negative offset should not be carried into the click cell.**

Sizing it, in latent-normal units so the base rates are handled: SHARE's +5.65 pp at a 48.5 % base is
+0.142 SD; koetke's −8.54 pp at a 44.0 % base is −0.213 SD; inverse-variance pooled **+0.131 ±
0.020 SD**. Multiply by a construct-distance factor of 0.25–0.5 ("share what you just read" →
"subscribe to a third party's newsletter"), convert at a 13 % base rate
(100·φ(Φ⁻¹(0.87)) = 21.2 pp/SD) and apply the κ ≈ 1.4 latent-skew inflation that ANCHORS_I and
ANCHORS_K independently reproduced: **+1.0 … +2.0 pp**.

That is above the entry's +0.45. I nonetheless **recommend keeping +0.45**, and record +0.6 as my
own centre with band **−1.0 … +2.0**: the whole calculation hangs on a construct-distance factor I
cannot measure, the newsletter ask carries real friction that no train analogue has, and it is a
self-benefit ask like the one negative datapoint. Raising it is not worth spending prediction
variance on. **What matters for the parent's question is only the sign, and the sign is safe:
positive.**

---

## 7. What would make me wrong

* **The subject pole is one study.** Everything in §3 above the cause pole rests on
  `voelkel2024`'s dictator game. If the +1.97 is a property of *dictator games between people*
  rather than of *recipient alignment*, the whole swing evaporates and the right answer is the
  cause pole plus a lottery credit — i.e. about **−1.4**, exactly the value I am arguing against.
  I cannot rule this out with train data. The strongest thing I can say against it is that the third
  aligned datapoint (`vlasceanu` SHARE, +5.65) is not a dictator game and is not between people, and
  it sits on the same side.
* **Position, not recipient.** If the −1.85/−2.55 offsets are end-of-survey depletion (both items are
  late; `voelkel2024`'s DG is not) then "alignment" is mislabelled position. ANCHORS_K falsified
  *reading-time* depletion in `voelkel2026`, which is not the same as cumulative-survey depletion,
  and no block-order variable survives in either deposit, so I could not test it. If this is the
  truth, my centre is still roughly right (the target's item is also mid-battery) but for the wrong
  reason — and then the recipient coding in `recipient_alignment.csv` should not be reused.
* **The pass-through is cross-sectional.** +11.0 cents/SD is a control-group correlation, not a
  causal pass-through; if the true causal pass-through is half of it, my +0.40 becomes +0.20 and the
  centre moves to −0.6.
* **The level.** I inherited the $4.40 control level. If the lottery pushes control giving to $6
  instead, the level correction flips from 0.72 to 0.98 and my centre moves to about −0.8.
* **w is a judgement, not a measurement.** The table in §4 is deliberately printed so the parent can
  overrule it: at w = 0.15 the answer is −1.28 (≈ the −1.4 I am rejecting) and at w = 0.55 it is
  +0.44. My case for w = 0.35 is structural, not statistical.
* **AMS may not be aligned at all in respondents' heads.** The messages are about *climate
  scientists*; AMS is a professional society "of 12,000 scientists and other professionals". If
  respondents read it as just another climate non-profit, the target is a pure `voelkel2026` replay
  and the answer is the cause pole. Note that `voelkel2026`'s five recipients span
  −9.2 % to +47.2 %/SD of elasticity *among nominally identical climate NGOs* — recipient
  perception varies enormously, and I have no train handle on where a scientific society falls.

---

## 8. Blinding and recognition disclosure

I recognise `voelkel2024`, `voelkel2026`, `vlasceanu2024` and `koetke2024` as published studies and
have a general sense that behavioural outcomes in the first two were reported as weak. **No
remembered result was used as a number, and I made no retrieval attempt of any kind.** Every figure
here was computed in this session from the vendored microdata and questionnaires listed in
`_m_sources.csv`. Two target-study facts (the $10 lottery; the AMS and Katharine Hayhoe wordings)
come from `/workspace/benchmark/survey/survey.qsf`, which is public template material, not human
outcome data. I encountered no human outcome data from the target study. The only network use was
`uv pip install pypdf openpyxl`.
