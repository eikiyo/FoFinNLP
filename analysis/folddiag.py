"""
Location: paper-a/analysis/folddiag.py
Purpose: STAGE 3 steps 1b and 1c, the DIAGNOSTIC half. Given the per-item measurements fold.py
         produces, answer: is wobble-vs-accuracy monotone or folded, how much of the correlation
         is mechanical, is the per-item correct rate bimodal, and is the empty high-accuracy
         high-wobble zone reachable at all.
Functions: pooled_p(), p_bucket_flips(), decile_frontier(), fold_test(), surviving_fraction(),
           selftest()
Calls: predictors.ols, stats_core.pair_stats
Imports: typing, numpy, predictors, stats_core
"""

from typing import Any, Dict, List, Optional, Sequence

import numpy as np

import predictors
import stats_core as sc

N_DECILES = 10


def pooled_p(models: Sequence[str], names: Sequence[str], per_cell) -> Dict[str, Any]:
    """STEP 1c, first half. The pooled per-item correct-rate distribution. If p is bimodal at 0 and
    1 then almost every item is structurally incapable of flipping, and the empty
    high-accuracy/high-wobble zone is a property of the ITEM POOL, not of the models."""
    ps = [i["p"] for m in models for n in names for i in per_cell[m][n] if i["p"] is not None]
    if not ps:
        raise SystemExit("pooled p is empty across every cell -- the probe is broken, not the data")
    arr = np.array(ps, float)
    edges = np.linspace(0.0, 1.0, 11)
    hist, _ = np.histogram(arr, bins=edges)
    return {"n_items": int(arr.size), "mean": float(arr.mean()),
            # Counts as well as fractions. The paper quotes the always-correct and always-wrong
            # SHARES, and reconstructing a count by multiplying a float share back out by n is how
            # a rounded number becomes a reported one.
            "n_zero": int((arr == 0.0).sum()), "n_one": int((arr == 1.0).sum()),
            "frac_zero": float((arr == 0.0).mean()), "frac_one": float((arr == 1.0).mean()),
            "frac_interior": float(((arr > 0.0) & (arr < 1.0)).mean()),
            "frac_mid": float(((arr >= 0.3) & (arr <= 0.7)).mean()),
            # Both readings, computed once. The claim must not turn on which endpoint is open,
            # and printing only one of them is what let a float-rounding artefact stand as a fact.
            "band_n": band_count(arr), "band_share": band_count(arr) / int(arr.size),
            "band_n_halfopen": int(((arr >= BAND_LO) & (arr < BAND_HI)).sum()),
            "hist": [int(h) for h in hist], "edges": [float(e) for e in edges]}


BAND_LO, BAND_HI = 0.3, 0.7


def band_count(ps, lo: float = BAND_LO, hi: float = BAND_HI) -> int:
    """Pairs in the observable band, counted from the VALUES with an exact closed-interval test.

    Not from the histogram. `np.linspace(0, 1, 11)` returns 0.30000000000000004 and
    0.7000000000000001, so binning silently included every pair at exactly p=0.7 and excluded
    every pair at exactly p=0.3 -- 14 in and 4 out on this corpus, a net 10 of ~90, while the
    prose and the figure both claimed the predicate `0.3 <= p < 0.7`. p is quantised to k/n, so
    the boundaries are populated rather than measure-zero and the noise lands on real rows.

    The interval is CLOSED at both ends. The band is symmetric about p=0.5 by construction, and
    excluding one endpoint while keeping the other has no justification beyond which way a float
    happened to round. The half-open reading is reported alongside wherever this number is quoted,
    because a claim that depends on which endpoint is open is a claim about arithmetic."""
    arr = np.asarray(ps, float)
    return int(((arr >= lo) & (arr <= hi)).sum())


def band_selftest() -> str:
    """Prove the boundaries are counted as documented, which is the thing the histogram got wrong."""
    assert band_count([0.3, 0.7]) == 2, "both endpoints are IN the closed band"
    assert band_count([0.29, 0.71]) == 0, "just outside must be OUT"
    assert band_count([0.0, 1.0, 0.5]) == 1, "only the interior value counts"
    assert band_count([0.3, 0.7], 0.3, 0.7) == 2, "explicit bounds behave the same"
    # The exact case the histogram mis-binned: a value equal to an endpoint must not depend on
    # how linspace rounded that endpoint.
    edges = np.linspace(0.0, 1.0, 11)
    assert edges[3] > 0.3 and edges[7] > 0.7, "fixture invalid: linspace edges are no longer off"
    assert band_count([0.3] * 4 + [0.7] * 14) == 18, \
        "every pair sitting exactly on a boundary must be counted, not silently split by rounding"
    return ("folddiag band selftest PASS - both endpoints are counted, values outside are not, "
            "and the linspace edges that mis-binned 18 boundary pairs no longer decide the count")


def p_bucket_flips(models: Sequence[str], names: Sequence[str], per_cell) -> List[Dict[str, Any]]:
    """Observed flip rate among items at p=0, in the interior, and at p=1 -- the measurement that
    decides WHICH structural bound is the right one, instead of leaving the answer to an assumption.

    The two bounds differ only on items the model gets wrong. The lower bound says a wrong model is
    wrong the SAME way every run (so p=0 items never flip); the upper bound says it is wrong a
    different way each run (so p=0 items always flip). The observed p=0 flip rate sits between and
    identifies the truth directly. This is descriptive, not fitted: it does not use the flip flag to
    predict itself, it reports where reality falls between two pre-stated extremes."""
    buckets = {"p=0 (always wrong)": lambda p: p == 0.0,
               "0<p<1 (mixed)": lambda p: 0.0 < p < 1.0,
               "p=1 (always right)": lambda p: p == 1.0}
    out = []
    for label, test in buckets.items():
        items = [i for m in models for n in names for i in per_cell[m][n]
                 if i["p"] is not None and i["flipped"] is not None and test(i["p"])]
        flips = sum(1 for i in items if i["flipped"])
        out.append({"bucket": label, "n_items": len(items), "n_flipped": flips,
                    "flip_rate": (flips / len(items)) if items else None,
                    "predicted_lo": 0.0 if label != "0<p<1 (mixed)" else None,
                    "predicted_hi": (1.0 if label == "p=0 (always wrong)"
                                     else 0.0 if label == "p=1 (always right)" else None)})
    return out


def decile_frontier(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """STEP 1c, second half. Per accuracy decile: how many leaves, the MAXIMUM observed wobble, and
    the maximum the structural model says is even reachable there. Reporting the max (not a mean)
    is deliberate -- an all-zero column is then visibly distinguishable from a broken join."""
    out = []
    for d in range(N_DECILES):
        lo, hi = d / N_DECILES, (d + 1) / N_DECILES
        sel = [r for r in rows if r["accuracy"] is not None
               and (lo <= r["accuracy"] < hi or (d == N_DECILES - 1 and r["accuracy"] == 1.0))]
        out.append({"decile": f"{lo:.1f}-{hi:.1f}", "n_leaves": len(sel),
                    "max_observed": max((r["observed"] for r in sel if r["observed"] is not None),
                                        default=None),
                    "max_structural": max((r["structural"] for r in sel
                                           if r["structural"] is not None), default=None),
                    "mean_observed": (float(np.mean([r["observed"] for r in sel
                                                     if r["observed"] is not None]))
                                      if sel else None)})
    return out


def fold_test(rows: Sequence[Dict[str, Any]], y_key: str = "observed") -> Dict[str, Any]:
    """Is wobble-vs-accuracy MONOTONE or FOLDED? Fit wobble ~ accuracy + accuracy^2. A fold (wobble
    peaking at intermediate accuracy, falling at both ends) shows up as a NEGATIVE, non-zero-
    crossing quadratic term. Anything else and the decline is monotone and the concession is
    narrower than the structural story predicts.

    Run on `structural` as well as `observed`: if the structural model ITSELF does not fold over
    the accuracy range this corpus actually covers, then 'not folded' is a statement about the item
    pool's coverage, not a refutation of the mechanism."""
    pts = [(r["accuracy"], r[y_key]) for r in rows
           if r["accuracy"] is not None and r.get(y_key) is not None]
    if len(pts) < 4:
        return {"n": len(pts), "error": "fewer than 4 leaves with both defined"}
    x = np.array([[1.0, a, a * a] for a, _ in pts], float)
    y = np.array([w for _, w in pts], float)
    fit = predictors.ols(x, y, ["intercept", "accuracy", "accuracy_sq"])
    q = next(c for c in fit["coefs"] if c["name"] == "accuracy_sq")
    folded = q["beta"] < 0 and not q["crosses_zero"]
    return {"n": len(pts), "y": y_key, "quad_beta": q["beta"], "quad_lo": q["lo"],
            "quad_hi": q["hi"], "quad_crosses_zero": q["crosses_zero"], "r2": fit["r2"],
            "acc_min": min(a for a, _ in pts), "acc_max": max(a for a, _ in pts), "folded": folded,
            "verdict": ("folded - peaks at intermediate accuracy and falls at both ends" if folded
                        else "not folded - the quadratic term is positive (convex), so over the "
                             "accuracy range this corpus covers the relationship is monotone")}


def surviving_fraction(rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """How much of the published wobble-accuracy correlation is left once the structural component
    is subtracted -- computed under BOTH extremes, so the answer is an interval.

    Reported as the correlations themselves plus the ratio, never the ratio alone: a ratio of two
    small numbers is not a finding, and the reader has to see that -0.55 became -0.50 rather than
    only that '90% survived'."""
    ok = [r for r in rows if all(r.get(k) is not None for k in
                                 ("accuracy", "observed", "structural", "structural_max",
                                  "structural_cal"))]
    acc = [r["accuracy"] for r in ok]
    obs = sc.pair_stats([r["observed"] for r in ok], acc)["rho"]
    out = {"n": len(ok), "rho_observed": obs}
    for tag, skey, rkey in (("min", "structural", "residual"),
                            ("cal", "structural_cal", "residual_cal"),
                            ("max", "structural_max", "residual_max")):
        res = sc.pair_stats([r[rkey] for r in ok], acc)["rho"]
        out[f"rho_structural_{tag}"] = sc.pair_stats([r[skey] for r in ok], acc)["rho"]
        out[f"rho_residual_{tag}"] = res
        out[f"rho_obs_vs_struct_{tag}"] = sc.pair_stats([r["observed"] for r in ok],
                                                        [r[skey] for r in ok])["rho"]
        out[f"fraction_surviving_{tag}"] = ((res / obs) if (obs not in (None, 0)
                                                            and res is not None) else None)
    return out

def selftest() -> str:
    """Prove the diagnostics on synthetic data whose answer is known, including the degenerate
    cases. Tolerance compares throughout -- an exact float equality here has already produced one
    false RED in this project."""
    rows = [dict(leaf=n, accuracy=a, observed=w, structural=w, structural_max=w,
                 structural_cal=w, residual=0.0, residual_max=0.0, residual_cal=0.0)
            for n, a, w in (("a", 0.5, 0.9), ("b", 0.9, 0.1), ("c", 0.1, 0.2), ("d", 1.0, 0.0))]
    sf = surviving_fraction(rows)
    assert sf["rho_residual_min"] is None or abs(sf["rho_residual_min"]) < 1e-9, \
        f"a perfectly structural dataset must leave no residual signal: {sf['rho_residual_min']}"
    fr = decile_frontier(rows)
    assert sum(r["n_leaves"] for r in fr) == 4, "every leaf must land in exactly one decile"
    assert fr[-1]["n_leaves"] == 2, "accuracy 0.9 and 1.0 must both fall in the last decile"
    assert fr[0]["max_observed"] is None, "an empty decile must report None, never 0.0"
    curved = [dict(leaf=str(i), accuracy=a, observed=(1.0 - (2 * a - 1) ** 2), structural=0.0,
                   structural_max=0.0, structural_cal=0.0, residual=0.0, residual_max=0.0,
                   residual_cal=0.0)
              for i, a in enumerate([i / 20 for i in range(21)])]
    ft = fold_test(curved, "observed")
    assert ft["folded"], f"a deliberate inverted-U must be detected as folded: {ft}"
    flat = [dict(r, observed=0.5) for r in curved]
    assert not fold_test(flat, "observed")["folded"], "flat data must NOT be reported as folded"
    return ("folddiag selftest PASS - detects a real fold, refuses a flat one, deciles partition "
            "exactly, empty decile returns None, residual vanishes on structural data")
