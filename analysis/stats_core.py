"""
Location: paper-a/analysis/stats_core.py
Purpose: The rank statistics Paper A's C2 diagnostic runs on: tie mass, pairwise Spearman/Kendall
         over a leaf subset, distribution summaries, and the permutation null that preserves each
         model's exact tie structure and missingness pattern.
Functions: tie_fraction(), zero_fraction(), pair_stats(), all_pairs(), summarise(),
           rank_rows(), rho_matrix_from_ranks(), permutation_null(), selftest()
Calls: scipy.stats (spearmanr, kendalltau, rankdata)
Imports: itertools, math, numpy, scipy.stats, typing
"""

import itertools
import math
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
from scipy import stats


def tie_fraction(values: Sequence[float]) -> Optional[float]:
    """Share of a vector's entries whose value occurs MORE THAN ONCE in that same vector.
    Reported rather than a distinct-count ratio because it answers the question that matters:
    what proportion of this model's leaf scores carry no ordering information against a sibling."""
    vals = [v for v in values if v is not None]
    if not vals:
        return None
    counts: Dict[float, int] = {}
    for v in vals:
        counts[v] = counts.get(v, 0) + 1
    return sum(1 for v in vals if counts[v] > 1) / len(vals)


def zero_fraction(values: Sequence[float]) -> Optional[float]:
    vals = [v for v in values if v is not None]
    return (sum(1 for v in vals if v == 0.0) / len(vals)) if vals else None


def pair_stats(x: Sequence[Optional[float]], y: Sequence[Optional[float]]) -> Dict[str, Any]:
    """Spearman rho and Kendall tau-b over the positions where BOTH models have a value.
    A constant vector makes rho undefined; that is reported as None and counted, never coerced
    to 0.0 -- silently averaging an undefined coefficient as zero would drag the median toward
    the null and manufacture the exact result this diagnostic is trying to test."""
    pairs = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]
    n = len(pairs)
    if n < 3:
        return {"n": n, "rho": None, "tau": None, "reason": "n<3"}
    a = np.array([p[0] for p in pairs], float)
    b = np.array([p[1] for p in pairs], float)
    if a.std() == 0 or b.std() == 0:
        return {"n": n, "rho": None, "tau": None, "reason": "constant vector"}
    rho = float(stats.spearmanr(a, b).statistic)
    tau = float(stats.kendalltau(a, b, variant="b").statistic)
    out = {"n": n, "rho": None if math.isnan(rho) else rho,
           "tau": None if math.isnan(tau) else tau, "reason": None}
    if out["rho"] is None:
        out["reason"] = "nan from scipy"
    return out


def all_pairs(models: List[str], vectors: Dict[str, List[Optional[float]]]) -> List[Dict[str, Any]]:
    """Every unordered model pair, with its coefficients and both sides' tie fractions."""
    rows = []
    for m1, m2 in itertools.combinations(models, 2):
        st = pair_stats(vectors[m1], vectors[m2])
        rows.append(dict(st, model_a=m1, model_b=m2,
                         tie_a=tie_fraction(vectors[m1]), tie_b=tie_fraction(vectors[m2])))
    return rows


def summarise(rows: List[Dict[str, Any]], key: str = "rho") -> Dict[str, Any]:
    """Median / IQR / min / max over the DEFINED coefficients, with the undefined ones counted
    so a shrinking denominator can never pass as a clean distribution."""
    vals = sorted(r[key] for r in rows if r.get(key) is not None)
    undefined = sum(1 for r in rows if r.get(key) is None)
    if not vals:
        return {"n_pairs": len(rows), "n_defined": 0, "n_undefined": undefined,
                "median": None, "q1": None, "q3": None, "iqr": None, "min": None, "max": None}
    arr = np.array(vals, float)
    q1, q3 = (float(np.percentile(arr, 25)), float(np.percentile(arr, 75)))
    return {"n_pairs": len(rows), "n_defined": len(vals), "n_undefined": undefined,
            "median": float(np.median(arr)), "q1": q1, "q3": q3, "iqr": q3 - q1,
            "min": float(arr.min()), "max": float(arr.max()), "values": vals}


def rank_rows(mat: np.ndarray) -> np.ndarray:
    """Average ranks per row. Average ranks are what makes Pearson-on-ranks equal Spearman under
    ties, which is the identity the fast permutation path relies on."""
    return np.vstack([stats.rankdata(row, method="average") for row in mat])


def rho_matrix_from_ranks(ranks: np.ndarray) -> np.ndarray:
    """All pairwise Spearman rho at once. Rows with zero rank variance yield nan, preserved."""
    centred = ranks - ranks.mean(axis=1, keepdims=True)
    sd = np.sqrt((centred ** 2).sum(axis=1))
    with np.errstate(invalid="ignore", divide="ignore"):
        return (centred @ centred.T) / np.outer(sd, sd)


def permutation_rhos(mat: np.ndarray, n_perm: int, seed: int) -> np.ndarray:
    """
    (n_perm x n_pairs) of pairwise rho expected under NO agreement, given this exact tie structure
    and this exact n. Each model's OBSERVED VALUES are permuted among its OWN positions, so the
    multiset of values -- and therefore the tie structure -- is preserved by construction; only the
    pairing between models is destroyed. Returning every pair (not just the median) lets any
    pair-subset -- a capability tier, a serving-path split, the tie-filtered headline -- be scored
    against a null built the same way, instead of against a null for a different set of models.
    """
    rng = np.random.default_rng(seed)
    n_models, n_leaves = mat.shape
    iu = np.triu_indices(n_models, k=1)
    out = np.empty((n_perm, iu[0].size))
    for i in range(n_perm):
        perm = np.vstack([mat[r][rng.permutation(n_leaves)] for r in range(n_models)])
        out[i] = rho_matrix_from_ranks(rank_rows(perm))[iu]
    return out


def pair_index(models: List[str]) -> Dict[Tuple[str, str], int]:
    """Column index of each unordered pair in `permutation_rhos`, in the same order as
    np.triu_indices -- the ONE definition, so an observed pair and its null column cannot drift."""
    iu = np.triu_indices(len(models), k=1)
    return {(models[i], models[j]): c for c, (i, j) in enumerate(zip(*iu))}


def null_summary(rhos: np.ndarray, cols: Optional[Sequence[int]] = None) -> Dict[str, Any]:
    """The null distribution OF THE MEDIAN over a chosen set of pair columns."""
    sub = rhos if cols is None else rhos[:, list(cols)]
    if sub.size == 0:
        return {"n_perm": 0, "median_of_medians": None, "p97_5": None, "p02_5": None,
                "p95": None, "p99": None, "max": None, "min": None,
                "medians": [], "pooled_sample": []}
    with np.errstate(invalid="ignore"):
        med = np.nanmedian(sub, axis=1)
    med = med[~np.isnan(med)]
    pooled = sub[:50].ravel()
    pooled = pooled[~np.isnan(pooled)]
    return {"n_perm": int(med.size), "median_of_medians": float(np.median(med)),
            "p02_5": float(np.percentile(med, 2.5)), "p97_5": float(np.percentile(med, 97.5)),
            "p95": float(np.percentile(med, 95)), "p99": float(np.percentile(med, 99)),
            "max": float(med.max()), "min": float(med.min()),
            "medians": med.tolist(), "pooled_sample": pooled.tolist(),
            "n_pairs": int(sub.shape[1])}


def empirical_p(observed_median: Optional[float], null: Dict[str, Any]) -> Optional[float]:
    """One-sided permutation p: share of null medians at or above the observed one. Reported as
    `< 1/n_perm` when zero permutations reach it, never as a bare 0."""
    if observed_median is None or not null["medians"]:
        return None
    med = np.array(null["medians"], float)
    return float((med >= observed_median).sum() + 1) / (med.size + 1)


def selftest(mat: np.ndarray, models: List[str]) -> str:
    """
    Verify the FAST path against the reference one before any number built on it is trusted.
    Two arms, both required: the vectorised rank-correlation must reproduce scipy.spearmanr on
    the real observed matrix (else the whole null is measured with a different instrument than
    the observation), and a permutation must preserve each row's value multiset (else the null
    has the wrong tie structure and every comparison against it is inflated).
    """
    iu = np.triu_indices(len(models), k=1)
    fast = rho_matrix_from_ranks(rank_rows(mat))[iu]
    slow = np.array([stats.spearmanr(mat[i], mat[j]).statistic
                     for i, j in zip(*iu)], float)
    both = ~(np.isnan(fast) | np.isnan(slow))
    worst = float(np.abs(fast[both] - slow[both]).max()) if both.any() else 0.0
    if worst > 1e-9:
        raise SystemExit(f"SELFTEST FAILED: fast rho differs from scipy by {worst:.3e}")
    if (np.isnan(fast) != np.isnan(slow)).any():
        raise SystemExit("SELFTEST FAILED: fast/scipy disagree on which pairs are undefined")
    rng = np.random.default_rng(1)
    row = mat[0]
    if sorted(row[rng.permutation(row.size)].tolist()) != sorted(row.tolist()):
        raise SystemExit("SELFTEST FAILED: permutation did not preserve the value multiset")
    return (f"selftest PASS - vectorised rho matches scipy.spearmanr on all {int(both.sum())} "
            f"defined pairs (max |delta| {worst:.2e}); permutation preserves the tie multiset")
