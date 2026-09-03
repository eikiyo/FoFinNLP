"""
Location: paper-a/analysis/analyses.py
Purpose: The subsets and stratifications the brief's section-5 controls are defined over -- active
         subset, tie exclusion, empirical capability split, dropped-leaf accounting + common
         subset, serving-path split, answer-type strata -- each returning plain dicts so the
         report is GENERATED from the same objects the tables are written from, never hand-typed.
Functions: vectors(), active_subset(), aggregate_wobble(), capability_split(), drop_accounting(),
           common_subset(), pair_partition(), strata_pairs(), tie_table()
Calls: stats_core
Imports: typing, numpy, stats_core, config
"""

from typing import Any, Dict, List, Optional, Tuple

import numpy as np

import config
import stats_core as sc


def vectors(models: List[str], leaf_names: List[str],
            cells: Dict[str, Dict[str, Dict[str, Any]]]) -> Dict[str, List[Optional[float]]]:
    return {m: [cells[m][n]["wobble"] for n in leaf_names] for m in models}


def active_subset(models: List[str], leaf_names: List[str], cells) -> List[str]:
    """Leaves with non-zero wobble in AT LEAST ONE model (brief 5a). A leaf every model got
    perfectly stable carries no ordering information for any pair and only inflates tie mass."""
    return [n for n in leaf_names
            if any((cells[m][n]["wobble"] or 0) > 0 for m in models)]


def aggregate_wobble(models: List[str], leaf_names: List[str], cells) -> Dict[str, float]:
    """Per model, pooled flipped/measured items across every leaf -- the benchmark's own headline
    wobble number, recomputed here from the same two matrices everything else derives from."""
    out = {}
    for m in models:
        f = sum(cells[m][n]["flipped"] for n in leaf_names if not cells[m][n]["dropped"])
        k = sum(cells[m][n]["n_items"] for n in leaf_names if not cells[m][n]["dropped"])
        out[m] = (f / k) if k else float("nan")
    return out


def capability_split(agg_wobble: Dict[str, float]) -> Dict[str, Any]:
    """
    Empirical split (brief 5b): sort models by aggregate 0.7 wobble and cut at the LARGEST gap
    between consecutive values. A largest-gap (natural-break) rule is used rather than a median or
    a round number so the threshold is a property of the data, not a choice that could be tuned
    after seeing the correlations.
    """
    order = sorted(agg_wobble.items(), key=lambda kv: kv[1])
    gaps = [(order[i + 1][1] - order[i][1], i) for i in range(len(order) - 1)]
    best_gap, idx = max(gaps)
    threshold = (order[idx][1] + order[idx + 1][1]) / 2
    return {"threshold": threshold, "largest_gap": best_gap,
            "frontier": [m for m, v in order if v < threshold],
            "low": [m for m, v in order if v >= threshold],
            "sorted": order}


def drop_accounting(models: List[str], leaves: List[Dict[str, Any]], cells) -> Dict[str, Any]:
    """Brief 5c. Reports per model and per family, and reports ABSENT separately from DROPPED --
    a cell never run and a cell excluded by the >30% rule are different facts."""
    per_model = {m: {"dropped": sum(1 for l in leaves if cells[m][l["leaf"]]["dropped"]
                                    and not cells[m][l["leaf"]]["absent"]),
                     "absent": sum(1 for l in leaves if cells[m][l["leaf"]]["absent"])}
                 for m in models}
    per_family: Dict[str, int] = {}
    for l in leaves:
        per_family.setdefault(l["family"], 0)
        per_family[l["family"]] += sum(1 for m in models if cells[m][l["leaf"]]["dropped"])
    total = sum(v["dropped"] + v["absent"] for v in per_model.values())
    return {"per_model": per_model, "per_family": per_family, "total_dropped_cells": total,
            "n_cells": len(models) * len(leaves)}


def common_subset(models: List[str], leaf_names: List[str], cells) -> List[str]:
    """Leaves retained (measurable and present) for ALL models."""
    return [n for n in leaf_names if all(not cells[m][n]["dropped"] for m in models)]


def tie_table(models: List[str], vecs_full, vecs_active) -> List[Dict[str, Any]]:
    rows = []
    for m in models:
        rows.append({
            "model": m,
            "tie_full": sc.tie_fraction(vecs_full[m]), "zero_full": sc.zero_fraction(vecs_full[m]),
            "tie_active": sc.tie_fraction(vecs_active[m]),
            "zero_active": sc.zero_fraction(vecs_active[m]),
            "n_distinct_full": len({v for v in vecs_full[m] if v is not None}),
        })
    for r in rows:
        r["excluded"] = r["tie_full"] is not None and r["tie_full"] > config.TIE_THRESHOLD
    return rows


def pair_partition(rows: List[Dict[str, Any]], group: Dict[str, str],
                   labels: Tuple[str, str]) -> Dict[str, List[Dict[str, Any]]]:
    """Split pair rows by whether both members share a group tag (brief 5b within/across, 5d
    shared-vs-different serving path)."""
    same, cross = [], []
    for r in rows:
        (same if group[r["model_a"]] == group[r["model_b"]] else cross).append(r)
        r["group_a"], r["group_b"] = group[r["model_a"]], group[r["model_b"]]
    return {labels[0]: same, labels[1]: cross}


def within_group_pairs(rows: List[Dict[str, Any]], group: Dict[str, str],
                       name: str) -> List[Dict[str, Any]]:
    return [r for r in rows if group[r["model_a"]] == name and group[r["model_b"]] == name]


def strata_pairs(models: List[str], leaf_names: List[str], cells,
                 answer_type: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
    """Brief 5f: rerun the pairwise distribution inside each answer-type stratum. A stratum with
    fewer than 4 leaves is reported but explicitly marked as too small to carry a distribution."""
    out: Dict[str, Dict[str, Any]] = {}
    for kind in sorted(set(answer_type[n] for n in leaf_names)):
        subset = [n for n in leaf_names if answer_type[n] == kind]
        vecs = vectors(models, subset, cells)
        rows = sc.all_pairs(models, vecs)
        ties = [sc.tie_fraction(vecs[m]) for m in models]
        zeros = [sc.zero_fraction(vecs[m]) for m in models]
        out[kind] = {"n_leaves": len(subset), "leaves": subset, "rows": rows,
                     "summary": sc.summarise(rows), "too_small": len(subset) < 4,
                     # Tie mass INSIDE the stratum. Without it a low stratum median cannot be
                     # told apart from a stratum the estimator simply cannot see (the exact trap
                     # the tie control exists for, one level down).
                     "mean_tie": float(np.mean([t for t in ties if t is not None])),
                     "mean_zero": float(np.mean([z for z in zeros if z is not None]))}
    return out


def serving_within_tier(ctx_rows: List[Dict[str, Any]], serving: Dict[str, str],
                        tier: Dict[str, str], keep_tier: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Isolate the serving-layer question from the capability question.

    Every routed and every direct model in this lineup is in the frontier tier and both local
    models are in the low tier, so the raw same-path/different-path split of 5d is CONFOUNDED with
    5b: "different path" is where all the low-vs-frontier pairs live. Restricting to one tier
    removes that, and is what actually answers "is the agreement an artefact of the infrastructure".
    """
    keep = [r for r in ctx_rows
            if tier[r["model_a"]] == keep_tier and tier[r["model_b"]] == keep_tier]
    same = [r for r in keep if serving[r["model_a"]] == serving[r["model_b"]]]
    diff = [r for r in keep if serving[r["model_a"]] != serving[r["model_b"]]]
    return {"same_path": same, "different_path": diff}


def complete_matrix(models: List[str], leaf_names: List[str], cells) -> np.ndarray:
    """The observed matrix as a dense array. Asserts completeness, because the fast permutation
    path is only valid when every pair shares the same n -- a silent hole would make the null and
    the observation two different tests."""
    rows = []
    for m in models:
        vals = [cells[m][n]["wobble"] for n in leaf_names]
        if any(v is None for v in vals):
            raise SystemExit(f"matrix incomplete for {m}: the fast permutation path requires a "
                             f"complete matrix; fall back to the pairwise path")
        rows.append(vals)
    return np.array(rows, float)
