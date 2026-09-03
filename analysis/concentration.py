"""
Location: paper-a/analysis/concentration.py
Purpose: Brief 4c -- the TIE-IMMUNE route to the same question. Does instability concentrate on a
         minority of leaves, and do different models concentrate on the SAME minority? Answered by
         set overlap of top-K leaves rather than by a rank coefficient, so a vector that is 85%
         zeros cannot degrade the answer the way it degrades Spearman.
Functions: top_k(), concentration_rows(), overlap(), pairwise_overlap(), leaf_hit_counts()
Calls: none (pure over the two matrices)
Imports: itertools, statistics, typing, config
"""

import itertools
import statistics
from typing import Any, Dict, List, Tuple

import config


def top_k(vec: Dict[str, float], k: int = config.TOP_K) -> List[str]:
    """The k highest-wobble leaves for one model. Ties are broken by leaf name so the ranking is
    deterministic and regenerable; how many of the k are actually NON-ZERO is reported alongside,
    because for a model with fewer than k unstable leaves the tail of this list is padding."""
    ordered = sorted(vec.items(), key=lambda kv: (-kv[1], kv[0]))
    return [name for name, _ in ordered[:k]]


def concentration_rows(models: List[str], leaf_names: List[str], cells,
                        k: int = config.TOP_K) -> List[Dict[str, Any]]:
    rows = []
    for m in models:
        vec = {n: (cells[m][n]["wobble"] or 0.0) for n in leaf_names
               if not cells[m][n]["dropped"]}
        total_rate = sum(vec.values())
        total_items = sum(cells[m][n]["flipped"] for n in vec)
        top = top_k(vec, k)
        rows.append({
            "model": m,
            "n_leaves": len(vec),
            "n_nonzero": sum(1 for v in vec.values() if v > 0),
            "top_k": top,
            "top_k_nonzero": sum(1 for n in top if vec[n] > 0),
            "share_of_rate_mass": (sum(vec[n] for n in top) / total_rate) if total_rate else None,
            "share_of_item_mass": (sum(cells[m][n]["flipped"] for n in top) / total_items)
                                  if total_items else None,
        })
    return rows


def overlap(rows: List[Dict[str, Any]], nonzero_only: bool = True) -> Dict[str, Any]:
    """Strict intersection of every model's top-K set, plus the honest caveat: when a model has
    fewer than K non-zero leaves, its padded entries are excluded so the intersection is not
    counting shared zeros as shared instability."""
    sets = []
    for r in rows:
        s = r["top_k"][: r["top_k_nonzero"]] if nonzero_only else r["top_k"]
        sets.append(set(s))
    inter = set.intersection(*sets) if sets else set()
    union = set.union(*sets) if sets else set()
    return {"intersection": sorted(inter), "intersection_size": len(inter),
            "union_size": len(union), "per_model_set_sizes": [len(s) for s in sets]}


def pairwise_overlap(rows: List[Dict[str, Any]], nonzero_only: bool = True) -> Dict[str, Any]:
    """Distribution of |A ∩ B| over the 66 model pairs' top-K sets, and the same as a Jaccard.
    A distribution, because a single 12-way intersection is one number and one number cannot show
    whether agreement is broad-but-imperfect or genuinely absent."""
    sets = {r["model"]: set(r["top_k"][: r["top_k_nonzero"]] if nonzero_only else r["top_k"])
            for r in rows}
    pairs = []
    for a, b in itertools.combinations(sorted(sets), 2):
        inter = sets[a] & sets[b]
        union = sets[a] | sets[b]
        pairs.append({"model_a": a, "model_b": b, "shared": len(inter),
                      "jaccard": (len(inter) / len(union)) if union else None,
                      "size_a": len(sets[a]), "size_b": len(sets[b])})
    shared = [p["shared"] for p in pairs]
    jac = [p["jaccard"] for p in pairs if p["jaccard"] is not None]
    return {"pairs": pairs,
            "median_shared": statistics.median(shared) if shared else None,
            "min_shared": min(shared) if shared else None,
            "max_shared": max(shared) if shared else None,
            "median_jaccard": statistics.median(jac) if jac else None}


def leaf_hit_counts(rows: List[Dict[str, Any]], nonzero_only: bool = True) -> List[Tuple[str, int]]:
    """How many models' top-K each leaf appears in. This is what a shared difficulty dimension
    would look like if it existed: a handful of leaves hit by nearly every model."""
    counts: Dict[str, int] = {}
    for r in rows:
        for n in (r["top_k"][: r["top_k_nonzero"]] if nonzero_only else r["top_k"]):
            counts[n] = counts.get(n, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def zero_leaf_counts(models: List[str], leaf_names: List[str], cells) -> Dict[str, Any]:
    zero_all = [n for n in leaf_names
                if all((cells[m][n]["wobble"] or 0) == 0 for m in models)]
    return {"zero_in_all_models": zero_all, "n_zero_in_all": len(zero_all),
            "n_nonzero_in_at_least_one": len(leaf_names) - len(zero_all),
            "n_leaves": len(leaf_names)}
