"""
Location: paper-a/analysis/transfer_items.py
Purpose: BLOCK 1a-1c. Transfer computed over ITEMS rather than tasks, with a permutation null and a
         model-level bootstrap. Task-level top-k truncated for 50 of 90 pairs because most tasks
         never flip; items do not, so the headline stops being a statement about truncation. The
         null permutes each model's values among its OWN positions, and the bootstrap resamples
         CONFIGURATIONS, not pairs, because the 90 pairs share ten models and pair-level
         resampling would report a precision the design does not have.
Functions: item_cells(), observed(), permutation_null(), model_bootstrap(), selftest()
Calls: transfer.directed_transfer / transfer_rows / summarise_transfer (reused unchanged)
Imports: statistics, typing, numpy, transfer
"""

import statistics
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

import transfer


def item_cells(models: Sequence[str], names: Sequence[str], per_cell,
               keep: Optional[Dict[str, set]] = None
               ) -> Tuple[List[str], Dict[str, Dict[str, Dict[str, float]]]]:
    """(item keys, a cells-shaped dict keyed by item) so `transfer` runs UNCHANGED over items.

    The score is per-item dispersion, the share of runs disagreeing with the modal answer. An item
    measurable for one model and not another would silently give the two models different-length
    vectors, so an item is kept only where EVERY model measured it; the count that survives is
    reported by the caller rather than assumed."""
    keys, out = [], {m: {} for m in models}
    for n in names:
        idxs = sorted({i["item"] for i in per_cell[models[0]][n]
                       if keep is None or i["item"] in keep[n]})
        for idx in idxs:
            vals = {}
            for m in models:
                hit = next((i for i in per_cell[m][n] if i["item"] == idx), None)
                if hit is None or hit["flipped"] is None:
                    vals = {}
                    break
                vals[m] = hit["dispersion"]
            if not vals:
                continue
            key = f"{n}::{idx}"
            keys.append(key)
            for m in models:
                out[m][key] = {"wobble": vals[m]}
    return keys, out


def observed(models: Sequence[str], keys: Sequence[str], cells, frontier: Sequence[str],
             k: int) -> Dict[str, Any]:
    """The headline, built through the same two functions the task-level number came from, plus
    the mean and hits-against-expected that the median cannot represent."""
    rows = transfer.transfer_rows(list(frontier), keys, cells, [k])
    vecs = {m: {x: cells[m][x]["wobble"] for x in keys} for m in frontier}
    return dict(transfer.summarise_transfer(rows, k, list(frontier)),
                **transfer_stats(vecs, frontier, k, len(keys)),
                n_items=len(keys), rows=rows)


def transfer_stats(vecs: Dict[str, Dict[str, float]], frontier: Sequence[str], k: int,
                   n_items: int) -> Dict[str, Optional[float]]:
    """Median, mean, and total hits against expected, over every ordered frontier pair.

    All three, because the MEDIAN is degenerate on this corpus and reporting it alone would say
    the opposite of what the data shows. Overlap of a five-item set takes values in {0, 0.2, ...},
    and most pairs share nothing, so the median reads 0.000 at k=3 while the pairs that do overlap
    do so about ten times more often than chance. A statistic that cannot represent a minority
    effect is not evidence against one."""
    tops = {m: (transfer.top_k_nonzero(vecs[m], k), set(transfer.top_k_nonzero(vecs[m], 2 * k)))
            for m in frontier}
    rates, hits, expected = [], 0, 0.0
    for a in frontier:
        for b in frontier:
            if a == b or not tops[a][0] or not tops[b][1]:
                continue
            h = sum(1 for x in tops[a][0] if x in tops[b][1])
            rates.append(h / len(tops[a][0]))
            hits += h
            expected += len(tops[a][0]) * len(tops[b][1]) / n_items
    if not rates:
        return {"median": None, "mean": None, "hits": None, "expected": None, "ratio": None}
    return {"median": statistics.median(rates), "mean": sum(rates) / len(rates),
            "hits": hits, "expected": expected,
            "ratio": (hits / expected) if expected else None,
            "n_pairs_sharing": sum(1 for r in rates if r > 0), "n_pairs": len(rates)}


def permutation_null(models: Sequence[str], keys: Sequence[str], cells,
                     frontier: Sequence[str], k: int, n_perm: int = 2000,
                     seed: int = 20260729) -> Dict[str, Any]:
    """The null distribution of the median transfer under NO cross-model agreement.

    Each configuration's values are permuted among its OWN item positions, so its value multiset
    survives exactly: the number of non-zero items, the tie structure, and therefore the effective
    k and whether it truncates are all identical to the observed data. Permuting values ACROSS
    models would instead change how many unstable items each model has, and the resulting null
    would describe a different corpus."""
    rng = np.random.default_rng(seed)
    base = {m: np.array([cells[m][x]["wobble"] for x in keys], float) for m in frontier}
    draws: Dict[str, List[float]] = {"median": [], "mean": [], "hits": []}
    for _ in range(n_perm):
        vecs = {m: dict(zip(keys, rng.permutation(base[m]))) for m in frontier}
        st = transfer_stats(vecs, frontier, k, len(keys))
        for stat in draws:
            if st[stat] is not None:
                draws[stat].append(st[stat])
    out: Dict[str, Any] = {"n_perm": n_perm, "seed": seed}
    for stat, vals in draws.items():
        arr = np.array(vals, float)
        out[stat] = {"median": float(np.median(arr)), "p95": float(np.percentile(arr, 95)),
                     "p97_5": float(np.percentile(arr, 97.5)), "max": float(arr.max()),
                     "min": float(arr.min()), "values": vals}
    return out


def empirical_p(obs: Optional[float], values: Sequence[float]) -> Optional[str]:
    """One-sided p, reported as `< 1/(n+1)` when no permutation reaches the observed value. Never
    a bare zero: no permutation reaching it is a statement about N draws, not about the truth."""
    if obs is None or not len(values):
        return None
    arr = np.array(values, float)
    hits = int((arr >= obs).sum())
    return f"< {1.0 / (arr.size + 1):.5f}" if hits == 0 else f"{(hits + 1) / (arr.size + 1):.5f}"


def model_bootstrap(rows: List[Dict[str, Any]], frontier: Sequence[str], k: int,
                    n_boot: int = 2000, seed: int = 20260729) -> Dict[str, Any]:
    """95% interval on the median transfer, resampling CONFIGURATIONS with replacement.

    The 90 pairs are not independent observations: they are ten models crossed with themselves, so
    resampling pairs would treat one model's behaviour as up to eighteen independent facts and
    report an interval far tighter than the design supports. When a draw repeats a model, pairs of
    it with ITSELF are dropped rather than scored 1.0, which a duplicate would otherwise inject as
    a perfect transfer that was never measured."""
    rng = np.random.default_rng(seed)
    rate = {(r["from"], r["to"]): r["rate"] for r in rows
            if r["k"] == k and r.get("rate") is not None}
    fr = list(frontier)
    meds, means, npairs = [], [], []
    for _ in range(n_boot):
        draw = [fr[i] for i in rng.integers(0, len(fr), len(fr))]
        vals = [rate[(a, b)] for ia, a in enumerate(draw) for ib, b in enumerate(draw)
                if ia != ib and a != b and (a, b) in rate]
        if vals:
            meds.append(statistics.median(vals))
            means.append(sum(vals) / len(vals))
            npairs.append(len(vals))
    out = {"n_boot": len(meds), "seed": seed,
           "mean_pairs_per_draw": float(np.mean(npairs)) if npairs else None}
    for name, vals in (("median", meds), ("mean", means)):
        arr = np.array(vals, float)
        out[name] = {"point": float(np.median(arr)), "lo": float(np.percentile(arr, 2.5)),
                     "hi": float(np.percentile(arr, 97.5))}
    return out


def _vec(keys, top, tail, scale):
    """One model's item vector: `top` most unstable, then `tail` mildly unstable, rest exactly 0.
    Enough non-zero entries that a top-2k does not truncate, so a truncation assertion tests the
    statistic rather than the fixture's size."""
    out = {}
    for i, k in enumerate(keys):
        out[k] = (scale * (1.0 - i / 100) if i in top
                  else (0.2 * (1.0 - i / 100) if i in tail else 0.0))
    return out


def _fixture() -> Tuple[List[str], Dict[str, Dict[str, Dict[str, float]]], List[str]]:
    """Three models that agree exactly on which five items are most unstable. Each carries twelve
    non-zero items so the 2k side is full."""
    keys = [f"L::{i}" for i in range(30)]
    top, tail = set(range(5)), set(range(5, 12))
    cells = {m: {k: {"wobble": v} for k, v in _vec(keys, top, tail, s).items()}
             for m, s in (("a", 1.0), ("b", 0.9), ("c", 0.8))}
    return keys, cells, ["a", "b", "c"]


def _disjoint(n_models: int = 3, span: int = 20):
    """Models whose unstable items cannot overlap: a true zero, the negative control."""
    keys = [f"L::{i}" for i in range(span * n_models)]
    cells = {m: {kk: {"wobble": v} for kk, v in
                 _vec(keys, set(range(span * j, span * j + 5)),
                      set(range(span * j + 5, span * j + 12)), 1.0).items()}
             for j, m in enumerate(["a", "b", "c"][:n_models])}
    return keys, cells, ["a", "b", "c"][:n_models]


def _st_statistic() -> None:
    """Perfect agreement, true disjointness, and the minority case in between."""
    keys, cells, fr = _fixture()
    obs = observed(fr, keys, cells, fr, 5)
    assert obs["n_truncated"] == 0, f"the fixture must not truncate: {obs['n_truncated']}"
    assert obs["median"] == 1.0, f"three models agreeing exactly must give median 1.0: {obs}"
    assert obs["ratio"] > 1.0, f"a real effect must exceed chance: {obs['ratio']}"
    ok, oc, ofr = _disjoint()
    o = observed(ofr, ok, oc, ofr, 5)
    assert o["median"] == 0.0 and o["hits"] == 0, \
        f"disjoint unstable sets must be zero on BOTH statistics: {o['median']}/{o['hits']}"
    minority = dict(oc)
    minority["c"] = {kk: dict(v) for kk, v in oc["a"].items()}          # c now mirrors a
    mo = observed(ofr, ok, minority, ofr, 5)
    assert mo["median"] == 0.0 and mo["hits"] > 0, \
        (f"a MINORITY of agreeing pairs must leave the median at 0 with hits positive -- this is "
         f"exactly the case that reporting the median alone would call 'no effect': {mo}")


def _st_inference() -> None:
    """The null must sit below a real effect, and the bootstrap must bracket the observation and
    lose pairs to repeated draws rather than scoring a model against itself."""
    keys, cells, fr = _fixture()
    obs = observed(fr, keys, cells, fr, 5)
    null = permutation_null(fr, keys, cells, fr, 5, n_perm=200, seed=1)
    assert null["median"]["median"] < obs["median"], \
        f"the null median must sit BELOW a real agreement: {null['median']} vs {obs['median']}"
    p = empirical_p(obs["median"], null["median"]["values"])
    assert p.startswith("<") or float(p) < 0.2, "a real effect must be unlikely under the null"
    assert empirical_p(None, null["median"]["values"]) is None, "an absent observation has no p"
    boot = model_bootstrap(obs["rows"], fr, 5, n_boot=200, seed=1)
    assert boot["median"]["lo"] <= obs["median"] <= boot["median"]["hi"], \
        f"the bootstrap interval must contain the observed median: {boot}"
    assert boot["mean_pairs_per_draw"] < len(fr) * (len(fr) - 1), \
        "a resample with repeats must yield FEWER usable pairs, not the full set"


def selftest() -> str:
    """Prove the statistic and its null BOTH discriminate, on data whose answer is known."""
    _st_statistic()
    _st_inference()
    return ("transfer_items selftest PASS - perfect agreement scores 1.0 with no truncation, "
            "disjoint sets score 0.0 on median AND hits, a minority-agreement fixture leaves the "
            "median at 0.0 with positive hits (the case the median alone would misreport), the "
            "permutation null sits below a real effect, and the model-level bootstrap brackets "
            "the observation while dropping self-pairs from repeated draws")
