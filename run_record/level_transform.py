"""tools/level_transform.py - idea_03.

The three-level ATE decomposition that every idea_03 val submission and the target
entry are built from.  A predicted ATE table for one study is written as

    ate(a, o) = g  +  ( m(o) - g )  +  ( ate(a, o) - m(o) )
                ^        ^                  ^
                |        |                  message level  (arm x outcome residual)
                |        outcome level  (which outcomes move at all)
                study/grand level

and each level carries its own amplitude multiplier:

    ate'(a, o) = g + lam_btw * ( m(o) - g ) + kap * ( ate(a, o) - m(o) )

`kap` is M1w (message-level shrink); `lam_btw` is M5 (outcome-profile amplitude).
Both are STUDY-level scalars applied uniformly to every cell of the study.  Applying
them per-cell or per-outcome is forbidden - see DESIGN.md R12/R13 and the proof in
`within_invariance()` below.
"""
import numpy as np
import pandas as pd


def transform(df, kap=1.0, lam_btw=1.0, lam_all=1.0, outcome_col="outcome",
              value_col="ate"):
    """Return a copy of `df` with the three-level amplitudes applied."""
    d = df.copy()
    x = d[value_col].astype(float)
    g = x.mean()
    mo = x.groupby(d[outcome_col]).transform("mean")
    d[value_col] = lam_all * (g + lam_btw * (mo - g) + kap * (x - mo))
    return d


def decompose(df, outcome_col="outcome", value_col="ate"):
    """Variance shares of the outcome level vs the message level."""
    x = df[value_col].astype(float)
    mo = x.groupby(df[outcome_col]).transform("mean")
    btw, wth = mo.var(ddof=0), (x - mo).var(ddof=0)
    tot = x.var(ddof=0)
    return dict(n=len(x), mean=x.mean(), sd_tot=np.sqrt(tot),
                sd_btw=np.sqrt(btw), sd_wth=np.sqrt(wth),
                share_btw=btw / tot if tot > 0 else np.nan)


def pearson_within(h, l, outcome):
    """The organizers' pearson_within_outcome(), reimplemented for checking."""
    d = pd.DataFrame({"h": h, "l": l, "o": outcome}).dropna()
    d["hc"] = d.h - d.groupby("o").h.transform("mean")
    d["lc"] = d.l - d.groupby("o").l.transform("mean")
    if len(d) < 3 or d.hc.std() == 0 or d.lc.std() == 0:
        return np.nan
    return float(np.corrcoef(d.hc, d.lc)[0, 1])


def within_invariance(df, truth, kaps=(1.0, 0.5, 0.2, 0.05)):
    """Demonstrate that a study-uniform `kap` cannot move r_within at all.

    The organizers centre both sides within outcome and then take ONE pooled
    Pearson r.  Scaling every within-outcome residual of the submission by the
    same constant rescales `l_c` and leaves the correlation exactly unchanged.
    Therefore M1w applied uniformly is invisible to r_within_adj, and any
    r_within movement attributed to it was fresh-draw noise.  A kappa that
    differs ACROSS outcomes is not a shrink at all: it re-weights outcomes in
    the pooled r_within and rescales the outcome profile.  That is what the
    s2 candidate did and what the first gate rejected.
    """
    return {k: pearson_within(truth, transform(df, kap=k).ate.values,
                              df.outcome.values) for k in kaps}


REGIME = {
    # brief-only regime test: >= 6 treatment arms that are variants of one
    # persuasive goal  ->  "many-variant" (megastudy-shaped); else "distinct".
    "many_variant": dict(kap=0.20, lam_btw=0.45),
    "distinct":     dict(kap=1.00, lam_btw=1.00),
}


def regime_of(n_arms, variants_of_one_goal=True):
    return "many_variant" if (n_arms >= 6 and variants_of_one_goal) else "distinct"
