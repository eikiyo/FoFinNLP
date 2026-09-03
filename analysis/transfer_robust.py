"""
Location: paper-a/analysis/transfer_robust.py
Purpose: BLOCK 1e-1g. The three checks that decide what the transfer result is ALLOWED to claim.
         1e accuracy-matched: do models agree on which items are UNSTABLE, or only on which are
         HARD? 1f serving path: is part of the agreement shared infrastructure rather than shared
         behaviour? 1g leave-one-out: does one configuration carry the result?
Functions: item_accuracy(), strata(), accuracy_matched(), path_split(), leave_one_out(), selftest()
Calls: transfer_items.transfer_stats (the ONE statistic, so a stratum and the headline agree)
Imports: statistics, typing, config, transfer_items
"""

import statistics
from typing import Any, Dict, List, Optional, Sequence

import transfer_items as TI

# Accuracy bins. Coarse deliberately: with 432 items and 10 configurations a finer grid gives
# strata too small to carry a top-5 statistic, and a stratum that cannot support the statistic
# reports the bin size rather than anything about the models.
BINS = ((0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.01))


def item_accuracy(models: Sequence[str], names: Sequence[str], per_cell,
                  keys: Sequence[str]) -> Dict[str, float]:
    """Pooled accuracy per item: the share of configurations whose majority answer is correct.

    Pooled across the SAME configurations the transfer is computed over, so 'matched on accuracy'
    means matched on the difficulty those models actually experienced, not on a difficulty label
    assigned by a different population."""
    lookup = {}
    for n in names:
        for m in models:
            for it in per_cell[m][n]:
                if it["flipped"] is not None:
                    lookup.setdefault(f"{n}::{it['item']}", []).append(bool(it.get("majority")))
    return {k: (sum(lookup[k]) / len(lookup[k])) for k in keys if lookup.get(k)}


def strata(keys: Sequence[str], acc: Dict[str, float]) -> Dict[str, List[str]]:
    """Items grouped into accuracy bins, keyed by a readable label."""
    out: Dict[str, List[str]] = {f"{lo:.2f}-{min(hi, 1.0):.2f}": [] for lo, hi in BINS}
    for k in keys:
        if k not in acc:
            continue
        for lo, hi in BINS:
            if lo <= acc[k] < hi:
                out[f"{lo:.2f}-{min(hi, 1.0):.2f}"].append(k)
                break
    return out


def accuracy_matched(cells, frontier: Sequence[str], bins: Dict[str, List[str]],
                     k: int) -> List[Dict[str, Any]]:
    """The headline statistic recomputed INSIDE each accuracy stratum.

    If agreement is really agreement about difficulty, it dissolves once difficulty is held fixed.
    A stratum with too few items to fill a top-2k is reported with its size and marked, never
    silently dropped: an empty row and a null result look identical in a table and mean opposite
    things."""
    out = []
    for label, ks in sorted(bins.items()):
        if len(ks) < 2 * k:
            out.append({"stratum": label, "n_items": len(ks), "usable": False,
                        "reason": f"fewer than {2 * k} items, cannot fill a top-{2 * k}"})
            continue
        vecs = {m: {x: cells[m][x]["wobble"] for x in ks} for m in frontier}
        st = TI.transfer_stats(vecs, frontier, k, len(ks))
        out.append({"stratum": label, "n_items": len(ks), "usable": True, "reason": "", **st})
    return out


def path_split(rows: List[Dict[str, Any]], serving: Dict[str, str], k: int,
               family: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
    """Mean transfer for routed-routed, direct-direct and mixed ordered pairs.

    If same-path pairs agree with each other more than mixed ones, part of the shared instability
    is the serving layer rather than the models. Reported whichever way it comes out; a control run
    only when it is expected to be null is not a control.

    Every group is ALSO reported with same-FAMILY pairs excluded. There are three direct-served
    configurations and two of them are one family, so a single family pair is a sixth of that
    group: without the exclusion, 'models on the same serving path agree' and 'two versions of one
    model agree' are the same number wearing different labels."""
    groups: Dict[str, List[float]] = {}
    cross: Dict[str, List[float]] = {}
    for r in rows:
        if r["k"] != k or r.get("rate") is None:
            continue
        pa, pb = serving.get(r["from"], "?"), serving.get(r["to"], "?")
        label = f"{pa}-{pb}" if pa == pb else "mixed"
        groups.setdefault(label, []).append(r["rate"])
        if family is None or family.get(r["from"]) != family.get(r["to"]):
            cross.setdefault(label, []).append(r["rate"])
    out = []
    for lab, v in sorted(groups.items()):
        c = cross.get(lab, [])
        out.append({"pairing": lab, "n_pairs": len(v), "mean": sum(v) / len(v),
                    "median": statistics.median(v),
                    "n_pairs_cross_family": len(c),
                    "mean_cross_family": (sum(c) / len(c)) if c else None})
    return out


def leave_one_out(keys: Sequence[str], cells, frontier: Sequence[str],
                  k: int) -> List[Dict[str, Any]]:
    """Drop each configuration in turn and recompute the headline over the remaining nine.

    Shows no single model carries the result. Reported on the MEAN and the hits ratio rather than
    the median, because the median is degenerate on this corpus and a leave-one-out over a
    statistic that cannot move is not a sensitivity analysis."""
    out = []
    full = TI.transfer_stats({m: {x: cells[m][x]["wobble"] for x in keys} for m in frontier},
                             frontier, k, len(keys))
    out.append({"dropped": "(none)", "n_models": len(frontier), "mean": full["mean"],
                "ratio": full["ratio"], "hits": full["hits"]})
    for drop in frontier:
        rest = [m for m in frontier if m != drop]
        st = TI.transfer_stats({m: {x: cells[m][x]["wobble"] for x in keys} for m in rest},
                               rest, k, len(keys))
        out.append({"dropped": drop, "n_models": len(rest), "mean": st["mean"],
                    "ratio": st["ratio"], "hits": st["hits"]})
    return out


def _fx():
    """Twelve items; a and b share their unstable set, c is disjoint. Accuracy is arranged so the
    agreeing pair's items sit in ONE stratum, which is what makes the matched test meaningful."""
    keys = [f"L::{i}" for i in range(24)]
    cells = {"a": {x: {"wobble": 1.0 - i / 100 if i < 12 else 0.0} for i, x in enumerate(keys)},
             "b": {x: {"wobble": 0.9 - i / 100 if i < 12 else 0.0} for i, x in enumerate(keys)},
             "c": {x: {"wobble": 1.0 - i / 100 if i >= 12 else 0.0} for i, x in enumerate(keys)}}
    return keys, cells, ["a", "b", "c"]


def _st_strata() -> None:
    """Binning must be exhaustive, and a stratum too small for the statistic must say so."""
    keys, cells, fr = _fx()
    acc = {x: (0.9 if i < 12 else 0.1) for i, x in enumerate(keys)}
    bins = strata(keys, acc)
    assert sum(len(v) for v in bins.values()) == len(keys), "every item must land in a stratum"
    assert len(bins["0.75-1.00"]) == 12 and len(bins["0.00-0.25"]) == 12, f"binning wrong: {bins}"
    hi = next(r for r in accuracy_matched(cells, fr, bins, 3) if r["stratum"] == "0.75-1.00")
    assert hi["usable"] and hi["hits"] > 0, f"agreement inside a stratum must survive: {hi}"
    small = accuracy_matched(cells, fr, {"tiny": keys[:3]}, 3)[0]
    assert small["usable"] is False and "fewer than" in small["reason"], \
        f"an unusable stratum must say WHY, not report a number from too few items: {small}"


def selftest() -> str:
    """Prove each check can change its verdict, not merely produce a number."""
    keys, cells, fr = _fx()
    _st_strata()
    rows = [{"k": 3, "from": "a", "to": "b", "rate": 1.0},
            {"k": 3, "from": "a", "to": "c", "rate": 0.0},
            {"k": 3, "from": "b", "to": "c", "rate": 0.0}]
    serving = {"a": "routed", "b": "routed", "c": "direct"}
    ps = path_split(rows, serving, 3)
    rr = next(r for r in ps if r["pairing"] == "routed-routed")
    mx = next(r for r in ps if r["pairing"] == "mixed")
    assert rr["mean"] == 1.0 and mx["mean"] == 0.0, \
        f"the split must separate same-path from mixed pairs: {ps}"

    # With a AND b in one family, the routed-routed group is entirely same-family and its
    # cross-family mean must vanish rather than silently repeating the confounded number.
    fam = path_split(rows, serving, 3, {"a": "fam1", "b": "fam1", "c": "fam2"})
    rrf = next(r for r in fam if r["pairing"] == "routed-routed")
    assert rrf["mean"] == 1.0 and rrf["n_pairs_cross_family"] == 0 \
        and rrf["mean_cross_family"] is None, \
        (f"a group with no cross-family pair left must report None, not the same-family mean "
         f"relabelled as a control: {rrf}")

    loo = leave_one_out(keys, cells, fr, 3)
    assert loo[0]["dropped"] == "(none)" and len(loo) == len(fr) + 1, "every model dropped once"
    dropped_a = next(r for r in loo if r["dropped"] == "a")
    assert dropped_a["hits"] == 0, \
        (f"dropping one of the only two agreeing models must collapse the effect to zero -- if it "
         f"does not, the leave-one-out is not sensitive to anything: {dropped_a}")
    return ("transfer_robust selftest PASS - every item lands in exactly one accuracy stratum, an "
            "under-sized stratum reports why instead of a number, the serving split separates "
            "same-path from mixed pairs, and dropping a configuration that carries the effect "
            "collapses it to zero")
