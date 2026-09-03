"""
Location: paper-a/analysis/categories.py
Purpose: STEP 3, the descriptive layer. Model x category wobble with WILSON score intervals (not
         the normal approximation -- most cells here sit near zero, where the normal interval is
         simply wrong), the worst-category-to-mean ratio that carries the paper's deployment
         recommendation, and an explicit map of which cell pairs are statistically
         indistinguishable so prose can never order them.
Functions: wilson(), category_cells(), model_ratios(), indistinguishable_pairs(), selftest()
Calls: none (pure over the cells built by matrix.py)
Imports: math, typing
"""

import math
from typing import Any, Dict, List, Optional, Sequence, Tuple

MIN_LEAVES = 3          # below this a category is reported with n but marked not estimable
Z = 1.959963984540054   # 95%


def wilson(k: int, n: int, z: float = Z) -> Optional[Tuple[float, float]]:
    """Wilson score interval for a binomial proportion. Chosen over the normal approximation
    because it stays inside [0, 1] and remains correct at k = 0, which is where most of this
    matrix lives -- a normal interval on 0/300 returns [0, 0] and would assert certainty."""
    if n <= 0:
        return None
    p, z2 = k / n, z * z
    denom = 1 + z2 / n
    centre = (p + z2 / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n))) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def category_cells(models: Sequence[str], leaves: List[Dict[str, Any]],
                   cells) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """Per (model, category): flipped and measured ITEM counts summed over that category's leaves,
    with the Wilson interval on the resulting rate. Counts are summed, never rates averaged --
    averaging per-leaf rates would weight a 3-item leaf like a 30-item one."""
    by_cat: Dict[str, List[Dict[str, Any]]] = {}
    for l in leaves:
        by_cat.setdefault(l["family"], []).append(l)
    out: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for m in models:
        out[m] = {}
        for cat, ls in by_cat.items():
            flipped = sum(cells[m][l["leaf"]]["flipped"] for l in ls)
            measured = sum(cells[m][l["leaf"]]["n_items"] for l in ls)
            # Tasks that CONTRIBUTED items, not tasks the registry assigns to the category. On the
            # full corpus these are the same number and nothing moves. Under an item exclusion they
            # are not: the provenance audit empties 6 of cap_table's 7 tasks, and counting the
            # registry's 7 would let a one-task category clear the three-task estimability floor
            # and become the "worst category" the paper's recommendation rests on. Counting the
            # container instead of the leaf is a logged failure class in this project.
            n_leaves = sum(1 for l in ls if cells[m][l["leaf"]]["n_items"] > 0)
            ci = wilson(flipped, measured)
            out[m][cat] = {"flipped": flipped, "measured": measured, "n_leaves": n_leaves,
                           "n_leaves_registered": len(ls),
                           "rate": (flipped / measured) if measured else None,
                           "lo": ci[0] if ci else None, "hi": ci[1] if ci else None,
                           "estimable": n_leaves >= MIN_LEAVES and measured > 0}
    return out


def model_ratios(models: Sequence[str], cat_cells, agg_wobble: Dict[str, float]
                 ) -> List[Dict[str, Any]]:
    """Per model: mean wobble, WORST-category wobble, and their ratio -- the direct evidence for a
    recommendation of the form 'a model's headline number understates its worst clause type by
    Nx'. Only estimable categories can be the worst; a 1-leaf category must never be the peak that
    the recommendation rests on."""
    rows = []
    for m in models:
        est = {c: v for c, v in cat_cells[m].items() if v["estimable"] and v["rate"] is not None}
        if not est:
            rows.append({"model": m, "mean": agg_wobble[m], "worst_cat": None, "worst": None,
                         "ratio": None, "n_estimable": 0})
            continue
        worst_cat = max(est, key=lambda c: est[c]["rate"])
        worst = est[worst_cat]["rate"]
        rows.append({"model": m, "mean": agg_wobble[m], "worst_cat": worst_cat, "worst": worst,
                     "worst_lo": est[worst_cat]["lo"], "worst_hi": est[worst_cat]["hi"],
                     "ratio": (worst / agg_wobble[m]) if agg_wobble[m] else None,
                     "n_estimable": len(est)})
    return rows


def indistinguishable_pairs(cat_cells, model: str) -> List[Tuple[str, str]]:
    """Every pair of that model's category cells whose Wilson intervals OVERLAP. These may not be
    ordered in prose: 'category X is worse than Y' is a claim the data does not support when the
    intervals cross, and near-zero cells with wide intervals cross constantly."""
    est = [(c, v) for c, v in cat_cells[model].items() if v["estimable"] and v["lo"] is not None]
    out = []
    for i in range(len(est)):
        for j in range(i + 1, len(est)):
            (ca, a), (cb, b) = est[i], est[j]
            if a["lo"] <= b["hi"] and b["lo"] <= a["hi"]:
                out.append((ca, cb))
    return out


def selftest() -> str:
    """Wilson against published reference values, and against the two degenerate cases that the
    normal approximation gets wrong. A helper that has only ever been run on convenient input has
    not been shown to be correct."""
    lo, hi = wilson(0, 100)                       # exact-zero comparisons would false-red on the
    assert lo < 1e-12 and 0.03 < hi < 0.04, f"wilson(0,100) wrong: {lo},{hi}"   # IEEE-754 residue
    lo, hi = wilson(100, 100)
    assert hi > 1 - 1e-12 and 0.96 < lo < 0.97, f"wilson(100,100) wrong: {lo},{hi}"
    lo, hi = wilson(50, 100)                      # symmetric case, textbook 0.404-0.596
    assert abs(lo - 0.4038) < 0.001 and abs(hi - 0.5962) < 0.001, f"wilson(50,100) wrong: {lo},{hi}"
    assert wilson(0, 0) is None, "wilson must refuse n=0 rather than divide"
    lo1, hi1 = wilson(5, 20)
    lo2, hi2 = wilson(50, 200)                    # same rate, 10x n -> strictly tighter
    assert (hi2 - lo2) < (hi1 - lo1), "wilson interval must narrow as n grows"
    # The estimability floor must count CONTRIBUTING tasks. Proven against the shape the provenance
    # exclusion actually produces: a category the registry lists 4 tasks for, 3 of which were
    # emptied. Counting the registry's 4 would clear the floor on the strength of one task.
    ls = [{"leaf": f"L{i}", "family": "F"} for i in range(4)]
    emptied = {"m": {"L0": {"flipped": 2, "n_items": 5}, "L1": {"flipped": 0, "n_items": 0},
                     "L2": {"flipped": 0, "n_items": 0}, "L3": {"flipped": 0, "n_items": 0}}}
    cc = category_cells(["m"], ls, emptied)["m"]["F"]
    assert cc["n_leaves"] == 1 and not cc["estimable"], \
        f"a category reduced to one contributing task must NOT be estimable: {cc}"
    assert cc["n_leaves_registered"] == 4, "the registry count must still be reported, not lost"
    full = {"m": {f"L{i}": {"flipped": 1, "n_items": 5} for i in range(4)}}
    cf = category_cells(["m"], ls, full)["m"]["F"]
    assert cf["n_leaves"] == 4 and cf["estimable"], \
        f"with every task contributing, the count must be unchanged from the registry: {cf}"
    return ("categories selftest PASS - Wilson correct at 0/n, n/n, symmetric, n=0 refused; the "
            "estimability floor counts contributing tasks and refuses an emptied category")
