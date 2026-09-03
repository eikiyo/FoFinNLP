"""
Location: paper-a/analysis/contamination.py
Purpose: THE §0 GATE, and the only thing that may run before the paper is drafted. 46 of 470 items
         carry a provenance defect: the validating quote is outside the window the model is shown,
         or is not in the source document at all. An item whose answer is not in its window cannot
         be answered from its window, so the model must guess -- and guessing is maximally
         unstable. If wobble is higher on those items, every headline number in this paper is
         partly a measurement of a defect in our own resource. This decides which numbers are the
         paper's headline numbers.
Functions: flagged_index(), oracle_ids(), keep_sets(), subset_cells(),
           newcombe(), partition_rows(), pooled_row(), recompute(), run(), selftest()
Calls: oracle_audit (the flag source), fold (per-item flip flags), categories, analyses, transfer
Imports: json, math, typing, analyses, categories, config, fold, oracle_audit, transfer
"""

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

import adjudication as ADJ
import contam_checks as CK
import analyses as an
import categories
import config
import fold
import oracle_audit
import transfer

MATERIAL = "the Wilson interval on the difference excludes zero"


def flagged_index(audit_rows: List[Dict[str, Any]]) -> Dict[str, Set[str]]:
    """leaf -> the set of oracle ids the audit flagged. Taken from `oracle_audit.audit_all()`
    rather than re-derived, so the partition and the reported counts cannot disagree."""
    out: Dict[str, Set[str]] = {}
    for r in audit_rows:
        if r["issues"]:
            out.setdefault(r["leaf"], set()).add(str(r["item"]))
    return out


def oracle_ids(leaves: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """leaf -> oracle ids IN FILE ORDER, which is the order `runner.load_instances` builds its
    instance list in, and therefore the order `fold.item_rates` indexes items by. Read from the
    same `oracle.jsonl` the audit read; the index<->id mapping is re-derived, never assumed."""
    out: Dict[str, List[str]] = {}
    for entry in leaves:
        path = config.probity_root() / entry["rel"] / "oracle.jsonl"
        out[entry["leaf"]] = [str(json.loads(l)["id"])
                              for l in path.read_text().splitlines() if l.strip()]
    return out


def keep_sets(names: Sequence[str], flagged: Dict[str, Set[str]], ids: Dict[str, List[str]],
              excluded: Optional[Dict[str, Set[str]]] = None) -> Dict[str, Any]:
    """Positional index sets for both partitions, plus the join audit.

    A join that RUNS is not a join that MATCHED. If the id sets do not overlap, the flagged
    partition is empty, the difference is exactly zero, and this module prints a confident clean
    bill of health for the worst possible reason: it compared nothing. So the overlap is counted
    and a zero overlap is fatal."""
    excluded = ADJ.exclusions() if excluded is None else excluded
    clean: Dict[str, Set[int]] = {}
    flag: Dict[str, Set[int]] = {}
    drop: Dict[str, Set[int]] = {}
    matched = unmatched = missing_drop = 0
    for n in names:
        seq = ids.get(n, [])
        want = flagged.get(n, set())
        hit = {i for i, iid in enumerate(seq) if iid in want}
        matched += len(hit)
        unmatched += len(want) - len(hit)
        # The adjudicated exclusions come out of BOTH partitions and out of the all-items reading,
        # so a headline number cannot include an item the author removed. They are subtracted, not
        # deleted: the raw responses stay on disk and the flag row carries the verdict and reason.
        gone = {i for i, iid in enumerate(seq) if iid in excluded.get(n, set())}
        missing_drop += len(excluded.get(n, set())) - len(gone)
        drop[n] = gone
        flag[n] = hit - gone
        clean[n] = set(range(len(seq))) - hit - gone
    if matched == 0:
        raise SystemExit("CONTAMINATION JOIN MATCHED 0 ITEMS -- the id<->index join is broken, not "
                         "the data. Refusing to report a null difference from an empty partition.")
    if unmatched:
        raise SystemExit(f"{unmatched} flagged ids were not found in their leaf's oracle order -- "
                         "the audit and the reconstruction disagree about what an item is.")
    if missing_drop:
        raise SystemExit(f"{missing_drop} adjudicated exclusions were not found in their leaf's "
                         "oracle order -- an exclusion that matches nothing silently excludes "
                         "nothing, which would report the pre-adjudication corpus as adjudicated.")
    return {"clean": clean, "flagged": flag, "excluded": drop,
            "n_excluded": sum(len(v) for v in drop.values()), "n_matched": matched,
            "n_leaves_with_flags": sum(1 for n in names if flag[n]),
            "n_leaves_audited": sum(1 for n in names if ids.get(n))}


def subset_cells(models: Sequence[str], names: Sequence[str], per_cell,
                 keep: Optional[Dict[str, Set[int]]] = None) -> Dict[str, Dict[str, Dict]]:
    """A cells dict in the exact shape `matrix.load_cells` produces, counted over a subset of each
    leaf's items. `keep=None` means every item, which is what makes the identity check below run
    through the SAME code path the clean-only numbers come from."""
    out: Dict[str, Dict[str, Dict]] = {}
    for m in models:
        out[m] = {}
        for n in names:
            items = [i for i in per_cell[m][n]
                     if i["flipped"] is not None and (keep is None or i["item"] in keep[n])]
            flipped = sum(1 for i in items if i["flipped"])
            maj = sum(1 for i in items if i.get("majority"))
            out[m][n] = {"flipped": flipped, "n_items": len(items), "absent": False,
                         "dropped": not items, "n_majority": maj,
                         "accuracy": (maj / len(items)) if items else None,
                         "wobble": (flipped / len(items)) if items else None}
    return out


def filter_per_cell(models: Sequence[str], names: Sequence[str], per_cell,
                    keep: Dict[str, Set[int]]):
    """The same partition, applied to the RAW per-item records rather than to their counts, so that
    every existing per-item diagnostic (`folddiag.pooled_p`, `p_bucket_flips`, `fold.leaf_rows`)
    runs on clean-only data UNCHANGED. Filter once, reuse everything."""
    return {m: {n: [i for i in per_cell[m][n] if i["item"] in keep[n]] for n in names}
            for m in models}



def newcombe(k1: int, n1: int, k2: int, n2: int) -> Optional[Dict[str, float]]:
    """Newcombe's score interval for the DIFFERENCE of two independent proportions (p1 - p2),
    composed from the two single-proportion Wilson intervals rather than introducing a second
    interval implementation.

        lower = d - sqrt((p1-l1)^2 + (u2-p2)^2)
        upper = d + sqrt((u1-p1)^2 + (p2-l2)^2)

    Independence is an ASSUMPTION here and it is the one that could be wrong: both partitions come
    from the same runs of the same models. It is stated in the output rather than buried."""
    if n1 <= 0 or n2 <= 0:
        return None
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = categories.wilson(k1, n1)
    l2, u2 = categories.wilson(k2, n2)
    d = p1 - p2
    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return {"d": d, "lo": max(-1.0, lo), "hi": min(1.0, hi),
            "excludes_zero": (lo > 0) or (hi < 0), "width": hi - lo}


def _rate_row(cells_m, names: Sequence[str]) -> Tuple[int, int]:
    return (sum(cells_m[n]["flipped"] for n in names),
            sum(cells_m[n]["n_items"] for n in names))


def partition_rows(models: Sequence[str], names: Sequence[str], clean, flag
                   ) -> List[Dict[str, Any]]:
    """Per model: wobble on flagged items, wobble on clean items, both with Wilson intervals, and
    the interval on their difference. `n_flagged` rides on every row -- a wide interval on 46 items
    is NO POWER, not NO EFFECT, and the two must never be reported as the same verdict."""
    rows = []
    for m in list(models) + ["POOLED"]:
        if m == "POOLED":
            kf, nf = (sum(r["k_flagged"] for r in rows), sum(r["n_flagged"] for r in rows))
            kc, nc = (sum(r["k_clean"] for r in rows), sum(r["n_clean"] for r in rows))
        else:
            kf, nf = _rate_row(flag[m], names)
            kc, nc = _rate_row(clean[m], names)
        cf, cc = categories.wilson(kf, nf), categories.wilson(kc, nc)
        rows.append({"model": m, "k_flagged": kf, "n_flagged": nf, "k_clean": kc, "n_clean": nc,
                     "w_flagged": (kf / nf) if nf else None,
                     "w_clean": (kc / nc) if nc else None,
                     "lo_flagged": cf[0] if cf else None, "hi_flagged": cf[1] if cf else None,
                     "lo_clean": cc[0] if cc else None, "hi_clean": cc[1] if cc else None,
                     "diff": newcombe(kf, nf, kc, nc)})
    return rows


def recompute(models: Sequence[str], leaves: List[Dict[str, Any]], cells,
              frontier: Sequence[str], ks: Sequence[int] = (5, 10)) -> Dict[str, Any]:
    """Every headline the spec names, rebuilt on one cells dict. Called twice -- once on the
    published all-item cells and once on clean-only -- so the delta is a difference between two
    runs of the SAME function, never between a fresh computation and a remembered number."""
    names = [l["leaf"] for l in leaves]
    active = an.active_subset(list(models), names, cells)
    rows = transfer.transfer_rows(models, active, cells, ks)
    return {"agg": an.aggregate_wobble(list(models), names, cells),
            "cat": categories.category_cells(models, leaves, cells),
            "active": active,
            "split": an.capability_split(an.aggregate_wobble(list(models), names, cells)),
            "transfer": {k: transfer.summarise_transfer(rows, k, list(frontier)) for k in ks}}


def run(models: Sequence[str], leaves: List[Dict[str, Any]], published_cells,
        frontier: Sequence[str], accuracy=None) -> Dict[str, Any]:
    """The gate, end to end. Controls first: nothing here is read until the join has matched and
    the partition has been shown to sum back to the published counts."""
    names = [l["leaf"] for l in leaves]
    audit = oracle_audit.audit_all()
    per_cell = fold.collect(models, leaves)["per_cell"]
    published_all = subset_cells(models, names, per_cell)
    checks = [CK.identity_check(models, names, published_all, published_cells, accuracy)]
    keep = keep_sets(names, flagged_index(audit), oracle_ids(leaves))
    # The "all items" reading is the BEFORE-the-audit contrast, so it must sit on the same corpus
    # as the after: every item minus the ones the author excluded. Left as the raw published set,
    # the all-vs-clean delta would be part audit and part adjudication, and the paper attributes
    # the whole of it to the audit. `published_all` is kept separately for the identity check,
    # which must run against what was actually published.
    keep["all"] = {n: keep["clean"][n] | keep["flagged"][n] for n in names}
    whole = subset_cells(models, names, per_cell, keep["all"])
    clean = subset_cells(models, names, per_cell, keep["clean"])
    flag = subset_cells(models, names, per_cell, keep["flagged"])
    dropped = subset_cells(models, names, per_cell, keep["excluded"])
    checks.append(CK.sum_check(models, names, clean, flag, published_cells, dropped))
    rows = partition_rows(models, names, clean, flag)
    pooled = rows[-1]
    return {"checks": checks, "join": keep, "rows": rows, "pooled": pooled,
            "audit_summary": oracle_audit.summarise(audit), "audit_rows": audit,
            "material": bool(pooled["diff"] and pooled["diff"]["excludes_zero"]),
            "per_cell": per_cell, "keep": keep, "cells_clean": clean, "cells_flagged": flag,
            "cells_excluded": dropped, "n_excluded": keep["n_excluded"],
            "cells_all": whole,
            "all_items": recompute(models, leaves, whole, frontier),
            "cells_published": published_all, "n_published_items": sum(
                published_all[models[0]][n]["n_items"] for n in names),
            "clean_only": recompute(models, leaves, clean, frontier),
            "n_models_diff_excludes_zero": sum(
                1 for r in rows[:-1] if r["diff"] and r["diff"]["excludes_zero"])}


def selftest() -> str:
    """Prove the difference interval discriminates BOTH ways, and prove the partition helper is
    exact. A gate that has only ever seen convenient input has not been shown to work."""
    big = newcombe(90, 100, 10, 100)
    assert big["excludes_zero"] and big["lo"] > 0, f"a real difference must be detected: {big}"
    same = newcombe(50, 100, 50, 100)
    assert not same["excludes_zero"] and abs(same["d"]) < 1e-12, \
        f"identical rates must give a difference interval containing zero: {same}"
    tiny = newcombe(1, 2, 500, 1000)
    assert not tiny["excludes_zero"], "a 2-item sample must NOT manufacture a significant difference"
    assert tiny["width"] > big["width"], "an underpowered comparison must have the wider interval"
    assert newcombe(0, 0, 5, 10) is None, "an empty partition must refuse, never return 0.0"
    neg = newcombe(10, 100, 90, 100)
    assert neg["excludes_zero"] and neg["hi"] < 0, "the interval must detect a NEGATIVE difference"
    per_cell = {"m": {"L": [{"item": 0, "flipped": True, "majority": False},
                            {"item": 1, "flipped": False, "majority": True},
                            {"item": 2, "flipped": None, "majority": True}]}}
    whole = subset_cells(["m"], ["L"], per_cell)["m"]["L"]
    assert (whole["flipped"], whole["n_items"], whole["wobble"]) == (1, 2, 0.5), \
        f"unmeasurable items must be excluded from both counts: {whole}"
    assert whole["accuracy"] == 0.5 and whole["n_majority"] == 1, \
        f"accuracy must be counted over the SAME measured items as wobble: {whole}"
    half = subset_cells(["m"], ["L"], per_cell, {"L": {1}})["m"]["L"]
    assert half["n_items"] == 1 and half["flipped"] == 0, f"the keep set must filter: {half}"
    empty = subset_cells(["m"], ["L"], per_cell, {"L": set()})["m"]["L"]
    assert empty["wobble"] is None and empty["accuracy"] is None and empty["dropped"], \
        "an empty partition must be None (not measured), never 0.0 (perfectly stable / all wrong)"
    filt = filter_per_cell(["m"], ["L"], per_cell, {"L": {0, 2}})
    assert [i["item"] for i in filt["m"]["L"]] == [0, 2], f"filter_per_cell must keep order: {filt}"
    return ("contamination selftest PASS - the difference interval fires on a real gap, stays "
            "silent on equal rates, refuses an underpowered one, detects a negative gap, and the "
            "partition counter is exact on measured / unmeasurable / empty for wobble AND accuracy")
