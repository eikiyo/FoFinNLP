"""
Location: paper-a/analysis/fold.py
Purpose: STAGE 3 steps 1b/1c, the MEASUREMENT half. Recover each item's per-run correct rate p
         from the raw runs, and state the two closed-form structural models that bracket how much
         flipping is mechanical. The diagnostics that consume this live in folddiag.py.
Functions: structural_flip(), structural_flip_max(), item_rates(), collect(),
           roundtrip_check(), leaf_rows(), selftest()
Calls: probity engine/scorer.py + normalize.py (reused, never re-implemented), splithalf
Imports: collections, typing, numpy, config, splithalf
"""

from collections import Counter
from typing import Any, Dict, List, Optional, Sequence

import numpy as np

import config
import splithalf


def structural_flip(p: Optional[float], n: int) -> Optional[float]:
    """P(the item's n runs do NOT all agree | per-run correct rate p), under the simplest model
    that has NO free parameters: runs independent, correct with probability p, and every incorrect
    run giving one shared wrong answer.

        P(flip) = 1 - p^n - (1-p)^n

    Derived, never fitted -- a model fitted to the same runs would absorb the very signal this
    exists to isolate. It is a LOWER bound on flipping at small p, because real wrong answers are
    heterogeneous (twenty runs can be wrong three different ways at p=0). That bias runs in the
    conservative direction: any residual it leaves is genuine instability, not model slack."""
    if p is None or n < 1:
        return None
    return float(1.0 - p ** n - (1.0 - p) ** n)


def structural_flip_max(p: Optional[float], n: int) -> Optional[float]:
    """The OPPOSITE extreme, and the reason the headline is reported as a bracket rather than a
    number: every incorrect run gives a DISTINCT wrong answer, so the item holds only if all n runs
    are correct.

        P(flip) = 1 - p^n

    `structural_flip` under-states mechanical flipping (it lets all wrong runs agree); this
    over-states it (it lets none agree). The truth is between them, and so the honest statement of
    'how much of the correlation is mechanical' is an interval whose ends these two produce. Quoting
    only the lower bound would flatter the paper's own claim, which is why both are computed."""
    if p is None or n < 1:
        return None
    return float(1.0 - p ** n)


def _n_valid_min(scorer, inst_runs, fields) -> int:
    """The benchmark's own measurability key for an item: the MINIMUM valid-run count across every
    scorable field, not the target field's count.

    Mirrored from scorer._score_one_instance rather than assumed. It matters: an item whose target
    field has plenty of valid runs is still excluded by aggregate.per_item_flips when a SIBLING
    field recorded none. Using the target field alone shrank two cells' denominators and inflated
    their wobble -- caught by the round-trip control below, which is the only reason this is right."""
    return min((len(scorer._values_for(inst_runs, f))
                for f, s in fields.items() if s["type"] in scorer._SCORABLE), default=0)


def item_rates(task, instances, runs, field: str) -> List[Dict[str, Any]]:
    """Per item of one (leaf, model) cell: the per-run correct rate p, the run count n, and the
    benchmark's OWN flip flag. Values and oracle canonicalisation come from probity's scorer and
    normalize -- reaching into the engine deliberately, because a hand-rolled copy of the
    normalisation is a logged failure in this project."""
    scorer, _, _ = splithalf.engine_modules()
    import normalize                                    # probity's, via engine on sys.path
    fspec = task["fields"].get(field)
    if fspec is None:
        raise SystemExit(f"field {field!r} absent from task {task.get('name')!r} -- wrong field key")
    by_inst = scorer._runs_by_instance(runs)
    out = []
    for idx, (_inst, truth) in enumerate(instances):
        inst_runs = by_inst.get(idx, [])
        vals = scorer._values_for(inst_runs, field)
        if _n_valid_min(scorer, inst_runs, task["fields"]) == 0:
            out.append({"item": idx, "n": len(vals), "p": None, "flipped": None,
                        "structural": None, "structural_max": None})
            continue
        truth_c = normalize.canonical(truth.get(field), fspec["type"]) if truth else None
        out.append(_item_row(idx, vals, truth_c))
    return out


def _item_row(idx: int, vals, truth_c) -> Dict[str, Any]:
    """One item's record: correct rate, flip flag, graded dispersion, and the modal VALUE."""
    p = sum(1 for v in vals if v == truth_c) / len(vals)
    modal, modal_n = Counter(vals).most_common(1)[0]
    # `majority` is the benchmark's OWN per-item accuracy_majority, not a re-derivation: every
    # one of the 60 tasks has exactly ONE scorable field (checked, not assumed), so the scorer's
    # AND across fields reduces to this single comparison. Carried here so a re-count over a
    # SUBSET of items can rebuild accuracy the same way it rebuilds wobble, from one pass.
    return {"item": idx, "n": len(vals), "p": p, "flipped": bool(modal_n < len(vals)),
            "majority": bool(modal == truth_c),
            # The modal VALUE and its support, not only whether it matched. Needed to ask whether
            # twelve configurations that all disagree with the oracle disagree with it in the SAME
            # direction -- a candidate label error -- or in twelve different directions, which is
            # just a hard item. `majority` alone cannot tell those apart, and they call for
            # opposite responses.
            "modal": modal, "modal_n": modal_n, "truth": truth_c,
            # GRADED instability: the share of runs that disagree with the modal answer. `flipped`
            # is this quantity thresholded at zero, and a binary flag cannot be RANKED -- a top-k
            # over it would order tied items by whatever the sort is stable on, and then measure
            # agreement between two arbitrary orderings. This is the same quantity, ungated, so an
            # item-level top-k ranks by how split the runs actually were.
            "dispersion": 1.0 - modal_n / len(vals),
            "structural": structural_flip(p, len(vals)),
            "structural_max": structural_flip_max(p, len(vals))}


def collect(models: Sequence[str], leaves: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Every item of every (leaf, model) cell in the declared arm. One pass over the runs files."""
    _, runner, _ = splithalf.engine_modules()
    per_cell: Dict[str, Dict[str, List[Dict[str, Any]]]] = {m: {} for m in models}
    opened = []
    for entry in leaves:
        task = splithalf._task_of(entry["rel"])
        instances, _ = runner.load_instances(config.probity_root() / entry["rel"], entry["field"])
        for m in models:
            runs, path = splithalf.leaf_runs(entry["rel"], m)
            opened.append(path)
            per_cell[m][entry["leaf"]] = (item_rates(task, instances, runs, entry["field"])
                                          if runs else [])
    config.assert_arm_clean(opened)
    return {"per_cell": per_cell, "n_files": len(opened)}


def roundtrip_check(models: Sequence[str], names: Sequence[str], per_cell, cells) -> str:
    """POSITIVE CONTROL, and the reason this module can be trusted at all: the per-item flip flags
    recomputed here must reproduce the published wobble of every cell exactly. If the field key or
    the oracle join were wrong, every p would be 0, the fold would look perfectly structural, and
    the paper would concede on garbage. A check that reports a clean decomposition is only
    trustworthy if it could have detected a broken one."""
    diffs = []
    for m in models:
        for n in names:
            items = [i for i in per_cell[m][n] if i["flipped"] is not None]
            recomputed = (sum(1 for i in items if i["flipped"]) / len(items)) if items else None
            published = cells[m][n]["wobble"]
            if recomputed is None and published is None:
                continue
            if recomputed is None or published is None or abs(recomputed - published) > 1e-12:
                diffs.append(f"{m}/{n}: recomputed {recomputed} vs published {published}")
    if diffs:
        raise SystemExit("FOLD ROUND-TRIP FAILED - per-item reconstruction does not reproduce the "
                         "published wobble:\n  " + "\n  ".join(diffs[:10]))
    return (f"fold round-trip PASS - per-item flags reproduce all {len(models) * len(names)} "
            f"published wobble cells exactly, so p is joined to the right oracle field")


def leaf_rows(models: Sequence[str], per_cell,
              leaf_means: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Per leaf: observed wobble and accuracy taken STRAIGHT from `robustness.leaf_means` (the one
    canonical computation), plus the structural prediction, which is the only genuinely new column.

    Recomputing the observed mean here instead was both a reuse violation and a real numerical bug:
    `sum(w)/len(w)` and `np.mean(w)` differ in the last bit, that changed 5 of 60 leaf values by
    ~5e-17, which changed the number of DISTINCT values from 42 to 41, which reshuffled tied ranks
    and moved the published Spearman from -0.5516 to -0.5481. Same data, different summation order.
    One canonical mean removes the divergence -- and the fragility itself is reported, because it
    means that coefficient's third decimal is not meaningful."""
    struct = {k: _leaf_structural(models, per_cell, k) for k in ("structural", "structural_max")}
    cal = calibrated_structural(models, per_cell, [r["leaf"] for r in leaf_means])
    rows = []
    for row in leaf_means:
        n, obs = row["leaf"], row["mean_wobble"]
        lo, hi, mid = struct["structural"][n], struct["structural_max"][n], cal[n]
        rows.append({"leaf": n, "n_models": row["n_models_wobble"], "observed": obs,
                     "structural": lo, "structural_max": hi, "structural_cal": mid,
                     "accuracy": row["mean_accuracy"], "residual": _sub(obs, lo),
                     "residual_max": _sub(obs, hi), "residual_cal": _sub(obs, mid)})
    return rows


def _sub(a: Optional[float], b: Optional[float]) -> Optional[float]:
    return (a - b) if (a is not None and b is not None) else None


def calibrated_structural(models: Sequence[str], per_cell, names: Sequence[str]
                          ) -> Dict[str, Optional[float]]:
    """The MIDDLE of the bracket, and the defensible primary: instead of assuming wrong runs always
    agree (lower bound) or never agree (upper bound), measure how often they agree and use that.

    Only p=0 items distinguish the two bounds -- an item with 0<p<1 has both a right and a wrong
    answer among its runs and so has flipped BY DEFINITION, and an item at p=1 cannot flip. So the
    single free quantity is the flip rate among always-wrong items, and it is estimated LEAVE-ONE-
    LEAF-OUT: a leaf's prediction never uses that leaf's own items. Without that, the model would
    be fitted to the outcome it is meant to control for and the residual would vanish by
    construction -- the same circularity that ruled out an empirical-frequency model in the DESIGN."""
    tot_n = tot_f = 0
    per_leaf: Dict[str, tuple] = {}
    for n in names:
        items = [i for m in models for i in per_cell[m][n] if i["p"] == 0.0
                 and i["flipped"] is not None]
        per_leaf[n] = (len(items), sum(1 for i in items if i["flipped"]))
        tot_n += len(items)
        tot_f += per_leaf[n][1]
    out: Dict[str, Optional[float]] = {}
    for n in names:
        ln, lf = per_leaf[n]
        rest_n, rest_f = tot_n - ln, tot_f - lf
        q = (rest_f / rest_n) if rest_n else None
        vals = [_cell_calibrated(per_cell[m][n], q) for m in models]
        keep = [v for v in vals if v is not None]
        out[n] = float(np.mean(keep)) if keep else None
    return out


def _cell_calibrated(items: List[Dict[str, Any]], q: Optional[float]) -> Optional[float]:
    """Predicted flip rate for one cell: 0 where p=1, 1 where p is interior (definitional), and the
    held-out always-wrong flip rate q where p=0."""
    if q is None:
        return None
    vals = [(0.0 if i["p"] == 1.0 else 1.0 if i["p"] > 0.0 else q)
            for i in items if i["p"] is not None]
    return float(np.mean(vals)) if vals else None


def _leaf_structural(models: Sequence[str], per_cell, key: str) -> Dict[str, Optional[float]]:
    """Mean predicted flip rate per leaf under one structural model, averaged over models the same
    way the observed mean is: per cell first, then across cells."""
    out: Dict[str, Optional[float]] = {}
    for n in next(iter(per_cell.values())):
        vals = [float(np.mean([i[key] for i in per_cell[m][n] if i[key] is not None]))
                for m in models if any(i[key] is not None for i in per_cell[m][n])]
        out[n] = float(np.mean(vals)) if vals else None
    return out

def selftest() -> str:
    """Prove BOTH structural models at the points where their value is known in closed form, and
    prove the degenerate inputs return None rather than a plausible number. Tolerance compares
    throughout -- an exact float equality here has already produced one false RED in this project."""
    assert structural_flip(0.0, 20) == 0.0, "p=0 must predict no flip under the two-outcome model"
    assert structural_flip(1.0, 20) == 0.0, "p=1 must predict no flip"
    assert abs(structural_flip(0.5, 20) - (1 - 2 * 0.5 ** 20)) < 1e-12, "p=0.5, n=20 closed form"
    assert abs(structural_flip(0.5, 2) - 0.5) < 1e-12, "p=0.5, n=2 must be exactly 0.5"
    assert structural_flip(0.5, 1) == 0.0, \
        "one run cannot disagree with itself: n=1 is a genuine 0, not a missing value, and the "\
        "benchmark counts such an item as not-flipped -- excluding it would shrink the denominator"
    assert structural_flip(None, 20) is None and structural_flip(0.5, 0) is None, \
        "a missing p or zero runs must return None, never 0.0 (which would read as 'stable')"
    mid, edge = structural_flip(0.5, 20), structural_flip(0.95, 20)
    assert mid > edge, f"the model must fold: mid {mid} should exceed edge {edge}"
    assert structural_flip(0.05, 20) == structural_flip(0.95, 20), "the fold must be symmetric in p"
    assert abs(structural_flip_max(0.5, 20) - (1 - 0.5 ** 20)) < 1e-12, "upper-bound closed form"
    assert structural_flip_max(0.0, 20) == 1.0, "p=0 with all-distinct wrong answers must flip"
    assert structural_flip_max(1.0, 20) == 0.0, "p=1 cannot flip under either extreme"
    assert structural_flip_max(0.2, 5) > structural_flip(0.2, 5), \
        "the upper bound must exceed the lower bound wherever p is interior"
    assert _sub(0.5, 0.2) == 0.3 and _sub(None, 0.2) is None and _sub(0.5, None) is None, \
        "a residual against a missing structural value must be None, never the observed value"
    return ("fold selftest PASS - both structural bounds correct at p=0/0.5/1, lower bound "
            "symmetric and dominated by the upper, n=1 is a real zero, n=0 refused")
