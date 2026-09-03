"""
Location: paper-a/analysis/robustness.py
Purpose: STEP 4. The four checks a reviewer asks for after the headline: is wobble just difficulty
         (4a), how precise is the estimate (4b bootstrap), does one model carry it (4c
         leave-one-out), and does the item-weighting choice decide the reading (4d).
Functions: leaf_means(), wobble_vs_accuracy(), nightmare_leaves(), bootstrap_median(),
           leave_one_out(), weighting_sensitivity()
Calls: none (pure over the cells + published scored blocks)
Imports: statistics, typing, numpy, stats_core
"""

import statistics
from typing import Any, Dict, List, Optional, Sequence

import numpy as np

import stats_core as sc

HIGH_ACC = 0.90        # "models usually get it right"
HIGH_WOBBLE = 0.30     # "...and still flip run to run"


def leaf_means(models: Sequence[str], names: Sequence[str], cells,
               accuracy: Dict[str, Dict[str, Optional[float]]]) -> List[Dict[str, Any]]:
    """Per leaf: mean wobble and mean majority-accuracy ACROSS models, over the models where each
    is defined. Counted separately per quantity, because a cell can have a wobble and no accuracy."""
    out = []
    for n in names:
        w = [cells[m][n]["wobble"] for m in models if cells[m][n]["wobble"] is not None]
        a = [accuracy[m][n] for m in models if accuracy[m].get(n) is not None]
        out.append({"leaf": n, "mean_wobble": (sum(w) / len(w)) if w else None,
                    "n_models_wobble": len(w),
                    "mean_accuracy": (sum(a) / len(a)) if a else None,
                    "n_models_accuracy": len(a)})
    return out


def wobble_vs_accuracy(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """The reviewer's objection in one coefficient: are we just measuring item difficulty?

    Reported with the shared-denominator caveat attached, because wobble and accuracy are computed
    from the SAME runs: a leaf where every run fails to parse contributes to both. The coefficient
    is evidence, not proof, and the nightmare-leaf count below is the mechanism-free companion."""
    pairs = [(r["mean_wobble"], r["mean_accuracy"]) for r in rows
             if r["mean_wobble"] is not None and r["mean_accuracy"] is not None]
    if len(pairs) < 3:
        return {"n": len(pairs), "rho": None, "reason": "fewer than 3 leaves with both defined"}
    st = sc.pair_stats([p[0] for p in pairs], [p[1] for p in pairs])
    return {"n": len(pairs), "rho": st["rho"], "tau": st["tau"], "reason": st.get("reason") or ""}


def nightmare_leaves(rows: List[Dict[str, Any]], high_acc: float = HIGH_ACC,
                     high_wobble: float = HIGH_WOBBLE) -> Dict[str, Any]:
    """Leaves models usually get RIGHT and still flip on. These are the deployment cases the paper
    is actually about, and they are countable without any correlation at all."""
    hits = [r for r in rows if (r["mean_accuracy"] or 0) >= high_acc
            and (r["mean_wobble"] or 0) >= high_wobble]
    return {"threshold_accuracy": high_acc, "threshold_wobble": high_wobble,
            "n": len(hits), "leaves": [r["leaf"] for r in
                                       sorted(hits, key=lambda r: -r["mean_wobble"])]}


def bootstrap_median(models: Sequence[str], names: Sequence[str], cells, n_boot: int,
                     seed: int) -> Dict[str, Any]:
    """Percentile bootstrap over LEAVES for the median pairwise rho. The permutation null says
    'not zero'; this says 'how precise'. Resampling leaves changes the tie structure in each
    replicate, so some pairs go undefined -- those are counted, and the worst case is reported,
    rather than silently shrinking the interval."""
    rng = np.random.default_rng(seed)
    vec = {m: [cells[m][n]["wobble"] for n in names] for m in models}
    meds, undef = [], []
    for _ in range(n_boot):
        idx = rng.integers(0, len(names), len(names))
        res = {m: [vec[m][i] for i in idx] for m in models}
        rows = sc.all_pairs(list(models), res)
        vals = [r["rho"] for r in rows if r["rho"] is not None]
        undef.append(len(rows) - len(vals))
        if vals:
            meds.append(float(np.median(vals)))
    arr = np.array(meds) if meds else np.array([np.nan])
    return {"n_boot": len(meds), "median": float(np.median(arr)),
            "lo": float(np.percentile(arr, 2.5)), "hi": float(np.percentile(arr, 97.5)),
            "max_undefined_pairs_in_a_replicate": int(max(undef)) if undef else 0,
            "n_leaves_resampled": len(names)}


def leave_one_out(models: Sequence[str], names: Sequence[str], cells) -> List[Dict[str, Any]]:
    """Drop each model, recompute the headline median. Twelve numbers that show whether one model
    carries the result -- and if either 1B model moves it materially, that belongs in the paper."""
    out = []
    for drop in models:
        keep = [m for m in models if m != drop]
        vec = {m: [cells[m][n]["wobble"] for n in names] for m in keep}
        s = sc.summarise(sc.all_pairs(keep, vec))
        out.append({"dropped": drop, "n_models": len(keep), "n_pairs": s["n_pairs"],
                    "n_defined": s["n_defined"], "median": s["median"], "iqr": s["iqr"]})
    return out


def weighting_sensitivity(models: Sequence[str], names: Sequence[str],
                          cells) -> List[Dict[str, Any]]:
    """Aggregate wobble two ways: item-weighted (sum flips / sum items, what the benchmark reports)
    and leaf-equal (mean of per-leaf rates). If the capability ORDER changes between them, the
    stage-1 tier split rests on the weighting choice and that must be said."""
    out = []
    for m in models:
        flipped = sum(cells[m][n]["flipped"] for n in names)
        items = sum(cells[m][n]["n_items"] for n in names)
        rates = [cells[m][n]["wobble"] for n in names if cells[m][n]["wobble"] is not None]
        out.append({"model": m, "item_weighted": (flipped / items) if items else None,
                    "leaf_equal": statistics.mean(rates) if rates else None,
                    "n_leaves": len(rates), "n_items": items})
    return out


def rank_agreement(rows: List[Dict[str, Any]], a: str, b: str) -> Optional[float]:
    """Spearman between two orderings of the models -- used to say whether the weighting choice
    reorders capability, rather than eyeballing two columns."""
    st = sc.pair_stats([r[a] for r in rows], [r[b] for r in rows])
    return st["rho"]
