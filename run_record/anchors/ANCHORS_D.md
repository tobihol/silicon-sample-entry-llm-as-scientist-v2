# ANCHORS_D — control-arm LEVEL and SUBGROUP-GAP anchors from the train split

Run: 20260827T203601Z_s2b (idea_03 sub-agent, train-split-only job).
Scope: `/workspace/datasets/*` only. No validation data, no web, no retrieval.
All numbers are **percent of the item's scale range** (0 = scale floor, 100 = scale ceiling),
i.e. the benchmark's pp-of-scale-range unit, unless a row is explicitly flagged as a
"% saying X" top-box percentage.

Machine-readable companion: **`levels.csv`** (2,220 rows;
columns `construct, source_dataset, source_item, moderator, level, year, n, mean_0_100, se, lo, hi, format, weight, note`).
Per-source intermediates: `_pew_rows.csv _gss_rows.csv _ccam_rows.csv _wellcome_rows.csv
_v26_rows.csv _glig_rows.csv _geiger_rows.csv _koetke_rows.csv _agley_rows.csv _w135_rows.csv
_tisp_rows.csv _anes_rows.csv`, plus `_headroom.csv`.

---

## 0. Dataset inventory — what actually exists in the train split

| dataset | US population measure | demographics | weight | in levels.csv |
|---|---|---|---|---|
| `tisp` | **the target study's own 12-item trust-in-scientists scale (1–5)** + `CLIM_TRUST` trust in climate scientists (1–5) + a Pew-style confidence item + 5-item climate policy support (1–4); US n=2,559, 2022–23 | gender, age, education (4), income, 5-pt conservatism | `WEIGHT_CNTRY` | ✔ (84) |
| `anes` | 2020 `V202173` 0–100 **feeling thermometer for scientists** (n=7,367); 2024 `V242420` 4-pt CSES trust in scientists (n=4,702); 2020 climate severity/importance (1–5) | party (+leaners), race, gender, age, education, income | `V200010b` / 2024 full-sample | ✔ (113) |
| `pew_atp` w42/w100/w114 | 4-pt **confidence in scientists / medical scientists** "to act in the best interests of the public"; w42 adds a 5-item **environmental-research-scientist** battery (good research / fair+accurate / admits mistakes / transparent about funding conflicts / cares about public) | party, party-lean, ideology, race, gender, age, education, (w42) income | `WEIGHT_W42/W100/W114` | ✔ (403) |
| `pew_atp/toplines/w135_climate_scientists.csv` | **published Pew W135 (2023, N=8,842) toplines: ENV26a–d "how well do climate scientists understand …"**, 4-pt, with 2016/2021 trend and party × education breaks | party-lean, education, party×education | Pew published weighted % (no SE) | ✔ (48) |
| `gss` | `consci` **confidence in the scientific community**, 3-pt, 1973–2024 (39 waves); `tempgen` greenhouse danger (5-pt, ISSP years) | party(+leaners), ideology(7), race, gender, age, education | `wtssps` | ✔ (349) |
| `wellcome` 2018/2020 | 4-pt trust in scientists in this country / trust science / competence / benevolence / **funding transparency (2018 Q14B)**; 2020 climate-threat 3-pt; US n≈1,000 each | gender, age(3), education(3), income quintile — **no party, no race** | `wgt` / `WGT` | ✔ (169) |
| `ccam` | climate belief/worry/harm/policy/`sci_consensus`, 2008–2024, 35,309 rows | party(+leaners), ideology, race(5), gender, age(3), education, income(3) | `weight_aggregate` | ✔ (320) |
| `voelkel2026` | **the design twin**: 8 climate outcome families, all 0–100 sliders, pre and post, control arm n=3,183 | party(3), ideology(7), race(5), gender, age(6), education(3), income | none (quota panel, **unweighted**) | ✔ (448) |
| `gligoric2025` | trust in 35 scientist occupations (2 × 7-pt bipolar), incl. **climatologists / environmental scientists / ecologists / meteorologists / oceanographers**, control arm n=2,248 | ideology 1–10, gender, age, education — **no party, no race** | unweighted | ✔ (200) |
| `geiger2026` | Većkalov US control cell: **`scientist_trust` = trust in climate scientists (1–7)**, n=125; vdL2019 US control n=3,151 belief/worry/policy (1–7) + consensus (0–100) with party | ideology 0–10 / party3 | unweighted | ✔ (51) |
| `koetke2024` | METI 14-item trust in scientists (7-pt bipolar), 5 US studies n=298–679 | political conviction only | unweighted | ✔ (15) |
| `agley2021` | 21-item Trust in Science Inventory (1–5) baseline, Prolific n=1,024 | gender, race, age, 1–10 political | unweighted | ✔ but **flagged unusable as a level** (see §6) |
| `vlasceanu2024`, `voelkel2024`, `ces`, `acs`, `sce`, `hackenburg2025`, `tappin2023`, `spampatti2023`, `bago2025`, `attari2016`, `schmidbetsch2019`, `gatewaybelief` | no US-population trust-in-scientists item with demographics that is not already better covered above (`ces`/`acs` = demographics only; `sce` = response format only; the rest are experiments on other constructs) | — | — | ✘ |

---

## 1. CONTROL-LEVEL ANCHOR — where does US trust in scientists sit on 0–100?

### 1a. Trust in **scientists in general**, by item format (weighted, nationally representative)

| source / year | item format | mean (pp of range) | se | n |
|---|---|---|---|---|
| GSS 2024 | 3-pt confidence in the scientific community | **62.2** | 0.98 | 2,121 |
| GSS 2022 | 3-pt | 63.2 | 1.09 | 2,314 |
| GSS 2021–24 pooled | 3-pt | 65.6 | 0.54 | 7,089 |
| Pew W114 2022 | 4-pt confidence "act in best interests of the public" | 66.8 | 0.58 | 5,259 |
| Pew W100 2021 | 4-pt | 67.0 | 0.48 | 7,181 |
| GSS 2021 | 3-pt | 70.3 | 0.76 | 2,654 |
| ANES 2024 | 4-pt CSES trust in scientists | 71.0 | 0.57 | 4,702 |
| TISP 2022–23 | **1–5 agreement, the target's own 12-item scale** | **71.5** | 0.41 | 2,559 |
| TISP 2022–23 | 1–5 Pew-style confidence item | 70.9 | 0.56 | 2,559 |
| Pew W42 2019 | 4-pt | 73.3 | 0.69 | 2,231 |
| ANES 2020 | **0–100 feeling thermometer** | **78.0** | 0.36 | 7,367 |
| Wellcome 2018 / 2020 | 4-pt "trust scientists in this country" | 76.8 / 81.7 | 1.07 / 1.00 | 968 / 993 |
| Wellcome 2020 | 4-pt "trust science" | 84.2 | 0.94 | 959 |
| *(non-representative convenience samples for contrast)* | | | | |
| koetke2024 S1–S5 (2023) | 7-pt bipolar METI, 14 items | 73.8 – 81.0 | 0.4–0.9 | 298–679 |
| gligoric2025 control (2024) | 7-pt bipolar, grand mean over 35 occupations | 71.7 | 0.43 | 2,248 |

**Format effect is large: ~62 → ~84, a 22-pp spread across formats for the same construct.**
Ordered lowest → highest: **3-pt confidence (62–66) < 4-pt confidence (67–73) ≈ 1–5 agreement composite (71–72) < 4-pt "trust X" (77–82) < 0–100 thermometer (78) < "trust science" (84).**
Rules of thumb from these data:
- A 12-item 1–5 agreement composite (the target's scale) sits at **71–72**.
- Moving to a 0–100 thermometer/slider adds roughly **+6 pp**.
- Moving to a coarse 3-pt confidence item costs roughly **−6 to −9 pp**.
- Coarse scales also inflate variance: sd 32.5 pp (3-pt GSS) vs 20.6 pp (12-item 1–5 composite).

### 1b. Trust in **CLIMATE scientists specifically** — lower than scientists in general

| source / year | item | mean | n |
|---|---|---|---|
| **TISP 2022–23** `CLIM_TRUST` (1–5), same respondents as the 71.5 above | trust in climate scientists | **67.0** (se 0.65) | 2,557 |
| Pew W135 2023 ENV26a (4-pt) | understand *whether* climate change is occurring | 63.7 | 8,842 |
| Pew W135 2023 ENV26d | understand extreme weather | 60.3 | 8,842 |
| Pew W135 2023 ENV26b | understand the *causes* | 59.3 | 8,842 |
| Pew W135 2023 ENV26c | understand the *best ways to address* it | **50.8** | 8,842 |
| Pew W42 2019, 5-item environmental-research-scientist composite (4-pt) | | 67.2 (se 0.64) | 2,201 |
| gligoric2025 2024 control, climatologists (7-pt bipolar) | | 61.8 (se 1.85) | 248 |
| geiger2026/Većkalov US control 2022 (1–7) | trust in climate scientists | 80.3 (se 2.28) | **125, left-skewed convenience sample — treat as an upper outlier** |

**Anchor: within-respondent, trust in climate scientists runs ~4–5 pp BELOW trust in
scientists in general** (TISP: 67.0 vs 71.5, same 2,559 people, same 1–5 format;
gligoric2025: climatologists 61.8 vs 35-occupation grand mean 71.7, i.e. −9.9 pp).
Item content matters more than that within the climate battery: competence-about-facts
items (~60–64) sit ~10–13 pp above competence-about-*solutions* items (50.8).

### 1c. Sub-dimension ordering inside a trust battery (Pew W42 env-scientists, 2019, weighted)

| facet | mean |
|---|---|
| does a good job conducting research (competence) | 75.4 |
| cares about the best interests of the public (benevolence) | 72.1 |
| provides fair and accurate information (integrity) | 71.4 |
| is transparent about industry conflicts of interest | 59.4 |
| admits mistakes and takes responsibility | **57.5** |

Wellcome 2018 replicates the ordering: competence 80.2 > benevolence 71.4 > **funding
transparency 62.6**; company scientists sit ~13 pp below university scientists
(58.6 / 53.2). **Openness/integrity facets sit 13–18 pp below competence facets** — an
important shape constraint on a 13-outcome trust battery.

---

## 2. PARTY GAP (Republican − Democrat), pp of scale range

### Trust in scientists in general (weighted, representative, 2019–2024)

| source | year | Rep | Dem | gap |
|---|---|---|---|---|
| Pew W42 | 2019 | 70.0 | 78.3 | **−8.4** |
| ANES thermometer | 2020 | 70.5 | 85.9 | −15.4 |
| GSS `consci` | 2021 | 59.2 | 81.3 | −22.1 |
| Pew W100 | 2021 | 56.1 | 78.8 | −22.7 |
| Pew W114 | 2022 | 56.2 | 77.7 | −21.5 |
| GSS `consci` | 2022 | 51.3 | 72.7 | −21.4 |
| GSS `consci` | 2024 | 54.7 | 71.9 | −17.2 |
| ANES CSES 4-pt | 2024 | 59.9 | 82.0 | −22.1 |
| GSS pooled | 2021–24 | 55.2 | 75.8 | −20.5 |

**Median ≈ −21 pp; spread −8 to −23 pp** (leaner-folded values are within ~1.5 pp of the
3-category values; the leaner rule below barely matters). The 2019 Pew reading (−8) and
the 2020 thermometer (−15) are the low end; every post-2020 representative source lands
at −17 to −23.

### Trust in **climate** scientists — the gap is ~1.4× larger

| source | item | Rep/lean | Dem/lean | gap |
|---|---|---|---|---|
| Pew W135 2023 | understand *whether* occurring | 48.2 | 79.0 | **−30.8** |
| Pew W135 2023 | understand causes | 43.6 | 73.9 | −30.3 |
| Pew W135 2023 | understand extreme weather | 45.4 | 73.6 | −28.2 |
| Pew W135 2023 | understand best ways to address | 37.5 | 64.1 | −26.6 |
| Pew W42 2019 | env-scientist 5-item composite | 59.1 | 75.1 | −16.0 (vs −8.4 for generic scientists in the *same* wave) |

**Ideology proxies confirm the amplification.** TISP 2022–23, same respondents:
least- vs most-conservative quintile gap is **−22.2 pp for `CLIM_TRUST`** but only
**−9.3 pp for the 12-item generic trust scale** (2.4×). gligoric2025 (control arm):
conservative(6–10) − liberal(1–5) is **−16.2 pp for climatologists**, −16.1 for
environmental scientists, −11.0 for epidemiologists, but only **−5.5 pp** for the
35-occupation grand mean and −3.6 for biologists.

**Anchor for the target: a −21 pp party gap on generic trust, ~−28 to −30 pp on
climate-scientist-specific items.**

### Climate attitudes (not trust) — the party gap is bigger still
CCAM 2020–24 weighted, Rep − Dem: worry −40.5, priority −47.8, harm to future generations
−37.7, regulate CO₂ −33.2, fund renewables −31.8, "GW is happening" −41.1 pp,
perceived scientific consensus −43.6 pp. voelkel2026 control-arm pre (unweighted):
concern −37.0, policies −32.8, companies −26.8, belief −22.8, specific policies −24.7,
intent −22.4, non-policy intent −15.7, candidate −12.9.
ANES 2020: climate severity −39.6, climate importance −38.9.

### Leaner rule
Where both are available I report **(a) 3-category self-ID** (Republican / Independent /
Democrat, "something else"/refused dropped) and **(b) leaners folded**
(Pew `F_PARTYSUM_FINAL` Rep/Lean Rep vs Dem/Lean Dem; GSS `partyid` 0–1 + "ind, close to
dem" = Dem, 5–6 + "ind, close to rep" = Rep, pure independents excluded; ANES
`party_leanersfolded` as built by the prior session; CCAM `party_w_leaners`).
The two definitions differ by ≤1.7 pp in every source; folding leaners *narrows* the
Independent cell and leaves Rep/Dem means essentially unchanged.

---

## 3. RACE, EDUCATION, AGE, GENDER gaps (pp of scale range)

### Race (trust in scientists; weighted; 2019–2024 sources)

| contrast | median | range | notes |
|---|---|---|---|
| Black − White | **−3.3** | −11.4 … +5.2 | GSS shows the largest negative gaps (−8 to −11); Pew shows −1 to −4 on generic confidence; the gap *reverses* on the "admits mistakes"/"transparent about funding" facets (+3 to +5) |
| Hispanic − White | **−1.9** | −5.6 … +2.9 | small and unstable |
| Asian − White | **+7.5** | +5.4 … +12.8 | the only consistently large racial gap; ANES 2020 thermometer +5.4, Pew W114 medical scientists +12.8 |

**Race is a weak moderator of trust** (|median| ≤ 3.3 pp for Black/Hispanic vs White) —
much weaker than party (−21) or education (+9).

**Race behaves oppositely on climate attitudes**, where minority respondents are *more*
pro-climate: voelkel2026 control pre, Black − White +5.3 (belief), +13.8 (concern),
+12.7 (policies); Hispanic − White +4.0/+12.2/+8.5; Asian − White +8.9/+12.5/+9.0.
CCAM 2020–24 replicates the sign (e.g. "GW is happening": Black +7.0, Hispanic +8.8,
Other +14.0 vs White).

### Education (college graduate or more − high-school or less)

| | value |
|---|---|
| median across 36 trust items/sources | **+8.6 pp** |
| range | +4.1 … +15.5 (one negative outlier, Wellcome 2020 "govt leaders value scientists" −8.6, which is not a trust item) |
| largest | GSS 2021 +15.5, ANES 2024 CSES +15.1, GSS 2021–24 +13.0, Wellcome 2018 Q11C +12.1, Pew W100 +12.0 |
| TISP 12-item composite (EDU4 − EDU3) | +6.7; `CLIM_TRUST` +10.6 |

**Anchor: +9 pp, and ~+10 to +11 pp for climate-scientist items.** Education is the
second-strongest moderator after party. On *climate attitudes* it is much weaker
(voelkel2026 control pre: Bachelor+ − HS-or-less is only +3.4 belief, +1.6 concern).

### Age (60+/65+ − 18–29)

| | value |
|---|---|
| median across 39 trust items/sources | **−1.8 pp** (essentially flat) |
| range | −8.8 … +6.1 |

**Age is not a meaningful moderator of trust in scientists** (Wellcome 2018 is the only
source with consistently large negative gaps, −4 to −9). On *climate attitudes* age is a
strong negative gradient: voelkel2026 control pre 65+ − 18–24 is −14.0 (belief), −14.0
(concern), −15.1 (policy support), −12.7 (intent).

### Gender (Female − Male)

| | value |
|---|---|
| median across 32 trust items/sources | **+0.7 pp** |
| range | −6.5 … +5.3 |
| structure | GSS is consistently negative (women *lower*, −3.4 to −6.5); TISP and Wellcome-2018 are consistently positive (+2 to +5); Pew is ~0 |

**Gender is a null-to-tiny moderator of trust (|gap| ≲ 3 pp), sign inconsistent across
sources.** On climate attitudes it is small but consistently positive:
voelkel2026 +6.2 (concern), +3.6 (policies), +2.0 (belief).

### Income (secondary)
TISP 2022–23: lowest (<$30k) 68.4 → highest (≥$168k) 81.2, **+12.8 pp**.
ANES 2020 thermometer: +2.4 (lowest → ≥$168k band spread ~5 pp).
Income is largely education's shadow; use +5 to +12 pp top-vs-bottom.

### Party × education interaction (the one interaction with hard published evidence)
Pew W135 2023, **% saying climate scientists understand *whether* climate change is
occurring "very well"**:

| | HS or less | Some college | College grad | Postgrad | within-party edu slope |
|---|---|---|---|---|---|
| Dem/lean Dem | 36 | 52 | 63 | 72 | **+36 pts** |
| Rep/lean Rep | 10 | 12 | 12 | 13 | **+3 pts** |

Education raises trust in climate scientists **only among Democrats**. Any subgroup
moderation prediction that applies a uniform education slope across party will be wrong
in this family.

---

## 4. CEILING / FLOOR COMPRESSION AND HEADROOM

Weighted distributional facts (`_headroom.csv`):

| source / item | format | mean | sd | % at top box | % at bottom box | headroom to 100 |
|---|---|---|---|---|---|---|
| ANES 2020 scientists thermometer | 0–100 | 78.0 | 20.9 | 29.4 % at exactly 100 | 0.8 % | 22.0 pp |
| TISP 12-item composite | 1–5, 12-item mean | 71.5 | 20.6 | 9.9 % at 5.0 | 0.9 % | 28.5 pp |
| TISP single item (`TRUST_SCI_expert`) | 1–5 | 73.4 | 24.8 | 32.8 % | 3.1 % | 26.6 pp |
| TISP `CLIM_TRUST` | 1–5 | 67.0 | 32.5 | 35.5 % | 10.3 % | 33.0 pp |
| Pew W114 confidence in scientists | 4-pt | 66.8 | 26.8 | 27.9 % | 4.6 % | 33.2 pp |
| Pew W42 env-scientist composite | 4-pt, 5 items | 67.2 | 22.2 | 9.2 % | 1.4 % | 32.8 pp |
| GSS 2021–24 `consci` | 3-pt | 65.6 | 32.5 | 41.6 % | 10.4 % | 34.4 pp |
| voelkel2026 control-arm post, `Policies` | 0–100 slider | 68.0 | 29.3 | 16.7 % at 100 (30.4 % ≥ 90) | — | 32.0 pp |
| voelkel2026 control-arm post, `Companies` | 0–100 slider | 70.9 | 28.1 | 18.5 % at 100 (33.7 % ≥ 90) | — | 29.1 pp |
| voelkel2026 control-arm post, `Belief` | 0–100 slider | 65.4 | 22.5 | 2.2 % at 100 (16.4 % ≥ 90) | — | 34.6 pp |

**What this implies for the maximum plausible upward ATE.**
Nominal headroom is 22–35 pp, but the *usable* headroom is far smaller because the
top box is already occupied:
- **Single-item coarse scales (3-pt, 4-pt, single 1–5) are the most compressed**: 28–42 %
  of respondents are already at the ceiling and cannot move up at all. A message that
  moved *every remaining* respondent up one full category on the Pew 4-pt item would gain
  at most ~33 pp; realistically, a one-category shift in 10 % of the movable 72 % is
  ≈ +2.4 pp.
- **Multi-item composites are the least compressed** (TISP 12-item: only 9.9 % at ceiling,
  sd 20.6) — they preserve the most room to move and the least noise. The target study's
  12-item scale is in this class.
- **0–100 sliders** look uncompressed on paper but voelkel2026 shows 17–19 % pile-up at
  exactly 100 on high-mean outcomes; sd 22–29 pp.
- Empirically, in the design twin the *entire* control-arm pre→post drift is
  **|Δ| ≤ 2.1 pp on every one of 8 outcomes** (Belief +0.44, Concern +0.19, Policies
  +0.42, PoliciesSp +0.68, Companies −0.92, Candidate −2.12, Intent +0.02,
  IntentNp −0.28). Message ATEs in this family live in the same ±0–3 pp band, not in the
  20–35 pp of nominal headroom.
- Ceiling compression is **asymmetric by subgroup**: Democrats on climate items are at
  76–85 (headroom 15–24 pp) while Republicans are at 41–53 (headroom 47–59 pp). Any
  prediction of larger treatment effects among Republicans is a headroom statement, not
  only a persuasion statement — and gligoric2025 is the counter-evidence: five messages
  explicitly designed to raise conservatives' trust all failed.

---

## 5. YEAR-OVER-YEAR TREND VISIBLE INSIDE THE TRAIN SPLIT

**Trust in scientists fell after 2020 and has not recovered.**

- GSS `consci` (3-pt, weighted), the longest series: **1973–2018 is flat at 66–72**
  (30 waves; mean 68.4, sd of wave means 1.5, range 65.6-72.0). Then 2018 70.8 → 2021 70.3 → **2022 63.2 →
  2024 62.2**. The 2021→2024 drop of **−8.2 pp is the largest 3-year move in 51 years.**
- Pew 4-pt confidence in scientists: 2019 **73.3** → 2021 67.0 → 2022 66.8 (**−6.5 pp**).
- Pew W135 climate-scientist understanding: 2016 → 2021 → 2023, ENV26a 65.7 → 67.0 →
  63.7; ENV26b 62.6 → 62.3 → 59.3; ENV26c 58.2 → 57.0 → **50.8** (−7.4 pp since 2016;
  the "best ways to address" item fell most).
- Wellcome runs the other way over its two waves (2018 76.8 → 2020 81.7 on Q11C), which
  is the mid-2020 COVID "rally" peak; the Pew/GSS series show that peak reversing by 2022.
- **The decline is almost entirely partisan.** GSS party gap by year:
  1973–2000 the gap is **zero or slightly Republican-favouring** (+2 to +8 pp Rep in the
  1970s–80s), crosses zero ~2000–2006, then −1.4 (2012), −6.0 (2014), −5.5 (2016),
  −7.2 (2018), **−22.1 (2021), −21.4 (2022), −17.2 (2024)**. Democrats moved
  75.6 (2018) → 71.9 (2024) (−3.7); Republicans moved 68.4 → 54.7 (**−13.7**).
- Climate *attitudes* did **not** fall: CCAM `worry` 2008 55.3 → 2016 53.4 → 2021 60.9 →
  2024 59.1; "GW is happening" 71.2 → 70.3 → 73.2 → 71.4; perceived scientific consensus
  46.5 → 49.3 → 58.3 → 57.3. **Climate belief plateaued high while trust in scientists
  fell** — the two constructs decoupled after 2020.

**Implication for a study fielded 2025–26:** anchor the control level to the *2022–2024*
readings, not to pre-2020 values — i.e. generic trust ≈ 63–71 depending on format
(12-item 1–5 composite ≈ 70–72), climate-scientist trust ≈ 58–67, and a party gap of
−21 pp (generic) / −28 to −30 pp (climate-specific).

---

## 6. WEIGHTING AND COVERAGE CAVEATS

**Weighted** (survey weight named in `levels.csv:weight`): `tisp` (`WEIGHT_CNTRY`),
`anes` (`V200010b` 2020 post-election; 2024 full-sample), `pew_atp` w42/w100/w114
(`WEIGHT_W42/W100/W114`), `gss` (`wtssps` person post-stratification), `wellcome`
(`wgt`/`WGT` national weight), `ccam` (`weight_aggregate`).
`pew_atp_w135_topline` rows are Pew's own **published weighted percentages** — means are
derived from those percentages, and **no SE is available** (`se` is blank).

**Unweighted** (`weight` column says so): `voelkel2026`, `gligoric2025`, `geiger2026`,
`koetke2024`, `agley2021`. These are quota/convenience online panels; use them for
*shapes and gaps*, not for population levels.

SEs are Taylor-linearised weighted-mean SEs (design effects from the weights are
absorbed; clustering/stratification are **not** modelled, so true SEs are somewhat larger
— GSS and ANES design effects are typically 1.5–2.0, implying ~20–40 % wider intervals).

Specific caveats:
1. **`agley2021` is flagged unusable as a level anchor.** Its `Trust1_*` item mean (48.2)
   is *not* direction-corrected: the Trust in Science Inventory contains reverse-worded
   items and the raw file has no reversal. Its subgroup *gaps* are still directionally
   meaningful but attenuated. Rows carry a WARNING in `note`.
2. **Wellcome `WGM_Index` was dropped** — its scaling is not recoverable from the derived
   csv (a naïve reversal gives 29.9, inconsistent with its components at 72–82).
3. **CCAM `educ_category` changes meaning in 2021**: from 2021 on, high-school graduates
   are folded into code 1. All CCAM education rows here are rebuilt from the detailed
   `educ` variable (1–9 = HS or less, 10–11 = some college, 12–14 = Bachelor+), not from
   `educ_category`. Anyone reusing CCAM must do the same.
4. **TISP has no US party ID and no race/ethnicity** — only a 5-point conservatism
   self-placement (`DEM_POL_conservative`, coded 1 = least → 5 = most conservative; the
   top two categories are mildly non-monotonic, 4 = 57.8 vs 5 = 62.8 on `CLIM_TRUST`).
   Wellcome and gligoric2025 also lack party and race.
5. **Pew W100 contains a Black/Hispanic oversample** (4,533 of 14,497); `WEIGHT_W100`
   corrects it, and all W100 rows here are weighted, but unweighted W100 race marginals
   are not national.
6. **Pew scientist-confidence items are form-split half-samples** (`CONF_G`/`CONFD_F2`
   asked of ~half), so n ≈ 2,200–7,200 rather than the full wave.
7. **`geiger2026`/Većkalov US cell is n=125** with 78 left-leaning vs 28 right-leaning —
   its 80.3 trust-in-climate-scientists level is the highest in the whole table and should
   be treated as sample composition, not as a population anchor.
8. **gligoric2025 rated each occupation in a random subset** (~250 of the 2,248 control
   respondents per occupation), so per-occupation SEs are 1.4–1.9 pp; only the
   35-occupation grand mean has n = 2,248.
9. **ANES 2020 is US citizens 18+; Wellcome is 15+ RDD phone (65 % of the unweighted
   sample is 50+); GSS is English/Spanish-speaking adults.** The target study is
   census-quota US adults 18+, closest in structure to `voelkel2026` and `ccam`.
10. Minimum cell size enforced: 25 (40 for CCAM). No cell below that is in `levels.csv`.
