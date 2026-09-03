"""
Location: paper-a/analysis/conservative.py
Purpose: STAGE 3 steps 1a and 1d. Rebuild the worst-to-mean ratio on the most PESSIMISTIC reading
         the data permits (Wilson lower bound of the worst category against the Wilson upper bound
         of the mean), and restate the capability claim as a regression with no shared denominator.
         If the conservative ratio collapses toward 1, that is the finding and the spine changes.
Functions: model_totals(), _estimable(), _ranked(), conservative_rows(), worst_on_mean(),
           best_models_absolute(), selftest()
Calls: categories.wilson, predictors.ols
Imports: typing, numpy, categories, predictors
"""

from typing import Any, Dict, List, Optional, Sequence

import numpy as np

import categories
import predictors

STRICT_MIN_LEAVES = 5      # the 1a sensitivity floor, stricter than categories.MIN_LEAVES (3)
RATIO_BAR = 2.0            # "how many models still exceed 2x at the lower bound"


def model_totals(models: Sequence[str], names: Sequence[str], cells) -> Dict[str, Dict[str, int]]:
    """Per model, the two counts every interval in this module is built from: flipped items and
    measured items summed over ALL leaves. Counts, never rates -- a Wilson interval needs k and n,
    and averaging per-leaf rates would weight a 3-item leaf like a 30-item one."""
    out = {}
    for m in models:
        out[m] = {"flipped": sum(cells[m][n]["flipped"] for n in names),
                  "measured": sum(cells[m][n]["n_items"] for n in names)}
    return out


def _estimable(cat_cells_m: Dict[str, Dict[str, Any]], min_leaves: int) -> Dict[str, Dict]:
    """That model's categories that clear a leaf-count floor and actually measured something.
    The floor is a parameter, not the module constant, because 1a reports both 3 and 5."""
    return {c: v for c, v in cat_cells_m.items()
            if v["n_leaves"] >= min_leaves and v["measured"] > 0 and v["rate"] is not None}


def _ranked(est: Dict[str, Dict], key: str) -> List[tuple]:
    """Categories ordered worst-first on `key` (`rate` for the point estimate, `lo` for the
    selection-robust form). Returned as a list so the second-worst is addressable."""
    return sorted(est.items(), key=lambda kv: -(kv[1][key] or 0.0))


def conservative_rows(models: Sequence[str], cat_cells, totals, min_leaves: int
                      ) -> List[Dict[str, Any]]:
    """Per model, every ratio the paper could quote, from most permissive to most pessimistic.

    `robust_*` is the PRIMARY conservative form: the largest Wilson LOWER bound over categories,
    i.e. the category we can be most confident is genuinely bad. Taking the point-estimate winner
    and then quoting its lower bound (`point_worst_lo`) is exposed to the winner's curse -- the
    category that looks worst is partly the one that got lucky -- so it is reported beside, never
    as the headline. `excl` removes the worst category's items from the mean's denominator, because
    the worst category otherwise sits INSIDE the quantity it is being compared against."""
    rows = []
    for m in models:
        t = totals[m]
        m_lo, m_hi = categories.wilson(t["flipped"], t["measured"]) or (None, None)
        est = _estimable(cat_cells[m], min_leaves)
        row = {"model": m, "n_estimable": len(est), "min_leaves": min_leaves,
               "mean": (t["flipped"] / t["measured"]) if t["measured"] else None,
               "mean_lo": m_lo, "mean_hi": m_hi, "measured": t["measured"]}
        rows.append(_fill_ratios(row, est, t) if est else _blank_ratios(row))
    return rows


def _blank_ratios(row: Dict[str, Any]) -> Dict[str, Any]:
    for k in ("point_cat", "robust_cat", "second_cat"):
        row[k] = None
    for k in ("point_rate", "point_lo", "point_hi", "robust_lo", "robust_rate", "second_rate",
              "second_lo", "point_ratio", "cons_ratio", "cons_ratio_point", "cons_ratio_excl",
              "mean_excl_hi"):
        row[k] = None
    return row


def _fill_ratios(row: Dict[str, Any], est: Dict[str, Dict], t: Dict[str, int]) -> Dict[str, Any]:
    """The four ratios, all built from the same two Wilson bounds so they are directly comparable."""
    by_rate, by_lo = _ranked(est, "rate"), _ranked(est, "lo")
    pc, pv = by_rate[0]
    rc, rv = by_lo[0]
    row.update({"point_cat": pc, "point_rate": pv["rate"], "point_lo": pv["lo"],
                "point_hi": pv["hi"], "robust_cat": rc, "robust_rate": rv["rate"],
                "robust_lo": rv["lo"],
                "second_cat": by_rate[1][0] if len(by_rate) > 1 else None,
                "second_rate": by_rate[1][1]["rate"] if len(by_rate) > 1 else None,
                "second_lo": by_rate[1][1]["lo"] if len(by_rate) > 1 else None})
    excl_k, excl_n = t["flipped"] - pv["flipped"], t["measured"] - pv["measured"]
    excl = categories.wilson(excl_k, excl_n) if excl_n > 0 else None
    row["mean_excl_hi"] = excl[1] if excl else None
    hi, mean = row["mean_hi"], row["mean"]
    row["point_ratio"] = (pv["rate"] / mean) if mean else None
    row["cons_ratio"] = (rv["lo"] / hi) if (hi and rv["lo"] is not None) else None
    row["cons_ratio_point"] = (pv["lo"] / hi) if (hi and pv["lo"] is not None) else None
    row["cons_ratio_excl"] = (rv["lo"] / row["mean_excl_hi"]) if row["mean_excl_hi"] else None
    return row


def survivors(rows: Sequence[Dict[str, Any]], bar: float = RATIO_BAR) -> Dict[str, Any]:
    """How many models still clear the bar once every number is read pessimistically. This is the
    single figure that decides whether the paper's spine survives step 1a."""
    defined = [r for r in rows if r["cons_ratio"] is not None]
    return {"n_models": len(rows), "n_defined": len(defined), "bar": bar,
            "n_over_bar": sum(1 for r in defined if r["cons_ratio"] > bar),
            "n_over_bar_point": sum(1 for r in defined
                                    if (r["point_ratio"] or 0) > bar),
            "models_over_bar": [r["model"] for r in defined if r["cons_ratio"] > bar],
            "median_cons": float(np.median([r["cons_ratio"] for r in defined])) if defined else None,
            "median_point": float(np.median([r["point_ratio"] for r in defined
                                             if r["point_ratio"] is not None])) if defined else None}


def worst_on_mean(rows: Sequence[Dict[str, Any]], y_key: str = "point_rate",
                  keep: Optional[Sequence[str]] = None, label: str = "all") -> Dict[str, Any]:
    """STEP 1d. Regress WORST-category wobble on MEAN wobble -- the capability claim with no shared
    denominator anywhere. A slope BELOW 1 would mean the worst category falls more SLOWLY than the
    mean as models improve, which is the paper's claim stated without ever forming a ratio.

    The INTERCEPT is returned too, and it matters more than the slope: a ratio that grows as models
    improve can be produced entirely by a positive intercept (worst -> a > 0 while mean -> 0), which
    is a different sentence from 'the worst category resists improvement'.

    n = 12 models, and two of them sit an order of magnitude away from the rest, so `keep` runs the
    same fit on a pre-registered subset rather than leaving the result to two leverage points."""
    sel = [r for r in rows if keep is None or r["model"] in set(keep)]
    pts = [(r["mean"], r[y_key]) for r in sel
           if r["mean"] is not None and r.get(y_key) is not None]
    if len(pts) < 3:
        return {"n": len(pts), "y": y_key, "label": label, "error": "fewer than 3 models"}
    x = np.array([[1.0, a] for a, _ in pts], float)
    fit = predictors.ols(x, np.array([b for _, b in pts], float), ["intercept", "mean_wobble"])
    slope = next(c for c in fit["coefs"] if c["name"] == "mean_wobble")
    icept = next(c for c in fit["coefs"] if c["name"] == "intercept")
    return {"n": len(pts), "y": y_key, "label": label, "slope": slope["beta"], "se": slope["se"],
            "lo": slope["lo"], "hi": slope["hi"], "r2": fit["r2"],
            "intercept": icept["beta"], "intercept_lo": icept["lo"], "intercept_hi": icept["hi"],
            "intercept_above_zero": bool(icept["lo"] > 0.0),
            "slope_below_one": bool(slope["hi"] < 1.0),
            "interval_spans_one": bool(slope["lo"] <= 1.0 <= slope["hi"])}


def best_models_absolute(rows: Sequence[Dict[str, Any]], k: int = 3) -> List[Dict[str, Any]]:
    """The k most stable models by MEAN wobble, with their ABSOLUTE worst-category figures.

    The paper must quote absolutes beside every ratio: '5x' between 2.5% and 12.5% reads nothing
    like '5x' between 10% and 50%, and a reviewer outside the project will ask which one it is."""
    ok = sorted([r for r in rows if r["mean"] is not None], key=lambda r: r["mean"])[:k]
    return [{"model": r["model"], "mean": r["mean"], "point_cat": r["point_cat"],
             "point_rate": r["point_rate"], "point_lo": r["point_lo"], "point_hi": r["point_hi"],
             "robust_cat": r["robust_cat"], "robust_lo": r["robust_lo"],
             "point_ratio": r["point_ratio"], "cons_ratio": r["cons_ratio"]} for r in ok]


def selftest() -> str:
    """Prove the conservative machinery goes RED on the corruption it exists to catch, and GREEN on
    a known-good case. A gate proven only on convenient input has not been proven."""
    cells = {"cat_bad": {"n_leaves": 6, "measured": 100, "flipped": 40, "rate": 0.40,
                         "lo": categories.wilson(40, 100)[0], "hi": categories.wilson(40, 100)[1]},
             "cat_ok": {"n_leaves": 6, "measured": 100, "flipped": 5, "rate": 0.05,
                        "lo": categories.wilson(5, 100)[0], "hi": categories.wilson(5, 100)[1]},
             "cat_tiny": {"n_leaves": 2, "measured": 10, "flipped": 9, "rate": 0.90,
                          "lo": categories.wilson(9, 10)[0], "hi": categories.wilson(9, 10)[1]}}
    tot = {"M": {"flipped": 45, "measured": 200}}
    r = conservative_rows(["M"], {"M": cells}, tot, min_leaves=5)[0]
    assert r["point_cat"] == "cat_bad", f"1-leaf-floor breach: {r['point_cat']}"
    assert r["n_estimable"] == 2, f"the 2-leaf category must be excluded at floor 5: {r}"
    assert r["cons_ratio"] < r["point_ratio"], "conservative ratio must be below the point ratio"
    assert r["mean_excl_hi"] < r["mean_hi"], "removing the worst category must lower the mean"
    flat = {c: dict(v, flipped=20, rate=0.20, lo=categories.wilson(20, 100)[0],
                    hi=categories.wilson(20, 100)[1]) for c, v in cells.items() if c != "cat_tiny"}
    rf = conservative_rows(["M"], {"M": flat}, {"M": {"flipped": 40, "measured": 200}},
                           min_leaves=5)[0]
    assert abs(rf["point_ratio"] - 1.0) < 1e-12, f"flat data must give ratio 1: {rf['point_ratio']}"
    assert rf["cons_ratio"] < 1.0, "flat data must give a conservative ratio below 1"
    empty = conservative_rows(["M"], {"M": {}}, tot, min_leaves=5)[0]
    assert empty["cons_ratio"] is None, "no estimable category must yield None, never a number"
    return ("conservative selftest PASS - floor excludes small categories, conservative < point, "
            "flat data collapses to 1, degenerate input returns None")
