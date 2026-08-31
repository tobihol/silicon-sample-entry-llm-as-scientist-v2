# ANCHORS_B — empirical magnitudes of randomized message effects on trust-in-scientists and adjacent climate attitudes

All effects in **percentage points of scale range**: `ate_pp = 100*(mean_arm - mean_control)/(hi-lo)`.
Row-level file: `trust_effects.csv` (967 rows, 11 datasets, 8 outcome families).
Everything below is computed from `/workspace/datasets/*` (TRAIN split) only. No web, no validation data.

## 0. What was minable, and what was not

| dataset | usable | what came out |
|---|---|---|
| koetke2024 | yes | S2–S4 persona vignettes (High/Low intellectual humility) + **S5: 3 genuine text arms vs control** on METI trust, belief-in-research, behaviour |
| gligoric2025 | yes, **with a fix** | control arm is a *general-population* sample (ideology mean 5.4) while all 5 message arms are conservatives (ideology 7.8). The raw full-sample contrast is confounded (spuriously −2 to −3 pp). Only the ideology≥7 / ≥8 restrictions are used. |
| agley2021 | yes | 2-arm infographic RCT, 21-item trust 1–5, **pre and post** |
| geiger2026 | yes | (a) vdL 2019 US consensus RCT n=6,301 pre/post; (b) Većkalov 2024 3-arm, incl. **trust in climate scientists 1–7** (US n≈120/arm; 27-country n≈3,500/arm) |
| gatewaybelief | yes | Exp1 (Maertens 2020, 4 arms, T1/T2) and Exp2 (vdL 2017, 6 arms, pre/post). Supplemental study not mined (longitudinal, redundant). |
| spampatti2023 | yes | 6 inoculation texts vs passive control, 0–100 affect, climate belief, MIST, WEPT; USA (n≈70/arm) and all-12-country (n≈850/arm) |
| schmidbetsch2019 | partly | attitude/intention vs "advocate absent" is a *presence-of-rebuttal* contrast, not a message-content contrast; the **advocate-credibility** DVs are only defined when the advocate is present, so those are style-vs-style contrasts (ref = technique rebuttal) |
| tappin2023 | yes | 48 human-written ~150-word arms, no-cue cells only (`Info-only` vs `Control`), 7-pt agreement signed toward the message |
| hackenburg2025 | yes | 623 message arms with ≥10 respondents (720 LLM + 10 human), 0–100 slider already oriented to the message direction, plus `treatment_message_word_count` |
| attari2016 | yes, with caveat | **no control arm and no pre-measure** — these are vignette-vs-vignette messenger-consistency contrasts, not message ATEs. Kept for the credibility→policy proximity ratio only. |

`.rds` for tappin2023 could not be read by `pyreadr` ("unrecognized object"); converted with the system `Rscript`.

---

## 1. Typical magnitude of a randomized short-text ATE

### 1a. Trust in scientists — the headline number

Restricting to **short-text/graphic arms with a real control** (drops the koetke persona vignettes, which change the described scientist rather than adding a message):

| statistic | value (pp of scale range) |
|---|---|
| n rows | 39 (22 in the strict "core" subset) |
| **median \|ate_pp\|** | **0.97** |
| IQR of \|ate_pp\| | 0.48 – 1.66 |
| 90th pct \|ate_pp\| | 2.40 |
| max \|ate_pp\| | 5.03 (a n≈86 climatologists cell, se 4.6 — noise) |
| mean *signed* ate_pp | **+0.58** |

On **broad multi-item trust composites only** (the closest structural analogue to the target's 4-dimension battery): 19 arm×outcome cells, **median \|ate\| = 0.64 pp, IQR 0.26–0.95, mean signed +0.88 pp, max 3.79 pp**.

The individual studies:

- **gligorić 2025** — 5 messages *purpose-built to raise conservatives' trust in scientists*, n≈880/arm, 70-item composite: **+0.17, +0.17, +0.48, +0.64, +0.93 pp**. All null. Replicated at ideology≥8: +0.18 … +0.92.
- **agley 2021** — "how science works" infographic, 21-item trust 1–5, n≈510/arm: post-only **−0.00 pp**, DiD **+0.66 pp** (se 0.30).
- **Većkalov 2024** — consensus messages → trust in climate scientists 1–7: 27-country n≈3,500/arm **−0.05 / +0.71 pp**; USA n≈120/arm +0.97 / +2.22 pp (se 3.1, uninformative).
- **koetke 2024 S5** — the only arms that clear 1 pp: 3 intellectual-humility framings of an interview excerpt, n≈170/arm, **+1.56, +1.95, +3.79 pp** on METI (mean +2.4).
- For contrast, **koetke S2–S4 persona vignettes** (the scientist *is* described as humble vs arrogant) reach **+4.2 to +16.4 pp**. That is the ceiling of what a stimulus can do to trust — and it requires rewriting the target of the trust judgement, not appending a message.

### 1b. Ranked table of outcome families

Core subset = short-text arm vs a real control (drops attari, koetke persona vignettes, schmid presence-of-advocate, duplicated country/ideology cuts, and hackenburg's degenerate `pythia` arms). k = 644 rows.

| rank | outcome_family | k | median \|ate_pp\| | IQR | max \|ate\| | mean signed | **SD across arms** | rms(se) | **SD_true** |
|---|---|---|---|---|---|---|---|---|---|
| 1 | consensus_perception | 18 | **9.05** | 7.0–15.4 | 20.05 | +9.51 | 7.28 | 1.22 | **7.17** |
| 2 | policy *(proximal — see note)* | 503 | **7.33** | 3.9–11.8 | 32.45 | +7.13 | 7.39 | 5.78 | **4.60** |
| 3 | behavior | 9 | 4.06 | 0.1–7.5 | 10.21 | −4.29 | 4.02 | 4.84 | 0.00 |
| 4 | belief | 34 | **2.30** | 1.2–3.7 | 8.31 | +1.38 | 3.14 | 2.36 | **2.08** |
| 5 | credibility (style vs style) | 18 | 1.81 | 0.7–3.4 | 6.95 | −0.85 | 2.67 | 2.84 | 0.00 |
| 6 | concern / worry | 16 | **1.68** | 0.7–2.5 | 3.83 | +1.35 | 1.58 | 1.51 | **0.48** |
| 7 | affect slider (other) | 24 | 1.60 | 0.7–4.2 | 4.77 | +0.27 | 2.81 | 3.51 | 0.00 |
| 8 | **trust_scientists** | 22 | **1.17** | 0.7–1.9 | 3.79 | +0.63 | 1.52 | 2.46 | **0.00** |

**Note on `policy`.** That family is bimodal and the split is the whole story:

| policy sub-family | k | median \|ate\| | IQR | mean |
|---|---|---|---|---|
| **proximal**: the message argues *for this exact policy*, DV never pre-asked (tappin, hackenburg) | 487 | **7.58** | 4.2–12.1 | +7.34 |
| **downstream**: climate/consensus message → climate-policy support | 24 | **1.63** | 1.0–3.5 | +1.82 |

So "policy is easy to move" is false. *Directly-argued, never-previously-asked* attitudes are easy to move (7–8 pp). Everything one step removed from what the message asserts sits at 1–2 pp, and generalized trust in scientists sits below that at ≈0.6–1.2 pp.

---

## 2. The proximity gradient

Ratio = (effect on the construct the message directly asserts) ÷ (effect on a downstream construct), same arm, same sample.

**Consensus messages ("97% of climate scientists agree") → perceived consensus vs downstream:**

| study | perceived consensus (pp) | ÷ belief | ÷ worry | ÷ policy | ÷ trust in scientists |
|---|---|---|---|---|---|
| vdL 2019 US, post-only (n=3,150/arm) | 16.79 | ×4.8 | ×5.7 | ×8.9 | — |
| vdL 2019 US, DiD | 16.20 | ×7.5 | ×10.4 | ×13.2 | — |
| vdL 2019 US, DiD excl. exact-97 parroters | 9.54 | ×6.1 | ×18.7 | ×18.3 | — |
| Većkalov 2024, 27 countries, classic (n=3,500/arm) | 6.50 | ×5.0 | ×6.2 | ×17.1 | ×(−130) — trust ATE is −0.05 |
| Većkalov 2024, 27 countries, updated | 6.36 | ×4.7 | ×7.0 | ×9.8 | ×9.0 |
| gateway Exp1 (Maertens 2020) Consensus arm | 8.40 | ×2.9 | (sign flip) | ×60 | — |
| gateway Exp2 (vdL 2017) PieChartOnly | 19.41 | — | ×10.0 | ×8.1 | — |

**Messenger-credibility manipulation → credibility vs policy support** (attari 2019 Study 1, 6 policies, ~305/cell):

| policy | credibility (pp) | policy support (pp) | ratio |
|---|---|---|---|
| CCS / carbon tax / nuclear / population / transit | 19.6 – 23.2 | 1.6 – 6.3 | **×3.5 – ×4.7** (renewables ×11.9, ceiling) |

**Rule.** One construct step away from what the text asserts costs a factor of **≈3–8**. Two steps (assertion → belief → policy/behaviour) costs **≈10–20**. Generalized *trust in the scientists* is not on the causal path of a consensus message at all: it stays at 0 while perceived consensus moves 6–16 pp (Većkalov: 6.4 pp on consensus, +0.3 pp on trust ⇒ ratio ≈ ×20, and not distinguishable from zero at n=7,000).

The mirror-image case is worth stating: koetke S5's "limits of methods / limits of results" arms **raise** METI trust in the scientist by 1.6–3.8 pp while **lowering** belief in her research by 6.2–8.3 pp. Trust in a person and belief in their findings can move in opposite directions within one message.

---

## 3. Are re-asked (pre-measured) outcomes less movable?

**Yes, by roughly a third, and the stickiness is measurable directly.**

(a) **DiD ÷ post-only ratio** on the same pre-measured outcome:

| study / outcome | post-only | DiD | DiD/post-only |
|---|---|---|---|
| vdL 2019 consensus (0–100 slider) | 16.79 | 16.20 | 0.96 |
| vdL 2019 belief (1–7) | 3.49 | 2.17 | **0.62** |
| vdL 2019 worry (1–7) | 2.96 | 1.56 | **0.53** |
| vdL 2019 policy (1–7) | 1.88 | 1.23 | **0.65** |
| schmid Exp6 attitude (0–100 POMP) | 14.64 | 10.77 | 0.74 |
| Većkalov 27-ctry consensus | 6.50 | 6.69 | 1.03 |
| agley trust (1–5) | −0.00 | +0.66 | n/a (both ≈0) |

Median ratio on Likert outcomes ≈ **0.65**: about a third of a naive post-only difference on a pre-measured Likert item is baseline imbalance/noise, not treatment. Sliders (0–100) show ratio ≈1 because they are high-variance and low-autocorrelation.

(b) **Response stickiness in the control arm** (vdL 2019, n=3,151):

| outcome | % giving the *identical* post answer | sd(post−pre) | sd(pre) | ratio | r(pre,post) |
|---|---|---|---|---|---|
| consensus 0–100 | 18.4% (44% within ±2) | 13.4 | 22.4 | 0.60 | 0.82 |
| belief 1–7 | 29.5% | 0.90 | 1.76 | 0.51 | 0.87 |
| worry 1–7 | 29.4% | 0.80 | 1.83 | 0.44 | 0.91 |
| policy 1–7 | 37.4% | 0.80 | 1.57 | 0.51 | 0.87 |
| **agley 21-item trust composite 1–5** | — | **0.19** | **0.61** | **0.31** | **0.956** |

A multi-item trust composite is the stickiest instrument in the whole corpus: within-person retest change SD is only **31%** of the cross-sectional SD, r = 0.956. Even a treatment that genuinely moves people has almost no room on that scale.

(c) **Never-asked vs re-asked, across studies.** Policy attitudes that were *never pre-asked* and are directly argued (tappin 7-pt, hackenburg 0–100) move **+4.9 to +7.3 pp** on average; climate-policy support that *was* pre-asked moves **+1.2 to +1.8 pp**. That is a ≈4× gap, partly proximity and partly re-ask anchoring — I cannot separate them cleanly with these data, but both point the same way.

---

## 4. Message-level heterogeneity: SD of the ATE across arms, real vs sampling

`var_true = var(ate_pp) − mean(se_pp²)`; negative ⇒ reported as 0.

| tournament | k arms | n/arm | mean ATE | SD across arms | rms(se) | **SD_true** |
|---|---|---|---|---|---|---|
| **tappin2023**, 48 human ~150-word messages → 7-pt policy agreement | 48 | 127 | +4.88 | 4.10 | 3.81 | **1.50** |
| …same, residualized within issue | 48 | 127 | — | 3.99 | 3.81 | **1.16** |
| …between-issue component | 24 | — | — | 2.98 | 2.69 | 1.26 |
| **hackenburg2025**, 623 arms → 0–100 slider (pooled over 10 issues) | 623 | 19 | +6.20 | 8.19 | 6.56 | **4.91** |
| …residualized within issue | 623 | 19 | — | 7.81 | 6.56 | **4.24** |
| …within issue, excluding `pythia` (broken/off-topic messages) | 439 | 22 | +7.60 | 6.91 | 6.05 | **3.33** |
| …within issue, **frontier models only (GPT-4 + Claude 3 Opus)** | 60 | 80 | +8.99 | 3.04 | 3.34 | **0.00** |
| gligorić, 5 trust messages → trust in scientists | 5 | 884 | +0.48 | 0.33 | 0.96 | **0.00** |
| koetke S5, 3 IH messages → METI trust | 3 | 174 | +2.43 | 1.19 | 1.43 | **0.00** |
| koetke S5, 3 IH messages → belief in research | 3 | 174 | −5.24 | 3.68 | 1.82 | **3.19** |
| spampatti, 6 inoculation texts → 0–100 affect (12 countries) | 6 | 849 | +1.84 | 0.94 | 1.06 | **0.00** |
| spampatti, 6 inoculation texts → climate belief | 6 | 849 | +0.50 | 0.46 | 1.05 | **0.00** |
| Većkalov, 2 consensus messages → perceived consensus | 2 | 3,500 | +6.43 | 0.10 | 0.34 | **0.00** |

**Reading.** Between-message heterogeneity is small and, on trust-like outcomes, statistically indistinguishable from zero. In the two large human-message tournaments the *real* SD across arms is ≈**1.2–1.5 pp** on a 7-pt scale around a mean of ≈5 pp — i.e. **CV ≈ 25–30%**. The apparently larger hackenburg number (SD_true 4.2 pp within issue) is almost entirely a *message-competence* effect: when the arms are restricted to messages a competent writer would produce, SD_true collapses to **0** and the observed spread (3.0 pp) is fully explained by sampling error (rms se 3.3 pp).

Practical consequence: given a set of 16 professionally written interventions aimed at the same construct, the between-arm spread of the true ATEs should be expected to be **small relative to the shared mean**, and most of the observed arm-to-arm spread in any single realized dataset is sampling noise.

---

## 5. Dose / length

`hackenburg2025` is the only source with per-message word counts (median 212 words for LLM, 157 for the 10 human messages; range 14–519).

| word-count sextile (all 623 arms) | k | mean words | mean ATE (pp) |
|---|---|---|---|
| ≤136 | 104 | 88 | **2.50** |
| 137–189 | 104 | 166 | 6.88 |
| 189–211 | 104 | 201 | 7.52 |
| 211–239 | 107 | 225 | 6.58 |
| 239–277 | 100 | 256 | 7.20 |
| ≥277 | 104 | 319 | 6.52 |

Within-issue r(words, ATE) = **0.143** (p = 3e-4), slope **+1.46 pp per 100 words** — but that is driven entirely by the truncated/degenerate short outputs. Excluding `pythia`: r = **0.064** (ns), slope **+0.84 pp/100 words**, and the quintile means are flat (6.6, 7.8, 8.6, 7.6, 7.5 pp from 150 to 297 words). The 10 **human** messages average 157 words and achieve **+8.78 pp** — as good as the 212-word frontier-LLM messages.

**Conclusion:** there is a floor effect below ≈140 words (a message too short to make its case loses ~4 pp) and **no dose gradient above ≈150 words**. Length is a proxy for completeness, not a dose.

---

## 6. Rules of thumb (numbers to carry forward)

1. **A short text arm moves generalized trust in scientists by ≈ +0.6 to +1.0 pp of scale range.** Prior centre: **+0.8 pp**; 50% interval 0.3–1.7 pp; 90% of arms below 2.4 pp; treat anything above **4 pp** as implausible for a message that does not rewrite who the trusted party is.
2. **Sign is almost always positive but small.** Mean signed ATE across 39 short-text trust cells = **+0.58 pp**; only 8/39 are negative and none significantly so.
3. **Proximity discount.** Effect on the construct the message directly asserts ÷ effect one step downstream ≈ **4–8**; ÷ two steps downstream ≈ **10–20**. If you predict X pp on a directly-asserted outcome, predict ≈ X/5 on the next construct and ≈ X/15 two constructs away.
4. **Trust is not downstream of a consensus/belief message.** Većkalov: +6.4 pp on perceived consensus, **−0.05 / +0.71 pp on trust in climate scientists** at n = 7,000. Do not route belief gains into trust gains.
5. **Re-asked Likert outcomes lose ≈35%.** DiD/post-only median 0.65 on 1–7 items; ≈1.0 on 0–100 sliders. A 21-item trust composite has r(pre,post) = 0.956 and a change SD 31% of the cross-sectional SD.
6. **Between-arm SD of true ATEs is ≈ 25–30% of the mean ATE** for professionally written messages on one outcome (tappin: mean 4.9, SD_true 1.2–1.5). For a set of 16 trust interventions whose mean is ≈+0.8 pp, the implied SD across arms is **≈0.2–0.4 pp** — i.e. the arms are nearly interchangeable and the ranking is mostly noise. Predicting a near-flat profile with a small positive common offset dominates predicting a spread.
7. **Observed spread ≫ true spread.** With n ≈ 1,000/arm on a 1–7 trust composite (SD ≈ 20 pp of range), se ≈ 0.9 pp per arm; so an observed arm-to-arm SD of ≈1 pp is fully consistent with SD_true = 0. Expect the realized (human-half) ATEs to scatter with SD ≈ sqrt(0.3² + se²).
8. **Length:** no dose effect above 150 words; below ≈140 words expect a ≈4 pp penalty on proximal outcomes.
9. **Subgroup moderation is real but modest and concentrated on the proximal outcome.** vdL 2019 consensus DiD: Republicans **20.1**, Independents **16.8**, Democrats **13.1** pp (a 7 pp R−D gap on the proximal outcome) but only **2.24 vs 1.13** pp on belief and **1.60 vs 0.97** pp on policy — a ≈1 pp partisan gap on downstream outcomes. Moderation shrinks with the same proximity factor as the main effect. Baselines drive it: Democrats start at 72.6/82.2/82.4 pp (ceiling), Republicans at 61.5/57.6/62.8.
10. **Behaviour/behavioural intention is the least reliable family** — median \|ate\| 4.1 pp but SD_true = 0 and mean signed **−4.3** across 9 cells (koetke S5's follow-up interest fell in all three arms). Predict ≈0 with wide uncertainty.
11. **Ceiling matters.** Control means on trust scales are 68–86 pp of range; on climate belief 86–92 pp. Anything with a control mean above ~80 pp of range has at most ~20 pp of headroom and empirically moves <2 pp.
