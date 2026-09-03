"""
Location: paper-a/analysis/transfer.py
Purpose: STEP 2. Turn the rank correlation into a number a deployment engineer can act on: if I
         know model A's k most unstable clauses, how many of them land in model B's 2k most
         unstable? Directional (the relation is not symmetric), truncated rather than zero-padded,
         and always reported against the chance line for the k that was ACTUALLY used.
Functions: top_k_nonzero(), directed_transfer(), transfer_rows(), summarise_transfer()
Calls: concentration.top_k (reused ranking), stats_core (summaries)
Imports: statistics, typing, concentration, stats_core
"""

import statistics
from typing import Any, Dict, List, Optional, Sequence

import concentration
import stats_core as sc


def top_k_nonzero(vec: Dict[str, float], k: int) -> List[str]:
    """The model's k most unstable leaves, TRUNCATED to its non-zero entries. A model with 7
    non-zero leaves has no meaningful 'top 10'; padding the rest with zeros would rank arbitrary
    stable leaves and manufacture overlap with whatever the other model happened to rank there."""
    ranked = concentration.top_k(vec, k)
    return [n for n in ranked if (vec.get(n) or 0) > 0][:k]


def directed_transfer(vec_a: Dict[str, float], vec_b: Dict[str, float], k: int,
                      n_leaves: int) -> Optional[Dict[str, Any]]:
    """A -> B: what share of A's top-k unstable leaves fall inside B's top-2k?

    The chance line is computed from the EFFECTIVE k after truncation on both sides, not from the
    nominal k -- truncation changes the size of B's target set, and a fixed 2k/N baseline would
    silently overstate how far the result sits above chance."""
    a = top_k_nonzero(vec_a, k)
    b = set(top_k_nonzero(vec_b, 2 * k))
    if not a or not b:
        return None
    hit = sum(1 for n in a if n in b)
    return {"k_requested": k, "k_effective_a": len(a), "k_effective_b": len(b),
            "truncated_a": len(a) < k, "truncated_b": len(b) < 2 * k,
            "hits": hit, "rate": hit / len(a), "chance": len(b) / n_leaves,
            "lift": hit / len(a) - len(b) / n_leaves}


def transfer_rows(models: Sequence[str], leaf_names: Sequence[str], cells,
                  ks: Sequence[int]) -> List[Dict[str, Any]]:
    """Every ORDERED pair at every k. Ordered, not unordered: A->B and B->A genuinely differ when
    the two models have different numbers of non-zero leaves, and averaging them away would hide
    the asymmetry that matters to someone choosing which model to profile first."""
    vecs = {m: {n: (cells[m][n]["wobble"] or 0.0) for n in leaf_names} for m in models}
    rows = []
    for k in ks:
        for a in models:
            for b in models:
                if a == b:
                    continue
                r = directed_transfer(vecs[a], vecs[b], k, len(leaf_names))
                if r is None:
                    rows.append({"k": k, "from": a, "to": b, "rate": None,
                                 "reason": "a model has no non-zero leaves at this k"})
                    continue
                rows.append(dict(r, k=k, **{"from": a, "to": b}))
    return rows


def summarise_transfer(rows: List[Dict[str, Any]], k: int,
                       members: Optional[Sequence[str]] = None) -> Dict[str, Any]:
    """Median, IQR and the chance line over a set of directed pairs. `members` restricts to a model
    subset (the frontier-only headline). n is carried on every summary because a median over 6
    pairs and a median over 132 are not the same claim."""
    sel = [r for r in rows if r["k"] == k
           and (members is None or (r["from"] in members and r["to"] in members))]
    ok = [r for r in sel if r.get("rate") is not None]
    out = dict(sc.summarise(sel, key="rate"), k=k)          # median/IQR/undefined, one place only
    if not ok:
        return dict(out, chance=None, median_lift=None, n_truncated=0, n_models=0)
    return dict(out,
                chance=statistics.median([r["chance"] for r in ok]),
                median_lift=statistics.median([r["lift"] for r in ok]),
                n_truncated=sum(1 for r in ok if r["truncated_a"] or r["truncated_b"]),
                # The effective k is reported because at this arm most models have FEWER than k
                # non-zero leaves: a "top 10" that is really a top 7 is a different claim, and a
                # summary that hides it lets the nominal k stand in for a number never achieved.
                k_eff_a=statistics.median([r["k_effective_a"] for r in ok]),
                k_eff_b=statistics.median([r["k_effective_b"] for r in ok]),
                n_models=len({r["from"] for r in ok} | {r["to"] for r in ok}))
