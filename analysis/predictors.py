"""
Location: paper-a/analysis/predictors.py
Purpose: STEP 3, second half. A small, interpretable, DESCRIPTIVE model of what predicts a leaf's
         mean wobble across models. 60 leaves and a handful of predictors is not a predictive
         model and is never presented as one: adjusted R^2 sits beside R^2, every coefficient
         carries an interval, and the leaf count is quoted in the same breath as the fit.
Functions: leaf_features(), design_matrix(), ols(), fit_report(), nested_comparison()
Calls: none (pure over leaf metadata + the wobble matrix)
Imports: json, typing, numpy, config
"""

import json
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

import config

ARITHMETIC_TYPES = ("number",)


def leaf_features(leaves: List[Dict[str, Any]], answer_types: Dict[str, str]) -> List[Dict]:
    """One feature row per leaf. Every feature is derivable from artefacts already on disk -- no
    new annotation, so nothing here can disagree with the benchmark."""
    out = []
    for l in leaves:
        d = config.probity_root() / l["rel"]
        n_items, doc_chars = 0, []
        path = d / "oracle.jsonl"
        if path.exists():
            for line in path.read_text().splitlines():
                if line.strip():
                    n_items += 1
        qdir = d / "corpus" / "questions"
        if qdir.exists():
            doc_chars = [p.stat().st_size for p in sorted(qdir.iterdir()) if p.is_file()]
        out.append({
            "leaf": l["leaf"], "family": l["family"], "answer_type": answer_types.get(l["leaf"]),
            "n_items": n_items,
            "clause_chars": float(np.median(doc_chars)) if doc_chars else None,
            "is_numeric": 1.0 if answer_types.get(l["leaf"]) == "numeric" else 0.0,
            "is_binary": 1.0 if answer_types.get(l["leaf"]) == "binary" else 0.0,
            "is_multi": 1.0 if answer_types.get(l["leaf"]) == "multi_part" else 0.0,
        })
    return out


def design_matrix(feats: List[Dict], cols: Sequence[str]) -> Tuple[np.ndarray, List[str], List[int]]:
    """X with an intercept, plus the row indices that survived. Rows with a missing predictor are
    DROPPED and counted, never imputed -- a mean-imputed clause length would invent a data point
    and quietly shrink the interval around every other coefficient."""
    keep, rows = [], []
    for i, f in enumerate(feats):
        vals = [f.get(c) for c in cols]
        if any(v is None for v in vals):
            continue
        keep.append(i)
        rows.append([1.0] + [float(v) for v in vals])
    return np.array(rows, float), ["intercept"] + list(cols), keep


def ols(x: np.ndarray, y: np.ndarray, names: Sequence[str]) -> Dict[str, Any]:
    """Least squares with classical standard errors. numpy only -- no new dependency for what is
    a 5-column regression."""
    n, p = x.shape
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    resid = y - x @ beta
    dof = n - p
    if dof <= 0:
        return {"n": n, "p": p, "error": "more predictors than observations"}
    sigma2 = float(resid @ resid) / dof
    xtx_inv = np.linalg.pinv(x.T @ x)
    se = np.sqrt(np.maximum(np.diag(xtx_inv) * sigma2, 0.0))
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - float(resid @ resid) / ss_tot if ss_tot > 0 else None
    adj = (1 - (1 - r2) * (n - 1) / dof) if r2 is not None else None
    return {"n": n, "p": p, "r2": r2, "adj_r2": adj, "sigma": float(np.sqrt(sigma2)),
            "coefs": [{"name": nm, "beta": float(b), "se": float(s),
                       "lo": float(b - 1.96 * s), "hi": float(b + 1.96 * s),
                       "crosses_zero": bool((b - 1.96 * s) <= 0 <= (b + 1.96 * s))}
                      for nm, b, s in zip(names, beta, se)]}


def fit_report(feats: List[Dict], mean_wobble: Dict[str, float],
               cols: Sequence[str]) -> Dict[str, Any]:
    x, names, keep = design_matrix(feats, cols)
    if x.size == 0:
        return {"error": "no complete rows", "n_dropped": len(feats)}
    y = np.array([mean_wobble[feats[i]["leaf"]] for i in keep], float)
    return dict(ols(x, y, names), n_dropped=len(feats) - len(keep), columns=list(cols))


def nested_comparison(feats: List[Dict], mean_wobble: Dict[str, float],
                      base: Sequence[str], added: Sequence[str]) -> Dict[str, Any]:
    """Does `added` explain anything once `base` is in the model? This is the mechanism question
    -- 'does category still matter once answer type is accounted for' -- and it is answered by the
    change in adjusted R^2, which (unlike R^2) can go DOWN when a block adds only noise."""
    a = fit_report(feats, mean_wobble, base)
    b = fit_report(feats, mean_wobble, list(base) + list(added))
    if "error" in a or "error" in b:
        return {"error": a.get("error") or b.get("error")}
    return {"base_cols": list(base), "added_cols": list(added),
            "r2_base": a["r2"], "r2_full": b["r2"],
            "adj_base": a["adj_r2"], "adj_full": b["adj_r2"],
            "delta_adj": b["adj_r2"] - a["adj_r2"],
            "verdict": ("the added block explains nothing once the base is in the model"
                        if b["adj_r2"] <= a["adj_r2"] else
                        "the added block still explains variance beyond the base")}


def category_dummies(feats: List[Dict]) -> List[str]:
    """One 0/1 column per family, minus one held out as the reference level."""
    fams = sorted({f["family"] for f in feats})[1:]
    for f in feats:
        for fam in fams:
            f[f"fam_{fam}"] = 1.0 if f["family"] == fam else 0.0
    return [f"fam_{fam}" for fam in fams]
