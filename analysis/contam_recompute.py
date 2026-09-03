"""
Location: paper-a/analysis/contam_recompute.py
Purpose: The §0 gate's second half. Once the partition is proven exact, rebuild the ITEM-LEVEL
         headline numbers on clean items only -- the per-item correct-rate distribution, the
         accuracy-decile frontier, the surviving fraction of the wobble-accuracy correlation, the
         conservative worst-to-mean ratio, and split-half reliability. Nothing here re-implements
         a diagnostic: the per-item records are filtered once and every existing stage-3 function
         is run over the filtered copy unchanged.
Functions: parity_cells(), reliability_rows(), diagnostics(), conservative_block(), rebuild()
Calls: contamination.filter_per_cell/subset_cells, fold, folddiag, conservative, robustness,
       splithalf, categories
Imports: typing, config, contamination, conservative, fold, folddiag, robustness, splithalf
"""

from typing import Any, Dict, List, Optional, Sequence, Set

import categories
import config
import contamination as C
import conservative
import fold
import folddiag
import robustness
import splithalf
import stats_core as sc


def parity_cells(models: Sequence[str], leaves: List[Dict[str, Any]],
                 keep: Optional[Dict[str, Set[int]]] = None) -> Dict[str, Any]:
    """Per-item flip flags for the ODD runs and the EVEN runs of every cell, restricted to `keep`.

    This is the only new pass over the raw runs the gate needs, and it exists because split-half
    reliability is quoted in the abstract: if the headline wobble numbers are clean-only, a
    reliability computed over the items those numbers exclude is a different instrument. One pass
    serves both halves.

    The engine's own cell-level measurability rule is applied to each half exactly as
    `splithalf._score` applies it -- a half-cell over the parse-failure threshold contributes
    nothing, not a number. Without that this would be a DIFFERENT estimator wearing the same name,
    and `reliability_control` below (which requires the unfiltered run to reproduce the published
    reliability per model) would have no way to notice."""
    scorer, runner, _ = splithalf.engine_modules()
    names = [l["leaf"] for l in leaves]
    halves: Dict[int, Dict[str, Dict[str, List[Dict[str, Any]]]]] = {
        0: {m: {} for m in models}, 1: {m: {} for m in models}}
    opened = []
    for entry in leaves:
        task = splithalf._task_of(entry["rel"])
        instances, _ = runner.load_instances(config.probity_root() / entry["rel"], entry["field"])
        for m in models:
            runs, path = splithalf.leaf_runs(entry["rel"], m)
            opened.append(path)
            for parity in (0, 1):
                sub = [r for r in runs if r.get("run_idx", 0) % 2 == parity]
                ok = bool(sub) and scorer.score_runs(task, instances, sub).get("measurable", False)
                halves[parity][m][entry["leaf"]] = (
                    fold.item_rates(task, instances, sub, entry["field"]) if ok else [])
    config.assert_arm_clean(opened)
    return {p: C.subset_cells(models, names, halves[p], keep) for p in (0, 1)}


def reliability_control(rows: List[Dict[str, Any]], published_csv) -> str:
    """POSITIVE CONTROL on the reliability path. Run over ALL items, this must reproduce the
    published per-model split-half reliability exactly. If it does not, the clean-only figure is a
    different estimator and its delta measures the estimator, not the exclusion."""
    pub = {}
    for line in published_csv.read_text().splitlines()[1:]:
        f = line.split(",")
        if len(f) > 6 and f[6]:
            pub[f[0]] = float(f[6])
    # The published CSV stores 6 decimals, so the comparison is made at the quantum the file
    # actually holds. A tighter tolerance reds on the file's own rounding, which is a false RED
    # about the formatter rather than a finding about the estimator.
    bad = [f"{r['model']}: recomputed {r['r_full']} vs published {pub[r['model']]}"
           for r in rows if r["model"] in pub
           and (r["r_full"] is None or abs(r["r_full"] - pub[r["model"]]) > 5e-7)]
    if not pub:
        raise SystemExit("reliability control read 0 published values -- the probe is broken")
    if bad:
        raise SystemExit("RELIABILITY CONTROL FAILED:\n  " + "\n  ".join(bad))
    return (f"reliability PASS - the item-partition path reproduces all {len(pub)} published "
            f"split-half values exactly, so the clean-only figure differs only by the item set")


def reliability_rows(models: Sequence[str], names: Sequence[str], halves) -> List[Dict[str, Any]]:
    """Per model: the odd-half wobble vector against the even-half vector over the tasks, and the
    Spearman-Brown step up to full length. Same estimator as `splithalf.reliability_rows`, run over
    a restricted item set; the correction itself is reused, never re-derived."""
    rows = []
    for m in models:
        va = [halves[0][m][n]["wobble"] for n in names]
        vb = [halves[1][m][n]["wobble"] for n in names]
        st = sc.pair_stats(va, vb)
        defined = [(x, y) for x, y in zip(va, vb) if x is not None and y is not None]
        rows.append({"model": m, "n_leaves": len(defined), "r_half": st["rho"],
                     "r_full": splithalf.spearman_brown(st["rho"]),
                     "reason": st.get("reason") or ""})
    return rows


def _median(vals: Sequence[Optional[float]]) -> Optional[float]:
    ok = sorted(v for v in vals if v is not None)
    if not ok:
        return None
    mid = len(ok) // 2
    return ok[mid] if len(ok) % 2 else (ok[mid - 1] + ok[mid]) / 2


def diagnostics(models: Sequence[str], leaves: List[Dict[str, Any]], per_cell) -> Dict[str, Any]:
    """Every item-level stage-3 diagnostic, run over one per-item record set. Called twice -- on
    the unfiltered records and on the clean-only copy -- so each delta is a difference between two
    runs of the SAME function, never between a computation and a remembered number.

    Wobble AND accuracy are both re-counted from the same records by `subset_cells`, which the
    gate's identity check has already shown reproduces the published matrices exactly. Reading
    accuracy from `scored.json` instead would mean the two axes of Figure 1(b) came from different
    item sets the moment a filter is applied."""
    names = [l["leaf"] for l in leaves]
    cells = C.subset_cells(models, names, per_cell)
    acc = {m: {n: cells[m][n]["accuracy"] for n in names} for m in models}
    means = robustness.leaf_means(models, names, cells, acc)
    rows = fold.leaf_rows(models, per_cell, means)
    return {"pooled_p": folddiag.pooled_p(models, names, per_cell),
            "p_buckets": folddiag.p_bucket_flips(models, names, per_cell),
            "frontier": folddiag.decile_frontier(rows),
            "surviving": folddiag.surviving_fraction(rows),
            "zone": robustness.nightmare_leaves(means),
            "rho": robustness.wobble_vs_accuracy(means),
            "leaf_rows": rows, "leaf_means": means}


def conservative_block(models: Sequence[str], leaves: List[Dict[str, Any]], cells,
                       frontier: Sequence[str]) -> Dict[str, Any]:
    """Appendix Table 4's first two rows -- the worst-to-mean ratio under both estimability floors,
    and the capability-gradient regression -- rebuilt on one cells dict. These are the paper's
    most-attacked numbers, so they are recomputed rather than assumed stable under the exclusion."""
    names = [l["leaf"] for l in leaves]
    cat = categories.category_cells(models, leaves, cells)
    totals = conservative.model_totals(models, names, cells)
    out: Dict[Any, Any] = {}
    for floor in (3, 5):
        rows = conservative.conservative_rows(models, cat, totals, floor)
        out[floor] = {"rows": rows,
                      "median_point": _median([r["point_ratio"] for r in rows]),
                      "median_cons": _median([r["cons_ratio"] for r in rows]),
                      "n_over_2x": sum(1 for r in rows
                                       if (r["cons_ratio"] or 0) > conservative.RATIO_BAR)}
    out["gradient"] = [
        conservative.worst_on_mean(out[3]["rows"], "point_rate", None, "all 12 models"),
        conservative.worst_on_mean(out[3]["rows"], "point_rate", frontier, "frontier only")]
    out["cat"] = cat
    return out


def rebuild(models: Sequence[str], leaves: List[Dict[str, Any]], gate: Dict[str, Any],
            published_cells, active_all: Sequence[str], active_clean: Sequence[str],
            frontier: Sequence[str]) -> Dict[str, Any]:
    """The whole clean-only rebuild, plus the all-item version of each number beside it.

    Reliability is computed over the ACTIVE subset, matching `stage2._step1`: a task no model ever
    wobbles on carries no ranking information and only inflates tie mass. Because the exclusion
    also SHRINKS that subset (a task whose only unstable items were flagged goes silent), the
    same-leaf-set control is computed too -- otherwise a change in reliability could be the item
    filter or the smaller leaf set and the number could not say which."""
    names = [l["leaf"] for l in leaves]
    clean_pc = C.filter_per_cell(models, names, gate["per_cell"], gate["keep"]["clean"])
    # The reported "all" reading sits on the SAME corpus as the clean one -- every item minus the
    # 7 the author excluded at adjudication -- matching `contamination.run`, whose comment states
    # that attribution rule. Unfiltered, this branch fed Table 5 a pairs row of 5,632 (the raw
    # 470-item corpus) above an items row of 463, under a caption saying both columns drop the 7.
    # The unfiltered corpus is kept for `rel_control` below, whose whole point is to reproduce the
    # PUBLISHED split-half values exactly.
    all_pc = C.filter_per_cell(models, names, gate["per_cell"], gate["keep"]["all"])
    halves_pub = parity_cells(models, leaves)
    halves_all = parity_cells(models, leaves, gate["keep"]["all"])
    halves_clean = parity_cells(models, leaves, gate["keep"]["clean"])
    return {
        "all": {"diag": diagnostics(models, leaves, all_pc),
                "cons": conservative_block(models, leaves, published_cells, frontier),
                "rel": reliability_rows(models, active_all, halves_all)},
        "clean": {"diag": diagnostics(models, leaves, clean_pc),
                  "cons": conservative_block(models, leaves, gate["cells_clean"], frontier),
                  "rel": reliability_rows(models, active_clean, halves_clean)},
        "rel_same_leaves": reliability_rows(models, active_all, halves_clean),
        "rel_control": reliability_control(reliability_rows(models, active_all, halves_pub),
                                           config.PAPER_ROOT / "out" / "tables" /
                                           "split_half_reliability.csv"),
        "per_cell_clean": clean_pc}


def median_reliability(rows: List[Dict[str, Any]]) -> Optional[float]:
    return _median([r["r_full"] for r in rows])


def selftest() -> str:
    """Prove the median helper on the cases that break naive implementations, since every
    reliability and ratio headline in the audit is read off it."""
    assert _median([1.0, 2.0, 3.0]) == 2.0, "odd-length median"
    assert _median([1.0, 2.0, 3.0, 4.0]) == 2.5, "even-length median must interpolate"
    assert _median([3.0, 1.0, 2.0]) == 2.0, "the median must sort first"
    assert _median([None, 2.0, None]) == 2.0, "undefined entries must be dropped, not counted as 0"
    assert _median([None, None]) is None, "an all-undefined vector must be None, never 0.0"
    return "contam_recompute selftest PASS - median exact on odd/even/unsorted/None/all-None"
