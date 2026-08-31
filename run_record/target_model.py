"""tools/target_model.py - idea_03 target-study prediction (DRAFT v5, session s7).

v4 -> v5 CHANGELOG (session s7; DESIGN.md 12; runs/20260828T083214Z_s7/val/PREREG_S7.md):
  1. A_MULT 0.40 -> 0.55, and NOTHING ELSE.  A22 is closed by MEASUREMENT.  The
     assertion-match term was the last number in the entry resting on an argument;
     anchors/ANCHORS_N.md (child `anchors-assert`, train split only, 6 studies,
     79 rows in anchors/assertion_train.csv) measures it.  Estimand, fixed in the
     pre-registration BEFORE the child reported: the EXCESS pp-of-scale-range effect
     of an elicit-and-correct arm on the item asking the respondent's own belief in
     the corrected claim (class C2), over the same arm's effect on that study's other,
     non-corrected outcomes (E_out).
       E_hat(C2) = +1.30 pp, se 0.23, dof 5, k = 6 studies, 95% CI [+0.71, +1.90];
       LOSO range +1.15 to +1.41; corroborated by the between-arm contrast
       E_arm = +1.02 pp (se 0.44, dof 1, too few dof to stand alone under R29).
     The entry's authored C2 value was 0.86 pp (its two full cells, 1.00 and 0.72).
     PREREG_S7.md rule A22-1 combines an authored prior N(0.86, 0.40^2) with the
     measurement: posterior 1.191 pp -> A_MULT = 0.40 x 1.191/0.86 = 0.554 -> 0.55
     after rounding and the R20 cap.  The rule was symmetric and was written to move
     the entry DOWN if the measurement had come back near 0.2 pp, which is what s6's
     declaration expected; it came back high instead and the same arithmetic applies.
     KIND (R27): TRAIN-SOURCED, subject to a validation-sourced constraint.  The old
     value 0.40 was authored (the smallest value keeping the assertion cell the Funding
     arm's largest) under R20's validated mix band [0.15, 0.30]; the new value is
     measured on train and still inside that band (model-side mix 0.238 -> 0.293).
     The band is what caps the move: the uncapped posterior wanted 0.554 and the band
     binds at about 0.55-0.57.
     What the measurement does NOT support, recorded rather than smoothed over:
     there is NO funding-correction arm anywhere in the train split (the Funding cell
     inherits only the generic C2 pool); the social-norm cells (High public trust) are
     supported at E_arm +0.09 +/- 0.54 pp and E_out +0.61 pp (k=1) and are RAISED here
     only because the pre-registered rule moves the multiplier and not the shape
     (A24 in OPEN.md); and the C1 class - the item asking for the corrected quantity
     itself, +9.4 pp - is worth nothing, because the target scores no C1 item.
  2. Nothing else moves.  KAPPA 0.20, S_MULT 1.00, LAM_BTW 1.00, the ASSERTION_MATCH
     shape (2.5 / 1.8 / 0.9 / 0.6), control levels, S_ARM, the outcome profile,
     donation_ams -0.40 / L_OUT 0.997, the exact-zero moderation floor and the whole
     synthesis pipeline are untouched.

v3 -> v4 CHANGELOG (session s6; DESIGN.md 11; runs/20260828T074119Z_s6/val/PREREG_S6.md):
  1. A_MULT 0.4647 -> 0.40 and S_MULT 0.6289 -> 1.00: the v3 message-level DIRECTION
     change REVERTS to the promoted state.  A18 resolved.  Two independent reasons.
     (a) TEXT: the frozen definitions place `tools` inside durable state, and only
     techniques that survive the gate enter durable state.  v3's values had exactly
     one warrant - the AM-ISO measurement - which was declared as mechanism M10/R23
     and REJECTED (runs/20260828T060726Z_s5/gate_m10-targeting.json).
     (b) EVIDENCE: the measurement does not support the move even on its own terms.
     beall2017's three matched-amplitude tables differ only in the targeted SHARE of
     message variance (0.000 / 0.712 / 1.000 -> r_adj 0.3398 / 0.5352 / 0.5451): the
     curve is 8x steeper below the incumbent share than above it, so the entry's
     v2 -> v3 move (share 0.634 -> 0.855) was worth about +0.008 r_adj.  s6 then
     re-measured the noise scale with two byte-identical replications and
     sd(r_adj|beall2017) went 0.0116 -> 0.0659 (3 dof), taking the AM-ISO reading
     from "12.6 sigma" to 2.2 sigma.
  2. donation_ams re-anchored on ANCHORS_M (the A14-residual child, train split, so
     R27 puts it under the split rule and not the gate).  Mean ATE -0.70 -> -0.40 and
     L_OUT 0.000 -> 0.997 (= 0.883 x the trust loading).  ANCHORS_M measures the
     recipient-alignment step ANCHORS_K could not close at +4.29 +/- 0.61 pp between a
     follow-through whose recipient IS the message's subject and one whose recipient is
     an aligned non-subject cause, and it corrects two arithmetic slips in ANCHORS_K's
     -0.70 that happened to cancel.  It also overturns the exact-zero between-arm SD on
     the INFERENCE: voelkel2026's tau_hat = 0 has a 95% upper limit of 1.485 and the
     same study returns tau = 0.192 for an attitude composite whose arms demonstrably
     differ, so the zero is a floor artefact of an underpowered heterogeneity design.
     Both moves were pre-registered as conditions in PREREG_S6.md 2 BEFORE the child
     reported, and both conditions were met.
  3. NOTHING ELSE MOVES.  KAPPA, LAM_BTW, control levels, S_ARM, the outcome profile,
     newsletter_signup (+0.45, ANCHORS_M explicitly recommends keeping it over its own
     +0.6), the exact-zero moderation floor and the whole synthesis pipeline are
     untouched.

v2 -> v3 CHANGELOG (session s5) - item 1 REVERTED by v4 above; item 2 stands:
  1. [REVERTED] A_MULT/S_MULT direction change on the AM-ISO measurement.
  2. donation_ams: mean ATE +0.05 -> -0.70 and L_OUT -> 0.000 (ANCHORS_K).  A
     behavioural follow-through is a near-constant negative offset plus a small
     fraction of the attitude effect, with a noise-corrected between-arm SD of 0.
     By the scorer's own directional rule the expected credit is 0.62 negative /
     0.50 exact zero / 0.38 positive, so v2's small positive was the worst of the
     three available answers (R24/R25).

v1 -> v2 CHANGELOG (each line has its evidence; see DESIGN.md 9):
  1. LAM_BTW 0.50 -> 1.00.  v1's extra shrink of the outcome profile was the M5
     mechanism.  [EVIDENCE CORRECTED TWICE - s5 and s6.  s4 read the two mix probes
     as 17-28 sigma and opposite in sign; s5's affine-class re-pooling made them
     5.3 sigma and 0.8 sigma; s6's replications made beall's sd 0.0659, so the two
     probes are now 0.9 sigma and 0.8 sigma - two nulls.  The DECISION stands, but
     it now rests on the s3 gate having PROMOTED the table that carries LAM_BTW = 1,
     not on either probe.  DESIGN X2 / R18 / 11.2.]
     With LAM_BTW = 1 the entry sits at the mix the gate actually promoted.
  2. ASSERTION_MATCH is now multiplied by A_MULT = 0.40.  In v1 the four additive
     cells were 4x larger than the whole rest of the message level and drove the
     entry to mix = 1.002, i.e. 6.6x the promoted mix and 3x the largest mix ever
     scored (DESIGN 9.4 / R20).  A_MULT = 0.40 is the SMALLEST value at which the
     assertion-match cell is still the Funding arm's own largest cell - the
     qualitative design claim survives - and it lands the table at mix = 0.249,
     inside the validated band [0.15, 0.30].
  3. S_ARM replaced by anchors/ANCHORS_H (arm_scores.csv), a train-split feature
     coding of all 16 texts.  v1's hand ordering and ANCHORS_H agree at r = 0.52;
     ANCHORS_H contains v1's facet-headroom argument plus three train-split
     corrections v1 did not have (emotive/moralised load is negative, myth-first
     debunking is negative, length is null).  ANCHORS_H's own LOSO shrinkage
     (lambda = 0.20) is NOT applied to the ordering: correlation metrics are
     scale-free, so the ordering is carried at full strength and only the
     amplitude is shrunk, which is what KAPPA does.
  4. KAPPA stays at the promoted 0.20.  ANCHORS_H's independent train-split rule
     ("arm SD ~ 0.10 x mean|ATE|, band 0.05-0.20") implies KAPPA = 0.148 with band
     0.074-0.295; 0.20 is inside it.  A promoted constant is not re-tuned on one
     new anchor without gate-grade evidence.
  5. Control levels refreshed from anchors/ANCHORS_I (A9 adjudicated).

DRAFT v1 header follows.

THE ONLY PLACE PREDICTED TARGET NUMBERS ENTER.  `tools/target_entry.py` imports
`target_table` from here; everything downstream (synthesis, verify, validator) is
mechanical.

Structure - the same three-level decomposition every validation submission used
(`tools/level_transform.py`), plus one additive design term:

    ate(a, o) =  g
              +  LAM_BTW * ( m(o) - g )        outcome level  (which outcomes move)
              +  KAPPA   * s(a) * L(o)         message level  (rank-1, DESIGN R9)
              +  A(a, o)                       assertion-match, additive (M3-v2)

KAPPA and LAM_BTW are STUDY-level scalars.  They are never varied by cell or by
outcome: doing that is what the first gate rejected (DESIGN R12/R13).

Calibration of the two scalars (measured, not assumed) - both from the two reliable
many-variant validation tasks, whose regime matches the target's (>= 6 arms that are
variants of one persuasive goal):

    KAPPA   = 0.20   message-level amplitude.  beta_within = 0.150 (beall2017, 96
                     cells) and 0.153 (goldwert2026, 204 cells); ANCHORS_C's
                     independent train-split band 0.15-0.35.  Pre-registered as
                     "kappa ~ 0.2" in REPORT s2b before any of this was scored.
    LAM_BTW = 0.50   outcome-level amplitude.  beta_between implied 0.384
                     (beall2017) and 0.418 (goldwert2026) at kappa=1; measured
                     again directly after kappa=0.20 as 0.402 and 0.561.

Levels and profiles come from anchors/ (train split only).  No target outcome data
exists anywhere in this container and none was sought.
"""
import numpy as np
import pandas as pd

KAPPA = 0.20      # promoted (gate_m1w-v2-k02.json).  Sets the message level's TOTAL
                  # amplitude; v3 does not change it, and the message level's total
                  # norm is identical in v2 and v3 (1.5884 pp, mix inside [0.15,0.30]).
LAM_BTW = 1.00    # v2: the extra outcome-profile shrink is REJECTED (DESIGN X2/R18)

# v3: the message level's DIRECTION, measured.  AM-ISO (runs/20260828T060726Z_s5,
# PREREG_AM.md) held the outcome profile and the total message norm fixed on four
# validation studies and moved the message budget between the content-TARGETED cells
# and the GENERIC arm-quality ordering.  Targeted won on 4 of 4:
#   beall2017 +0.205 r_adj (12.6 sigma), dablander2025 +0.408 (21.5), goldwert2026
#   +0.216 (2.3), kim2024 +0.211 (1.8).  On beall2017, the only task where the
# decomposition is well conditioned, the r_adj-optimal targeted:generic norm ratio is
# X/Y = 4.0 (1 sigma band 2.9-6.6) against an allocation of 1.57 actually used - my
# authoring is generic-heavy by 2.55x (band 1.85-4.20).
# v3 applies the LOWER end of that band, 1.85, to the entry's own v2 ratio (1.315),
# giving a targeted:generic norm ratio of 2.43, at unchanged total norm.  Nothing
# here is a per-cell kappa override (DESIGN R12/R13): both terms are message level,
# the split is a direction and not an amplitude, and the mix (DESIGN R20) is unchanged.
A_MULT = 0.55     # v5: MEASURED (A22 closed).  ANCHORS_N, train split, 6 studies:
                  # the class-C2 excess of an elicit-and-correct arm on the own-belief
                  # item about the corrected claim is +1.30 pp (se 0.23, dof 5, CI
                  # [0.71, 1.90], LOSO 1.15-1.41).  PREREG_S7 rule A22-1 (written
                  # before the child reported, and symmetric): posterior of the
                  # authored 0.86 pp prior N(0.86, 0.40^2) and the measurement is
                  # 1.191 pp, so A_MULT = 0.40 x 1.191/0.86 = 0.554 -> 0.55 under the
                  # R20 mix cap.  KIND (R27): train-sourced under a validation-sourced
                  # band; mix 0.238 -> 0.293, still inside the validated [0.15, 0.30].
                  # v4 held 0.40 as an AUTHORED value (smallest value keeping the
                  # assertion cell the Funding arm's own largest), which is why a train
                  # measurement of the same quantity governs it and no gate is needed.
                  # The two social-norm cells rise with it although ANCHORS_N does not
                  # support them (A24); the shape is not re-authored, by rule.
S_MULT = 1.00     # v4: REVERTED.  v3 set these to 0.4647 / 0.6289 on the AM-ISO
                  # measurement, which was declared to the gate as mechanism M10/R23 and
                  # REJECTED (gate_m10-targeting.json, failure family
                  # "donation/behavioral outcomes").  The frozen definitions put `tools`
                  # inside durable state and let only gate-surviving techniques into it,
                  # so a constant whose sole warrant is a rejected technique cannot stay.
                  # It also does not survive its own evidence: beall2017's three
                  # matched-amplitude points (targeted share 0.000 / 0.712 / 1.000 ->
                  # r_adj 0.3398 / 0.5352 / 0.5451) show the curve SATURATES at or below
                  # where the entry already sits, and the s6 replications raised
                  # sd(r_adj|beall) from 0.0116 to 0.0659, taking the whole measurement
                  # from 12.6 sigma to 2.2 sigma.  DESIGN 11; PREREG_S6.md.

# --------------------------------------------------------------- control levels
# Native units.  0-100 sliders / composites; donation in dollars; signup a rate.
# Source: anchors/outcome_profile.csv (ANCHORS_E, 13 rows over 46 study x measure
# train-split cells) with anchors/ANCHORS_D.md owning the trust block.
# Recorded disagreement (OPEN A9): ANCHORS_D recommends 60-67 for a
# climate-scientist composite; ANCHORS_E derives 69 (TISP 12-item generic 71.5,
# minus the 4-5 pp climate-specific penalty, plus 2-4 pp for the 0-100 slider
# format).  ANCHORS_E is the anchor of record here because it was built for these
# 13 outcomes specifically; the level enters Tier-2 means and Section-3 shapes,
# never the ATEs.
CONTROL_MEAN = {
    "trust_multidimensional": 65.0,   # v2: ANCHORS_I, A9 ADJUDICATED (band 61-69)
    "trust_post":             66.0,   # v2: direct TISP CLIM_TRUST anchor; now ABOVE the composite
    "distrust_post":          32.0,   # NOT 100 - trust; modelled complement of 66 (sum ~98)
    "funding_perceptions":    64.0,   # 100 - funding_5; GSS natsci 2021-24 = 66.5
    "policy_role_mean":       67.0,   # TISP NORMPERC = the target's items verbatim
    "inst_trust_mean":        56.0,   # NASA/NPS high, federal government low
    "belief_post":            68.0,
    "concern_mean":           58.0,
    "policy_general":         66.0,
    "policy_specific_mean":   61.0,
    "behavior_mean":          40.0,
    "donation_ams":            4.40,  # v2: ANCHORS_I. The $10 is a LOTTERY (100 of ~18,000
                                      # selected, p ~ 0.006), so the expected cost of donating
                                      # a dollar is ~$0.006 - a near-hypothetical allocation,
                                      # and AMS is described as explicitly non-partisan.
    "newsletter_signup":       0.115, # proportion (ANCHORS_I band 0.05-0.20)
}

# The four trust subscales that compose the primary outcome.  Openness is the weak
# facet and therefore carries the headroom (ANCHORS_D: transparency 59.4,
# "admits mistakes" 57.5, competence 75.4).  Mean == CONTROL_MEAN[primary].
# v2: re-centred on 65 (A9) AND the facet spread halved.  ANCHORS_I could not support
# the "climate scientists lose most on integrity/openness" assumption and found evidence
# it may be BACKWARDS (pew_atp W42: environmental scientists rate BETTER than medical on
# "admits mistakes" +2.1 and "transparent about conflicts" +1.8, worse on "does a good
# job" -1.8; gligoric2025 shows no credible-vs-trustworthy gap for climatologists).
# An unsupported, possibly-inverted spread is shrunk toward flat, not carried at v1 size.
SUBSCALE_LEVEL = {"competence": 69.0, "integrity": 64.5,
                  "benevolence": 65.5, "openness": 61.0}

# ------------------------------------------------- outcome level: m(o), raw pp
# Mean ATE across the 16 arms for each outcome, in pp of scale range, BEFORE
# LAM_BTW.  = ANCHORS_E responsiveness x BASE_ATE_PP.
#
# ANCHORS_E's headline, and the thing that reorganised this table: responsiveness
# is a DISTANCE property, not an outcome property.  The target's 16 texts assert
# things about CLIMATE SCIENTISTS, so trust is the proximal block and all eleven
# other outcomes are one propagation step downstream - the inverse of
# voelkel2026 / vlasceanu2024, where belief/concern/policy are proximal.  The
# measured one-step discount is 0.21 (band 0.10-0.30), replicated six ways, and
# the decay FLATTENS after the first step (so it must not be chained twice).
# distrust_post is negative because it is NOT reverse-coded in cleaning;
# funding_perceptions is positive because it IS (= 100 - funding_5).
# newsletter_signup is high not because opting in is easy but because 1 point of
# RATE is 1.0 scored pp: a binary outcome is scale-efficient and can out-move the
# primary slider (vlasceanu's binary moved 4.5x its belief slider in one sample).
BASE_ATE_PP = 1.00                     # ANCHORS_E band 0.5-2.0 on the primary
M_RAW = {o: r * BASE_ATE_PP for o, r in {
    "trust_multidimensional":  +1.00,
    "trust_post":              +1.05,
    "distrust_post":           -0.75,
    "funding_perceptions":     +0.30,
    "policy_role_mean":        +0.30,
    "inst_trust_mean":         +0.28,
    "belief_post":             +0.28,
    "concern_mean":            +0.22,
    "policy_general":          +0.20,
    "policy_specific_mean":    +0.17,
    "behavior_mean":           +0.18,
    "donation_ams":            -0.40,   # v4: ANCHORS_M (A14 residual CLOSED).  A third
                                        # independent train-split read priced the one thing
                                        # ANCHORS_K could not: recipient alignment.  Same
                                        # specification on all five usable behavioural outcomes
                                        # (behaviour ~ treat + matched POST attitude), giving a
                                        # subject-aligned pole of +1.97 +/- 0.32 (voelkel2024's
                                        # dictator game, stable at 1/3/12 covariates) against a
                                        # cause-aligned pole of -2.32 +/- 0.52 (voelkel2026 and
                                        # vlasceanu WEPT, IV-pooled): a SWING of +4.29 +/- 0.61
                                        # pp, 7.1 sigma.  The AMS is the message's own subject,
                                        # so the entry gets w = 0.35 of the way to the subject
                                        # pole: direct -0.82, plus a +0.40 attitude pass-through,
                                        # centre -0.4 (band -1.6..+1.1).  It also corrects two
                                        # arithmetic slips in ANCHORS_K's -0.70 that cancelled
                                        # (a 0.5x attitude scaling against behavioural_levels,
                                        # and an absolute -2.5 carried across a 62 -> 44 pp
                                        # control-level change).  Caveat kept in the open: the
                                        # subject pole is ONE study and no train study randomises
                                        # the recipient, so the subject-vs-cause step is between
                                        # studies (OPEN A21).  Still negative, so the 0.62
                                        # directional credit of R25 is intact.
                                        # [superseded v3 note] ANCHORS_K (A14 RESOLVED, against v2):
                                        # INDEPENDENT second read of behavioural follow-through
                                        # decomposed the design twin: holding POST attitudes
                                        # fixed the direct effect on giving is -2.42 +/- 0.91
                                        # (voelkel2026) and -2.53 +/- 0.63 (vlasceanu WEPT),
                                        # i.e. a near-constant negative offset, NOT a shrunken
                                        # copy of the attitude effect: beh ~ -2.5 + 0.5*attitude.
                                        # It also falsified end-of-survey fatigue as the cause
                                        # for this design (arm-level corr(ATE, reading time)
                                        # = +0.08) and found that the target puts BOTH
                                        # behavioural asks mid-battery, not last.  Centre -0.7
                                        # (band -2.0..+0.6) rather than v26's -1.4 only because
                                        # the recipient (AMS) is the message's own subject, the
                                        # one contrast (voelkel2024, ratio 0.877, r = 0.832)
                                        # where recipient alignment is even indirectly measured.
                                        # Expected directional credit: 0.62 negative / 0.50
                                        # exact zero / 0.38 positive.  v2's +0.05 was the worst
                                        # of the three - it forfeited the guaranteed half credit
                                        # without buying the sign.
    "newsletter_signup":       +0.45,   # wide band 0.00-1.60
}.items()}

# --------------------------------------------- message level: rank-1 s(a), L(o)
# s(a): standardised arm score.  Read off the organizers' own family tags
# (survey/condition_codenames.csv, DESIGN 6.5) plus the facet-headroom argument:
# competence is already high (77) and has little room, openness/integrity are the
# weak facets (61-68), so arms that speak to transparency, process and motive
# outrank arms that restate competence.  This is design information only.
# v2: anchors/arm_scores.csv (ANCHORS_H).  sd(s) = 0.60.  Ordering carried at full
# strength (scale-free metrics); amplitude lives in KAPPA alone.  ANCHORS_H could
# NOT validate the ordering on train ("if assertion match is wrong, flat is right"):
# its 17-feature scheme scored LOSO r = -0.37 across three held-out megastudies, and
# the two train studies whose arm sets are as narrowly matched as the target's
# (gligoric2025, spampatti2023) had a noise-corrected between-arm SD of EXACTLY ZERO.
# The only replicable text-level signals are negative ones (emotive/moralised load,
# myth-first debunking) and they are in these numbers.  Length, narrative form,
# numeric evidence and named source are coded EXACTLY ZERO - all tested, all null.
S_ARM = {
    "Interview Prof. Maraun":        0.965,   # flimsy fish  [medium]
    "Peer-review":                   0.678,   # honored haddock  [medium]
    "Portrait Prof. Cherry":         0.634,   # complicated cockroach  [low]
    "Corporate reliance":            0.390,   # giant gibbon  [low]
    "Extreme weather predictions":   0.303,   # practical planarian  [medium]
    "Former skeptics":               0.303,   # limping llama  [low]
    "Interview Prof. Sebille":       0.282,   # heartfelt hummingbird  [low]
    "Consensus":                     0.181,   # jealous jaguar  [medium]
    "Model accuracy":                0.030,   # apple aardvark  [low]
    "Scientist community helpers":   -0.071,   # periwinkle partridge  [low]
    "Measurement & modeling (2)":    -0.143,   # orchid orangutan  [medium]
    "Funding":                       -0.157,   # phony parrotfish  [low]
    "Measurement & modeling (1)":    -0.473,   # perfect prawn  [medium]
    "High public trust":             -0.826,   # crushing chicken  [low]
    "Oil industry misinformation":   -1.027,   # worse wildfowl  [low]
    "Social justice":                -1.070,   # difficult dog  [medium]
}

# L(o): outcome loading of the rank-1 message term, in pp per unit of s(a).
# ANCHORS_C: the loading is NOT flat (CV 0.25-0.84), and the natural shape is the
# responsiveness profile itself - an arm that is better at moving trust is better
# at moving everything trust propagates into.  Scaled (x1.129, since sd(s)=0.62)
# so the RAW message-level SD on the trust block is 0.70 pp, the centre of
# ANCHORS_C's noise-corrected true band (0.4-0.8 pp).  KAPPA then shrinks it.
L_OUT = {
    "trust_multidimensional":  1.129,
    "trust_post":              1.186,
    "distrust_post":          -0.847,
    "funding_perceptions":     0.339,
    "policy_role_mean":        0.339,
    "inst_trust_mean":         0.316,
    "belief_post":             0.316,
    "concern_mean":            0.248,
    "policy_general":          0.226,
    "policy_specific_mean":    0.192,
    "behavior_mean":           0.203,
    "donation_ams":            0.997,   # v4: 0.883 x the trust loading.  ANCHORS_M (A14
                                        # residual, train split) overturns v3's exact zero on
                                        # the INFERENCE, not the point estimate: voelkel2026's
                                        # raw 1.19 < mean SE 1.65 does give tau_hat = 0.000, but
                                        # profile-ML puts the 95% upper limit at 1.485, and the
                                        # SAME study returns tau = 0.192 [<=1.287] for its own
                                        # attitude composite, whose arms demonstrably differ.
                                        # It is an underpowered heterogeneity design: the zero
                                        # is a floor artefact.  The informative estimate is
                                        # voelkel2024 (25 arms): tau(behaviour)/tau(attitude)
                                        # = 0.883 with arm-level r = +0.829, i.e. the arms that
                                        # move attitudes move giving, in the same order.
                                        # Pre-registered override condition (PREREG_S6.md 2:
                                        # "> 0.15 pp with its own correction shown") is met.
                                        # The gate's own failure family ("donation/behavioral")
                                        # points the same way: the s5 candidate zeroed
                                        # dablander's donation ordering and lost there.
    "newsletter_signup":       0.508,
}

# ------------------------------------------------- M3-v2: assertion match, additive
# DESIGN 6.6.  Exactly the cells where an arm elicits a quantity and corrects it
# on-screen, and a scored item later asks for that same quantity.  Entered as an
# ADDITIVE post-shrink term, never as a per-cell kappa override - the per-cell
# override is what the first gate rejected.  Units: pp of scale range.
ASSERTION_MATCH = {
    # v5: the SHAPE below is unchanged and stays AUTHORED; only A_MULT is measured.
    # ANCHORS_N's classes: the first two cells are C2 (the item asks the respondent's
    # own belief in the corrected claim; measured excess +1.30 pp), the last two are
    # C2n (the corrected quantity is a social norm; measured excess +0.61 pp on one
    # study, E_arm +0.09 +/- 0.54 on two - i.e. NOT supported at the size they now
    # carry, 0.495 and 0.330 pp).  Recorded as A24 rather than patched, because
    # PREREG_S7 rule A22-1 fixes the shape and moves only the multiplier.
    ("Funding", "funding_perceptions"):            2.5,  # elicits, then corrects with $ figures
    ("Consensus", "belief_post"):                  1.8,  # elicits agreement, then states 99%
    ("High public trust", "trust_post"):           0.9,  # norm -> personal attitude, half strength
    ("High public trust", "trust_multidimensional"): 0.6,
    # Ceiling: ANCHORS_D bounds realistic message ATEs at 0-3 pp (the design
    # twin's own control-arm pre-post drift is |d| <= 2.1 pp), so no cell in this
    # table exceeds 3 pp even where the assertion match is near-mechanical.
}

# ------------------------------------------------------------- moderator levels
# MAIN EFFECTS on the level (not interactions).  ANCHORS_D: party gap -27..-31 pp
# on climate-specific items, education +9-11 pp end to end, race/age/gender |<=3| pp.
# `clim` scales how climate-politicised an outcome is.
CLIM_WEIGHT = {
    "trust_multidimensional": 1.00, "trust_post": 1.00, "distrust_post": -1.00,
    "funding_perceptions": 0.85, "policy_role_mean": 0.70, "inst_trust_mean": 0.80,
    "belief_post": 1.15, "concern_mean": 1.20, "policy_general": 1.10,
    "policy_specific_mean": 1.05, "behavior_mean": 0.60,
    "donation_ams": 0.50, "newsletter_signup": 0.50,
}
PARTY_DELTA = {"Democrat": 11.0, "Independent": -3.0,
               "Republican": -16.0, "Other": -5.0}          # pp, x CLIM_WEIGHT
EDUC_DELTA = {"Less than high school": -6.0, "High school diploma / GED": -4.0,
              "Some college or Associate's degree": -1.0, "Bachelor's degree": 2.0,
              "Master's degree / Professional degree": 4.0,
              "Doctorate degree / Ph.D.": 6.0}
AGE_DELTA = {"18-29": 2.0, "30-44": 1.0, "45-59": -1.0, "60+": -2.0}
GENDER_DELTA = {"Male": -1.5, "Female": 1.5, "Other": 2.0}
RACE_DELTA = {"White / Caucasian": -1.0, "Black / African American": 2.0,
              "Hispanic / Latino": 2.0, "Asian / Asian American": 1.5, "Other": 0.0}
INCOME_DELTA = {"Less than $30,000": -1.0, "$30,000 to $55,999": -0.5,
                "$56,000 to $99,999": 0.0, "$100,000 to $167,999": 0.8,
                "$168,000 or more": 1.2}

# response shape: native-scale SD per outcome (ANCHORS_G refines these)
SHAPE_SD = {o: 22.0 for o in M_RAW}
SHAPE_SD.update({"trust_multidimensional": 21.0, "policy_role_mean": 20.0,
                 "inst_trust_mean": 20.0, "concern_mean": 26.0,
                 "policy_specific_mean": 21.0, "behavior_mean": 24.0,
                 "trust_post": 28.0, "distrust_post": 28.0, "donation_ams": 3.83,
                 "newsletter_signup": None})   # v2 SDs: anchors/behavioural_levels.csv

# v2: the control-arm response shape of `donation_ams` is TRI-modal, not bimodal -
# anchors/donation_shape.csv (ANCHORS_I): p(0) = 0.288, p(5) = 0.175, p(10) = 0.217,
# everything else <= 0.065.  The midpoint spike ranges from 4% (voelkel2026, $1 stake)
# to 48% (voelkel2024) in train and cannot be dropped; Section 3's OVL/KS/W1 read it.
DONATION_PMF_CSV = "anchors/donation_shape.csv"


def target_table(S, rng=None):
    """Return the draft target entry, in the contract tools/target_entry.py expects."""
    C, O = S["conditions"], S["outcomes"]
    interventions = [c for c in C if c != "control"]

    g = float(np.mean([M_RAW[o] for o in O]))
    ate = pd.DataFrame(0.0, index=C, columns=O)
    for o in O:
        outcome_level = g + LAM_BTW * (M_RAW[o] - g)
        for a in interventions:
            ate.loc[a, o] = outcome_level + S_MULT * KAPPA * S_ARM[a] * L_OUT[o]
    for (a, o), v in ASSERTION_MATCH.items():
        ate.loc[a, o] += A_MULT * v          # v2: R20 bound, DESIGN 9.4
    ate.loc["control"] = 0.0                     # control is the reference row

    mod_delta = {}
    for m, levels in S["moderators"].items():
        d = pd.DataFrame(0.0, index=levels, columns=O)
        src = {"party": PARTY_DELTA, "education": EDUC_DELTA, "age_band": AGE_DELTA,
               "gender": GENDER_DELTA, "race": RACE_DELTA, "income": INCOME_DELTA}[m]
        for lv in levels:
            for o in O:
                w = CLIM_WEIGHT[o] if m == "party" else 1.0
                # deltas are authored in pp of scale range; synthesize() adds
                # mod_delta in NATIVE units, so convert here.
                d.loc[lv, o] = (src[lv] * w * (0.35 if m != "party" else 1.0)
                                * S["scale_range"][o] / 100.0)
        mod_delta[m] = d

    return dict(control_mean=dict(CONTROL_MEAN), ate_pp=ate,
                mod_delta=mod_delta, shape=dict(SHAPE_SD),
                subscale_level=dict(SUBSCALE_LEVEL))
