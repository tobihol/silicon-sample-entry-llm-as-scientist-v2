#!/usr/bin/env python
"""
target_entry.py -- STRUCTURE ONLY (idea_03, session s2b).

Backward synthesis harness for the Silicon Sample Benchmark target entry.
Every number produced here is a PLACEHOLDER; the point of the file is the path:

    analysis-first table  ->  synthetic rows  ->  benchmark's own analyses
                                              ->  verification that the rows
                                                  reproduce the table.

Stages
------
S1  spec()          reads /workspace/benchmark (submission_spec.R + codebook.csv)
                    -> the 17 conditions, 13 outcomes, 6 moderators, scale ranges.
S2  target_table()  the ONLY place predicted numbers enter:
                      control_mean[outcome]                (level, 0-100 / $ / prop)
                      ate_pp[condition, outcome]           (pp of scale range)
                      mod_delta_pp[moderator_level, outcome] (level shift, no interaction
                                                            unless explicitly set)
                      shape[outcome] = (sd, dist family, clipping)
S3  synthesize()    draws individual rows from the table, honouring the census
                    quotas and the Tier-1 precision floor.
S4  verify()        recomputes condition x outcome means, ATEs vs control, and the
                    condition x moderator interaction contrasts FROM THE ROWS and
                    reports max |recovered - intended|.
S5  write_entry()   writes predictions/<team>_T1_<entry>_v1.csv in the analysis
                    schema, plus optional T2/T3 mirrors for inspection.

Run: /opt/kernel/venv/bin/python tools/target_entry.py --out <scaffold dir>
Then: cd <scaffold dir> && make manifest && make check
"""
import argparse, json, re, sys
from pathlib import Path
import sys
import numpy as np
try:
    sys.path.insert(0, "/workspace/run/anchors")
    import shape_lib                       # ANCHORS_G response-shape library
except Exception:                          # pragma: no cover
    shape_lib = None

# item counts per composite (codebook.csv section B): a composite is the mean of k
# INTEGER 0-100 sliders, so it lives on a 1/k lattice, not on the integers.
K_ITEMS = {"trust_multidimensional": 12, "policy_role_mean": 4, "inst_trust_mean": 5,
           "concern_mean": 3, "policy_specific_mean": 7, "behavior_mean": 6}
import pandas as pd

BENCH = Path("/workspace/benchmark")

# ---------------------------------------------------------------- S1  spec
def spec():
    src = (BENCH / "scripts/lib/submission_spec.R").read_text()

    def rvec(name):
        m = re.search(name + r"\s*<-\s*c\((.*?)\n\s*\)", src, re.S)
        return re.findall(r'"([^"]+)"', m.group(1))

    interventions = rvec("interventions")
    outcomes = rvec("  outcomes")
    mod_block = re.search(r"moderators <- list\((.*?)\n  \)", src, re.S).group(1)
    moderators = {}
    for mm in re.finditer(r"(\w+)\s*=\s*c\((.*?)\)", mod_block, re.S):
        moderators[mm.group(1)] = re.findall(r'"([^"]+)"', mm.group(2))
    trust_items = [f"trust_{d}_{i}" for d in
                   ("competence", "integrity", "benevolence", "openness") for i in (1, 2, 3)]
    scale_range = {o: 100.0 for o in outcomes}
    scale_range["donation_ams"] = 10.0
    scale_range["newsletter_signup"] = 1.0
    return dict(conditions=["control"] + interventions, interventions=interventions,
                outcomes=outcomes, moderators=moderators, trust_items=trust_items,
                scale_range=scale_range)


# ---------------------------------------------------------------- S2  table
# The real predicted numbers live in tools/target_model.py (idea_03 draft v1).
# `_placeholder_table` below is kept only as the format contract / fallback.
try:
    from target_model import target_table            # noqa: F401
except ImportError:  # pragma: no cover
    from tools.target_model import target_table      # noqa: F401


def _placeholder_table(S, rng):
    C, O = S["conditions"], S["outcomes"]
    control_mean = {o: 50.0 for o in O}
    control_mean["donation_ams"] = 2.0            # dollars
    control_mean["newsletter_signup"] = 0.10      # proportion

    ate_pp = pd.DataFrame(0.0, index=C, columns=O)   # pp of scale range
    ate_pp.loc["control"] = 0.0                      # control is the reference row

    # per-outcome level shift by moderator level (a main effect, NOT an interaction)
    mod_delta = {m: pd.DataFrame(0.0, index=lv, columns=O)
                 for m, lv in S["moderators"].items()}

    # response shape per outcome: sd on the native scale
    shape = {o: 22.0 for o in O}
    shape["donation_ams"] = 2.5
    shape["newsletter_signup"] = None                # Bernoulli
    return dict(control_mean=control_mean, ate_pp=ate_pp, mod_delta=mod_delta, shape=shape)


# ---------------------------------------------------------------- S3  rows
# US census-quota marginals; PLACEHOLDER weights, replaced by the real quotas.
QUOTA = dict(
    gender={"Male": .49, "Female": .50, "Other": .01},
    age_band={"18-29": .21, "30-44": .26, "45-59": .24, "60+": .29},
    race={"White / Caucasian": .60, "Black / African American": .13,
          "Hispanic / Latino": .18, "Asian / Asian American": .06, "Other": .03},
    education={"Less than high school": .09, "High school diploma / GED": .28,
               "Some college or Associate's degree": .28, "Bachelor's degree": .22,
               "Master's degree / Professional degree": .11, "Doctorate degree / Ph.D.": .02},
    income={"Less than $30,000": .22, "$30,000 to $55,999": .21,
            "$56,000 to $99,999": .25, "$100,000 to $167,999": .21,
            "$168,000 or more": .11},
    party={"Republican": .30, "Democrat": .32, "Independent": .34, "Other": .04},
)

def _center(resid, key_arrays, passes=8):
    """Sweep the residuals until their mean is ~0 in EVERY marginal moderator
    level as well as overall (iterative marginal centring). This is what makes
    the synthetic rows carry the intended cell means and the intended ZERO
    condition x moderator interactions instead of sampling noise."""
    e = np.asarray(resid, dtype=float)
    for _ in range(passes):
        for k in key_arrays:
            s = pd.Series(e)
            e = (s - s.groupby(pd.Series(k).to_numpy()).transform("mean")).to_numpy()
        e = e - e.mean()
    return e


def _quota_exact(levels, probs, n, rng):
    """Deterministic largest-remainder allocation of `n` rows to `levels`.

    The target is census-QUOTA sampled, so the moderator composition is fixed by
    design, not drawn.  Allocating it exactly (rather than multinomially) makes
    every condition carry the SAME composition, which is what makes the recovered
    ATE equal the intended ATE: with a random draw, the realised party/education
    mix differs by condition and, multiplied by moderator main effects of up to
    16 pp, injects ~0.3-0.6 pp of pure composition noise into every ATE.
    """
    raw = np.asarray(probs, dtype=float) * n
    base = np.floor(raw).astype(int)
    for i in np.argsort(-(raw - base))[: n - base.sum()]:
        base[i] += 1
    out = np.repeat(np.asarray(levels, dtype=object), base)
    return rng.permutation(out)


def _round_preserving(y, groups, lo, hi):
    """Integer-ise `y` so that each group's SUM is preserved exactly.

    Every scored item in this instrument is integer-valued (codebook.csv: the
    donation is in whole dollars, "All 0-100 slider items are also integers"),
    so a synthetic row set cannot carry a fractional cell mean.  Largest-remainder
    rounding inside each condition keeps the cell mean on the finest lattice the
    row count allows (1/n) instead of letting rounding bias walk it off.
    """
    y = np.clip(np.asarray(y, dtype=float), lo, hi)
    out = np.floor(y).astype(int)
    frac = y - out
    for g in np.unique(groups):
        idx = np.flatnonzero(groups == g)
        need = int(round(frac[idx].sum()))
        if need <= 0:
            continue
        cand = idx[out[idx] < hi]
        order = cand[np.argsort(-frac[cand])][:need]
        out[order] += 1
    return np.clip(out, lo, hi)


def _repair_cells(y, mu, keys, lo, hi, passes=8, step=1.0, rng=None):
    """Balance every marginal moderator cell mean onto the integer lattice.

    `_center` zeroes the residual mean inside each condition x moderator-level
    cell, but reflection at the bounds and integer rounding both re-inject error,
    and in the smallest cells (gender "Other" is 1% of an arm, ~30 rows) one
    stray unit is 0.03 native units per row.  This sweeps +1/-1 pairs - one unit
    into a deficient cell, one out of the largest surplus cell - so the CONDITION
    total is conserved exactly while each marginal cell is driven onto the
    nearest achievable lattice point.
    """
    y = np.asarray(y, dtype=float).copy()
    mu = np.asarray(mu, dtype=float) * np.ones(len(y))
    rng = np.random.default_rng(12345) if rng is None else rng
    for _ in range(passes):
        moved = 0
        for k in keys:
            k = np.asarray(k)
            for lv in np.unique(k):
                idx = np.flatnonzero(k == lv)
                need = int(round((mu[idx].mean() - y[idx].mean()) * len(idx) / step))
                if need == 0:
                    continue
                st = step if need > 0 else -step
                src = np.flatnonzero(k != lv)
                if len(src) == 0:            # the "all rows" key: move one-sided
                    cand = idx[(y[idx] + st >= lo - 1e-9) & (y[idx] + st <= hi + 1e-9)]
                    cand = rng.permutation(cand)[:abs(need)]
                    y[cand] += st
                    moved += len(cand)
                    continue
                a = idx[(y[idx] + st >= lo - 1e-9) & (y[idx] + st <= hi + 1e-9)]
                b = src[(y[src] - st >= lo - 1e-9) & (y[src] - st <= hi + 1e-9)]
                if len(a) == 0 or len(b) == 0:
                    continue
                # choose the moved rows AT RANDOM.  Selecting them by residual
                # extremity (the obvious choice) is a variance ratchet: every
                # sweep pulls the most extreme rows toward mu, and after 14
                # passes over 27 moderator levels it had flattened trust_post
                # from SD 24 to SD 11 and erased donation's entire zero spike.
                # Random selection leaves the response SHAPE untouched while
                # still moving the cell mean.
                #
                # Move by as many lattice STEPS as the cell needs, not one.  A
                # composite of k items lives on a 1/k lattice, so a 30-row cell
                # that is 1 pp out needs ~360 single steps and can never get
                # there at one step per row per pass; that ceiling, not sampling
                # noise, was what pinned the smallest interaction cells.
                # Multi-step moves were tried and reverted: clipping at the
                # bounds breaks the +/-  symmetry of the swap, so the CONDITION
                # mean drifts and max ATE error went 0.025 -> 1.87 pp.  One step
                # per row per pass keeps the ATEs exact; the price is that the
                # smallest marginal cells (gender "Other", ~1% of an arm) cannot
                # always be driven all the way onto the lattice.  That is the
                # right trade: Section 1 is the headline metric and the human
                # interaction contrast in those cells is itself pure noise.
                n_mv = min(abs(need), len(a), len(b))
                if n_mv == 0:
                    continue
                a = rng.permutation(a)[:n_mv]
                b = rng.permutation(b)[:n_mv]
                y[a] += st
                y[b] -= st
                moved += n_mv
        if moved == 0:
            break
    # the eligibility test carries a 1e-9 tolerance so lattice arithmetic does not
    # lock rows that sit exactly on a bound; snap back afterwards so no value can
    # print as 100.000000001 and trip the validator's range check.
    return np.clip(np.round(y / step) * step, lo, hi)


def synthesize(S, T, n_control=1000, n_intervention=500, seed=20260828, exact=False):
    rng = np.random.default_rng(seed)

    # quota-weighted centring of the moderator main effects: a level shift is a
    # statement about the GAP between levels, not about the population mean, so
    # the population-weighted mean of every mod_delta column must be zero or the
    # control level drifts away from the anchored value.
    modq = {}
    for m in S["moderators"]:
        w = pd.Series(QUOTA[m])
        d = T["mod_delta"][m]
        modq[m] = d.sub((d.mul(w.reindex(d.index), axis=0)).sum(axis=0), axis=1)

    rows, pid, deck = [], 0, None
    for cond in S["conditions"]:
        n = n_control if cond == "control" else n_intervention
        if exact:
            # ONE profile deck, reused by every condition (tiled for the larger
            # control arm).  Quota-exact marginals alone are not enough: within a
            # small marginal cell such as gender "Other" (1% of the arm) the JOINT
            # mix of the other five moderators still varies by condition, and with
            # party main effects of up to 16 pp that put ~7 pp of pure composition
            # noise on the smallest condition x moderator interaction contrasts.
            # A shared deck makes every condition x moderator-level cell carry an
            # identical composition, so the predicted ZERO interactions come out
            # of the rows as zeros rather than as noise.
            if deck is None or len(deck["_n"]) != n_intervention:
                deck = {m: _quota_exact(list(QUOTA[m]), list(QUOTA[m].values()),
                                        n_intervention, rng)
                        for m in S["moderators"]}
                deck["_n"] = np.zeros(n_intervention)
            reps = int(np.ceil(n / n_intervention))
            d = {m: np.tile(deck[m], reps)[:n] for m in S["moderators"]}
        else:
            d = {m: rng.choice(list(QUOTA[m]), size=n, p=list(QUOTA[m].values()))
                 for m in S["moderators"]}
        rec = {"profile_id": [f"p{pid + i:06d}" for i in range(n)],
               "condition": [cond] * n, **d}
        pid += n
        for o in S["outcomes"]:
            mu = T["control_mean"][o] + T["ate_pp"].loc[cond, o] * S["scale_range"][o] / 100.0
            for m in S["moderators"]:
                mu = mu + modq[m].reindex(d[m])[o].to_numpy()
            # condition x moderator-level INTERACTION (ANCHORS_F; zero for every
            # moderator except party, and zero in the control arm by definition)
            if cond != "control" and o in T.get("mod_inter", {}).get("party", {}):
                mu = mu + T["mod_inter"]["party"].reindex(d["party"])[o].to_numpy()
            mu = mu * np.ones(n)

            if o == "newsletter_signup":
                p = np.clip(mu, 0, 1)
                if exact:
                    # systematic (Madow) selection: each row keeps inclusion
                    # probability p_i, but the REALISED number of sign-ups is
                    # exactly round(sum p_i), so the cell rate carries no
                    # sampling noise.  A binomial draw would put ~0.6 pp of pure
                    # synthesis noise on an outcome whose whole predicted ATE is
                    # 0.3 pp - and 1 point of rate is 1.0 scored pp here.
                    order = rng.permutation(n)
                    c = np.cumsum(p[order])
                    sel = np.zeros(n, dtype=int)
                    sel[order] = (np.diff(np.concatenate(
                        ([0.0], np.floor(c + 1e-12)))) > 0).astype(int)
                    rec[o] = _repair_cells(
                        sel, p, [np.zeros(n, dtype=int)]
                                + [np.asarray(d[m]) for m in S["moderators"]],
                        0, 1, step=1.0, passes=14)
                else:
                    rec[o] = rng.binomial(1, p)
                continue

            hi = 10.0 if o == "donation_ams" else 100.0
            step = 1.0 / K_ITEMS.get(o, 1)          # composites live on a 1/k lattice
            if exact and shape_lib is not None:
                # ANCHORS_G: draw the CONTROL-CONDITION EMPIRICAL SHAPE rather than a
                # clipped Gaussian.  Measured on the 47 matched train items with the
                # organizers' own Section-3 metrics, this is OVL .852 / KS .052 /
                # W1 1.77 against OVL .776 / KS .105 / W1 4.99 for a clipped Gaussian
                # given the true SD.  ANCHORS_G also measures dSD/dmean = +0.021
                # +/- 0.040 across treated arms, i.e. a message is a PURE LOCATION
                # SHIFT, so `control_mean=` locks the treated SD to the control SD
                # and the predicted variance ratio is 1.00 everywhere.
                draws = np.sort(shape_lib.sample(
                    o, n, float(mu.mean()), rng,
                    control_mean=float(T["control_mean"][o])))
                # rank-assign the shape to the rows so the moderator gradient in
                # `mu` survives the transform, then repair the cell means.
                z = mu + rng.normal(0, T["shape"][o] or 1.0, n)
                y = draws[np.argsort(np.argsort(z))]
                rec[o] = _repair_cells(
                    y, mu, [np.zeros(n, dtype=int)]
                            + [np.asarray(d[m]) for m in S["moderators"]],
                    0.0, hi, step=step, passes=14)
            elif exact:
                e = _center(rng.normal(0, T["shape"][o], n),
                            [np.asarray(d[m]) for m in S["moderators"]])
                y = mu + e
                tgt = float(mu.mean())
                for _ in range(60):
                    y = np.where(y < 0, -y, y)
                    y = np.where(y > hi, 2 * hi - y, y)
                    gap = tgt - float(y.mean())
                    if abs(gap) < 1e-9:
                        break
                    y = y + gap
                yi = _round_preserving(y / step, np.zeros(n, dtype=int), 0, hi / step) * step
                rec[o] = _repair_cells(yi, mu, [np.asarray(d[m]) for m in S["moderators"]],
                                       0.0, hi, step=step)
            else:
                rec[o] = np.clip(np.round(mu + rng.normal(0, T["shape"][o], n)), 0, hi)
            if o == "donation_ams":
                rec[o] = np.asarray(rec[o]).astype(int)
        rows.append(pd.DataFrame(rec))
    df = pd.concat(rows, ignore_index=True)

    # trust items: 12 integer sliders whose four subscale means average to the
    # submitted primary outcome, per codebook.csv (check_lib warns if they drift).
    prim = df["trust_multidimensional"].to_numpy()
    items = np.clip(np.round(prim[:, None] + rng.normal(0, 8, (len(df), 12))), 0, 100)
    sub = items.reshape(len(df), 4, 3).mean(axis=2)
    items = np.clip(items + (prim - sub.mean(axis=1))[:, None], 0, 100)
    for j, it in enumerate(S["trust_items"]):
        df[it] = items[:, j]
    df["trust_multidimensional"] = items.reshape(len(df), 4, 3).mean(axis=2).mean(axis=1)
    return df


# ---------------------------------------------------------------- S4  verify
def verify(S, T, df):
    out = {}
    cells = df.groupby("condition")[S["outcomes"]].mean()
    ate = (cells - cells.loc["control"])
    ate_pp = ate.divide(pd.Series(S["scale_range"]), axis=1) * 100.0
    err = (ate_pp - T["ate_pp"].reindex(ate_pp.index)[ate_pp.columns]).abs()
    out["max_abs_ate_error_pp"] = float(err.to_numpy().max())
    out["mean_abs_ate_error_pp"] = float(err.to_numpy().mean())

    # Section 2: condition x moderator interaction contrast, recomputed as the
    # organizers' lm(outcome ~ condition * moderator) coefficient would be:
    # (cell[c, lvl] - cell[control, lvl]) - (cell[c, ref] - cell[control, ref]).
    worst = 0.0
    for m, levels in S["moderators"].items():
        ref = levels[0]
        g = df.groupby(["condition", m])[S["outcomes"]].mean()
        for c in S["conditions"][1:]:
            for lv in levels[1:]:
                try:
                    d = ((g.loc[(c, lv)] - g.loc[("control", lv)])
                         - (g.loc[(c, ref)] - g.loc[("control", ref)]))
                except KeyError:
                    continue
                worst = max(worst, float(np.abs(d.to_numpy()).max()))
    out["max_abs_interaction_pp_native"] = worst
    out["n_rows"] = int(len(df))
    out["min_n_per_condition"] = int(df["condition"].value_counts().min())
    return out


# ---------------------------------------------------------------- S5  write
def write_entry(S, df, outdir, team="example", entry="primary", version=1):
    outdir = Path(outdir)
    (outdir / "predictions").mkdir(parents=True, exist_ok=True)
    cols = (["profile_id", "condition"] + list(S["moderators"])
            + ["trust_multidimensional"] + S["trust_items"]
            + [o for o in S["outcomes"] if o != "trust_multidimensional"])
    p1 = outdir / "predictions" / f"{team}_T1_{entry}_v{version}.csv"
    df[cols].to_csv(p1, index=False)

    # Tier-2 / Tier-3 mirrors are NOT part of a Tier-1 deposit (one repo = one
    # entry = one tier, and `make manifest` fingerprints everything matching
    # predictions/<team_id>_*.csv). They live in derived/ for inspection only.
    der = outdir / "derived"; der.mkdir(parents=True, exist_ok=True)
    cells = df.groupby("condition")[S["outcomes"]].mean()
    t2 = cells.reset_index().melt("condition", var_name="outcome", value_name="mean")
    t2.to_csv(der / f"{team}_T2_{entry}_v{version}_cells_main.csv", index=False)
    recs = []
    for m, levels in S["moderators"].items():
        g = df.groupby(["condition", m])[S["outcomes"]].mean().reset_index()
        g = g.melt(["condition", m], var_name="outcome", value_name="mean")
        g = g.rename(columns={m: "moderator_level"}); g["moderator"] = m
        recs.append(g[["condition", "moderator", "moderator_level", "outcome", "mean"]])
    pd.concat(recs).to_csv(der / f"{team}_T2_{entry}_v{version}_cells_moderator.csv", index=False)
    t3 = (cells - cells.loc["control"]).drop(index="control").reset_index().melt(
        "condition", var_name="outcome", value_name="ate")
    t3.to_csv(der / f"{team}_T3_{entry}_v{version}.csv", index=False)
    return p1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/workspace/run/target_entry_scaffold")
    ap.add_argument("--n-control", type=int, default=1000)
    ap.add_argument("--n-intervention", type=int, default=500)
    ap.add_argument("--exact", action="store_true",
                    help="mean-matched synthesis: remove the sampling error of every "
                         "mean the scorer reads (cells and moderator cells)")
    a = ap.parse_args()
    S = spec()
    rng = np.random.default_rng(0)
    T = target_table(S, rng)
    df = synthesize(S, T, a.n_control, a.n_intervention, exact=a.exact)
    rep = verify(S, T, df)
    p = write_entry(S, df, a.out)
    print(json.dumps(dict(conditions=len(S["conditions"]), outcomes=len(S["outcomes"]),
                          moderators={k: len(v) for k, v in S["moderators"].items()},
                          file=str(p), **rep), indent=1))


if __name__ == "__main__":
    main()
